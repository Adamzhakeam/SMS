document.addEventListener('DOMContentLoaded', function() {
    console.log("DOMContentLoaded event fired");
    fetch('http://localhost:5000/fetchAllLeagues', {
        method: 'POST'
    })
    .then(response => {
        console.log("fetchAllLeagues response status:", response.status);
        return response.json();
    })
    .then(data => {
        console.log("fetchAllLeagues data:", data);
        const leagueSelect = document.getElementById('league');
        const leagueYearSelect = document.getElementById('leagueYear');

        data.forEach(league => {
            let option = document.createElement('option');
            option.value = league.leagueId;
            option.text = league.leagueName;
            leagueSelect.appendChild(option);

            let yearOption = document.createElement('option');
            yearOption.value = league.leagueYear;
            yearOption.text = league.leagueYear;
            leagueYearSelect.appendChild(yearOption);
        });
    })
    .catch(error => console.error('Error fetching leagues:', error));
});

document.getElementById('team-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const teamName = document.getElementById('teamName').value;
    const teamDesc = document.getElementById('teamDesc').value;
    const teamLogo = document.getElementById('teamLogo').value;
    const leagueId = document.getElementById('league').value;
    const location = document.getElementById('location').value;
    const activeYear = parseInt(document.getElementById('leagueYear').value);

    const payload = {
        teamName: teamName,
        teamDesc: teamDesc,
        teamLogo: teamLogo,
        leagueId: leagueId,
        location: location,
        activeYear:activeYear,
        others:{}
    };

    console.log("Submitting team:", payload);

    fetch('http://localhost:5000/addTeam', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        console.log("addTeam response status:", response.status);
        return response.json();
    })
    .then(data => {
        console.log("addTeam response data:", data);
        const responseDiv = document.getElementById('response');
        if (data.status) {
            responseDiv.textContent = 'Team registered successfully!';
            responseDiv.style.color = 'green';
        } else {
            responseDiv.textContent = `Error: ${data.log}`;
            responseDiv.style.color = 'red';
        }
    })
    .catch(error => console.error('Error:', error));
});
