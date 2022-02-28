import curses
from Simulation import *
from threading import Thread
from Control import *


def display_main():
    stdscr = curses.initscr()
    curses.noecho()
    stdscr.nodelay(True)
    stdscr.addstr(1, 25, '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>system runing<<<<<<<<<<<<<<<<<<<<<<<<<<', curses.A_REVERSE)
    stdscr.refresh()
    while 1:
        s_line = 3
        for i in Gyro.client_index:
            exec(
                "stdscr.addstr(s_line, 25, 'gyro {0} roll:'+str(round(gyro_{0}.roll, 2)) + '   ', curses.A_REVERSE)".format(
                    i))
            exec(
                "stdscr.addstr(s_line, 50, 'gyro {0} row:'+str(round(gyro_{0}.yaw, 2)) + '   ', curses.A_REVERSE)".format(
                    i))
            exec(
                "stdscr.addstr(s_line, 75, 'gyro {0} pitch:'+str(round(gyro_{0}.pitch, 2)) + '   ', curses.A_REVERSE)".format(
                    i))
            s_line = s_line + 2

        time.sleep(0.1)
        c = stdscr.getch()

        if c == ord('b'):
            break

        if c == ord('s'):
            break

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.noecho()
    stdscr.nodelay(True)

    stdscr.addstr(3, 25, 'gyro {0} roll:' + '135.11', curses.A_REVERSE)
    stdscr.refresh()

    time.sleep(1)
    stdscr.addstr(3, 25, 'gyro {0} roll:' + '0.01  ', curses.A_REVERSE)
    stdscr.refresh()

    while 1:

        c = stdscr.getch()

        if c == ord('b'):
            break
