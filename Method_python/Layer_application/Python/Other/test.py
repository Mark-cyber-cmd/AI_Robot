import curses

stdscr = curses.initscr()
curses.noecho()
stdscr.nodelay(1)

stdscr.addstr(1, 25, '>>>>>>>>>>>>>>>>>>>>>>>>>>system runing<<<<<<<<<<<<<<<<<<<<<<<', curses.A_REVERSE)

while 1:
    stdscr.addstr(3, 25, 'gyro 1 roll:' + str(5), curses.A_REVERSE)
    stdscr.refresh()

    c = stdscr.getch()

    if c == ord('b'):
        break
