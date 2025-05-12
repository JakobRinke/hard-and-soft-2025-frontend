
const choose_file_element = document.getElementById("choose_file");
const statistics_element = document.getElementById("statistics");


function makeVisisible(element, visibility) {
    if (visibility) {
        element.style.pointerEvents = "auto";
        element.style.visibility = "visible";
        element.style.position = "relative";
    } else {
        element.style.pointerEvents = "none";
        element.style.visibility = "hidden";
        element.style.position = "absolute";
    }
}

var current_file = null;
var current_file_id = null;
function open_choose_file() {
    makeVisisible(choose_file_element, true);
    makeVisisible(statistics_element, false);
    current_file = null;
    current_file_id = null;
}

function open_statistics(file_id) {
    console.log("open_statistics", file_id);
    makeVisisible(choose_file_element, false);
    makeVisisible(statistics_element, true);
    find_file(file_id).then((data) => {
        current_file = data;
        read_statistics();
    });
    current_file_id = file_id;
}


function reload_statistics() {
    open_statistics(current_file_id);
}

open_choose_file();