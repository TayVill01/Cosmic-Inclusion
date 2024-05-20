from gpiozero import Servo
from time import sleep, time
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory('127.0.0.1')

class CustomServo(Servo):
    def __init__(self, *args, initial_value, **kwargs):
        super().__init__(*args, initial_value=initial_value, **kwargs)
        self._current_angle = self.value_to_angle(initial_value)  # Initialize current angle

    @property
    def angle(self):
        """ Convert the servo value (-1 to 1) to an angle (0 to 270 degrees) """
        return (self.value - (-1)) * (270 - 0) / (1 - (-1)) + 0

    @angle.setter
    def angle(self, angle):
        """ Convert the angle (0 to 270 degrees) to the servo value (-1 to 1) """
        self.value = (angle - 0) * (1 - (-1)) / (270 - 0) + (-1)
        self._current_angle = angle

    def value_to_angle(self, value):
        """ Convert the servo value (-1 to 1) to an angle (0 to 270 degrees) """
        return (value - (-1)) * (270 - 0) / (1 - (-1)) + 0

    def goTo(self, target_angle, duration=3):
        self._current_angle = self.angle  # Ensure current angle is up to date
        self.target_angle = target_angle
        start_time = time()
        end_time = start_time + duration

        while time() < end_time:
            elapsed_time = time() - start_time
            progress = elapsed_time / duration
            eased_progress = self.ease_in_out(progress)
            current_angle = self._current_angle + (self.target_angle - self._current_angle) * eased_progress
            self.angle = current_angle
            sleep(0.02)

        # Ensure final position is set correctly
        self.angle = self.target_angle
        self._current_angle = self.target_angle

    def ease_in_out(self, t):
        # Cubic ease-in-out function
        return t * t * t * (t * (t * 6 - 15) + 10)

JermainePin = 21
MetroPin = ENTERNUM
Jermaine = CustomServo(pin=JermainePin, initial_value=.35, min_pulse_width=.0005, max_pulse_width=.0025, pin_factory=factory)
Metro = CustomServo(pin=MetroPin, initial_value=.35, min_pulse_width=.0005, max_pulse_width=.0025, pin_factory=factory)


try:
    target_angle = 90  
    duration = 3  
    Jermaine.goTo(target_angle, duration)
except KeyboardInterrupt:
    print('Program stopped')