
########### AutoBlindz Program #########

### Hookup List ###

    # Light Sensor to A0
    # Potentiometer to A1
    # Button to D3

    # Red H-bridge wire to pin 32
    # Black H-brideg wire to pin 36

## DEBUGGING ##

    # Blue LED to D5
    # Red LED to D6

import sys
import time
import grovepi
from Adafruit_PWM_Servo_Driver import PWM
import RPi.GPIO as GPIO





def startup():
    #This function is the first to run.
    global light_sensor_pin, relay_pin, potentiometer_pin, button_pin, led1_pin, led2_pin, mototrFw_pin, motorBk_pin, strText

    #GPIO.setwarnings(False)
    
    light_sensor_pin = 0
    potentiometer_pin = 1
    button_pin = 3
    led1_pin = 5 #for testing
    led2_pin = 6 #for testing
    
    motorFw_pin=33
    motorBk_pin=35

    strText = "First Run"

    grovepi.pinMode(potentiometer_pin,"INPUT")
    grovepi.pinMode(button_pin,"INPUT")
    grovepi.pinMode(led1_pin,"OUTPUT") #for testing
    grovepi.pinMode(led2_pin,"OUTPUT") #for testing
    grovepi.pinMode(light_sensor_pin,"INPUT")

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(motorFw_pin, GPIO.OUT)
    GPIO.setup(motorBk_pin, GPIO.OUT)

    time.sleep(1)
    checkTxt() #Get initial Settings

def powerupRestart():
    #This closes the shutters and blinds so the machine knows where the closed position is.

    #Check if the servos have the blinds closed.
        #if not, then close them.

    #Check if the trigger is pressed.
        #if not, then move the shutters until it is. Once it is, stop.

    n=1
    
def changeSettings(pt):
    #This function changes the settings
    global priority, light_thr, sch_blin, sch_shut
    
    priority = int(pt[1]) # "0" means Manual Controls, "1" means light sensative, "2" means schedule, and "3" means temperature 
    light_thr = int(pt[2]) # A number from 0 to 400
    sch_blin = pt[3] # The looveres. A list of times and values. ex: [[6,-100],[13:00,200],[18:30,0]]
    sch_shut = pt[4] # The shutters. A list of times and values. ex: [[6,-100],[13:00,200],[18:30,0]]

def checkTxt():
    #This function compares the contents settings.txt had with the contents it has now.
    global strText

    strPath = "settings.txt"
    fh = open(strPath)
    strTextNew = fh.read()
#    print("strTextNew = ",strTextNew)

    if(strTextNew != strText):
        pt = strTextNew.split("&") #Parsed Text
        strText = strTextNew
        changeSettings(pt)

def priorityLoop():
    #This is the main function. It is an infinite loop that checks priority Based on what the priority is, it does stuff.
    global priority
    
    while True:
        checkTxt() #Check for updates
        
        if (priority == 0):
            try:
                manual()
                    
            except IOError:
        	print("Error in manual")

            except KeyboardInterrupt:
                print("\nCaught KeyboardInterrupt, cleaning GPIO pins.\nGPIO mode before cleanup: "+str(GPIO.getmode()))
                GPIO.cleanup()
                print("GPIO mode after cleanup: "+str(GPIO.getmode())+"\nExiting Now. Thank you for your patience.")
                sys.exit()
        	
        elif (priority == 1):
            try:
                light()
                    
            except IOError:
        	print("Error in temperature")

            except KeyboardInterrupt:
                print("\nCaught KeyboardInterrupt, cleaning GPIO pins.\nGPIO mode before cleanup: "+str(GPIO.getmode()))
                GPIO.cleanup()
                print("GPIO mode after cleanup: "+str(GPIO.getmode())+"\nExiting Now. Thank you for your patience.")
                sys.exit()
        	
        elif (priority == 2):
            try:
                schedule()
                    
            except IOError:
        	print("Error in schedule")

            except KeyboardInterrupt:
                print("\nCaught KeyboardInterrupt, cleaning GPIO pins.\nGPIO mode before cleanup: "+str(GPIO.getmode()))
                GPIO.cleanup()
                print("GPIO mode after cleanup: "+str(GPIO.getmode())+"\nExiting Now. Thank you for your patience.")
                sys.exit()

        else:
            print("The priority is not 0, 1 or 2. It is",priority)

def manual():
    #This is a program that allows you to control the blinds with a knob.
    global potentiometer_pin, button_pin, led1_pin, led2_pin

    adc_ref = 5 #Reference voltage of ADC is 5v
    grove_vcc = 5 #Vcc of the grove interface is normally 5v
    full_angle = 300 #Full value of the rotary angle is 300 degrees, as per it's specs (0 to 300) 
    sensor_value = grovepi.analogRead(potentiometer_pin)  #Read sensor value from potentiometer
    voltage = round((float)(sensor_value) * adc_ref / 1023, 2) #Calculate voltage
    degrees = round((voltage * full_angle) / grove_vcc, 2) #Calculate rotation in degrees (0 to 300)  

    #This will be replaced with a distance measurment
    brightness = int(degrees / full_angle * 255) #Calculate LED brightess (0 to 255) from degrees (0 to 300)

    button_test = grovepi.digitalRead(button_pin) #Is the button on or off? On will control the blinds, off will control the shutters
    if (button_test==1): #Give PWM output to LED
        grovepi.analogWrite(led1_pin,brightness) #Move blinds
    else:
        grovepi.analogWrite(led2_pin,brightness) #Move shutters

    print("sensor_value =", sensor_value, " voltage =", voltage, " degrees =", degrees, " brightness =", brightness)

def light():
    #This is a program that regulates the blinds due to a temeperature threshold.
    global light_thr, led1_pin, led2_pin

    # Get sensor value
    sensor_value = grovepi.analogRead(light_sensor_pin)

    # Calculate resistance of sensor in K
    resistance = (float)(1023 - sensor_value) * 10 / sensor_value

    if (resistance > light_thr):
        # Send HIGH to switch on Relay
        grovepi.digitalWrite(led1_pin,1)
    else:
        # Send LOW to switch off Relay
        grovepi.digitalWrite(led1_pin,0)

    print("max_threshold: ",light_thr, "sensor_value =", sensor_value, " resistance =", resistance)
    time.sleep(.5)

def schedule():
    #This is a program that moves the blinds when it is a certain time every 5 seconds.
        ### For the final project, change this to a 1 second delay? or none?
    global sch_blin, sch_shut

    #Get current time:
    localtime = time.localtime(time.time())
    print(localtime[3],":",localtime[4])
 #   print(sch_blin)

#    sch_blin_p1 = sch_blin.split("%") #Parsed once. This gives a list where each element contains the hour, time, and amnt as one element.
#    plans = len(sch_blin_p1) #How many milestones there are planned
#    for i in range(plans): #If any if statement is false, then it skips the element and goes to the next one.
#        sch_blin_p2 = sch_blin_p1[i].split("$") #Parsed twice. This gives a list where the first element is hour:minutes and the other is amnt.
#        sch_blin_p3 = sch_blin_p2[0].split(":") #Parsed thrice. This gives a list where the first element is hours and the second is minutes.
#        print("compare hours: ",localtime[3], int(sch_blin_p3[0]))
#        if (localtime[3]>=int(sch_blin_p3[0])):
#            #This means that the current time hour step has passed. Now, check if the minutes have passed.
#            print("yes hours")

#            print("compare minutes: ",localtime[4], int(sch_blin_p3[1]))
#            if (localtime[4]>=int(sch_blin_p3[1])):
                #This means that the current time minute step has passed as well. Now, check if the next in the list has passed, starting with the hour.
#                print("yes minutes")

#               if i+1<plans:
                    #This means that another plan does exist.
#                    sch_blin_p2_next = sch_blin_p1[i+1].split("$")
#                    sch_blin_p3_next = sch_blin_p2[0].split(":")
#                    print("compare next minutes: ",localtime[3], int(sch_blin_p3_next[0]))
#                    if localtime[3]<=int(sch_blin_p3_new[1])):
                        #This means that the next plan has not happened yet, and so our current element is the plan that needs to be met.
#                        print("yes current minutes is the correct one")
#                        if localtime[3]<=int(sch_blin_p3_new[0])):
                            #This means that the hour is also correct.
#                            print("This is the correct plan to use.")
#                        else:
#                            print("next hours incorrect.")
#                    else:
#                        print("next minutes incorrect.")
#                else:
#                    print("This is the last plan.")
                    #Make sure these are the current settings.
#            else:
#                print("no minutes")
#        else:
#            print("no hours")
#    time.sleep(1)
#    print("\n")

    #The place we want to be is sch_blin[i][1], when sch_blin[i][0]is less than "localtime[3]:localtime[4]".
    #check if you are at the current sch_blin[i][1].
        #If you are not, then move there.









            

def motorForward(x):
    #This turns the motor CCW for x time steps, then stops.
    global motorFw_pin, motorBk_pin
    
    GPIO.output(motorFw_pinStepPinForward, GPIO.HIGH)
    print("forwarding running  motor")
    time.sleep(x)
    GPIO.output(motorFw_pin, GPIO.LOW)

def motorReverse(x):
    #This turns teh motor CW for x time steps, then stops.
    GPIO.output(motorBk_pin, GPIO.HIGH)
    print("backwarding running motor")
    time.sleep(x)
    GPIO.output(motorBk_pin, GPIO.LOW)

def moveServo(direction):
    #This moves a servo up or down.

    # Initialise the PWM device using the default address
    pwm = PWM(0x40)

    # Note if you'd like more debug output you can instead run:
    #pwm = PWM(0x40, debug=True)

    servoMin = 150  # Min pulse length out of 4096
    servoMax = 600  # Max pulse length out of 4096

    pwm.setPWMFreq(60)  # Set frequency to 60 Hz

    if (direction=="up"):
        pwm.setPWM(0, 0, servoMax)
    else:
        pwm.setPWM(0, 0, servoMin)



startup()
powerupRestart()
priorityLoop()











