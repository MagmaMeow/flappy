import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

GRAVITY = 0.5
BIRD_JUMP = -10
PIPE_SPEED = 3
PIPE_GAP = 150

class Bird:
    def __init__(self):
        self.image = pygame.Surface((34, 24))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(50, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def jump(self):
        self.velocity = BIRD_JUMP

    def draw(self):
        SCREEN.blit(self.image, self.rect)

class Pipe:
    def __init__(self, x):
        self.height = random.randint(100, HEIGHT - PIPE_GAP - 100)
        self.top_rect = pygame.Rect(x, 0, 50, self.height)
        self.bottom_rect = pygame.Rect(x, self.height + PIPE_GAP, 50, HEIGHT - self.height - PIPE_GAP)

    def update(self):
        self.top_rect.x -= PIPE_SPEED
        self.bottom_rect.x -= PIPE_SPEED

    def draw(self):
        pygame.draw.rect(SCREEN, (0, 255, 0), self.top_rect)
        pygame.draw.rect(SCREEN, (0, 255, 0), self.bottom_rect)

def main():
    bird = Bird()
    pipes = [Pipe(WIDTH + 100)]
    score = 0
    font = pygame.font.SysFont(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        bird.update()

        if pipes[-1].top_rect.x < WIDTH - 200:
            pipes.append(Pipe(WIDTH + 100))

        for pipe in pipes:
            pipe.update()

        pipes = [pipe for pipe in pipes if pipe.top_rect.x > -50]

        for pipe in pipes:
            if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
                pygame.quit()
                sys.exit()

        if bird.rect.top <= 0 or bird.rect.bottom >= HEIGHT:
            pygame.quit()
            sys.exit()

        SCREEN.fill((135, 206, 235))
        bird.draw()
        for pipe in pipes:
            pipe.draw()

        score_text = font.render(str(score), True, (255, 255, 255))
        SCREEN.blit(score_text, (WIDTH // 2, 20))

        pygame.display.flip()
        CLOCK.tick(60)

if __name__ == "__main__":
    main()
