import requests
import json

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

print(len(listIP))

url = "http://"+str(listIP[0])+"/json"
print(url)
headers = {
    "Content-Type": "application/json"
}

class LightStrip:
    LED_PIN = 18
    LED_FREQ_HZ = 800000
    LED_DMA = 10
    LED_BRIGHTNESS = 50
    LED_INVERT = False
    LED_CHANNEL = 0
    LED_PER_TARGET = 45
    NUM_TARGETS_ROOM = 8
    NUM_ROOMS = 4
    LED_COUNT = LED_PER_TARGET * NUM_TARGETS_ROOM * NUM_ROOMS

    BLACK = "000000"


    def __init__(self):
        """Create a new light strip object with the specs of the four box system"""
        print("Initialization")

    def targetCorrect(self, target):
        """Takes a target number in standard format and converts it to match the wiring of each room"""
        # Rerouting algorithm
        if(target >= 16):
            # Room 3 and 4 Correction
            return (target // 8)*8 + 7 - (target % 8)

        if(target >= 8 and target % 8 != 0):
            # Room 2 correction
            return target + 8 - 2*(target % 8)
        return target


    def colorWipe(self, targets, index):
        """Turn off last light of given index at all listed targets (simultaneous is key to prevent repeat calls to show)"""
        for i in range(0, len(targets)):
            url = "http://"+str(listIP[targets[i]])+"/json"
            data = {"seg":{"i":[index,"000000"]}}
            response = requests.post(url, headers=headers, data=json.dumps(data))
            print(response.json())

    def fillTarget(self, color, target):
        """Instantly change color of all lights in target range. This is where rerouting occurs"""
        url = "http://"+str(listIP[target])+"/json"
        data = '{"seg":{"i":['
        for i in range(0 , self.LED_PER_TARGET - 1):
            data = data + str(i)+', "' + color+'" ,'
        data = data + str(self.LED_PER_TARGET)+',"'+color +'"]}}'
        data_J = json.loads(data)
        #print(data_J)
        response = requests.post(url, headers=headers, data=json.dumps(data_J))
        print(response.json())

    def fillRemainingTarget(self, color, target, index):
        """Instantly change all remaining lights on a target to a different color"""
        start = index
        url = "http://"+str(listIP[target])+"/json"
        data = '{"seg":{"i":['
        for i in range(start, self.LED_PER_TARGET - 1):
            data = data + str(i)+', "' + color+'" ,'
        data = data + str(self.LED_PER_TARGET)+',"'+color +'"]}}'
        data_J = json.loads(data)
        #print(data_J)
        response = requests.post(url, headers=headers, data=json.dumps(data_J))
        print(response.json())

    def fillRoom(self, color, room):
        """Instantly change color of all lights in a room"""
        start = room*self.NUM_TARGETS_ROOM
        for i in range(start, start + 8):
            url = "http://"+str(listIP[i])+"/json"
            data = '{"seg":{"i":['
            for j in range(0 , 44):
                data = data + str(j)+', "' + color+'" , '
            data = data + '45,"0000FF"'
            data = data + ']}}'
            data_J = json.loads(data)
            #print(url)
            #print(data_J)
            response = requests.post(url, headers=headers, data=json.dumps(data_J))
            print(response.json())

    def resetAll(self):
        """Reset all of the LEDs in the smart box"""
        for i in range(len(listIP)):
            url = "http://"+str(listIP[i])+"/json"
            data = '{"seg":{"i":['
            for j in range(0 , 44):
                data = data + str(j)+', "000000" , '
            data = data + '45,"0000FF"'
            data = data + ']}}'
            data_J = json.loads(data)
            #print(url)
            #print(data_J)
            response = requests.post(url, headers=headers, data=json.dumps(data_J))
            print(response.json())
            

    def fillTargetSegment(self, color, target, segment):
        """Fill a segment of a target: (0) first ten (1) next thirteen (2) last ten"""
        start = 0
        url = "http://"+str(listIP[target])+"/json"

        data = '{"seg":{"i":['
        if(segment == 0):
            for i in range(start , 13):
                data = data + str(i)+', "' + color+'" ,'
            data = data + str(14)+',"'+color +'"]}}'
        if(segment == 1):
            for i in range(start + 15 , 28):
                data = data + str(i)+', "' + color+'" ,'
            data = data + str(29)+',"'+color +'"]}}'
        if(segment == 2):
            for i in range(start + 29 , 43):
                data = data + str(i)+', "' + color+'" ,'
            data = data + str(44)+',"'+color +'"]}}'
        data_J = json.loads(data)
        #print(data_J)
        response = requests.post(url, headers=headers, data=json.dumps(data_J))
        print(response.json())
