document.addEventListener('DOMContentLoaded', function() {
    console.log("DOMContentLoaded event fired");

    // Fetch all leagues and populate the select dropdown
    fetch('http://localhost:5000/fetchAllLeagues', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        console.log("Leagues fetched:", data);
        const leagueSelect = document.getElementById('leagueSelect');
        data.forEach(league => {
            let option = document.createElement('option');
            option.value = league.leagueId;
            option.text = `${league.leagueName} ${league.leagueYear}`;
            leagueSelect.appendChild(option);
        });
    })
    .catch(error => console.error('Error fetching leagues:', error));

    // Event listener for league selection
    document.getElementById('leagueSelect').addEventListener('change', function() {
        const leagueId = this.value;
        console.log("Selected leagueId:", leagueId);

        // Fetch league standings based on selected league
        fetch('http://localhost:5000/fetchLeagueStandings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ leagueId })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Standings fetched:", data);
            if (data.status) {
                const standingsTable = document.getElementById('standingsTable').getElementsByTagName('tbody')[0];
                standingsTable.innerHTML = '';

                // Sort the data if needed
                data.data.sort((a, b) => b.points - a.points || b.goalDifference - a.goalDifference || b.goalsFor - a.goalsFor);
                
                // Populate the table with the fetched standings
                data.data.forEach((team, index) => {
                    let row = standingsTable.insertRow();
                    row.insertCell(0).textContent = index + 1;
                    row.insertCell(1).textContent = team.teamName;
                    // console.log(team.teamName);
                    row.insertCell(2).textContent = team.wins;
                    row.insertCell(3).textContent = team.losses;
                    row.insertCell(4).textContent = team.draws;
                    row.insertCell(5).textContent = team.goalsFor;
                    row.insertCell(6).textContent = team.goalsAgainst;
                    row.insertCell(7).textContent = team.goalDifference;
                    row.insertCell(8).textContent = team.matchesPlayed;
                    row.insertCell(9).textContent = team.points;
                });
            } else {
                console.error('Error fetching standings:', data.log);
                const standingsTable = document.getElementById('standingsTable').getElementsByTagName('tbody')[0];
                standingsTable.innerHTML = ''; // Clear the table if there's an error
            }
        })
        .catch(error => console.error('Error fetching standings:', error));
    });
});
