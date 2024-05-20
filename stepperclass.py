from time import sleep 
import RPi.GPIO as GPIO
from math import pi, cos, sin

GPIO.setwarnings(False)
GPIO.setmode (GPIO.BCM)

class Stepper():
    __curent_position = 0
    __target_position = 0

    def __init__(self, dirPin:int, pulPin:int, limitPin:int=None, gearRatio=1, ppr=6400, enaPin=None):
        self.dirPin = dirPin
        self.pulPin = pulPin
        self.limitPin = limitPin
        self.gearRatio = gearRatio
        self.ppr = ppr
        self.enaPin = enaPin
        GPIO.setup(dirPin, GPIO.OUT)
        GPIO.setup(pulPin, GPIO.OUT)
        GPIO.setup(limitPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.limitPin, GPIO.RISING, callback=self.setHome)

    def goTo(self, angle):
        """ Rotate stepper motor to a specific angle from current angle """
        self.__target_position = angle
        change_in_value = self.__curent_position - self.__target_position
        self.rotate(change_in_value)

    def home(self):
        """ Rotates motor until limit switch """
        self.rotate(angle=-160, speed_factor=1)
    
    def setHome(self, channel):
        self.rotate(0)
        self.update_position(-160)

    def rotate(self, angle:float, speed_factor:float=5):
        """Rotate stepper motor by an angle at a given speed.
        
        Args:
            angle (float): Angle to rotate to (in degrees). CCW positive, CW negative
            speed (float): Speed of rotation default 5 (1-5 where 1 = .001 and 5 = .00000001).
        """
        self.__target_position = angle
        steps = self.degree_to_steps(abs(angle))
        speed = .001 / 10 ** speed_factor
        if angle < 0:
            self.clockwise(steps, speed)
            self.update_position(angle)
        else:
            self.c_clockwise(steps, speed)
            self.update_position(angle)

    def degree_to_steps(self, degrees:float) -> int:
        """ Converts degrees to steps based on PPR and gear ratio 
        Args:
            degree(float) - Desired angle in degrees
        Returns:
            int: equivalent steps for given angle
            """
        steps_per_revolution = self.ppr * self.gearRatio
        steps = int(degrees / 360 * steps_per_revolution)
        return steps

    def easing(self, step:int, total_steps:int) -> float:
        """ Easing function to accelerate and decelerate motion 
        Args:
            step: current step
            total_steps: total number of steps
        Returns:
            float: easing factor"""
        t = step / total_steps
        # cosine = (1 - cos(pi * t)) / 2
        sinu = sin((t - 0.5) * pi / 2)
        return abs(sinu)
    
    def update_position(self, angle):
        self.__curent_position = angle

    def clockwise(self, nsteps:int, base_speed:float) -> None:
        """ Turns steppers clockwise.
        Params:
            nsteps: int - Number of steps
            base_speed: float - Delay between pulses """
        GPIO.output(self.dirPin, GPIO.HIGH)
        for x in range(nsteps):
            ease_factor = self.easing(x, nsteps)
            step_delay = base_speed *  ease_factor
            GPIO.output(self.pulPin, GPIO.HIGH)
            sleep(step_delay)
            GPIO.output(self.pulPin,GPIO.LOW)
            sleep(step_delay)
            
    def c_clockwise(self, nsteps:int, base_speed:float) -> None:
        """Turns steppers counterclockwise.
         Params:
            nsteps: int - Number of steps
            base_speed: float - Delay between pulses """
        GPIO.output(self.dirPin, GPIO.LOW)
        for x in range(nsteps):
            ease_factor = self.easing(x, nsteps)
            step_delay = base_speed *  ease_factor
            GPIO.output(self.pulPin, GPIO.HIGH)
            sleep(step_delay)
            GPIO.output(self.pulPin,GPIO.LOW)
            sleep(step_delay)


        
Drake = Stepper(dirPin=20, pulPin=16, ppr=3200)        # joint 0
Kendrick = Stepper(dirPin=26, pulPin=19, gearRatio=10) # joint 1
Kendrick.rotate(direction=False, angle=90, speed_factor=6)


#input('ready')


#Kendrick.rotate(direction=True, angle=90, speed_factor=6)

#Kendrick.rotate(direction=False, angle=90, speed_factor=6)

#Kendrick.rotate(direction=True, angle=90, speed_factor=6)