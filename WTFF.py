import requests
import json
import time

prev_value = None
count = 0  # Initialize iteration count to zero

while True:
    #get SID
    urls = "https://hst-api.wialon.com/wialon/ajax.html?svc=token/login&params={\"token\":\"014dd3a86c5da0541a4412b8302df4213B5B97F52BDEFB8DCD427AFDA3C4453D2D49513C\"}"

    responses = requests.get(urls)

    if responses.status_code == 200:
        data = json.loads(responses.content.decode('utf-8'))
        eid = data["eid"]
        #print("EID: {}".format(eid))
    else:
        print("Error: {}".format(responses.status_code))

    #get the GPS location
    url2 = 'http://hst-api.wialon.com/wialon/ajax.html'
    params = {
        'svc': 'core/search_item',
        'params': '{"id":26711440,"flags":1024,"spec":{"itemsType":"avl_unit","propName":"acceleration","propValueMask":1}}',
        'sid': eid
    }
    #1024/8191
    response2 = requests.get(url2, params=params).json()

    print(response2)

    # Extract the values of "x" and "y" from the JSON response
    x = response2["item"]["pos"]["x"]
    y = response2["item"]["pos"]["y"]


    latitude = y
    longitude = x

    url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json"

    response = requests.get(url)


    

    if response.ok:
        data = response.json()
        if "road" in data.get("address", {}):
            street_name = data["address"]["road"]
            #print(f"The road is: {street_name}")
        else:
            print("No road information found in the response, set default value 70km/h")
            street_name = "ელგუჯა ამაშუკელის ქუჩა"
        
        #street_name = data["address"]["road"]
        #house_number = data["address"]["house_number"]
        #print(f"The address is: {street_name}")
    else:
        print("Error:", response.status_code)

    #print(f"x = {x}")
    #print(f"y = {y}")

    #extract speed limit from database

    # load data from JSON file
    with open('speedLimit_database_Tbilisi.json', 'r', encoding='utf-8') as f:
        speed_limits = json.load(f)

    # search for maxspeed of a given street name
    #street_name = 'ანა პოლიტკოვსკაიას ქუჩა'
    for d in speed_limits:
        if d['name'] == street_name:
            maxspeed = d['maxspeed']
            print(f"The maxspeed for {street_name} is {maxspeed} Km/h")
            break
    else:
        print(f"Sorry, no maxspeed found for {street_name}")
    
    if maxspeed and maxspeed.isdigit():
        #command_name = f"{int(maxspeed)} Km/h Speed Command"
        command_name = f"SpeedLimit {int(maxspeed)}"
        param_value = maxspeed
    else:
        command_name = " "

    # Define the initial parameters
    item_id = 26711440

    #command_name = "110 Km/h Speed Command"
    #command_name = f"{maxspeed} Km/h Speed Command"
    #param_value = maxspeed
    sid = eid
    print(command_name)

    # Construct the params dictionary
    params = {"itemId": item_id, "commandName": command_name, "param": f"setparam 11104:{param_value}", "linkType": "", "timeout": 60, "flags": 0}
    #print(params)
    # Construct the URL with updated sid and param_value
    url = f"https://hst-api.wialon.com/wialon/ajax.html?svc=unit/exec_cmd&params={json.dumps(params)}&sid={sid}"
    

    if maxspeed != prev_value:
        # Print the new value if it has changed
        print("New maxspeed value = ", maxspeed)
        # Send the request
        response = requests.get(url)
        # Check the response status code
        if response.status_code == 200:
            print("Request sent successfully")
        else:
            print("Error sending request: {}".format(response.status_code))


        # Update the current value and the previous value
        prev_value = maxspeed
    else:
        # Update the current value
        prev_value = maxspeed
        print("same maxspeed, request not sent")


    # Increment the iteration count and print it
    count += 1
    #print(f"Loop count = {count}")  
    print(" ")  
    print(" ")  

    # Wait for 5 seconds before making the next request
    time.sleep(2)    


