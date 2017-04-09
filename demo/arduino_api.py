import warnings
import serial
import serial.tools.list_ports


class ArduinoConnection:
    def __init__(self):
        self.ser = ArduinoConnection.get_arduino_serial()

    @staticmethod
    def get_arduino_serial():
        arduino_ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if 'GENUINO' in p.description
        ]

        if not arduino_ports:
            raise IOError("No Arduino found")
        if len(arduino_ports) > 1:
            warnings.warn('Multiple Arduinos found - using the first')

        ser = serial.Serial(arduino_ports[0])
        return ser

    def send_command(self, cmd):
        self.ser.write(str.encode(cmd))


class CrowdLessArduinoConnection(ArduinoConnection):
    def __init__(self):
        ArduinoConnection.__init__(self)
        self.ser.write(str.encode('0'))

    def green_door(self, door):
        self.send_command(str(door))


    def red_door(self, door):
        self.send_command(str(door+4))

    def green_all_doors(self):
        self.send_command('0')



