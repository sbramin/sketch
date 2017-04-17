#!/usr/bin/env python3
"""
@created 17/04/17
@author sbr

Sketch Pad app, who knew curses could be so fun.
"""

from curses import wrapper


class Pad(object):
    """ Sketch Pad

        A Pad keeps its size, what is drawn on it and contains the necessary methods
        to draw plus some validation.
    """

    def __init__(self, width=0, height=0):
        self.width = width
        self.height = height
        self.max_w = curses.COLS - 6
        self.max_h = curses.LINES - 8
        self.history = []
        self.maxyx = None
        self.frame = None

    def new(self, cmd):
        """ New Pad
        Returns a new Pad if size is within max size.
        """
        if self.height != 0 or self.width != 0:
            return self, "Pad already exists, quit to start again"
        try:
            self.width = int(cmd[1])
            self.height = int(cmd[2])
            if (self.width > self.max_w or self.height > self.max_h or
                    self.width < 2 or self.height < 2):
                self.width = 0
                self.height = 0
                return Pad(
                ), "Illegal pad size, pad must be between w:2-{} h:2-{}".format(
                    self.max_w, self.max_h)
            self.frame = curses.newwin(self.height + 2, self.width + 2, 4, 2)
            pos_y, pos_x = self.frame.getmaxyx()
            self.maxyx = [pos_y - 1, pos_x - 1]
            self.frame.box()
            self.frame.noutrefresh()
            curses.doupdate()
            return self, None

        except Exception as err:
            return Pad(), str(err)

    def not_ready(self):
        """ Checks Pad
        Checks if a Pad has already been started
        """
        return self.width == 0 or self.height == 0

    def validate_input(self, cmd):
        """ Input Validation
        Confirms if the entered cmd makes sense for the specific
        command issues, eg. r, l, b.
        """
        err = "Stay on the pad!"
        if self.not_ready():
            return None, None, None, None, "Cant start drawing until your pad's ready"
        try:
            if cmd[0].lower() in ['r', 'l']:
                pos_x1 = int(cmd[1])
                pos_y1 = int(cmd[2])
                pos_x2 = int(cmd[3])
                pos_y2 = int(cmd[4])

                if len(cmd) != 5:
                    return None, None, None, None, "Incorrect input, requires pos_x1, pos_y1, pos_x2, pos_y2"
                elif pos_x1 < 1 or pos_x1 >= self.maxyx[1] or pos_y1 < 1 or pos_y1 >= self.maxyx[0]:
                    return None, None, None, None, err
                elif pos_x2 < 1 or pos_x2 >= self.maxyx[1] or pos_y2 < 1 or pos_y2 >= self.maxyx[0]:
                    return None, None, None, None, err
                else:
                    return pos_x1, pos_y1, pos_x2, pos_y2, None

            elif cmd[0].lower() == 'b':
                pos_x1 = int(cmd[1])
                pos_y1 = int(cmd[2])
                colour = cmd[3]

                if len(cmd) != 4:
                    return None, None, None, None, "Incorrect input, required pos_x1, pos_y1, c"
                if pos_x1 < 1 or pos_x1 >= self.maxyx[1] or pos_y1 < 1 or pos_y1 >= self.maxyx[0]:
                    return None, None, None, None, err
                else:
                    return pos_x1, pos_y1, colour, None, None
        except Exception as err:
            return None, None, None, None, str(err)

    def draw(self, cmd):
        """ Draw Sorter
        Calls the correct drawer method based on the cmd specific.
        """
        opt = cmd[0].lower()
        if opt == 'l':
            return self.draw_line(cmd)
        elif opt == 'r':
            return self.draw_rectangle(cmd)
        elif opt == 'b':
            return self.draw_bucket(cmd)

    def draw_line(self, cmd):
        """Line Drawer
        Draws horizontal or vertical lines to the Pad frame.
        """
        pos_x1, pos_y1, pos_x2, pos_y2, err = self.validate_input(cmd)
        if err:
            return err
        elif (pos_y1 != pos_y2) and (pos_x1 != pos_x2):
            return "Thats not a horizontal or vertical line"
        elif pos_y1 == pos_y2:
            for pos_x in range(pos_x1, pos_x2 + 1):
                self.frame.addch(pos_y1, pos_x, 'X')
                self.frame.noutrefresh()
                self.history.append([pos_y1, pos_x])
        elif pos_x1 == pos_x2:
            for pos_y in range(pos_y1, pos_y2 + 1):
                self.frame.addch(pos_y, pos_x1, 'X')
                self.frame.noutrefresh()
                self.history.append([pos_y, pos_x1])

    def draw_rectangle(self, cmd):
        """Rectangle Drawer
        Draws rectangles to the Pad frame.
        """
        pos_x1, pos_y1, pos_x2, pos_y2, err = self.validate_input(cmd)
        if err:
            return err
        elif pos_x1 > pos_x2 or pos_y1 > pos_y2 or pos_x1 == pos_x2 or pos_y1 == pos_y2:
            return "pos_x2 and pos_y2 need to be larger than pos_x1 and pos_y1"

        for pos_x in range(pos_x1, pos_x2 + 1):
            self.frame.addch(pos_y1, pos_x, 'X')
            self.history.append([pos_y1, pos_x])
        for pos_y in range(pos_y1, pos_y2 + 1):
            self.frame.addch(pos_y, pos_x1, 'X')
            self.history.append([pos_y, pos_x1])
        for pos_x in range(pos_x1, pos_x2 + 1):
            self.frame.addch(pos_y2, pos_x, 'X')
            self.history.append([pos_y2, pos_x])
        for pos_y in range(pos_y1, pos_y2 + 1):
            self.frame.addch(pos_y, pos_x2, 'X')
            self.history.append([pos_y, pos_x2])
        self.frame.noutrefresh()

    def draw_bucket(self, cmd):
        """Draw Fill
        Fills the undrawn space with a specified colour.

        TODO: Start from a specific square, currently starts from 1,1
        TODO: Needs to handle more fill scenerios, not finished.
        """
        pos_x1, pos_y1, colour, _, err = self.validate_input(cmd)
        if err:
            return err
        pos_xs, pos_ys = [], []
        for pos_y in self.history:
            pos_ys.append(pos_y[0])
        for pos_x in self.history:
            pos_xs.append(pos_x[1])
        pos_x1, pos_y1 = 1, 1  # Need to remove this once function complete
        for pos_y in range(pos_x1, self.maxyx[0]):
            for pos_x in range(pos_y1, self.maxyx[1]):
                if [pos_y, pos_x] in self.history:
                    continue
                if pos_x in pos_xs and pos_y in pos_ys and [pos_y - 1, pos_x
                                                           ] in self.history:
                    self.history.append([pos_y, pos_x])
                    continue
                self.frame.addch(pos_y, pos_x, colour)
        self.frame.noutrefresh()


def sketch_setup(stdscr):
    """ Sketch Setup
    Setup Sketch app main frame and title

    """
    stdscr.addstr("Sketch Pad", curses.A_REVERSE)
    stdscr.chgat(-1, curses.A_REVERSE)
    stdscr.addstr(curses.LINES - 1, 0, "Enter Q to quit")
    stdscr.chgat(curses.LINES - 1, 7, 1, curses.A_BOLD | curses.color_pair(2))

    outer_frame = curses.newwin(curses.LINES - 2, curses.COLS, 1, 0)
    outer_frame.box()
    stdscr.noutrefresh()
    outer_frame.noutrefresh()
    curses.doupdate()


def sketch_print(frame, text):
    """ Sketch Printer
    Enables printing to the provided frame, causing the frame
    to clear before being printed to.
    """
    frame.refresh()
    frame.clear()
    frame.addstr(text)
    frame.noutrefresh()
    curses.doupdate()


def sketch_error(frame, prompt, err=""):
    """ Error Printer
    Uses sketch printer to printer errors to specific frame, if no
    error it uses the dafault error.
    """
    if err == "":
        err = "Invalid input please read README.md if you need help"
        sketch_print(frame, "{}{}.".format(prompt, err))
    else:
        sketch_print(frame, "{}Error: {}.".format(prompt, err))
    frame.getch()
    sketch_print(frame, prompt)


def sketch_input(pad):
    """ Sketch Input Control
    Handles main input into sketch app, doing minimal validation.
    """
    prompt = "Enter command: "
    input_frame = curses.newwin(2, curses.COLS - 4, 2, 2)
    curses.echo()
    sketch_print(input_frame, prompt)
    while True:
        c_input = input_frame.getstr()
        if len(c_input) > 1:
            cmd = c_input.decode("utf8").split()
            if cmd[0].lower() == 'c' and len(cmd) == 3:
                pad, err = pad.new(cmd)
                if err:
                    sketch_error(input_frame, prompt, err)
            elif len(cmd) == 5 or len(cmd) == 4:
                err = pad.draw(cmd)
                if err:
                    sketch_error(input_frame, prompt, err)
            else:
                sketch_error(input_frame, prompt)
        elif c_input == b'':
            sketch_print(input_frame, prompt)
        elif c_input == b'q' or c_input == b'Q':
            break
        else:
            sketch_error(input_frame, prompt)

        curses.doupdate()
    curses.noecho()


def main(stdscr):
    """ Sketch
    Sketch app is little like paint for the terminal.
    """
    sketch_setup(stdscr)
    pad = Pad()
    sketch_input(pad)


if __name__ == "__main__":
    wrapper(main)
