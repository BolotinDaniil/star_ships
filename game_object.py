from math import sin, cos, pi

import numpy as np

from settings_storage import settings


class GameObject:
    def __init__(self, pygame, surface, radius, angle, mass, position, color):
        self.pygame = pygame
        self.surface = surface

        self.radius = radius
        self.angle = angle
        self.mass = mass

        self.direction = np.array((cos(self.angle), -sin(self.angle)))

        self.previous_position = np.array(position)
        self.position = np.array(position)
        self.x, self.y = 0, 0
        self.acceleration = np.array((0., 0.))
        self.inst_velocity = np.array((0., 0.))
        self.total_force = np.array((0., 0.))

        self.color = color

    def add_forces(self, *forces):
        # Добавляем силы, действующие на объект
        self.total_force += sum(forces)

    def update(self, dt):
        # Verlet:                   p_i+1 = p_i + p_i - p_(i-1) + a * dt * dt
        # Time Corrected Verlet:    p_i+1 = p_i + (p_i - p_(i-1)) * (dt / prev_dt) + a * dt * dt

        self.direction = np.array((cos(self.angle), -sin(self.angle)))

        self.acceleration = self.total_force / self.mass

        t = self.position
        self.position = 2 * self.position - self.previous_position + self.acceleration * dt ** 2
        self.previous_position = t

        self.inst_velocity = (self.position - self.previous_position)
        self.x, self.y = (int(round(p * settings.SCALE)) for p in self.previous_position)

    def reset_forces(self):
        # Important to reset self.total_force
        self.total_force = np.array((0., 0.))

    def render(self, width=1):
        self.pygame.draw.circle(self.surface, self.color, (self.x, self.y), self.radius, width)

    def render_debug(self):
        # Velocity vector
        vx, vy = (int(v * settings.SCALE * settings.FPS) for v in self.inst_velocity)
        self.pygame.draw.line(self.surface, settings.green, (self.x, self.y), (self.x + vx, self.y + vy))

        # Total Force vector
        #max_force = 10**4
        #fx, fy = (int(f * settings.SCALE / max_force) for f in self.total_force)
        #self.pygame.draw.line(self.surface, settings.yellow, (self.x, self.y), (self.x + fx, self.y + fy))
