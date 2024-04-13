import asyncio
import hashlib
import json
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from urllib.parse import quote

import pybfbc2stats
from pybfbc2stats.asyncio_client import AsyncClient
from pybfbc2stats.constants import LookupType
from pybfbc2stats.packet import Packet

from app import config
from app.cache import RedisClient
from app.config import (
    CLIENT_USERNAME,
    CLIENT_PASSWORD,
    CACHE_TTL_PERSONAS_BY_NAME,
    CLIENT_MAX_RETRIES,
    CACHE_TTL_PERSONAS_BY_ID,
)
from app.constants import (
    ApiNamespace,
    ApiPlatform,
    StatsKeySet,
    STATS_KEY_SETS,
    LEADERBOARD_PAGE_SIZE,
    LeaderboardSortKey,
    IdentifierType,
    FeslNamespace,
    MAINTAIN_PLAYER_IDS,
    DUMMY_TID,
    FeslPlatform,
    TheaterPlatform,
)
from app.exceptions import (
    PlayerNotFoundException,
    DataSourceException,
    NoPersonasException,
    TooManyPersonasException,
)
from app.utility import clean_string_value, clean_server_details
from app.singleton import Singleton


@dataclass
class ClientInstance:
    client: AsyncClient
    busy: bool = False
    last_used: datetime = datetime.min


class FeslClientInstance(ClientInstance):
    client: pybfbc2stats.AsyncFeslClient


class TheaterClientInstance(ClientInstance):
    client: pybfbc2stats.AsyncTheaterClient


class EaApiClient(metaclass=Singleton):
    timeout: float
    platforms: List[ApiPlatform]
    instances: Dict[ApiPlatform, ClientInstance]
    logger: logging.Logger

    initialized: bool = False

    def __init__(self, platforms: List[ApiPlatform], timeout: float = 3.0):
        self.platforms = platforms
        self.timeout = timeout
        self.logger = logging.getLogger(self.__class__.__name__)

    async def initialize(
        self,
    ) -> None:
        self.instances = {}
        for platform in self.platforms:
            self.instances[platform] = await self.create_instance(platform)
        self.initialized = True

    async def create_instance(self, platform: ApiPlatform) -> ClientInstance:
        pass

    async def shutdown_instance(self, instance: ClientInstance) -> None:
        pass

    async def get_instance(
        self, platform: ApiPlatform, replace_permanent: bool = False
    ) -> ClientInstance:
        if not self.initialized:
            await self.initialize()

        # Get default client or create temporary one
        if replace_permanent:
            self.logger.warning(
                f"Creating new permanent {platform} client instance to replace existing one"
            )
            instance = await self.create_instance(platform)
        elif self.instances[platform].busy:
            self.logger.warning(
                f"Clients exhausted, creating new (temporary) {platform} client instance"
            )
            instance = await self.create_instance(platform)
        else:
            instance = self.instances[platform]
            # Mark client as busy
            instance.busy = True

        return instance

    async def return_instance(
        self, instance: ClientInstance, encountered_error: bool = False
    ) -> None:
        shutdown_given_instance = False
        if instance not in self.instances.values():
            # Returned client instance is temporary, logoff and close connection (error flag safe to ignore)
            shutdown_given_instance = True
        else:
            # Returned client instance is permanent, check renew on error
            index = list(self.instances.values()).index(instance)
            platform = list(self.instances.keys())[index]
            if encountered_error:
                # There was an error with the client instance => replace it
                self.instances[platform] = await self.get_instance(platform, True)
                shutdown_given_instance = True
            # Mark permanent client as non-busy and update last used timestamp
            instance.busy = False
            instance.last_used = datetime.now()

        if shutdown_given_instance:
            # Attempt to shut down old client
            try:
                await self.shutdown_instance(instance)
            except pybfbc2stats.Error:
                pass

    async def maintain_instances(self) -> None:
        if not self.initialized:
            await self.initialize()

        self.logger.debug("Running client instance maintenance")
        for platform, instance in self.instances.items():
            if datetime.now() - instance.last_used < timedelta(
                seconds=config.CLIENT_PING_INTERVAL
            ):
                self.logger.debug(
                    f"Client instance for {platform} has been used recently, skipping maintenance"
                )
                continue

            self.logger.debug(
                f"Waiting for {platform} client instance to become available"
            )
            # Wait for client to become available
            while instance.busy:
                await asyncio.sleep(0.1)

            # Mark client as busy
            self.logger.debug(f"Marking {platform} client instance as busy")
            instance.busy = True

            # Run client's keepalive method
            self.logger.debug(f"Running {platform} client instance's keepalive method")
            encountered_error = False
            try:
                await self.instance_keepalive(instance, platform)
            except pybfbc2stats.Error as e:
                self.logger.warning(
                    f"Encountered an error during {platform} client instance maintenance keepalive"
                )
                self.logger.debug(e)
                encountered_error = True
            except Exception as e:
                # Log to error since pybfbc2stats should handle all errors
                self.logger.error(
                    f"Encountered an error during {platform} client instance maintenance keepalive",
                    e,
                )
                encountered_error = True

            # Use common method to return client (and replace it on error)
            self.logger.debug(
                f"Completed {platform} client instance maintenance "
                f'{"with" if encountered_error else "without"} errors, returning client instance'
            )
            await self.return_instance(instance, encountered_error)

    @staticmethod
    async def instance_keepalive(
        instance: ClientInstance, platform: ApiPlatform
    ) -> None:
        pass


class FeslApiClient(EaApiClient):
    instances: Dict[ApiPlatform, FeslClientInstance]

    def __init__(self, timeout: float = 3.0):
        super().__init__(
            [FeslPlatform.pc, FeslPlatform.ps3, FeslPlatform.xbox360], timeout
        )

    async def create_instance(self, platform: ApiPlatform) -> FeslClientInstance:
        return FeslClientInstance(
            pybfbc2stats.AsyncFeslClient(
                CLIENT_USERNAME,
                CLIENT_PASSWORD,
                pybfbc2stats.Platform[platform],
                timeout=self.timeout,
            )
        )

    async def shutdown_instance(self, instance: FeslClientInstance) -> None:
        await instance.client.logout()
        await instance.client.connection.close()

    async def get_instance(
        self, platform: ApiPlatform, replace_permanent: bool = False
    ) -> FeslClientInstance:
        return await super().get_instance(platform, replace_permanent)

    @staticmethod
    async def instance_keepalive(
        instance: FeslClientInstance, platform: ApiPlatform
    ) -> None:
        await instance.client.get_stats(MAINTAIN_PLAYER_IDS[platform], [b"kills"])

    async def get_json(
        self, platform: ApiPlatform, packet: Packet, list_entry_prefix: bytes
    ) -> List[dict]:
        data = None
        attempt = 0
        while data is None and attempt < CLIENT_MAX_RETRIES:
            instance = await self.get_instance(platform)
            # Set correct transaction id on packet
            tid = instance.client.get_transaction_id()
            packet.set_tid(tid)
            encountered_error = False
            try:
                # Will either send login or do nothing if client instance is a permanent one
                await instance.client.login()
                await instance.client.connection.write(packet)
                raw_response = await instance.client.get_complex_response(tid)
                data, *_ = instance.client.parse_list_response(
                    raw_response, list_entry_prefix
                )
            except pybfbc2stats.ConnectionError as e:
                # Set error flag
                encountered_error = True
                # Increase attempt counter
                attempt += 1
            finally:
                # Return client instance (and replace it on error)
                await self.return_instance(instance, encountered_error)

        if data is None:
            raise DataSourceException(
                "All attempts to retrieve data from source failed"
            )

        return data

    async def get_json_cached(
        self,
        platform: ApiPlatform,
        packet: Packet,
        list_parse_prefix: bytes,
        ttl: int = config.CACHE_TTL_DEFAULT,
        additional_cache_key_elements: List[str] = None,
    ) -> List[dict]:
        sha256_hash = hashlib.sha256()
        sha256_hash.update(bytes(packet))
        cache_key = f"packet:{sha256_hash.hexdigest()}"
        # Add any additional elements to the cache key
        if additional_cache_key_elements is not None:
            cache_key += ":" + ":".join(additional_cache_key_elements)

        redis_client = RedisClient()
        cached_data = await redis_client.get_from_cache(cache_key)
        if cached_data is not None:
            data = json.loads(cached_data)
        else:
            data = await self.get_json(platform, packet, list_parse_prefix)

            cacheable_data = json.dumps(data)
            await redis_client.set_to_cache(cache_key, cacheable_data, ttl)

        return data

    async def find_persona_by_identifiers(
        self,
        identifiers: List[str],
        identifier_type: IdentifierType,
        namespace: ApiNamespace,
    ) -> Optional[List[dict]]:
        # Most IDEs will show a type error (which is correct),
        # but passing bytes works the same since Namespace is a bytes Enum
        fesl_namespace = FeslNamespace[namespace]
        quoted = [quote(identifier) for identifier in identifiers]
        packet = pybfbc2stats.AsyncFeslClient.build_user_lookup_packet(
            DUMMY_TID, quoted, bytes(fesl_namespace), LookupType[identifier_type]
        )
        # Use whichever platform has a client available (defaulting to pc if all are busy)
        platform = next(
            (key for (key, instance) in self.instances.items() if not instance.busy),
            FeslPlatform.pc,
        )
        results = await self.get_json_cached(platform, packet, b"userInfo.")

        relevant_results = [
            r
            for r in results
            if r.get("userId") is not None
            and r.get("userName") is not None
            and r.get("namespace") == fesl_namespace.name
        ]
        if len(relevant_results) > 0:
            return [
                {
                    "pid": int(r["userId"]),
                    "name": clean_string_value(r["userName"]),
                    "namespace": r["namespace"],
                    "oid": int(r["masterUserId"]),
                    "xuid": int(r["xuid"]) if "xuid" in r else None,
                }
                for r in relevant_results
            ]

    async def search_persona_name(
        self, name: str, namespace: ApiNamespace
    ) -> List[dict]:
        # Most IDEs will show a type error (which is correct),
        # but passing bytes works the same since Namespace is a bytes Enum
        fesl_namespace = FeslNamespace[namespace]
        packet = pybfbc2stats.AsyncFeslClient.build_search_packet(
            DUMMY_TID, quote(name), bytes(fesl_namespace)
        )
        # Use whichever platform has a client instance available (defaulting to pc if all are busy)
        platform = next(
            (key for (key, instance) in self.instances.items() if not instance.busy),
            FeslPlatform.pc,
        )
        results = await self.get_json_cached(
            platform, packet, b"users.", ttl=config.CACHE_TTL_PERSONA_SEARCH
        )

        if len(results) > 0:
            personas = [
                {"pid": int(r["id"]), "name": clean_string_value(r["name"])}
                for r in results
            ]
        else:
            personas = []

        return personas

    async def get_persona_stats(
        self, player_id: int, platform: FeslPlatform, key_set: StatsKeySet
    ) -> dict:
        cache_key = f"stats:{player_id}:{platform}:{key_set}"

        redis_client = RedisClient()
        cached_data = await redis_client.get_from_cache(cache_key)
        if cached_data is not None:
            data = json.loads(cached_data)
        else:
            data = None
            attempt = 0
            while data is None and attempt < CLIENT_MAX_RETRIES:
                instance = await self.get_instance(platform)
                encountered_error = False
                try:
                    # Will either send login or do nothing if client instance is a permanent one
                    await instance.client.login()
                    data = await instance.client.get_stats(
                        player_id, STATS_KEY_SETS[key_set]
                    )
                except pybfbc2stats.ConnectionError as e:
                    encountered_error = True
                finally:
                    await self.return_instance(instance, encountered_error)

            if data is None:
                raise DataSourceException(
                    "All attempts to retrieve data from source failed"
                )

            cacheable_data = json.dumps(data)
            await redis_client.set_to_cache(cache_key, cacheable_data)

        return data

    async def get_leaderboard(
        self,
        platform: FeslPlatform,
        min_rank: int,
        max_rank: int,
        sort_by: LeaderboardSortKey,
    ) -> List[dict]:
        packet = pybfbc2stats.AsyncFeslClient.build_leaderboard_query_packet(
            DUMMY_TID,
            min_rank,
            max_rank,
            sort_by.encode("utf8"),
            pybfbc2stats.DEFAULT_LEADERBOARD_KEYS,
        )
        # Leaderboard packets do not reference the platform => add platform as additional cache key
        parsed_response = await self.get_json_cached(
            platform, packet, b"stats.", additional_cache_key_elements=[str(platform)]
        )
        # Turn sub lists into dicts and return result
        leaderboard = [
            {
                key: pybfbc2stats.AsyncFeslClient.dict_list_to_dict(value)
                if isinstance(value, list)
                else value
                for (key, value) in persona.items()
            }
            for persona in parsed_response
        ]

        # Cleanup usernames
        for persona in leaderboard:
            persona["name"] = clean_string_value(persona["name"])

        return leaderboard


class TheaterApiClient(EaApiClient):
    instances: Dict[ApiPlatform, TheaterClientInstance]

    def __init__(self, timeout: float = 5.0):
        super().__init__([TheaterPlatform.pc, TheaterPlatform.ps3], timeout)

    async def create_instance(self, platform: ApiPlatform) -> TheaterClientInstance:
        # Get theater details from FESL (not using existing client instance, since the lkey needs to be "fresh")
        fesl_instance = await FeslApiClient().create_instance(platform)
        host, port = await fesl_instance.client.get_theater_details()
        lkey = await fesl_instance.client.get_lkey()

        return TheaterClientInstance(
            pybfbc2stats.AsyncTheaterClient(
                host, port, lkey, pybfbc2stats.Platform[platform], timeout=self.timeout
            )
        )

    async def shutdown_instance(self, instance: TheaterClientInstance) -> None:
        await instance.client.connection.close()

    async def get_instance(
        self, platform: ApiPlatform, replace_permanent: bool = False
    ) -> TheaterClientInstance:
        return await super().get_instance(platform, replace_permanent)

    @staticmethod
    async def instance_keepalive(
        instance: TheaterClientInstance, platform: ApiPlatform
    ) -> None:
        await instance.client.get_lobbies()

    async def get_servers(self, platform: TheaterPlatform) -> List[dict]:
        cache_key = f"servers:{platform}"

        redis_client = RedisClient()
        cached_data = await redis_client.get_from_cache(cache_key)
        if cached_data is not None:
            servers = json.loads(cached_data)
        else:
            servers = None
            attempt = 0
            while servers is None and attempt < CLIENT_MAX_RETRIES:
                instance = await self.get_instance(platform)
                encountered_error = False
                try:
                    lobbies = await instance.client.get_lobbies()

                    # Fetch server ids from lobbies
                    servers = []
                    for lobby in lobbies:
                        lobby_servers = await instance.client.get_servers(
                            int(lobby["LID"])
                        )
                        servers.extend(lobby_servers)
                except pybfbc2stats.ConnectionError as e:
                    self.logger.error(
                        f"Failed to retrieve server list from theater "
                        f"(attempt {attempt + 1}/{CLIENT_MAX_RETRIES})"
                    )
                    self.logger.debug(e)
                    encountered_error = True
                    attempt += 1
                finally:
                    await self.return_instance(instance, encountered_error)

            if servers is None:
                raise DataSourceException("Failed to retrieve server list from theater")

            # Clean up server entries (clean up strings, remove obsolete details, ...)
            servers = [clean_server_details(server) for server in servers]

            # Sort server list by lobby and game id
            servers.sort(key=lambda x: x["LID"] + x["GID"])

            # Cache server list
            cacheable_data = json.dumps(servers)
            await redis_client.set_to_cache(
                cache_key, cacheable_data, config.CACHE_TTL_SERVERS
            )

        return servers

    async def get_server(
        self, platform: TheaterPlatform, lobby_id: int, game_id: int
    ) -> dict:
        cache_key = f"server:{platform}:{lobby_id}:{game_id}"
        return await self.get_gdat(
            cache_key,
            platform,
            lid=str(lobby_id).encode("utf8"),
            gid=str(game_id).encode("utf8"),
        )

    async def get_current_server(
        self,
        platform: TheaterPlatform,
        persona_name: str = None,
        persona_id: int = None,
    ) -> dict:
        if persona_name is None and persona_id is None:
            raise ValueError("Either a persona name or persona id must be provided")

        if platform is TheaterPlatform.pc:
            namespace = ApiNamespace.battlefield
        else:
            namespace = ApiNamespace.psn

        if persona_id is None:
            personas = await get_personas(namespace, [persona_name])
            persona = personas.pop()
        else:
            persona = {"pid": persona_id}

        cache_key = f'server:{platform}:{persona["pid"]}'
        return await self.get_gdat(
            cache_key, platform, uid=str(persona["pid"]).encode("utf8")
        )

    async def get_gdat(
        self, cache_key: str, platform: TheaterPlatform, **kwargs: bytes
    ) -> dict:
        redis_client = RedisClient()
        cached_data = await redis_client.get_from_cache(cache_key)
        if cached_data is not None:
            server = json.loads(cached_data)
        else:
            server = None
            attempt = 0
            while server is None and attempt < CLIENT_MAX_RETRIES:
                instance = await self.get_instance(platform)
                encountered_error = False
                try:
                    general, detailed, players = await instance.client.get_gdat(
                        **kwargs
                    )
                    server = {**general, **detailed, "D-Players": players}
                except pybfbc2stats.ConnectionError as e:
                    self.logger.error(
                        f"Failed to retrieve server details from theater"
                        f"(attempt {attempt + 1}/{CLIENT_MAX_RETRIES})"
                    )
                    self.logger.debug(e)
                    encountered_error = True
                    attempt += 1
                finally:
                    await self.return_instance(instance, encountered_error)

            if server is None:
                raise DataSourceException(
                    "Failed to retrieve server details from theater"
                )

            server = clean_server_details(server)

            cacheable_data = json.dumps(server)
            await redis_client.set_to_cache(
                cache_key, cacheable_data, config.CACHE_TTL_SERVERS
            )

        return server


async def get_personas(
    namespace: ApiNamespace,
    persona_names: List[str] = None,
    persona_ids: List[int] = None,
) -> List[dict]:
    client = FeslApiClient()
    redis_client = RedisClient()
    if persona_names is not None:
        identifiers = [persona_name.lower() for persona_name in persona_names]
        identifier_type = IdentifierType.playerName
    elif persona_ids is not None:
        identifiers = [str(persona_id) for persona_id in persona_ids]
        identifier_type = IdentifierType.playerId
    else:
        raise ValueError("Either a persona name or persona id must be provided")

    if len(identifiers) == 0:
        raise NoPersonasException("No persona names/ids to look up")
    elif len(identifiers) > config.MULTI_LOOKUP_MAX_PERSONAS:
        raise TooManyPersonasException("Too many persona names/ids to look up")

    # Attempt to fetch personas from cache
    cache_keys = [
        f"persona:{namespace}:{identifier_type}:{identifier}"
        for identifier in identifiers
    ]
    cached_personas = await redis_client.get_multiple_from_cache(cache_keys)

    # Check whether we need look up any personas or we can serve entirely from cache
    identifiers_to_lookup = []
    personas_from_cache = [json.loads(cp) for cp in cached_personas if cp is not None]
    if 0 < len(personas_from_cache) < len(identifiers):
        # Some personas were found in cache, determine which identifiers still need to be looked up
        if identifier_type == IdentifierType.playerName:
            identifiers_to_lookup = list(
                set(identifiers)
                - set([fc["name"].lower() for fc in personas_from_cache])
            )
        else:
            identifiers_to_lookup = list(
                set(identifiers) - set([str(fc["pid"]) for fc in personas_from_cache])
            )
    elif len(personas_from_cache) == 0:
        # None of the personas was found in cache, look all up now
        identifiers_to_lookup = identifiers

    # Look up any missing personas
    personas_from_fesl = []
    if len(identifiers_to_lookup) > 0:
        results = await client.find_persona_by_identifiers(
            identifiers_to_lookup, identifier_type, namespace
        )

        if results is None and len(personas_from_cache) == 0:
            # Raise exception if no personas could be retrieved via FESL and none were found in cache
            raise PlayerNotFoundException("No persona found with given persona name/id")
        elif results is not None:
            # Create cacheable mapping dicts
            name_keyed_mapping = {
                f'persona:{persona["namespace"]}:{IdentifierType.playerName}:{persona["name"].lower()}': json.dumps(
                    persona
                )
                for persona in results
            }
            id_keyed_mapping = {
                f'persona:{persona["namespace"]}:{IdentifierType.playerId}:{persona["pid"]}': json.dumps(
                    persona
                )
                for persona in results
            }

            await redis_client.set_multiple_to_cache(
                name_keyed_mapping, CACHE_TTL_PERSONAS_BY_NAME
            )
            # Don't cache personas by their id as long to allow player name changes to be reflected earlier
            await redis_client.set_multiple_to_cache(
                id_keyed_mapping, CACHE_TTL_PERSONAS_BY_ID
            )

            personas_from_fesl = results

    return sorted([*personas_from_cache, *personas_from_fesl], key=lambda d: d["name"])


async def search_persona_name(namespace: ApiNamespace, persona_name: str) -> List[dict]:
    client = FeslApiClient()
    return await client.search_persona_name(persona_name, namespace)


async def get_stats(
    platform: FeslPlatform,
    key_set: StatsKeySet,
    persona_name: str = None,
    persona_id: int = None,
) -> dict:
    if persona_name is None and persona_id is None:
        raise ValueError("Either a persona name or persona id must be provided")

    client = FeslApiClient()

    if platform is FeslPlatform.pc:
        namespace = ApiNamespace.battlefield
    elif platform is FeslPlatform.ps3:
        namespace = ApiNamespace.psn
    else:
        namespace = ApiNamespace.xbl

    if persona_id is None:
        personas = await get_personas(namespace, [persona_name])
        persona = personas.pop()
    else:
        persona = {"pid": persona_id}

    stats = await client.get_persona_stats(persona["pid"], platform, key_set)

    return stats


async def get_leaderboard(
    platform: FeslPlatform, page: int, sort_by: LeaderboardSortKey
) -> List[dict]:
    min_rank = (page - 1) * LEADERBOARD_PAGE_SIZE + 1
    max_rank = page * LEADERBOARD_PAGE_SIZE
    client = FeslApiClient()
    return await client.get_leaderboard(platform, min_rank, max_rank, sort_by)


async def get_servers(platform: TheaterPlatform) -> List[dict]:
    theater_client = TheaterApiClient()
    return await theater_client.get_servers(platform)


async def get_server(platform: TheaterPlatform, lobby_id: int, game_id: int) -> dict:
    theater_client = TheaterApiClient()
    return await theater_client.get_server(platform, lobby_id, game_id)


async def get_current_server(
    platform: TheaterPlatform, persona_name: str = None, persona_id: int = None
) -> dict:
    theater_client = TheaterApiClient()
    return await theater_client.get_current_server(platform, persona_name, persona_id)
