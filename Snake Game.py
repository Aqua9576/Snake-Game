import pygame, sys, random
from pygame.math import Vector2
pygame.font.init()

pygame.init()

class FRUIT():
    def __init__(self,cell_number, cell_size, screen):
        self.cell_number = cell_number
        self.cell_size = cell_size
        self.screen = screen
        self.x = random.randint(0, cell_number - 2)
        self.y = random.randint(0, cell_number - 2)
        self.pos = Vector2(self.x, self.y)


    def drawfruit(self):
        fruit_rect = pygame.Rect(int (self.pos.x * self.cell_size), (self.pos.y * self.cell_size), self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, pygame.Color("blue"), fruit_rect)


class SNAKE():
    def __init__(self, cell_number, cell_size, screen):
        self.cell_number = cell_number
        self.cell_size = cell_size
        self.screen = screen
        self.body = [Vector2(7,14),Vector2(6,14),Vector2(5,14)]
        self.direction = Vector2(1,0)

    def drawsnake(self):
        for blocks in self.body:
            x_coord = (blocks.x * self.cell_size)
            y_coord = int (blocks.y * self.cell_size)
            snake_rect = pygame.Rect(x_coord, y_coord, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen,pygame.Color("red"),snake_rect)


    def movement(self): #inserts a new block from the 0th iteration at 0 and deletes the last element of the list
        body_copy = self.body[:-1]
        body_copy.insert(0,body_copy[0] + self.direction)
        self.body = body_copy
    

class MAIN():
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.cell_size = 40
        self.cell_number = 20
        self.height = 700
        self.screen = pygame.display.set_mode((self.cell_number * self.cell_size,self.height))
        self.snake = SNAKE(self.cell_number, self.cell_size, self.screen)
        self.fruit = FRUIT(self.cell_number, self.cell_size, self.screen)
        self.high_score = {}
        self.fruitseaten = 0
        self.game_flag = True
        self.game_state = True

    def update(self): #continuously checks the events happening
        snake, fruit, flag = self.death_checker()
        self.snake = snake
        self.fruit = fruit
        self.snake.movement()
        self.hitbox()
        self.quit_game()

    def draw_elements(self):
        self.fruit.drawfruit()
        self.snake.drawsnake()
    
    def hitbox(self): #checks if snakehead hits food
        if self.fruit.pos == self.snake.body[0]:
            self.fruitseaten += 1
            self.snake.body.append(self.snake.body[1])
            self.fruit.x = random.randint(0, self.cell_number - 5)
            self.fruit.y = random.randint(0, self.cell_number - 5)
            self.fruit.pos = Vector2(self.fruit.x, self.fruit.y)
    
    
    def death_checker(self): #checks if snake hits the boundary or the snake hits itself
        if (not 0 <= self.snake.body[0].x <= self.cell_number) or (not 0 <= self.snake.body[0].y <= self.cell_number):
            snake, fruit, flag =  self.game_over()
            return snake, fruit, flag
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
               snake, fruit, flag = self.game_over()
               return snake, fruit, flag
        return self.snake, self.fruit, self.game_flag

    def game_over(self): #asks name and checks for retry
        name = ""
        name_label = "Name: "
        name_text = self.font.render(name_label, True, (255, 255, 255))
        case = False
        while True:
            my_name = self.font.render(name, True, (255, 255, 255))
            self.screen.blit(name_text, (250, 250))
            self.screen.blit(my_name, (325, 250))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key != pygame.K_RETURN:
                        name += chr(event.key)
                    if event.key == pygame.K_RETURN:
                        case = True
                        if case == True:
                            break
            pygame.display.update()
            self.screen.fill((0,0,0))
            if case == True:
                break 
        try_again = "Do you want to try again? y/n"
        try_again_text = self.font.render(try_again, True, (255, 255, 255))
        while True:
            self.screen.blit(try_again_text, (240, 320))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        self.game_flag = False
                    elif event.key == pygame.K_y:
                        self.game_flag = True    
                    new_snake = SNAKE(self.cell_number, self.cell_size, self.screen)
                    new_fruit = FRUIT(self.cell_number, self.cell_size, self.screen)
                    ind_score = self.calculate_score(self.fruitseaten)
                    self.high_score[name] = ind_score
                    self.fruitseaten = 0
                    return new_snake, new_fruit, self.game_flag
            pygame.display.update()
        
    def calculate_score(self, fruitseaten): #calculates the score for each individual
        if fruitseaten == 0:
            return 0
        else:
            individual_score = self.calculate_score(fruitseaten - 1) + 10 
            return individual_score
        
    def quit_game(self): #shows score and quits the game
        if self.game_flag == False:
                self.scores()

    def scores(self): #displays the final scores of all players
        new_screen = pygame.display.set_mode((self.cell_number * self.cell_size,self.height))
        player_text = self.font.render("Player Name:", True, (255, 255, 255))
        scores_text = self.font.render("Score:", True, (255, 255, 255))
        new_screen.blit(player_text, (200, 200))
        new_screen.blit(scores_text, (500, 200))
        stepper = 1
        pygame.display.update()
        for names in self.high_score:
            individual_name_text = self.font.render((names), True, (255,255,255))
            individual_score_text = self.font.render(str(self.high_score[names]), True, (255, 255, 255))
            new_screen.blit (individual_name_text, (200, 200 + (20 * (stepper))))
            new_screen.blit (individual_score_text, (500, 200 + (20 * (stepper))))
            stepper += 1
            pygame.display.update()


    def start_game(self): #game initializer
        time = pygame.time.Clock()
        snake_update = pygame.USEREVENT
        pygame.time.set_timer(snake_update, 150)
        while self.game_flag == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == snake_update:
                    self.update()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.snake.direction != Vector2(0,1):
                        self.snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_DOWN and self.snake.direction != Vector2(0,-1):
                        self.snake.direction = Vector2(0, 1)
                    if event.key == pygame.K_LEFT and self.snake.direction != Vector2(1,0):
                        self.snake.direction = Vector2(-1, 0)
                    if event.key == pygame.K_RIGHT and self.snake.direction != Vector2(-1,0):
                        self.snake.direction = Vector2(1, 0)
            self.screen.fill((0,0,0))
            self.draw_elements()
            pygame.display.update()
            time.tick(60)
        self.scores()
        pygame.display.update()
        pygame.time.delay(3000)
        pygame.quit()
        sys.exit()


while True:
    main_game = MAIN()
    main_game.start_game()
    print (main_game.game_flag)