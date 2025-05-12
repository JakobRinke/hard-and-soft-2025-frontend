

function read_statistics() {
    fill_table();
}


function fill_table() {
    const table = document.querySelector("#statistics-table-content")
    table.innerHTML = renderTable(current_file.get_basic_table_data()).outerHTML;
}