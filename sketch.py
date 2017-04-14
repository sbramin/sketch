#!/usr/bin/env python3

import curses


def terminal_start():
    Stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

    if curses.has_colors():
        curses.start_color()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    return Stdscr


def terminal_end():
    curses.nocbreak()
    curses.echo()
    curses.curs_set(1)
    curses.endwin()


def main():
    stdscr = terminal_start()

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
            #command_frame.refresh()
            #command_frame.clear()
            command_frame.addstr("C ")
        elif c == curses.KEY_ENTER or c == 10 or c == 13:
            command_frame.addstr("ENTER ")
        elif c == ord('q') or c == ord('Q'):
            break

        stdscr.noutrefresh()
        outer_frame.noutrefresh()
        command_frame.noutrefresh()
        curses.doupdate()

    terminal_end()


if __name__ == "__main__":
    main()

