#!/usr/bin/env python3

from logging import debug
import curses
from time import sleep


def logging_level(level, name):
    """Log Level

    Sets the logging level for the app that calls it.

    Args:
        level (str): info, debug, warning
        name (str): name of the app, results in name.log

    Example:
        debug logging for nods::

            logging_level("debug", "nods")

    Returns:
       None
    """
    from logging import basicConfig, getLogger, INFO, DEBUG, WARNING
    from os import makedirs
    from os.path import join, exists

    dataDir = './'
    logDir = join(dataDir, 'log')
    logFile = join(logDir, (name + '.log'))
    exists(logDir) or makedirs(logDir)

    if level == "info":
        basicConfig(
            datefmt='%Y-%m-%d %H:%M:%S',
            format='%(asctime)s %(levelname)s %(message)s',
            filename=logFile,
            level=INFO)
        getLogger("paramiko").setLevel(INFO)
    elif level == "warning":
        basicConfig(
            datefmt='%Y-%m-%d %H:%M:%S',
            format='%(asctime)s %(levelname)s %(message)s',
            filename=logFile,
            level=WARNING)
        getLogger("paramiko").setLevel(WARNING)
    else:
        basicConfig(
            datefmt='%Y-%m-%d %H:%M:%S',
            format='%(asctime)s %(levelname)s %(message)s',
            filename=logFile,
            level=DEBUG)
        getLogger("paramiko").setLevel(DEBUG)


def sketch_setup():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    if curses.has_colors():
        curses.start_color()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

    stdscr.addstr("Sketch Pad", curses.A_REVERSE)
    stdscr.chgat(-1, curses.A_REVERSE)
    stdscr.addstr(curses.LINES-1, 0, "Enter Q to quit")
    stdscr.chgat(curses.LINES-1, 7, 1, curses.A_BOLD | curses.color_pair(2))

    outer_frame = curses.newwin(curses.LINES-2, curses.COLS, 1,0)

    command_frame = outer_frame.subwin(curses.LINES-6, curses.COLS-4, 3, 2)
    command_frame.addstr("Enter command: ")

    outer_frame.box()
    stdscr.noutrefresh()
    outer_frame.noutrefresh()
    curses.doupdate()

    return command_frame


def sketch_teardown():
    curses.nocbreak()
    curses.echo()
    curses.curs_set(1)
    curses.endwin()


def sketch_print(frame, text):
    frame.refresh()
    frame.clear()
    frame.addstr(text)
    frame.noutrefresh()
    curses.doupdate()




def sketch_error(frame, prompt, err=""):
    sketch_print(frame, "{}Error: Invalid input, try again. {}".format(prompt, err))
    sleep(3)
    sketch_print(frame, prompt)


def sketch_input(command_frame):
    prompt = "Enter command: "
    curses.echo()
    while True:
        sketch_print(command_frame, prompt)
        c = command_frame.getstr()
        debug(c)
        if len(c) > 1:
            cmd = c.decode("utf8").split()
            debug(cmd)
            if len(cmd) < 3:
                sketch_error(command_frame, prompt)
        elif c == b'q' or c == b'Q':
            break
        else:
            sketch_error(command_frame, prompt)

        curses.doupdate()
    curses.noecho()

    """
    if c == ord('c') or c == ord('C')
        #command_frame.refresh()
        #command_frame.clear()
        sketch_frame.addstr("C ")
    elif c == curses.KEY_ENTER or c == 10 or c == 13:
        sketch_frame.addstr("ENTER ")
    elif c == ord('q') or c == ord('Q'):
        break
    """





def main():
    logging_level('debug', 'sketch')
    main_frame = sketch_setup()
    sketch_input(main_frame)
    sketch_teardown()


if __name__ == "__main__":
    main()

