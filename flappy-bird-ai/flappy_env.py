import pygame, sys, random
from pygame import display, time
from pygame.surfarray import array3d
from pygame.event import pump
import gymnasium as gym
from gymnasium import spaces
import cv2
import numpy as np

class FlappyEnv(gym.Env):

	def draw_floor(self):
		self.screen.blit(floor_surface,(floor_x_pos,900))
		self.screen.blit(floor_surface,(floor_x_pos + 576,900))

	def create_pipe(self):
		random_pipe_pos = random.choice(pipe_height)
		bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
		top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 300))
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

	def check_collision(self, pipes):
		global can_score
		for pipe in pipes:
			if bird_rect.colliderect(pipe):
				death_sound.play()
				can_score = True
				return False

		if bird_rect.top <= -100 or bird_rect.bottom >= 900:
			can_score = True
			return False

		return True

	def rotate_bird(self, bird):
		new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
		return new_bird

	def bird_animation(self):
		new_bird = bird_frames[bird_index]
		new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
		return new_bird,new_bird_rect

	def score_display(self, game_state):
		if game_state == 'main_game':
			score_surface = game_font.render(str(int(score)),True,(255,255,255))
			score_rect = score_surface.get_rect(center = (288,100))
			screen.blit(score_surface,score_rect)
		if game_state == 'game_over':
			score_surface = game_font.render(f'Score: {int(score)}' ,True,(255,255,255))
			score_rect = score_surface.get_rect(center = (288,100))
			screen.blit(score_surface,score_rect)

			high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
			high_score_rect = high_score_surface.get_rect(center = (288,850))
			screen.blit(high_score_surface,high_score_rect)

	def update_score(score, high_score):
		if score > high_score:
			high_score = score
		return high_score

	def pipe_score_check():
		global score, can_score 
		
		if pipe_list:
			for pipe in pipe_list:
				if 95 < pipe.centerx < 105 and can_score:
					score += 1
					score_sound.play()
					can_score = False
				if pipe.centerx < 0:
					can_score = True

	def __init__(self):
		super(FlappyEnv, self).__init__()
		pygame.init()

		self.history = []
		for i in range(0,6):
			self.history.append(np.zeros((576,1024)))
		
		self.screen = pygame.display.set_mode((576,1024))
		self.clock = pygame.time.Clock()
		self.game_font = pygame.font.Font('04B_19.ttf',40)

		n_actions = 2
		self.action_space = spaces.Discrete(n_actions)
		self.observation_space = spaces.Box(low=0, high=1024, shape=(576,1024,1), dtype=np.uint8)

		self.gravity = 0.25
		self.bird_movement = 0
		self.game_active = True
		self.score = 0
		self.high_score = 0
		self.can_score = True
		self.bg_surface = pygame.image.load('assets/background-day.png').convert()
		self.bg_surface = pygame.transform.scale2x(bg_surface)

		self.floor_surface = pygame.image.load('assets/base.png').convert()
		self.floor_surface = pygame.transform.scale2x(floor_surface)
		self.floor_x_pos = 0

		self.bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
		self.bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
		self.bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
		self.bird_frames = [bird_downflap,bird_midflap,bird_upflap]
		self.bird_index = 0
		self.bird_surface = bird_frames[bird_index]
		self.bird_rect = bird_surface.get_rect(center = (100,512))

		self.BIRDFLAP = pygame.USEREVENT + 1
		pygame.time.set_timer(BIRDFLAP,200)

		self.pipe_surface = pygame.image.load('assets/pipe-green.png')
		self.pipe_surface = pygame.transform.scale2x(pipe_surface)
		self.pipe_list = []
		self.SPAWNPIPE = pygame.USEREVENT
		pygame.time.set_timer(SPAWNPIPE,1200)
		self.pipe_height = [400,600,800]

		self.game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
		self.game_over_rect = game_over_surface.get_rect(center = (288,512))

		self.SCOREEVENT = pygame.USEREVENT + 2
		pygame.time.set_timer(SCOREEVENT,100)
        
	def reset(self):
		self.history_frame = np.zeros((576,1024))
		self.history_frame_2 = np.zeros((576,1024))
		self.screen.fill((0,0,0))

		self.gravity = 0.25
		self.bird_movement = 0
		self.game_active = True
		self.score = 0
		self.high_score = 0
		self.can_score = True
		self.bg_surface = pygame.image.load('assets/background-day.png').convert()
		self.bg_surface = pygame.transform.scale2x(bg_surface)

		self.floor_surface = pygame.image.load('assets/base.png').convert()
		self.floor_surface = pygame.transform.scale2x(floor_surface)
		self.floor_x_pos = 0

		self.bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
		self.bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
		self.bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
		self.bird_frames = [bird_downflap,bird_midflap,bird_upflap]
		self.bird_index = 0
		self.bird_surface = bird_frames[bird_index]
		self.bird_rect = bird_surface.get_rect(center = (100,512))

		self.BIRDFLAP = pygame.USEREVENT + 1
		pygame.time.set_timer(BIRDFLAP,200)

		self.pipe_surface = pygame.image.load('assets/pipe-green.png')
		self.pipe_surface = pygame.transform.scale2x(pipe_surface)
		self.pipe_list = []
		self.SPAWNPIPE = pygame.USEREVENT
		pygame.time.set_timer(SPAWNPIPE,1200)
		self.pipe_height = [400,600,800]

		self.game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
		self.game_over_rect = game_over_surface.get_rect(center = (288,512))

		self.SCOREEVENT = pygame.USEREVENT + 2
		pygame.time.set_timer(SCOREEVENT,100)

		image = cv2.cvtColor(cv2.resize(image, (576,1024)), cv2.COLOR_BGR2GRAY)
		_, image = cv2.threshold(image, 1, 576, cv2.THRESH_BINARY)
		image = image / 255

		del self.history[0]
		self.history.append(image)
		#print(type(image))
		#print(image.shape)
		image = np.concatenate((self.history[-5], self.history[-3], image), axis=0)
		#print(image.shape)
		image = np.expand_dims(image, axis=-1)
		#print(image.shape)
		return image


	def step(self, action):
		scoreholder = self.score
		self.screen.fill((0, 0, 0))

		pump()

		reward = -0.001
		done = False

		if action == 1:
			self.bird_movement = 0
			self.bird_movement -= 12

	def render(self):
		if self.game_active == True:
			# Bird
			self.bird_movement += gravity
			self.rotated_bird = rotate_bird(bird_surface)
			self.bird_rect.centery += bird_movement
			self.screen.blit(rotated_bird,bird_rect)
			self.game_active = check_collision(pipe_list)

			# Pipes
			self.pipe_list = move_pipes(pipe_list)
			self.draw_pipes(pipe_list)
			
			# Score
			self.pipe_score_check()
			self.score_display('main_game')
		else:
			self.screen.blit(game_over_surface,game_over_rect)
			self.high_score = update_score(score,high_score)
			self.score_display('game_over')

		# Floor
		self.floor_x_pos -= 1
		self.draw_floor()
		if self.floor_x_pos <= -576:
			self.floor_x_pos = 0

	def close(self):
		pass

	def preprocessing(self, image):
		pass


		

def draw_floor():
	screen.blit(floor_surface,(floor_x_pos,900))
	screen.blit(floor_surface,(floor_x_pos + 576,900))

def create_pipe():
	random_pipe_pos = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 300))
	return bottom_pipe,top_pipe

def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= 5
	visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
	return visible_pipes

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= 1024:
			screen.blit(pipe_surface,pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface,False,True)
			screen.blit(flip_pipe,pipe)

def check_collision(pipes):
	global can_score
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			death_sound.play()
			can_score = True
			return False

	if bird_rect.top <= -100 or bird_rect.bottom >= 900:
		can_score = True
		return False

	return True

def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
	return new_bird

def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
	return new_bird,new_bird_rect

def score_display(game_state):
	if game_state == 'main_game':
		score_surface = game_font.render(str(int(score)),True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)
	if game_state == 'game_over':
		score_surface = game_font.render(f'Score: {int(score)}' ,True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)

		high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
		high_score_rect = high_score_surface.get_rect(center = (288,850))
		screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score

def pipe_score_check():
	global score, can_score 
	
	if pipe_list:
		for pipe in pipe_list:
			if 95 < pipe.centerx < 105 and can_score:
				score += 1
				score_sound.play()
				can_score = False
			if pipe.centerx < 0:
				can_score = True

#pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 2, buffer = 1024)
pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True
bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [400,600,800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,512))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100
SCOREEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SCOREEVENT,100)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active:
				bird_movement = 0
				bird_movement -= 12
				flap_sound.play()
			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				pipe_list.clear()
				bird_rect.center = (100,512)
				bird_movement = 0
				score = 0

		if event.type == SPAWNPIPE:
			pipe_list.extend(create_pipe())

		if event.type == BIRDFLAP:
			if bird_index < 2:
				bird_index += 1
			else:
				bird_index = 0

			bird_surface,bird_rect = bird_animation()

	screen.blit(bg_surface,(0,0))

	if game_active:
		# Bird
		bird_movement += gravity
		rotated_bird = rotate_bird(bird_surface)
		bird_rect.centery += bird_movement
		screen.blit(rotated_bird,bird_rect)
		game_active = check_collision(pipe_list)

		# Pipes
		pipe_list = move_pipes(pipe_list)
		draw_pipes(pipe_list)
		
		# Score
		pipe_score_check()
		score_display('main_game')
	else:
		screen.blit(game_over_surface,game_over_rect)
		high_score = update_score(score,high_score)
		score_display('game_over')


	# Floor
	floor_x_pos -= 1
	draw_floor()
	if floor_x_pos <= -576:
		floor_x_pos = 0
	

	pygame.display.update()
	clock.tick(120)
