''''
    this module is responsible for creating tables 
    where leagues are registered 

'''

import kisa_utils as kutils 
import pprint


def addLeagueToDb(leagues:dict)->dict:
    '''
    this function is responsible for adding a league to the database
    '''
    dbPath = kutils.config.getValue('smsDb/rootPath')
    dbTable = kutils.config.getValue('smsDb/tables')
    entryId = leagues['entryId']
    leagueId = leagues['leagueId']
    timestamp = leagues['timestamp']
    leagueName = leagues['leagueName']
    leagueYear = leagues['leagueYear']
    leagueStartDate = leagues['leagueStartDate']
    leagueEndDate = leagues['leagueEndDate']
    others = leagues['others']
    print(leagueId)

    
    with kutils.db.Api(dbPath, dbTable, readonly=False)as db:
        insertStatus = db.insert(
            "league",[entryId,leagueId,timestamp,leagueName,leagueYear,leagueStartDate,leagueEndDate,others]
        )
        # print(insertStatus)
        return insertStatus
    
def fetchAllTheLeagues():
        dbPath = kutils.config.getValue('smsDb/rootPath')
        dbTable = kutils.config.getValue('smsDb/tables')
        with kutils.db.Api(dbPath,dbTable ,readonly=True) as db:
            fetchResults = db.fetch(
                "league",['*'],
                condition = "",  # No condition
        conditionData = [] , # No condition data
        limit = 100  ,# Example limit, adjust as needed
        returnDicts = True,
        returnNamespaces = False,
        parseJson = True,
        returnGenerator = False,
            )
            # index = 0
            
            for league in range(len(fetchResults)):
                # for index in range(len(league[index])):
                # index+=1
                print(fetchResults[league])
            return fetchResults
def fetchSpecificLeague(leagueDetails:dict):
    dbPath = kutils.config.getValue('smsDb/rootPath')
    dbTable = kutils.config.getValue('smsDb/tables')
    with kutils.db.Api(dbPath,dbTable, readonly=True) as db:
        fetchResults = db.fetch(
            "league",
            columns = ['*'],
            condition = " leagueName = ? AND leagueYear = ?",# Condition
            conditionData = [leagueDetails['leagueName'],leagueDetails['leagueYear']], #condition data
            limit = 100 ,# Example limit, adjust as needed
            returnDicts= False,
            returnNamespaces = False,
            parseJson = False,
            returnGenerator = False,
        )
        print(leagueDetails['leagueName'])
        return fetchResults
            
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
        "tables":{
            'league':'''
                            entryId             varchar(32) not null,
                            leagueId            varchar(32) PRIMARY KEY not null,
                            timestamp           varchar(32) not null,
                            leagueName          varchar(32) not null,
                            leagueYear          varchar(32) not null,
                            leagueStartDate     varchar(32) not null,
                            leagueEndDate       varchar(32) not null,
                            others              json       
                            
            ''',
            
        }
        
    
    }
    defaults['dbPath'] = defaults["rootPath"]+"/db/"+defaults["dbName"]
    config_topic = "smsDb"
    
    for key in defaults:
        if 1 or not kutils.config.getValue(config_topic + "/" + key):
            kutils.config.setValue(config_topic + "/" + key , defaults[key])
            
init()

if __name__ == "__main__":
    
    
    leagues = {
        
                            'entryId':            "entryId-"+kutils.codes.new(),
                            'leagueId':           "leagueId-"+kutils.codes.new(),
                            'timestamp':          kutils.dates.currentTimestamp(),
                            'leagueName':         'kccacup League',
                            'leagueYear':        2019,
                            'leagueStartDate':     '20/03/2019',
                            'leagueEndDate':     '13/11/2019',
                            'others':             ""
    }
    leagueDetails ={
        'leagueYear': 2019,
        'leagueName':'chappa League'
    }
    
    # addLeagueToDb(leagues)
    # pprint.pprint(fetchAllTheLeagues())
    createStandingsTable()
    # pprint.pprint(fetchSpecificLeague(leagueDetails))