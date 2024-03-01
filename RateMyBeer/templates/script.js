const API_BASE_URL = 'http://localhost:8090'; // Adjust if your Flask app runs on a different port

document.getElementById('addForm').onsubmit = function(event) {
    event.preventDefault();
    addReview();
};

function addReview() {
    // Gather form data. Here, only beer_name is used as an example.
    const data = {
        beer_name: document.getElementById('beer_name').value,
        // Add more fields as necessary
    };

    fetch(`${API_BASE_URL}/add`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert(data.msg);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function deleteReview() {
    const beerId = document.getElementById('deleteId').value;

    fetch(`${API_BASE_URL}/del?beer_beerId=${beerId}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert(data.msg);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function editReview() {
    const beerId = document.getElementById('editId').value;
    const newReview = document.getElementById('newReview').value;

    const data = {
        id: beerId,
        new_review: newReview,
    };

    fetch(`${API_BASE_URL}/edit`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert(data.msg);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function fetchData() {
    fetch(`${API_BASE_URL}/select`)
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        const reviews = data.data;
        const display = document.getElementById('dataDisplay');
        display.innerHTML = ''; // Clear previous data
        reviews.forEach(review => {
            const div = document.createElement('div');
            div.innerHTML = `Name: ${review.beer_name} - Review: ${review.review_text}`;
            // Add more details as needed
            display.appendChild(div);
        });
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
