from flask import Flask, request, jsonify
from flask_cors import CORS
import kisa_utils as kutils
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..')))
app = Flask(__name__)
CORS(app)

@app.route('/fetchLeagueStandings', methods=['POST'])
def handleFetchLeagueStandings():
    from kisa_utils.structures import validator 
    from db import fetch_teams_with_standings

    payload = request.get_json()
    payloadStructure = {
        'leagueId': kutils.config.getValue('standingsApi/leagueId')
    }
    payloadValidationResponse = validator.validate(payload,payloadStructure)
    
    if payloadValidationResponse['status']:
        print('___',payload.get('leagueId'))
        if not payload.get('leagueId'):
            return jsonify({'status': False, 'log': 'The value for leagueId is missing'})
        
        fetchResponse = fetch_teams_with_standings(payload)
        if not fetchResponse:
            return jsonify({'status': False, 'log': 'There are no standings in the table for this league'})
        
    
        return jsonify({'status': True, 'data': fetchResponse})
    else:
        return jsonify({'status': False, 'log': 'Invalid payload structure'})

@app.route('/fetchAllLeagues', methods=['POST'])
def handleFetchAllLeagues():
    from backend.league.db import fetchAllTheLeagues
    leagues = fetchAllTheLeagues()
    return jsonify(leagues)

def init():
    defaults = {
        'leagueId': str
    }
    config_topic = 'standingsApi'
    
    for key in defaults:
        if 1 or not kutils.config.getValue(config_topic + '/' + key):
            kutils.config.setValue(config_topic + '/' + key, defaults[key])
            
init()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
