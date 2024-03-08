"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Eetu Petänen
Opiskelijanumero: 151082922
eetu.petanen@gmail.com
11.12.2023

A program with an advanced UI using the tkinter library.
The advanced components include a menu and styled entry fields. Entry fields are created in a for loop.

The program is a simple and fun number game I decided to call Skipp-5.

The rules of the game are simple.
The game is played on a 5x5 board. The goal of the game is to fill the board with numbers 1-25.
Start the game by entering the number 1 in ANY square you want.

Each move must satisfy the following three conditions:
1. Each entry must be 1 larger than the previous.
2. When moving horizontally or vertically skip over 2 squares.
3. When moving diagonally skip over 1 square.

The user is given visual feedback based on the value entered. Only the squares of the possible moves are enabled.

The rules of the game are found in the menu under Help --> Rules
"""

import tkinter as tk
from tkinter import ttk  # Import ttk for themed widgets


class SkippApp:

    def __init__(self, root, size):
        self.highscore = None
        self.info = None
        self.root = root
        self.menubar = tk.Menu(self.root)  # Initialize a menubar
        self.last_entry_location = None
        self.current_entry_location = None
        self.entry_grid = None
        self.highscore_val = 0

        self.root.title("Skipp-5")

        self.size = size

        self.frames = {}  # A dictionary to store all the frames(pages) of the program

        # Create all the pages
        self.create_main_frame()
        self.create_help_frame()
        self.create_about_frame()

        self.open_from_file()  # Read a highscore from a file, if exists
        self.show_frame("Main")  # Set the page to the Main page

    def create_main_frame(self):
        """
        A method to create the main page.
        The main page creates the playing grid and handles the different menus

        """
        main_frame = ttk.Frame(self.root)  # ttk.Frame creates a new page
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.entry_grid, self.current_entry_location = self.create_grid(main_frame)

        self.last_input = 0

        # Create the menu "file"
        filemenu = tk.Menu(self.menubar, tearoff=0)

        # Add submenus
        filemenu.add_command(label="New Game", command=self.new_game)
        filemenu.add_command(label="Save", command=self.save_to_file)
        filemenu.add_command(label="Close")

        filemenu.add_separator()  # Creates a separator in the menu

        filemenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

        # Create the menu "Help"
        helpmenu = tk.Menu(self.menubar, tearoff=0)

        # Create submenus
        helpmenu.add_command(label="Rules", command=lambda: self.show_frame("Help"))
        helpmenu.add_command(label="About...", command=lambda: self.show_frame("About"))
        self.menubar.add_cascade(label="Help", menu=helpmenu)

        #  Create a custom style for the labels
        style = ttk.Style()
        style.configure("TLabel", padding=5, font=('Arial', 10))

        #  Create a label component for the highscore
        self.highscore = ttk.Label(self.root, text="Highscore: 0", style="TLabel", width=14)
        self.highscore.grid(row=6, column=0)

        #  Create a label component for the info text
        #  Used to display info messages to the player on error
        self.info = ttk.Label(self.root, text="", style="TLabel")
        self.info.grid(row=7, column=0)

        # Bind keyboard shortcuts to different commands
        self.root.bind('<Control-n>', self.new_game)
        self.root.bind('<Control-s>', self.save_to_file)

        # Add the main frame to the frames dictionary
        self.frames["Main"] = main_frame

    def create_help_frame(self):
        """
        A method to create the help page.

        The method creates a new ttk frame that acts as a page.

        """

        help_frame = ttk.Frame(self.root)
        help_frame.grid(row=0, column=0, sticky="nsew")

        #  Create a tinker Text widget
        help_text = tk.Text(help_frame, wrap=tk.WORD, height=10, width=50)
        help_text.pack(padx=10, pady=10)

        # Rules of the game
        help_text.insert(tk.END, "Skipp-5\n\nSkipp-5 is a simple and fun number game played on a 5x5 board. "
                                 "The goal of the game is to fill the board with numbers 1-25."
                                 "\n\nStart the game by entering the "
                                 "number 1 in ANY square you want.\n\nEach move must satisfy the"
                                 "following three conditions:\n1. Each entry must be 1 larger than the previous.\n2. "
                                 "When moving horizontally or vertically skip over 2 squares.\n3. When moving "
                                 "diagonally skip over 1 square.")

        # Button to return to the main page (frame="Main")
        back_button = ttk.Button(help_frame, text="Back to The Game", command=lambda: self.show_frame("Main"))
        back_button.pack(pady=10)

        # Add the help frame to the frames dictionary
        self.frames["Help"] = help_frame

    def create_about_frame(self):
        """

        A method to create the about page.

        The method creates a new ttk frame that acts as a page.
        """

        about_frame = ttk.Frame(self.root)
        about_frame.grid(row=0, column=0, sticky="nsew")

        #  Create a tinker Text widget to hold the about info
        about_text = tk.Text(about_frame, wrap=tk.WORD, height=10, width=50)
        about_text.pack(padx=10, pady=10)

        #  Credits
        about_text.insert(tk.END, "Skipp-5\n\nA fun and simple number game\nCreated by:\nEetu Petänen")

        # Button to return to the main page (frame="Main")
        back_button = ttk.Button(about_frame, text="Back to The Game", command=lambda: self.show_frame("Main"))
        back_button.pack(pady=10)

        # Add the help frame to the frames dictionary
        self.frames["About"] = about_frame

    def show_frame(self, page_name):
        """
        A method to set the current frame(page) shown

        :param page_name: string
        :return: None
        """

        # Hide all frames
        for frame in self.frames.values():
            frame.grid_remove()

        # Show the chosen frame
        self.frames[page_name].grid(row=0, column=0, sticky="nsew")

    def new_game(self, event=None):
        """
        A method to create a new game.
        Accessible by CTRL+n
        :param event: This is required to handle keyboard shortcut events.
        :return: None
        """

        self.last_input = 0  # Sets the last input back to 0
        self.entry_grid, self.current_entry_location = self.create_grid(self.frames["Main"])  # Creates an empty grid

    def save_to_file(self, event=None):
        """
        A method to save the highscore to a file
        :param event: This is required to handle keyboard shortcut events.
        :return: None
        """

        filename = "skipp5.txt"
        try:
            save_file = open(filename, mode="w")
            save_file.write(str(self.highscore_val))  # Write the high score to the file

        except OSError:
            print(f"Error: opening the file '{filename}' failed!")
            return

    def open_from_file(self):
        """
        A method to read the highscore from a file if it exists.
        :return: None
        """

        filename = "skipp5.txt"
        highscore = 0
        try:
            save_file = open(filename, mode="r")

        #  If a previous high score file doesn't exist, return
        except FileNotFoundError:
            return

        #  If the high score file fails to open
        except OSError:
            print(f"Error: opening the file '{filename}' failed!")
            return

        for line in save_file:
            highscore = int(line)

        # If the score read from the high score file is greater than the current score, set the high score. This is
        # future proofing for situations where a file might be opened in other events than the start of the program
        prev_score = int(self.highscore["text"].rstrip().split(":")[1])
        if highscore > prev_score:
            self.highscore_val = highscore
            self.highscore["text"] = f"Highscore: {highscore}"

    def create_grid(self, parent_frame):
        """
        Create the 5x5 grid of styled tkinter Entry widgets
        :param parent_frame: string. The frame (page) where to create.
        :return: entry_list, current_entry_location
        """

        entry_list = []
        current_entry_location = [0, 0]  # Initialize with the first entry

        def update_current_location(event, row, col):
            """
            A method to set the location of the number entered by the player.
            The playing grid has rows and columns with indexes 0-4.

            :param event:
            :param row: int
            :param col: int
            :return: None
            """
            current_entry_location[0] = row
            current_entry_location[1] = col

        def on_key_release(event, row, col):
            """
            A method to handle submitting a number in an Entry field. A number is submitted by pressing the spacebar
            or the Enter key. This enables the player to input values with two digits

            :param event: A keyboard event
            :param i:
            :param j:
            :return:
            """

            input_value = self.entry_grid[row][col].get()  # Get the number entered by the player
            if event.char in (' ', '\r'):  # Check for space bar or enter key

                # Check if the value entered by the player is 1 greater than the previous value
                try:
                    if int(input_value) == self.last_input + 1:
                        self.info["text"] = ""
                        self.last_input = int(input_value)  # A variable to track the last value
                        self.update_possible_moves()  # Calculate the possible locations for the next moves
                        self.last_entry_location = [row, col]  # A variable to track the coordinates of the last entry
                    else:
                        self.info["text"] = "Value must be 1 greater than the previous"

                # If the entered value isn't a number 1 greater than the previous value
                # give visual feedback to the player
                except ValueError:
                    self.info["text"] = "Value must be 1 greater than the previous"

        #  Create a custom style for the tkinter Entry widgets
        style = ttk.Style()
        style.configure("TEntry", padding=5, relief="flat", background="#edf2f7", font=('Arial', 14))

        #  Create the entry widgets in a for loop
        #  Each entry widgets is placed on a grid at position [x,y].
        #  Each entry has two event handlers bound to it, for handling keyboard events (spacebar/Enter)
        for x in range(self.size):
            row = []
            for y in range(self.size):
                entry = ttk.Entry(parent_frame, style="TEntry", width=8, justify="center")
                entry.grid(row=x, column=y, padx=2, pady=2)
                entry.bind("<FocusIn>", lambda event, x=x, y=y: update_current_location(event, x, y))
                entry.bind("<KeyRelease>", lambda event, x=x, y=y: on_key_release(event, x, y))
                row.append(entry)
            entry_list.append(row)

        return entry_list, current_entry_location

    def update_possible_moves(self):

        """

        A method to calculate the possible moves based on the player's last entry. The entry fields that satisfy the
        rules of the game are given the state "normal" and all the other entry fields are set to disabled state.

        :return: None
        """

        all_entries_disabled = True  # A boolean to track whether all entries have state "disabled"

        for x in range(self.size):  # Loop through rows
            for y in range(self.size):  # Loop through columns
                entry = self.entry_grid[x][y]  # The entry field at coordinates [x,y]

                #  If the entry field satisfies the rules of the game set state to "normal",
                #  otherwise set state to "disabled"
                entry_state = "normal" if self.is_valid_move(entry, x, y) else "disabled"
                entry["state"] = entry_state

                # Check if any entry is still enabled
                if entry_state == "normal":
                    all_entries_disabled = False

        # If all entries on the grid have state "disabled"
        if all_entries_disabled:
            prev_score = int(self.highscore["text"].rstrip().split(":")[1])  # Get the previous high score
            current_score = int(self.entry_grid[self.last_entry_location[0]][self.last_entry_location[1]].get()) + 1

            if current_score > prev_score:
                self.highscore_val = current_score
                self.highscore["text"] = f"Highscore: {current_score}"
            self.save_to_file()   # Save the highscore to file skipp5.txt

    def is_valid_move(self, entry, row, col):
        """
        A method to check if the move is valid based on the rules of the game.
        Each move must satisfy the following three conditions:
        1. Each entry must be 1 larger than the previous.
        2. When moving horizontally or vertically skip over 2 squares.
        3. When moving diagonally skip over 1 square.

        This method is concerned with conditions 2 and 3.

        :param entry: The tk Entry field at coordinates [x,y]
        :param row: int
        :param col: int
        :return: True/False
        """

        last_row, last_col = self.current_entry_location

        # Calculate the horizontal distance of a given row when compared to the player's last input
        row_diff = abs(row - last_row)

        # Calculate the vertical distance of a given row when compared to the player's last input
        col_diff = abs(col - last_col)

        # If a number has already been inputted to the entry field, it isn't a valid space moving forward
        if any(char.isdigit() for char in entry.get()):
            return False

        #  Return True for entries with a horizontal or vertical distance of 3 or a diagonal distance of 2.
        #  The grid contains rows and columns with indices 0-4.
        #  E.g.1. The Entry field at [0,3] is at a horizontal distance of 3-0=3 from the Entry field [0,0].
        #  Therefore, 2 squares are skipped.
        #
        #  E.g.2. The Entry field at [2,2] is at a horizontal distance of 2-0=2 and a vertical distance of 2-0=2
        #  from the entry field [0,0] thus giving a diagonal distance of 2. Therefore, 1 square is skipped.

        return (row_diff == 3 and col_diff == 0) or (row_diff == 0 and col_diff == 3) or (
                row_diff == 2 and col_diff == 2)


def main():
    root = tk.Tk()
    # The size of the grid isn't hard coded. The game is typically played on a 5x5 board, but other sizes are possible
    app = SkippApp(root, size=5)
    root.config(menu=app.menubar)   # Initialize the menubar
    root.iconbitmap("Skipp5.ico")   # Set a custom icon for the program
    root.mainloop()


if __name__ == "__main__":
    main()
