import curses
from Control import *
from Simulation import *
from threading import Thread

def display_main():
    stdscr = curses.initscr()
    curses.noecho()
    stdscr.nodelay(True)
    stdscr.addstr(1, 25, '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>system runing<<<<<<<<<<<<<<<<<<<<<<<<<<', curses.A_REVERSE)
    stdscr.refresh()
    while 1:
        s_line = 3
        for i in Gyro.client_index:
            exec("stdscr.addstr(s_line, 25, 'gyro {0} roll:'+str(round(gyro_{0}.roll, 2)), curses.A_REVERSE)".format(i))
            exec("stdscr.addstr(s_line, 50, 'gyro {0} row:'+str(round(gyro_{0}.yaw, 2)), curses.A_REVERSE)".format(i))
            exec("stdscr.addstr(s_line, 75, 'gyro {0} pitch:'+str(round(gyro_{0}.pitch, 2)), curses.A_REVERSE)".format(i))
            s_line = s_line + 2

        time.sleep(0.1)
        c = stdscr.getch()

        if c == ord('b'):
            break

        if c == ord('s'):
            simulation_thread = Thread(target=simulation_start, args=())
            simulation_thread.setDaemon(True)
            simulation_thread.start()

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


if __name__ == "__main__":
    display_main()
