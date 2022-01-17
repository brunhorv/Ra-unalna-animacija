import pygame
from pygame.locals import *
import random

width = 1270
height = 670

GRAVITY_PRESENTS = 1
GRAVITY_SNOW = 1.5
NEW_PRESENT_PROBABILITY = 0.2
NEW_DYNAMITE_PROBABILITY = 0.01
red = (200, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
HIGHSCORE = 0
screen = pygame.display.set_mode((width, height))


class Hero(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.hero_img = pygame.image.load("player_res.png")
        self.image = pygame.Surface((70, 80), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(0, 0))
        self.pos_x = 0
        self.pos_y = 0


class Dynamite(pygame.sprite.Sprite):
    def __init__(self, pos, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.Surface((45, 30), pygame.SRCALPHA)
        self.present_img = pygame.image.load("dynamite_res.png")
        self.rect = self.image.get_rect(center=pos)
        self.pos_x = pos[0]
        self.pos_y = pos[1]


class Present(pygame.sprite.Sprite):

    def __init__(self, pos, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.Surface((45, 30), pygame.SRCALPHA)
        self.present_img = pygame.image.load("present_res.png")
        self.rect = self.image.get_rect(center=pos)
        self.pos_x = pos[0]
        self.pos_y = pos[1]


class Button():

    click_color = (50, 150, 255)
    focus_color = (50, 100, 200)

    text_col = (0, 0, 0)
    width = 200
    height = 60

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.clicked = False
        self.action = False

    def draw_button(self):

        button_rect = Rect(self.x, self.y, self.width, self.height)
        pos = pygame.mouse.get_pos()

        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                pygame.draw.rect(screen, self.click_color, button_rect)
            elif self.clicked == True and pygame.mouse.get_pressed()[0] == 0:
                self.action = True
                self.clicked = False
            else:
                pygame.draw.rect(screen, self.click_color, button_rect)
        else:
            pygame.draw.rect(
                screen, self.focus_color, button_rect)

        font = pygame.font.Font('freesansbold.ttf', 32)
        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width / 2) -
                               int(text_len / 2), self.y + 15))
        return self.action


def update(presents):
    for i in range(len(presents)):
        x, y = presents[i].pos_x, presents[i].pos_y
        presents[i].pos_x = x
        presents[i].pos_y = y+GRAVITY_PRESENTS
        presents[i].rect.topleft = (x, y+1)


def init_snow(number):
    snow = list()
    for _ in range(number):
        x, y = random.randint(0, width), random.randint(0, height)
        snow.append([x, y])
    return snow


def draw_snow(snow, screen):
    for i in range(len(snow)):
        pygame.draw.circle(screen, (255, 255, 255), snow[i], 3)


def update_snow(snow):
    for i in range(len(snow)):
        x, y = snow[i]

        if y >= height:
            snow[i] = [random.randint(0, width), 0]
        else:
            snow[i] = [x, y+GRAVITY_SNOW]


def detect_collision_and_draw(elements, hero, screen, score, type):
    for idx, element in enumerate(elements):
        _, y = element.pos_x, element.pos_y
        if y >= 530:
            present_r = element.rect
            hero_r = hero.rect
            collide = present_r.colliderect(hero_r)

            if collide:
                score += 1

            if type == "Present":
                elements[idx] = Present(
                    (random.randint(0, width), -30), screen)
            if type == "Dynamite":
                elements[idx] = Dynamite(
                    (random.randint(0, width), -30), screen)

        else:
            screen.blit(element.present_img,
                        (element.pos_x, element.pos_y))
    return score


def run_game():
    presents = list()
    lifes = list()
    dynamites = list()
    snow = init_snow(30)
    pygame.init()
    font = pygame.font.Font('freesansbold.ttf', 32)
    clock = pygame.time.Clock()

    score = 0
    lifes = 3
    text_score = font.render(f'Score: {score}', True, red)
    text_rect_score = text_score.get_rect()

    text_lifes = font.render(f'Remaining lives: {lifes}', True, red)
    text_rect_lifes = text_score.get_rect()
    text_rect_lifes.topright = (width-170, 0)

    running = True
    hero = Hero(screen)

    while running:
        play_again = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        update(presents)
        update(dynamites)

        screen.fill((0, 0, 0))

        x, _ = pygame.mouse.get_pos()
        hero.rect.topleft = (x, 550)
        screen.blit(hero.hero_img, (x, 550))

        score = detect_collision_and_draw(
            presents, hero, screen, score, type="Present")
        dynamites_collected = detect_collision_and_draw(
            dynamites, hero, screen, 0, type="Dynamite")

        lifes -= dynamites_collected

        if lifes == 0:
            global HIGHSCORE
            HIGHSCORE = max(HIGHSCORE, score)
            screen.fill((0, 0, 0))
            font = pygame.font.Font('freesansbold.ttf', 50)
            text_go = font.render(f'Game over!', True, red)
            text_rect_go = text_go.get_rect()
            text_rect_go.topright = (width//2 + 100, height//2)
            text_current_highscore = font.render(
                f'Current highscore: {HIGHSCORE}', True, red)
            text_rect_highscore = text_current_highscore.get_rect()
            text_rect_highscore.topright = (width, 0)
            restartButton = Button(375, 450, 'Play Again')
            quitButton = Button(600, 450, "Quit")
            knocked_santa = pygame.image.load("knocked_santa.jpg")

            while play_again == False:
                screen.fill((0, 0, 0))
                screen.blit(knocked_santa, (0, 0))
                screen.blit(text_go, text_rect_go)
                screen.blit(text_current_highscore, text_rect_highscore)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit(0)

                if restartButton.draw_button():
                    play_again = True
                    lifes = 3
                    run_game()

                if quitButton.draw_button():
                    exit(0)

                pygame.display.flip()
                clock.tick(60)

        update_snow(snow)
        draw_snow(snow, screen)

        p = random.uniform(0, 1)

        if p < NEW_PRESENT_PROBABILITY and len(presents) < 70:
            presents.append(Present((random.randint(0, width), -20), screen))

        p = random.uniform(0, 1)

        if p < NEW_DYNAMITE_PROBABILITY and len(dynamites) < 10:
            dynamites.append(Dynamite((random.randint(0, width), -20), screen))

        text_score = font.render(f'Score: {score}', True, red)
        screen.blit(text_score, text_rect_score)

        text_lifes = font.render(f'Remaining lifes: {lifes}', True, red)
        screen.blit(text_lifes, text_rect_lifes)

        pygame.display.flip()
        clock.tick(60)


run_game()
pygame.quit()
