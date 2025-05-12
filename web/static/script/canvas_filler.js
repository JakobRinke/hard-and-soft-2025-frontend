

const PLAYER_COLOR = '#FF0000';
const PLAYER_PATH_COLOR = '#FCC';

const ALCOHOL_COLOR = '#00FF00';
const MAGNETIC_FIELD_COLOR = '#0000FF';
const BUMP_COLOR = '#FFFF00';

const ALCOHOL_THRESHOLD = 0.04;
const MAGNETIC_FIELD_THRESHOLD = 35.3;
const BUMP_THRESHOLD = 0.005;



function convertX(x) {
    return (x / worldXSize) * canvasXSize;
}

function convertY(y) {
    return canvasYSize - (y / worldYSize) * canvasYSize;
}



const worldXSize = 200;
const worldYSize = 200;

const canvas = document.getElementById('map-canvas');
const ctx = canvas.getContext('2d');
const canvasXSize = canvas.width;
const canvasYSize = canvas.height;

function fill_canvas() {

    // Draw the Grid JPG or the map
    // TODO
    
    // Draw players
    for (let i = 0; i < current_file.timestamps.length; i++) {
        const x = current_file.x[i];
        const y = current_file.y[i];
        if (i == current_file.timestamps.length - 1) {
            markPointOfInterest(ctx, x, y, PLAYER_COLOR, true);
        } else {
            markPointOfInterest(ctx, x, y, PLAYER_PATH_COLOR);
        }
    }

    // Draw points of interest
    for (let i = 0; i < current_file.timestamps.length; i++) {
        const x = current_file.x[i];
        const y = current_file.y[i];
        if (current_file.alcohol[i] >= ALCOHOL_THRESHOLD) {
            markPointOfInterest(ctx, x, y, ALCOHOL_COLOR);
        }
        if (current_file.vibration[i] >= BUMP_THRESHOLD) {
            markPointOfInterest(ctx, x, y, BUMP_COLOR);
        }

        if (current_file.magnetic_field[i] >= MAGNETIC_FIELD_THRESHOLD) {
            markPointOfInterest(ctx, x, y, MAGNETIC_FIELD_COLOR);
        }
    }
    
}

function clear_canvas() {
    ctx.clearRect(0, 0, canvasXSize, canvasYSize);
    ctx.fillStyle = '#f0f0f0';
    ctx.fillRect(0, 0, canvasXSize, canvasYSize);
}


const POINT_RADIUS = 5;
const PLAYER_RADIUS = 10;
function markPointOfInterest(ctx, x, y, color, is_player = false) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(convertX(x), convertY(y),  is_player ? PLAYER_RADIUS : POINT_RADIUS , 0, Math.PI * 2);
    ctx.fill();
    ctx.closePath();
}


// Build a legend under the canvas
const legend = document.getElementById('legend');
const legendColors = [
    { color: PLAYER_COLOR, label: 'Player' },
    { color: PLAYER_PATH_COLOR, label: 'Player Path' },
    { color: ALCOHOL_COLOR, label: 'Alcohol' },
    { color: MAGNETIC_FIELD_COLOR, label: 'Magnetic Field' },
    { color: BUMP_COLOR, label: 'Bump' }
];

legendColors.forEach(item => {
    const legendItem = document.createElement('div');
    legendItem.style.display = 'flex';
    legendItem.style.alignItems = 'center';
    legendItem.style.marginBottom = '5px';

    const colorBox = document.createElement('div');
    colorBox.style.width = '20px';
    colorBox.style.height = '20px';
    colorBox.style.backgroundColor = item.color;
    colorBox.style.marginRight = '10px';

    const label = document.createElement('span');
    label.textContent = item.label;

    legendItem.appendChild(colorBox);
    legendItem.appendChild(label);
    legend.appendChild(legendItem);
}
);
