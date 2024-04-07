import pygame
from Food import Food

DIRECTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'STOP']

class Snake:
    def __init__(self, board, food): 
        self.board = board
        mid_point = len(board) // 2
        self.position_head = [mid_point, mid_point]
        self.position_tail = self.position_head[:]
        self.length = 1
        self.direction = 'STOP'
        self.board_size = len(board)
        self.food = food

        self.board[self.position_head[0]][self.position_head[1]] = 2 # Starta mitt på spelplanen
        
    def set_direction(self, direction_key):
        new_direction = None

        if direction_key == pygame.K_w and self.direction != 'DOWN':
            new_direction = 'UP'
        elif direction_key == pygame.K_s and self.direction != 'UP':
            new_direction = 'DOWN'
        elif direction_key == pygame.K_a and self.direction != 'RIGHT':
            new_direction = 'LEFT'
        elif direction_key == pygame.K_d and self.direction != 'LEFT':
            new_direction = 'RIGHT'

        # Only set the direction if it's a valid direction
        if new_direction in DIRECTIONS:
            self.direction = new_direction
            
    def move(self):
        old_head_position = self.position_head.copy()

        if self.direction == 'UP':
            self.position_head[1] = (self.position_head[1] - 1) % self.board_size
        elif self.direction == 'DOWN':
            self.position_head[1] = (self.position_head[1] + 1) % self.board_size
        elif self.direction == 'LEFT':
            self.position_head[0] = (self.position_head[0] - 1) % self.board_size
        elif self.direction == 'RIGHT':
            self.position_head[0] = (self.position_head[0] + 1) % self.board_size

        if self.board[self.position_head[0]][self.position_head[1]] in [1, 3]:
            print("Game over")
            self.running = False  # Stop the game
            pygame.quit()
            return
        elif self.board[self.position_head[0]][self.position_head[1]] == 5:
            self.length += 1
            self.food.eat_food()
            print("Food eaten! new length: ", self.length)
        elif self.board[self.position_head[0]][self.position_head[1]] == 6:
            self.length += 1
            self.food.eat_special_food()
            print("Food eaten! new length: ", self.length)
            
        self.board[self.position_head[0]][self.position_head[1]] = 2 
        self.board[old_head_position[0]][old_head_position[1]] = 0
        
