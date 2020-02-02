from pyproj import Geod
import json






def dms(dd,lat=True):
    is_positive = dd >= 0
    suf = ("N " if lat else "E ") if is_positive else ("S " if lat else "W ")
    dd = abs(dd)
    minutes,seconds = divmod(dd*3600,60)
    degrees,minutes = divmod(minutes,60)
    degrees = degrees if is_positive else -degrees
    return (suf+str(int(degrees))+"°"+str(int(minutes))+'\''+str(round(seconds,3))+"\"")

def to_json(obj):
    json = {}
    for attr in dir(obj):
        if not callable(getattr(obj, attr)) and not attr.startswith("__") and obj.__dict__[attr]:
            json[attr] = obj.__dict__[attr]
    return json


# CLASSES

class Ship:

    def __init__(self, name="Ship"):
        self.name = name
        self.lat = None
        self.lon = None
        self.hdg = None
        self.sog = None

    def __repr__(self):
        return "Ship: "+json.dumps(to_json(self))


class Target:

    def __init__(self, name="Target",mmsi=""):
        self.name = name
        self.mmsi = mmsi
        self.lat = None
        self.lon = None
        self.hdg = None
        self.sog = None

    def __repr__(self):
        return "Target: "+json.dumps(to_json(self), indent=2, sort_keys=True)


class Rotator:

    def __init__(self, name="Target",mmsi=""):
        self.moving = False
        self.brg = 0
        self.drc = 0
        self.trc = 0
        self.err = 0

    def __repr__(self):
        return "Rotator: "+json.dumps(to_json(self), indent=2, sort_keys=True)

class Settings:

    def __init__(self, rmc_ip="",rmc_port=0,ais_ip="",ais_port=0,freq=1,ship=None,target=None,rotator=None):
        self.rmc_ip = rmc_ip
        self.rmc_port = rmc_port
        self.ais_ip = ais_ip
        self.ais_port = ais_port
        self.freq = freq
        self.ship = ship
        self.target = target
        self.rotator = rotator

    def __repr__(self):
        return "Settings:\n"+json.dumps(self.export(), indent=2, sort_keys=False)

    def export(self):
        sts = {"settings":{}}
        sts["settings"]["rmc_ip"] = self.rmc_ip
        sts["settings"]["rmc_port"] = self.rmc_port
        sts["settings"]["ais_ip"] = self.ais_ip
        sts["settings"]["ais_port"] = self.ais_port
        sts["settings"]["freq"] = self.freq
        if self.ship:
            sts["ship"] = to_json(self.ship)
        if self.target:
            sts["target"] = to_json(self.target)
        if self.rotator:
            sts["rotator"] = to_json(self.rotator)
        return sts

    def save(self,filename):
        with open("./lib/settings/"+filename+".json","w") as f:
            f.write(json.dumps(self.export(), indent=2, sort_keys=True))

    def load(self,filename):
        with open("./lib/settings/"+filename+".json","r") as f:
            try:
                data = json.load(f)
            except:
                return "JSON file parse error"

            try:
                for unit, attrs in data.items():
                    obj = {"settings":self,"ship":self.ship,"target":self.target,"rotator":self.rotator}[unit]
                    
                    if not obj:
                        obj = eval(unit.title())()

                    for key, value in attrs.items():
                        obj.__dict__[key] = value

                    self.__dict__[unit] = obj

            except:
                return "Settings file corrupt"
                



