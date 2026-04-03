import random

import pygame


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
BACKGROUND_COLOR = (20, 20, 30)
SQUARE_COUNT = 15
FPS = 60


class Square:
	cap = 40
	pity = 0
	def __init__(self) -> None:
		self.square_size = random.randint(20, WINDOW_WIDTH//10)
		self.x = random.randint(0, WINDOW_WIDTH - self.square_size)
		self.y = random.randint(0, WINDOW_HEIGHT - self.square_size)
		self.topspd = (25/self.square_size)*10
		self.vx = random.choice([-1, 1]) * random.uniform(5.0/(self.square_size*0.1), self.topspd)
		self.vy = random.choice([-1, 1]) * random.uniform(5.0/(self.square_size*0.1), self.topspd)
		self.color = (
			random.randint(60, 255),
			random.randint(60, 255),
			random.randint(60, 255),
		)
		self.pulse = 0

	def getrect(self):
		return pygame.Rect(self.x, self.y, self.square_size, self.square_size)

	@staticmethod
	def squarecreation(listofsquares):
		new = Square()
		listofsquares.append(new)
		return listofsquares

	def squarecollision(self, other, listofsquares):
		a = self.getrect()
		b = other.getrect()
		if a.colliderect(b):
			self.pulse = FPS//3
			other.pulse = FPS//3
			overlap_x = min(a.right, b.right) - max(a.left, b.left)
			overlap_y = min(a.bottom, b.bottom) - max(a.top, b.top)
			if overlap_x < overlap_y:
				if self.cap >= len(listofsquares):
					if random.randint(1, 500-Square.pity) == 1:
						Square.pity = 0
						self.squarecreation(listofsquares)
					else:
						Square.pity += 1
				
				# self is to the left
				if a.x < b.x:
					if self.vx - other.vx > 0:
						self.vx *= -1
						self.vx += random.uniform(-2.0, 2.0)
						# fix the bug where sometimes the small square move with the big square
						if other.vx < 0:
							other.vx *= -1
							other.vx += random.uniform(-2.0, 2.0)
						self.x = b.x - a.width
						
					return True
				# self is to the right
				elif a.x > b.x:
					if self.vx - other.vx < 0:
						self.vx *= -1
						self.vx += random.uniform(-2.0, 2.0)
						if other.vx > 0:
							other.vx *= -1
							other.vx += random.uniform(-2.0, 2.0)
						self.x = b.x + b.width
					
					return True
						
			else:
				# self is above
				if a.y < b.y:
					if self.vy - other.vy > 0:
						self.vy *= -1
						self.vy += random.uniform(-2.0, 2.0)
						if other.vy < 0:
							other.vy *= -1
							other.vy += random.uniform(-2.0, 2.0)
						self.y = b.y - a.height
					return True
				# self is below
				elif a.y > b.y:
					if self.vy - other.vy < 0:
						self.vy *= -1
						self.vy += random.uniform(-2.0, 2.0)
						if other.vy > 0:
							other.vy *= -1
							other.vy += random.uniform(-2.0, 2.0)
						self.y = b.y + b.height
					return True
			
			# After position set, there is a small chance to create a random square. Since there are a lot of checks
			# make the chance very low


	def move(self) -> None:
		# cap max speed.
		if self.vx > self.topspd + 5.0:
				self.vx -= 1.0
		if self.vy > self.topspd + 5.0:
				self.vy -= 1.0
		
		self.x += self.vx
		self.y += self.vy
		
		# Bounce on screen edges by reversing direction.
	def bordercollision(self, listofsquares):
		if self.x <= 0 or self.x >= WINDOW_WIDTH - self.square_size:
			self.pulse = FPS//3
			self.vx *= -1
			self.x = max(0, min(self.x, WINDOW_WIDTH - self.square_size))
			if self.cap >= len(listofsquares):
				if random.randint(1, 500-Square.pity) == 1:
					Square.pity = 0
					self.squarecreation(listofsquares)
				else:
					self.pity += 1

		if self.y <= 0 or self.y >= WINDOW_HEIGHT - self.square_size:
			self.pulse = FPS//3
			self.vy *= -1
			self.y = max(0, min(self.y, WINDOW_HEIGHT - self.square_size))
			if self.cap >= len(listofsquares):
				if random.randint(1, 500-Square.pity) == 1:
					Square.pity = 0
					self.squarecreation(listofsquares)
				else:
					self.pity += 1

	

	def draw(self, surface: pygame.Surface) -> None:
		# Using pulse boost instead of pulse for easier control of brightness. Pulse_boost spans from 0.0 to 1.0		
		pulse_boost = self.pulse / (FPS//3)
		state_color = tuple(min(255, int(c + pulse_boost*50)) for c in self.color)
		pygame.draw.rect(surface, state_color, (self.x, self.y, self.square_size, self.square_size))
		if self.pulse > 0:
			self.pulse -= 1



def main() -> None:
	pygame.init()
	screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption("Random Moving Squares")
	clock = pygame.time.Clock()
	font = pygame.font.SysFont(None, 36)
	squares = [Square() for _ in range(SQUARE_COUNT)]
	running = True

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		for square in squares:
			square.move()
			square.bordercollision(squares)
			
		for squarea in squares:
			for squareb in squares:
				if squarea != squareb:
					havewecheckthisalready = False
					for _ in range(5):
						# check 5 times to make sure small squares wont phase thru another when they move too fast
						if not havewecheckthisalready:
							havewecheckthisalready = squarea.squarecollision(squareb, squares)		

		screen.fill(BACKGROUND_COLOR)
		for square in squares:
			square.draw(screen)
		text1 = font.render(f"Squares: {len(squares)} / {Square.cap}", True, (255, 255, 255))
		text2 = font.render(f"Spawn Chance: {round((1/(500-Square.pity))*100, 3)}%", True, (255, 255, 255))
		screen.blit(text1, (10, 10))
		screen.blit(text2, (10, 10 + font.get_height()))		
		pygame.display.flip()
		clock.tick(FPS)

	pygame.quit()


if __name__ == "__main__":
	main()
