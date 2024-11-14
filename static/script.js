function searchJobs() {
    const skills = document.getElementById("skills").value;
    fetch(`/search_jobs?skills=${encodeURIComponent(skills)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const jobTableBody = document.getElementById("jobTable").getElementsByTagName("tbody")[0];
            jobTableBody.innerHTML = ""; // Clear previous results
            
            // Check if data is empty and handle accordingly
            if (data.length === 0) {
                const noResultsRow = document.createElement("tr");
                noResultsRow.innerHTML = `<td colspan="5">No job listings found.</td>`;
                jobTableBody.appendChild(noResultsRow);
                return;
            }

            data.forEach(job => {
                const row = document.createElement("tr");
                
                // Make sure to include a platform name and a job link if available
                row.innerHTML = `
                    <td>${job.platform || 'N/A'}</td>
                    <td>${job.title || 'N/A'}</td>
                    <td>${job.company || 'N/A'}</td>
                    <td>${job.location || 'N/A'}</td>
                    <td><a href="${job.link || '#'}" target="_blank">View Job</a></td>
                `;
                
                jobTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            alert('An error occurred while fetching job listings. Please try again later.');
        });
}
function handleSignup(event) {
    event.preventDefault();
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch('signup.html', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Sign-up successful!');
        } else {
            alert('Sign-up failed: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred during sign-up.');
    });
}
