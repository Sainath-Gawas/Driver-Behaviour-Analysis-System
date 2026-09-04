import RPi.GPIO as GPIO
import time

# PIN SETUP
TRIG = 23
ECHO = 24

brake_btn = 8
horn_btn = 25

green = 16
yellow = 20
red = 21
buzzer = 12

# PARAMETERS
DIST_THRESHOLD = 15   # cm
INTERVAL = 30         # seconds

# Weights
W_DISTANCE = 0.45
W_BRAKE = 0.40
W_HORN = 0.15

SCALE = 5
HORN_INTERVAL = 0.5  # seconds

# GPIO SETUP
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(brake_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(horn_btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(yellow, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)

def get_distance():
    GPIO.output(TRIG, GPIO.LOW)
    time.sleep(0.000002)
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    start_time = time.time()

    # Wait for ECHO to become HIGH
    while GPIO.input(ECHO) == GPIO.LOW:
        pulse_start = time.time()
        if time.time() - start_time > 0.04:
            return 100

    # Wait for ECHO to become LOW
    while GPIO.input(ECHO) == GPIO.HIGH:
        pulse_end = time.time()
        if time.time() - start_time > 0.04:
            return 100

    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 34300) / 2
    return distance


def set_output(score):
    if score >= 85:
        GPIO.output(green, GPIO.HIGH)
        GPIO.output(yellow, GPIO.LOW)
        GPIO.output(red, GPIO.LOW)
        GPIO.output(buzzer, GPIO.LOW)

    elif score >= 70:
        GPIO.output(green, GPIO.LOW)
        GPIO.output(yellow, GPIO.HIGH)
        GPIO.output(red, GPIO.LOW)
        GPIO.output(buzzer, GPIO.LOW)

    else:
        GPIO.output(green, GPIO.LOW)
        GPIO.output(yellow, GPIO.LOW)
        GPIO.output(red, GPIO.HIGH)
        GPIO.output(buzzer, GPIO.HIGH)

# MAIN
try:
    while True:
        distance_count = 0
        brake_count = 0
        horn_count = 0

        brake_flag = False
        distance_flag = False

        last_horn_time = 0
        start = time.time()

        while (time.time() - start) < INTERVAL:

            distance = get_distance()
            if distance < DIST_THRESHOLD:
                if not distance_flag:
                    distance_count += 1
                    distance_flag = True
            else:
                distance_flag = False

            # Brake
            if GPIO.input(brake_btn) == GPIO.LOW:
                if not brake_flag:
                    brake_count += 1
                    brake_flag = True
                    time.sleep(0.05)
            else:
                brake_flag = False

            # Horn
            current_time = time.time()
            if GPIO.input(horn_btn) == GPIO.LOW:
                if current_time - last_horn_time > HORN_INTERVAL:
                    horn_count += 1
                    last_horn_time = current_time

            time.sleep(0.2)


        # SCORING
        penalty = (W_DISTANCE * distance_count) + \
                  (W_BRAKE * brake_count) + \
                  (W_HORN * horn_count)

        score = 100 - (penalty * SCALE)
        if score < 0:
            score = 0


        # DISPLAY RESULT
        print("Distance:", distance_count,
              "Brake:", brake_count,
              "Horn:", horn_count,
              "Score:", round(score, 2))
        set_output(score)


except KeyboardInterrupt:
    GPIO.cleanup()
    print("Program stopped.")