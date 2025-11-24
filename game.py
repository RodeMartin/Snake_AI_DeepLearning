import pygame
import random
import os
import math
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
pygame.mixer.init()

font = pygame.font.SysFont('arial', 25)
font_hud = pygame.font.SysFont('monospace', 20, bold=True)
font_title = pygame.font.SysFont('arial', 40, bold=True)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# szin
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (20, 20, 30)
GRID_COLOR = (40, 40, 50)
HUD_BG = (50, 50, 60)
ACCENT = (0, 200, 255)

BLOCK_SIZE = 20
SPEED = 80 

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(6, 12)
        self.life = random.randint(10, 25)
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.size -= 0.5 # zsugorodas

    def draw(self, surface):
        if self.life > 0 and self.size > 0:
            pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), int(self.size), int(self.size)))

class SnakeGameAI:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.hud_width = 240
        self.display = pygame.display.set_mode((self.w + self.hud_width, self.h))
        pygame.display.set_caption('Snake AI - Beadandó')
        self.clock = pygame.time.Clock()
        
        self.img_head = None
        self.img_body = None
        self.img_apple = None
        self.snd_eat = None
        self.snd_die = None
        self._load_assets()
        
        self.display_epsilon = 0
        self.display_game_num = 0
        self.particles = []
        
        self.reset()

    def _load_assets(self):
        try:
            self.img_head = pygame.image.load(os.path.join('resources', 'head.png'))
            self.img_body = pygame.image.load(os.path.join('resources', 'body.png'))
            self.img_apple = pygame.image.load(os.path.join('resources', 'apple.png'))
            self.snd_eat = pygame.mixer.Sound(os.path.join('resources', 'eat.wav'))
            self.snd_die = pygame.mixer.Sound(os.path.join('resources', 'die.wav'))
            self.snd_eat.set_volume(0.3)
            self.snd_die.set_volume(0.3)
        except: pass

    def show_menu(self):
        waiting = True
        while waiting:
            self.display.fill(BG_COLOR)
            title = font_title.render("SNAKE AI PROJEKT", True, ACCENT)
            text1 = font.render("Nyomj [T]-t a MI TANÍTÁSÁHOZ", True, WHITE)
            text2 = font.render("Nyomj [P]-t a LEJÁTSZÁSHOZ (betanított modell)", True, WHITE)
            text3 = font.render("Nyomj [Q]-t a KILÉPÉSHEZ", True, WHITE)
            
            self.display.blit(title, (self.w/2 - title.get_width()/2 + self.hud_width/2, 100))
            self.display.blit(text1, (self.w/2 - text1.get_width()/2 + self.hud_width/2, 200))
            self.display.blit(text2, (self.w/2 - text2.get_width()/2 + self.hud_width/2, 250))
            self.display.blit(text3, (self.w/2 - text3.get_width()/2 + self.hud_width/2, 300))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return 'quit'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t: return 'train'
                    if event.key == pygame.K_p: return 'play'
                    if event.key == pygame.K_q: return 'quit'

    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self.bombs = []
        self.particles = []
        self._place_food()
        self._place_bombs()
        self.frame_iteration = 0
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake or (hasattr(self, 'bombs') and self.food in self.bombs):
            self._place_food()

    def _place_bombs(self):
        self.bombs = []
        for _ in range(3):
            while True:
                x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE )*BLOCK_SIZE 
                y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE )*BLOCK_SIZE
                pt = Point(x, y)
                if pt not in self.snake and pt != self.food and pt not in self.bombs:
                    self.bombs.append(pt)
                    break

    def play_step(self, action):
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        dist_before = math.sqrt((self.head.x - self.food.x)**2 + (self.head.y - self.food.y)**2)
        self._move(action)
        self.snake.insert(0, self.head)
        
        reward = 0
        game_over = False
        
        dist_after = math.sqrt((self.head.x - self.food.x)**2 + (self.head.y - self.food.y)**2)
        if dist_after < dist_before: reward = 1
        else: reward = -1.5

        # utkozes
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            if self.snd_die: self.snd_die.play()

            explosion_color = (200, 200, 200) # fal
            particle_count = 30
            
            if self.head in self.bombs:
                explosion_color = (255, 0, 255) # bomba
                particle_count = 60 
            
            # particles
            for _ in range(particle_count):
                self.particles.append(Particle(self.head.x, self.head.y, explosion_color))
            
            # freeze game for explosion
            for _ in range(20): 
                self._update_ui()
                self.clock.tick(60) 

            return reward, game_over, self.score
            
        if self.head == self.food:
            if self.snd_eat: self.snd_eat.play()
            self.score += 1
            reward = 10
            for _ in range(15):
                self.particles.append(Particle(self.food.x + 10, self.food.y + 10, (255, 50, 50)))
            self._place_food()
        else:
            self.snake.pop()
        
        self._update_ui()
        self.clock.tick(SPEED)
        return reward, game_over, self.score
    
    def is_collision(self, pt=None):
        if pt is None: pt = self.head
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0: return True
        if pt in self.snake[1:]: return True
        if pt in self.bombs: return True
        return False

    def _draw_snake(self):
        SNAKE_GREEN = (0, 255, 100)
        EYE_WHITE = (255, 255, 255)
        EYE_BLACK = (0, 0, 0)

        # body
        for i in range(len(self.snake) - 1):
            pt1 = self.snake[i]
            pt2 = self.snake[i+1]
            center1 = (pt1.x + BLOCK_SIZE // 2, pt1.y + BLOCK_SIZE // 2)
            center2 = (pt2.x + BLOCK_SIZE // 2, pt2.y + BLOCK_SIZE // 2)
            pygame.draw.line(self.display, SNAKE_GREEN, center1, center2, int(BLOCK_SIZE * 0.8))

        # circles
        for i, pt in enumerate(self.snake):
            center = (int(pt.x + BLOCK_SIZE // 2), int(pt.y + BLOCK_SIZE // 2))
            
            if i == 0:
                # green head
                radius = int(BLOCK_SIZE // 2 * 0.9)
                pygame.draw.circle(self.display, SNAKE_GREEN, center, radius)
                
                # szem:off_f: tavolsag a fejtol
                # off_s: tavolsag egymastol
                off_f = 6 
                off_s = 5
                
                eye_1 = (0,0)
                eye_2 = (0,0)
                pupil_1 = (0,0)
                pupil_2 = (0,0)

                if self.direction == Direction.RIGHT:
                    eye_1 = (center[0] + off_f, center[1] - off_s)
                    eye_2 = (center[0] + off_f, center[1] + off_s)
                    pupil_1 = (eye_1[0] + 2, eye_1[1])
                    pupil_2 = (eye_2[0] + 2, eye_2[1])
                elif self.direction == Direction.LEFT:
                    eye_1 = (center[0] - off_f, center[1] - off_s)
                    eye_2 = (center[0] - off_f, center[1] + off_s)
                    pupil_1 = (eye_1[0] - 2, eye_1[1])
                    pupil_2 = (eye_2[0] - 2, eye_2[1])
                elif self.direction == Direction.UP:
                    eye_1 = (center[0] - off_s, center[1] - off_f)
                    eye_2 = (center[0] + off_s, center[1] - off_f)
                    pupil_1 = (eye_1[0], eye_1[1] - 2)
                    pupil_2 = (eye_2[0], eye_2[1] - 2)
                elif self.direction == Direction.DOWN:
                    eye_1 = (center[0] - off_s, center[1] + off_f)
                    eye_2 = (center[0] + off_s, center[1] + off_f)
                    pupil_1 = (eye_1[0], eye_1[1] + 2)
                    pupil_2 = (eye_2[0], eye_2[1] + 2)

                # eyes
                pygame.draw.circle(self.display, EYE_WHITE, eye_1, 4)
                pygame.draw.circle(self.display, EYE_WHITE, eye_2, 4)
                # pupils
                pygame.draw.circle(self.display, EYE_BLACK, pupil_1, 2)
                pygame.draw.circle(self.display, EYE_BLACK, pupil_2, 2)

            else: # test
                radius = int(BLOCK_SIZE // 2 * 0.8)
                pygame.draw.circle(self.display, SNAKE_GREEN, center, radius)

    def _update_ui(self):
        self.display.fill(BG_COLOR)
        SOFT_GRID = (30, 30, 40)
        for x in range(0, self.w, BLOCK_SIZE): pygame.draw.line(self.display, SOFT_GRID, (x, 0), (x, self.h))
        for y in range(0, self.h, BLOCK_SIZE): pygame.draw.line(self.display, SOFT_GRID, (0, y), (self.w, y))
            
        for bomb in self.bombs:
            center = (bomb.x + BLOCK_SIZE//2, bomb.y + BLOCK_SIZE//2)
            pygame.draw.circle(self.display, (150, 0, 150), center, BLOCK_SIZE//2 - 4)
            start_1, end_1 = (bomb.x + 4, bomb.y + 4), (bomb.x + BLOCK_SIZE - 4, bomb.y + BLOCK_SIZE - 4)
            start_2, end_2 = (bomb.x + BLOCK_SIZE - 4, bomb.y + 4), (bomb.x + 4, bomb.y + BLOCK_SIZE - 4)
            pygame.draw.line(self.display, (255, 0, 255), start_1, end_1, 3)
            pygame.draw.line(self.display, (255, 0, 255), start_2, end_2, 3)

        if hasattr(self, 'particles'):
            for p in self.particles[:]:
                p.move()
                p.draw(self.display)
                if p.life <= 0 or p.size <= 0: self.particles.remove(p)

        apple_center = (self.food.x + BLOCK_SIZE//2, self.food.y + BLOCK_SIZE//2)
        pygame.draw.circle(self.display, (200, 0, 0), apple_center, BLOCK_SIZE//2 - 2)
        pygame.draw.line(self.display, (0, 255, 0), (apple_center[0], apple_center[1]-5), (apple_center[0]+3, apple_center[1]-8), 2)

        self._draw_snake()

        hud_x = self.w
        pygame.draw.rect(self.display, HUD_BG, (hud_x, 0, self.hud_width, self.h))
        pygame.draw.line(self.display, ACCENT, (hud_x, 0), (hud_x, self.h), 3)
        
        def draw_text(txt, y, color=WHITE, size_font=font_hud):
            surface = size_font.render(txt, True, color)
            self.display.blit(surface, (hud_x + 10, y))

        draw_text("SNAKE AI v1.3", 20, ACCENT)
        draw_text("-------------", 40, ACCENT)
        draw_text(f"Jatek: {self.display_game_num}", 70)
        draw_text(f"Pontszam: {self.score}", 100)
        draw_text(f"Felfedezes: {int(self.display_epsilon)}%", 150)
        
        bar_width = 200
        bar_fill = int((self.display_epsilon / 80.0) * bar_width)
        pygame.draw.rect(self.display, BLACK, (hud_x + 10, 180, bar_width, 10))
        pygame.draw.rect(self.display, (255, 165, 0), (hud_x + 10, 180, max(0, min(bar_fill, bar_width)), 10))
        
        status = "GONDOLKODAS..." if self.display_epsilon < 5 else "FELFEDEZES..."
        color = (0, 255, 0) if self.display_epsilon < 5 else (255, 255, 0)
        draw_text(f"Statusz: {status}", 220, color)
        draw_text("Iranyitas:", 400, ACCENT)
        draw_text("Zard be az ablakot a kilepeshez.", 430, (150, 150, 150), pygame.font.SysFont('arial', 15))

        pygame.display.flip()
        
    def _move(self, action):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)
        if np.array_equal(action, [1, 0, 0]): new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]): new_dir = clock_wise[(idx + 1) % 4]
        else: new_dir = clock_wise[(idx - 1) % 4]
        self.direction = new_dir
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT: x += BLOCK_SIZE
        elif self.direction == Direction.LEFT: x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN: y += BLOCK_SIZE
        elif self.direction == Direction.UP: y -= BLOCK_SIZE
        self.head = Point(x, y)