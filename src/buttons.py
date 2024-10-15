import pygame
import time
from typing import List, Tuple

class Button:
    """
    This is the base button class. It will be used as a parent class for all of the other button classes.
    """
    def __init__(self: object, screen: object, centre: Tuple[int, int], width: int, height: int, 
                 bg_colour: Tuple[int, int, int], border_colour: Tuple[int, int, int], border_width: int, 
                 interactive=True) -> object:
        """
        screen: pygame screen object
            - used as the pygame surface that all parts of the button is drawn to.
        centre: List[int, int]
            - is used for the centre of the button.
            - pygame draws rectangle objects with a 'start xy' and 'end xy', so the 'centre' is converted.
        width: int
            - the width of the button.
            - measured in number of pixels.
        height: int
            - the height of the button.
            - measured in number of pixels.
        bg_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's background, this is the main part of the button.
        border_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's border, this is the outline of the button.
        border_width: int
            - this is width of the border.
            - recommened values between 0 and 10.
            - measured in number of pixels.
        interactive: bool [True]
            - default value is True.
            - if False, then the button will not get updated at all during the program's runtime.
        """
        self.surface = screen
        self.centre_pos = centre
        self.width = width
        self.height = height
        self.start_xy = (centre[0] - width//2, centre[1] - height//2)
        self.end_xy = (centre[0] + width//2, centre[1] + height//2)
        self.initial_bg_colour = bg_colour
        self.bg_colour = bg_colour
        self.border_colour = border_colour
        self.border_width = border_width
        self.pygame_button_object = pygame.Rect(self.start_xy[0], self.start_xy[1], self.width, self.height)
        self.interactive = interactive
        self.current_events = []
        self.clicked = False

    def draw(self: object) -> None:
        """
        Uses the pygame button object created in the constructor.
        Draws the button as a filled rectangle with the colour of the self.bg_colour.
        Draws the border as a rectangular border with width self.border_width and colour self.border_colour'.
        """
        pygame.draw.rect(self.surface, self.bg_colour, self.pygame_button_object)
        pygame.draw.rect(self.surface, self.border_colour, self.pygame_button_object, self.border_width)

    def check_mouse_hover(self: object) -> bool:
        """
        Finds the coordinates of the mouse and then uses the pygame rect method collidepoint().
        """
        mouse_xy = pygame.mouse.get_pos()
        
        if self.pygame_button_object.collidepoint(mouse_xy):
            return True
        else:
            return False
    
    def check_mouse_click(self: object) -> bool:
        """
        Checks the pygame event queue for a mousebuttondown event
        """
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
        return False

    def apply_mouse_hover(self: object) -> None:
        """
        This is here to test it works.
        """
        self.bg_colour = (255, 255, 255)

    def apply_mouse_click(self: object) -> None:
        """
        Will set the 'clicked' attribute to True.
        """
        self.clicked = True

    def reset_button(self: object) -> None:
        self.bg_colour = self.initial_bg_colour

    def apply_mouse_click_or_hover(self: object) -> None:
        """
        The button should behave differently for a hover and a click, but a click will always starts with a hover.
        """
        if self.check_mouse_click():
            self.apply_mouse_click()
        else:
            self.apply_mouse_hover()

    def update(self: object, events: List[str]) -> None:
        """
        Checks potential self.events, otherwise ensures that the button is reset.
        """
        self.events = events
        if self.interactive:
            if self.check_mouse_hover():
                self.apply_mouse_click_or_hover()
            else:
                self.reset_button()


class BASE_SliderButton(Button):
    """
    A class that is used to define the general features for the two different 'SliderButton' classes.
    """
    def __init__(self: object, screen: object, centre: List[int], width: int, height: int, bg_colour: Tuple[int, int, int],
                 border_colour: Tuple[int, int, int], border_width: int, slider_bar_length: int,
                 slider_bar_height: int, bar_colour: Tuple[int, int, int]) -> object:
        """
        screen: pygame screen object
            - used as the pygame surface that all parts of the button is drawn to.
        centre: List[int, int]
            - is used for the centre of the button.
            - pygame draws rectangle objects with a 'start xy' and 'end xy', so the 'centre' is converted.
        width: int
            - the width of the button.
            - measured in number of pixels.
        height: int
            - the height of the button.
            - measured in number of pixels.
        bg_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's background, this is the main part of the button.
        border_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's border, this is the outline of the button.
        border_width: int
            - this is width of the border.
            - recommened values between 0 and 10.
            - measured in number of pixels.
        slider_bar_length: int
            - the number of pixels from the far most left of the bar to the far most right of the bar.
            - the slider's bar length will be the same as the slider's 'limit'.
            - the 'limit' of the slider is how far the button part of the slider can move from its centre.
        slider_bar_height: int
            - the width of the bar.
        bar_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's bar, this is the line behind the button that shows the 'limit' for the slider button.
       """
        super().__init__(screen, centre, width, height, bg_colour, border_colour, border_width)
        # Used to set the bounds of the slider, half 'slide_length' on left side and half 'side_length' on right side
        # self.slide_length = bar_length
        # The neutral position of the slider, used to make sure the slider isn't taken out of its bounds
        self.bar_colour = bar_colour
        self.limit = slider_bar_length//2

        self.value = 0

    def draw(self: object) -> None:
        """
        Draws the bar then calls the draw method from the parent class for the button.
        """
        pygame.draw.rect(self.surface, self.bar_colour, self.bar_rect_object)
        super().draw()

    def check_mouse_button_up(self: object) -> bool:
        """
        Is needed so the slider can stop moving when the user is no longer dragging it.
        """
        for event in self.events:
            if event.type == pygame.MOUSEBUTTONUP:
                return True
        return False
    
    def apply_mouse_click(self: object) -> None:
        """
        Will keep updating the position of the slider button until the mouse button is released.
        """
        super().apply_mouse_click()
        self.update_slider_pos()


class HorizontalSliderButton(BASE_SliderButton):
    """
    The HorizontalSliderButton class is the class that defines the behaviour and functionality which is specific to horizontal
    sliders.
    """
    def __init__(self: object, screen: object, centre: List[int], width: int, height: int, bg_colour: Tuple[int, int, int],
                 border_colour: Tuple[int, int, int], border_width: int, slider_bar_length: int,
                 slider_bar_height: int, bar_colour: Tuple[int, int, int]) -> object:
        """
        screen: pygame screen object
            - used as the pygame surface that all parts of the button is drawn to.
        centre: List[int, int]
            - is used for the centre of the button.
            - pygame draws rectangle objects with a 'start xy' and 'end xy', so the 'centre' is converted.
        width: int
            - the width of the button.
            - measured in number of pixels.
        height: int
            - the height of the button.
            - measured in number of pixels.
        bg_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's background, this is the main part of the button.
        border_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's border, this is the outline of the button.
        border_width: int
            - this is width of the border.
            - recommened values between 0 and 10.
            - measured in number of pixels.
        slider_bar_length: int
            - the number of pixels from the far most left of the bar to the far most right of the bar.
            - the slider's bar length will be the same as the slider's 'limit'.
            - the 'limit' of the slider is how far the button part of the slider can move from its centre.
        slider_bar_height: int
            - the width of the bar.
        bar_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's bar, this is the line behind the button that shows the 'limit' for the slider button.
       """
        super().__init__(screen, centre, width, height, bg_colour, border_colour, border_width, slider_bar_length,
                         slider_bar_height, bar_colour)
        slider_bar_width = slider_bar_length

        self.bar_rect_object = pygame.Rect(centre[0] - slider_bar_width//2, centre[1] - slider_bar_height//2,
                                           slider_bar_width, slider_bar_height)
        self.neutral_position = centre[0]
        self.bar_length = slider_bar_length

    def update_slider_pos(self: object) -> None:
        """
        Updates the x position of the button part of the slider.
        """
        mouse_xy = pygame.mouse.get_pos()
        if mouse_xy[0] >= self.neutral_position + self.limit - self.width//2:
            self.centre_pos[0] = self.neutral_position + self.limit - self.width//2
        elif mouse_xy[0] <= self.neutral_position - self.limit + self.width//2:
            self.centre_pos[0] = self.neutral_position - self.limit + self.width//2
        else:
            self.centre_pos[0] = mouse_xy[0]
        
        self.pygame_button_object = pygame.Rect(self.centre_pos[0] - self.width//2, self.start_xy[1], self.width, self.height)

        self.value = -1 * (self.bar_length / 100) * ((self.neutral_position - self.centre_pos[0] ))
        self.value = -1 * (self.neutral_position - self.centre_pos[0])/abs(self.neutral_position - self.centre_pos[0] - self.width//2)


class VerticalSliderButton(BASE_SliderButton):
    """
    The VerticalSliderButton class is the class that defines the behaviour and functionality which is specific to vertical sliders.
    """
    def __init__(self: object, screen: object, centre: List[int], width: int, height: int, bg_colour: Tuple[int, int, int],
                 border_colour: Tuple[int, int, int], border_width: int, slider_bar_width: int,
                 slider_bar_length: int, bar_colour: Tuple[int, int, int]) -> object:
        """
        screen: pygame screen object
            - used as the pygame surface that all parts of the button is drawn to.
        centre: List[int, int]
            - is used for the centre of the button.
            - pygame draws rectangle objects with a 'start xy' and 'end xy', so the 'centre' is converted.
        width: int
            - the width of the button.
            - measured in number of pixels.
        height: int
            - the height of the button.
            - measured in number of pixels.
        bg_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's background, this is the main part of the button.
        border_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's border, this is the outline of the button.
        border_width: int
            - this is width of the border.
            - recommened values between 0 and 10.
            - measured in number of pixels.
        slider_bar_length: int
            - the number of pixels from the far most left of the bar to the far most right of the bar.
            - the slider's bar length will be the same as the slider's 'limit'.
            - the 'limit' of the slider is how far the button part of the slider can move from its centre.
        slider_bar_height: int
            - the width of the bar.
        bar_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's bar, this is the line behind the button that shows the 'limit' for the slider button.
       """
        super().__init__(screen, centre, width, height, bg_colour, border_colour, border_width, slider_bar_length,
                         slider_bar_width, bar_colour)
        slider_bar_height = slider_bar_length

        self.bar_rect_object = pygame.Rect(centre[0] - slider_bar_width//2, centre[1] - slider_bar_height//2,
                                           slider_bar_width, slider_bar_height)
        self.neutral_position = centre[1]
        self.bar_length = slider_bar_length

    def update_slider_pos(self: object) -> None:
        """
        Updates the y position of the button part of the slider.
        """
        mouse_xy = pygame.mouse.get_pos()
        if mouse_xy[1] >= self.neutral_position + self.limit - self.height//2:
            self.centre_pos[1] = self.neutral_position + self.limit - self.height//2
        elif mouse_xy[1] <= self.neutral_position - self.limit + self.height//2:
            self.centre_pos[1] = self.neutral_position - self.limit + self.height//2
        else:
            self.centre_pos[1] = mouse_xy[1]
        
        self.pygame_button_object = pygame.Rect(self.start_xy[0], self.centre_pos[1] - self.height//2, self.width, self.height)

        self.value = -1 * (self.bar_length / 100) * ((self.neutral_position - self.centre_pos[1] ))


class TextButton(Button):
    """
    The TextButton has the same functionality as the Button but also allows for there to be text on the face of the button
    """
    def __init__(self: object, screen: object, centre: List[int], width: int, height: int, bg_colour: Tuple[int, int, int],
                 border_colour: Tuple[int, int, int], border_width: int, font: str, text_size: int, text: str,
                 text_colour: Tuple[int, int, int], interactive=True) -> object:
        """
        screen: pygame screen object
            - used as the pygame surface that all parts of the button is drawn to.
        centre: List[int, int]
            - is used for the centre of the button.
            - pygame draws rectangle objects with a 'start xy' and 'end xy', so the 'centre' is converted.
        width: int
            - the width of the button.
            - measured in number of pixels.
        height: int
            - the height of the button.
            - measured in number of pixels.
        bg_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's background, this is the main part of the button.
        border_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's border, this is the outline of the button.
        border_width: int
            - this is width of the border.
            - recommened values between 0 and 10.
            - measured in number of pixels.
        font: str
            - the style of font of the text.
            - E.g.: "Arial", "Comic Sans", etc.
        text_size: int
            - the size of the text.
        text: str
            - the text shown on the button.
        text_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's text.
        interactive: bool [True]
            - default value is True.
            - if False, then the button will not get updated at all during the program's runtime.
        """
        super().__init__(screen, centre, width, height, bg_colour, border_colour, border_width, interactive)

        self.sys_font = pygame.font.SysFont(font, text_size)
        self.text_colour = text_colour
        self.text = text

    def apply_mouse_click(self: object) -> None:
        """
        Currently it prints the text on the button to the terminal. This is to test that this feature works correctly.
        The intension is that this will create an alert that the menu system will use to determine which menu page to show next.
        """
        super().apply_mouse_click()
        print(self.text)

    def draw_text(self: object) -> None:
        """
        This method will update the text to the current pygame surface.
        """
        lines = str(self.text).split("\n")
        number_of_lines = len(lines)
        if number_of_lines > 1:
            for line_num, line in enumerate(lines):
                textobj = self.sys_font.render(line, 1, self.text_colour)
                textrect = textobj.get_rect()
                textrect.center = [self.centre_pos[0], self.centre_pos[1] + ((line_num - 1)* 10)]
                self.surface.blit(textobj, textrect)
        else:
            textobj = self.sys_font.render(str(self.text), 1, self.text_colour)
            textrect = textobj.get_rect()
            textrect.center = self.centre_pos
            self.surface.blit(textobj, textrect)


    def draw(self: object) -> None:
        """
        Draws the button and the text to the screen.
        """
        super().draw()
        self.draw_text()


class TextInputBox(TextButton):
    """
    Inherits from the TextButton and allows for the text to be changed by the user by clicking on the button and typing.
    The colour of the border changes depending on whether the button is 'selected' (clicked on) or not. There is also a default
    text that will be displayed to the button if there is no other text to display.
    """
    def __init__(self: object, screen: object, centre: List[int], width: int, height: int, bg_colour: Tuple[int, int, int],
                 unselected_border_colour: Tuple[int, int, int], selected_border_colour: Tuple[int, int, int],
                 border_width: int, font: str, text_size: int, default_text: str, text_colour: Tuple[int, int, int],
                 hidden=False) -> object:
        """
        screen: pygame screen object
            - used as the pygame surface that all parts of the button is drawn to.
        centre: List[int, int]
            - is used for the centre of the button.
            - pygame draws rectangle objects with a 'start xy' and 'end xy', so the 'centre' is converted.
        width: int
            - the width of the button.
            - measured in number of pixels.
        height: int
            - the height of the button.
            - measured in number of pixels.
        bg_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's background, this is the main part of the button.
        border_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's border, this is the outline of the button.
        border_width: int
            - this is width of the border.
            - recommened values between 0 and 10.
            - measured in number of pixels.
        font: str
            - the style of font of the text.
            - E.g.: "Arial", "Comic Sans", etc.
        text_size: int
            - the size of the text.
        default_text: str
            - the default text that is shown on the button.
            - this text is shown when there is no other text to show.
            - recommended to use default text as a prompt. E.g.: 'Enter Text', 'Enter Password', etc.
        text_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's text.
        interactive: bool [True]
            - default value is True.
            - if False, then the button will not get updated at all during the program's runtime.
        hidden: bool [False]
            - default value is Fales.
            - if True, then the button will only display asterisks instead of the inputted text (unless that text is the default
              text).
            - E.g.: 'password123' -> '***********'.
        """
        self.unselected_border_colour = unselected_border_colour
        self.selected_border_colour = selected_border_colour
        self.border_colour = self.unselected_border_colour
        self.default_text = default_text
        # Creates a copy of the width for when the button is reset as 'width' will change during runtime.
        self.minimum_width = width
        self.hidden = hidden

        super().__init__(screen, centre, width, height, bg_colour, self.border_colour, border_width, font, text_size, 
                         default_text, text_colour)

    def apply_mouse_click(self: object) -> None:
        """
        The border colour is changed to the 'selected' border colour to show that the button is currently being selected.
        """
        super().apply_mouse_click()
        self.border_colour = self.selected_border_colour

    def apply_text_submit(self: object) -> None:
        """
        Currently it prints the text on the button to the terminal and resets the button's text. This is to test that this 
        feature works correctly. The intension is similar to that of the TextButton, but will primarily be used to submitting 
        different values for data entry purposes suchs as for entering data fields that are restricted to certain values 
        (i.e. the student's class name or the teacher's title).
        """
        print(self.text)
        self.text = self.default_text 
        self.width = self.minimum_width
        # Calls update_size to reset the size of the button to be in line with the default text.
        self.update_size()

    def update_size(self: object) -> None:
        """
        Increases the width of the button to accomodate the ammount of text that needs to be displayed. The new size of the button
        is calculated each time the method is called and it does not add on to a previous value. This allows the size of the button
        to both increase and decrease as required. It will also ensure that the button does not decrease past a minimum size
        (specified by the origional value of the 'width' attribute).
        """
        width = 12 * len(self.text)
        if width >= self.minimum_width:
            self.width = width

        self.start_xy = (self.centre_pos[0] - self.width//2, self.centre_pos[1] - self.height//2)
        self.end_xy = (self.centre_pos[0] + self.width//2, self.centre_pos[1] + self.height//2)
        self.pygame_button_object = pygame.Rect(self.start_xy[0], self.start_xy[1], self.width, self.height)

    def check_default_text(self: object) -> None:
        """
        Checks if the button's text is the default text and if the button is selected. In which case it will set the button's text
        to the empty string so that the user can input their desired text.
        """
        if (self.border_colour == self.selected_border_colour) and (self.text == self.default_text):
            self.text = ""

    def update_text(self: object) -> None:
        """
        Will check all Pygame 'KEYDOWN' events to determine if the text in the button needs to be updated.
        """
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                # Checks if the size needs to be updated.
                self.update_size()
                if event.key == pygame.K_BACKSPACE:
                    # [:-1] copies up to (i.e. not including) the last item in a list/string.
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.apply_text_submit()
                else:
                    # 'unicode' is an attribute that certain Pygame events have that corresponds to the character they represent
                    # i.e. the Pygame event that corresponds to the 'a' key being pressed will have a 'unicode' attribute of 'a'.
                    # The unicode attribute also takes into account key modifiers so that when the keys 'a' and 'shift' and pressed,
                    # the events have a single unicode attribute 'A'.
                    self.text += event.unicode

    def reset_button(self: object) -> None:
        """
        Resets the colour of the button as well as checking if the button's text is the empty string and if the button is 
        not selected. If so it will set the button's text to the default text specified in initialisation.
        """
        super().reset_button()
        if self.text == "" and (self.border_colour == self.unselected_border_colour):
            self.text = self.default_text

    def draw_text(self: object):
        if not self.hidden or self.text == self.default_text:
            super().draw_text()
        else:
            hidden_text = len(self.text) * "*"
            textobj = self.sys_font.render(hidden_text, 1, self.text_colour)
            textrect = textobj.get_rect()
            textrect.center = self.centre_pos
            self.surface.blit(textobj, textrect)

    def update(self, events):
        """
        It will call the super class's update and then also check if the user clicks off of the button. It will also check if it is
        currently selected and if so it will call the 'update_text' method to check if the button's text needs to be changed.
        """
        super().update(events)
        self.check_default_text()
        if self.check_mouse_click() and not self.check_mouse_hover():
            self.border_colour = self.unselected_border_colour
        if self.border_colour == self.selected_border_colour:
            self.update_text()


class TextInputBoxRightExpansion(TextInputBox):
    """
    TextInputBoxRightExpansion acts very similarly to TextInputBox. The only difference is that instead of expanding both ways to 
    accomodate the extra text it needs to display, it will only expand to the right.
    """
    def __init__(self: object, screen: object, centre: List[int], width: int, height: int, bg_colour: Tuple[int, int, int],
                 unselected_border_colour: Tuple[int, int, int], selected_border_colour: Tuple[int, int, int],
                 border_width: int, font: str, text_size: int, text: str, text_colour: Tuple[int, int, int]) -> object:
        """
        screen: pygame screen object
            - used as the pygame surface that all parts of the button is drawn to.
        centre: List[int, int]
            - is used for the centre of the button.
            - pygame draws rectangle objects with a 'start xy' and 'end xy', so the 'centre' is converted.
        width: int
            - the width of the button.
            - measured in number of pixels.
        height: int
            - the height of the button.
            - measured in number of pixels.
        bg_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's background, this is the main part of the button.
        border_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's border, this is the outline of the button.
        border_width: int
            - this is width of the border.
            - recommened values between 0 and 10.
            - measured in number of pixels.
        font: str
            - the style of font of the text.
            - E.g.: "Arial", "Comic Sans", etc.
        text_size: int
            - the size of the text.
        default_text: str
            - the default text that is shown on the button.
            - this text is shown when there is no other text to show.
            - recommended to use default text as a prompt. E.g.: 'Enter Text', 'Enter Password', etc.
        text_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's text.
        interactive: bool [True]
            - default value is True.
            - if False, then the button will not get updated at all during the program's runtime.
        """
        super().__init__(screen, centre, width, height, bg_colour, unselected_border_colour, selected_border_colour,
                         border_width, font, text_size, text, text_colour)
        self.increased_size = 0
        self.origional_x_pos = centre[0]

    def update_text_pos(self: object) -> None:
        """
        Checks if the button needs to change its size in order to accomodate the new length of the text.
        The size of the button will now decrease beyond a minimum value. This herehherhehr
        """
        if self.width == self.minimum_width:
            self.centre_pos = [self.origional_x_pos, self.centre_pos[1]]

        x_update = 6 * len(self.text)
        if x_update >= (self.minimum_width // 2):
            self.centre_pos = [self.origional_x_pos + x_update - self.width // 4, self.centre_pos[1]]

    def update_size(self: object) -> None:
        """
        Increases the width of the button to accomodate the ammount of text that needs to be displayed. The size of the button
        only updates to the right. The new size of the button is calculated each time the method is called and it does not add 
        on to a previous value. This allows the size of the button to both increase and decrease as required. It will also ensure 
        that the button does not decrease past a minimum size (specified by the origional value of the 'width' attribute).
        """
        width = 12 * len(self.text)
        if width >= self.minimum_width:
            self.width = width

        self.centre_pos = [self.centre_pos[0], self.centre_pos[1]]
        self.end_xy = (self.centre_pos[0] + self.width//2, self.centre_pos[1] + self.height//2)
        self.pygame_button_object = pygame.Rect(self.start_xy[0], self.start_xy[1], self.width, self.height)

    def update(self: object, events) -> None:
        """
        It will call the super class's update and then also check if the user clicks off of the button. It will also check if it is
        currently selected and if so it will call the 'update_text' method to check if the button's text needs to be changed.
        """
        super().update(events)
        self.update_text_pos()


class DropDownSelectButton(TextButton):
    """
    
    """
    def __init__(self: object, screen: object, centre: List[int], width: int, height: int, bg_colour: Tuple[int, int, int],
                 unselected_border_colour: Tuple[int, int, int], selected_border_colour: Tuple[int, int, int],
                 border_width: int, font: str, text_size: int, text_options: Tuple[str], text_colour: Tuple[int, int, int],
                 gap=0) -> object:
        """
        screen: pygame screen object
            - used as the pygame surface that all parts of the button is drawn to.
        centre: List[int, int]
            - is used for the centre of the button.
            - pygame draws rectangle objects with a 'start xy' and 'end xy', so the 'centre' is converted.
        width: int
            - the width of the button.
            - measured in number of pixels.
        height: int
            - the height of the button.
            - measured in number of pixels.
        bg_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's background, this is the main part of the button.
        unselected_border_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's border when the button is not selected, this is the outline of the button.
        selected_border_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's border when the button is selected, this is the outline of the button.
        border_width: int
            - this is width of the border.
            - recommened values between 0 and 10.
            - measured in number of pixels.
        font: str
            - the style of font of the text.
            - E.g.: "Arial", "Comic Sans", etc.
        text_size: int
            - the size of the text.
        text_options: Tuple[str]
            - the first element in 'text_options' will be the default text for the button.
            - this text is shown when there is no other text to show and will be the initial text of the button.
            - recommended to use default text as a prompt. E.g.: 'Choose an Option', 'Enter Title', etc.
        text_colour: Tuple[int, int, int]
            - (red, green, blue) all values are between 0 and 225.
            - the colour of the button's text.
        gap: int [0]
            - the space (in pixels) between the different options / button components.
            - the default value is 0 and the recommened limit it 10.
        """
        self.unselected_border_colour = unselected_border_colour
        self.selected_border_colour = selected_border_colour
        self.border_colour = self.unselected_border_colour
        self.options = text_options
        # Creates a list of 'TextButton' objects to be used as the button components for the 'options'
        self.option_objects = [TextButton(screen, [centre[0], centre[1] + i * (height + gap)], width, height, bg_colour, 
                                           unselected_border_colour, border_width, font, text_size, text_options[i], text_colour) 
                                for i in range(1, len(text_options))]
        # A flag that keeps track of whether or not the options (drop down part of this drop down button) should be shown or not.
        self.show_options = False

        # Is used to create the 'main' button which is a 'TextButton' object that will always be shown and is what activates the
        # other 'TextButton' objects when clicked.
        super().__init__(screen, centre, width, height, bg_colour, self.border_colour, border_width, font, text_size, 
                         text_options[0], text_colour)

    def apply_mouse_click(self: object) -> None:
        """
        Toggles the 'options' by inverting the 'show_options' flag.
        If currently showing option button components -> no longer show option button components (and vice versa).
        """
        super().apply_mouse_click()
        self.show_options = not self.show_options

    def update(self: object, events) -> None:
        """
        It will call the super class's update and then also check if the option button components are currently active.
        If so it will call each of their 'update' and 'draw' mehtods. Also if the user has clicked on one of the option
        buttons, then the current 'self.text' (i.e. the main button's text) will be set to the option button's text. This
        will give the user visual feedback that the option has been selected.
        """
        super().update(events)
        if self.show_options:
            for option in self.option_objects:
                option.update(events)
                option.draw()
                if option.check_mouse_click() and option.check_mouse_hover():
                    self.text = option.text
                

