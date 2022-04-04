import serial
import re
import demjson

def parseFWInfo(s):
    res = {}
    r = re.compile(r"(^| )([A-Z_]+):")
    for dummy, key in r.findall(s):
        res[key] = re.findall(r"(.+?)( [A-Z_]+:|$)", s[s.find(key) + len(key) + 1:])[0][0]
    return res

class Printer:
    def __init__(self):
        pass

    def open(self, port, baud=115200):
        print('connecting to ' + port)
        self.ser = serial.Serial(port, baud)
        print('connected')
        self.getFirmwareInfo()
    
    def getFirmwareInfo(self):
        self.ser.write(str.encode("M115\n"))

        self.firmwareInfo = parseFWInfo(self.readline())
        if 'MACHINE_TYPE' in self.firmwareInfo:
            self.machine = self.firmwareInfo['MACHINE_TYPE']

        while True:
            line = self.readline()
            if line.startswith('Cap:'):
                key, value = re.search(r"^Cap:([A-Z_]+):(.+)$", line).groups()
                self.firmwareInfo[key] = bool(value)
            elif line.startswith('area:'):
                self.area = demjson.decode(line[5:])
            else:
                print(line)
            if line == 'ok':
                break

        print(self.firmwareInfo)
        print(self.area)

    def close(self):
        print('close')
        self.ser.close()

    def readline(self):
        return self.ser.readline().decode().rstrip('\r\n')

    def send(self, command):
        self.ser.write(str.encode(command + "\n"))
        print(command)
        res = []

        while True:
            line = self.readline()
            print(line)
            if line == 'ok':
                return
            res.append(line)
