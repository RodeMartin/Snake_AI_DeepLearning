import pygame
import torch
import random
import numpy as np
import csv
import os
from collections import deque
from game import SnakeGameAI, Direction, Point
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 
        self.gamma = 0.9 
        self.memory = deque(maxlen=MAX_MEMORY) 
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            dir_l, dir_r, dir_u, dir_d,
            
            game.food.x < game.head.x, 
            game.food.x > game.head.x, 
            game.food.y < game.head.y, 
            game.food.y > game.head.y
        ]
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state, is_training=True):
        if is_training:
            self.epsilon = max(0, 80 - self.n_games * 2)
        else:
            self.epsilon = 0

        final_move = [0,0,0]
        if is_training and random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move

def run_game(mode='train'):
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    
    if mode == 'train' and not os.path.exists('stats.csv'):
        with open('stats.csv', 'w', newline='') as f:
            csv.writer(f).writerow(['Jatek', 'Pont', 'Rekord'])

    if mode == 'play':
        model_path = './model/model.pth'
        if os.path.exists(model_path):
            agent.model.load_state_dict(torch.load(model_path))
            agent.model.eval()
            print("Modell betöltve!")
        else:
            print("Nincs mentett modell! Előbb tanítsd meg (Train mode).")
            return

    while True:
        game.display_epsilon = agent.epsilon if mode == 'train' else 0
        game.display_game_num = agent.n_games

        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old, is_training=(mode=='train'))
        reward, done, score = game.play_step(final_move)
        
        if mode == 'train':
            state_new = agent.get_state(game)
            agent.train_short_memory(state_old, final_move, reward, state_new, done)
            agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.reset()
            agent.n_games += 1
            
            if mode == 'train':
                agent.train_long_memory()
                if score > record:
                    record = score
                    agent.model.save()
                
                with open('stats.csv', 'a', newline='') as f:
                    csv.writer(f).writerow([agent.n_games, score, record])
            
            if score > record: record = score
            print('Jatek:', agent.n_games, 'Pont:', score, 'Rekord:', record)

            if mode == 'train':
                plot_scores.append(score)
                total_score += score
                mean_score = total_score / agent.n_games
                plot_mean_scores.append(mean_score)
                plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    temp_game = SnakeGameAI()
    selected_mode = temp_game.show_menu()

    if selected_mode == 'train':
        run_game(mode='train')
    elif selected_mode == 'play':
        run_game(mode='play')
    else:
        print("Kilépés...")
        pygame.quit()