from machine import Pin, time_pulse_us
import time

#PIN SETUP
TRIG = Pin(3, Pin.OUT)
ECHO = Pin(2, Pin.IN)

brake_btn = Pin(14, Pin.IN, Pin.PULL_UP)
horn_btn = Pin(15, Pin.IN, Pin.PULL_UP)

green = Pin(16, Pin.OUT)
yellow = Pin(17, Pin.OUT)
red = Pin(18, Pin.OUT)
buzzer = Pin(19, Pin.OUT)

#PARAMETERS
DIST_THRESHOLD = 15   # cm
INTERVAL = 30         # seconds

# Weights
W_DISTANCE = 0.45
W_BRAKE = 0.40
W_HORN = 0.15

SCALE = 5

def get_distance():
    TRIG.low()
    time.sleep_us(2)
    
    TRIG.high()
    time.sleep_us(10)
    TRIG.low()

    duration = time_pulse_us(ECHO, 1)
    
    if duration < 0:
        return 100  # fallback if error

    distance = (duration * 0.0343) / 2
    return distance

def set_output(score):
    if score >= 85:
        green.value(1)
        yellow.value(0)
        red.value(0)
        buzzer.value(0)

    elif score >= 70:
        green.value(0)
        yellow.value(1)
        red.value(0)
        buzzer.value(0)

    else:
        green.value(0)
        yellow.value(0)
        red.value(1)
        buzzer.value(1)

#MAIN LOOP
while True:
    distance_count = 0
    brake_count = 0
    horn_count = 0
    brake_flag=False
    distance_flag=False
    last_horn_time = 0
    HORN_INTERVAL = 0.5   # seconds
    start = time.time()

    while (time.time() - start) < INTERVAL:

        distance = get_distance()

        if distance < DIST_THRESHOLD:
            if not distance_flag:
                distance_count += 1
                distance_flag = True
        else:
            distance_flag = False

        if brake_btn.value() == 0:
            if not brake_flag:
                brake_count += 1
                brake_flag = True
                time.sleep(0.05)
        else:
            brake_flag = False

        # Horn press
        current_time = time.time()

        if horn_btn.value() == 0:
            if current_time - last_horn_time > HORN_INTERVAL:
                horn_count += 1
                last_horn_time = current_time

        time.sleep(0.2)

    #SCORING
    penalty = (W_DISTANCE * distance_count) + \
              (W_BRAKE * brake_count) + \
              (W_HORN * horn_count)

    score = 100 - (penalty * SCALE)

    if score < 0:
        score = 0

    print("Distance:", distance_count,
          "Brake:", brake_count,
          "Horn:", horn_count,
          "Score:", round(score, 2))

    #display score
    set_output(score)
