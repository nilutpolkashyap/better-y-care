from PyQt5.QtWidgets import QMainWindow, QApplication, QLCDNumber, QProgressBar, QLabel, QComboBox, QPushButton
from PyQt5 import uic
import sys
from PyQt5.QtCore import QTime, QTimer
from datetime import datetime
import psutil
import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())
port_list = []
value = ""

for p in ports:
	port_list.append(p[0])

def convertTime(seconds):
	minutes, seconds = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)
	return "%d:%02d:%02d" % (hours, minutes, seconds)

class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()

		# Load the ui file
		uic.loadUi("battery_value.ui", self)

		# Define our widgets
		self.lcd = self.findChild(QLCDNumber, "lcdNumber1")	
		
		self.timelcd = self.findChild(QLCDNumber, "lcdNumber2")	
		
		self.pbar = self.findChild(QProgressBar, "progressBar")
		
		self.power_status = self.findChild(QLabel, "label4")
		self.power_status.setText("NO")

		self.com_label = self.findChild(QLabel, "label5")

		self.button = self.findChild(QPushButton, "pushButton")

		self.port_box = self.findChild(QComboBox, "comboBox")
		self.port_box.addItems(port_list)

		value = self.port_box.currentText()
		self.com_label.setText(value)
		# print(type(value))

		self.button.clicked.connect(self.clickme)
		
		self.pbar.setStyleSheet("QProgressBar "
                          "{"
                          "background-color : rgb(255, 53, 53);" 
                          "border : 3px solid black;"
                          "}"
                          "QProgressBar::chunk"
                          "{"
                          "background-color : rgb(61, 255, 58);"
                          "border :1px solid red;"
                          "}"
                          )

		# Create A Timer
		self.timer = QTimer()
		self.timer.timeout.connect(self.lcd_number)
		self.timer.timeout.connect(self.plug_check)

		# Start the timer and update every second
		self.timer.start(1000)

		# Call the lcd function
		self.lcd_number()

		# Show The App
		self.show()
		
		
	def clickme(self):
		value = self.port_box.currentText()
		self.com_label.setText(value)
	
	def lcd_number(self):
		# Get the time
        # time = datetime.now()
        # formatted_time = time.strftime("%I:%M:%S %p")
		
		battery = psutil.sensors_battery()
		percent = battery.percent

		# self.port_box.clear()

		# Set number of LCD Digits
		# self.lcd.setDigitCount(12)
		# Make Text Flat (no white outline)
		self.lcd.setSegmentStyle(QLCDNumber.Flat)

		# Display The Time
		self.lcd.display(percent)
		
		
	def plug_check(self):
		battery = psutil.sensors_battery()
		plugged = battery.power_plugged
		
		if plugged:
			plug = 1
			self.power_status.setText("YES")
			time = "00:00:00"
			self.timelcd.display(time)  
			
		else:
			plug = 0
			self.power_status.setText("NO")
			time = convertTime(battery.secsleft)
			self.timelcd.display(time)         
			
		self.pbar.setValue(plug)
	
# Initialize The App
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()


