

/// Data Structure: data={"c1": [1, 2, 3], ..}
function renderTable(data) {
    const table = document.createElement('table');
    table.className = 'table table-striped table-bordered';
    const thead = document.createElement('thead');
    const tbody = document.createElement('tbody');

    // Create header row
    const headerRow = document.createElement('tr');
    for (const key in data) {
        const th = document.createElement('th');
        th.textContent = key;
        headerRow.appendChild(th);
    }
    thead.appendChild(headerRow);

    // Create data rows
    for (let i = 0; i < data[Object.keys(data)[0]].length; i++) {
        const row = document.createElement('tr');
        for (const key in data) {
            const td = document.createElement('td');
            let value = data[key][i];

            if (!isNaN(value)) {
                if (Number(value) === value && value % 1 !== 0) {
                    // Format decimal numbers to 4 places
                    value = value.toFixed(4);
                }
                td.style.textAlign = 'right'; // Align numbers to the left
            } else if (new Date(value).toString() !== 'Invalid Date') {
                // Format timestamps
                value = new Date(value).toLocaleString();
            }

            td.textContent = value;
            row.appendChild(td);
        }
        tbody.appendChild(row);  }

    table.appendChild(thead);
    table.appendChild(tbody);
    return table;
}