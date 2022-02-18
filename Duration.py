class Duration:
	def __init__(self, positif:"bool"=True, hours:"int"=0, minutes:"int"=0) -> None:
		assert isinstance(positif, bool), "Le paramètre \"positif\" doit être un bouléen."
		self.positif = positif
		self.setHours(hours=hours, minutes=minutes)
		self.setMinutes(minutes=minutes)

	def setHours(self, hours:"int"=0, minutes:"int"=0) -> None:
		assert isinstance(hours, int), "Le paramètre \"hours\" doit être un nombre entier."
		assert isinstance(minutes, int), "Le paramètre \"minutes\" doit être un nombre entier."
		self.hours = hours + int(minutes / 60)
	
	def setMinutes(self, minutes:"int"=0) -> None:
		assert isinstance(minutes, int), "minutes doit être un nombre entier"
		self.minutes = minutes % 60

	def getHours(self) -> "int":
		return self.hours if self.positif else -self.hours
	
	def getHoursStr(self) -> "str":
		return str(self.getHours()) if self.hours != 0 or self.positif else "-0"
	
	def getMinutes(self) -> "int":
		return self.minutes

	def toMinutes(self) -> "int":
		minutes = self.getMinutes() + self.getHours() * 60
		return minutes if self.positif else -minutes

	@staticmethod
	def fromMinutes(minutes:"int") -> "Duration":
		return Duration(positif=minutes>=0, minutes=abs(minutes))

	def update(self, duration:"Duration") -> None:
		assert isinstance(duration, Duration), "le paramètre \"duration\" doit être un objet du type Duration"
		self.positif = duration.positif
		self.hours = duration.hours
		self.minutes = duration.minutes

	def __add__(self, duration:"Duration") -> "Duration":
		assert isinstance(duration, Duration), "Le paramètre \"duration\" doit être un objet du type Duration."
		return Duration.fromMinutes(self.toMinutes + duration.toMinutes)
	
	def __iadd__(self, duration:"Duration") -> None:
		self.update(self + duration)

	def __sub__(self, duration:"Duration") -> "Duration":
		assert isinstance(duration, Duration), "Le paramètre \"duration\" doit être un objet du type Duration."
		return Duration.fromMinutes(self.toMinutes - duration.toMinutes)

	def __isub__(self, duration:"Duration") -> None:
		self.update(self - duration)