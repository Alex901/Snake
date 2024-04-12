import sys
import pygame
from Menu import Menu
from Snake import Snake
from Food import Food
from queue import PriorityQueue

CELL_SIZE = 15  # Storleken på varje cell i pixlar
GRID_SIZE = 31  # Antal celler i varje riktning
SCREEN_SIZE = CELL_SIZE * GRID_SIZE # Definierar storleken på fönstret i pixlar
SCORE = 0 # Variabel som håller koll på poängen
SCORE_MULTIPLIER = 1 # Variabel som håller koll på poängmultiplikatorn
GAME_SPEED = 10 # Variabel som håller koll på spelets hastighet
LEVEL = 1


class Game: # Klassen som hanterar spelet 
    def __init__(self, board_size=GRID_SIZE):   # Konstruktor, skulle int behöva variabeln för board_size här. 
        pygame.display.set_caption("SNAKE ITH")     # Sätter titeln för fönstret till Snake
        self.score = 0; # Variabel som håller koll på poängen
        self.level = 1; # Variabel som håller koll på vilken nivå spelaren är på
        self.board_size = board_size # Storleken på spelplanen
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))   # Skapar fönstret med definierad storlek
        self.menu = Menu(self.screen, self)  # Skapar en huvudmenyn
        self.DIFFICULTY = ["Easy", "Medium", "Hard","Impossible"] 
        self.BORDERS = ["On", "Off"] 
        self.borders = 0    # Denna är nog överflödig
        self.difficulty = 0  
        self.game_board = [[0 for _ in range(board_size)] for _ in range(board_size)]  # Skapar spelmatrisen
        self.update_border()  # Uppdaterar om det ska finnas kanter eller inte
        self.food = Food(self) # Skapar klassen för maten
        self.start = False 
        self.snake = Snake(self)
        self.clock = pygame.time.Clock()  # Skapar en klocka för att hålla koll på spelets hastighet
        self.god = False # Variabel som håller koll på om autospel är på eller inte
        self.game_speed = 0; 
    
    def update_gamespeed(self):     # Funktion som uppdaterar spelets hastighet
        self.game_speed = 8 + self.difficulty*8 * self.level*0.2 
        
    
    def update_border(self): # Funktion som uppdaterar om det ska finnas kanter eller inte
        if self.borders == 0:
            for i in range(self.board_size):
                self.game_board[0][i] = 1 
                self.game_board[self.board_size - 1][i] = 1
                self.game_board[i][0] = 1
                self.game_board[i][self.board_size - 1] = 1
        else:
            for i in range(self.board_size):
                self.game_board[0][i] = 0
                self.game_board[self.board_size - 1][i] = 0
                self.game_board[i][0] = 0
                self.game_board[i][self.board_size - 1] = 0
        
        
    def draw_score_level(self):
        font = pygame.font.Font(None, 36)  # ritar ut poäng och nivå
        score_text = font.render(f"Score: {self.score}", True, (176,196,222))  
        level_text = font.render(f"Level: {self.level}", True, (176,196,222))  

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))
                        
    def draw_grid(self): # Funktion som ritar ut spelplanen baserat på spelmatrisen
        for i in range(self.board_size):
            for j in range(self.board_size):
                x = i * CELL_SIZE
                y = j * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (76, 187, 23), rect, 1) # Ritar ut rutnätet

                inner_rect = pygame.Rect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2)
                if self.game_board[i][j] == 1:      # Stenväggarna
                    pygame.draw.rect(self.screen, (189, 180, 169), inner_rect, 0)
                elif self.game_board[i][j] == 2: # Ormens Huvud
                    pygame.draw.rect(self.screen, (0, 0, 128), inner_rect, 0)
                elif self.game_board[i][j] == 3: # Ormens Kropp
                    pygame.draw.rect(self.screen, (72, 61, 139), inner_rect, 0)
                elif self.game_board[i][j] == 5: # Maten
                    pygame.draw.circle(self.screen, (0, 255, 0), inner_rect.center, inner_rect.width//2)
                elif self.game_board[i][j] == 6: # Specialmaten
                    pygame.draw.circle(self.screen, (255, 0, 0), inner_rect.center, inner_rect.width//2)
                else:   # Tom cell = "gärs"
                    pygame.draw.rect(self.screen, (34,139,34), inner_rect, 0)
        
    def run(self): # Huvudloopen för spelet
        choice = None   # För att hålla spelaren i menyn ända tills spelaren väljer "starta"
        while choice != "Start":
            self.menu.display()
            pygame.display.flip()
            choice = self.menu.handle_input()
        
        self.running = True
        self.draw_grid()   
        self.draw_score_level()  
        pygame.display.flip() # Uppdaterar fönstret

        while self.running:     # Huvudloopen för själva spelet
            for event in pygame.event.get():   # Loopar igenom alla händelser som sker
                if event.type == pygame.QUIT:  # Så man kan stänga ner spelet
                    sys.exit()
                elif event.type == pygame.KEYDOWN:  # Om en tangent trycks ner
                    if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]: # Om det är en riktningstangent = börja spelet
                        self.start = True
                        self.update_gamespeed()
                        self.snake.set_direction(event.key)
                    elif event.key == pygame.K_g:
                        self.god = not self.god
                        self.start = not self.start
            
            if self.start: # Om spelet har startat     
                self.print_board(self.snake.body)
                if self.god:
                    self.update_gamespeed()
                    self.auto_play()
                    
                self.draw_grid()  
                self.draw_score_level() 
                self.food.remove_special_food() # Ta bort specialmaten om den har existerat för länge
                pygame.display.flip()  # Uppdaterar fönstret
                
                self.clock.tick(self.game_speed)  # Uppdaterar klockan
                if not self.food.exists: # Om det inte finns någon mat på spelplanen
                    self.food.spawn_food() # Skapa ny mat

                
            self.snake.move()   # Flytta ormen         

        pygame.quit()  # Stänger ner pygame
        
    def auto_play(self):
        self.start = True  # Ifall man inte har startat spelet
        food_pos, special_food_pos, head_pos = self.find_positions()
        print("Food pos: ", food_pos, special_food_pos, head_pos)
        
        target_pos = special_food_pos if special_food_pos is not None else food_pos 
        print("Target pos: ", target_pos)
        if target_pos is not None:
            path = self.A_star(head_pos, target_pos)
            self.print_board(path)
        else: 
            target_pos = (self.board_size // 2, self.board_size // 2)
            path = self.A_star(head_pos, target_pos)
            self.print_board(path)
        if path:  # Check if the path list is not empty
            next_pos = path[0]  # Get the next position from the path
            self.snake.direction = self.get_direction(self.snake.position_head, next_pos)  # Set the snake's direction
            self.snake.set_direction(self.snake.direction)  # Update the snake's direction
            path.pop(0)  # Remove the next position from the path
        else:
            print("No path found")

    def get_next_position(self, direction):
        directions = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}
        head_pos = self.snake.position_head

        if direction == 'STOP':
            return head_pos

        dx, dy = directions[direction]
        return (head_pos[0] + dx, head_pos[1] + dy) 

    def A_star(self, start, target):
        open_set = PriorityQueue()
        open_set.put((0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, target)}

        while not open_set.empty():
            current = open_set.get()[1]
            if current == target:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]

            for neighbor in self.get_neighbors(current):
                temp_g_score = g_score[current] + 1

                if neighbor in self.snake.body[1:]:
                    # If the neighbor cell is occupied by a part of the snake, add a cost based on the position of that part
                    temp_g_score += 1000 / (2 ** (len(self.snake.body) - self.snake.body.index(neighbor) - 1))
                elif self.game_board[neighbor[0]][neighbor[1]] == 1 or self.game_board[neighbor[0]][neighbor[1]] == 3:
                    temp_g_score += 1000

                if temp_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.heuristic(neighbor, target)
                    open_set.put((f_score[neighbor], neighbor))
    
    def heuristic(self, pos, target):
        return abs(pos[0] - target[0]) + abs(pos[1] - target[1])
    
    def get_neighbors(self, pos):
        neighbors = [
            (pos[0] - 1, pos[1]), 
            (pos[0] + 1, pos[1]), 
            (pos[0], pos[1] - 1), 
            (pos[0], pos[1] + 1),  
        ]


        return [neighbor for neighbor in neighbors if 0 <= neighbor[0] < len(self.game_board[0]) and 0 <= neighbor[1] < len(self.game_board) and neighbor not in self.snake.body[1:]]
    
    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        return path[::-1]
    
    def distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def is_valid(self, pos):
        x, y = pos
        valid = (
            0 <= x < self.board_size and 
            0 <= y < self.board_size and 
            self.game_board[x][y] != '1' and  
            (x, y) not in self.snake.body  
        )
        if not valid:
            if not (0 <= x < self.board_size and 0 <= y < self.board_size):
                print(f"Position {pos} is out of bounds")
            elif self.game_board[x][y] == '1':
                print(f"Position {pos} is a wall")
            elif (x, y) in self.snake.body:
                print(f"Position {pos} is part of the snake's body")
        return valid
    

    def get_direction(self, current_pos, next_pos):
        dx, dy = next_pos[0] - current_pos[0], next_pos[1] - current_pos[1]
        if dx < 0:
            return 'LEFT'
        elif dx > 0:
            return 'RIGHT'
        elif dy < 0:
            return 'UP'
        else:
            return 'DOWN'

    def find_positions(self):
        food_pos = None
        special_food_pos = None
        head_pos = None

        for i in range(len(self.game_board)):
            for j in range(len(self.game_board[i])):
                if self.game_board[i][j] == 5:  # 
                    food_pos = (i, j)
                elif self.game_board[i][j] == 6:  
                    special_food_pos = (i, j)
                elif self.game_board[i][j] == 2: 
                    head_pos = (i, j)

        return food_pos, special_food_pos, head_pos
    
    def print_board(self, path):
        food_pos, special_food_pos, head_pos = self.find_positions()
        for j in range(len(self.game_board[0])):  
            for i in range(len(self.game_board)):  
                pos = (i, j)
                if pos == head_pos:
                    print('H', end='')
                elif self.game_board[i][j] == 3:
                    print('\033[31mB\033[0m', end='')
                elif pos == food_pos:
                    print('F', end='')  
                elif pos == special_food_pos:
                    print('SF', end='')
                elif pos in path:
                    print('\033[34mP\033[0m', end='')  
                else:
                    print(self.game_board[i][j], end='')  
            print()
        
    def reset(self):
        self.score = 0
        self.level = 1
        self.game_board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.update_border()
        self.food = Food(self)
        self.snake = Snake(self)
        self.god = False
        self.path = []  # Reset path for auto-play
        self.start = False
        print("Reset")
        print(self.god)
        
        
def main():
    game = Game() 
    game.run() 
        
if __name__ == "__main__":
    main()