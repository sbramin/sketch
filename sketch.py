#!/usr/bin/env python3

import curses


class Pad(object):
    def __init__(self, w=0, h=0):
        self.w = w
        self.h = h
        self.max_w = curses.COLS - 6
        self.max_h = curses.LINES - 8

    def new(self, cmd):
        if self.h != 0 or self.w != 0:
            return self, "Pad already exists, focus on your drawing or quit to start again"
        try:
            self.w = int(cmd[1])
            self.h = int(cmd[2])
            if self.w > self.max_w or self.h > self.max_h or self.w < 2 or self.h < 2:
                self.w = 0
                self.h = 0
                return Pad(), "Illegal pad size, pad must be between w:2-{} h:2-{}".format(
                    self.max_w, self.max_h)
            self.frame = curses.newwin(self.h+2, self.w+2, 4, 2)
            self.maxyx = self.frame.getmaxyx()
            self.frame.box()
            self.frame.noutrefresh()
            curses.doupdate()
            return self, None

        except Exception as err:
            return Pad(), str(err)

    def not_ready(self):
        if self.w == 0 or self.h == 0:
            return True
        else:
            return False

    def frame(self):
        return self.frame

    def validate_input(self, cmd):
        if self.not_ready():
            return None, None, None, None, "Cant start drawing until your pad's ready"
        try:
            x1 = int(cmd[1])
            y1 = int(cmd[2])
            x2 = int(cmd[3])
            y2 = int(cmd[4])

            err = "Stay on the pad!"
            if x1 < 1 or x1 >= self.maxyx[1]-1 or y1 < 1 or y1 >= self.maxyx[0]-1:
                return None, None, None, None, err
            elif x2 < 1 or x2 >= self.maxyx[1]-1 or y2 < 1 or y2 >= self.maxyx[0]-1:
                return None, None, None, None, err
            else:
                return x1, y1, x2, y2, None
        except Exception as err:
            return None, None, None, None, str(err)

    def draw(self, cmd):
        opt = cmd[0].lower()
        if opt == 'l':
            return self.draw_line(cmd)
        elif opt == 'r':
            return self.draw_rectangle(cmd)
        elif opt == 'b':
            return self.draw_bucket(cmd)
        pass


    def draw_line(self, cmd):
        x1, y1, x2, y2, err = self.validate_input(cmd)
        if err:
            return err
        elif (y1 != y2) and (x1 != x2):
            return "Thats not a horizontal or vertical line"
        elif y1 == y2:
            for x in range(x1,x2+1):
                self.frame.addch(y1, x, 'X')
                self.frame.noutrefresh()
        elif x1 == x2:
            for y in range(y1,y2+1):
                self.frame.addch(y, x1, 'X')
                self.frame.noutrefresh()

    def draw_rectangle(self, cmd):
        x1, y1, x2, y2, err = self.validate_input(cmd)
        if err:
            return err
        elif x1 > x2 or y1 > y2 or x1 == x2 or y1 == y2:
            return "x2 and y2 need to be larger than x1 and y1"

        for x in range(x1,x2+1):
            self.frame.addch(y1, x, 'X')
        for y in range(y1,y2+1):
            self.frame.addch(y, x1, 'X')
        for x in range(x1,x2+1):
            self.frame.addch(y2, x, 'X')
        for y in range(y1,y2+1):
            self.frame.addch(y, x2, 'X')
        self.frame.noutrefresh()

    def draw_bucket(self, cmd):
        x1, y1, x2, y2, err = self.validate_input(cmd)
        if err:
            return err


def sketch_setup(stdscr):
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
    frame.refresh()
    frame.clear()
    frame.addstr(text)
    frame.noutrefresh()
    curses.doupdate()


def sketch_error(frame, prompt, err=""):
    if err == "":
        err = "Invalid input please read README.md if you need help"
        sketch_print(frame, "{}{}.".format(prompt, err))
    else:
        sketch_print(frame, "{}Error: {}.".format(prompt, err))
    frame.getch()
    sketch_print(frame, prompt)


def sketch_input(pad):
    prompt = "Enter command: "
    input_frame = curses.newwin(2, curses.COLS - 4, 2, 2)
    curses.echo()
    sketch_print(input_frame, prompt)
    while True:
        c = input_frame.getstr()
        if len(c) > 1:
            cmd = c.decode("utf8").split()
            if cmd[0].lower() == 'c' and len(cmd) == 3:
                pad, err = pad.new(cmd)
                if err:
                    sketch_error(input_frame, prompt, err)
            elif len(cmd) == 5:
                err = pad.draw(cmd)
                if err:
                    sketch_error(input_frame, prompt, err)
            else:
                sketch_error(input_frame, prompt)
        elif c == b'':
            sketch_print(input_frame, prompt)
        elif c == b'q' or c == b'Q':
            break
        else:
            sketch_error(input_frame, prompt)

        curses.doupdate()
    curses.noecho()


def main(stdscr):
    sketch_setup(stdscr)
    pad = Pad()
    sketch_input(pad)


if __name__ == "__main__":
    curses.wrapper(main)
