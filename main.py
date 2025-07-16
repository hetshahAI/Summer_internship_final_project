#boot.py / main.py
from machine import Pin, ADC, SoftI2C, PWM, deepsleep, reset_cause, DEEPSLEEP_RESET, PWM
import esp32
from esp32 import wake_on_ext1
import ssd1306
import time
import random


# --- Splash Screen ---
def show_startup_screen():
    oled.fill(0)
    oled.text(" Quarky GO", 15, 5)
    oled.text(" v0.0.1", 25, 20)
    oled.show()
    time.sleep(2) # Show for 2 seconds


# --- OLED Setup ---
i2c = SoftI2C(scl=Pin(19), sda=Pin(18))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
oled.write_cmd(0xA0)
oled.write_cmd(0xC0)
show_startup_screen()


# --- Inputs ---
adc = ADC(Pin(36))
adc.atten(ADC.ATTN_11DB)
center_btn = Pin(13, Pin.IN, Pin.PULL_DOWN)

# --- Wake for Sleep Mode ---
wake_pin = Pin(13, mode=Pin.IN, pull=Pin.PULL_DOWN)
wake_on_ext1(pins=(wake_pin,), level=esp32.WAKEUP_ANY_HIGH)

# --- Constants ---
WIDTH, HEIGHT = 128, 32
MENU_ITEMS = ["Sleep Mode", "Servo Control", "Motor Control", "Catch Game", "Dino Game", "Exit"]
VISIBLE_ITEMS = 3
menu_choice = 0

# --- Helper Functions ---
def read_joystick():
    val = adc.read()
    if 3000 < val <= 4095: return 'L'
    if 2000 < val < 2700: return 'D'
    if 1000 < val < 1800: return 'U'
    if 500 < val < 900: return 'R'
    return None

def draw_menu():
    oled.fill(0)
    start = max(0, min(len(MENU_ITEMS) - VISIBLE_ITEMS, menu_choice - 1))
    for i in range(VISIBLE_ITEMS):
        index = start + i
        if index >= len(MENU_ITEMS): break
        prefix = ">" if index == menu_choice else " "
        oled.text(prefix + MENU_ITEMS[index], 5, i * 10)
    draw_scrollbar(start)
    oled.show()

def draw_scrollbar(start_index):
    total = len(MENU_ITEMS)
    if total <= VISIBLE_ITEMS: return
    bar_height = HEIGHT * VISIBLE_ITEMS // total
    bar_pos = HEIGHT * start_index // total
    # Draw top and bottom cap lines
    oled.pixel(WIDTH - 3, 0, 1)
    oled.pixel(WIDTH - 3, HEIGHT - 1, 1)
    # Draw scrollbar
    oled.fill_rect(WIDTH - 3, bar_pos, 2, bar_height, 1)


def show_submenu(choice):
    oled.fill(0)
    oled.text(">Restart" if choice == 0 else " Restart", 5, 5)
    oled.text(">Exit" if choice == 1 else " Exit", 5, 20)
    oled.show()

def joystick_active():
    val = adc.read()
    if center_btn.value(): return True
    if 3000 < val <= 4095 or 2000 < val < 2700 or 1000 < val < 1800 or 500 < val < 900:
        return True
    return False

# --- Sleep Mode ---
def enter_sleep_mode():
    oled.fill(0)
    if reset_cause() == DEEPSLEEP_RESET:
        oled.text("Woke from sleep", 0, 0)
    else:
        oled.text("Power on", 0, 0)
    oled.text("Waiting input...", 0, 10)
    oled.text("Sleep in 30 sec", 0, 20)
    oled.show()
    last_time = time.ticks_ms()
    while True:
        if joystick_active():
            last_time = time.ticks_ms()
        if time.ticks_diff(time.ticks_ms(), last_time) > 30000:
            oled.fill(0)
            oled.text("Sleeping...", 0, 10)
            oled.show()
            time.sleep(2)
            oled.poweroff()
            deepsleep()
        time.sleep(0.1)

# --- Servo Control ---
def run_servo_control_menu():
    submenu = ["Servo 1", "Servo 2"]
    sub_sel = 0
    while True:
        oled.fill(0)
        for i, item in enumerate(submenu):
            prefix = ">" if i == sub_sel else " "
            oled.text(prefix + item, 5, i * 12)
        oled.show()
        dir = read_joystick()
        if dir == 'U': sub_sel = (sub_sel - 1) % len(submenu)
        elif dir == 'D': sub_sel = (sub_sel + 1) % len(submenu)
        elif center_btn.value():
            while center_btn.value(): pass
            run_servo_slider(Pin(22) if sub_sel == 0 else Pin(0))
            break
        time.sleep(0.2)

def run_servo_slider(servo_pin):
    pwm = PWM(servo_pin, freq=50)
    angle = 90

    def angle_to_duty(angle):
        return int((angle / 180 * 2 + 0.5) / 20 * 1023)

    def update_display():
        oled.fill(0)
        oled.text("Angle: " + str(angle), 25, 0)
        bar = int((angle / 180) * 100)
        oled.fill_rect(10, 20, bar, 6, 1)
        oled.rect(10, 20, 100, 6, 1)
        oled.show()

    pwm.duty(angle_to_duty(angle))
    update_display()

    while True:
        dir = read_joystick()
        if dir == 'L' and angle > 0:
            angle = max(0, angle - 10)
            pwm.duty(angle_to_duty(angle))
            update_display()
            time.sleep(0.2)
        elif dir == 'R' and angle < 180:
            angle = min(180, angle + 10)
            pwm.duty(angle_to_duty(angle))
            update_display()
            time.sleep(0.2)
        elif center_btn.value():
            while center_btn.value(): pass
            break

from machine import Pin, PWM
from time import sleep

# motor control
def run_motor_control_menu():
    motor_menu = ["Motor 1", "Motor 2", "Both Motors"]
    sub_sel = 0
    while True:
        oled.fill(0)
        for i in range(len(motor_menu)):
            prefix = ">" if i == sub_sel else " "
            oled.text(prefix + motor_menu[i], 5, i * 12)
        oled.show()

        dir = read_joystick()
        if dir == 'U': sub_sel = (sub_sel - 1) % len(motor_menu)
        elif dir == 'D': sub_sel = (sub_sel + 1) % len(motor_menu)
        elif center_btn.value():
            while center_btn.value(): pass
            if sub_sel == 0:
                run_motor_fade(Pin(27), "Motor 1")     # Motor 1 on GPIO 27
            elif sub_sel == 1:
                run_motor_fade(Pin(32), "Motor 2")     # Motor 2 on GPIO 34
            else:
                run_motor_fade_both(Pin(27), Pin(32)) # Both motors
            break
        sleep(0.2)

def run_motor_fade(pin, name):
    motor = PWM(pin, freq=1000)
    oled.fill(0)
    oled.text(name + " running", 5, 5)
    oled.text("Press Btn to exit", 5, 20)
    oled.show()

    while True:
        # Fade in
        for duty in range(0, 1024, 10):
            motor.duty(duty)
            if center_btn.value():
                while center_btn.value(): pass
                motor.deinit()
                Pin(pin, Pin.OUT).value(0)
                return
            sleep(0.01)
        # Fade out
        for duty in range(1023, -1, -10):
            motor.duty(duty)
            if center_btn.value():
                while center_btn.value(): pass
                motor.deinit()
                Pin(pin, Pin.OUT).value(0)
                return
            sleep(0.01)

def run_motor_fade_both(pin1, pin2):
    motor1 = PWM(pin1, freq=1000)
    motor2 = PWM(pin2, freq=1000)
    oled.fill(0)
    oled.text("Both Motors running", 0, 5)
    oled.text("Press Btn to exit", 5, 20)
    oled.show()

    while True:
        for duty in range(0, 1024, 10):
            motor1.duty(duty)
            motor2.duty(duty)
            if center_btn.value():
                while center_btn.value(): pass
                motor1.deinit()
                motor2.deinit()
                return
            sleep(0.01)
        for duty in range(1023, -1, -10):
            motor1.duty(duty)
            motor2.duty(duty)
            if center_btn.value():
                while center_btn.value(): pass
                motor1.deinit()
                motor2.deinit()
                return
            sleep(0.01)



# --- Catch Game ---
def run_catch_game():
    BASKET_W, BASKET_H, BALL_SIZE, LIFE_BALL_SIZE = 20, 5, 3, 5
    MAX_LIVES, score, lives = 3, 0, 3
    basket_x = WIDTH // 2 - BASKET_W // 2
    ball_x = random.randint(0, WIDTH - BALL_SIZE)
    ball_y, is_life_ball = 0, False
    menu_sel = 0

    def draw_lives(n):
        for i in range(n): oled.fill_rect(i * 8 + 2, 0, 6, 6, 1)

    def draw_score(s): oled.text(str(s), WIDTH - 20, 0)

    def draw_basket(x):
        for i in range(BASKET_H): oled.pixel(x, HEIGHT - BASKET_H + i, 1)
        for i in range(BASKET_W): oled.pixel(x + i, HEIGHT - 1, 1)
        for i in range(BASKET_H): oled.pixel(x + BASKET_W - 1, HEIGHT - BASKET_H + i, 1)

    def draw_ball(x, y, t):
        if t == "life":
            oled.pixel(x+2,y,1); oled.pixel(x+2,y+4,1)
            oled.pixel(x,y+2,1); oled.pixel(x+4,y+2,1)
            oled.pixel(x+2,y+2,1)
        else:
            oled.fill_rect(x, y, BALL_SIZE, BALL_SIZE, 1)

    def show_game_over(s):
        oled.fill(0)
        oled.text("Game Over", 30, 5)
        oled.text("Score: " + str(s), 25, 20)
        oled.show()
        time.sleep(2)

    oled.fill(0)
    oled.text("Catch Game", 25, 5)
    oled.text("Press Btn to Go", 5, 20)
    oled.show()
    while not center_btn.value(): time.sleep(0.1)

    while True:
        oled.fill(0)
        ball_y += 1 if not is_life_ball else 2
        if ball_y >= HEIGHT - BASKET_H:
            if basket_x <= ball_x <= basket_x + BASKET_W:
                if is_life_ball and lives < MAX_LIVES: lives += 1
                elif not is_life_ball: score += 1
            elif not is_life_ball: lives -= 1
            ball_y = 0
            ball_x = random.randint(0, WIDTH - BALL_SIZE)
            is_life_ball = random.randint(0, 9) == 0

        dir = read_joystick()
        if dir == 'L' and basket_x > 0: basket_x -= 4
        elif dir == 'R' and basket_x < WIDTH - BASKET_W: basket_x += 4

        draw_lives(lives)
        draw_score(score)
        draw_basket(basket_x)
        draw_ball(ball_x, ball_y, "life" if is_life_ball else "normal")
        oled.show()
        time.sleep(0.03)

        if lives <= 0:
            show_game_over(score)
            while True:
                show_submenu(menu_sel)
                dir = read_joystick()
                if dir in ['U', 'L']: menu_sel = 0
                elif dir in ['D', 'R']: menu_sel = 1
                if center_btn.value():
                    if menu_sel == 0: return run_catch_game()
                    else: return
                time.sleep(0.2)

# --- Dino Game ---
def run_dino_game():
    GROUND_Y = HEIGHT - 5
    DINO_X = 10
    DINO_W = 8
    DINO_H = 8
    OBSTACLE_W = 4
    OBSTACLE_H = 8
    OBSTACLE_GAP = 60

    dino_y = GROUND_Y - DINO_H
    dino_vy = 0
    is_jumping = False
    obstacle_x = WIDTH
    score = 0
    menu_sel = 0

    def draw_ground():
        for x in range(WIDTH):
            oled.pixel(x, GROUND_Y, 1)

    def draw_dino(y):
        x = DINO_X
        oled.pixel(x+6,y,1)
        oled.fill_rect(x+4,y+1,4,1,1)
        oled.fill_rect(x+3,y+2,6,1,1)
        oled.fill_rect(x+2,y+3,7,1,1)
        oled.fill_rect(x+2,y+4,8,1,1)
        oled.fill_rect(x+1,y+5,7,1,1)
        oled.fill_rect(x+1,y+6,6,1,1)
        oled.pixel(x,y+6,1)
        oled.fill_rect(x,y+7,3,1,1)
        oled.fill_rect(x+5,y+7,2,1,1)

    def draw_obstacle(x):
        oled.fill_rect(x, GROUND_Y - OBSTACLE_H, OBSTACLE_W, OBSTACLE_H, 1)

    def check_collision(y, ox):
        return DINO_X + DINO_W > ox and DINO_X < ox + OBSTACLE_W and y + DINO_H > GROUND_Y - OBSTACLE_H

    def show_game_over(s):
        oled.fill(0)
        oled.text("Game Over", 20, 5)
        oled.text("Score: " + str(s), 25, 20)
        oled.show()
        time.sleep(2)

    # Start Screen
    oled.fill(0)
    oled.text("Dino Game", 25, 5)
    oled.text("Press Btn to Go", 0, 20)
    oled.show()
    while not center_btn.value():
        time.sleep(0.1)

    # Game Loop
    while True:
        oled.fill(0)

        # Jump Logic
        if center_btn.value() and not is_jumping:
            dino_vy = -4
            is_jumping = True
        dino_y += dino_vy
        dino_vy += 0.3
        if dino_y >= GROUND_Y - DINO_H:
            dino_y = GROUND_Y - DINO_H
            dino_vy = 0
            is_jumping = False

        # Obstacle logic
        obstacle_x -= 2
        if obstacle_x < -OBSTACLE_W:
            obstacle_x = WIDTH + random.randint(0, OBSTACLE_GAP)
            score += 1

        draw_ground()
        draw_dino(int(dino_y))
        draw_obstacle(obstacle_x)
        oled.text("S:" + str(score), 100, 0)
        oled.show()

        # Collision check
        if check_collision(int(dino_y), obstacle_x):
            show_game_over(score)
            while True:
                show_submenu(menu_sel)
                dir = read_joystick()
                if dir in ['U', 'L']:
                    menu_sel = 0
                elif dir in ['D', 'R']:
                    menu_sel = 1
                if center_btn.value():
                    while center_btn.value(): pass
                    if menu_sel == 0:
                        return run_dino_game() # Restart
                    else:
                        return # Exit back to menu
                time.sleep(0.2)

# --- MAIN LOOP ---
while True:
    draw_menu()
    dir = read_joystick()
    if dir in ['U', 'L']:
        menu_choice = (menu_choice - 1) % len(MENU_ITEMS)
        time.sleep(0.2)
    elif dir in ['D', 'R']:
        menu_choice = (menu_choice + 1) % len(MENU_ITEMS)
        time.sleep(0.2)
    if center_btn.value():
        oled.fill(0)
        oled.text("Loading...", 30, 10)
        oled.show()
        time.sleep(0.5)
        while center_btn.value(): pass
        if menu_choice == 0:
            enter_sleep_mode()
        elif menu_choice == 1:
            run_servo_control_menu()
        elif menu_choice == 2:
            run_motor_control_menu()
        elif menu_choice == 3:
            run_catch_game()
            while center_btn.value(): pass
        elif menu_choice == 4:
            run_dino_game()
            while center_btn.value(): pass
        elif menu_choice == 5:
            oled.fill(0)
            oled.text("Bye!", 50, 10)
            oled.show()
            time.sleep(1)
            break
