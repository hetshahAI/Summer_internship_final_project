import time
import random

def show_submenu(oled, menu_sel):
    oled.fill(0)
    oled.text(">Restart" if menu_sel == 0 else " Restart", 5, 5)
    oled.text(">Exit" if menu_sel == 1 else " Exit", 5, 20)
    oled.show()

def run_dino_game(oled, read_joystick, center_btn):
    WIDTH, HEIGHT = 128, 32
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

    oled.fill(0)
    oled.text("Dino Game", 25, 5)
    oled.text("Press Btn to Go", 0, 20)
    oled.show()
    while not center_btn.value():
        time.sleep(0.1)

    while True:
        oled.fill(0)

        if center_btn.value() and not is_jumping:
            dino_vy = -4
            is_jumping = True
        dino_y += dino_vy
        dino_vy += 0.3
        if dino_y >= GROUND_Y - DINO_H:
            dino_y = GROUND_Y - DINO_H
            dino_vy = 0
            is_jumping = False

        obstacle_x -= 2
        if obstacle_x < -OBSTACLE_W:
            obstacle_x = WIDTH + random.randint(0, OBSTACLE_GAP)
            score += 1

        draw_ground()
        draw_dino(int(dino_y))
        draw_obstacle(obstacle_x)
        oled.text("S:" + str(score), 100, 0)
        oled.show()

        if check_collision(int(dino_y), obstacle_x):
            show_game_over(score)
            while True:
                show_submenu(oled, menu_sel)
                dir = read_joystick()
                if dir in ['U', 'L']: menu_sel = 0
                elif dir in ['D', 'R']: menu_sel = 1
                if center_btn.value():
                    while center_btn.value(): pass
                    if menu_sel == 0:
                        return run_dino_game(oled, read_joystick, center_btn)
                    else:
                        return
                time.sleep(0.2)
