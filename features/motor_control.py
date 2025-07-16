from machine import Pin, PWM
from time import sleep

def run_motor_fade(oled, center_btn, pin, name):
    motor = PWM(pin, freq=1000)
    oled.fill(0)
    oled.text(name + " running", 5, 5)
    oled.text("Press Btn to exit", 5, 20)
    oled.show()

    while True:
        for duty in range(0, 1024, 10):
            motor.duty(duty)
            if center_btn.value():
                while center_btn.value(): pass
                motor.deinit()
                Pin(pin, Pin.OUT).value(0)
                return
            sleep(0.01)
        for duty in range(1023, -1, -10):
            motor.duty(duty)
            if center_btn.value():
                while center_btn.value(): pass
                motor.deinit()
                Pin(pin, Pin.OUT).value(0)
                return
            sleep(0.01)

def run_motor_fade_both(oled, center_btn, pin1, pin2):
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

def run_motor_control_menu(oled, read_joystick, center_btn):
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
                run_motor_fade(oled, center_btn, Pin(27), "Motor 1")
            elif sub_sel == 1:
                run_motor_fade(oled, center_btn, Pin(32), "Motor 2")
            else:
                run_motor_fade_both(oled, center_btn, Pin(27), Pin(32))
            break
        sleep(0.2)
