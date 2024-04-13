import argparse
import json

from app.constants import ApiNamespace

GAMES = ['bfbc2', 'bf3', 'bf4', 'bfh', 'bf1', 'bfv']

parser = argparse.ArgumentParser('Group players into sets to generate test data for bulk persona lookups')
parser.add_argument('--games', help='Games to generate test sets for', nargs='+', choices=GAMES, default=GAMES)
parser.add_argument('--namespaces', help='Namespaces to generate test sets for', nargs='+',
                    choices=list(ApiNamespace), default=list(ApiNamespace))
parser.add_argument('--set-size', help='Number of personas to group into one test data set', type=int, default=30)
parser.add_argument('--max-sets', help='Maximum number of test data sets to generate (per game, platform and language)',
                    type=int, default=12)
args = parser.parse_args()

players = []
for game in args.games:
    with open(f'../tests/players/{game}.json', 'r') as playerFile:
        players.extend(json.load(playerFile))

testData = []
for game in args.games:
    for namespace in args.namespaces:
        usePlayers = [p for p in players if p['game'] == game and p['namespace'] == namespace]
        for i in range(0, len(usePlayers), args.set_size):
            setPlayers = usePlayers[i:i + args.set_size]
            testData.append({
                'namespace': namespace,
                'names': [p['name'] for p in setPlayers],
                'pids': [p['pid'] for p in setPlayers]
            })

with open('../tests/multi-persona-lookup-test-data-sets-generated.json', 'w') as testDataFile:
    json.dump(testData, testDataFile, indent=2)
