from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/simulation', methods=['GET'])
def get_simulation_status():
    status = {"traffic_status": "Green light for North"}
    return jsonify(status)

@app.route('/control_light', methods=['POST'])
def control_traffic_light():
    data = request.json
    direction = data.get('direction')
    if direction:
        if direction == 'north':
            lights[0].state = 'GREEN'
        else:
            lights[0].state = 'RED'
        return jsonify({"message": f"Traffic light for {direction} updated to {lights[0].state}"})
    return jsonify({"error": "Invalid direction"}), 400

if __name__ == '__main__':
    app.run(debug=True)
