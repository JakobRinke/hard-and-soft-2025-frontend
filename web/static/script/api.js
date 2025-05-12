

async function get_api_data(url) {
    const response = await fetch(url, {
        method: 'GET',
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status} \n ${response.statusText} \n ${await response.text()}`);
    }
    const json = await response.json();
    if (json.error) {
        throw new Error(json.error);
    }
    return json['data'];
}

async function find_files() {
    const url = "/data";
    const data = await get_api_data(url);
    // Sort the data list by converting string to timestamp
    data.sort((a, b) => {
        const timestampA = new Date(a).getTime();
        const timestampB = new Date(b).getTime();
        return timestampA - timestampB; // Sort in ascending order
    });  
    return data;
}

class SensorData {
    constructor(data) {
        this.data = data;
        this.timestamps = this.data['timestamps']
        this.alcohol = this.data['alcohol']
        this.magnetic_field = this.data['magnetic_field']
        this.ultrasonic = this.data['ultrasonic']
        this.vibration = this.data['vibration']
        this.x = this.data['x']
        this.y = this.data['y']
    }

    get_basic_table_data() {
        return {
            "Timestamp": this.timestamps,
            "Alcohol": this.alcohol,
            "Magnetic Field": this.magnetic_field,
            "Ultrasonic": this.ultrasonic,
            "Vibration": this.vibration,
            "X": this.x,
            "Y": this.y,
        }
    }
}

async function find_file(file_id) {
    const url = `/data/${file_id}`;
    const data = await get_api_data(url);

    return new SensorData(data);
}

