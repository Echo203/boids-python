import pygame

from const import BOID_SPEED, BOID_TURN_SPEED


class Boid(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, rotation):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.rotation = rotation

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(
            screen,
            "white",
            self.triangle(),
            1,
        )

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.move(dt)

        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_s]:
            self.move(-dt)

    def rotate(self, dt):
        self.rotation += BOID_TURN_SPEED * dt

    def move(self, dt, intensity):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * (BOID_SPEED * intensity) * dt
        self.position += rotated_with_speed_vector
