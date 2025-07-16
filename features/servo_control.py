from machine import Pin, PWM
import time

def run_servo_slider(oled, read_joystick, center_btn, servo_pin):
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

def run_servo_control_menu(oled, read_joystick, center_btn):
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
            run_servo_slider(oled, read_joystick, center_btn, Pin(22) if sub_sel == 0 else Pin(0))
            break
        time.sleep(0.2)
