from random import randrange
from typing import List
import buttons

class ImplementationError(Exception):
	"""
	This is a custom type of error that is raised when I have not yet implemented a certain 
	feature for the program. It will help with debuging and testing purposes as it specifies
	what the feautre is that has not yet been implmented as well as what the current menu was
	when the expcetion/error was raised.
	"""
	def __init__(self: object, message: str, menu: str, payload=None):
		"""
		message: str
			- the message that will be displayed as the error message. 
			- i.e. this is the feature that has not been implemented.
		menu: str
			- the menu from which a button pressed caused this exception.
		payload: int [None]
			- The 'payload' attribute is required for all Python Exception objects.
			- The defalut value is 'None' and does not need to be specified for the function 
			  of this Exception subclass.
		"""
		self.message = message
		self.payload = payload
		self.menu = menu

	def __str__(self: object):
		"""
		This methods dictates what the error message will look like. In this case it will look like:
		"tests.ImplementationError: The '[INSERT FEATURE]' has not yet been implemented in the '[INSERT MENU]' menu."
		"""
		return f"The '{self.message}' has not yet been implemented in the '{self.menu}' menu."


class UnkownUseCaseError(Exception):
	"""
	This is a custom type of error that is raised when the feature requested by the user is not known.
	"""
	def __init__(self: object, message: str, menu: str, payload=None):
		"""
		message: str
			- the message that will be displayed as the error message. 
			- i.e. this is the feature that is not known.
		payload: int [None]
			- The 'payload' attribute is required for all Python Exception objects.
			- The defalut value is 'None' and does not need to be specified for the function 
			  of this Exception subclass.
		"""
		self.message = message
		self.payload = payload

	def __str__(self: object):
		"""
		This methods dictates what the error message will look like. In this case it will look like:
		"tests.UnkownUseCaseError: Unkown use of the '[INSERT FEATURE]' feature."
		"""
		return f"Unkown use of the '{self.message}' feature."


def all_button_stress_test(screen):
	"""
	This test will fill the screen with objects of the 'Button' class. It is intended to stress the system as
	the number of button objects in this test far exceeds the number that will ever be needed at a given time
	by the final program.
	"""
	button_ls = []
	for j in range(1, 10):
		button_ls += [buttons.Button(screen, [60 * i, 60 * j], 50, 50, 
					 (randrange(0, 255), randrange(0, 255), randrange(0, 255)),
					 (randrange(0, 255), randrange(0, 255), randrange(0, 255)),10) 
					  for i in range(1,13)]
	return button_ls

def v_slider_stress_test(screen):
	"""
	This test will fill the screen with objects of the 'VerticalSliderButton' class. It is intended to stress 
	the system as the number of slider button objects in this test far exceeds the number that will ever be 
	needed at a given time by the final program.
	"""
	button_ls = []
	for j in range(1, 3):
		button_ls += [buttons.VerticalSliderButton(screen, [100 * i, 200 * j], 60, 30, 
									 (randrange(0, 255), randrange(0, 255), randrange(0, 255)),
									 (randrange(0, 255), randrange(0, 255), randrange(0, 255)), 5, 15, 150,
									 (randrange(0, 255), randrange(0, 255), randrange(0, 255)))
						for i in range(1, 8)]

	return button_ls

def h_slider_stress_test(screen):
	"""
	This test will fill the screen with objects of the 'HorizontalSliderButton' class. It is intended to stress 
	the system as the number of slider button objects in this test far exceeds the number that will ever be 
	needed at a given time by the final program.
	"""
	button_ls = []
	for j in range(1, 6):
		button_ls += [buttons.HorizontalSliderButton(screen, [130 + 180 * i, 100 * j], 30, 60, 
									 (randrange(0, 255), randrange(0, 255), randrange(0, 255)),
									 (randrange(0, 255), randrange(0, 255), randrange(0, 255)), 5, 150, 15,
									 (randrange(0, 255), randrange(0, 255), randrange(0, 255)))
						for i in range(0, 4)]

	return button_ls

def text_button_stress_test(screen):
	"""
	This test will fill the screen with objects of the 'TextButton' class. It is intended to stress the system as
	the number of text button objects in this test far exceeds the number that will ever be needed at a given time
	by the final program.
	"""
	button_ls = []
	test_num = 0
	for j in range(1, 6):
		button_ls += [buttons.TextButton(screen, [115 * i, 100 * j], 100, 75, 
					 (randrange(0, 255), randrange(0, 255), randrange(0, 255)),
					 (randrange(0, 255), randrange(0, 255), randrange(0, 255)), 10, "Arial", 20, f"Test {test_num + i}", (0, 0, 0))
					  for i in range(1,7)]
		test_num += 7
	return button_ls

def text_input_test(screen):
	"""
	This test instantiates a single 'TextInputButton' object so that I can test its functionality.
	"""
	button_ls = [buttons.TextInputBox(screen, [200, 200], 200, 100, (255, 0, 0), (0, 255, 0), (0, 0, 255), 10, "Arial", 20,
									  "Enter Text", (0, 255, 255))]
	
	return button_ls

def text_input_test_2(screen):
	"""
	This test instantiates a single 'TextInputButtonRightExpansion' object so that I can test its functionality.
	"""
	button_ls = [buttons.TextInputBoxRightExpansion(screen, [200, 200], 200, 100, (0, 0, 255), (255, 255, 0), (255, 0, 255), 10, "Arial", 20,
									  "Enter Text", (0, 255, 255))]
	
	return button_ls

def drop_down_test(screen):
	"""
	This test instantiates a single 'DropDownSelectButton' object with 3 options so that I can test their functionality.
	"""
	button_ls = [buttons.DropDownSelectButton(screen, [200, 200], 200, 100, (0, 0, 255), (255, 255, 0), (255, 0, 255), 10, 
											  "Arial", 20, ["Main", "option 1", "option 2"], (0, 255, 255), 5)]
	
	return button_ls

def all_button_types_test(screen):
	"""
	This test instantiates one type of all of the buttons so that I can test all of the buttons together.
	This test is also useful for getting feedback about the buttons from my stakeholders.
	"""
	button_ls = [buttons.TextButton(screen, [400, 100], 500, 200, (255, 0, 0), (0, 255, 0), 3, "Arial", 40, 
									"ALL BUTTON TYPES TEST", (0, 255, 255), False),
				 buttons.Button(screen, [100, 100], 50, 50, (255, 0, 0), (0, 255, 0), 3),
				 buttons.Button(screen, [80, 300], 20, 20, (255, 0, 0), (0, 255, 0), 2),
				 buttons.HorizontalSliderButton(screen, [400, 250], 30, 60, 
									 (randrange(0, 255), randrange(0, 255), randrange(0, 255)),
									 (randrange(0, 255), randrange(0, 255), randrange(0, 255)), 5, 150, 15,
									 (randrange(0, 255), randrange(0, 255), randrange(0, 255))),
				 buttons.VerticalSliderButton(screen, [600, 400], 60, 30, 
									 (randrange(0, 255), randrange(0, 255), randrange(0, 255)),
									 (randrange(0, 255), randrange(0, 255), randrange(0, 255)), 5, 15, 150,
									 (randrange(0, 255), randrange(0, 255), randrange(0, 255))),
				 buttons.TextInputBoxRightExpansion(screen, [400, 400], 200, 100, (255, 0, 0), (0, 255, 0), (0, 0, 255), 10, "Arial", 20,
									  "Enter Text", (0, 255, 255)),
				 buttons.TextInputBox(screen, [300, 525], 200, 100, (0, 0, 255), (255, 255, 0), (255, 0, 255), 10, "Arial", 20,
									  "Enter Text", (0, 255, 255)),
				 buttons.DropDownSelectButton(screen, [200, 200], 200, 100, (0, 0, 255), (255, 255, 0), (255, 0, 255), 10, 
											  "Arial", 20, ["Chose and option", "option 1", "option 2", "option 3"], 
											  (0, 255, 255), 5)
				 ]
	return button_ls
