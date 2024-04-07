import pygame
from Food import Food
import random

DIRECTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'STOP']

class Snake:    # Klassen för ormen
    def __init__(self, board, food): 
        self.board = board # för att hantera ormen behöver vi tillgång till spelplanen *duh*
        mid_point = len(board) // 2 # hitta mitten på spelplanen så vi kan starta ormen där
        self.position_head = [mid_point, mid_point] # ormens huvud
        self.length = 1 # ormens längd
        self.direction = 'STOP' # ormens riktning, STOP för att ormen inte ska röra sig från start
        self.board_size = len(board) # storleken på spelplanen, så jag kan hålla koll på om jag går utanför spelplanen 
        self.food = food    # behöver tillgång till maten för att kunna äta den
        self.body = [self.position_head[:]] # för att hålla koll på ormens kropp

        self.board[self.position_head[0]][self.position_head[1]] = 2 # Starta mitt på spelplanen
        
    def set_direction(self, direction_key): # Funktion som sätter ormens riktning, inga konstigheter
        new_direction = None   

        if direction_key == pygame.K_w and self.direction != 'DOWN':
            new_direction = 'UP'
        elif direction_key == pygame.K_s and self.direction != 'UP':
            new_direction = 'DOWN'
        elif direction_key == pygame.K_a and self.direction != 'RIGHT':
            new_direction = 'LEFT'
        elif direction_key == pygame.K_d and self.direction != 'LEFT':
            new_direction = 'RIGHT'

        
        if new_direction in DIRECTIONS: # denna if sats behövs egentligen inte, men extra felhantering är aldrig fel
            self.direction = new_direction
            
    def move(self): # Funktion som flyttar ett steg i vald riktning
        
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
            self.running = False  # TODO: Lägg till game over skärm här i något skede
            pygame.quit()
            return
        elif self.board[self.position_head[0]][self.position_head[1]] == 5: # om man äter maten
            self.food.eat_food()    
            self.length += 1
            self.body.insert(0, self.position_head[:])  # Lägg till en ny del till ormens kropp
        elif self.board[self.position_head[0]][self.position_head[1]] == 6: # om man äter specialmaten
            self.food.eat_special_food()
            self.length += 1
            self.body.insert(0, self.position_head[:]) 
            
            num_walls = random.randint(1, 5)  # lägger till 1-5 väggar när man äter specialmaten

            for _ in range(num_walls):
                while True:
                    wall_x = random.randint(0, self.board_size - 1)
                    wall_y = random.randint(0, self.board_size - 1)
                    if self.board[wall_x][wall_y] == 0:  
                        self.board[wall_x][wall_y] = 1
                        break
        else:
            self.body.insert(0, self.position_head[:]) 
            old_tail_position = self.body.pop() 
            self.board[old_tail_position[0]][old_tail_position[1]] = 0  
            
        for position in self.body[1:]:  # Rita ut ormens kropp
            self.board[position[0]][position[1]] = 3

        self.board[self.position_head[0]][self.position_head[1]] = 2 # Rita ut ormens huvud
        

        