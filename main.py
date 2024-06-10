import pygame, random

pygame.init()
pygame.font.init()
pygame.display.init()

WIDTH, HEIGHT = 800, 800
SQ_HEIGHT = 40
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
       
class grid(object):
    def __init__(self, SQ_HEIGHT):
        self.x = 0
        self.y = 0
        self.width = 40
        self.height = SQ_HEIGHT
        self.colour = True

    def draw(self):
        top_bar = pygame.Rect(0,0, (self.width*WIDTH//self.width), self.height)
        pygame.draw.rect(win, "white", top_bar)
        self.x = 0
        self.y = 0 + self.height
        for _ in range(0,HEIGHT//self.height):
            for _ in range(0, WIDTH//self.width):
                square = pygame.Rect(self.x,self.y,self.width,self.height)
                if self.colour:
                    pygame.draw.rect(win, (162,209,73), square)
                    self.x += self.width
                    self.colour = False
                else:
                    pygame.draw.rect(win, (170,215,81), square)
                    self.x += self.width
                    self.colour = True

            if self.colour:
                self.colour = False
            else:
                self.colour = True

            self.x = 0
            self.y += self.height
        self.x = 0
        self.y = 0
        
class snake_part(object):
    def __init__(self):
        self.x = 5
        self.y = 5 + SQ_HEIGHT
        self.width = 30
        self.height = 30
        self.vel = 2
        self.target_x = 45
        self.target_y = 5
        self.up = False
        self.down = False
        self.left = False
        self.right = True
        self.hitbox = [self.x, self.y, self.width, self.height]

    def draw(self):
        self.snake_head = pygame.Rect(self.x,self.y,self.width,self.height)
        self.hitbox = [self.x, self.y, self.width, self.height]
        pygame.draw.rect(win, "blue", self.snake_head) 
        
class fruit(object):
    def __init__(self):
        self.x = 7.5
        self.y = 7.5
        self.width = 25
        self.height = 25
        self.seed = 1
        self.hitbox = [self.x, self.y, self.width, self.height]
    
    def random_place(self):
        random.seed(self.seed)
        self.x = ((random.randint(0,WIDTH//40))*40) + 7.5
        self.y = ((random.randint(0,HEIGHT//40))*40) + 7.5
        if self.x < 0 or self.x > 800 or self.y < 0 + SQ_HEIGHT or self.y > 800:
            self.random_seed()
            self.random_place()
    
    def draw(self):
        self.random_place()
        self.apple = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hitbox = [self.x, self.y, self.width, self.height]
        pygame.draw.rect(win, "red", self.apple)
    
    def random_seed(self):
        self.seed = random.randint(0,HEIGHT**WIDTH)
        self.random_place()

def redraw_display():
    win.fill((0,0,0))
    text = score_font.render("Score: " + str(score), 1, (0,0,0) )
    grid.draw()
    win.blit(text, (5,-5))
    fruit.draw()
    snake.draw()
    pygame.display.update()

### MAIN ###
clock = pygame.time.Clock()
snake = snake_part()
grid = grid(SQ_HEIGHT)
fruit = fruit()
score_font = pygame.font.SysFont("comicsans", 34, True, False)
score = 0
run = True
change = "right"

while run:
    clock.tick(60)

    for event in pygame.event.get(): # Red X exit Clause
        if event.type == pygame.QUIT:
            run = False        
    
    if snake.x != snake.target_x and snake.right: # Checks to see if snake has reached next square and increments with its vel if not in the correct direction
        snake.x += snake.vel
        redraw_display()
    
    elif snake.x != snake.target_x and snake.left:
        snake.x -= snake.vel
        redraw_display()
    
    elif snake.y != snake.target_y and snake.up:
        snake.y -= snake.vel
        redraw_display()
    
    elif snake.y != snake.target_y and snake.down:
        snake.y += snake.vel
        redraw_display()
    
    else:   # Change direction clause
        if change == "up":
            snake.up = True
            snake.left = False
            snake.right = False
            snake.down = False
        elif change == "left":
            snake.up = False
            snake.left = True
            snake.right = False
            snake.down = False
        elif change == "right":
            snake.up = False
            snake.left = False
            snake.right = True
            snake.down = False
        elif change == "down":
            snake.up = False
            snake.left = False
            snake.right = False
            snake.down = True

        if snake.up:    # Changes targert coords based on direction
            snake.target_y -= grid.height

        elif snake.left:
            snake.target_x -= grid.width
                
        elif snake.right:
            snake.target_x += grid.width
                
        elif snake.down:
            snake.target_y += grid.height

    if snake.x >= WIDTH - snake.width: # Boundaries
        run = False
    
    elif snake.x < 0:
        run = False
    
    elif snake.y < 0 + SQ_HEIGHT:
        run = False
    
    elif snake.y > HEIGHT - snake.height:
        run = False

    if snake.hitbox[1] < fruit.hitbox[1] + fruit.hitbox[3] and snake.hitbox[1] + snake.hitbox[3] > fruit.hitbox[1]: # Snake + Fruit hitboxes comparision
        if snake.hitbox[0] + snake.hitbox[2] > fruit.hitbox[0] and snake.hitbox[0] < fruit.hitbox[0] + fruit.hitbox[2]:
            fruit.random_seed()
            score += 1
            # Score + Increment snake size


    keys = pygame.key.get_pressed() # User inputs for direction changes

    if keys[pygame.K_UP] and not snake.up and not snake.down:
        change = "up"

    if keys[pygame.K_LEFT] and not snake.left and not snake.right:
        change = "left"
        
    if keys[pygame.K_RIGHT] and not snake.right and not snake.left:
        change = "right"
        
    if keys[pygame.K_DOWN] and not snake.down and not snake.up:
        change = "down"


pygame.quit()