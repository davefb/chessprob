import curses
stdscr = curses.initscr()

curses.noecho()
curses.cbreak()
stdscr.keypad(1)


win = curses.newwin(100,100)

#curses.nocbreak();
#stdscr.keypad(0);
#curses.echo()

