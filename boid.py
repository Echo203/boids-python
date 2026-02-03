import pygame
from math import sqrt, pow, atan2, degrees

from const import (
    BOID_MAX_SPEED,
    BOID_TURN_SPEED,
    BOID_ACC_RATE,
    BOID_SLOW_RATE,
    BOID_SEPARATION_DISTANCE,
)


class Boid(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, rotation=0):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.rotation = rotation

        self.target_rotation = rotation
        self.target_velocity = 0

        self.current_speed = BOID_MAX_SPEED / 2

    # Drawing dynamic triangle based on position and rotation
    # So that we now where the triangle is pointing
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
            self.steer_left(dt)

        if keys[pygame.K_d]:
            self.steer_right(dt)

        if keys[pygame.K_w]:
            self.speed_up()

        if keys[pygame.K_s]:
            self.slow_down()

    def rotate(self, dt):
        self.rotation += BOID_TURN_SPEED * dt

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * self.current_speed * dt
        self.position += rotated_with_speed_vector

    def speed_up(self):
        if self.current_speed < BOID_MAX_SPEED:
            self.current_speed *= 1 + BOID_ACC_RATE

    def slow_down(self):
        self.current_speed *= 1 - BOID_SLOW_RATE

    def steer_right(self, dt):
        self.rotate(dt)

    def steer_left(self, dt):
        self.rotate(-dt)

    # Euclidian distance for self and boid to check with
    def is_too_close_to(self, other):
        distance = sqrt(
            pow(self.position[0] - other.position[0], 2)
            + pow(self.position[1] - other.position[1], 2)
        )
        if distance < BOID_SEPARATION_DISTANCE:
            return True
        return False

    def steer_away(self, other, dt):
        dx = other.position[0] - self.position[0]
        dy = other.position[1] - self.position[1]

        # math.atan2 returns radians; convert to degrees
        # We negate dy because Pygame's Y-axis increases downwards
        target_angle = degrees(atan2(-dy, dx))

        # 2. Calculate the shortest turn (-180 to 180)
        diff = (target_angle - self.rotation + 180) % 360 - 180

        # 3. Decide turn direction
        # If diff > 0, the target is to your LEFT. To steer AWAY, turn RIGHT.
        # If diff < 0, the target is to your RIGHT. To steer AWAY, turn LEFT.
        if diff > 0:
            self.steer_right(dt)  # Rotate Clockwise
        elif diff < 0:
            self.steer_left(dt)  # Rotate Counter-Clockwise

        print(self.rotation % 360)  # Keep rotation within 0-360
