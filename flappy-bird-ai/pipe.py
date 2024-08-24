import pygame
import random

class Pipe():
    def __init__(self):
        self.pipe_surface = pygame.image.load('assets/pipe-green.png')
        self.pipe_surface = pygame.transform.scale2x(self.pipe_surface)
        self.pipe_list = []
        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE,1200)
        self.pipe_height = [400,600,800]

    def create_pipe(self):
        random_pipe_pos = random.choice(self.pipe_height)
        bottom_pipe = self.pipe_surface.get_rect(midtop = (700,random_pipe_pos))
        top_pipe = self.pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 300))
        return bottom_pipe,top_pipe

    def move_pipes(self, pipes):
        for pipe in pipes:
            pipe.centerx -= 5
        visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
        return visible_pipes

    def draw_pipes(self, pipes):
        for pipe in pipes:
            if pipe.bottom >= 1024:
                screen.blit(pipe_surface,pipe)
            else:
                flip_pipe = pygame.transform.flip(pipe_surface,False,True)
                screen.blit(flip_pipe,pipe)