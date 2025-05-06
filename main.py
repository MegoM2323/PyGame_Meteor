import pygame
import random
import json
from pygame.locals import *

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

SCREEN_SIZE = (1280, 720)
dis_width = SCREEN_SIZE[0]
dis_height = SCREEN_SIZE[1]

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)

dis = pygame.display.set_mode((dis_width, dis_height))

pygame.display.set_caption('Meteor')

clock = pygame.time.Clock()

procent_list = {
    'Easy': 9,
    'Middle': 15,
    'Hard': 19,
    'Unreal': 25,
}
procent_in_second = procent_list['Easy']
level = 'Easy'

procent_bonus_generate = {
    1: {'procent': 17, 'reward': 5},
    2: {'procent': 7, 'reward': 10},
    3: {'procent': 3, 'reward': 25},
}

person_size = 30
block_size = 40
bonus_size = 40
game_over_offset = person_size * 0.5 + block_size - 0.01

preson_speed = 10
koef = 0.3

start_speed = 9
limit_speed = 15

# Доработать !!!
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("bahnschrift", 35)

BLOCKS = []
BONUS = []

all_sprites = pygame.sprite.Group()


def write_json(data):
    with open("data.json", "w") as f:
        json.dump(data, f)


def read_json():
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except:
        data = {
            'Easy': 0,
            'Middle': 0,
            'Hard': 0,
            'Unreal': 0,
        }
        write_json(data)
    return dict(data)


def set_score(score):
    value = score_font.render("Ваш счёт: " + str(score), True, yellow)
    dis.blit(value, [0, 0])


def person(x1, y1):
    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.image.load('images/' + 'rocket.png')
    sprite.size = sprite.image.get_size()
    sprite.image = pygame.transform.scale(sprite.image, (int(sprite.size[0] * 0.48), int(sprite.size[1] * 0.48)))
    sprite.rect = sprite.image.get_rect()
    all_sprites.add(sprite)
    sprite.rect.x = x1 - person_size * 0.53
    sprite.rect.y = y1 - person_size * 0.5

    # pygame.draw.rect(dis, green, [x1, y1, person_size, person_size])


def message(msg, color, x, y):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [x, y])


def blocks_render(block_list):
    for block in block_list:
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load('images/meteor/' + block['image'])
        sprite.size = sprite.image.get_size()
        sprite.image = pygame.transform.scale(sprite.image, (int(sprite.size[0] * 1), int(sprite.size[1] * 1)))
        sprite.rect = sprite.image.get_rect()
        all_sprites.add(sprite)
        sprite.rect.x = block['x'] - block_size * 0.1
        sprite.rect.y = block['y'] + block['speed'] - block_size * 0.2

        # pygame.draw.rect(dis, green, [block['x'], block['y'] + block['speed'], block['size'], block['size']])


def block_generate():
    x = round(random.randrange(0, dis_width - person_size) / 10.0) * 10.0
    y = -limit_speed
    speed = round(random.randrange(start_speed, limit_speed))
    num = random.randrange(1, 16)
    if num <= 9:
        num = '0' + str(num)
    image = f'Meteors_{num}.gif'
    return {'x': x, 'y': y, 'speed': speed, 'size': block_size, 'image': image}


def bonus_render():
    global BONUS
    for bonus in BONUS:
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.image.load('images/' + bonus['image'])
        sprite.size = sprite.image.get_size()
        sprite.image = pygame.transform.scale(sprite.image, (int(sprite.size[0] * 0.5), int(sprite.size[1] * 0.5)))
        sprite.rect = sprite.image.get_rect()
        all_sprites.add(sprite)
        sprite.rect.x = bonus['x'] - bonus_size * 0.35
        sprite.rect.y = bonus['y'] - bonus_size * 0.35

        #pygame.draw.rect(dis, green, [bonus['x'], bonus['y'], bonus['size'], bonus['size']])


def bonus_generate():
    global dis_width, BONUS
    num = random.randrange(0, 1000)
    spawn_flag = False
    for i in list(procent_bonus_generate.keys())[::-1]:
        if int(num) <= procent_bonus_generate[i]['procent']:
            num = '0' + str(i)
            spawn_flag = True
            break
    if not spawn_flag:
        return
    x = round(random.randrange(0, dis_width - bonus_size) / 10.0) * 10.0
    y = dis_height - 50
    life_time = round(random.randrange(35 * 3, 60 * 6))
    image = f'bonus/bonus_{num}.gif'
    BONUS.append({'x': x, 'y': y, 'size': block_size, 'image': image, 'life_time': life_time, 'type': int(num)})


def gameLoop():
    global BLOCKS, all_sprites, procent_in_second, level, SCREEN_SIZE, BONUS

    data = read_json()

    game_over = False
    game_close = False

    x1 = round(dis_width / 4) * 3
    y1 = dis_height - 50

    x2 = round(dis_width / 4)
    y2 = dis_height - 50

    score = 0

    x1_change = 0
    x2_change = 0

    while not game_over:
        if random.randrange(0, 100) <= procent_in_second:
            BLOCKS.append(block_generate())
        bonus_generate()
        while game_close == True:

            if procent_in_second == procent_list['Easy']:
                level = 'Easy'
                if data['Easy'] < score:
                    data['Easy'] = score
            elif procent_in_second == procent_list['Middle']:
                level = 'Middle'
                if data['Middle'] < score:
                    data['Middle'] = score
            elif procent_in_second == procent_list['Hard']:
                level = 'Hard'
                if data['Hard'] < score:
                    data['Hard'] = score
            elif procent_in_second == procent_list['Unreal']:
                level = 'Unreal'
                if data['Unreal'] < score:
                    data['Unreal'] = score
            write_json(data)

            BLOCKS = []
            BONUS = []
            dis.fill(black)
            message("Вы проиграли! Нажмите Q для выхода или R для повторной игры", red, dis_width / 6, dis_height / 2.5)
            message("Выбери сложность", yellow, dis_width / 6, dis_height / 2.5 + 30 * 1)
            message("Easy - E", yellow, dis_width / 6, dis_height / 2.5 + 30 * 2)
            message("Middle - M", yellow, dis_width / 6, dis_height / 2.5 + 30 * 3)
            message("Hard - H", yellow, dis_width / 6, dis_height / 2.5 + 30 * 4)
            message("Unreal - U", yellow, dis_width / 6, dis_height / 2.5 + 30 * 5)

            message("Рекорд:", yellow, dis_width / 3 * 2, dis_height / 2.5 + 30 * 1)
            message(f"Easy: {data['Easy']}", yellow, dis_width / 3 * 2, dis_height / 2.5 + 30 * 2)
            message(f"Middle: {data['Middle']}", yellow, dis_width / 3 * 2, dis_height / 2.5 + 30 * 3)
            message(f"Hard: {data['Hard']}", yellow, dis_width / 3 * 2, dis_height / 2.5 + 30 * 4)
            message(f"Unreal: {data['Unreal']}", yellow, dis_width / 3 * 2, dis_height / 2.5 + 30 * 5)

            message(f"Текуший уровень: {level}", yellow, dis_width / 4 * 3, 0)

            set_score(score)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_e:
                        procent_in_second = procent_list['Easy']
                        gameLoop()
                    if event.key == pygame.K_m:
                        procent_in_second = procent_list['Middle']
                        gameLoop()
                    if event.key == pygame.K_h:
                        procent_in_second = procent_list['Hard']
                        gameLoop()
                    if event.key == pygame.K_u:
                        procent_in_second = procent_list['Unreal']
                        gameLoop()
                    if event.key == pygame.K_r:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    x1_change = -person_size * koef
                elif event.key == pygame.K_l:
                    x1_change = person_size * koef
                elif event.key == pygame.K_a:
                    x2_change = -person_size * koef
                elif event.key == pygame.K_d:
                    x2_change = person_size * koef

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_j and x1_change == -person_size * koef:
                    x1_change = 0
                elif event.key == pygame.K_l and x1_change == person_size * koef:
                    x1_change = 0
                elif event.key == pygame.K_a and x2_change == -person_size * koef:
                    x2_change = 0
                elif event.key == pygame.K_d and x2_change == person_size * koef:
                    x2_change = 0

        if x1 + x1_change - person_size * 0.95 > x2 and x1 + person_size + x1_change < dis_width:
            x1 += x1_change
        if x2 + x2_change + person_size * 0.95 < x1 and 0 < x2 - person_size * koef + x2_change:
            x2 += x2_change
        dis.fill(black)

        blocks_render(BLOCKS)
        new_BLOCKS = []
        for i in range(len(BLOCKS)):
            BLOCKS[i]['y'] += BLOCKS[i]['speed']
            if (x1 - game_over_offset <= BLOCKS[i]['x'] <= x1 + game_over_offset or x2 - game_over_offset <= BLOCKS[i][
                'x'] <= x2 + game_over_offset) and \
                    (BLOCKS[i]['y'] - BLOCKS[i]['speed'] <= y1 <= BLOCKS[i]['y'] or BLOCKS[i]['y'] - BLOCKS[i][
                        'speed'] <= y2 <= BLOCKS[i]['y']):
                game_close = True
                break
            if BLOCKS[i]['y'] > dis_height:
                score += 1
            else:
                new_BLOCKS.append(BLOCKS[i])
        BLOCKS = new_BLOCKS

        bonus_render()
        new_BONUS = []
        for i in range(len(BONUS)):
            BONUS[i]["life_time"] -= 1
            if BONUS[i]["life_time"] > 0:
                if x1 - game_over_offset <= BONUS[i]['x'] <= x1 + game_over_offset or x2 - game_over_offset <= BONUS[i][
                        'x'] <= x2 + game_over_offset:
                    message(f'+{procent_bonus_generate[BONUS[i]["type"]]["reward"]}', green, BONUS[i]['x'], BONUS[i]['y'] - 70)
                    score += procent_bonus_generate[BONUS[i]["type"]]['reward']
                else:
                    new_BONUS.append(BONUS[i])
        BONUS = new_BONUS

        person(x1, y1)
        person(x2, y2)
        all_sprites.draw(dis)
        all_sprites = pygame.sprite.Group()

        set_score(score)
        pygame.display.update()

        clock.tick(60)
    pygame.quit()
    quit()


gameLoop()
