from typing import Any, Callable

from Exceptions.InputException import InputException
from Structures.Move import Move

class GameInputHandler:
	minFirstInputBorder: int = 20
	maxFirstInputBorder: int = 30

	minMoveInputBorder: int = 3
	maxMoveInputBorder: int = 5

	@staticmethod
	def handleInput(input: Callable, *args) -> Any:
		while True:
			try:
				return input(*args)
			except InputException as e:
				print(f'Draugi, nav labi: {e}')
			except Exception as e:
				print(f'Draugi, super nav labi: {e}')

	@staticmethod
	def getHandledFirstMove(playerId: int) -> Move:
		return GameInputHandler.handleInput(GameInputHandler.getFirstMove, playerId)

	@staticmethod
	def getHandledMove(playerId: int) -> Move:
		return GameInputHandler.handleInput(GameInputHandler.getMove, playerId)

	@staticmethod
	def getFirstMove(playerId: int) -> Move:
		firstInput = int(input(f'Input a number ({GameInputHandler.minFirstInputBorder}-{GameInputHandler.maxFirstInputBorder}): '))

		if not GameInputHandler.isFirstInputValid(firstInput):
			raise InputException(f'First input is invalid! Not between {GameInputHandler.minFirstInputBorder} and {GameInputHandler.maxFirstInputBorder}.')

		return Move(playerId, firstInput, Move.TYPE_FIRST)

	@staticmethod
	def isFirstInputValid(firstInput: int) -> bool:
		return firstInput >= GameInputHandler.minFirstInputBorder and firstInput <= GameInputHandler.maxFirstInputBorder

	@staticmethod
	def getMove(playerId: int) -> Move:
		moveInput = int(input(f'Input a number ({GameInputHandler.minMoveInputBorder}-{GameInputHandler.maxMoveInputBorder}): '))

		if not GameInputHandler.isMoveInputValid(moveInput):
			raise InputException(f'First input is invalid! Not between {GameInputHandler.minMoveInputBorder} and {GameInputHandler.maxMoveInputBorder}.')

		return Move(playerId, moveInput)

	@staticmethod
	def isMoveInputValid(moveInput: int) -> bool:
		return moveInput >= GameInputHandler.minMoveInputBorder and moveInput <= GameInputHandler.maxMoveInputBorder