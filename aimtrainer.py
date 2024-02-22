import pygame 
import math
import random
import time

pygame.init() # initialize pygame

WIDTH, HEIGHT = 600, 400 # number of pixels for window

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # open a window on screen
pygame.display.set_caption("Aim Trainer") # name of window

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT 
TARGET_PADDING = 30

BG_COLOR = (0, 25, 40) # RGB
LIVES = 3
TOP_BAR_HEIGHT = 50

LABEL_FONT = pygame.font.SysFont("comicsans", 24) # font size

class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    SECOND_COLOR = "yellow"
    
    def __init__(self, x, y): # x and y is where we place target on screen
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE: # if we reach max size, then go false
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE # if self.grow is true, then keep growing
        else:
            self.size -= self.GROWTH_RATE # if false, then shrink

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8) # changes based on current target size
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)

    def collide(self, x, y):
        dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return dis <= self.size # If the distance is less than or equal to the size, it returns True, indicating a collision has occurred. If the distance is greater than the size, it returns False, indicating no collision has occurred.


def draw(win, targets):
    win.fill(BG_COLOR) # fill window with bg color
    
    for target in targets:
        target.draw(win)


def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100) # give us number of ms 
    seconds = int(round(secs % 60, 1)) # take seconds, mod by 60 
    minutes = int(secs // 60) 

    return f"{minutes:02d}:{seconds:02d}:{milli}" # always has 2 digits, if not 2 digits, then start with 0 ; 01,02,03

def draw_top_bar(win, elapsed_time, target_pressed, misses):
    pygame.draw.rect(win, "green", (0, 0, WIDTH, TOP_BAR_HEIGHT)) # present on window, in green color, start at 0,0 which is top left corner, then take up the entire width, but only our pre-defined height of 50
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, "black") # text you want to draw, and colour 
    
    speed = round(target_pressed / elapsed_time, 1) # round to 1 decimal place
    speed_label = LABEL_FONT.render(
        f"Speed: {speed} t/s", 1, "black")
    
    hits_label = LABEL_FONT.render(
        f"Hits: {target_pressed}", 1, "black"
    )
    
    lives_label = LABEL_FONT.render(
        f"Lives: {LIVES - misses}", 1, "black"
    )

    win.blit(time_label, (5, 5)) # coordinates 
    win.blit(speed_label, (200, 5)) 
    win.blit(hits_label, (400, 5))
    win.blit(lives_label, (500, 5)) 
 
def end_screen(win, elapsed_time, target_pressed, clicks):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, "white") # text you want to draw, and colour 
    
    speed = round(target_pressed / elapsed_time, 1) # round to 1 decimal place
    speed_label = LABEL_FONT.render(
        f"Speed: {speed} t/s", 1, "white")
    
    hits_label = LABEL_FONT.render(
        f"Hits: {target_pressed}", 1, "white"
    )

    accuracy = round(target_pressed / clicks * 100, 1)
    accuracy_label = LABEL_FONT.render(
        f"Accuracy: {accuracy}%", 1, "white"
    )

    win.blit(time_label, (get_middle(time_label), 100)) # coordinates 
    win.blit(speed_label, (get_middle(speed_label), 150)) 
    win.blit(hits_label, (get_middle(hits_label), 200))
    win.blit(accuracy_label, (get_middle(accuracy_label), 250))

    pygame.display.update()
    
    run = True 
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN: 
                run = False
                break

def get_middle(surface):
    return WIDTH / 2 - surface.get_width() / 2 

def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    target_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT) # trigger this event every target increment ms

    while run:
        clock.tick(60) # run this loop at 60 fps
        click = False
        mouse_position = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get(): # loop through every event in pygame
            if event.type == pygame.QUIT: # if we quit, end loop
                run = False
                break

            if event.type == TARGET_EVENT: # if user playing
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING) # generate a randint in the range of: target padding (30) and the width - target_padding -> so the radius does not go off screen
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)

                target = Target(x, y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1 

        for target in targets:
            target.update() # change size of target; doesn't start from 0
            if target.size <= 0:
                targets.remove(target) # remove target from screen when size is 0 so comp doesnt slow down
                misses += 1 # if its 0 we didn't press the target so we missed

            if click and target.collide(*mouse_position): # * will break down the tupple to individual components so it gives us x and y separately
                targets.remove(target)
                target_pressed += 1 

        if misses >= LIVES:
            end_screen(WIN, elapsed_time, target_pressed, clicks)

        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, target_pressed, misses)
        pygame.display.update()


    pygame.quit()

if __name__ == "__main__":
    main()




