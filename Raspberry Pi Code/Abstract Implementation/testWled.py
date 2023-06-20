import requests
import json

url = "http://192.168.1.8/json"
print(url)
headers = {
    "Content-Type": "application/json"
}

listIP = [
    "10.1.10.107",
    "10.1.10.108",
    "10.1.10.122",
    "10.1.10.124",
    "10.1.10.13",
    "10.1.10.137",
    "10.1.10.15",
    "10.1.10.159",
    "10.1.10.169",
    "10.1.10.19",
    "10.1.10.196",
    "10.1.10.204",
    "10.1.10.210",
    "10.1.10.219",
    "10.1.10.23",
    "10.1.10.230",
    "10.1.10.240",
    "10.1.10.25",
    "10.1.10.36",
    "10.1.10.37",
    "10.1.10.42",
    "10.1.10.53",
    "10.1.10.52",
    "10.1.10.83",
    "10.1.10.91",
    "10.1.10.97",
    "10.1.10.113",
    "10.1.10.43",
    "10.1.10.109",
    "10.1.10.84",
    "10.1.10.197",
    "10.1.10.106",
    ]
color = "FF0000"

data = '{"seg":{"i":['
for i in range(44):
    data = data + str(i)+', "' + color+'" , '
data = data + '45,"0000FF"'
#data = data + '0,"FF0000", 2,"00FF00", 4,"0000FF"'
data = data + ']}}'
print(data)

data_J = json.loads(data)
#response = requests.post(url, headers=headers, data=json.dumps(data_J))
#print(response.json())


json_data ={'on':True, 'bri':255 ,'v':True}
#r = requests.post("http://192.168.1.8/json/state", json=json_data)
#print (r.status_code)
#print (r.json())



def fillRoom(color, room):
    """Instantly change color of all lights in a room"""
    start = room*8
    print(room)
    for i in range(start, start + 8):
        url = "http://"+str(listIP[i])+"/json"
        data = '{"seg":{"i":['
        
        for j in range(0 , 44):
            data = data + str(j)+', "' + color+'" , '
        data = data + '45,"0000FF"'
        data = data + ']}}'
        data_J = json.loads(data)
        print(url)
        print(data_J)
    

fillRoom("FF0000" , 2)
