from flask import Flask, render_template, request, jsonify
from datetime import datetime
import http.client
import json 

app = Flask(__name__)

@app.route('/info')
def info():
    return render_template('wellriseInfo.html')

@app.route('/second', methods=['POST'])
def second():
     return render_template('wellriseInfo.html') 

def convert_datetime_to_string(dt):
    return str(dt)

def load_json():
    # Assuming your JSON file is named 'data.json' and located in the same directory
    with open('data.json') as file:
        data = json.load(file)
    return data

def calculate_time_difference():
    data = load_json()
    data = data["timestamps"]

    # Extract the first two timestamps (assuming the timestamps are in ISO 8601 format)
    time_format = "%H:%M:%S"
    time1 = datetime.strptime(data[1], time_format)
    time2 = datetime.strptime(data[0], time_format)


    # Calculate the difference
    time_difference = time1 - time2

    return time_difference

@app.route('/')
def index():
    data = load_json()
    data = data["timestamps"]

    # Calculate the time difference
    time_difference = calculate_time_difference()
    time_difference = convert_datetime_to_string(time_difference)
    time_format = "%H:%M:%S"
    if int(data[0][0:1]) < 12: 
        time1 = data[0] + "am"
    else: 
        time1 = data[0] + "pm"
    if int(data[1][0:1]) < 12: 
        time2 = data[1] + "am"
    else: 
        time2 = data[1] + "pm"


    #time1 = datetime.strptime(data[0], "%H:%M:%S")
    #time2 = datetime.strptime(data[1], "%H:%M:%S")

    print(type(time1))
    print(time1)
    print(time2)
    # Pass it to the template
    return render_template('index.html', time_difference=time_difference, time1 = time1, time2 = time2)

if __name__ == '__main__':
    app.run(debug=True)


##

# File paths
input_file = "tempdata.json"
output_file = "data.json"

# Step 1: Read the string from tempdata.json
try:
    with open(input_file, "r") as f:
        raw_data = f.read().strip()  # Strip any leading/trailing whitespace
except FileNotFoundError:
    print(f"Error: {input_file} not found.")
    raw_data = None

if raw_data:
    # Step 2: Split the string into a list of timestamps based on the semicolon delimiter
    timestamps = raw_data.split(";")

    # Step 3: Create a dictionary with the list of timestamps
    data_dict = {
        "timestamps": timestamps
    }

    # Step 4: Write the dictionary to data.json
    with open(output_file, "w") as f:
        json.dump(data_dict, f, indent=4)

    print(f"Data successfully written to {output_file}.")
else:
    print("No data to process.")   


##

@app.route('/log', methods=['POST'])
def log_press():
    # Get the JSON data sent from the Arduino
    data = request.get_json()
    
    if 'press_time' in data:
        # Extract the press time (assumed to be in UNIX timestamp format or ISO string)
        press_time = datetime.strptime(data['press_time'],  "%H:%M:%S")

        # Add it to the press_times list
        press_times.append(press_time)

        # If there's more than one press, calculate the time difference
        if len(press_times) > 1:
            time_difference = press_times[-2] - press_times[-1]
            time_difference = convert_datetime_to_string(time_difference)
            

            print(f"{time_difference=}")
            #return jsonify({'time_difference': str(time_difference)})
            return render_template("index.html", jsonObj = time_difference)
        else:
            return jsonify({'time_difference': 'First press, no difference yet.'})
    else:
        return jsonify({'error': 'Invalid data format'}), 400

if __name__ == '__main__':
    app.run(debug=True)


