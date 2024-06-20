from flask import Flask, request, jsonify
from flask_cors import CORS
import kisa_utils as kutils

app = Flask(__name__)
CORS(app)

@app.route('/addLeague', methods=['POST'])
def handleAddLeague():
    from db import addLeagueToDb, fetchAllTheLeagues, fetchSpecificLeague

    # Extract the payload from the request
    payload = request.get_json()

    # Add server-side generated fields
    payload['entryId'] = "entryId-" + kutils.codes.new()
    payload['leagueId'] = "leagueId-"+kutils.codes.new()
    payload['timestamp'] = kutils.dates.currentTimestamp()
    print(payload['leagueId'])
    # Define the expected structure for validation
    payloadStructure = {
        'entryId': kutils.config.getValue('smsDb/entryId'),
        'leagueId': kutils.config.getValue('smsDb/leagueId'),
        'timestamp': kutils.config.getValue('smsDb/timestamp'),
        'leagueName': kutils.config.getValue('smsDb/leagueName'),
        'leagueYear': kutils.config.getValue('smsDb/leagueYear'),
        'leagueStartDate': kutils.config.getValue('smsDb/leagueStartDate'),
        'leagueEndDate': kutils.config.getValue('smsDb/leagueEndDate'),
        'others': kutils.config.getValue('smsDb/others')
    }
    
    # Validate the payload
    payloadValidationResponse = kutils.structures.validator.validate(payload, payloadStructure)
    
    if payloadValidationResponse['status']:
        for key in ['leagueName', 'leagueYear', 'leagueStartDate', 'leagueEndDate']:
            if not payload[key]:
                return jsonify({'status': False, 'log': f'The value for {key} is missing. Please provide it.'})
        
        # Insert the league into the database
        insertionResponse = addLeagueToDb(payload)
        return jsonify(insertionResponse)
    
    return jsonify(payloadValidationResponse)

@app.route('/fetchAllLeagues', methods=['POST'])
def handleFetchAllLeagues():
    from db import  fetchAllTheLeagues

    # Fetch all leagues from the database
    fetchResponse = fetchAllTheLeagues()
    return jsonify(fetchResponse)

@app.route('/fetchSpecificLeague', methods=['POST'])
def handleFetchSpecificLeague():
    from db import fetchSpecificLeague

    # Extract the payload from the request
    payload = request.get_json()

    # Define the expected structure for validation
    payloadStructure = {
        'leagueName': str,
        'leagueYear': int
    }
    
    # Validate the payload
    payloadValidationResponse = kutils.structures.validator.validate(payload, payloadStructure)
    
    if payloadValidationResponse['status']:
        for key in payload:
            if not payload[key]:
                return jsonify({'status': False, 'log': f'The value for {key} is missing. Please provide it.'})
        
        # Fetch the specific league from the database
        fetchResponse = fetchSpecificLeague(payload)
        return jsonify(fetchResponse)
    
    return jsonify(payloadValidationResponse)

def init():
    smsDbDefaults = {
        'entryId': str,
        'leagueId': str,
        'timestamp': str,
        'leagueName': str,
        'leagueYear': int,
        'leagueStartDate': str,
        'leagueEndDate': str,
        'others': dict
    }
    config_topic = 'smsDb'

    for key in smsDbDefaults:
        if not kutils.config.getValue(config_topic + '/' + key):
            kutils.config.setValue(config_topic + '/' + key, smsDbDefaults[key])

init()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
