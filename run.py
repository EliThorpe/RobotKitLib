# python run.py robot.py

import sys
import robot
import time
from networktables import NetworkTables
import threading
import logging


logging.basicConfig(level=logging.DEBUG)

ip = "10.10.10.10" #ip address



class main():
    def __init__(self):
         """
        Construct robot disconnect, and powered on
        """
        self.r = robot.MyRobot()
        self.current_mode = ""
        self.disabled = True
        
    def connect(self):
        """
        Connect to robot NetworkTables server
        """
        NetworkTables.initialize(server=ip)
        NetworkTables.addConnectionListener(self.connectionListener, immediateNotify=True)


    def connectionListener(self, connected, info):
        """
        Setup the listener to detect any changes to the robotmode table
        """
        print(info, "; Connected=%s" % connected)
        sd = NetworkTables.getTable("RobotMode")
        sd.addEntryListener(self.valueChanged)

   
    def valueChanged(self, table, key, value, isNew):
        """
        Check for new changes and use them
        """
        print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key, value, isNew))
        if(key == "Mode"):
            self.setupMode(value)
        if(key == "Disabled"):
            self.disabled = value
        
    def start(self):    
        self.r.robotInit()

    def setupMode(self, m):
        """
        Run the init function for the current mode
        """
        self.current_mode = m

        if m == "Teleop":
            self.r.teleopInit()
        elif m == "Auton":
            self.r.autonomousInit()

    def auton(self):
        self.r.autonomousPeriodic
        time.sleep(0.02)

    def teleop(self):
        self.r.teleopPeriodic()
        time.sleep(0.02)

    def mainLoopThread(self):
        """
        Loop the mode function
        """
        while not self.disabled:
            if self.current_mode == "Auton":
                self.auton()
            elif self.current_mode == "Teleop":
                self.teleop()
            





if __name__ == "__main__":
    m = main()
    m.connect()

    x = threading.Thread(target=m.mainLoopThread)
    x.start()


    
