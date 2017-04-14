#!/usr/bin/env python3

import curses


def main(stdscr):
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    stdscr.addstr("Sketch Pad", curses.A_REVERSE)
    stdscr.chgat(-1, curses.A_REVERSE)

    stdscr.addstr(curses.LINES-1, 0, "Press Q to quit")

    stdscr.chgat(curses.LINES-1, 7, 1, curses.A_BOLD | curses.color_pair(2))

    outer_frame = curses.newwin(curses.LINES-2, curses.COLS, 1,0)

    command_frame = outer_frame.subwin(curses.LINES-6, curses.COLS-4, 3, 2)

    command_frame.addstr("Enter command: ")

    outer_frame.box()

    stdscr.noutrefresh()
    outer_frame.noutrefresh()

    curses.doupdate()

    while True:
        c = outer_frame.getch()
        if c == ord('c') or c == ord('C'):
           command_frame.addstr("Text appears!")
        elif c == ord('q') or c == ord('Q'):
            break

        stdscr.noutrefresh()
        outer_frame.noutrefresh()
        command_frame.noutrefresh()
        curses.doupdate()

    curses.nocbreak()
    curses.echo()
    curses.curs_set(1)
    curses.endwin()


if __name__ == "__main__":
    main(curses.initscr())

