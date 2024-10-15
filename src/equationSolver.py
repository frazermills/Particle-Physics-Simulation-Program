import pygame
from typing import List
import buttons
import sympy
from tests import UnkownUseCaseError

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
# Initialising the ‘sympy’ ‘symbol’ objects and grouping them together in a list.
s, u, v, a, t = sympy.symbols('s u v a t')
SUVAT_vars = [s, u, v, a, t]

# Creating my five SUVAT equations using the ‘symbol’ objects that I instantiated from the ‘sympy’ module.
SUVA = u**2 + 2*a*s
SUVT = ((u+v)*t)/2
SUAT = u*t + 0.5 * t**2
SVAT = v*t - 0.5 * t**2
UVAT = u + a*t

# Putting the five SUVAT equations into a dictionary so that I can reference them as ‘no s’, ‘no u’, etc.
SUVAT_EQUATIONS = {
	"SUVA": sympy.Eq(v**2, SUVA),
	"SUVT": sympy.Eq(s, SUVT),
	"SUAT": sympy.Eq(s, SUAT),
	"SVAT": sympy.Eq(s, SVAT),
	"UVAT": sympy.Eq(v, UVAT)
}

class EquationSolver:
	"""
	This is the base equation solver class for the 'Equation Solver' feature.
	Due to time constraints this class was not fully implemented but still exists as it is required as a dependency for the
	'GeneralSUVATSolver' class.
	"""
	def __init__(self, screen, title, equation_variables, colour_scheme=DEFAULT_COLOUR_SCHEME, border_width=3, 
				 title_width=300, title_height=100, title_font="Arial", title_size=40, variable_width=50, variable_height=50, 
				 variable_font="Arial", variable_size=20) -> object:
		"""
		screen: pygame screen object
			- used as the pygame surface that all of the buttons will be drawn to.
		title: str
			- the title of the equation solver page.
		equation_variables: List[str]
			- a list of all of the individual variables that are in the equation.
			- e.g. F = ma would have 3 separate 'equation_variables'.
		colour_scheme: Tuple[Tuple[int, int, int]] [DEFAULT_COLOUR_SCHEME]
			- The colours for the different components of the buttons and title in the menu page.
			- order of items:
				0. title_bg_colour		- the colour of the title's background, this is the main part of the title.
				1. title_border_colour	- the colour of the title's border, this is outline of the title.
				2. title_text_colour	  - the colour of the title's text.
				3. variable_bg_colour	 - the colour of the variables' background, this is the main part of the variable buttons.
				4. variable_border_colour - the colour of the variables' border, this is outline of the variable buttons.
				5. variable_text_colour   - the colour of the variables' text.
		border_width: int [3]
			- the width of the borders for both the title and the button variables.
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
		variable_width: int [200]
			- the width of the variable buttons.
			- an integer for the number of pixels.
		variable_height: int [80]
			- the height of the variable buttons.
			- an integer for the number of pixels.
		variable_font: str ["Arial"]
			- the font style for the button variable's text on the menu page.
		variable_size: int [20]
			- the font size of the text in the variable buttons.
		"""
		self.screen = screen
		self.show_plain_text = False

		self.centre_x = screen.get_width() // 2
		self.centre_y = screen.get_height() // 2
		# Decomposing the 'colour_scheme' list into the its colour values.
		title_bg_col, title_border_col, title_text_col, variable_bg_col, variable_border_col, variable_text_col = colour_scheme[:6]
		variable_selected_border_col = title_border_col
		# Creating the title button (which is not interactive) as a single object in a list to help create the button list.
		self.menu_buttons = [buttons.TextButton(screen, [self.centre_x, 100], title_width, title_height, title_bg_col, title_border_col, 
										   border_width, title_font, title_size, title, title_text_col, False),
						buttons.TextButton(screen, [screen.get_width() - 100, screen.get_height() - 50], 150, 80, 
										  title_bg_col, title_border_col, border_width, variable_font, variable_size, 
										  "Go Back", title_text_col),
						buttons.TextButton(screen, [100, screen.get_height() - 50], 150, 80, 
										  variable_bg_col, variable_border_col, border_width, variable_font, variable_size, 
										  "Solve", variable_text_col),
						buttons.TextButton(screen, [screen.get_width() - 200, 240], 
										   300, 100, title_bg_col, title_border_col, border_width, 
										   variable_font, variable_size, "Equation:", title_text_col, False),
						buttons.TextButton(screen, [screen.get_width() - 200, 370], 
										   300, 100, title_bg_col, title_border_col, border_width, 
										   variable_font, variable_size, "Rearranged:", title_text_col, False),
						buttons.TextButton(screen, [screen.get_width() - 200, 500], 
										   300, 100, title_bg_col, title_border_col, border_width, 
										   variable_font, variable_size, "Answer:", title_text_col, False),
						buttons.TextButton(screen, [screen.get_width()//2, screen.get_height() - 50], 
										   200, 80, variable_bg_col, variable_border_col, border_width, 
										   variable_font, variable_size, "View In Plain Text", variable_text_col)]
		# Finding the number of variables. 
		number_of_variables = len(equation_variables)

		y_offset = number_of_variables * (variable_height // 2) + variable_height//4
		# Creating a list of all the variable buttons.
		self.variable_buttons = []
		for i, variable in enumerate(equation_variables):
			self.variable_buttons.append(buttons.TextInputBox(screen, [100 * (1 + (i // 4)), (self.centre_y + i * 80) - y_offset], 
													 variable_width, variable_height, variable_bg_col, variable_border_col, 
													 variable_selected_border_col, border_width, variable_font, variable_size, 
													 equation_variables[i], variable_text_col))
			
		# Creating the button list attribute which contains all interactive and non-interactive buttons.
		self.button_ls = self.menu_buttons + self.variable_buttons

	def solve(self):
		"""
		This method has not been implemented due to time constraints.
		"""
		pass

	def update_menu(self: object, events: List[str]) -> None:
		"""
		This method will iterate over every button in the 'button_ls' attribute and will call each button's 'update' and 'draw' methods 
		in turn.
		"""
		for button in self.button_ls:
			button.update(events)
			button.draw()
			

class GeneralSUVATSolver(EquationSolver):
	def __init__(self, screen, title, equation_variables, colour_scheme=DEFAULT_COLOUR_SCHEME, border_width=3, 
				 title_width=300, title_height=100, title_font="Arial", title_size=40, variable_width=50, variable_height=50, 
				 variable_font="Arial", variable_size=20) -> object:
		"""
		screen: pygame screen object
			- used as the pygame surface that all of the buttons will be drawn to.
		title: str
			- the title of the equation solver page.
		equation_variables: List[str]
			- a list of all of the individual variables that are in the equation.
			- e.g. F = ma would have 3 separate 'equation_variables'.
		colour_scheme: Tuple[Tuple[int, int, int]] [DEFAULT_COLOUR_SCHEME]
			- The colours for the different components of the buttons and title in the menu page.
			- order of items:
				0. title_bg_colour		- the colour of the title's background, this is the main part of the title.
				1. title_border_colour	- the colour of the title's border, this is outline of the title.
				2. title_text_colour	  - the colour of the title's text.
				3. variable_bg_colour	 - the colour of the variables' background, this is the main part of the variable buttons.
				4. variable_border_colour - the colour of the variables' border, this is outline of the variable buttons.
				5. variable_text_colour   - the colour of the variables' text.
		border_width: int [3]
			- the width of the borders for both the title and the button variables.
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
		variable_width: int [200]
			- the width of the variable buttons.
			- an integer for the number of pixels.
		variable_height: int [80]
			- the height of the variable buttons.
			- an integer for the number of pixels.
		variable_font: str ["Arial"]
			- the font style for the button variable's text on the menu page.
		variable_size: int [20]
			- the font size of the text in the variable buttons.
		"""
		super().__init__(self, screen, title, equation_variables, colour_scheme, border_width, title_width, title_height, 
						 title_font, title_size, variable_width, variable_height, variable_font, variable_size)

		self.variable_buttons = [buttons.TextInputBox(screen, [100, (self.centre_y + i * 80) - y_offset], variable_width, 
												variable_height, variable_bg_col, variable_border_col, variable_selected_border_col,
												border_width, variable_font, variable_size, equation_variables[i], variable_text_col)
						  for i in range(number_of_variables)]
		# Creating the button list attribute which contains all interactive and non-interactive buttons.
		self.button_ls = self.menu_buttons + self.variable_buttons

	def solve(self):
		"""
		This method will check which is the missing variable and choose an appropriate 'SUVAT' equation. It will then rearrange that 
		equation for the unkown variable (which is different from the missing variable). Finally it will substitute in all of the known
		values and then display the equation steps in the suitable buttons on the 'Generate SUVAT Sovler' menu screen.
		"""
		# Check which equation to use.
		if self.variable_buttons[0].text == "X":
			equation = SUVAT_EQUATIONS["UVAT"]
		elif self.variable_buttons[1].text == "X":
			equation = SUVAT_EQUATIONS["SVAT"]
		elif self.variable_buttons[2].text == "X":
			equation = SUVAT_EQUATIONS["SUAT"]
		elif self.variable_buttons[3].text == "X":
			equation = SUVAT_EQUATIONS["SUVT"]
		elif self.variable_buttons[4].text == "X":
			equation = SUVAT_EQUATIONS["SUVA"]
		else:
			raise UnkownUseCaseError("SUVAT equation")

		# Finds the unkown variable.
		unkown_variable = None
		for i, variable in enumerate(self.variable_buttons):
			if variable.text == "?":
				unkown_variable = SUVAT_vars[i]

		# Rearranges the equation.
		rearranged_equation = sympy.solve(equation, unkown_variable)
		if not self.show_plain_text:
			self.menu_buttons[3].text = sympy.pretty(equation)
			self.menu_buttons[3].text = self.menu_buttons[3].text.replace("─", " ", 2)
			if '\n' in self.menu_buttons[3].text:
				self.menu_buttons[3].text = "   " + self.menu_buttons[3].text 

			formatted_rearranged_equation = f"{unkown_variable} = {sympy.pretty(rearranged_equation[0])}"
		else:
			self.menu_buttons[3].text = equation
			formatted_rearranged_equation = f"{unkown_variable} = {rearranged_equation[0]}"


		self.menu_buttons[4].text = formatted_rearranged_equation
		
		# Substitutes in the values.
		sub_values = {}
		for i in range(5):
			if self.variable_buttons[i].text not in ["X", "?"]:
				if type(float(self.variable_buttons[i].text)) == float:
					sub_values[SUVAT_vars[i]] = float(self.variable_buttons[i].text)

		solution = sympy.simplify(rearranged_equation[0]).evalf(subs = sub_values)
		self.menu_buttons[5].text = f"Answer: {unkown_variable} = {solution:.2f} (2 d.p)"
		# Updates the 'Sovle' button's state as it should no longer be 'clicked'.
		self.menu_buttons[2].clicked = False
