from doctest import master
from tkinter import Tk, StringVar, Frame, Label, Entry, Button
from tkinter.font import Font
from turtle import update
from Duration import Duration
from os.path import isfile
from json import dumps, loads

class Window(Tk):
	MEMORY_FILE:"str" = "memory.json"
	MEMORY_CUMUL:"str" = "MEMORY_CUMUL"
	MEMORY_HISTORY:"str" = "MEMORY_HISTORY"
	MEMORY_HISTORY_DATE:"str" = "MEMORY_HISTORY_DATE"
	MEMORY_HISTORY_TIME:"str" = "MEMORY_HISTORY_TIME"
	ENTRY_WIDTH:"int" = 2
	PADDING:"int" = 10

	def __init__(self):
		super().__init__()
		self.FONT:"Font" = Font(root=self, size=15)
		self.title(string="Pointage Horaire")
		self.data:"dict[str,any]" = self.restoreData()
		self.createCumulFrame()
		self.createTodayFrame()
		self.createNewCumulFrame()

	def createCumulFrame(self):
		self.cumul:"Duration" = Duration.fromMinutes(minutes=self.data[Window.MEMORY_CUMUL])
		self.cumulHourTextVariable:"StringVar" = StringVar(value=self.cumul.getHours())
		self.cumulMinutesTextVariable:"StringVar" = StringVar(value=self.cumul.getMinutes())
		cumulFrame:"Frame" = Frame(master=self)
		cumulFrame.grid(column=0, row=0)
		Label(master=cumulFrame, text="Cumul enregistré : ", font=self.FONT).grid(column=0, row=0)
		Label(master=cumulFrame, textvariable=self.cumulHourTextVariable, font=self.FONT).grid(column=1, row=0)
		Label(master=cumulFrame, text="H", font=self.FONT).grid(column=2, row=0)
		Label(master=cumulFrame, textvariable=self.cumulMinutesTextVariable, font=self.FONT).grid(column=3, row=0)

	def createTodayFrame(self):
		self.todayFrame :'Frame'= Frame(master=self, padx=Window.PADDING)
		self.todayFrame.grid(column=0, row=1)
		self.createFormFrame()
		self.createCumulTodayFrame()

	def createFormFrame(self):
		self.formFrame:"Frame" = Frame(master=self.todayFrame, padx=Window.PADDING)
		self.formFrame.grid(column=0, row=0)
		self.createEntryFrame()
		self.createButtonFrame()

	def createEntryFrame(self):
		entryFrame:"Frame" = Frame(master=self.formFrame)
		entryFrame.grid(column=0, row=0)

		self.hoursTextVariable:"StringVar" = StringVar(value="0")
		hoursEntry:"Entry" = Entry(master=entryFrame, textvariable=self.hoursTextVariable, width=Window.ENTRY_WIDTH, font=self.FONT)
		hoursEntry.grid(column=0, row=0)
		hoursEntry.config(validate="key", validatecommand=(self.register(func=self.checkHoursInput), "%P"))

		Label(master=entryFrame, text="H", font=self.FONT).grid(column=1, row=0)
		
		self.minutesTextVariable:"StringVar" = StringVar(value="00")
		minutesEntry:"Entry" = Entry(master=entryFrame, textvariable=self.minutesTextVariable, width=Window.ENTRY_WIDTH, font=self.FONT)
		minutesEntry.grid(column=2, row=0)
		minutesEntry.config(validate="key", validatecommand=(self.register(func=self.checkMinutesInput), "%P"))

	@staticmethod
	def checkInputIsInt(input:"str", max:"int"):
		try:
			number:"int" = int(input)
			assert int(number) >= 0 and number < max, "La valeur entrée doit être un entier positif strictement inférieur à {}".format(max)
			return True
		except Exception:
			return input == ""
	@staticmethod
	def checkHoursInput(input:"str") -> "bool":
		return Window.checkInputIsInt(input=input, max=100)
	@staticmethod
	def checkMinutesInput(input:"str") -> "bool":
		return Window.checkInputIsInt(input=input, max=60)

	def createButtonFrame(self):
		buttonFrame:"Frame" = Frame(master=self.formFrame)
		buttonFrame.grid(column=0, row=1)
		Button(master=buttonFrame, text="-", command=self.substractToTodayCumul, font=self.FONT, padx=Window.PADDING).grid(column=0, row=0)
		Button(master=buttonFrame, text="+", command=self.addToTodayCumul, font=self.FONT, padx=Window.PADDING).grid(column=1, row=0)

	def createCumulTodayFrame(self):
		cumulTodayFrame:"Frame" = Frame(master=self.todayFrame, padx=Window.PADDING)
		cumulTodayFrame.grid(column=1, row=0)
		self.cumulToday:"Duration" = Duration.fromMinutes(minutes=7*60)
		self.cumulTodayHourTextVariable:"StringVar" = StringVar(value=self.cumulToday.getHours())
		self.cumulTodayMinutesTextVariable:"StringVar" = StringVar(value=self.cumulToday.getMinutes())
		Label(master=cumulTodayFrame, text="Cumul aujourd'hui : ", font=self.FONT).grid(column=0, row=0)
		Label(master=cumulTodayFrame, textvariable=self.cumulTodayHourTextVariable, font=self.FONT).grid(column=1, row=0)
		Label(master=cumulTodayFrame, text="H", font=self.FONT).grid(column=2, row=0)
		Label(master=cumulTodayFrame, textvariable=self.cumulTodayMinutesTextVariable, font=self.FONT).grid(column=3, row=0)

	def updateTodayCumulAndNewCumul(self, durationToAdd:"Duration"):
		self.cumulToday += durationToAdd
		self.cumulTodayHourTextVariable.set(value=self.cumulToday.getHours())
		self.cumulTodayMinutesTextVariable.set(value=self.cumulToday.getMinutes())

		self.newCumul = self.cumul + self.cumulToday
		self.newCumulHourTextVariable.set(value=self.newCumul.getHours())
		self.newCumulMinutesTextVariable.set(value=self.newCumul.getMinutes())

	def getEntryDuration(self):
		return Duration.fromMinutes(minutes=int(self.hoursTextVariable.get())*60+int(self.minutesTextVariable.get()))

	def substractToTodayCumul(self):
		self.updateTodayCumulAndNewCumul(self.getEntryDuration()*-1)

	def addToTodayCumul(self):
		self.updateTodayCumulAndNewCumul(self.getEntryDuration())

	def createNewCumulFrame(self):
		self.newCumul:"Duration" = self.cumul + self.cumulToday
		self.newCumulHourTextVariable:"StringVar" = StringVar(value=self.newCumul.getHours())
		self.newCumulMinutesTextVariable:"StringVar" = StringVar(value=self.newCumul.getMinutes())
		newCumulFrame:"Frame" = Frame(master=self)
		newCumulFrame.grid(column=0, row=2)
		Label(master=newCumulFrame, text="Nouveau Cumul : ", font=self.FONT).grid(column=0, row=0)
		Label(master=newCumulFrame, textvariable=self.newCumulHourTextVariable, font=self.FONT).grid(column=1, row=0)
		Label(master=newCumulFrame, text="H", font=self.FONT).grid(column=2, row=0)
		Label(master=newCumulFrame, textvariable=self.newCumulMinutesTextVariable, font=self.FONT).grid(column=3, row=0)

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
		self.data[Window.MEMORY_CUMUL] = self.newCumul.toMinutes()
		dataJson:"str" = dumps(obj=self.data, indent=4, ensure_ascii=False)
		with open(Window.MEMORY_FILE, "w") as file:
			file.write(dataJson)
	
	def destroy(self) -> None:
		self.saveData()
		return super().destroy()