# Imports modules
import pygame
import menus
import equationSolver
import tests

def main():

    # Useful constants
    WIDTH = 800
    HEIGHT = 650
    SIZE = (WIDTH, HEIGHT)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # pygame initialisation
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()

    menu = menus.Menu(screen, "A Level Physics Helper", ["Login", "Sign Up", "Continue As Guest", "Quit"])
    # menu = equationSolver.EquationSolver(screen, "test", ["w", "x", "y", "z"])
    
    # Main loop
    while True:

        events = pygame.event.get()

        # Checks for the users closing the program using their OS's window manager.
        for event in events:
            if event.type == pygame.QUIT:
                menus.handle_quit(screen, events)

        # Updates the menu, this function will either return the menu object passed or a new menu object.
        menu = menus.update_menu_system(menu, events, screen)

        # Updates the screen so that all items drawn can be seen by user.
        pygame.display.update()
        # Clears the screen by filling it with black so that the screen is ready to have new items drawn to it.
        screen.fill(BLACK)

# Run the main function if this is the main file.
if __name__ == "__main__":
    main()
