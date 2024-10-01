import curses
from curses import wrapper
import time
import random
import textwrap  # Used for wrapping text to fit the terminal width
import os  # Import os module to handle file paths

def start_screen(stdscr):
    """
    Displays the welcome screen and waits for the user to press any key to begin.
    """
    stdscr.clear()
    stdscr.addstr("Welcome to the speed typing test!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()
            
def display_text(stdscr, target, current, wpm=0):
    """
    Displays the target text, user's current input, and the WPM on the screen.
    Highlights correct and incorrect characters.
    """
    stdscr.clear()
    stdscr.addstr(0, 0, f"WPM: {wpm}\n\n")  # Display WPM at the top

    # Get the height and width of the terminal window
    h, w = stdscr.getmaxyx()
    
    # Replace any newlines in the target text with spaces
    target_text_no_newlines = target.replace('\n', ' ').replace('\r', '')

    # Wrap the target text so it fits within the terminal width
    target_lines = textwrap.wrap(target_text_no_newlines, w)

    # Display the target text line by line starting from line index 2
    for idx, line in enumerate(target_lines):
        stdscr.addstr(idx + 2, 0, line, curses.color_pair(3))

    # Convert the current text list to a string
    current_str = ''.join(current)

    # Display the user's input with correct coloring
    cursor_y = 2  # Start displaying input from line 2
    cursor_x = 0  # Start at the first column
    for i, char in enumerate(current_str):
        if i < len(target_text_no_newlines):
            correct_char = target_text_no_newlines[i]
            if char == correct_char:
                color = curses.color_pair(1)  # Green for correct characters
            else:
                color = curses.color_pair(2)  # Red for incorrect characters
        else:
            color = curses.color_pair(2)  # Red for extra characters

        # Move to the next line if at the end of the screen width
        if cursor_x >= w:
            cursor_x = 0
            cursor_y += 1

        # Display the character with the appropriate color
        stdscr.addch(cursor_y, cursor_x, char, color)
        cursor_x += 1  # Move to the next column

def load_text():
    """
    Loads text from 'text.txt', splits it into paragraphs, and returns a random paragraph.
    Returns:
    - A randomly selected paragraph from the text file as a string.
    """
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Build the full path to the text.txt file
    text_file_path = os.path.join(script_dir, 'text.txt')
    
    with open(text_file_path, "r", encoding='utf-8') as f:
        content = f.read()
        # Split the content into paragraphs using double newlines as the delimiter
        paragraphs = content.split('\n\n')
        # Clean up each paragraph by replacing single newlines with spaces and stripping whitespace
        paragraphs = [p.replace('\n', ' ').strip() for p in paragraphs if p.strip()]
        return random.choice(paragraphs)  # Return a random paragraph

def wpm_test(stdscr):
    """
    Runs the main typing test loop, capturing user input and calculating WPM.
    """
    target_text = load_text()  # Load a random paragraph
    current_text = []  # List to store user's input characters
    wpm = 0
    start_time = time.time()  # Record the start time
    stdscr.nodelay(True)  # Set getkey() to be non-blocking

    while True:
        time_elapsed = max(time.time() - start_time, 1)  # Ensure time_elapsed is at least 1
        # Calculate WPM: total characters typed divided by 5 (average word length), adjusted for time
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        # Check if the user has finished typing the target text
        target_text_no_newlines = target_text.replace('\n', ' ').replace('\r', '')
        if ''.join(current_text) == target_text_no_newlines:
            stdscr.nodelay(False)  # Stop non-blocking mode
            break  # Exit the typing loop

        try:
            key = stdscr.getkey()
        except:
            continue  # No input was received, continue the loop

        if ord(key) == 27:  # If the Escape key is pressed
            break  # Exit the typing loop

        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if current_text:
                current_text.pop()  # Remove the last character from current_text
        elif len(current_text) < len(target_text_no_newlines):
            current_text.append(key)  # Add the pressed key to current_text

def main(stdscr):
    """
    Initializes the curses application and starts the typing test.
    """
    # Turn off cursor blinking
    curses.curs_set(0)

    # Initialize color pairs for text coloring
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Correct input (Green)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Incorrect input (Red)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Default text (White)

    start_screen(stdscr)  # Display the welcome screen
    while True:
        wpm_test(stdscr)  # Start the typing test

        stdscr.addstr(0, 0, "You completed the text! Press any key to continue or ESC to exit...")
        key = stdscr.getkey()
        if ord(key) == 27:  # If the Escape key is pressed
            break  # Exit the program

wrapper(main)  # Start the curses application
