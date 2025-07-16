import time
import random

def show_submenu(oled, menu_sel):
    oled.fill(0)
    oled.text(">Restart" if menu_sel == 0 else " Restart", 5, 5)
    oled.text(">Exit" if menu_sel == 1 else " Exit", 5, 20)
    oled.show()

def run_catch_game(oled, read_joystick, center_btn):
    WIDTH, HEIGHT = 128, 32
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
                show_submenu(oled, menu_sel)
                dir = read_joystick()
                if dir in ['U', 'L']: menu_sel = 0
                elif dir in ['D', 'R']: menu_sel = 1
                if center_btn.value():
                    if menu_sel == 0: return run_catch_game(oled, read_joystick, center_btn)
                    else: return
                time.sleep(0.2)
