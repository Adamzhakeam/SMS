'''
    this module is responsible for creation of table of standings 
    adding,updating a,deleting and selecting of data to view from the table 
    
'''

import kisa_utils as kutils

# def updateGoalsAgainst(matchResults:dict)->list:
#     '''
#         this function is responsible for updating teams for the goals against
#         scored by a team
#         @param matchResults:is a dictionary that contains facts about team after a match
#     '''
#     dbPath = kutils.config.getValue('smsDb/rootPath')
#     dbTables = kutils.config.getValue('smsDb/tables')
#     with kutils.db.Api(dbPath,dbTables, readonly=False) as db:
#         teamCurrentGoals = db.fetch('tableOfStandings',['goalsAgainst'],'teamName =? and leagueId = ?',[matchResults['homeTeam'],matchResults['leagueId']] ,
#             limit=2,returnDicts = False,returnNamespaces = False,parseJson= False,returnGenerator = False)
        
#         currentGoals = teamCurrentGoals[0][0] if teamCurrentGoals else 0
        
#         newGoals = currentGoals + matchResults['awayScore']
        
#         updateGoalsAgainstResult = db.update('tableOfStandings',['goalsAgainst'],[newGoals],'teamName=?',[matchResults['homeTeam']])
        
#     with kutils.db.Api(dbPath,dbTables, readonly=False) as db:
        
#         teamCurrentGoals = db.fetch(
#             'tableOfStandings',['goalsAgainst'],'teamName = ? and  leagueId = ?',[matchResults['awayTeam'],matchResults['awayTeam']],
#             limit=2,returnDicts = False,returnNamespaces = False,parseJson= False,returnGenerator = False)
        
#         currentAwayGoals = teamCurrentGoals[0][0] if teamCurrentGoals else 0
#         newAwayGoals = currentAwayGoals + matchResults['homeScore']
        
#         updateAwayGoalsAwayResult = db.update('tableOfStandings',['goalsAgainst'],[newAwayGoals],'teamName=?',[matchResults['awayTeam']])
#         return [updateGoalsAgainstResult,updateAwayGoalsAwayResult]
# ---- the above code is the old version ------

def updateGoalsAgainst(matchResults:dict) -> list:
    '''
        this module is responsible for updating goals for 
        of both home team and awayTeam
        @param matchResults 0701121290: 'homeTeam','awayTeam',HomeScore and awayScore 
        are the expected keys in the dictionary 
    '''
    dbPath = kutils.config.getValue('smsDb/rootPath')
    dbTable = kutils.config.getValue('smsDb/tables')
    
    teams = ['homeTeam','awayTeam']
    updateResults = []
    teamData = {}
    
    with kutils.db.Api(dbPath,dbTable, readonly=False) as db:
        for team in teams:
            teamName = matchResults[team]
            fetchResults = db.fetch(
                'tableOfStandings',
                ['goalsAgainst'],
                'teamName=? and leagueId=?',
                [teamName,matchResults['leagueId']],
                limit=1,
                returnDicts=False,
                returnNamespaces=False,
                parseJson = False,
                returnGenerator=False
            )
            if fetchResults:
                currentGoalsAgainst = fetchResults[0][0]
                newGoalsAgainst = currentGoalsAgainst + matchResults[f'{team[:4]}Score']
                teamData[teamName] = newGoalsAgainst
            else:
                return(f'No existing record found for 1{teamName} in league {matchResults["leagueId"]}')
            for teamName,newGoalsAgainst in teamData.items():
                updateResult= db.update(
                    'tableOfStandings',
                    ['goalsAgainst'],
                    [newGoalsAgainst],
                    'teamName=?',
                    [teamName],
                    
                )
                updateResults.append(updateResult)
    return {
        'status':True, 'log':''
    }
# def updateGoalsFor(matchResults:dict)->list:
#     '''
#         this function is responsible for updating teams for the goals for 
#         scored by a team
#         @param matchResults:is a dictionary that contains facts about team after a match
#     '''
#     dbPath = kutils.config.getValue('smsDb/rootPath')
#     dbTables = kutils.config.getValue('smsDb/tables')
#     with kutils.db.Api(dbPath,dbTables, readonly=False) as db:
#         teamCurrentGoals = db.fetch(
#             'tableOfStandings',['goalsFor'],'teamName = ?',[matchResults['homeTeam']],limit=2,
#             returnDicts = False,returnNamespaces = False,parseJson= False,returnGenerator = False
#         )
#         currentGoals = teamCurrentGoals[0][0] if teamCurrentGoals else 0
#         newGoals = currentGoals + matchResults['homeScore']
        
#         updateGoalsForResult = db.update('tableOfStandings',['goalsFor'],[newGoals],'teamName=?',[matchResults['homeTeam']])
#     with kutils.db.Api(dbPath,dbTables, readonly=False) as db:
#         teamCurrentGoals = db.fetch(
#             'tableOfStandings',['goalsFor'],'teamName = ?',[matchResults['awayTeam']],limit=2,
#             returnDicts = False,returnNamespaces = False,parseJson= False,returnGenerator = False
#         )
#         currentAwayGoals = teamCurrentGoals[0][0] if teamCurrentGoals else 0
#         newAwayGoals = currentAwayGoals + matchResults['awayScore']
        
#         updateAwayGoalsForResult = db.update('tableOfStandings',['goalsFor'],[newAwayGoals],'teamName=?',[matchResults['awayTeam']])
#         return [updateGoalsForResult,updateAwayGoalsForResult]
 
 
#______this the refactored version of the above code ---------------------
def updateGoalsFor(matchResults: dict) -> list:
    dbPath = kutils.config.getValue('smsDb/rootPath')
    dbTable = kutils.config.getValue('smsDb/tables')
    teams = ['homeTeam', 'awayTeam']
    updateResults = []
    teamData = {}

    with kutils.db.Api(dbPath, dbTable, readonly=False) as db:
        for team in teams:
            teamName = matchResults[team]
            fetchResults = db.fetch(
                'tableOfStandings',
                ['teamName', 'goalsFor'],
                'teamName=? and leagueId=?',
                [teamName, matchResults['leagueId']],
                limit=1,
                returnDicts=True,
                returnNamespaces=False,
                parseJson=False,
                returnGenerator=False
            )
            if fetchResults:
                currentGoalsFor = fetchResults[0]['goalsFor']
                newGoalsFor = currentGoalsFor + matchResults[f'{team[:4]}Score']
                teamData[teamName] = newGoalsFor
            else:
                return(f'No existing record found for 2 {teamName} in league {matchResults["leagueId"]}')
        
        for teamName, newGoalsFor in teamData.items():
            updateResult = db.update(
                'tableOfStandings',
                ['goalsFor'],
                [newGoalsFor],
                'teamName=? and leagueId=?',
                [teamName, matchResults['leagueId']]
            )
            updateResults.append(updateResult)

    return {
        'status':True,
        'log':''
    }

        
def calculateGoalDifference(matchResults:dict)->dict:
    '''
        this function is responsible for calculating the goal 
        difference between teams 
        
        @param matchResults:is a dictionary that contains facts about teams after a match 
    '''
    
    homeGoalDifference = matchResults['homeScore'] - matchResults['awayScore']
    awayGoalDifference = -homeGoalDifference
    
    return{
        'homeGoalDifference':homeGoalDifference,
        'homeTeam':matchResults['homeTeam'],
        'awayGoalDifference':awayGoalDifference,
        'awayTeam':matchResults['awayTeam']
    }

def calculatePoints(matchResults: dict) -> dict:
    """
    This function calculates team points based on match results.
    @param matchResults: Dictionary containing match facts, team names, and their scores.
    """
    # Map for the points based on the comparison of home and away scores
    pointsMap = {
        1: (3, 0),  # Home team wins
        -1: (0, 3),  # Away team wins
        0: (1, 1)  # Draw
    }

    # Calculate the score difference
    scoreDifference = (matchResults['homeScore'] > matchResults['awayScore']) - (matchResults['homeScore'] < matchResults['awayScore'])

    # Get points from the map
    homePoints, awayPoints = pointsMap[scoreDifference]
    

    return {
        'homePoints': homePoints,
        'homeTeam': matchResults['homeTeam'],
        'awayPoints': awayPoints,
        'awayTeam': matchResults['awayTeam']
    }
def calculateWinsLossesAndDraws(matchResults: dict) -> dict:
    '''
    This function is responsible for calculating the wins,
    draws, and losses according to the match results.
    
    @param matchResults: Dictionary containing match details. Expected keys:
                         'homeTeam', 'awayTeam', 'homeScore', 'awayScore'
    @return: Dictionary containing updated wins, losses, and draws for both teams.
    '''
    
    scoreDifference = matchResults['homeScore'] - matchResults['awayScore']
    homeWin = int(scoreDifference > 0)
    awayWin = int(scoreDifference < 0)
    draw = int(scoreDifference == 0)
    
    return {
        'homeTeam': matchResults['homeTeam'],
        'homeWins': homeWin,
        'homeLosses': awayWin,
        'homeDraws': draw,
        'awayTeam': matchResults['awayTeam'],
        'awayWins': awayWin,
        'awayLosses': homeWin,
        'awayDraws': draw
    }
    
# def updateWinDrawLoss(matchResults:dict)->list:
#     '''
#         this function is responsible for updating team's win,loss and draw status 
        
#         @param matchResults: Dictionary containing match details . expected keys:
#                                 'homeTeam',awayTeam,'homeScore','awayScore','leagueId'
#     '''
#     dbPath = kutils.config.getValue('smsDb/rootPath')
#     dbTable = kutils.config.getValue('smsDb/tables')
#     matchStatus = calculateWinsLossesAndDraws(matchResults)
    
#     with kutils.db.Api(dbPath, dbTable, readonly=False)as db:
#         fetchResults = db.fetch('tableOfStandings',['wins','losses','draws'], 'teamName=? and leagueId = ?',[matchResults['homeTeam'],matchResults['leagueId']],
#                                 limit = 1, returnDicts=False,returnNamespaces=False,parseJson=False,returnGenerator=False)
        
       
#         currentHomewins,currentHomeLosses,currentHomeDraws = fetchResults[0][0],fetchResults[0][1],fetchResults[0][2]
#         newHomeWins = currentHomewins+matchStatus['homeWins']
#         newHomeLosses = currentHomeLosses+matchStatus['homeLosses']
#         newHomeDraws = currentHomeDraws+matchStatus['homeDraws']
#         updateStatus = db.update('tableOfStandings',['wins','losses','draws'],[newHomeWins,newHomeLosses,newHomeDraws],'teamName=?',[matchResults['homeTeam']])
#         return updateStatus

# ----------the above code is the old version --and below is the refactored version
def updateWinDrawLoss(matchResults: dict) -> list:
    '''
    This function is responsible for updating team's win, loss, and draw status.
    
    @param matchResults: Dictionary containing match details. Expected keys:
                         'homeTeam', 'awayTeam', 'homeScore', 'awayScore', 'leagueId'
    '''
    dbPath = kutils.config.getValue('smsDb/rootPath')
    dbTable = kutils.config.getValue('smsDb/tables')
    matchStatus = calculateWinsLossesAndDraws(matchResults)
    teams = ['homeTeam', 'awayTeam']
    updateResults = []

    with kutils.db.Api(dbPath, dbTable, readonly=False) as db:
        for team in teams:
            teamName = matchResults[team]
            # Check if the team exists in the database
            fetchResults = db.fetch(
                'tableOfStandings',
                ['*'],
                'teamName=? and leagueId=?',
                [teamName, matchResults['leagueId']],
                limit=1,
                returnDicts=True,
                returnNamespaces=False,
                parseJson=False,
                returnGenerator=False
            )
            
            # if not fetchResults:
                
                # return {
                #     'status':False,
                #     'log':f'3{teamName} does not exist'
                # }
            print(f'results',fetchResults)
            print(f'priviouswins',fetchResults[0].get('wins'))
            currentWins, currentLosses, currentDraws = fetchResults[0].get('wins'), fetchResults[0].get('losses'), fetchResults[0].get('draws')
            newWins = currentWins + matchStatus[f'{team[:4]}Wins']
            newLosses = currentLosses + matchStatus[f'{team[:4]}Losses']
            newDraws = currentDraws + matchStatus[f'{team[:4]}Draws']

            updateResult = db.update(
                'tableOfStandings',
                ['wins', 'losses', 'draws'],
                [newWins, newLosses, newDraws],
                'teamName=? and leagueId=?',
                [teamName, matchResults['leagueId']]
            )
            updateResults.append(updateResult)

    return {
        'status':True,
        'log':''
    }


# def updateGoalDifference(matchResults:dict)->list:
#     dbPath = kutils.config.getValue('smsDb/rootPath')
#     dbTable = kutils.config.getValue('smsDb/tables')
#     goalDifference = calculateGoalDifference(matchResults)
#     with kutils.db.Api(dbPath, dbTable, readonly=False) as db:
#         fetchResponse = db.fetch('tableOfStandings',['goalDifference'],'teamName=?',[matchResults['homeTeam']],limit = 2,
#                                  returnDicts=False,returnNamespaces=False,parseJson=False,returnGenerator=False)
#         currentHomeDifference = fetchResponse[0][0] if fetchResponse else 0
#         newGoalDifference = currentHomeDifference + goalDifference['homeGoalDifference']
#         homeTeamUpdateResult =db.update('tableOfStandings', ['goalDifference'],[newGoalDifference], 'teamName=?',[matchResults['homeTeam']])
#         awayFetchResponse = db.fetch('tableOfStandings',['goalDifference'],'teamName=?',[matchResults['awayTeam']],limit = 2,
#                                  returnDicts=False,returnNamespaces=False,parseJson=False,returnGenerator=False)
#         currentAwayDifference = awayFetchResponse[0][0] if awayFetchResponse else 0
        
#         newAwayDifference = currentAwayDifference + goalDifference['awayGoalDifference']
        
#         awayTeamUpdateResult =db.update('tableOfStandings', ['goalDifference'], [newAwayDifference ],'teamName=?',[matchResults['awayTeam']])
#         return[homeTeamUpdateResult,awayTeamUpdateResult]

def updateGoalDifference(matchResults: dict) -> list:
    dbPath = kutils.config.getValue('smsDb/rootPath')
    dbTable = kutils.config.getValue('smsDb/tables')
    goalDifference = calculateGoalDifference(matchResults)
    teams = ['homeTeam', 'awayTeam']
    updateResults = []

    with kutils.db.Api(dbPath, dbTable, readonly=False) as db:
        for team in teams:
            teamName = matchResults[team]
            # Fetch team data if it exists
            fetchResponse = db.fetch('tableOfStandings', ['goalDifference'], 'teamName = ?',[teamName], limit=1, returnDicts=True, returnNamespaces=False, parseJson=False, returnGenerator=False)
            # if not fetchResponse:
            #     return(f"Team {teamName} does not exist in the database.")
            
            currentDifference = fetchResponse[0].get('goalDifference', 0)
            newDifference = currentDifference + goalDifference[f'{team[:4]}GoalDifference']
            
            # Update the team's goal difference
            updateResult = db.update('tableOfStandings', ['goalDifference'], [newDifference], 'teamName = ?',[teamName])
            updateResults.append(updateResult)

    return {
        'status':True,
        'log':''
    }


def updatePoints(matchResults:dict)->list:
    dbPath = kutils.config.getValue('smsDb/rootPath')
    dbTable = kutils.config.getValue('smsDb/tables')
    points = calculatePoints(matchResults)
    with kutils.db.Api(dbPath, dbTable, readonly=False) as db:
        fetchResponse = db.fetch('tableOfStandings',['points'],'teamName=?',[matchResults['homeTeam']],limit = 2,
                                 returnDicts=False,returnNamespaces=False,parseJson=False,returnGenerator=False)
        currentHomePoints = fetchResponse[0][0] if fetchResponse else 0
        newHomePoints = currentHomePoints + points['homePoints']
        homeTeamUpdateResult =db.update('tableOfStandings', ['points'],[newHomePoints], 'teamName=?',[matchResults['homeTeam']])
    # with kutils.db.Api(dbPath,dbTable, readonly=False) as db:
        awayFetchResponse = db.fetch('tableOfStandings',['points'],'teamName=?',[matchResults['awayTeam']],limit = 2,
                                 returnDicts=False,returnNamespaces=False,parseJson=False,returnGenerator=False)
        # print(awayFetchResponse)
        currentAwayPoints = awayFetchResponse[0][0] if awayFetchResponse else 0
        # print(currentAwayPoints)
        newAwayPoints = currentAwayPoints + points['awayPoints']
        # print(newAwayPoints)
        awayTeamUpdateResult =db.update('tableOfStandings', ['points'], [newAwayPoints],'teamName=?',[matchResults['awayTeam']])
        updateResponse = []
        return {
            'status':True,
            'log':''
        }

# def updateGoalDifference(matchResults: dict) -> list:
#     dbPath = kutils.config.getValue('smsDb/rootPath')
#     dbTable = kutils.config.getValue('smsDb/tables')
#     goalDifference = calculateGoalDifference(matchResults)
#     teams = ['homeTeam', 'awayTeam']
#     updateResults = []

#     with kutils.db.Api(dbPath, dbTable, readonly=False) as db:
#         for team in teams:
#             teamName = matchResults[team]
#             # Fetch team data if it exists
#             fetchResponse = db.fetch('tableOfStandings', ['goalDifference'], f'teamName = ?',[teamName], limit=1, returnDicts=True, returnNamespaces=False, parseJson=False, returnGenerator=False)
#             if not fetchResponse:
#                 raise ValueError(f"Team {teamName} does not exist in the database.")
            
#             currentDifference = fetchResponse[0].get('goalDifference', 0)
#             newDifference = currentDifference + goalDifference[f'{team[:4]}GoalDifference']
            
#             # Update the team's goal difference
#             updateResult = db.update('tableOfStandings', ['goalDifference'], [newDifference], f'teamName=?',[teamName])
#             updateResults.append(updateResult)

#     return {
#         'status':True,
#         'log':''
#     }

def addMatchperformanceToDb(matchResults:dict)->dict:
    '''
    this function is responsible for adding a team to table of standings when team is registered 
    @param machResults: 'entryId','standingsId','leagueId','teamName','wins','losses','draws',
                        'goalsFor','goalsAgainst',goalsDifference','matchesPlayed','points',others 
    '''
    # createStandingsTable()
    # print('running')
    dbPath = kutils.config.getValue('smsDb/rootPath')
    dbTable = kutils.config.getValue('smsDb/tables')
    entryId = matchResults['entryId']
    standingsId=matchResults['standingsId']
    leagueId = matchResults['leagueId']
    teamName = matchResults['teamName']
    wins = matchResults['wins']
    losses = matchResults['losses']
    draws = matchResults['draws']
    goalsFor = matchResults['goalsFor']
    goalsAgainst = matchResults['goalsAgainst']
    goalDifference = matchResults['goalDifference']
    matchesPlayed = matchResults['matchesPlayed']
    points = matchResults['points']
    others = matchResults['others']
    with kutils.db.Api(dbPath, dbTable, readonly=False) as db:
        insertionResponse = db.insert(
            'tableOfStandings',[entryId,standingsId,leagueId,teamName,wins,losses,draws,goalsFor,goalsAgainst,
                                goalDifference,matchesPlayed,points,others]
        )
        return insertionResponse
    
    
def createStandingsTable():
    dbPath = kutils.config.getValue('smsDb/rootPath')
    standingsTable = kutils.config.getValue('smsDb/tables')
    print(standingsTable)
    with kutils.db.Api(dbPath,standingsTable, readonly=False) as db:
       creationResponse =  db.createTables(standingsTable)
    print('create',creationResponse)
    return creationResponse
       
       
def fetchAllStandings(leagueDetails:dict)->dict:
    '''
        this function is responsible for for fetching all standings of a league depending on the league details
        @ param leagueDetails:'leagueId'  are the expected keys in the dictionary
    '''
    dbPath = kutils.config.getValue('smsDb/rootPath')
    dbTables = kutils.config.getValue('smsDb/tables')
    with kutils.db.Api(dbPath, dbTables, readonly=True) as db:
        db.fetch()
        fetchResults = db.fetch(
            'tableOfStandings',['*'],'leagueId = ? ',[leagueDetails['leagueId']],limit = 100, 
            returnDicts=True,returnNamespaces=False,parseJson=False, returnGenerator=False
        )
        return fetchResults
    
def fetch_teams_with_standings(matchdetails:dict):
    dbPath = kutils.config.getValue('smsDb/rootPath')
    dbTables = kutils.config.getValue('smsDb/tables')
    table = 'tableOfStandings'
    columns = [
        'teamName', 'wins', 'losses', 'draws',
        'goalsFor', 'goalsAgainst', 'goalDifference',
        'matchesPlayed', 'points'
    ]
    condition = 'leagueId = ?'  # Example condition to filter teams with non-zero points
    condition_data = [matchdetails['leagueId']]
    limit = 100  # Example limit
    print('conditional data',condition_data)
    with kutils.db.Api(dbPath,dbTables, readonly=True) as db:
        standings_data = db.fetch(
            table, columns, condition, condition_data,
            limit=limit, returnDicts=True, parseJson=False
        )

    # Sort the standings_data from best to worst based on points, goal difference, etc.
    standings_data.sort(key=lambda x: (x['points'], x['goalDifference'], x['goalsFor']), reverse=True)

    return standings_data


def init():
    defaults = {
        'rootPath':'/tmp/sms',
        'dbName':'sms.db',
        'tables':{
            'tableOfStandings':
                '''
                entryId         varchar(32) not null,
                standingsId     varchar(32) PRIMARY KEY not null,
                leagueId       varchar(32) not null,
                teamName        varchar(32) not null,
                wins            INTEGER DEFAULT 0,
                losses          INTEGER DEFAULT 0,
                draws           INTEGER DEFAULT 0,
                goalsFor        INTEGER DEFAULT 0,
                goalsAgainst    INTEGER DEFAULT 0,
                goalDifference  INTEGER DEFAULT 0,
                matchesPlayed   INTEGER DEFAULT 0,
                points          INTEGER DEFAULT 0,
                others          json,
                FOREIGN KEY (leagueId) REFERENCES leagues (leagueId)
                
                '''
        }
    }
    
    defaults['dbPath'] = defaults['rootPath']+'/db/'+defaults['dbName']
    config_topic = 'smsDb'
    for key in defaults:
        if 1 or not kutils.config.getValue(config_topic + '/' + key):
            kutils.config.setValue(config_topic + '/' + key, defaults[key])
            
init()
        
if __name__ == '__main__':
    standings = {
        'entryId': kutils.codes.new(),
        'standingsId':kutils.codes.new(),
        'leagueId':'leagueId-VOMEg0HAbLiH',
        'teamName':'TeamX',
        'wins':     0,
        'losses':   0,
        'draws':    0,
        'goalsFor':0,
        'goalsAgainst':0,
        'goalDifference':0,
        'matchesPlayed':0,
        'points':0,
        'others':''
    }
    
    matchResults = {
    'homeScore': 6,
    'awayScore': 5,
    'homeTeam': 'SCVILLAFC',
    'awayTeam': 'MENGO-FC',
    'leagueId':'leagueId-yGr0F2K9ivN9',
}
    
    # print(createStandingsTable())
    # print(fetch_teams_with_standings({'leagueId':'leagueId-yGr0F2K9ivN9'}))
    # print(fetchAllStandings())
    print(updateWinDrawLoss(matchResults))
    # print(updateGoalsAgainst(matchResults))
    # print('goalsfor',updateGoalsFor(matchResults))
    # print('points',updatePoints(matchResults))
    # print('goalDifference',updateGoalDifference(matchResults))
    # print(addMatchperformanceToDb(standings))
    # result = calculatePoints(matchResults)
    # print(calculateGoalDifference(matchResults))
    # print(result)