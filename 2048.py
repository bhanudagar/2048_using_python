from tkinter import Frame, Label, CENTER #frame and label are classes in tkinter and center is some justifying content

import Logics #our logics file
import constants as c #our constants file


class Game2048(Frame): #Inherited from Frame class, super class is Frame. # Frame lets us build a box type of thing.
	# out game2048 class will inherit all the functions and properties of class Frame.
	def __init__(self): #constructor, it needs an object of game2048 class to work upon.

		Frame.__init__(self)

		self.grid() # tkinter has a grid manager which allow us to create all the widgets in the form of grid. Our frame will look like a grid.
		# till here, a grid frame is created.

		self.master.title('2048') #everything in Frame class has a master. Since, we ourselves are a Frame, our master here will be the boundary of our frame.
								# so it's title will be 2048

		self.master.bind("<Key>", self.key_down) # this frame that we created is binded i.e., whatever happens in this frame i.e., whenever any key is pressed,
								#I will go to this self.key_down function that is implemented later on in the code.

		self.commands = {c.KEY_UP: Logics.move_up, c.KEY_DOWN: Logics.move_down,
						c.KEY_LEFT: Logics.move_left, c.KEY_RIGHT: Logics.move_right
						}


		self.grid_cells = [] # there will be some cells in the grid. Initially, they will be empty.

		self.init_grid() #the grid is created. It will be initialized by this function. It will add the grid cells in the grid.

		self.init_matrix() # It basically initializes the game.

		self.update_grid_cells() # initially all the grid cells had 0,0,0,.... but if 2 has come, its background color and text color needs to be changed.
								# It makes changes on the UI. Whenever a new movement occurs, we have to call update_grid_cells to make new changes in UI.

		self.mainloop() #it actually runs the program. It means our frame is ready. Run our program.



	# Now we will implement our one of the main functionalities. That is, initialising our grid.
	def init_grid(self):
		background = Frame(self, bg = c.BACKGROUND_COLOR_GAME, # this creates a frame. Frame is a type of widget. bg color is selected as above.
							width = c.SIZE, height = c.SIZE)

		background.grid()

		for i in range(c.GRID_LEN):
			grid_row = [] # each row of grid will have something.
			for j in range(c.GRID_LEN):
				cell = Frame(background, bg = c.BACKGROUND_COLOR_CELL_EMPTY,
							width = c.SIZE / c.GRID_LEN,
							height = c.SIZE / c.GRID_LEN)

				cell.grid(row = i, column = j, padx = c.GRID_PADDING,
							pady = c.GRID_PADDING)
				# we have created a widget label and visualised it as a grid. this label will actually cover the blocks in the grid.
				# LABELS WILL BE AS FOLLOWS -> 
				#[L1,L2,L3,L4],[L5,L6,L7,L8],[....],[....]
				# WE WILL MAKE CHANGES TO THE LABEL AND THEN THE CELL WILL CHANGE.
				t = Label(master = cell, text = "",
							bg = c.BACKGROUND_COLOR_CELL_EMPTY,
							justify = CENTER, font = c.FONT, width = 5, height = 2)

				t.grid()
				grid_row.append(t)

			self.grid_cells.append(grid_row)


	def init_matrix(self): #it will just create a matrix. our UI part is created. We will now internally create a matrix.
		self.matrix = Logics.start_game()
		Logics.add_new_two(self.matrix)
		Logics.add_new_two(self.matrix)


	def update_grid_cells(self):
		for i in range(c.GRID_LEN):
			for j in range(c.GRID_LEN): #it will create a matrix equal to grid length -> [L1,l2,l3,l4],[l5,...]..
				new_number = self.matrix[i][j]

				if new_number == 0: #if there is no number on current position,
					self.grid_cells[i][j].configure(
						text = "", bg = c.BACKGROUND_COLOR_CELL_EMPTY)
				
				else:
					self.grid_cells[i][j].configure(text = str(new_number),
						bg = c.BACKGROUND_COLOR_DICT[new_number],
						fg = c.CELL_COLOR_DICT[new_number])

		self.update_idletasks() #update_idletask is in frame library. when we're changing the color, it can take some time, it will wait till all the colors are done

# what happens when we press a key
	def key_down(self, event):
		key = repr(event.char) # it gives you the key pressed.

		if key in self.commands:
			self.matrix, changed = self.commands[repr(event.char)](self.matrix) # this is calling self matrix. tht means we already 

			if changed:
				Logics.add_new_two(self.matrix)
				self.update_grid_cells()

				changed = False

				if Logics.get_current_state(self.matrix) == 'WON':
					self.grid_cells[1][1].configure(
							text = "You", bg = c.BACKGROUND_COLOR_CELL_EMPTY)
					self.grid_cells[1][2].configure(
							text = "Win!", bg = c.BACKGROUND_COLOR_CELL_EMPTY)

				if Logics.get_current_state(self.matrix) == 'LOST':
					self.grid_cells[1][1].configure(
							text = "You", bg = c.BACKGROUND_COLOR_CELL_EMPTY)
					self.grid_cells[1][2].configure(
							text = "Lose!", bg = c.BACKGROUND_COLOR_CELL_EMPTY)



gamegrid = Game2048()