class Duration:
	def __init__(self, positif:"bool"=True, hours:"int"=0, minutes:"int"=0) -> None:
		assert isinstance(positif, bool), "Le paramètre \"positif\" doit être un bouléen."
		assert isinstance(hours, int) and hours >= 0, "Le paramètre \"hours\" doit être un entier positif."
		assert isinstance(minutes, int) and minutes >= 0, "Le paramètre \"minutes\" doit être un entier positif."
		self.minutes:"int" = hours * 60 + minutes
		if not positif:
			self.minutes *= -1

	def getHours(self) -> "int":
		if self.minutes > -60 and self.minutes < 0:
			return "-0"
		return int(self.minutes / 60)

	def getMinutes(self) -> "int":
		return abs(self.minutes) % 60

	def toMinutes(self) -> "int":
		return self.minutes

	@staticmethod
	def fromMinutes(minutes:"int") -> "Duration":
		return Duration(positif=minutes>=0, minutes=abs(minutes))

	def __add__(self, duration:"Duration") -> "Duration":
		assert isinstance(duration, Duration), "Le paramètre \"duration\" doit être un objet du type Duration."
		return Duration.fromMinutes(self.toMinutes + duration.toMinutes)
	
	def __iadd__(self, duration:"Duration") -> None:
		self.minutes += duration.minutes

	def __sub__(self, duration:"Duration") -> "Duration":
		assert isinstance(duration, Duration), "Le paramètre \"duration\" doit être un objet du type Duration."
		return Duration.fromMinutes(self.toMinutes - duration.toMinutes)

	def __isub__(self, duration:"Duration") -> None:
		self.minutes -= duration.minutes