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
    time_difference = time2 - time1

    return time_difference

@app.route('/')
def index():
    data = load_json()
    data = data["timestamps"]
    
    # Calculate the time difference
    time_difference = calculate_time_difference()
    time_difference = convert_datetime_to_string(time_difference)
    time_format = "%H:%M:%S"
    time1 = datetime.strptime(data[1], time_format)
    time2 = datetime.strptime(data[0], time_format)
    
    # Pass it to the template
    return render_template('index.html', time_difference=time_difference, time1 = time1, time2 = time2)

if __name__ == '__main__':
    app.run(debug=True)



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
            time_difference = press_times[-1] - press_times[-2]
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
