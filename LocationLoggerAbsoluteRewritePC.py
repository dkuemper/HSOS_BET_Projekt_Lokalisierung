import serial
import time
import logging
import atexit

import paho.mqtt.publish as publish
MQTT_SERVER = "131.173.119.76"
MQTT_PATH = "test/test0"


@atexit.register
def goodbye():
    ser.write(b'lep\r')

# lep sendet Position (aufgr. des C-Moduls) bei jedem DWM Event. Wird abgebrochen, laeuft lep noch weiter. Beim naechsten Skriptaufruf stoppt das Skript das bereits laufende lep, anstatt das "eigene" zu starten. Loesung: Wird das Skript abgebrochen, wird das laufende "lep" Kommando beendet.
# keine Umlaute in den Kommentaren Schreiben!
# Aktuell fuer Listener konfiguriert

logger = logging.getLogger('locationLogger')
hdlr = logging.FileHandler('/home/pi/PythonLogger/loggerLocation.log','w')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

counter = 0
print('Test')
time.sleep(1)
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200,
    timeout=0.1
)
#Fuer VM Anwendung port ttyACM0
time.sleep(1)
ser.write(b'\r')
ser.write(b'\r')
#Wechsel in den UART Shell Modus braucht etwas Zeit
time.sleep(3)
ser.write(b'lep\r')	#Start des LEP Aufrufs
time.sleep(0.5)
while True:
	res = ser.readline()
	counter += 1
	if len(res)>12:
		if "dwm" not in res:
			publish.single(MQTT_PATH, res, hostname=MQTT_SERVER)
			logger.info('%i: %s',counter,res)
			ser.write(b'av\r')
			res = ser.readline()
			res = ser.readline()
			logger.info('%i: %s',counter,res)
			publish.single(MQTT_PATH, res, hostname=MQTT_SERVER)
