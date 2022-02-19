from tkinter import Tk, StringVar, Frame, Label
from tkinter.font import Font
from Duration import Duration
from os.path import isfile
from json import dumps, loads

class Window(Tk):
	MEMORY_FILE:"str" = "memory.json"
	MEMORY_CUMUL:"str" = "MEMORY_CUMUL"
	MEMORY_HISTORY:"str" = "MEMORY_HISTORY"
	MEMORY_HISTORY_DATE:"str" = "MEMORY_HISTORY_DATE"
	MEMORY_HISTORY_TIME:"str" = "MEMORY_HISTORY_TIME"

	def __init__(self):
		super().__init__()
		self.FONT:"Font" = Font(root=self, size=15)
		self.title(string="Pointage Horaire")
		self.data:"dict[str,any]" = self.restoreData()
		self.createCumuleFrame()

	def createCumuleFrame(self):
		self.cumule:"Duration" = Duration.fromMinutes(self.data[Window.MEMORY_CUMUL])
		self.cumuleHourTextVariable:"StringVar" = StringVar(value=self.cumule.getHours())
		self.cumuleMinutesTextVariable:"StringVar" = StringVar(value=self.cumule.getMinutes())
		cumuleFrame:"Frame" = Frame(master=self)
		cumuleFrame.grid(column=0, row=0)
		Label(master=cumuleFrame, text="Cumule : ", font=self.FONT).grid(column=0, row=0)
		Label(master=cumuleFrame, textvariable=self.cumuleHourTextVariable, font=self.FONT).grid(column=1, row=0)
		Label(master=cumuleFrame, text="H", font=self.FONT).grid(column=2, row=0)
		Label(master=cumuleFrame, textvariable=self.cumuleMinutesTextVariable, font=self.FONT).grid(column=3, row=0)
	
	def restoreData(self) -> "dict[str,any]":
		try:
			assert isfile(Window.MEMORY_FILE), "Memory file does not exist."
			with open(Window.MEMORY_FILE, "r") as file:
				content:"str" = file.read()
			return loads(content)
		except Exception:
			return {
				Window.MEMORY_CUMUL: 0
			}
	
	def saveData(self):
		dataJson:"str" = dumps(obj=self.data, indent=4, ensure_ascii=False)
		with open(Window.MEMORY_FILE, "w") as file:
			file.write(dataJson)
	
	def destroy(self) -> None:
		self.saveData()
		return super().destroy()