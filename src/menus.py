import pygame
import time
import buttons
import physics
import equationSolver
import dataBase
from typing import List
from tests import ImplementationError, UnkownUseCaseError

database = dataBase.DataBase()

# A defalt colour scheme I developed by picking colours that I thought looked similar to the ones in the design stage of the
# project. This is currently a prototype so I will need to consult my stakeholders about the current colour scheme.
DEFAULT_COLOUR_SCHEME = (
    (87, 201, 242), 
    (18, 49, 227), 
    (0, 0, 0),
    (252, 173, 3), 
    (252, 94, 3), 
    (62, 69, 201),
    (18, 49, 227)
)

# The 'MENU_TITLES' dictionary is a way of referencing the different types of menu titles such that if they change,
# I only need to change this dictionary instead of changing a string literal at multiple point throughout the code base.
MENU_TITLES = {
    "Main Menu": "A Level Physics Helper",
    "Login Menu": "Login Menu",
    "Sign Up Menu": "Create an Account",
    "Guest Menu": "Guest Mode",
    "Student Menu": "Student Mode",
    "Teacher Menu": "Teacher Mode",
    "Vis 1": "Visualisations Page 1",
    "Vis 2": "Visualisations Page 2",
    "Vis 3": "Visualisations Page 3",
    "Space Phys": "Space Physics",
    "Space System": "SolarBody",
    "Rigid Bodies": "Rigid Body Particles",
    "PointP": "PointParticle",
    "EqSol 1": "Equation Solver Page 1",
    "EqSol SUVAT": "General SUVAT Solver",
    # etc.
}

def handle_sign_up_clicked(current_menu, events, screen):
    menu_title = current_menu.button_ls[0].text
    if menu_title == MENU_TITLES["Main Menu"]:
        current_menu = SignUpMenu(screen, "Create an Account", [["Full Name", False], ["Password", True], 
                                  ["Password Again", True]], [["Class ID", "A", "B", "C", "D"], ["Year", "12", "13"]])
    elif menu_title == MENU_TITLES["Sign Up Menu"]:
        if dataBase.validate_sign_up(current_menu):
            password_hash = dataBase.generate_password_hash(current_menu.button_ls[2].text)
            names = current_menu.button_ls[1].text.split(" ")
            surname = names.pop()
            first_names = ""
            for name in names:
                first_names += f"{name} "
            first_names = first_names.strip()
            classID = current_menu.button_ls[4].text + current_menu.button_ls[5].text
            ID = dataBase.generate_next_id(database, "students")
            data = [ID, first_names, surname, classID, password_hash]
            database.add_data("students", data)
            current_menu = Menu(screen, "A Level Physics Helper", ["Login", "Sign Up", "Continue As Guest", "Quit"])
    else:
        raise UnkownUseCaseError("Sign Up")

    return current_menu

def handle_user_login(current_menu, screen, database):
    entered_userID = current_menu.button_ls[1].text
    entered_password_hash = dataBase.generate_password_hash(current_menu.button_ls[2].text)

    rows = database.read_all_data_from_table("students")

    userIDs = [row[0] for row in rows]
    if entered_userID in userIDs:
        id_index = userIDs.index(entered_userID)
        user_record = rows[id_index]
    else:
        raise Exception("User with given user ID not in database")

    if user_record[4] == entered_password_hash:
        current_menu = Menu(screen, f"Welcome back, {user_record[1]}!", ["Access Main Page", "Quit"])

    return current_menu

def handle_login_clicked(current_menu: object, events: List[str], screen: object):
    """
    This subroutine will check which menu screen is the 'current_menu' and depending on its result it will apply the suitable
    method of the 'Login' button. If the 'current_menu' isn't recognised as one of the predefined menus from the 'MENU_TITLES',
    then this subroutine will raise an implmentation error. For any other case this subroutine will raise an unkown use case error.
    """
    menu_title = current_menu.button_ls[0].text
    if menu_title == MENU_TITLES["Main Menu"]:
        current_menu = LoginMenu(screen, "Login Menu", [["User ID", False], ["Password", True]]) 
    elif menu_title == MENU_TITLES["Login Menu"]:
        current_menu = handle_user_login(current_menu, screen, database)
    else:
        raise UnkownUseCaseError("Login")
    
    return current_menu

def handle_go_back_clicked(current_menu, events, screen):
    """
    This subroutine will check which menu screen is the 'current_menu' and depending on its result it will apply the suitable
    method of the 'Go Back' button. If the 'current_menu' isn't recognised as one of the predefined menus from the 'MENU_TITLES',
    then this subroutine will raise an implmentation error. For any other case this subroutine will raise an unkown use case error.
    """
    menu_title = current_menu.button_ls[0].text
    if menu_title in [MENU_TITLES["Login Menu"], MENU_TITLES["Sign Up Menu"], MENU_TITLES["Guest Menu"]]:
        current_menu = Menu(screen, "A Level Physics Helper", ["Login", "Sign Up", "Continue As Guest", "Quit"])
    elif menu_title == MENU_TITLES["Vis 1"]:
        current_menu = Menu(screen, "Guest Mode", ["Visualisations", "Equation Solver", "Go Back", "Quit"])
    elif menu_title == MENU_TITLES["Vis 2"]:
        current_menu = Menu(screen, "Visualisations Page 1", ["Cloth Physics", "Rigid Bodies", "Next Page", "Go Back"])
    elif menu_title == MENU_TITLES["Vis 3"]:
        current_menu = Menu(screen, "Visualisations Page 2", ["Phase Change", "Fire Visualisation", "Next Page", "Go Back"])
    elif menu_title == MENU_TITLES["Space Phys"]:
        current_menu = Menu(screen, "Visualisations Page 3", ["Space Physics", "Go Back"])
    elif menu_title == MENU_TITLES["Space System"]:
        current_menu = Menu(screen, "Space Physics", ["Solar System", "N-Body", "Binary Stars", "Go Back"])
    elif menu_title == MENU_TITLES["Rigid Bodies"]:
        current_menu = Menu(screen, "Visualisations Page 1", ["Cloth Physics", "Rigid Bodies", "Next Page", "Go Back"])
    elif menu_title == MENU_TITLES["PointP"]:
        current_menu = Menu(screen, "Rigid Body Particles", ["Point Particles",  "Polygons", "Go Back"])
    elif menu_title == MENU_TITLES["EqSol 1"]:
        current_menu = Menu(screen, "Guest Mode", ["Visualisations", "Equation Solver", "Go Back", "Quit"])
    elif menu_title == MENU_TITLES["EqSol SUVAT"]:
        current_menu = Menu(screen, "Equation Solver Page 1", ["General SUVAT",  "Waves", "Next Page", "Go Back"])
    else:
        raise UnkownUseCaseError("Go Back", menu_title)
    
    return current_menu

def handle_next_page_clicked(current_menu, events, screen):
    """
    This subroutine will check which menu screen is the 'current_menu' and depending on its result it will apply the suitable
    method of the 'Next Page' button. If the 'current_menu' isn't recognised as one of the predefined menus from the 'MENU_TITLES',
    then this subroutine will raise an implmentation error. For any other case this subroutine will raise an unkown use case error.
    """
    menu_title = current_menu.button_ls[0].text
    if menu_title == MENU_TITLES["Vis 1"]:
        current_menu = Menu(screen, "Visualisations Page 2", ["Phase Change", "Fire Visualisation", "Next Page", "Go Back"])
    elif menu_title == MENU_TITLES["Vis 2"]:
        current_menu = Menu(screen, "Visualisations Page 3", ["Space Physics", "Go Back"])
    elif menu_title == MENU_TITLES["EqSol 1"]:
        current_menu = Menu(screen, "Equation Solver Page 2", ["Mechanics",  "Materials", "Next Page", "Go Back"])
    else:
        raise UnkownUseCaseError("Next Page", menu_title)

    return current_menu

def handle_quit(screen, events):
    """
    This subroutine sets the current menu to the ‘goodbye’ menu and then it will manually clear, draw to, and update the screen. 
    It does this so that the user can see the new menu screen. It will then wait 2 seconds so that the user has time to read the 
    text on the screen before the program closes (by calling 'pygame.quit' and 'quit').
    """
    current_menu = Menu(screen, "Goodbye", ["The program will close soon"], option_width=300)
    screen.fill((0,0,0))
    current_menu.update_menu(events)
    pygame.display.update()
    database.close_connection()
    quit()
    
def update_menu_system(current_menu, events, screen):
    """
    This is the function that handles all of the menus in the menu system. It is the way that all of the menus are 'linked together'.
    It will return the current menu that needs to be rendered.
    """
    current_menu.update_menu(events)
    for button in current_menu.button_ls:
        if button.clicked and str(type(button))[16:-2] == "TextButton": # and object type is text button
            if button.text == "Login":
                current_menu = handle_login_clicked(current_menu, events, screen)
            elif button.text == "Sign Up":
                current_menu = handle_sign_up_clicked(current_menu, events, screen)
            elif button.text == "Continue As Guest":
                current_menu = Menu(screen, "Guest Mode", ["Visualisations", "Equation Solver", "Go Back", "Quit"])
            elif button.text == "Access Main Page":
                current_menu = Menu(screen, "Logged In User Mode", ["Visualisations", "Equation Solver", "Log Out", "Quit"])
            elif button.text == "Log Out":
                current_menu = Menu(screen, "You have successfully been logged out", ["Return to Main Menu", "Quit"], 
                                    title_width=790, option_width=250)
            elif button.text == "Return to Main Menu":
                current_menu = Menu(screen, "A Level Physics Helper", ["Login", "Sign Up", "Continue As Guest", "Quit"])
            elif button.text == "Visualisations":
                current_menu = Menu(screen, "Visualisations Page 1", ["Cloth Physics", "Rigid Bodies", "Next Page", "Go Back"])
            elif button.text == "Equation Solver":
                current_menu = Menu(screen, "Equation Solver Page 1", ["General SUVAT", "Any Other", "Next Page", "Go Back"])
            elif button.text == "General SUVAT":
                current_menu = equationSolver.GeneralSUVATSolver(screen, "General SUVAT Solver", ["S", "U", "V", "A", "T"], title_width=500)
            elif button.text == "Any Other":
                current_menu = equationSolver.EquationSolver(screen, "'Any Other' Equations Solver", 10 * [""], title_width=500)
            elif button.text == "Solve":
                current_menu.solve()
            elif button.text == "View In Plain Text":
                current_menu.show_plain_text = not current_menu.show_plain_text
                button.clicked = False
                print("Swapped")
            elif button.text == "Waves":
                current_menu = equationSolver.EquationSolver(screen, "Waves Test", ["c", "f", "λ"])
            elif button.text == "Go Back":
                current_menu = handle_go_back_clicked(current_menu, events, screen)
            elif button.text == "Next Page":
                current_menu = handle_next_page_clicked(current_menu, events, screen)
            elif button.text == "Quit":
                current_menu = handle_quit(screen, events)
            elif button.text == "Space Physics":
                current_menu = Menu(screen, "Space Physics", ["Solar System", "N-Body", "Binary Stars", "Go Back"])
            elif button.text == "Solar System":
                current_menu = physics.SolarSystem(screen)
            elif button.text == "Rigid Bodies":
                current_menu = Menu(screen, "Rigid Body Particles", ["Point Particles",  "Polygons", "Go Back"])
            elif button.text == "Point Particles":
                current_menu = physics.PointParticleSystem(screen, 150)
            elif button.text == "Phase Change":
                pass
                # current_menu = physics.PhaseChangeSystem(screen)
        elif str(type(button))[16:-2] in ["HorizontalSliderButton", "VerticalSliderButton"]:
            # button_value = -1 * (button.neutral_position - button.centre_pos[0])
            # button_value =  -1 * ((button.neutral_position - button.centre_pos[0]) / (2/3 * button.limit))
            button_value = button.value
            print("limit", button.limit, "value", button_value)

    return current_menu

class Menu:
    """
    This is the base menu class. It will be used to create 'selection' menus where there is a title for the menu and many options
    that the user can choose from.
    """
    def __init__(self: object, screen: object, title: str, options: List[str], colour_scheme=DEFAULT_COLOUR_SCHEME, border_width=3, 
                 title_width=500, title_height=100, title_font="Arial", title_size=40, option_width=200, option_height=80, 
                 option_font="Arial", option_size=20) -> object:
        """
        screen: pygame screen object
            - used as the pygame surface that all of the buttons will be drawn to.
        title: str
            - the title of the menu page.
        options: List[str]
            - a list of all of that options that the user can select.
            - each option will be its own button.
            - the order of the options in the list will correspond to their order in the menu (i.e. the first option will be the 
              heighest up and the last option will be the lowest down on the menu page).
        colour_scheme: Tuple[Tuple[int, int, int]] [DEFAULT_COLOUR_SCHEME]
            - The colours for the different components of the buttons and title in the menu page.
            - order of items:
                0. title_bg_colour      - the colour of the title's background, this is the main part of the title.
                1. title_border_colour  - the colour of the title's border, this is outline of the title.
                2. title_text_colour    - the colour of the title's text.
                3. option_bg_colour     - the colour of the options' background, this is the main part of the option buttons.
                4. option_border_colour - the colour of the options' border, this is outline of the option buttons.
                5. option_text_colour   - the colour of the options' text.
        border_width: int [3]
            - the width of the borders for both the title and the button options.
            - an integer for the number of pixels.
        title_width: int [500]
            - the width of the box containing the title.
            - an integer for the number of pixels.
        title_height: int [100]
            - the height of the box containing the title.
            - an integer for the number of pixels.
        title_font: str ["Arial"]
            - the font style for the title's text on the menu page.
        title_size: int [40]
            - the font size of the text in the title.
        option_width: int [200]
            - the width of the option buttons.
            - an integer for the number of pixels.
        option_height: int [80]
            - the height of the option buttons.
            - an integer for the number of pixels.
        option_font: str ["Arial"]
            - the font style for the button option's text on the menu page.
        option_size: int [20]
            - the font size of the text in the option buttons.
        """
        self.centre_x = screen.get_width() // 2
        # Decomposing the 'colour_scheme' list into the its colour values.
        title_bg_col, title_border_col, title_text_col, option_bg_col, option_border_col, option_text_col = colour_scheme[:6]
        # Creating the title button (which is not interactive) as a single object in a list to help create the button list.
        title_button = [buttons.TextButton(screen, [self.centre_x, 100], title_width, title_height, title_bg_col, title_border_col, 
                                           border_width, title_font, title_size, title, title_text_col, False)]
        # Creating a list of all the option buttons.
        option_buttons = [buttons.TextButton(screen, [self.centre_x, 100 + (i + 1) * 120], option_width, option_height, option_bg_col,
                                            option_border_col, border_width, option_font, option_size, options[i], option_text_col)
                          for i in range(len(options))]
        # Creating the button list attribute which contains all interactive and non-interactive buttons.
        self.button_ls = title_button + option_buttons

    def update_menu(self: object, events: List[str]) -> None:
        """
        Updates all of the buttons in the button list by calling their respective 'update' and 'draw' methods.
        """
        for button in self.button_ls:
            button.update(events)
            button.draw()


class LoginMenu(Menu):
    """
    The 'LoginMenu' class consists of a title for the menu page as well as a number of text input fields.
    """
    def __init__(self: object, screen: object, title: str, fields: List[str], colour_scheme=DEFAULT_COLOUR_SCHEME, border_width=3, 
                 title_width=500, title_height=100, title_font="Arial", title_size=40, field_width=200, field_height=80, 
                 field_font="Arial", field_size=20) -> object:
        """
        screen: pygame screen object
            - used as the pygame surface that all of the buttons will be drawn to.
        title: str
            - the title of the menu page.
        fields: List[str]
            - a list of all of that fields that the user has to complete.
            - each option will be its own button.
            - the order of the fields in the list will correspond to their order in the menu (i.e. the first field will be the 
              heighest up and the last field will be the lowest down on the menu page).
        colour_scheme: Tuple[Tuple[int, int, int]] [DEFAULT_COLOUR_SCHEME]
            - The colours for the different components of the buttons and title in the menu page.
            - order of items:
                0. title_bg_colour      - the colour of the title's background, this is the main part of the title.
                1. title_border_colour  - the colour of the title's border, this is outline of the title.
                2. title_text_colour    - the colour of the title's text.
                3. option_bg_colour     - the colour of the options' background, this is the main part of the option buttons.
                4. option_border_colour - the colour of the options' border, this is outline of the option buttons.
                5. option_text_colour   - the colour of the options' text.
        border_width: int [3]
            - the width of the borders for both the title and the button options.
            - an integer for the number of pixels.
        title_width: int [500]
            - the width of the box containing the title.
            - an integer for the number of pixels.
        title_height: int [100]
            - the height of the box containing the title.
            - an integer for the number of pixels.
        title_font: str ["Arial"]
            - the font style for the title's text on the menu page.
        title_size: int [40]
            - the font size of the text in the title.
        field_width: int [200]
            - the width of the fields.
            - an integer for the number of pixels.
        field_height: int [80]
            - the height of the fields.
            - an integer for the number of pixels.
        field_font: str ["Arial"]
            - the font style for the fields' text on the menu page.
        field_size: int [20]
            - the font size of the text in the fields.
        """
        super().__init__(screen, title, []) 

        field_bg_col, unselected_field_border_col, field_text_col, selected_field_border_col = colour_scheme[-4:]
        field_names = [field[0] for i, field in enumerate(fields)]
        is_hidden = [field[1] for i, field in enumerate(fields)]
        
        fields_ls = [buttons.TextInputBox(screen, [self.centre_x, 100 + (i + 1) * 120], field_width, field_height, field_bg_col,
                                          unselected_field_border_col, selected_field_border_col, border_width, field_font, 
                                          field_size, field_names[i], field_text_col, is_hidden[i])
                          for i in range(len(field_names))]

        login_button = [buttons.TextButton(screen, [self.centre_x, screen.get_height() - field_height - 120], field_width - 30,
                                           field_height - 10, field_bg_col, unselected_field_border_col, border_width, field_font, field_size, 
                                           "Login", field_text_col)]

        # Creating the 'Go Back' button.
        back_button = [buttons.TextButton(screen, [self.centre_x, screen.get_height() - 100], field_width - 30, field_height - 10, 
                                          field_bg_col, unselected_field_border_col, border_width, field_font, field_size, 
                                          "Go Back", field_text_col)]
        
        self.button_ls += fields_ls + login_button + back_button


class SignUpMenu(Menu):
    """
    The 'SignUpMenu' class consists of a title for the menu page as well as a number of text input fields and drop down select data entry fields.
    """
    def __init__(self: object, screen: object, title: str, text_input_fields: List[str], multi_select_fields: List[List[str]],
                 colour_scheme=DEFAULT_COLOUR_SCHEME, border_width=3, gap=3, title_width=500, title_height=100, title_font="Arial", 
                 title_size=40, field_width=200, field_height=80, field_font="Arial", field_size=20) -> object:
        """
        screen: pygame screen object
            - used as the pygame surface that all of the buttons will be drawn to.
        title: str
            - the title of the menu page.
        fields: List[str]
            - a list of all of that fields that the user has to complete.
            - each option will be its own button.
            - the order of the fields in the list will correspond to their order in the menu (i.e. the first field will be the 
              heighest up and the last field will be the lowest down on the menu page).
        colour_scheme: Tuple[Tuple[int, int, int]] [DEFAULT_COLOUR_SCHEME]
            - The colours for the different components of the buttons and title in the menu page.
            - order of items:
                0. title_bg_colour      - the colour of the title's background, this is the main part of the title.
                1. title_border_colour  - the colour of the title's border, this is outline of the title.
                2. title_text_colour    - the colour of the title's text.
                3. option_bg_colour     - the colour of the options' background, this is the main part of the option buttons.
                4. option_border_colour - the colour of the options' border, this is outline of the option buttons.
                5. option_text_colour   - the colour of the options' text.
        border_width: int [3]
            - the width of the borders for both the title and the button options.
            - an integer for the number of pixels.
        title_width: int [500]
            - the width of the box containing the title.
            - an integer for the number of pixels.
        title_height: int [100]
            - the height of the box containing the title.
            - an integer for the number of pixels.
        title_font: str ["Arial"]
            - the font style for the title's text on the menu page.
        title_size: int [40]
            - the font size of the text in the title.
        field_width: int [200]
            - the width of the fields.
            - an integer for the number of pixels.
        field_height: int [80]
            - the height of the fields.
            - an integer for the number of pixels.
        field_font: str ["Arial"]
            - the font style for the fields' text on the menu page.
        field_size: int [20]
            - the font size of the text in the fields.
        """
        super().__init__(screen, title, []) 

        field_bg_col, unselected_field_border_col, field_text_col, selected_field_border_col = colour_scheme[-4:]
        field_names = [field[0] for i, field in enumerate(text_input_fields)]
        is_hidden = [field[1] for i, field in enumerate(text_input_fields)]

        text_input_fields_ls = [buttons.TextInputBox(screen, [self.centre_x + (self.centre_x // 2.5), 100 + (i + 1) * 120], 
                                                     field_width, field_height, field_bg_col, unselected_field_border_col, 
                                                     selected_field_border_col, border_width, field_font, field_size, 
                                                     field_names[i], field_text_col, is_hidden[i])
                                for i in range(len(field_names))]

        multi_select_fields_ls = [buttons.DropDownSelectButton(screen, [self.centre_x - (self.centre_x // 2.5), 100 + (i + 1) * 120],
                                                               field_width, field_height, field_bg_col, unselected_field_border_col,
                                                               selected_field_border_col, border_width, field_font, field_size, 
                                                               multi_select_fields[i], field_text_col, gap)
                                  for i in range(len(multi_select_fields))]
        
        login_button = [buttons.TextButton(screen, [self.centre_x + (self.centre_x // 2.5), screen.get_height() - field_height - 15], field_width - 30,
                                           field_height - 10, field_bg_col, unselected_field_border_col, border_width, field_font, 
                                           field_size, "Sign Up", field_text_col)]

        # Creating the 'Go Back' button.
        back_button = [buttons.TextButton(screen, [self.centre_x - (self.centre_x // 2.5), screen.get_height() - field_height - 15], field_width - 30, 
                                          field_height - 10, field_bg_col, unselected_field_border_col, border_width, field_font, field_size, 
                                          "Go Back", field_text_col)]

        self.button_ls += text_input_fields_ls + login_button + back_button + multi_select_fields_ls[::-1]
        

