from flask import Flask, request, jsonify
from flask_cors import CORS
import kisa_utils as kutils
import sys,os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..')))

app = Flask(__name__)
CORS(app)

@app.route('/addMatchResult', methods=['POST'])
def handleAddMatchResult():
    '''
    Endpoint to add match results to the database.
    Expects a JSON payload with keys: 'entryId', 'leagueId', 'timestamp', 'matchId',
    'homeTeam', 'awayTeam', 'homeScore', 'awayScore', 'matchDate', 'others'
    '''
    from db import addMatchResultsToDb
    payload = request.get_json()
    payload['entryId'] = 'entryId-'+kutils.codes.new()
    payload['matchId'] = 'matchId-'+kutils.codes.new()
    payload['timestamp'] = kutils.dates.currentTimestamp()
    print(payload['timestamp'])
    payloadStructure = {
        'entryId': kutils.config.getValue('smsDb/entryId'),
        'leagueId': kutils.config.getValue('smsDb/leagueId'),
        'timestamp': kutils.config.getValue('smsDb/timestamp'),
        'matchId': kutils.config.getValue('smsDb/matchId'),
        'homeTeam': kutils.config.getValue('smsDb/homeTeam'),
        'awayTeam': kutils.config.getValue('smsDb/awayTeam'),
        'homeScore': kutils.config.getValue('smsDb/homeScore'),
        'awayScore': kutils.config.getValue('smsDb/awayScore'),
        'matchDate': kutils.config.getValue('smsDb/matchDate'),
        'others': kutils.config.getValue('smsDb/others')
    }
    
    payloadValidationResponse = kutils.structures.validator.validate(payload, payloadStructure)
    
    if payloadValidationResponse['status']:
        for key in payload:
            if not payload[key]:
                return {'status': False, 'log': f'The value for {key} is missing. Please provide it.'}
        
        insertionResponse = addMatchResultsToDb(payload)
        if not insertionResponse['status']:
            return jsonify(insertionResponse)
        return jsonify(insertionResponse)
    return jsonify(payloadValidationResponse)

@app.route('/fetchAllMatches', methods=['POST'])
def handleFetchAllMatches():
    '''
    Endpoint to fetch all match results from the database.
    '''
    from db import fetchAllMatches
    fetchResponse = fetchAllMatches()
    return jsonify(fetchResponse)

@app.route('/fetchAllTeams',methods=['POST'])
def handleFetchAllTeams():
    '''
    this endpoint is responsible for handling fetching teams from database 
    '''
    from backend.team.db import fetchAllTeams
    payload = request.get_json()
    
    payloadStructure = {
        'leagueId':kutils.config.getValue('smsDb/leagueId')
    }
    validationResponse = kutils.structures.validator.validate(payload,payloadStructure)
    if validationResponse['status']:
        for key in payload:
            if not payload[key]:
                return{'status':False , 'log':f'the vale for {key} is missing'}
    teams = fetchAllTeams(payload)
    return jsonify(teams)
@app.route('/fetchAllLeagues',methods=['POST'])
def handleAllLeagues():
    '''
    this endpoint is responsible for handling fetching all teams from database 
    '''
    from backend.league.db import fetchAllTheLeagues
    leagues = fetchAllTheLeagues()
    return jsonify((leagues))

def init():
    smsDbDefaults = {
        
        'entryId': str,
        'leagueId': str,
        'timestamp': str,
        'matchId': str,
        'homeTeam': str,
        'awayTeam': str,
        'homeScore': int,
        'awayScore': int,
        'matchDate': str,
        'others': dict
    }
    config_topic = 'smsDb'

    for key in smsDbDefaults:
        if 1 or not kutils.config.getValue(config_topic + '/' + key):
            kutils.config.setValue(config_topic + '/' + key, smsDbDefaults[key])

init()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
