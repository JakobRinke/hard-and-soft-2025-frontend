

function read_statistics() {
    console.log("Updating statistics");
    fill_table();
    fill_canvas();
}


function fill_table() {
    const table = document.querySelector("#statistics-table-content")
    table.innerHTML = renderTable(current_file.get_basic_table_data()).outerHTML;
}


async function auto_reload_statistics() {
    for (let i = 0; i < 10; i++) {
        await new Promise(resolve => setTimeout(resolve, 5000));
        if (current_file_id != null) {
            reload_statistics();
        }
    }
}


auto_reload_statistics();