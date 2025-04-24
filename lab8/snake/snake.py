import pygame
import time
import random

snake_speed = 15


window_x = 720
window_y = 480




black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


pygame.init()


pygame.display.set_caption('Змейка')
game_window = pygame.display.set_mode((window_x, window_y))


fps = pygame.time.Clock()

# ИЗМЕНЕНО: Добавлены параметры границ и игрового поля
border_thickness = 10
top_margin = 40  # Верхний отступ для очков и уровня
game_area = {
    "left": border_thickness,
    "top": top_margin,
    "right": window_x - border_thickness,
    "bottom": window_y - border_thickness
}

# ИЗМЕНЕНО: Начальная позиция змейки с учетом верхнего отступа
snake_position = [100, top_margin + 10]

# ИЗМЕНЕНО: Тело змейки с учетом верхнего отступа
snake_body = [
    [100, top_margin + 10],
    [90, top_margin + 10],
    [80, top_margin + 10],
    [70, top_margin + 10]
]

# ИЗМЕНЕНО: Генерация фрукта внутри игровой области
fruit_position = [
    random.randrange(game_area["left"] + 10, game_area["right"], 10),
    random.randrange(game_area["top"] + 10, game_area["bottom"], 10)
]

fruit_spawn = True


direction = 'RIGHT'
change_to = direction


score = 0


level = 1
font = pygame.font.Font(None, 30)
def drawText(text, font, surface, x, y) :
    textobj = font.render(text, 1, white)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# ДОБАВЛЕНО: Функция для отрисовки красных границ
def draw_borders():
    # Только верхняя граница игрового поля (ниже очков)
    pygame.draw.rect(game_window, red, pygame.Rect(0, top_margin, window_x, border_thickness))
    # Левая граница (начиная с верхней границы)
    pygame.draw.rect(game_window, red, pygame.Rect(0, top_margin, border_thickness, window_y - top_margin))
    # Правая граница (начиная с верхней границы)
    pygame.draw.rect(game_window, red, pygame.Rect(window_x - border_thickness, top_margin, border_thickness, window_y - top_margin))
    # Нижняя граница
    pygame.draw.rect(game_window, red, pygame.Rect(0, window_y - border_thickness, window_x, border_thickness))

# ИЗМЕНЕНО: Добавлено позиционирование счета
def show_score(choice, color, font, size) :
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (10, 10)  # Разместим счет в верхнем левом углу
    game_window.blit(score_surface, score_rect)


def game_over() :
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()


while True :
    for event in pygame.event.get() :
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_UP :
                change_to = 'UP'
            if event.key == pygame.K_DOWN :
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT :
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT :
                change_to = 'RIGHT'
            # ДОБАВЛЕНО: Выход по клавише Esc
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
    
 
    if change_to == 'UP' and direction != 'DOWN' :
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP' :
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT' :
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT' :
        direction = 'RIGHT'

 
    if direction == 'UP' :
        snake_position[1] -= 10
    if direction == 'DOWN' :
        snake_position[1] += 10
    if direction == 'LEFT' :
        snake_position[0] -= 10
    if direction == 'RIGHT' :
        snake_position[0] += 10

    
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1] :
        score += 10
        fruit_spawn = False
    else :
        snake_body.pop()

    # ИЗМЕНЕНО: Генерация новой позиции фрукта в пределах игрового поля
    if not fruit_spawn :
        fruit_position = [
            random.randrange(game_area["left"] + 10, game_area["right"], 10),
            random.randrange(game_area["top"] + 10, game_area["bottom"], 10)
        ]

    fruit_spawn = True
    game_window.fill(black)
    
    # ДОБАВЛЕНО: Рисуем границы
    draw_borders()

    for pos in snake_body :
        pygame.draw.rect(game_window, green,
                         pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))

    # ИЗМЕНЕНО: Проверка столкновения с границами игрового поля
    if (snake_position[0] < game_area["left"] or 
        snake_position[0] >= game_area["right"] or 
        snake_position[1] < game_area["top"] or 
        snake_position[1] >= game_area["bottom"]):
        game_over()

  
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1] :
            game_over()

    
    if score >= level * 30:
        level += 1
        snake_speed += 5

    drawText('Level %s' % (level), font, game_window, 640, 10)

    show_score(1, white, 'times new roman', 20)

    pygame.display.update()

    fps.tick(snake_speed)