import turtle
import random
import time
import colorsys
import sys

# Настройка экрана
screen = turtle.Screen()
screen.title("MaxFpsTest by helfz     tiktok @.helfzsasal         discord helfz_")
screen.bgcolor("black")
screen.tracer(0)
screen.listen()

# Глобальные переменные
balls = []
fps_counter = 0
last_fps_update = time.time()
fps = 60
spawn_cooldown = 0.05
last_spawn_time = 0
spawning = False
total_spawned = 0
cleared_count = 0
hue = 0
balls_before_clear = 0  # Добавлено для хранения количества шаров ДО очистки
program_running = True  # Флаг для контроля работы программы

# Счётчик шаров
counter = turtle.Turtle()
counter.hideturtle()
counter.penup()
counter.color("white")
counter.goto(-380, 350)

# Текст статистики
stats_text = turtle.Turtle()
stats_text.hideturtle()
stats_text.penup()
stats_text.color("white")
stats_text.goto(0, 0)

def update_counters():
    counter.clear()
    counter.write(f"Шаров: {len(balls)} | FPS: {fps}", font=("Arial", 14, "normal"))

def show_stats(ball_count):
    global program_running
    
    # Определяем реакцию
    if ball_count < 500:
        reaction = "ТЫ ЧЕ НА ПЕЧКЕ?"
    elif 500 <= ball_count < 1000:
        reaction = "МАЛО"
    elif 1000 <= ball_count < 1500:
        reaction = "НЕПЛОХО"
    elif 1500 <= ball_count < 2000:
        reaction = "ХОРОШО"
    elif 2000 <= ball_count < 3000:
        reaction = "ОЧЕНЬ ХОРОШО"
    elif 3000 <= ball_count < 6000:
        reaction = "ОТЛИЧНО"
    elif 6000 <= ball_count < 10000:
        reaction = "ЗАМЕЧАТЕЛЬНО!!!"
    elif 10000 <= ball_count < 20000:
        reaction = "АХУЕТЬ"
    else:
        reaction = "СУКА ТЫ КТО ТАКОЙ БЛЯТЬ"
    
    # Показываем статистику 10 секунд
    stats_text.clear()
    stats_text.write(f"{reaction}\nШаров было: {ball_count}",  # Изменено на "было"
                   align="center", font=("Arial", 24, "bold"))
    screen.update()
    time.sleep(10)
    stats_text.clear()
    program_running = False  # Устанавливаем флаг для завершения программы

class Ball(turtle.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.goto(x, y)
        self.dx = random.uniform(-5, 5)
        self.dy = random.uniform(-5, 0)
        self.gravity = 0.2
        self.energy_loss = 0.9
        self.min_bounce = 3.0
        self.hue_offset = random.random()
        
    def update_color(self, base_hue):
        current_hue = (base_hue + self.hue_offset * 0.1) % 1.0
        r, g, b = colorsys.hsv_to_rgb(current_hue, 1.0, 1.0)
        self.color(r, g, b)
        
    def update(self):
        self.dy -= self.gravity
        self.setx(self.xcor() + self.dx)
        self.sety(self.ycor() + self.dy)

        if self.ycor() < -300:
            self.sety(-300)
            self.dy = abs(self.dy) * self.energy_loss
            if self.dy < self.min_bounce:
                self.dy = self.min_bounce

        if abs(self.xcor()) > 380:
            self.dx *= -1

def spawn_ball(x=None, y=None):
    global last_spawn_time, total_spawned
    current_time = time.time()
    if current_time - last_spawn_time > spawn_cooldown:
        if x is None and y is None:
            x = random.randint(-350, 350)
            y = random.randint(0, 350)
        balls.append(Ball(x, y))
        total_spawned += 1
        last_spawn_time = current_time
        update_counters()

def delete_all_balls_except_one():
    global cleared_count, balls_before_clear
    if balls:
        balls_before_clear = len(balls)  # Сохраняем количество ДО очистки
        # Оставляем только 1 случайный шар
        ball_to_keep = random.choice(balls)
        for ball in balls[:]:
            if ball != ball_to_keep:
                ball.hideturtle()
                balls.remove(ball)
        cleared_count += 1
        update_counters()

def check_fps():
    global fps, fps_counter, last_fps_update
    fps_counter += 1
    current_time = time.time()
    
    if current_time - last_fps_update >= 1:
        fps = fps_counter
        fps_counter = 0
        last_fps_update = current_time
        
        if fps < 5 and balls:
            delete_all_balls_except_one()  # Сначала очищаем
            show_stats(balls_before_clear)  # Показываем статистику ПОСЛЕ очистки, но с числом ДО очистки
        
        update_counters()

# Обработка клавиш
def start_spawning():
    global spawning
    spawning = True

def stop_spawning():
    global spawning
    spawning = False

screen.onkeypress(start_spawning, "w")
screen.onkeyrelease(stop_spawning, "w")
screen.listen()

# Основной цикл
while program_running:
    if spawning:
        spawn_ball()
    
    check_fps()

    for ball in balls:
        ball.update_color(hue)
        ball.update()

    hue = (hue + 0.01) % 1.0
    screen.update()
    time.sleep(0.001)

# Закрытие программы
screen.bye()
sys.exit()