from Input.GameInputHandler import GameInputHandler
from Structures.Move import Move

class ConsoleGame:
	# Game attributes
	isLive: bool = False
	bank: int = 0
	score: int = 0

	# Settings
	scoreThreshold: int = 3000

	# Current move Player ID
	currentPlayerId: int

	# Containers
	playerIds: list[int] = []
	moves: list[Move] = []

	def play(self) -> None:
		self.launch()

		self.populatePlayers()
		self.handleFirstInput()

		while self.isLive:
			self.switchCurrentPlayer()
			self.handleMove()

			if self.areGameBoundariesMet():
				self.die()
				
				self.calculateFinalScore()
				
				print(f'\n\n\nThe final score is: {self.score} with bank value of {self.bank}')
				self.announceWinner(self.getWinner())

		self.printMoveDebug()

	def printMoveDebug(self) -> None:
		print('\n\n\nMOVE DEBUG DATA:')

		for move in self.moves:
			print(move.getData())

	def launch(self) -> None:
		self.isLive = True

	def areGameBoundariesMet(self) -> bool:
		return self.score >= self.scoreThreshold

	def setCurrentPlayer(self, playerId) -> None:
		self.currentPlayerId = playerId

	def getFirstPlayerId(self) -> int:
		return self.playerIds[0]

	def getSecondPlayerId(self) -> int:
		return self.playerIds[1]

	# Supports 2 players only
	def switchCurrentPlayer(self) -> None:
		if self.currentPlayerId == self.getFirstPlayerId():
			self.currentPlayerId = self.getSecondPlayerId()
			print('--Switched from ply1 to ply2!--')
		else:
			self.currentPlayerId = self.getFirstPlayerId()
			print('--Switched from ply2 to ply1!--')

	def die(self) -> None:
		self.isLive = False

	def populatePlayers(self) -> None:
		playerIds: list[int] = [0, 1]

		for playerId in playerIds:
			self.playerIds.append(playerId)

		self.currentPlayerId = self.getFirstPlayerId()

	def handleFirstInput(self) -> None:
		move: Move = GameInputHandler.getHandledFirstMove(self.currentPlayerId)

		self.score += move.getValue()
		self.recordMove(move)

		print(f'Bank! {self.bank}')
		print(f'Score! {self.score}')

	def handleMove(self) -> None:
		move: Move = GameInputHandler.getHandledMove(self.currentPlayerId)

		self.score *= move.getValue()
		self.recordMove(move)

		self.recalculateScore()
		self.recalculateBank()

	def recalculateScore(self) -> None:
		print(f'Score before recalculation: {self.score}')

		if self.score % 2 == 0:
			self.score += 1
		else:
			self.score -= 1

		print(f'> Score after recalculation: {self.score}')

	def recalculateBank(self) -> None:
		if self.score % 10 == 0 or self.score % 10 == 5:
			self.bank += 1

		print(f'Bank! {self.bank}')

	def recordMove(self, move: Move) -> None:
		self.moves.append(move)

	def calculateFinalScore(self) -> None:
		if self.score % 2 == 0:
			self.score -= self.bank
		else:
			self.score += self.bank

	@staticmethod
	def announceWinner(winnerPlayerId: int) -> None:
		print(f'<####### The winner is Player No. {winnerPlayerId + 1}!')

	def getWinner(self) -> int:
		if self.score % 2 == 0:
			return self.getFirstPlayerId()

		return self.getSecondPlayerId()