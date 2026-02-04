import pygame
from math import sqrt, pow, atan2, degrees
import random

from const import (
    ALIGNMENT_FACTOR,
    BOID_MAX_SPEED,
    BOID_MIN_SPEED,
    BOID_MAX_TURN_SPEED,
    BOID_ACC_RATE,
    BOID_SLOW_RATE,
    BOID_SEPARATION_DISTANCE,
    NEIGHBOUR_RANGE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
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

        self.angular_velocity = 0.0

        self.target_rotation = rotation

        self.current_speed = random.randint(BOID_MIN_SPEED, BOID_MAX_SPEED)
        self.target_speed = self.current_speed

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

        if self.target_speed > self.current_speed:
            self.speed_up()
        elif self.target_speed < self.current_speed:
            self.slow_down()

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
        self.rotation += BOID_MAX_TURN_SPEED * dt

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * self.current_speed * dt
        self.position += rotated_with_speed_vector

    def speed_up(self):
        if self.current_speed < BOID_MAX_SPEED:
            self.current_speed *= 1 + BOID_ACC_RATE

    def slow_down(self):
        if self.current_speed > BOID_MIN_SPEED:
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

    def steer_away(self, list_of_boids, dt):
        avg_dx = 0
        avg_dy = 0
        for boid in list_of_boids:
            avg_dx = boid.position[0] - self.position[0]
            avg_dy = boid.position[1] - self.position[1]

        # math.atan2 returns radians, convert to degrees
        target_angle = degrees(atan2(avg_dy, avg_dx))

        # 2. Calculate the shortest turn (-180 to 180)
        diff = (target_angle - self.rotation + 180) % 360 - 180

        angle_difference = max(
            -BOID_MAX_TURN_SPEED * dt, min(BOID_MAX_TURN_SPEED * dt, diff)
        )

        # Add the diffrence between vectors to target rotation times ratio
        self.rotation += angle_difference

    def is_in_visible_range(self, other):
        distance = sqrt(
            pow(self.position[0] - other.position[0], 2)
            + pow(self.position[1] - other.position[1], 2)
        )
        if distance > NEIGHBOUR_RANGE:
            return False
        return True

    def align(self, neighbours, dt):
        # Get avrage velocity of all neighbours
        # xv_avg = 0
        # yv_avg = 0

        # for neighbour in neighbours:
        #     xv_avg += neighbour.velocity[0]
        #     yv_avg += neighbour.velocity[1]

        # xv_avg /= len(neighbours)
        # yv_avg /= len(neighbours)

        speed_avg = 0
        rot_avg = 0
        for neighbour in neighbours:
            speed_avg += neighbour.current_speed
            rot_avg += neighbour.rotation

        speed_avg = speed_avg / len(neighbours)
        self.target_speed = speed_avg

        rot_avg = rot_avg / len(neighbours)
        diff = (rot_avg - self.rotation + 180) % 360 - 180
        angle_difference = max(
            -BOID_MAX_TURN_SPEED * dt, min(BOID_MAX_TURN_SPEED * dt, diff)
        )

        self.rotation += angle_difference

    def cohesion(self, neighbours, dt):
        x_avg = 0
        y_avg = 0
        for neighbour in neighbours:
            x_avg += neighbour.position[0]
            y_avg += neighbour.position[1]

        x_avg = x_avg / len(neighbours)
        y_avg = y_avg / len(neighbours)

        target_angle = degrees(atan2(y_avg, x_avg))

        diff = (target_angle - self.rotation + 180) % 360 - 180

        angle_difference = max(
            -BOID_MAX_TURN_SPEED * dt, min(BOID_MAX_TURN_SPEED * dt, diff)
        )

        self.rotation += angle_difference

    def check_margins(self, margin, dt):
        steer_direction = pygame.Vector2(0, 0)

        if self.position.x < margin:
            steer_direction.x += 1  # Push Right
        elif self.position.x > SCREEN_WIDTH - margin:
            steer_direction.x -= 1  # Push Left

        if self.position.y < margin:
            steer_direction.y += 1  # Push Down
        elif self.position.y > SCREEN_HEIGHT - margin:
            steer_direction.y -= 1  # Push Up

        # 2. If we aren't near a margin, do nothing
        if steer_direction.length() == 0:
            return

        # 3. Calculate the target angle based on your move() vector (0, 1)
        # This finds the angle between 'Down' and our desired push direction
        target_angle = pygame.Vector2(0, 1).angle_to(steer_direction)

        diff = (target_angle - self.rotation + 180) % 360 - 180

        angle_difference = max(
            -BOID_MAX_TURN_SPEED * dt, min(BOID_MAX_TURN_SPEED * dt, diff)
        )
        self.rotation += angle_difference
