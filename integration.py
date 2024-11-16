import requests

def get_traffic_data():
    response = requests.get('https://api.example.com/traffic_data')
    return response.json()

def update_traffic_lights_based_on_data():
    traffic_data = get_traffic_data()
    if traffic_data['north_traffic'] > 50:
        lights[0].state = "GREEN"
    else:
        lights[0].state = "RED"
