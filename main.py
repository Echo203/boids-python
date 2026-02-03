import pygame
import sys

from boid import Boid
from const import SCREEN_HEIGHT, SCREEN_WIDTH, AMMOUNT_OF_BOIDS


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
    one_boid = Boid(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 10, 0)

    # boirds_array = []
    # for i in range(AMMOUNT_OF_BOIDS):
    #     boirds_array.append(
    #         Boid((SCREEN_WIDTH / 2) + i * 5, (SCREEN_HEIGHT / 2) + i * 5, 10)
    #     )

    while True:
        # Exit on close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Background
        screen.fill("black")

        updatable.update(dt)

        # Looping boids against boids to calculate avrages
        # for boids_i in boids:

        # for drawed in drawable:
        #     drawed.draw(screen)

        # FPS settings
        pygame.display.flip()
        dt = clock.tick(144) / 1000


if __name__ == "__main__":
    main()
