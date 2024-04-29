// const API_BASE_URL = 'http://localhost:8090'; // Adjust if your Flask app runs on a different port

// document.getElementById('manageForm').onsubmit = function(event) {
//     event.preventDefault();
//     createTable();
// };

// function createTable() {
//     const beerName = document.getElementById('beer_name').value;
//     const beerType = document.getElementById('beer_type').value;
//     const rating = document.getElementById('rating').value;
//     const quantity = document.getElementById('quantity').value;

//     if (!beerName || !beerType || !rating || !quantity) {
//         alert("Please fill in all fields.");
//         return;
//     }

//     const tableContainer = document.getElementById('tableContainer');
//     tableContainer.innerHTML = ''; // Clear previous table

//     const table = document.createElement('table');
//     table.className = 'data-table';

//     const headerRow = table.insertRow();
//     ['Beer Name', 'Beer Type', 'Review', 'Rating', 'Actions'].forEach(text => {
//         const cell = headerRow.insertCell();
//         cell.textContent = text;
//     });

//     const newRow = table.insertRow();
//     newRow.insertCell().textContent = beerName;
//     newRow.insertCell().textContent = beerType;
//     const reviewInput = document.createElement('input');
//     reviewInput.type = 'text';
//     reviewInput.className = 'review-input';
//     newRow.insertCell().appendChild(reviewInput);
//     newRow.insertCell().textContent = rating;

//     const actionsCell = newRow.insertCell();
//     const updateButton = document.createElement('button');
//     updateButton.textContent = 'Update';
//     updateButton.onclick = function() {
//         showUpdateModal(newRow);
//     };
//     actionsCell.appendChild(updateButton);

//     const deleteButton = document.createElement('button');
//     deleteButton.textContent = 'Delete';
//     deleteButton.onclick = function() {
//         if (confirm('Are you sure you want to delete this review?')) {
//             newRow.remove();
//             showToast('Review deleted successfully.');
//         }
//     };
//     actionsCell.appendChild(deleteButton);

//     tableContainer.appendChild(table);
// }

// function showUpdateModal(row) {
//     const modal = document.createElement('div');
//     modal.className = 'modal';
//     const modalContent = document.createElement('div');
//     modalContent.className = 'modal-content';
//     const modalHeader = document.createElement('div');
//     modalHeader.className = 'modal-header';
//     const title = document.createElement('h2');
//     title.className = 'modal-title';
//     title.textContent = 'Update Review';
//     const closeButton = document.createElement('button');
//     closeButton.className = 'close-button';
//     closeButton.textContent = '×';
//     closeButton.onclick = function() {
//         modal.style.display = 'none';
//         document.body.removeChild(modal);
//     };

//     modalHeader.appendChild(title);
//     modalHeader.appendChild(closeButton);

//     const form = document.createElement('div');
//     form.className = 'modal-body';

//     createInputField(form, 'Beer Name', row.cells[0].textContent);
//     createSelectField(form, 'Beer Type', row.cells[1].textContent, ['Ale', 'Lager', 'Stout']);
//     createInputField(form, 'Review', row.cells[2].firstChild.value);
//     createInputField(form, 'Rating', row.cells[3].textContent);

//     const updateBtn = document.createElement('button');
//     updateBtn.textContent = 'Save Changes';
//     updateBtn.onclick = function() {
//         row.cells[0].textContent = form.children[0].lastChild.value;
//         row.cells[1].textContent = form.children[1].lastChild.value;
//         row.cells[2].firstChild.value = form.children[2].lastChild.value;
//         row.cells[3].textContent = form.children[3].lastChild.value;
//         modal.style.display = 'none';
//         document.body.removeChild(modal);
//         showToast('Review updated successfully.');
//     };

//     const modalFooter = document.createElement('div');
//     modalFooter.className = 'modal-footer';
//     modalFooter.appendChild(updateBtn);

//     modalContent.appendChild(modalHeader);
//     modalContent.appendChild(form);
//     modalContent.appendChild(modalFooter);

//     modal.appendChild(modalContent);
//     document.body.appendChild(modal);
//     modal.style.display = 'flex';
// }

// function createInputField(form, label, value) {
//     const inputGroup = document.createElement('div');
//     inputGroup.className = 'input-group';
//     const inputLabel = document.createElement('label');
//     inputLabel.className = 'input-label';
//     inputLabel.textContent = label;
//     const inputField = document.createElement('input');
//     inputField.className = 'modal-input';
//     inputField.value = value;
//     inputGroup.appendChild(inputLabel);
//     inputGroup.appendChild(inputField);
//     form.appendChild(inputGroup);
// }

// function createSelectField(form, label, currentType, options) {
//     const group = document.createElement('div');
//     group.className = 'input-group';
//     const selectLabel = document.createElement('label');
//     selectLabel.className = 'input-label';
//     selectLabel.textContent = label;
//     const select = document.createElement('select');
//     select.className = 'modal-input';
//     options.forEach(option => {
//         const opt = document.createElement('option');
//         opt.value = option;
//         opt.textContent = option;
//         if (option === currentType) opt.selected = true;
//         select.appendChild(opt);
//     });
//     group.appendChild(selectLabel);
//     group.appendChild(select);
//     form.appendChild(group);
// }

// function showToast(message) {
//     const toast = document.createElement('div');
//     toast.className = 'toast';
//     toast.textContent = message;
//     document.body.appendChild(toast);
//     setTimeout(() => {
//         toast.classList.add('show');
//     }, 100);
//     setTimeout(() => {
//         toast.classList.remove('show');
//         setTimeout(() => {
//             toast.remove();
//         }, 500);
//     }, 3000);
// }
const API_BASE_URL = 'http://localhost:8090';

document.getElementById('manageForm').onsubmit = function(event) {
    event.preventDefault();
    fetchData();
};

function createTable(reviews) {
    const tableContainer = document.getElementById('tableContainer');
    tableContainer.innerHTML = '';
    const table = document.createElement('table');
    table.className = 'data-table';

    const headerRow = table.insertRow();
    ['Beer Name', 'Beer Type', 'Review', 'Rating', 'Actions'].forEach(text => {
        const cell = headerRow.insertCell();
        cell.textContent = text;
    });

    reviews.forEach(review => {
        const newRow = table.insertRow();
        newRow.insertCell().textContent = review.beer_name;
        newRow.insertCell().textContent = review.beer_type;
        const reviewInput = document.createElement('input');
        reviewInput.type = 'text';
        reviewInput.className = 'review-input';
        reviewInput.value = review.review_text;
        newRow.insertCell().appendChild(reviewInput);
        newRow.insertCell().textContent = review.rating;

        const actionsCell = newRow.insertCell();
        const updateButton = document.createElement('button');
        updateButton.textContent = 'Update';
        updateButton.onclick = function() {
            updateReview(review.review_id, reviewInput.value, review.rating);
        };
        actionsCell.appendChild(updateButton);

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.onclick = function() {
            deleteReview(review.review_id);
        };
        actionsCell.appendChild(deleteButton);
    });

    tableContainer.appendChild(table);
}

function fetchData() {
    fetch(`${API_BASE_URL}/select`, {
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

function updateReview(reviewId, reviewText, rating) {
    const data = { review_id: reviewId, review_text: reviewText, rating: rating };
    fetch(`${API_BASE_URL}/update_review`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        showToast(data.message);
        fetchData(); // Refresh data
    })
    .catch((error) => {
        console.error('Error:', error);
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
        showToast(data.message);
        fetchData(); // Refresh data
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
        }, 500);
    }, 3000);
}
