from doctest import master
from tkinter import Tk, StringVar, Frame, Label, Entry, Button
from tkinter.font import Font
from turtle import update
from Duration import Duration
from os.path import isfile
from json import dumps, loads
from emoji import emojize

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
		self.createCumuleFrame()
		self.createTodayFrame()

	def createCumuleFrame(self):
		self.cumule:"Duration" = Duration.fromMinutes(minutes=self.data[Window.MEMORY_CUMUL])
		self.cumuleHourTextVariable:"StringVar" = StringVar(value=self.cumule.getHours())
		self.cumuleMinutesTextVariable:"StringVar" = StringVar(value=self.cumule.getMinutes())
		cumuleFrame:"Frame" = Frame(master=self)
		cumuleFrame.grid(column=0, row=0)
		Label(master=cumuleFrame, text="Cumule enregistré : ", font=self.FONT).grid(column=0, row=0)
		Label(master=cumuleFrame, textvariable=self.cumuleHourTextVariable, font=self.FONT).grid(column=1, row=0)
		Label(master=cumuleFrame, text="H", font=self.FONT).grid(column=2, row=0)
		Label(master=cumuleFrame, textvariable=self.cumuleMinutesTextVariable, font=self.FONT).grid(column=3, row=0)

	def createTodayFrame(self):
		self.todayFrame :'Frame'= Frame(master=self, padx=Window.PADDING)
		self.todayFrame.grid(column=0, row=1)
		self.createFormFrame()
		self.createCumuleTodayFrame()

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
		Button(master=buttonFrame, text="J'ai travaillé ! {}".format(emojize(":beaming_face_with_smiling_eyes:")), command=self.substractToTodayTime, font=self.FONT, padx=Window.PADDING).grid(column=0, row=0)
		Button(master=buttonFrame, text="J'ai trop de travail ! {}".format(emojize(":loudly_crying_face:")), command=self.addToTodayTime, font=self.FONT, padx=Window.PADDING).grid(column=1, row=0)

	def createCumuleTodayFrame(self):
		cumuleTodayFrame:"Frame" = Frame(master=self.todayFrame, padx=Window.PADDING)
		cumuleTodayFrame.grid(column=1, row=0)
		self.cumuleToday:"Duration" = Duration.fromMinutes(minutes=7*60)
		self.cumuleTodayHourTextVariable:"StringVar" = StringVar(value=self.cumuleToday.getHours())
		self.cumuleTodayMinutesTextVariable:"StringVar" = StringVar(value=self.cumuleToday.getMinutes())
		Label(master=cumuleTodayFrame, text="Cumule aujourd'hui : ", font=self.FONT).grid(column=0, row=0)
		Label(master=cumuleTodayFrame, textvariable=self.cumuleTodayHourTextVariable, font=self.FONT).grid(column=1, row=0)
		Label(master=cumuleTodayFrame, text="H", font=self.FONT).grid(column=2, row=0)
		Label(master=cumuleTodayFrame, textvariable=self.cumuleTodayMinutesTextVariable, font=self.FONT).grid(column=3, row=0)

	def updateCumuleToday(self, durationToAdd:"Duration"):
		self.cumuleToday += durationToAdd
		self.cumuleTodayHourTextVariable.set(value=self.cumuleToday.getHours())
		self.cumuleTodayMinutesTextVariable.set(value=self.cumuleToday.getMinutes())

	def getEntryDuration(self):
		return Duration.fromMinutes(minutes=int(self.hoursTextVariable.get())*60+int(self.minutesTextVariable.get()))

	def substractToTodayTime(self):
		self.updateCumuleToday(self.getEntryDuration()*-1)

	def addToTodayTime(self):
		self.updateCumuleToday(self.getEntryDuration())

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