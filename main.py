import random

import pygame


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (20, 20, 30)
SQUARE_COUNT = 1000
FPS = 60


class Square:
	def __init__(self) -> None:
		self.square_size = random.randint(10, WINDOW_WIDTH//8)
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

	def move(self) -> None:
		self.x += self.vx
		self.y += self.vy

		# Bounce on screen edges by reversing direction.
		if self.x <= 0 or self.x >= WINDOW_WIDTH - self.square_size:
			self.vx *= -1
			self.x = max(0, min(self.x, WINDOW_WIDTH - self.square_size))

		if self.y <= 0 or self.y >= WINDOW_HEIGHT - self.square_size:
			self.vy *= -1
			self.y = max(0, min(self.y, WINDOW_HEIGHT - self.square_size))

	def draw(self, surface: pygame.Surface) -> None:
		pygame.draw.rect(surface, self.color, (self.x, self.y, self.square_size, self.square_size))



def main() -> None:
	pygame.init()
	screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption("Random Moving Squares")
	clock = pygame.time.Clock()

	squares = [Square() for _ in range(SQUARE_COUNT)]
	running = True

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		for square in squares:
			square.move()

		screen.fill(BACKGROUND_COLOR)
		for square in squares:
			square.draw(screen)

		pygame.display.flip()
		clock.tick(FPS)

	pygame.quit()


if __name__ == "__main__":
	main()
