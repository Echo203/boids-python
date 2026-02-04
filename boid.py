import pygame
from math import sqrt, pow, atan2, degrees
import random

from const import (
    ALIGNMENT_FACTOR,
    SEPARATION_FACTOR,
    COHESION_FACTOR,
    BOID_ANGULAR_VELOCITY,
    BOID_ANGULAR_DUMP,
    BOID_STEER_FORCE,
    BOID_MAX_SPEED,
    BOID_MIN_SPEED,
    BOID_MAX_TURN_SPEED,
    BOID_FOV,
    BOID_ACC_RATE,
    BOID_SLOW_RATE,
    BOID_SEPARATION_DISTANCE,
    NEIGHBOUR_RANGE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)

from helpers import calc_angle_diff, calc_distance_two_boids, normalize


class Boid(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, rotation=0):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.radius = radius
        self.rotation = rotation

        self.angular_velocity = BOID_ANGULAR_VELOCITY

        self.target_rotation = rotation

        self.current_speed = random.randint(BOID_MIN_SPEED, BOID_MAX_SPEED)
        self.target_speed = self.current_speed

        self.state = {"separation": False, "alignment": False, "cohesion": False}

        self.separation_vector = pygame.Vector2(0, 0)
        self.alignment_vector = pygame.Vector2(0, 0)
        self.cohesion_vector = pygame.Vector2(0, 0)

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
        # keys = pygame.key.get_pressed()

        if self.target_speed > self.current_speed:
            self.speed_up()
        elif self.target_speed < self.current_speed:
            self.slow_down()

        if not (self.state["separation"]):
            self.separation_vector = pygame.Vector2(0, 0)
        if not (self.state["alignment"]):
            self.alignment_vector = pygame.Vector2(0, 0)
            self.cohesion_vector = pygame.Vector2(0, 0)

        steering = (
            normalize(self.separation_vector) * SEPARATION_FACTOR
            + normalize(self.alignment_vector) * ALIGNMENT_FACTOR
            + normalize(self.cohesion_vector) * COHESION_FACTOR
        )
        # if steering[0] != 0 and steering[1] != 0:
        #     print(f"steering: {steering}")
        # if self.state["separation"] or self.state["alignment"]:
        #     print(
        #         f"Separating: {self.state['separation']}\nAlign and cohes: {self.state['alignment']}"
        #     )
        #     print(f"desired_angle: {steering.as_polar()[1]}")
        #     print(f"self.rotation: {self.rotation}")
        #     print(f"diff: {calc_angle_diff(self.rotation, steering.as_polar()[1])}")

        if steering.length_squared() > 0.0001:
            desired_angle = steering.as_polar()[1]

            diff = calc_angle_diff(self.rotation, desired_angle)

            if abs(diff) > 1.0:
                # print(f"steering.as_polar(): {steering.as_polar()}")
                # print(f"self.angular_velocity: {self.angular_velocity}")
                self.turn_towards_angle(desired_angle, dt)
        self.move(dt)

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

    def turn_towards_angle(self, angle, dt):
        self.angular_velocity += angle * BOID_STEER_FORCE * dt
        self.angular_velocity *= BOID_ANGULAR_DUMP
        # print(
        #     f"Current rotation: {self.rotation}\nSteering towards: {angle}\nUpdated Rotation: {self.rotation + self.angular_velocity * dt}"
        # )
        self.rotation += self.angular_velocity * dt

    # Euclidian distance for self and boid to check with
    def is_too_close_to(self, other):
        # Check distance
        distance = sqrt(
            pow(self.position[0] - other.position[0], 2)
            + pow(self.position[1] - other.position[1], 2)
        )

        # Check if in front
        forward_vector = pygame.Vector2(0, 1).rotate(self.rotation)
        to_other = other.position - self.position
        dist = to_other.length()
        if dist > 0:
            to_other_norm = to_other / dist
        # This takes a vector and creates relative position according to rotation
        # From 1.0 <- Exacly in front
        # To -1.0 <- Exacly behind
        how_ahead = forward_vector.dot(to_other_norm)

        # print(f"how_ahead: {how_ahead}")
        if distance < BOID_SEPARATION_DISTANCE and how_ahead > BOID_FOV:
            return True
        return False

    def steer_away(self, list_of_boids, dt):
        smallest_distance = BOID_SEPARATION_DISTANCE
        closes_boid = list_of_boids[0]

        for boid in list_of_boids:
            dist = calc_distance_two_boids(self, boid)
            if dist < smallest_distance:
                smallest_distance = dist
                closes_boid = boid
            # print(dist)
        self.separation_vector = pygame.Vector2(
            closes_boid.position[0], closes_boid.position[1]
        )

    def is_in_visible_range(self, other):
        distance = sqrt(
            pow(self.position[0] - other.position[0], 2)
            + pow(self.position[1] - other.position[1], 2)
        )
        forward_vector = pygame.Vector2(0, 1).rotate(self.rotation)
        to_other = other.position - self.position
        dist = to_other.length()
        if dist > 0:
            to_other_norm = to_other / dist

        how_ahead = forward_vector.dot(to_other_norm)

        if distance > NEIGHBOUR_RANGE and how_ahead > BOID_FOV:
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
        alignment_vector_avg = pygame.Vector2(0, 0)
        for neighbour in neighbours:
            speed_avg += neighbour.current_speed
            neighbour_direction = pygame.Vector2(0, 1).rotate(neighbour.rotation)
            alignment_vector_avg += neighbour_direction

        speed_avg = speed_avg / len(neighbours)
        self.target_speed = speed_avg

        if alignment_vector_avg.length_squared() > 0:
            alignment_vector_avg.normalize()

        alignment_vector_avg = alignment_vector_avg / len(neighbours)

        self.alignment_vector = alignment_vector_avg
        # self.turn_towards_angle(diff, dt)

    def cohesion(self, neighbours, dt):
        x_avg = 0
        y_avg = 0
        for neighbour in neighbours:
            x_avg += neighbour.position[0]
            y_avg += neighbour.position[1]

        x_avg = x_avg / len(neighbours)
        y_avg = y_avg / len(neighbours)

        target_angle = degrees(atan2(y_avg, x_avg))

        diff = calc_angle_diff(target_angle, self.rotation)

        self.cohesion_vector = pygame.Vector2(x_avg, y_avg)
        # self.turn_towards_angle(diff, dt)

    def switch_separation_to(self, is_separating):
        self.state["separation"] = is_separating

    def switch_align_and_cohes_to(self, is_aligning):
        self.state["alignment"] = is_aligning
        self.state["cohesion"] = is_aligning
