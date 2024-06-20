'''
this module is responsible for creating table of results
updating ,and inserting data in to te table in the database 
'''


import sys,os

# Ensure the backend directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import kisa_utils as kutils


# with kutils.db.Api() as db:
    
#     pass


def addMatchResultsToDb(matchResults: dict) -> dict:
    '''
        This function handles the addition of team results into tableOfResults.
        @param matchResults: 'entryId', 'leagueId', 'matchId', 'homeTeam', 'awayTeam', 'homeScore', 'awayScore',
                             'others' and 'timestamp' are the expected keys.
    '''
    dbPath = kutils.config.getValue('smsDb/rootPath')
    dbName = kutils.config.getValue('smsDb/tables')
    from backend.tableOfStandings.db import updateGoalDifference, updateGoalsFor, updateGoalsAgainst, updatePoints, updateWinDrawLoss

    entryId = matchResults['entryId']
    leagueId = matchResults['leagueId']
    timestamp = matchResults['timestamp']
    matchId = matchResults['matchId']
    homeTeam = matchResults['homeTeam']
    awayTeam = matchResults['awayTeam']
    homeScore = matchResults['homeScore']
    awayScore = matchResults['awayScore']
    matchDate = matchResults['matchDate']
    others = matchResults['others']
    teams = ['homeTeam', 'awayTeam']
    
    print(f'Database path: {dbPath}, Database name: {dbName}')
    print(f'Match Results: {matchResults}')
    
    with kutils.db.Api(dbPath, dbName, readonly=False) as db:
        for team in teams:
            teamName = matchResults[team]
            print(f'Checking team: {teamName} in league: {matchResults["leagueId"]}')
            
            # Check if the team exists in the database
            fetchResults = db.fetch(
                'teams',
                ['teamName'],
                'teamName=? and leagueId=?',
                [teamName, matchResults['leagueId']],
                limit=1,
                returnDicts=True,
                returnNamespaces=False,
                parseJson=False,
                returnGenerator=False
            )
            print(f'Fetch results for {teamName}: {fetchResults}')
            
            if not fetchResults:
                return {
                    'status': False,
                    'log': f'{teamName} does not exist'
                }

        insertResults = db.insert(
            'tableOfResults', [entryId, leagueId, timestamp, matchId, homeTeam, awayTeam, homeScore, awayScore, matchDate, others]
        )
        print(f'Insert results: {insertResults}')

    if insertResults['status']:
        updateFunctions = [
            updateWinDrawLoss(matchResults), updateGoalDifference(matchResults), updatePoints(matchResults),
            updateGoalsFor(matchResults), updateGoalsAgainst(matchResults)
        ]
        
        for updateFunction in updateFunctions:
            print('Update function result:', updateFunction)
            if not updateFunction['status']:
                return {
                    'status': False, 'log': f'{updateFunction} failed to update table of standings'
                }
        return {
            'status': True, 'log': ''
        }
    
    return insertResults

def fetchAllMatches():
    dbPath = kutils.config.getValue('smsDb/rootPath')
    dbName = kutils.config.getValue('smsDb/tables')
    with kutils.db.Api(dbPath,dbName, readonly=True) as db:
        fetchResults = db.fetch(
            'tableOfResults',
            ['*'],
            '',
            [],
            limit= 100,
            returnDicts=False,
            returnNamespaces=False,
            parseJson=False,
            returnGenerator=False
        )
        return fetchResults

def init():
    defaults = {
        'rootPath':'/tmp/sms',
        'dbName':'sms.db',
        'tables':{
            "tableOfResults":'''
                                entryId         varchar(32) not null,
                                leagueId        varchar(32) not null,
                                timestamp       varchar(32) not null,
                                matchId         varchar(32) not null,
                                homeTeam        varchar(32) not null,
                                awayTeam        varchar(32) not null,
                                homeScore       varchar(32) not null,
                                awayScore       varchar(32) not null,
                                matchDate       varchar(32) not null,
                                others          json,
                                FOREIGN KEY (leagueId) REFERENCES leagues (leagueId)
                                
            
            '''
        }
    }
    defaults['dbPath'] = defaults['rootPath']+"/db/"+defaults["dbName"]
    config_topic = "smsDb"
    
    for key in defaults:
        if 1 or not kutils.config.setValue(config_topic + "/" + key):
            kutils.config.setValue(config_topic + "/" + key , defaults[key])
    
    
init()

if __name__ == "__main__":
    match = {
        'entryId': 'entryId-'+kutils.codes.new(),
        'leagueId': 'leagueId-VOMEg0HAbLiH',
        'timestamp': kutils.dates.currentTimestamp(),
        'matchId': 'matchId-'+kutils.codes.new(),
        'homeTeam': 'teamA',
        'awayTeam': 'teamB',
        'homeScore': 4,
        'awayScore': 3,
        'matchdate':'02/06/2024',
        'others':{}
    }
    
    print(addMatchResultsToDb(match))
    # print(calculateGoalDifference(match))
    import pprint
    # pprint.pprint(fetchAllMatches())