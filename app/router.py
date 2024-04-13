from typing import List

from fastapi import APIRouter, Path, Query, Body

from app import config
from app.constants import (
    ApiNamespace,
    StatsKeySet,
    LEADERBOARD_PAGE_SIZE,
    LeaderboardSortKey,
    FeslPlatform,
    TheaterPlatform,
)
from app.fetch import (
    get_personas,
    get_stats,
    get_leaderboard,
    search_persona_name,
    get_servers,
    get_server,
    get_current_server,
)
from app.utility import CacheableJSONResponse

# Anyone requesting .../[endpoint]/ instead of just .../[endpoint] would get redirected to .../[endpoint],
# potentially leaking a CDN origin domain in the 307 redirect header => disable slash redirects
router = APIRouter(redirect_slashes=False)


@router.get(
    "/persona/{namespace}/by-name/{persona_name}",
    summary="Find a persona/player in a given namespace based on their name",
    tags=["Persona resolution"],
)
async def r_get_persona_by_name(
    namespace: ApiNamespace = Path(
        ...,
        description="Namespace/platform of the persona/player (most namespaces are "
        "also available under aliases, for example: pc = cem_ea_id)",
    ),
    persona_name: str = Path(
        ..., description="Name of the persona/player", example="Krut0r"
    ),
):
    personas = await get_personas(namespace, persona_names=[persona_name])
    return CacheableJSONResponse(
        content=personas.pop(), max_age=config.CACHE_MAX_AGE_PERSONAS
    )


@router.get(
    "/persona/{namespace}/by-id/{persona_id}",
    summary="Find a persona/player in a given namespace based on their (persona) id",
    tags=["Persona resolution"],
)
async def r_get_persona_by_id(
    namespace: ApiNamespace = Path(
        ...,
        description="Namespace/platform of the persona/player (most namespaces are "
        "also available under aliases, for example: pc = cem_ea_id)",
    ),
    persona_id: int = Path(
        ..., description="Id of the persona/player", example=315923098
    ),
):
    personas = await get_personas(namespace, persona_ids=[persona_id])
    return CacheableJSONResponse(
        content=personas.pop(), max_age=config.CACHE_MAX_AGE_PERSONAS
    )


@router.get(
    "/persona/{namespace}/search-name/{persona_name}",
    summary="Find personas/players in a given namespace based on a (partial) name",
    description="You can use * as a trailing wildcard, <strong>but:</strong> the FESL backend returns an error both if "
    "a) no matching results were found or b) too many matching results were found.",
    tags=["Persona resolution"],
)
async def r_get_persona_search_name(
    namespace: ApiNamespace = Path(..., description="Namespace to search in"),
    persona_name: str = Path(..., description="Name to search for", example="Krut0r"),
):
    results = await search_persona_name(namespace, persona_name)
    content = {"query": persona_name, "namespace": namespace, "results": results}
    return CacheableJSONResponse(
        content=content, max_age=config.CACHE_MAX_AGE_PERSONA_SEARCH
    )


@router.post(
    "/personas/{namespace}/by-names",
    summary=f"Find multiple personas/players in a given namespace based on their names "
    f"(min: 1, max: {config.MULTI_LOOKUP_MAX_PERSONAS})",
    tags=["Persona resolution"],
)
async def r_post_personas_by_names(
    namespace: ApiNamespace = Path(
        ...,
        description="Namespace/platform of the persona/player (most namespaces are "
        "also available under aliases, for example: pc = cem_ea_id)",
    ),
    persona_names: List[str] = Body(
        ...,
        description=f"JSON list of 1-{config.MULTI_LOOKUP_MAX_PERSONAS} persona names",
        example=["Krut0r", "Mr.249", "jackfrags"],
    ),
):
    personas = await get_personas(namespace, persona_names=list(set(persona_names)))
    return CacheableJSONResponse(
        content=personas, max_age=config.CACHE_MAX_AGE_PERSONAS
    )


@router.post(
    "/personas/{namespace}/by-ids",
    summary=f"Find multiple personas/players in a given namespace based on their (persona) ids "
    f"(min: 1, max: {config.MULTI_LOOKUP_MAX_PERSONAS})",
    tags=["Persona resolution"],
)
async def r_post_personas_by_ids(
    namespace: ApiNamespace = Path(
        ...,
        description="Namespace/platform of the persona/player (most namespaces are "
        "also available under aliases, for example: pc = cem_ea_id)",
    ),
    persona_ids: List[int] = Body(
        ...,
        description=f"JSON List of 1-{config.MULTI_LOOKUP_MAX_PERSONAS} persona ids",
        example=[315923098, 1985055004, 873707483],
    ),
):
    personas = await get_personas(namespace, persona_ids=list(set(persona_ids)))
    return CacheableJSONResponse(
        content=personas, max_age=config.CACHE_MAX_AGE_PERSONAS
    )


@router.get(
    "/stats/{platform}/by-name/{persona_name}",
    summary="Get stats for a persona/player on a given platform based on their name",
    tags=["Battlefield: Bad Company 2 stats"],
)
async def r_get_stats_by_name(
    platform: FeslPlatform = Path(..., description="Platform of the persona/player"),
    persona_name: str = Path(
        ..., description="Name of the persona/player", example="Krut0r"
    ),
    key_set: StatsKeySet = Query(
        StatsKeySet.default, description="Set of data keys/points to fetch"
    ),
):
    stats = await get_stats(platform, key_set, persona_name=persona_name)
    return CacheableJSONResponse(content=stats)


@router.get(
    "/stats/{platform}/by-id/{persona_id}",
    summary="Get stats for a persona/player on a given platform based on their (persona) id",
    tags=["Battlefield: Bad Company 2 stats"],
)
async def r_get_stats_by_id(
    platform: FeslPlatform = Path(..., description="Platform of persona/player"),
    persona_id: int = Path(
        ..., description="Id of the persona/player", example=315923098
    ),
    key_set: StatsKeySet = Query(
        StatsKeySet.default, description="Set of data keys/points to fetch"
    ),
):
    stats = await get_stats(platform, key_set, persona_id=persona_id)
    return CacheableJSONResponse(content=stats)


@router.get(
    "/leaderboard/{platform}/{sort_by}/{page}",
    summary="Get a page of the leaderboard for a given platform",
    tags=["Battlefield: Bad Company 2 stats"],
)
async def r_get_leaderboard(
    platform: FeslPlatform = Path(..., description="Platform to get leaderboard for"),
    sort_by: LeaderboardSortKey = Path(..., description="Attribute to sort players by"),
    page: int = Path(
        ...,
        ge=1,
        le=5000,
        description=f"Which page of the leaderboard to return "
        f"(each page contains {LEADERBOARD_PAGE_SIZE} entries)",
        example=1,
    ),
):
    leaderboard = await get_leaderboard(platform, page, sort_by)
    return CacheableJSONResponse(content=leaderboard)


@router.get(
    "/servers/{platform}",
    summary=f"Get the available servers for a given platform",
    tags=["Battlefield: Bad Company 2 servers"],
)
async def r_get_servers(
    platform: TheaterPlatform = Path(..., description="Platform to get server list for")
):
    servers = await get_servers(platform)
    return CacheableJSONResponse(content=servers, max_age=config.CACHE_MAX_AGE_SERVERS)


@router.get(
    "/servers/{platform}/{lobby_id}/{game_id}",
    summary="Get details and currently active players for a given game (server) id from a given lobby id",
    tags=["Battlefield: Bad Company 2 servers"],
)
async def r_get_server(
    platform: TheaterPlatform = Path(..., description="Platform of the game server"),
    lobby_id: int = Path(
        ..., description="Id of the lobby the server is from (LID)", example=257
    ),
    game_id: int = Path(..., description="Id of the game server (GID)", example=119168),
):
    server = await get_server(platform, lobby_id, game_id)
    return CacheableJSONResponse(content=server, max_age=config.CACHE_MAX_AGE_SERVERS)


@router.get(
    "/servers/{platform}/current/by-name/{persona_name}",
    summary="Get details and currently active players for a given persona's/player's current server "
    "based on their name",
    description="This endpoint returns details about the server a persona/player is currently playing on. If the "
    "persona does not exist or is not currently playing online, it returns a 404 Not Found error.",
    tags=["Battlefield: Bad Company 2 servers"],
)
async def r_get_current_server_by_name(
    platform: TheaterPlatform = Path(..., description="Platform of the game server"),
    persona_name: str = Path(
        ..., description="Name of the persona/player", example="Krut0r"
    ),
):
    server = await get_current_server(platform, persona_name=persona_name)
    return CacheableJSONResponse(content=server, max_age=config.CACHE_MAX_AGE_SERVERS)


@router.get(
    "/servers/{platform}/current/by-id/{persona_id}",
    summary="Get details and currently active players for a given persona's/player's current server "
    "based on their id",
    description="This endpoint returns details about the server a persona/player is currently playing on. If the "
    "persona does not exist or is not currently playing online, it returns a 404/Not found error.",
    tags=["Battlefield: Bad Company 2 servers"],
)
async def r_get_current_server_by_name(
    platform: TheaterPlatform = Path(..., description="Platform of the game server"),
    persona_id: int = Path(
        ..., description="Id of the persona/player", example=315923098
    ),
):
    server = await get_current_server(platform, persona_id=persona_id)
    return CacheableJSONResponse(content=server, max_age=config.CACHE_MAX_AGE_SERVERS)
