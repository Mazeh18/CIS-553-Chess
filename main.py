import pygame

from src.constants import WINDOW_TITLE, FPS
from src.controllers.screen_navigation_controller import ScreenNavigationController


def main() -> None:
    pygame.init()

    surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption(WINDOW_TITLE)

    clock = pygame.time.Clock()
    nav_controller = ScreenNavigationController(surface)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                continue

            if nav_controller.current_screen:
                nav_controller.current_screen.handle_event(event)

        if nav_controller.current_screen:
            nav_controller.current_screen.update(dt)

        if nav_controller.current_screen:
            nav_controller.current_screen.draw()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
