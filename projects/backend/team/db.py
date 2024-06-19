'''
    this module is responsible for regestering teams and updating the data about teams 
    
'''

import sys,os

# Ensure the backend directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import kisa_utils as kutils


def addTeamToDb(teamDetails:dict)->dict:
    '''
        this function is responsible for inserting a team and its details in he database
        @param teamDetails: 'entryId','teamId','teamName','teamDesc','teamLogo','leagueId',
                            'location' and 'others' are expected keys in the dictionary
    '''
    from backend.tableOfStandings.db import addMatchperformanceToDb
    dbPath = kutils.config.getValue('smsDb/rootPath')
    dbTables = kutils.config.getValue('smsDb/tables')
    entryId = teamDetails['entryId']
    teamId = teamDetails['teamId']
    teamName = teamDetails['teamName']
    teamDesc = teamDetails['teamDesc']
    teamLogo = teamDetails['teamLogo']
    leagueId = teamDetails['leagueId']
    location = teamDetails['location']
    activeYear = teamDetails['activeYear']
    others = teamDetails['others']
    
    with kutils.db.Api(dbPath, dbTables, readonly=False) as db:
        
        insertionResponse = db.insert(
            'teams',[entryId,teamId,teamName,teamDesc,teamLogo,leagueId,location,activeYear,others]
        )
        if insertionResponse['status']:
            standingsResponse = addMatchperformanceToDb(teamDetails)
            return standingsResponse
        else:
            return insertionResponse
        
def fetchTeamsFromDb(leagueDetails:dict)->dict:
    ''''
            this function is responsible for fetching teams according to the league they are 
            registered under 
            @ param teamAttributes:'leagueId'is an expected key in the dictionary
    '''
    dbPath = kutils.config.getValue('smsDb/rootPath')
    dbTables = kutils.config.getValue('smsDb/tables')
    teamsLeagueId = leagueDetails['leagueId']
    with kutils.db.Api(dbPath, dbTables, readonly=True) as db:
        fetchResponse = db.fetch(
            'teams',['teamName','teamLogo','leagueId','location'],'leagueId = ?',[teamsLeagueId],limit=100,
            returnDicts = True,returnNamespaces = False, parseJson = False, returnGenerator= False
        )
    if not fetchResponse['status'] :
        return fetchResponse

def fetchAllTeams(teamDetail:dict)->dict:
    dbPath = kutils.config.getValue('smsDb/rootPath')
    dbTable = kutils.config.getValue('smsDb/tables')
    with kutils.db.Api(dbPath,dbTable, readonly=True) as db:
        fetchResponse = db.fetch(
            'teams',
            ['*'],
         condition = "leagueId = ?",  # No condition
        conditionData = [teamDetail['leagueId']] , # No condition data
            limit = 100,
            returnDicts=True ,
            returnNamespaces= False,
            parseJson=False,
            returnGenerator=False
        )
        print(fetchResponse)
        return fetchResponse

def createStandingsTable():
    dbPath = kutils.config.getValue('smsDb/rootPath')
    standingsTable = kutils.config.getValue('smsDb/tables')
    print(standingsTable)
    with kutils.db.Api(dbPath,standingsTable, readonly=False) as db:
       creationResponse =  db.createTables(standingsTable)
    print('create',creationResponse)
    return creationResponse
            
    
    
def init():
    defaults = {
        'rootPath':'/tmp/sms',
        'dbName':'sms.db',
        'tables':{
            'teams':'''
                        entryId         varchar(32) not null,
                        teamId          varchar(32) PRIMARY KEY not null,
                        teamName        varchar(255) not null,
                        teamDesc        varchar (255) not null,
                        teamLogo        varchar  (255) not null,
                        leagueId        varchar (255) not null,
                        location        varchar (255) not null,
                        activeYear      integer (255) not null,
                        others          json,
                        FOREIGN KEY (leagueId) REFERENCES leagues (leagueId)
                        
            '''
        }
    }
    defaults['dbPath'] = defaults['rootPath']+'/db/'+defaults['dbName']
    config_topic = 'smsDb'
    for key in defaults:
        if 1 or not kutils.config.getValue(config_topic + '/' + key):
            kutils.config.setValue(config_topic + '/' + key,defaults[key])
            
init()
    
if __name__ == '__main__':
    teamDetails = {
        'entryId': kutils.codes.new(),
        'teamId': kutils.codes.new(),
        'teamName': 'teamB',
        'standingsId':kutils.codes.new(),
        'teamDesc':'we are the gunners',
        'teamLogo': 'https://example.com/teamA.png',
        'leagueId': 'leagueId-VOMEg0HAbLiH',
        'location':'kawempe',
        'wins':     0,
        'losses':   0,
        'draws':    0,
        'goalsFor':0,
        'goalsAgainst':0,
        'goalDifference':0,
        'matchesPlayed':0,
        'points':0,
        'others':   ''
    }    
    
    teamAttributes = {
        'leagueName':'kccaCup',
        'leagueYear':2024,
        'leagueId':'leagueId-VOMEg0HAbLiH',
        
    }
    
    # print(fetchTeamsFromDb(teamAttributes))
    # print(addTeamToDb(teamDetails))
    print(fetchAllTeams({'leagueId':"leagueId-yGr0F2K9ivN9"}))
    # createStandingsTable()
    