from __future__ import annotations
from enum import Enum
from customtkinter import *
from CTkMessagebox import CTkMessagebox
from typing_extensions import Self, Any, Callable
from Core.UiGame import UiGame
from Exceptions.InputException import InputException
from random import randint
import time

class Layout: 
    controller: LayoutController

    font: tuple = ('Arial', 18)

    placed_elements: list = []

    def __init__(self, controller: LayoutController):
        self.controller = controller

    def create(self):
        self.initialize()
        self.place()

    def initialize(self):
        pass

    def place(self):
        pass

    # New method. The overrides are old ones. Too lazy to update.
    def destroy(self):
        element: CTkBaseClass
        for element in self.placed_elements:
            element.destroy()

        self.placed_elements = []

class MenuLayout(Layout):
    label: CTkLabel
    label_font: tuple = ('Arial', 36)

    buttons: list = []

    element_rel_x: float = 0.5 # In the middle
    
    label_rel_y: float = 0.1
    first_element_rel_y: float = 0.4

    inter_element_margin: float = 0.1

    element_width: int = 280
    element_height: int = 56

class MainMenuLayout(MenuLayout):
    label: CTkLabel
    startButton: CTkButton
    settingsButton: CTkButton
    exitButton: CTkButton

    def initialize(self):
        self.label = CTkLabel(
            master=self.controller.get_master(), 
            text="MIPamati",
            font=self.label_font,
            width=self.element_width,
            height=self.element_height
        )

        self.startButton = CTkButton(
            master=self.controller.get_master(), 
            text="Play!", 
            command=self.button_play,
            font=self.font,
            width=self.element_width,
            height=self.element_height
        )
        self.settingsButton = CTkButton(
            master=self.controller.get_master(), 
            text="Settings",
            command=self.button_settings,
            font=self.font,
            width=self.element_width,
            height=self.element_height
        )
        self.exitButton = CTkButton(
            master=self.controller.get_master(), 
            text="Exit", 
            command=self.button_exit,
            font=self.font,
            width=self.element_width,
            height=self.element_height
        )

        self.buttons = [self.startButton, self.settingsButton, self.exitButton]

    def place(self):
        self.label.place(relx=self.element_rel_x, rely=self.label_rel_y, anchor=N)
        self.placed_elements.append(self.label)

        btnIndex = 0
        for button in self.buttons:
            button.place(
                relx=self.element_rel_x, 
                rely=self.first_element_rel_y + self.inter_element_margin * btnIndex, 
                anchor=CENTER
            )
            self.placed_elements.append(button)
            
            btnIndex += 1

    def button_play(self):
        self.controller.play()

    def button_settings(self):
        self.controller.settings()

    def button_exit(self):
        title = "Stop! Wait a minute..."
        prompt = "Are you sure you wanna quit? Maybe give it another go ;)"
        
        positiveAnswer = 'Bye.'
        negativeAnswer = 'NO!'

        options = [positiveAnswer, negativeAnswer]
        
        answer = CTkMessagebox(
            master=self.controller.get_master(), 
            title=title, 
            title_color="red", 
            message=prompt, 
            options=options
        ).get()

        if answer is positiveAnswer:
            self.controller.terminate()

# TODO: implement settings
#   1. Who begins the game (Human || Computer || Random)
#   2. Alpha-beta pruning (ON || OFF)
#   3. Cheat window? (Shows game graph that generates from the turn you're on)
#   4. Endgame debug values? (processing time, calculated branch count)
class SettingsLayout(MenuLayout):
    def initialize(self):
        self.label = CTkLabel(
            master=self.controller.get_master(), 
            text="WIP Settings (get outta here)",
            font=self.label_font
        )
        self.mainMenuButton = CTkButton(
            master=self.controller.get_master(), 
            text="Go back!", 
            command=self.switch_to_main_menu,
            font=self.font,
            width=self.element_width,
            height=self.element_height
        )

    def place(self):
        self.label.place(relx=self.element_rel_x, rely=self.label_rel_y, anchor=N)
        self.mainMenuButton.place(relx=self.element_rel_x, rely=self.first_element_rel_y, anchor=CENTER)

        self.placed_elements = [self.label, self.mainMenuButton]

    def destroy(self):
        self.label.destroy()
        self.mainMenuButton.destroy()

    def switch_to_main_menu(self):
        self.controller.main_menu()

class GameLayout(Layout):
    game: UiGame = UiGame()

    goesFirstLabel: CTkLabel
    goesFirstValue: CTkLabel

    inputNumberLabel: CTkLabel
    inputNumberEntry: CTkEntry
    inputNumberConfirm: CTkButton

    algorithmLabel: CTkLabel
    algorithmValue: CTkLabel

    scoreLabel: CTkLabel
    scoreValue: CTkLabel
    
    bankLabel: CTkLabel
    bankValue: CTkLabel

    turnLabel: CTkLabel
    turnValue: CTkLabel

    def initialize(self):
        CTkMessagebox(
            master=self.controller.get_master(),
            width=1200,
            title="Help",
            message=LongMessage.GAME_DESCRIPTION.value, 
            option_1="COOL"
        ).get() # Value is dismissed, the method is used to resume execution ONLY after the box is closed
        print("Messagebox closed")

        self.mainMenuButton = CTkButton(
            master=self.controller.get_master(), 
            text="Quit (L)", 
            command=self.switch_to_main_menu,
            font=self.font,
            width=60,
            height=40
        )

        self.goesFirstLabel = CTkLabel(
            master=self.controller.get_master(), 
            text="Goes first",
            font=self.font
        )
        self.goesFirstValue = CTkLabel(
            master=self.controller.get_master(), 
            text="Nobody",
            font=self.font
        )

        self.inputNumberLabel = CTkLabel(
            master=self.controller.get_master(), 
            text="Input number",
            font=self.font
        )
        self.inputNumberEntry = CTkEntry(
            master=self.controller.get_master(),
            font=self.font,
            width=160,
            height=40
        )
        self.inputNumberConfirm = CTkButton(
            master=self.controller.get_master(), 
            text="OK", 
            command=self.confirm_input_number,
            font=self.font,
            width=40,
            height=40
        )

        self.algorithmLabel = CTkLabel(
            master=self.controller.get_master(), 
            text="Algorithm",
            font=self.font
        )
        self.algorithmValue = CTkLabel(
            master=self.controller.get_master(), 
            text="Nothing (+nothing)",
            font=self.font
        )

        self.scoreLabel = CTkLabel(
            master=self.controller.get_master(), 
            text="Score",
            font=self.font
        )
        self.scoreValue = CTkLabel(
            master=self.controller.get_master(), 
            text="0",
            font=self.font
        )

        self.bankLabel = CTkLabel(
            master=self.controller.get_master(), 
            text="Bank",
            font=self.font
        )
        self.bankValue = CTkLabel(
            master=self.controller.get_master(), 
            text="0",
            font=self.font
        )

        self.turnLabel = CTkLabel(
            master=self.controller.get_master(), 
            text="Turn",
            font=self.font
        )
        self.turnValue = CTkLabel(
            master=self.controller.get_master(), 
            text="0",
            font=self.font
        )

    def place(self):
        self.mainMenuButton.place(relx=0.01, rely=0.01)

        self.goesFirstLabel.place(relx=0.2, rely=0.1, anchor=N)
        self.goesFirstValue.place(relx=0.2, rely=0.17, anchor=N)

        self.inputNumberLabel.place(relx=0.5, rely=0.1, anchor=N)
        self.inputNumberEntry.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.inputNumberConfirm.place(relx=0.6, rely=0.2, anchor=CENTER)

        self.algorithmLabel.place(relx=0.8, rely=0.1, anchor=N)
        self.algorithmValue.place(relx=0.8, rely=0.17, anchor=N)

        self.scoreLabel.place(relx=0.5, rely=0.45, anchor=CENTER)
        self.scoreValue.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.bankLabel.place(relx=0.8, rely=0.45, anchor=CENTER)
        self.bankValue.place(relx=0.8, rely=0.5, anchor=CENTER)

        self.turnLabel.place(relx=0.8, rely=0.76, anchor=CENTER)
        self.turnValue.place(relx=0.8, rely=0.83, anchor=CENTER)

        self.placed_elements = [
            self.mainMenuButton,
            
            self.goesFirstLabel,
            self.goesFirstValue,
            
            self.inputNumberLabel, 
            self.inputNumberEntry,
            self.inputNumberConfirm,
            
            self.algorithmLabel,
            self.algorithmValue,
            
            self.scoreLabel,
            self.scoreValue,
            
            self.bankLabel,
            self.bankValue,
            
            self.turnLabel,
            self.turnValue,
        ]

        self.begin()

    def begin(self):
        self.reset_label_values()

        self.game.play(self.game.getHumanPlayerId())
        self.goesFirstValue.configure(text=str(self.game.getPlayerName()))
        
        self.turnValue.configure(text=f'{str(self.game.getPlayerName())} [0]')

        if self.game.isPlayerComputer():
            self.performComputerMoveWithFakeLatency()

    def reset_label_values(self):
        self.bankValue.configure(text='0')
        self.scoreValue.configure(text='0')
        self.turnValue.configure(text='')

    def confirm_input_number(self):
        if not self.performHumanMove():
            return
        
        self.performComputerMoveWithFakeLatency()
        
    def switchCurrentPlayer(self):
        print("SWITCHING CURRENT PLAYER...")
        self.game.switchCurrentPlayer()
        self.turnValue.configure(text=f'{self.game.getPlayerName()} [{str(self.game.getTurn())}]')
        
    def updateScoreAndBank(self):
        self.bankValue.configure(text=str(self.game.bank))
        self.scoreValue.configure(text=str(self.game.score))

    def performComputerMoveWithFakeLatency(self):
        # Disable input
        self.changeInputState(False)
        self.controller.ui_handler.debounce(self.performComputerMove)
        self.controller.ui_handler.debounce(self.changeInputState, 1000, True)

    def performComputerMove(self):
        moveValue = randint(20, 30) if self.game.isFirstInput else randint(3, 5)
        if not self.validateInput(moveValue):
            return 0
            
        self.performGameLoopActions()

    def changeInputState(self, enabled: bool):
        state = 'disabled' if not enabled else 'normal'
        self.inputNumberEntry.configure(state=state)
        self.inputNumberConfirm.configure(state=state)

    def validateInput(self, input: str):
        if self.game.isFirstInput:
            return self.handleInput(self.game.handleFirstInput, input)
        
        return self.handleInput(self.game.handleMove, input)

    def performHumanMove(self):
        if not self.validateInput(self.inputNumberEntry.get()):
            return 0

        self.performGameLoopActions()

        return 1

    # Happens after input validation (either Human or Computer)
    def performGameLoopActions(self):
        self.updateScoreAndBank()
        
        if self.game.areGameBoundariesMet():
            self.handleGameFinish()

            return
        
        self.switchCurrentPlayer()

    def handleGameFinish(self):
        self.game.calculateFinalScore()
        self.updateScoreAndBank()

        isHumanWinner: bool = self.game.getWinnerPlayerId() is self.game.getHumanPlayerId()

        CTkMessagebox(
            master=self.controller.get_master(),
            icon='check' if isHumanWinner else 'cancel',
            title="Draugi, ir labi!" if isHumanWinner else "Draugi, rēali nav labi..." ,
            message="You won!" if isHumanWinner else "You lost...", 
            option_1="gg"
        ).get()

        self.begin()
            
    def handleInput(self, callback: Callable, *args) -> int:
        try:
            callback(*args)

            return 1
        except InputException as e:
            CTkMessagebox(
                master=self.controller.get_master(),
                icon="cancel",
                title="Draugi, nav labi",
                message=e, 
                option_1="Ow!"
            ).get()

            return 0
        except ValueError as e:
            CTkMessagebox(
                master=self.controller.get_master(),
                icon="cancel",
                title="Draugi, super nav labi",
                message="Who do you think you are?", 
                option_1="I'm a tester."
            ).get()

            return 0

    def switch_to_main_menu(self):
        self.game.die()
        self.controller.main_menu()

class LayoutController:
    # UI Handler that does the nitty gritty actions, 
    # holds head CTk instance which layouts get applied to
    ui_handler: UiHandler
    
    current_layout: Layout | None = None

    ### CONTROLLER SETUP

    def set_ui_handler(self, ui_handler: UiHandler) -> Self:
        self.ui_handler = ui_handler
        
        return self

    def get_ui_handler(self) -> UiHandler:
        return self.ui_handler
    
    def get_master(self) -> CTk:
        return self.ui_handler.get_ui()
  
    ### LAYOUTS

    def main_menu(self) -> None:
        self.set_layout(MainMenuLayout(self))

    def play(self) -> None:
        self.set_layout(GameLayout(self))

    def settings(self) -> None:
        self.set_layout(SettingsLayout(self))
        
    ### HELPERS

    def set_layout(self, layout: Layout) -> None:
        if not self.current_layout:
            layout.create()
            self.current_layout = layout

            return
        
        layout.initialize()
        self.current_layout.destroy()
        layout.place()

        self.current_layout = layout

    def terminate(self) -> None:
        print('Izslēdzamies... 😴')
        self.ui_handler.terminate()

class UiInitializer:
    ui: CTk
    
    def __init__(self):
        set_appearance_mode("light") # Modes: system (default), light, dark
        set_default_color_theme("blue") # Themes: blue (default), dark-blue, green

    def setup(self, width: int = 800, height: int = 600) -> CTk:
        self.ui = CTk() 

        self.handle_window_size(width, height)
        self.register_key_press_events()

        return self.ui
    
    def handle_window_size(self, width: int, height: int):
        self.ui.geometry(f'{width}x{height}')
        self.ui.maxsize(width, height)
    
    def register_key_press_events(self):
        self.ui.bind('<Return>', self.key_pressed)

    def key_pressed(self, e):
        print('Key press event registered')
        print(type(e))
        print(f'{e.char} pressed')
        

class UiHandler:
    ui: CTk

    def __init__(self, ui: CTk):
        self.ui = ui

    # Made to acquire the UI to pass to the created UI elements.
    # Please don't use it to call methods from it!
    # Create methods in UiHandler (self) instead.
    def get_ui(self) -> CTk:
        return self.ui
    
    # Time in ms
    def debounce(self, callback: Callable, time: int = 1000, *args):
        self.ui.after(time, callback, *args)

    def mainloop(self):
        self.ui.mainloop()

    def terminate(self):
        self.ui.quit()

# Because who wants to see such long strings in code, am I right?
class LongMessage(Enum):
    GAME_DESCRIPTION = "Spēles sākumā ir dots cilvēka-spēlētāja izvēlētais skaitlis diapazonā no 20 līdz 30. Kopīgs punktu skaits ir vienāds ar 0 (punkti netiek skaitīti katram spēlētājam atsevišķi). Turklāt spēlē tiek izmantota spēles banka, kura sākotnēji ir vienāda ar 0. Spēlētāji veic gājienus pēc kārtas, reizinot pašreizējā brīdī esošu skaitli ar 3, 4 vai 5. Ja reizināšanas rezultātā tiek iegūts pāra skaitlis, tad kopīgajam punktu skaitam tiek pieskaitīts 1 punkts, bet ja nepāra skaitlis – tad 1 punkts tiek atņemts. Savukārt, ja tiek iegūts skaitlis, kas beidzas ar 0 vai 5, tad bankai tiek pieskaitīts 1 punkts. Spēle beidzas, kad ir iegūts skaitlis, kas ir lielāks par vai vienāds ar 3000. Ja kopīgais punktu skaits ir pāra skaitlis, tad no tā atņem bankā uzkrātos punktus. Ja tas ir nepāra skaitlis, tad tam pieskaita bankā uzkrātos punktus. Ja kopīgā punktu skaita gala vērtība ir pāra skaitlis, uzvar spēlētājs, kas uzsāka spēli. Ja nepāra skaitlis, tad otrais spēlētājs."

ui_handler = UiHandler(UiInitializer().setup())

layout_controller = LayoutController().set_ui_handler(ui_handler)
layout_controller.main_menu()

ui_handler.mainloop()