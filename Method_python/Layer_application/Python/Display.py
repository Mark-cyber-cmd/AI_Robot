import curses
from Simulation import *
from Control import *


def display_main():
    stdscr = curses.initscr()
    curses.noecho()
    stdscr.nodelay(True)
    stdscr.addstr(1, 25, '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>system runing<<<<<<<<<<<<<<<<<<<<<<<<<<', curses.A_REVERSE)
    stdscr.refresh()
    counter = 0
    while 1:
        s_line = 13
        stdscr.addstr(2, 25, '          Sampling {0}'.format(counter))
        stdscr.addstr(4, 25, '                Servo 3 {0}                  Servo 6 {1}            '.format(robot.position[3], robot.position[6]))
        stdscr.addstr(5, 25, '          Back 1000 ---> Front 0         Back 0 ---> Front 1000     ')
        stdscr.addstr(7, 25, '                Servo 2 {0}                  Servo 5 {1}            '.format(robot.position[2], robot.position[5]))
        stdscr.addstr(8, 25, '          Back 0 ---> Front 1000         Back 1000 ---> Front 0     ')
        stdscr.addstr(10, 25,'                Servo 1 {0}                  Servo 4 {1}            '.format(robot.position[1], robot.position[4]))
        stdscr.addstr(11, 25,'          Left 0 ---> Right 1000         Left 0 ---> Right 1000     ')
        for i in Gyro.client_index:
            exec("stdscr.addstr(s_line, 25, 'gyro {0} roll:'+str(round(gyro_{0}.roll, 2)) + '   ', curses.A_REVERSE)".format(i))
            exec("stdscr.addstr(s_line, 50, 'gyro {0} row:'+str(round(gyro_{0}.yaw, 2)) + '   ', curses.A_REVERSE)".format(i))
            exec("stdscr.addstr(s_line, 75, 'gyro {0} pitch:'+str(round(gyro_{0}.pitch, 2)) + '   ', curses.A_REVERSE)".format(i))
            s_line = s_line + 2

        c = stdscr.getch()

        if c == ord('b'):
            break

        if c == ord('s'):
            break

        counter = counter + 1

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


if __name__ == "__main__":

    display_main()
