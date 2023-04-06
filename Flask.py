from flask import Flask

app = Flask(__name__)

import requests
import json

@app.route('/')
def max_speed():
    prev_value = None
    count = 0

    while True:
        urls = "https://hst-api.wialon.com/wialon/ajax.html?svc=token/login&params={\"token\":\"014dd3a86c5da0541a4412b8302df4213B5B97F52BDEFB8DCD427AFDA3C4453D2D49513C\"}"

        responses = requests.get(urls)

        if responses.status_code == 200:
            data = json.loads(responses.content.decode('utf-8'))
            eid = data["eid"]
        else:
            print("Error: {}".format(responses.status_code))

        url2 = 'http://hst-api.wialon.com/wialon/ajax.html'
        params = {
            'svc': 'core/search_item',
            'params': '{"id":26711440,"flags":1024,"spec":{"itemsType":"avl_unit","propName":"acceleration","propValueMask":1}}',
            'sid': eid
        }
        response2 = requests.get(url2, params=params).json()

        x = response2["item"]["pos"]["x"]
        y = response2["item"]["pos"]["y"]

        latitude = y
        longitude = x

        api_key = 'AIzaSyB_PJPSU_BUfhLfqJZSIphqGtNi8AVhNOA'

        url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={y},{x}&language=ka&key={api_key}'

        response = requests.get(url)

        if response.ok:
            data = response.json()
            for result in data['results']:
                for component in result['address_components']:
                    if 'route' in component['types']:
                       street_name = component['long_name']
                    break
            else:
                street_name = "ელგუჯა ამაშუკელის ქუჩა"
                print("No road information found in the response, set default value 70km/h")
        else:
            print("Error:", response.status_code)

        with open('speedLimit_database_Tbilisi.json', 'r', encoding='utf-8') as f:
            speed_limits = json.load(f)

        for d in speed_limits:
            if d['name'] == street_name:
                maxspeed = d['maxspeed']
                break
        else:
            maxspeed = "Sorry, no maxspeed found for this street"

        if maxspeed and maxspeed.isdigit():
            command_name = f"SpeedLimit {int(maxspeed)}"
            param_value = maxspeed
        else:
            command_name = " "

        item_id = 26711440
        sid = eid

        params = {"itemId": item_id, "commandName": command_name, "param": f"setparam 11104:{param_value}", "linkType": "", "timeout": 60, "flags": 0}
        url = f"https://hst-api.wialon.com/wialon/ajax.html?svc=unit/exec_cmd&params={json.dumps(params)}&sid={sid}"

        if maxspeed != prev_value:
            prev_value = maxspeed

        return f'The maxspeed for {street_name} is {maxspeed} km/h'


if __name__ == '__main__':
    print("flask running")
   # app.run(host='localhost', port=8000, debug=True)






