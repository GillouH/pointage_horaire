#!/usr/bin/env python3

from os import chdir
from Window import Window

if __name__ == "__main__":
	chdir(path="\\".join(__file__.split("\\")[:-1]))
	Window().mainloop()