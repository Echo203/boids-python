import pygame
import random
import sys

from boid import Boid
from const import SCREEN_HEIGHT, SCREEN_WIDTH, AMMOUNT_OF_BOIDS, BOID_RADIUS


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Initializers
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    # Groups (to call selected type of sprites)
    boids = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    updatable = pygame.sprite.Group()

    # Containers for sprites
    Boid.containers = (boids, drawable, updatable)

    # Initial drawings (middle of the screen, radius of triangle = 10)
    one_boid = Boid((SCREEN_WIDTH + 300) / 2, SCREEN_HEIGHT / 2, BOID_RADIUS, 90)
    two_boid = Boid(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2, BOID_RADIUS, 270)

    boids_array = []
    for i in range(AMMOUNT_OF_BOIDS):
        boids_array.append(
            # Spawn boid, random position (x,y), radius from settings, random rotation
            Boid(
                random.randint(BOID_RADIUS, SCREEN_WIDTH - BOID_RADIUS),
                random.randint(BOID_RADIUS, SCREEN_HEIGHT - BOID_RADIUS),
                BOID_RADIUS,
                random.randint(0, 359),
            )
        )

    while True:
        # Exit on close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Background
        screen.fill("black")

        updatable.update(dt)

        # Looping boids against boids to calculate avrages
        for boid_i in boids:
            for boid_j in boids:
                if boid_i == boid_j:
                    continue
                if boid_i.is_too_close_to(boid_j):
                    boid_i.steer_away(boid_j, dt)

        for drawed in drawable:
            drawed.draw(screen)

        # FPS settings
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
