import curses
from curses import COLOR_BLACK, COLOR_GREEN, COLOR_RED, COLOR_WHITE, wrapper
from this import d
from time import time
from tracemalloc import start
import time
import random


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(1, 1, "Welcome to the speed typing test!\n Press any key to begin : ", curses.color_pair(3))  # row,column,text,color format
    stdscr.refresh()
    stdscr.getkey()


def diplay_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target, curses.color_pair(3))
    stdscr.addstr(1, 0, f" WPM : {wpm}")
    for i, ch in enumerate(current):
        if(target[i] == ch):
            stdscr.addstr(0, i, ch, curses.color_pair(1))
        else:
            if(ch == " "):
                ch = "_"
            stdscr.addstr(0, i, ch, curses.color_pair(2))


def load_text():
    with open("sample.txt","r") as f:
        lines = f.readlines()
        return random.choice(lines).strip() #To remove the trailing white space characters at the beginning or end. eg: \n


def wpm_test(stdscr):

    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)  # To update wpm if used does not enter anything

    while True:
        if(current_text==[]):
            start_time = time.time() #To enable used to clear everything and start again
        time_elapsed = max(1, time.time()-start_time)
        # if(time_elapsed!=0):
        lpm = (len(current_text)/time_elapsed)*60
        word_length = 5  # We are assuming this
        # I don't know whether going to calculate the exact average word legnth of the current_text
        # and wasting time would be more beneficial to calculate the exact wpm
        wpm = round(lpm / word_length)
        stdscr.clear()
        diplay_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False) #We are using a getkey in main function
            break

        try:
            letter = stdscr.getkey()  # To not crash due to nodelay function called above
        except:
            continue  # We want to skip rest of the code as no character is entered
        if ord(letter) == 27:  # ASCII
            break
        
        # if ord(letter) == 8:  # backspace
        if letter in ("KEY_BACKSPACE","\b","\x7f"): #This is a better way to check for backspace considering different operating systems
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(letter)
        stdscr.refresh()


def main(stdscr):
    curses.init_pair(1, COLOR_GREEN, COLOR_BLACK)
    curses.init_pair(2, COLOR_RED, COLOR_BLACK)
    curses.init_pair(3, COLOR_WHITE, COLOR_BLACK)
    while True:
        start_screen(stdscr)
        wpm_test(stdscr)
        stdscr.addstr( 2, 0, "You completed the test!\nPress any key to continue or Esc to exit")
        x = stdscr.getkey()
        if ord(x) == 27:
            break;

wrapper(main)
