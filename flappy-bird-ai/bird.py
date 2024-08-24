import pygame

class Bird():
    def __init__(self):
        self.bird_movement = 0
        self.bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
        self.bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
        self.bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
        self.bird_frames = [self.bird_downflap,self.bird_midflap,self.bird_upflap]
        self.bird_index = 0
        self.bird_surface = self.bird_frames[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center = (100,512))
        self.BIRDFLAP = pygame.USEREVENT + 1
        self.pygame.time.set_timer(self.BIRDFLAP,200)

    def rotate_bird(self, bird):
        new_bird = pygame.transform.rotozoom(bird,-(self.bird_movement) * 3,1)
        return new_bird


    def bird_animation(self):
        self.new_bird = self.bird_frames[self.bird_index]
        self.new_bird_rect = self.new_bird.get_rect(center = (100,self.bird_rect.centery))
        return self.new_bird,self.new_bird_rect

    def move(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.bird_movement = 0
                self.bird_movement -= 12

        if event.type == self.BIRDFLAP:
            if self.bird_index < 2:
                self.bird_index += 1
            else:
                self.bird_index = 0

            self.bird_surface,self.bird_rect = self.bird_animation()