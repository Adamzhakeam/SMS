from flask import Flask, request, jsonify
from flask_cors import CORS
import kisa_utils as kutils
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..')))
app = Flask(__name__)
CORS(app)

@app.route('/addTeam', methods=['POST'])
def handleAddTeam():
    from db import addTeamToDb

    payload = request.get_json()
    
    # Add server-side generated fields
    payload['entryId'] = "entryId-" + kutils.codes.new()
    payload['teamId'] = "teamId-" + kutils.codes.new()
    payload['timestamp'] = kutils.dates.currentTimestamp()
    payload['standingsId'] = 'standingsId-'+kutils.codes.new()
    # payload['wins'],payload['losses'],payload['draws'],payload['matchesPlayed'],payload['goalsFor'],payload['goalsAgainst'] = 0
    # Using a loop to initialize multiple values in a dictionary
    for key in ['wins', 'losses', 'draws', 'matchesPlayed', 'goalsFor', 'goalsAgainst','goalDifference','points']:
        payload[key] = 0


    payloadStructure = {
        'entryId': kutils.config.getValue('smsDb/entryId'),
        'teamId': kutils.config.getValue('smsDb/teamId'),
        'teamName': kutils.config.getValue('smsDb/teamName'),
        'teamDesc': kutils.config.getValue('smsDb/teamDesc'),
        'teamLogo': kutils.config.getValue('smsDb/teamLogo'),
        'leagueId': kutils.config.getValue('smsDb/leagueId'),
        'location': kutils.config.getValue('smsDb/location'),
        'standingsId':kutils.config.getValue('smsDb/standingsId'),
        'wins':kutils.config.getValue('smsDb/wins'),
        'losses':kutils.config.getValue('smsDb/losses'),
        'draws':kutils.config.getValue('smsDb/draws'),
        'goalsFor':kutils.config.getValue('smsDb/goalsFor'),
        'goalsAgainst':kutils.config.getValue('smsDb/goalsAgainst'),
        'goalDifference':kutils.config.getValue('smsDb/goalDifference'),
        'matchesPlayed':kutils.config.getValue('smsDb/matchesPlayed'),
        'timestamp': kutils.config.getValue('smsDb/timestamp'),
        'points':kutils.config.getValue('smsDb/points'),
        'activeYear':kutils.config.getValue('smsDb/activeYear'),
        'others': kutils.config.getValue('smsDb/others')
    }
    
    payloadValidationResponse = kutils.structures.validator.validate(payload, payloadStructure)
    
    if payloadValidationResponse['status']:
        for key in payload:
            if payload[key] is None:
                return jsonify({'status': False, 'log': f'The value for {key} is missing. Please provide it.'})
        
        insertionResponse = addTeamToDb(payload)
        return jsonify(insertionResponse)
    return jsonify(payloadValidationResponse)

@app.route('/fetchAllLeagues', methods=['POST'])
def handleFetchAllLeagues():
    from backend.league.db import fetchAllTheLeagues

    leagues = fetchAllTheLeagues()
    return jsonify(leagues)

def init():
    smsDbDefaults = {
        'entryId': str,
        'teamId': str,
        'teamName': str,
        'teamDesc': str,
        'teamLogo': str,
        'leagueId': str,
        'standingsId':str,
        'location': str,
        'timestamp': str,
        'wins':     int,
        'losses':   int,
        'draws':    int,
        'points':int,
        'goalsFor':int,
        'goalsAgainst':int,
        'goalDifference':int,
        'matchesPlayed':int,
        'points':int,
        'activeYear':int,
        'others': dict
    }
    config_topic = 'smsDb'

    for key in smsDbDefaults:
        if not kutils.config.getValue(config_topic + '/' + key):
            kutils.config.setValue(config_topic + '/' + key, smsDbDefaults[key])

init()

if __name__ == '__main__':
    import pprint
    app.run(debug=True, host='0.0.0.0', port=5000)
    # pprint.pprint(handleFetchAllLeagues())
