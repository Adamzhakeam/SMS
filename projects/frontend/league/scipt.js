document.getElementById('leagueForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const leagueData = {
        // entryId: "entryId-" + Date.now(), // Temporary unique ID generation
        // leagueId: "leagueId-" + Date.now(), // Temporary unique ID generation
        // timestamp: new Date().toISOString(), // Current timestamp
        leagueName: document.getElementById('leagueName').value,
        leagueYear: parseInt(document.getElementById('leagueYear').value),
        leagueStartDate: document.getElementById('leagueStartDate').value,
        leagueEndDate: document.getElementById('leagueEndDate').value,
        others: {}
    };

    try {
        const response = await fetch('http://localhost:5000/addLeague', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(leagueData)
        });
        
        const result = await response.json();
        document.getElementById('response').innerText = result.log || 'League added successfully!';
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('response').innerText = 'An error occurred while adding the league.';
    }
});
