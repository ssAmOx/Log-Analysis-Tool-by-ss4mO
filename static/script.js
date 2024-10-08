// Search Functionality (previously added)
document.getElementById('searchInput').addEventListener('keyup', function() {
    let input = document.getElementById('searchInput').value.toLowerCase();
    let table = document.getElementById('logsTable');
    let rows = table.getElementsByTagName('tr');

    for (let i = 1; i < rows.length; i++) { // Start from 1 to skip the header row
        let cells = rows[i].getElementsByTagName('td');
        let found = false;

        for (let j = 0; j < cells.length; j++) {
            if (cells[j].innerText.toLowerCase().includes(input)) {
                found = true;
                break;
            }
        }

        rows[i].style.display = found ? '' : 'none'; // Show or hide rows based on search
    }
});

// Sort Functionality
function sortTable(colIndex) {
    const table = document.getElementById("logsTable");
    const rows = Array.from(table.rows).slice(1); // Skip header row
    const isAscending = table.dataset.sortOrder === 'asc';

    rows.sort((a, b) => {
        const aText = a.cells[colIndex].innerText;
        const bText = b.cells[colIndex].innerText;

        // Adjust comparison based on column type
        if (colIndex === 1) { // Date column
            return isAscending ? new Date(aText) - new Date(bText) : new Date(bText) - new Date(aText);
        } else if (colIndex === 4 || colIndex === 5) { // Status Code and Response Size columns
            return isAscending ? aText - bText : bText - aText;
        } else {
            return isAscending ? aText.localeCompare(bText) : bText.localeCompare(aText);
        }
    });

    // Remove existing rows
    while (table.rows.length > 1) {
        table.deleteRow(1);
    }

    // Append sorted rows
    rows.forEach(row => table.appendChild(row));

    // Toggle sort order
    table.dataset.sortOrder = isAscending ? 'desc' : 'asc';
}
