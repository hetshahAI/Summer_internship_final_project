from machine import Pin, ADC, deepsleep, reset_cause, DEEPSLEEP_RESET
import time

def enter_sleep_mode(oled, adc, center_btn):
    def joystick_active():
        val = adc.read()
        if center_btn.value(): return True
        if 3000 < val <= 4095 or 2000 < val < 2700 or 1000 < val < 1800 or 500 < val < 900:
            return True
        return False

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
