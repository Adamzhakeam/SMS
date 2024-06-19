document.addEventListener('DOMContentLoaded', function() {
    console.log("DOMContentLoaded event fired");

    // Fetch all leagues and populate the league dropdown
    fetch('http://localhost:5000/fetchAllLeagues', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        console.log("Leagues fetched:", data);  // Debug log
        const leagueSelect = document.getElementById('league');
        data.forEach(league => {
            let option = document.createElement('option');
            option.value = league.leagueId;
            option.text = `${league.leagueName} ${league.leagueYear}`;
            leagueSelect.appendChild(option);
        });

        // Add event listener for league dropdown change
        leagueSelect.addEventListener('change', function() {
            const leagueId = leagueSelect.value;
            fetchTeams(leagueId);
        });
    })
    .catch(error => console.error('Error fetching leagues:', error));

    function fetchTeams(leagueId) {
        fetch('http://localhost:5000/fetchAllTeams', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ leagueId: leagueId })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Teams fetched:", data);  // Debug log
            const homeTeamSelect = document.getElementById('homeTeam');
            const awayTeamSelect = document.getElementById('awayTeam');
            
            // Clear previous options
            homeTeamSelect.innerHTML = '';
            awayTeamSelect.innerHTML = '';

            data.forEach(team => {
                let option = document.createElement('option');
                option.value = `${team.teamName}|${team.leagueId}|${team.activeYear}`;
                option.text = `${team.teamName} ${team.activeYear}`;
                homeTeamSelect.appendChild(option.cloneNode(true));
                awayTeamSelect.appendChild(option.cloneNode(true));
            });
        })
        .catch(error => console.error('Error fetching teams:', error));
    }
});

document.getElementById('match-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const leagueId = document.getElementById('league').value;
    const homeTeamInfo = document.getElementById('homeTeam').value.split('|');
    const awayTeamInfo = document.getElementById('awayTeam').value.split('|');

    const homeTeam = homeTeamInfo[0];
    const awayTeam = awayTeamInfo[0];
    const homeLeagueId = homeTeamInfo[1];
    const awayLeagueId = awayTeamInfo[1];
    const homeYear = homeTeamInfo[2];
    const awayYear = homeTeamInfo[2];

    const matchDate = document.getElementById('matchDate').value;
    const homeScore = parseInt(document.getElementById('homeScore').value);
    const awayScore = parseInt(document.getElementById('awayScore').value);
    const others = {"":""};

    if (homeTeam === awayTeam) {
        alert('Home team and away team must be different.');
        return;
    }

    if (homeLeagueId !== awayLeagueId || homeYear !== awayYear) {
        alert('Both teams must belong to the same league and year.');
        return;
    }

    const payload = {
        leagueId: leagueId,
        homeTeam: homeTeam,
        awayTeam: awayTeam,
        matchDate: matchDate,
        homeScore: homeScore,
        awayScore: awayScore,
        others: others
    };

    console.log("Submitting match result:", payload);  // Debug log

    fetch('http://localhost:5000/addMatchResult', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        console.log("addMatchResult response:", data);  // Debug log
        const responseDiv = document.getElementById('response');
        if (data.status) {
            responseDiv.textContent = 'Match result added successfully!';
            responseDiv.style.color = 'green';
        } else {
            responseDiv.textContent = `Error: ${data.log}`;
            responseDiv.style.color = 'red';
        }
    })
    .catch(error => console.error('Error submitting match result:', error));
});
