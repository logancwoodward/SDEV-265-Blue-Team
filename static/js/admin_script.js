let currentPage = 1;

// Load responses when the admin panel opens
function loadResponses(page = 1) {
    fetch(`/get_responses?page=${page}`)
        .then(response => response.json())
        .then(data => {
            const list = document.getElementById("responses-list");
            list.innerHTML = "";  // Clear previous results

            if (data.responses.length === 0) {
                list.innerHTML = "<p>No responses found.</p>";
                return;
            }

            data.responses.forEach(item => {
                const div = document.createElement("div");
                div.setAttribute("data-keyword", item.keyword.toLowerCase()); //filtering 

                div.innerHTML = `
                    <p><strong>${item.keyword}</strong>: ${item.response} 
                    ${item.link ? `<a href="${item.link}" target="_blank">Learn more</a>` : ''}</p>
                    <button onclick="editResponse('${item.keyword}', '${item.response}', '${item.link || ''}')">Edit</button>
                    <button onclick="deleteResponse('${item.keyword}')">Delete</button>
                `;
                list.appendChild(div);
            });

            updatePagination(data.total, data.per_page);
        })
        .catch(error => console.error("Error loading responses:", error));
}

// Function to filter responses in real-time
function filterResponses() {
    const input = document.getElementById("search-bar").value.toLowerCase();
    const rows = document.querySelectorAll("#responses-list div"); // Target response elements

    rows.forEach(row => {
        const keyword = row.getAttribute("data-keyword").toLowerCase();
        row.style.display = keyword.includes(input) ? "" : "none"; // Hide non-matching responses
    });
}

// Ensure the event listener is attached to the search bar
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("search-bar").addEventListener("input", filterResponses);
});

// Edit a response
function editResponse(keyword, oldResponse, oldLink) {
    const newResponse = prompt("Edit response:", oldResponse);
    const newLink = prompt("Edit link (optional):", oldLink);

    if (newResponse !== null) {
        fetch("/edit_response", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ keyword, response: newResponse, link: newLink })
        }).then(() => loadResponses(currentPage));
    }
}

// Delete a response
function deleteResponse(keyword) {
    if (confirm("Are you sure you want to delete this response?")) {
        fetch("/delete_response", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ keyword })
        }).then(() => loadResponses(currentPage));
    }
}

// Function to update pagination buttons
function updatePagination(totalResponses, perPage) {
    const paginationDiv = document.getElementById("pagination-controls");
    paginationDiv.innerHTML = ""; 

    const totalPages = Math.ceil(totalResponses / perPage);

    for (let i = 1; i <= totalPages; i++) {
        const button = document.createElement("button");
        button.innerText = i;
        button.onclick = () => {
            currentPage = i;
            loadResponses(i);
        };
        if (i === currentPage) {
            button.style.fontWeight = "bold";
        }
        paginationDiv.appendChild(button);
    }
}


// Load responses on page load
window.onload = () => {
    loadResponses();
};
