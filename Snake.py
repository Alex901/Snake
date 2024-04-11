import pygame
from Food import Food
import random

CELL_SIZE = 15  # Inte rätt sätt att göra saker på, men att skapa config fil för globala variabler för att undvika cirkulara beroenden känns tungt just nu :'D
GRID_SIZE = 31  
SCREEN_SIZE = CELL_SIZE * GRID_SIZE
DIRECTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'STOP']

class Snake:    # Klassen för ormen
    def __init__(self, game): 
        self.game = game
        self.board = game.game_board
        mid_point = len(self.board) // 2
        self.position_head = [mid_point, mid_point]
        self.length = 1
        self.direction = 'STOP'
        self.board_size = len(self.board)
        self.board_size_px = (self.board_size*31)/15
        self.food = game.food
        self.body = [self.position_head[:]]
        self.screen = game.screen

        self.board[self.position_head[0]][self.position_head[1]] = 2
        
    def set_direction(self, direction_key): # Funktion som sätter ormens riktning, inga konstigheter
        new_direction = None   

        print("Setting new direction: ", direction_key)
        
        
        if isinstance(direction_key, str):
            if direction_key == 'UP' and self.direction != 'DOWN':
                new_direction = 'UP'
            elif direction_key == 'DOWN' and self.direction != 'UP':
                new_direction = 'DOWN'
            elif direction_key == 'LEFT' and self.direction != 'RIGHT':
                new_direction = 'LEFT'
            elif direction_key == 'RIGHT' and self.direction != 'LEFT':
                new_direction = 'RIGHT'
        else:
            if direction_key == pygame.K_w and self.direction != 'DOWN':
                new_direction = 'UP'
            elif direction_key == pygame.K_s and self.direction != 'UP':
                new_direction = 'DOWN'
            elif direction_key == pygame.K_a and self.direction != 'RIGHT':
                new_direction = 'LEFT'
            elif direction_key == pygame.K_d and self.direction != 'LEFT':
                new_direction = 'RIGHT'

        
        if new_direction in DIRECTIONS: # updatera riktningen om den är giltig
            self.direction = new_direction
            
    def move(self): # Funktion som flyttar ett steg i vald riktning
        
        # Så att ormen rör sig i rätt riktning och teleporterar till andra sidan ifall den går utanför spelplanen(om där inte finns en vägg)
        if self.direction == 'UP':
            self.position_head[1] = (self.position_head[1] - 1) % self.board_size
        elif self.direction == 'DOWN':
            self.position_head[1] = (self.position_head[1] + 1) % self.board_size
        elif self.direction == 'LEFT':
            self.position_head[0] = (self.position_head[0] - 1) % self.board_size
        elif self.direction == 'RIGHT':
            self.position_head[0] = (self.position_head[0] + 1) % self.board_size

        # Kolla om ormen krockar med något + renderar game over menyn. Jag vet, "fel" ställe :)
        if self.board[self.position_head[0]][self.position_head[1]] in [1, 3]:
            self.running = False
            
            if self.board[self.position_head[0]][self.position_head[1]] == 1:
                print("Game Over: Hit a wall")
            elif self.board[self.position_head[0]][self.position_head[1]] == 3:
                print("Game Over: Hit tail")
            else:
                print("Game Over: Other")

            font = pygame.font.Font(None, 74)  
            game_over_text = font.render("Game Over", True, (128,0,0))  
            font = pygame.font.Font(None, 44) 
            score_text = font.render(f"Score: {self.game.score}", True, (255, 255, 255))  # Create the score text
            font = pygame.font.Font(None, 36) 
            menu_text = font.render("Back to Main Menu", True, (255, 255, 255)) 

            game_over_rect = game_over_text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 3)) 
            score_rect = score_text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE * 3 // 6))  
            menu_rect = menu_text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE * 4 // 6.5))  

            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(menu_text, menu_rect)

            pygame.display.flip() 

            while True:  
                mouse_pos = pygame.mouse.get_pos()  
                
                if menu_rect.collidepoint(mouse_pos):
                    menu_text = font.render("Back to Main Menu", True, (128,0,0))
                    self.screen.blit(menu_text, menu_rect)
                else:
                    menu_text = font.render("Back to Main Menu", True, (255, 255, 255))
                    self.screen.blit(menu_text, menu_rect) 
                    
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:  
                        if menu_rect.collidepoint(mouse_pos): 
                            self.game.reset()
                            self.game.run()   
                            return
                    
        # Kolla om positionen man är i är mat
        elif self.board[self.position_head[0]][self.position_head[1]] == 5: # om man äter maten
            self.food.eat_food()    
            self.length += 1
            self.body.insert(0, self.position_head[:])  # Lägg till en ny del till ormens kropp
        #kolla om pisitionen man är i är specialmat
        elif self.board[self.position_head[0]][self.position_head[1]] == 6: 
            self.food.eat_special_food()
            self.length += 1
            self.body.insert(0, self.position_head[:]) 
            
            num_walls = random.randint(self.game.difficulty, self.game.difficulty*3)  # lägger till slumpmässigt antal väggar

            for _ in range(num_walls):
                while True:
                    wall_x = random.randint(0, self.board_size - 1)
                    wall_y = random.randint(0, self.board_size - 1)
                    if self.board[wall_x][wall_y] == 0:  
                        self.board[wall_x][wall_y] = 1
                        break
        # annars bara flytta ormen
        else:
            self.body.insert(0, self.position_head[:]) 
            old_tail_position = self.body.pop() # tar bort sista delen av ormens kropp
            self.board[old_tail_position[0]][old_tail_position[1]] = 0  # återställ celler bakom ormen
            
        for position in self.body[1:]:  # Rita ut ormens kropp i matrisen
            self.board[position[0]][position[1]] = 3

        self.board[self.position_head[0]][self.position_head[1]] = 2 # Rita ut ormens huvud i matrisen
        

        