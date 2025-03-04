let currentPage = 1;

// ✅ Load Responses with Pagination
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
                div.setAttribute("data-keyword", item.keyword.toLowerCase());

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

// ✅ Filter Responses in Real-Time
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


// ✅ Ensure Search Works
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("search-bar").addEventListener("input", filterResponses);
});

// ✅ Edit a Response
function editResponse(oldKeyword, oldResponse, oldLink) {
    const newKeyword = prompt("Edit keyword:", oldKeyword);
    const newResponse = prompt("Edit response:", oldResponse);
    const newLink = prompt("Edit link (optional):", oldLink);

    if (newKeyword !== null && newResponse !== null) {
        fetch("/edit_response", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ oldKeyword, newKeyword, response: newResponse, link: newLink })
        }).then(() => loadResponses(currentPage));
    }
}


// ✅ Delete a Response
function deleteResponse(keyword) {
    if (confirm("Are you sure you want to delete this response?")) {
        fetch("/delete_response", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ keyword })
        }).then(() => loadResponses(currentPage));
    }
}

// ✅ Pagination Controls
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

// ✅ Add a New Response
document.getElementById("add-response-form").addEventListener("submit", function(event) {
    event.preventDefault();  // Stop page reload

    const keyword = document.getElementById("keyword").value.trim();
    const response = document.getElementById("response").value.trim();
    const link = document.getElementById("link").value.trim() || null;

    if (!keyword || !response) {
        alert("⚠️ Keyword and Response are required!");
        return;
    }

    fetch("/add_response", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ keyword, response, link })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("✅ Response added successfully!");
            loadResponses(currentPage);
        } else {
            alert("⚠️ Error: " + data.error);
        }
    })
    .catch(error => console.error("Error:", error));

    // Clear form fields after submission
    document.getElementById("keyword").value = "";
    document.getElementById("response").value = "";
    document.getElementById("link").value = "";
});

//  Load Responses on Page Load
window.onload = () => {
    loadResponses();
};
