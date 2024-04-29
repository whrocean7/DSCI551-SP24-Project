const API_BASE_URL = 'http://localhost:8090';

document.addEventListener('DOMContentLoaded', function() {
    const manageForm = document.getElementById('manageForm');
    manageForm.addEventListener('submit', function(event) {
        event.preventDefault();
        fetchData();
    });

    const addBtn = document.getElementById('addBtn');
    addBtn.addEventListener('click', function() {
        showAddModal();
    });

});

function createTable(reviews) {
    const tableContainer = document.getElementById('tableContainer');
    tableContainer.innerHTML = '';  // Clear previous table

    const table = document.createElement('table');
    table.className = 'data-table';

    const headerRow = table.createTHead().insertRow();
    ['Beer Name', 'Beer Type', 'Review', 'Rating', 'Actions'].forEach(text => {
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

        const actionsCell = row.insertCell();
        const updateButton = document.createElement('button');
        updateButton.textContent = 'Update';
        updateButton.dataset.reviewId = review.review_id;  // Save review ID in dataset for easier access
        updateButton.addEventListener('click', function() {
            console.log('Update button clicked');
            showUpdateModal(review);
        });
        actionsCell.appendChild(updateButton);

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.addEventListener('click', function() {
            deleteReview(review.review_id);
        });
        actionsCell.appendChild(deleteButton);
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
    const data = { review_id: reviewId };
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

function showAddModal() {
    const modal = document.getElementById('addModal');
    modal.style.display = 'block';
}

function closeAddModal() {
    const modal = document.getElementById('addModal');
    modal.style.display = 'none';
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
