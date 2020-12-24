import pygame
from pygame.locals import *
import time
import random
SIZE = 40


class Apple:
    def __init__(self, screen):
        self.apple = pygame.image.load("resources/apple2.png").convert_alpha()
        self.screen = screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,23)*SIZE
        self.y = random.randint(1,13)*SIZE


class Snake:
    def __init__(self, screen, length):
        self.screen = screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x, self.y = [SIZE]*length, [SIZE]*length
        self.direction = 'down'
        self.length = length

    def increase_length(self):
        self.length += 1
        self.x.append(1)
        self.y.append(1)

    def draw(self):
        #self.screen.fill((25, 32, 95))
        for i in range(self.length):
            self.screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        self.draw()


class Game:


    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((1000, 600))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
             if y1 >= y2 and y1 < y2 + SIZE:
                 return True
        return False

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.wav")
        pygame.mixer.Sound.play(sound)

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg.mp3")
        pygame.mixer.music.play()

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        #snake apple collision
        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.play_sound("eat")
            self.snake.increase_length()
            self.apple.move()

        #snake collision
        for i in range(1,self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("hit")
                raise Exception("Game Over")

        #collision with boundaries
        if not (40 <= self.snake.x[0] <= 950 and 40 <= self.snake.y[0] <= 550):
            self.play_sound("hit")
            raise Exception("Game Over")

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('forte', 30)
        line1 = font.render(f"Game Over! Your Score is {self.snake.length}", True, (255,255,255))
        self.surface.blit(line1, (200, 200))
        line1 = font.render(f"To play again press Enter.  To exit press Escape", True, (255, 255, 255))
        self.surface.blit(line1, (200, 350))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def display_score(self):
        font = pygame.font.SysFont('forte', 30)
        score = font.render(f"Score: {self.snake.length-1}", True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        # EVENT LOOP
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                        self.reset()

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()
                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
            time.sleep(0.2)


if __name__ == "__main__":
    game = Game()
    game.run()


