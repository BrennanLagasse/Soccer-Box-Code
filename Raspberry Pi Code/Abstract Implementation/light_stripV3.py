import requests
import json
import concurrent.futures

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

headers = {
    "Content-Type": "application/json"
}

print(listIP[0])
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

    def colorWipe(self, targets, index):
        """Turn off last light of given index at all listed targets (simultaneous is key to prevent repeat calls to show)"""
        print("colorWipe")
        for i in range(0, len(targets)):
            try:
                url = "http://"+str(listIP[targets[i]])+"/update?function=colorWipe&index="+str(index)+"&color=000000"
                response = requests.get(url)
                print(response.text)
            except Exception as e:
                print(e)

    def fillTarget(self, color, target):
        """Instantly change color of all lights in target range. This is where rerouting occurs"""
        print("fillTarget")
        try:
            url = "http://"+str(listIP[target])+"/update?function=fillTarget&index=0&color="+str(color)
            response = requests.get(url)
            print(response.text)
        except:
            pass

    def fillRemainingTarget(self, color, target, index):
        """Instantly change all remaining lights on a target to a different color"""
        print("fillRemainingTarget")
        try:
            url = "http://"+str(listIP[target])+"/update?function=fillTarget&index="+str(index)+"&color="+str(color)
            response = requests.get(url)
            print(response.text)
        except Exception as e:
            print(e)

    def fillRoom(self, color, room):
        """Instantly change color of all lights in a room"""
        print("fillRoom")
        start = room*self.NUM_TARGETS_ROOM
        for i in range(start, start + 8):
            try:
                url = "http://"+str(listIP[i])+"/update?function=fillTarget&index=0&color="+str(color)
                response = requests.get(url)
                print(response.text)
            except Exception as e:
                print(e)

    def resetAll(self):
        """Reset all of the LEDs in the smart box"""
        print("resetAll")
        for i in range(len(listIP)):
            try:
                url = "http://"+str(listIP[i])+"/update?function=fillTarget&index=0&color=000000"
                response = requests.get(url)
                print(response.text)
            except Exception as e:
                print(e)

    def fillTargetSegment(self, color, target, segment):
        """Fill a segment of a target: (0) first ten (1) next thirteen (2) last ten"""
        print("fillTargetSegment")
        url = "http://"+str(listIP[target])+"/json"
        try:
            url = "http://"+str(listIP[target])+"/update?function=fillTargetSegment&index="+str(segment)+"&color="+str(color)
            response = requests.get(url)
            print(response.text)
        except Exception as e:
            print(e)
