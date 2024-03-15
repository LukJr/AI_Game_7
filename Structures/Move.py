from typing import Any

class Move:
	TYPE_FIRST = 'first_input'
	TYPE_MOVE = 'move'

	playerId: int
	value: int
	type: str

	def __init__(self, playerId: int, value: int, type: str = TYPE_MOVE):
		self.playerId = playerId
		self.value = value
		self.type = type

	def getValue(self) -> int:
		return self.value

	def getData(self) -> dict[str, Any]:
		return {
			"playerId": self.playerId, 
			"value": self.value,
			"type": self.type
		}