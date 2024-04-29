const API_BASE_URL = 'http://localhost:8091';

document.addEventListener('DOMContentLoaded', function() {

    // Add event listener to the submit button inside the add modal
    const addForm = document.getElementById('addForm');
    addForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission behavior
        submitAdd(); // Call the function to handle addition
    });

    // Add event listener to the submit button inside the update modal
    const updateForm = document.getElementById('updateForm');
    updateForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission behavior
        submitUpdate(); // Call the function to handle update
    });

    const manageForm = document.getElementById('manageForm');
    manageForm.addEventListener('submit', function(event) {
        event.preventDefault();
        fetchData();
    });

    const addBtn = document.getElementById('addBtn');
    addBtn.addEventListener('click', function() {
        showAddModal();
    });

    const updateBtn = document.getElementById('updateBtn');
    updateBtn.addEventListener('click', function() {
        const reviewId = document.getElementById('review_id').value;
        const reviewText = document.getElementById('review_text_update').value;
        const rating = document.getElementById('rating_update').value;

        const review = {
            review_id: reviewId,
            review_text: reviewText,
            rating: rating
        };

        updateReview(review);
    });

});

function createTable(reviews) {
    const tableContainer = document.getElementById('tableContainer');
    tableContainer.innerHTML = '';  // Clear previous table

    const table = document.createElement('table');
    table.className = 'data-table';

    const headerRow = table.createTHead().insertRow();
    ['Beer Name', 'Beer Type', 'Review', 'Rating'].forEach(text => {
        const cell = headerRow.insertCell();
        cell.textContent = text;
    });

    const tbody = table.createTBody();
    reviews.forEach(review => {
        const row = tbody.insertRow();
        row.insertCell().textContent = review.beer_name;
        row.insertCell().textContent = review.beer_type;
        row.insertCell().textContent = review.review_text;
        row.insertCell().textContent = review.rating;

    //     const actionsCell = row.insertCell();
    //
    //     const updateButton = document.createElement('button');
    //     updateButton.textContent = 'Update';
    //     updateButton.dataset.reviewId = review.review_id;  // Save review ID in dataset for easier access
    //     updateButton.addEventListener('click', function() {
    //         showUpdateModal(review);
    //     });
    //     actionsCell.appendChild(updateButton);
    //
    //     const deleteButton = document.createElement('button');
    //     deleteButton.textContent = 'Delete';
    //     deleteButton.addEventListener('click', function() {
    //         deleteReview(review.review_id);
    //     });
    //     actionsCell.appendChild(deleteButton);
    });

    tableContainer.appendChild(table);
}

// function fetchData() {
//     fetch(`${API_BASE_URL}/select`, {
//         method: 'GET'
//     })
//     .then(response => response.json())
//     .then(data => {
//         createTable(data);
//     })
//     .catch((error) => {
//         console.error('Error:', error);
//     });
// }
function fetchData() {
    const beerName = document.getElementById('beer_name').value;
    const beerType = document.getElementById('beer_type').value;
    const rating = document.getElementById('rating').value;
    const quantity = document.getElementById('quantity').value;

    const queryParams = new URLSearchParams({
        beer_name: beerName,
        beer_type: beerType,
        rating: rating,
        Quantity: quantity
    });

    fetch(`${API_BASE_URL}/select?${queryParams}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        createTable(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}


// function updateReview(reviewId, reviewText, rating) {
//     console.log("updating right now..")
//     const data = { review_id: reviewId, review_text: reviewText, rating: rating };
//     console.log("updating right now..")
//     fetch(`${API_BASE_URL}/update_review`, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(data)
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log('Success:', data);
//         closeUpdateModal();  // Close the modal after submission
//         fetchData();  // Refresh data
//     })
//     .catch((error) => {
//         console.error('Error:', error);
//     });
// }
// 更新 updateReview 函数，使其接受 review 对象作为参数
function updateReview(review) {
    const API_BASE_URL = 'http://localhost:8090'; // 替换为您的后端API地址
    const data = { review_id: review.review_id, review_text: review.review_text, rating: review.rating };
    console.log('we are here')

    fetch(`${API_BASE_URL}/update_review`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        closeUpdateModal();  // 关闭模态框
        fetchData();  // 刷新数据
    })
    .catch((error) => {
        console.error('Error:', error);
        // 在此处处理错误，例如显示错误消息给用户
    });
}


function deleteReview(reviewId) {
    const confirmation = confirm("Are you sure you want to delete this Review?");
    if(confirmation) {
        const data = {review_id: reviewId};
        fetch(`${API_BASE_URL}/delete_review`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                fetchData();  // Refresh data
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }
}

function showAddModal() {
    const modal = document.getElementById('addModal');
    modal.style.display = 'block';
}

function closeAddModal() {
    const modal = document.getElementById('addModal');
    modal.style.display = 'none';

    document.getElementById('tableContainer').style.display = 'block';
}

function showUpdateModal(review) {
    const modal = document.getElementById('updateModal');
    document.getElementById('review_id').value = review.review_id;  // Populate fields with existing data
    document.getElementById('review_text_update').value = review.review_text;
    document.getElementById('rating_update').value = review.rating;
    modal.style.display = 'block';
}

function closeUpdateModal() {
    const modal = document.getElementById('updateModal');
    modal.style.display = 'none';
}

// Function to handle update submission
function submitUpdate() {
    // Get the updated review details from the form
    const reviewId = document.getElementById('review_id').value;
    const reviewText = document.getElementById('review_text_update').value;
    const rating = document.getElementById('rating_update').value;

    // Create a review object
    const updatedReview = {
        review_id: reviewId,
        review_text: reviewText,
        rating: rating
    };

    // Call the updateReview function
    updateReview(updatedReview);
}

// Function to handle addition submission
function submitAdd() {
    console.log("submitAdd is called!")
    // Get the review details from the form
    const beerName = document.getElementById('modal_beer_name').value;
    const beerType = document.getElementById('modal_beer_type').value;
    const reviewText = document.getElementById('modal_review_text').value;
    const rating = document.getElementById('modal_rating').value;

    // Create a review object
    const newReview = {
        beername: beerName,
        beertype: beerType,
        review_text: reviewText,
        rating: parseInt(rating)
    };

    // Call the addReview function
    addReview(newReview);
}

// Function to add a new review
function addReview(review) {
    // Define the API base URL
    const API_BASE_URL = 'http://localhost:8090';

    // Send a POST request to add the review
    fetch(`${API_BASE_URL}/add_review`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(review)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        closeAddModal(); // Close the modal after submission
        fetchData(); // Refresh data
    })
    .catch((error) => {
        console.error('Error:', error);
        // Handle errors here
    });
}

function showAddModal() {
    const modal = document.getElementById('addModal');
    modal.classList.add('confirmation-dialog'); // Add a class to the modal
    modal.style.display = 'block';

    document.getElementById('tableContainer').style.display = 'none';
}