#!/usr/bin/python
import RPi.GPIO as GPIO
import sys
import os.path
import time
import datetime
import smtplib
import logging
import platform
import ConfigParser
from subprocess import call


# Set level=logging.DEBUG for all logs. Else set ERROR.
logging.basicConfig(filename='/home/pi/easy/button.log',level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.info('================ NEW RUN ================')
logging.info('Python Version: %s',platform.python_version() )
logging.info('=========================================')

global lastButtonTime
global buttonDelay
global pressed

lastButtonTime = 0
buttonDelay = 1500
pressed = 0


def playNotify():
   config = ConfigParser.ConfigParser()
   config.read('/home/pi/easy/easybutton.cfg')
   notify = config.get ('defaults', 'notify')

   if os.path.isfile(notify):   
      call(["aplay", "-D", "bluealsa", notify])


# ---------------------------------------------------------
# Sends SMS message to any cell phone using gmail smtp gateway
# Use SMS gateway provided by mobile carrier:
#    AT&T:     phonenumber@mms.att.net
#    T-Mobile: phonenumber@tmomail.net
#    Verizon:  phonenumber@vtext.com
#    Sprint:   phonenumber@page.nextel.com
# ---------------------------------------------------------
def SendTxtMsg():

   config = ConfigParser.ConfigParser()
   config.read('/home/pi/easy/easybutton.cfg')

   fromStr = config.get('defaults', 'from')
   toStr = config.get('defaults', 'to')
   subjectStr = 'ButtonPushed'
   bodyStr = datetime.datetime.now().strftime("%A %B %d %I:%M %p")

   messageStr = ("From: %s\r\n" % fromStr
         + "To: %s\r\n" % toStr
         + "Subject: %s\r\n" % subjectStr
         + "\r\n"
         + bodyStr)

   # Establish a secure session with gmail's outgoing SMTP server using your gmail account
   server = smtplib.SMTP( "smtp.gmail.com", 587 )
   server.starttls()
   
   # Using your google account, generate an app password to use here
   server.login( config.get('defaults', 'user'), config.get('defaults','pw') )
   server.sendmail(fromStr, toStr, messageStr)
   server.quit
   logging.info('Button pressed: %s', bodyStr)



# ---------------------------------------------------------
# Remove override flag files.
def Reset():
    if os.path.isfile("/home/pi/easy/stop"):
       os.remove("/home/pi/easy/stop")

# ---------------------------------------------------------
# Invoked when a button press is deteced
def ButtonHandler(channel):
   global lastButtonTime
   global buttonDelay
   global pressed

   input = GPIO.input(1) 
   if (input == 0 and not pressed):
      millis = int(round(time.time() * 1000))
      if ((millis - lastButtonTime) > buttonDelay ):
          lastButtonTime = int(round(time.time() * 1000))
          pressed = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(1, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Button to GPIO1
GPIO.add_event_detect(1, GPIO.BOTH, callback=ButtonHandler)

Reset()

while os.path.isfile("/home/pi/easy/stop") is not True:
   if (pressed):
       SendTxtMsg()
       playNotify()
       pressed = 0

        
   time.sleep(0.2)

logging.info('EasyButton stopping...\n') 
Reset()
GPIO.cleanup()

