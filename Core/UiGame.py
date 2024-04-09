from Input.GameInputHandler import UiGameInputHandler
from Structures.Move import Move

from Exceptions import InputException

class UiGame:
	# Game attributes
	isLive: bool = False
	bank: int
	score: int

	# Settings
	scoreThreshold: int = 3000

	# Current move Player ID
	currentPlayerId: int

	# Containers
	playerIds: list[int] = []
	moves: list[Move] = []

	players: dict = {
		0: 'YOU',
		1: 'Computer'
	}

	isFirstInput: bool = True

	def play(self, startWith: int = 0) -> None:
		self.resetValues()

		self.populatePlayers(startWith)
		self.isLive = True

		print('Game started!')

	def resetValues(self) -> None:
		self.isFirstInput = True
		self.bank = 0
		self.score = 0
		self.playerIds = []
		self.moves = []

	def printMoveDebug(self) -> None:
		print('\n\n\nMOVE DEBUG DATA:')

		for move in self.moves:
			print(move.getData())

	def getTurn(self) -> int:
		#if not self.moves:
		#	return 0

		return len(self.moves)

	def areGameBoundariesMet(self) -> bool:
		return self.score >= self.scoreThreshold

	def setCurrentPlayer(self, playerId) -> None:
		self.currentPlayerId = playerId

	def isPlayerComputer(self) -> bool:
		print(self.currentPlayerId)
		return self.currentPlayerId == self.getComputerPlayerId()

	def getHumanPlayerId(self) -> int:
		return 0

	def getComputerPlayerId(self) -> int:
		return 1
	
	def getPlayerName(self) -> str:
		print(self.currentPlayerId)
		return self.players[self.currentPlayerId]

	# Supports 2 players only
	def switchCurrentPlayer(self) -> None:
		if self.currentPlayerId == self.getHumanPlayerId():
			self.currentPlayerId = self.getComputerPlayerId()
			print('--Switched from ply1 to ply2!--')
		else:
			self.currentPlayerId = self.getHumanPlayerId()
			print('--Switched from ply2 to ply1!--')



	def die(self) -> None:
		self.isLive = False
		print('Game shutdown.')

	def populatePlayers(self, goes_first_player_id: int = 0) -> None:
		playerIds: list[int] = [self.getHumanPlayerId(), self.getComputerPlayerId()] if goes_first_player_id == self.getHumanPlayerId() else [self.getComputerPlayerId(), self.getHumanPlayerId()]

		for playerId in playerIds:
			self.playerIds.append(playerId)

		self.currentPlayerId = goes_first_player_id

	def handleFirstInput(self, input: str) -> None:
		move: Move = UiGameInputHandler.getHandledFirstMove(self.currentPlayerId, input)

		self.score += move.getValue()
		self.recordMove(move)

		self.isFirstInput = False

		print(f'Bank! {self.bank}')
		print(f'Score! {self.score}')

	def handleMove(self, input: str) -> None:
		move: Move = UiGameInputHandler.getHandledMove(self.currentPlayerId, input)

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

	def getWinnerPlayerName(self) -> str:
		return self.players[self.getWinnerPlayerId()]
	
	def getWinnerPlayerId(self) -> int:
		if self.score % 2 == 0:
			return self.playerIds[0]
		
		return self.playerIds[1]