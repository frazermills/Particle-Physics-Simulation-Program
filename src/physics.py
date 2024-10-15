import math
import pygame
import buttons
from random import randint, random, uniform
from typing import List

class SolarBody:
	"""
	This is the class which describes the behaviour and functionality of the 'SolarBody' physics object.
	"""
	def __init__(self, screen, x, y):
		"""
		screen: pygame screen object
			- used as the pygame surface that all parts of the button is drawn to.
		x: int
			- this is the 'x' location of the SolarBody object.
			- pygame will use this in order to know how many pixels to draw the solar body from the left side of the screen.
		y: int
			- this is the 'y' location of the SolarBody object.
			- pygame will use this in order to know how many pixels to draw the solar body from the top of the screen.
		"""
		self.screen = screen
		self.g = 0.2
		self.mass = uniform(1, 10)
		self.size = int(self.mass / 2)
		self.x = x
		self.y = y
		self.momentum_x = uniform(200, 600)
		self.momentum_y = uniform(200, 600)
		self.dt = 0.001
		self.colour = (randint(0, 255), randint(0, 255), randint(0, 255))
		self.clicked = False
		self.text = "SolarBody"

	def move(self, x_y_central_mass):
		"""
		Given that the force between two solar bodies is proportional to the product of their masses divided by the distance between
		them squared. F = GMm/r^2
		First I calculate r^2 using Pythagoras's theorem (c^2 = a^2 + b^2)
		I can then find the force using F = GMm/r^2. Ultimately I want a velocity that I can add onto current x and y positions so
		that I can update the planets positions.
		Given that I know F = ma from Newton's second law, I can find the acceleration of the planet by dividing its force by its
		mass.
		Given also that acceleration is the rate of change of velocity with respect to time, I can integrate acceleration with
		repect to time to get velocity.
		In other words, velocity = integral of (acceleartion) dt -> v = at + c, where c is a constant. However, I can ignore c as 
		it is the velocity of the solar system relative to the universe. This means that the 'c' is the same for all solar masses 
		(the planets and the sun) in the simulation and therefore I can say that c = 0 as I am keeping the solar system's centre
		position fixed.
		Now that I have velocity vector I can resolve it into its x and y components so that I can add them to the planet's x and
		y position. To do this I must know the angle (theta) between the planet and the central mass (the sun). I can use 
		trigonometry to find this. 
		tan(theta) = opposite / adjacent = change in y / change in x -> theta = arctan(y2-y1/x2-x1)
		Now I can say the x component of velocity = velocity * cos(theta) and the y component of velocity = velocity * sin(theta).
		"""
		x2 = x_y_central_mass[0]
		y2 = x_y_central_mass[1]
		hyp = (self.x - x2) ** 2 + (self.y - y2) ** 2
		theta = math.atan2(y2 - self.y, x2 - self.x)
		force = (self.g * self.mass * 5e7) / hyp
		force_x = force * math.cos(theta)
		force_y = force * math.sin(theta)
		self.momentum_x += force_x * self.dt
		self.momentum_y += force_y * self.dt

		if self.x > self.screen.get_width() + 400 or self.x < -400:
			self.momentum_x *= -1
		if self.y > self.screen.get_height() + 400 or self.y < -400:
			self.momentum_y *= -1

		self.x += self.momentum_x / self.mass * self.dt
		self.y += self.momentum_y / self.mass * self.dt

	def draw(self):
		"""
		This method will draw a circle with centre of the x and y. It casts both of these floats to integers as pygame cannot draw
		'half of a pixel'.
		"""
		pygame.draw.circle(self.screen, self.colour, (int(self.x), int(self.y)), self.size)


class SolarSystem:
	"""
	This is the class which describes the behaviour and functionality of the 'SolarSystem' which is a collection of 'SolarBody' physics
	objects.
	"""
	def __init__(self: object, screen: object, sun_mass=5e7):
		"""
		screen: pygame screen object
			- used as the pygame surface that all parts of the button is drawn to.
		sun_mass: int [5e7]
			- this is the mass of the sun (the central mass).
			- this value will effect how strong of a graviational field there is between the SolarBody objects and this central mass.
		"""
		self.button_ls = []
		self.screen = screen
		self.sun_pos = [screen.get_width() // 2, screen.get_height() // 2]
		self.sun_mass = sun_mass

		self.planet_physics_objs = []
		for i in range(500):
			ang = uniform(0, 1) * 2 * math.pi
			hyp = math.sqrt(uniform(0, 1)) * 400
			adj = math.cos(ang) * hyp
			opp = math.sin(ang) * hyp
			x = 400 + adj
			y = 400 + opp
			p = SolarBody(screen, x, y)
			self.planet_physics_objs.append(p)

		self.buttons = [buttons.TextButton(screen, [screen.get_width() - 100, 50], 150, 80, (87, 201, 242), (18, 49, 227), 
									 3, "Arial", 20, "Go Back", (0, 0, 0))]
		
		self.button_ls = self.planet_physics_objs + self.buttons
		self.title = "SolarBody"

	def update_menu(self, events):
		"""
		This method will first draw the central mass (the sun) and then it will update and draw all of the SolarBody objects in turn.
		"""
		pygame.draw.circle(self.screen, (255, 0, 0), (400, 400), 20)

		for planet in self.planet_physics_objs:
			planet.move((400, 400))
			planet.draw()
		
		for button in self.buttons:
			button.update(events)
			button.draw()


class PointParticle:
	def __init__(self, screen, pos, size, x_offset, y_offset):
		self.screen = screen
		self.x = pos[0]
		self.y = pos[1]
		self.size = size
		self.x_offset = x_offset
		self.y_offset = y_offset
		self.colour = (255, 255, 0)
		self.speed = 0.01
		self.angle = 0
		self.GRAVITY = (0, 0.05)
		self.DRAG = 0.0001
		self.ELASTICITY = 0.8
		self.clicked = False
		self.text = "PointParticle"
	
	def draw(self):
		pygame.draw.circle(self.screen, self.colour, (int(self.x), int(self.y)), self.size)

	def add_vectors(self, vector1, vector2):
		x = math.sin(vector1[0]) * vector1[1] + math.sin(vector2[0]) * vector2[1]
		y = math.cos(vector1[0]) * vector1[1] + math.cos(vector2[0]) * vector2[1]
		mag = math.hypot(x, y)
		angle = (math.pi/2) - math.atan2(y, x)

		return angle, mag

	def move(self):
		self.angle, self.speed = self.add_vectors((self.angle, self.speed), self.GRAVITY)
		self.speed *= (1 - self.DRAG)
		self.x += (math.sin(self.angle) * self.speed)
		self.y += (math.cos(self.angle) * self.speed)

	def bounce(self):
		if self.x > self.screen.get_size()[0] - self.x_offset - self.size:
			self.x = 2*(self.screen.get_size()[0]-self.size) - self.x - 2*self.x_offset
			self.angle = -self.angle
			self.speed *= self.ELASTICITY
		elif self.x < self.size + self.x_offset:
			self.x = 2*self.size - self.x + 2*self.x_offset
			self.angle = -self.angle
			self.speed *= self.ELASTICITY

		if self.y > self.screen.get_size()[1] - self.size - 2*self.x_offset:
			self.y = 2*(self.screen.get_size()[1] - self.size) - self.y -2*self.x_offset - self.size
			self.angle = math.pi - self.angle
			self.speed *= self.ELASTICITY

		elif self.y < self.size + 2*self.y_offset:
			self.y = 2*self.size - self.y - 2*self.y_offset
			self.angle = math.pi - self.angle
			self.speed *= self.ELASTICITY

	def update(self):
		self.move()
		self.bounce()


class PointParticleSystem:
	def __init__(self, screen, particle_num=10, particle_size=10):
		self.screen = screen
		self.particle_objs = []
		self.x_offset = 6
		self.y_offset = 60

		for n in range(particle_num):
			x = randint(particle_size + self.x_offset, screen.get_width() - particle_size - self.x_offset)
			y = randint(particle_size + 2*self.y_offset + 2*self.x_offset, screen.get_height() - particle_size - 2*self.x_offset)

			particle = PointParticle(screen, (x, y), particle_size, self.x_offset + 2, self.y_offset + 2)
			particle.speed = random()
			particle.angle = uniform(0, math.pi*4)
		
			self.particle_objs.append(particle) 

		self.selected_particle = None
		self.buttons = [buttons.TextButton(screen, [screen.get_width() - 100, 50], 150, 80, 
										  (87, 201, 242), (18, 49, 227), 3, "Arial", 20, 
										  "Go Back", (0, 0, 0)),
						buttons.Button(screen, [screen.get_width() // 2, screen.get_height() // 2 + 50], 
										screen.get_width() - 2*self.x_offset, screen.get_height() - 2*self.y_offset, 
										(50, 50, 50), (250, 250, 250), 4, False)]
		self.button_ls = self.particle_objs + self.buttons

	def find_particle(self, mouse_x, mouse_y):
		for particle in self.particle_objs:
			if math.hypot(particle.x - mouse_x, particle.y - mouse_y) <= particle.size:
				self.selected_particle = particle

	def check_collide(self, particle1, particle2):
		dx = particle1.x - particle2.x
		dy = particle1.y - particle2.y

		dist = math.hypot(dx, dy)
		if dist < particle1.size + particle2.size:
			tangent = math.atan2(dy, dx)
			angle = 0.5 * math.pi + tangent

			angle1 = 2*tangent - particle1.angle
			angle2 = 2*tangent - particle2.angle
			speed1 = particle2.speed*particle1.ELASTICITY
			speed2 = particle1.speed*particle1.ELASTICITY

			particle1.angle, particle1.speed = angle1, speed1
			particle2.angle, particle2.speed = angle2, speed2

			angle = 0.5 * math.pi + tangent
			particle1.x += math.sin(angle)
			particle1.y -= math.cos(angle)
			particle2.x -= math.sin(angle)
			particle2.y += math.cos(angle)
	
	def update_buttons(self, events):
		for button in self.buttons:
			button.update(events)
			button.draw()

	def update_menu(self, events):
		self.update_buttons(events)
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				self.find_particle(mouse_x, mouse_y)

			elif event.type == pygame.MOUSEBUTTONUP:
				self.selected_particle = None

		for particle in self.particle_objs:
			if particle.colour == (0, 255, 0):
				particle.colour = (255, 255, 0)

		if self.selected_particle:
			self.selected_particle.colour = (0, 255, 0)
			mouse_x, mouse_y = pygame.mouse.get_pos()
			dx = mouse_x - self.selected_particle.x
			dy = mouse_y - self.selected_particle.y
			self.selected_particle.angle = math.atan2(dy, dx) + (math.pi/2)
			self.selected_particle.speed = math.hypot(dx, dy) * 0.005

		for i, particle in enumerate(self.particle_objs):
			particle.move()
			particle.bounce()

			for particle2 in self.particle_objs[i + 1:]:
				self.check_collide(particle, particle2)
				
			particle.draw()

