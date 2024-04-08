from __future__ import annotations
from enum import Enum
from customtkinter import *
from CTkMessagebox import CTkMessagebox
from typing_extensions import Self, Any

class Layout: 
    controller: LayoutController

    font: tuple = ('Arial', 13)

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
    label_font: tuple = ('Arial', 18)

    buttons: list = []

    element_rel_x: float = 0.5 # In the middle
    
    label_rel_y: float = 0.1
    first_element_rel_y: float = 0.4

    inter_element_margin: float = 0.07

class MainMenuLayout(MenuLayout):
    label: CTkLabel
    startButton: CTkButton
    settingsButton: CTkButton
    exitButton: CTkButton

    def initialize(self):
        self.label = CTkLabel(
            master=self.controller.get_master(), 
            text="MIPamati",
            font=self.label_font
        )

        self.startButton = CTkButton(
            master=self.controller.get_master(), 
            text="Play!", 
            command=self.button_play,
            font=self.font
        )
        self.settingsButton = CTkButton(
            master=self.controller.get_master(), 
            text="Settings",
            command=self.button_settings,
            font=self.font
        )
        self.exitButton = CTkButton(
            master=self.controller.get_master(), 
            text="Exit", 
            command=self.button_exit,
            font=self.font
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
        
        answer = CTkMessagebox(master=self.controller.get_master(), title=title, title_color="red", message=prompt, options=options).get()
        print(answer)

        if answer is positiveAnswer:
            self.controller.terminate()


class GameLayout(Layout):
    inputNumberLabel: CTkLabel
    inputNumberEntry: CTkEntry

    def initialize(self):
        CTkMessagebox(
            master=self.controller.get_master(),
            width=1200,
            title="Help",
            message=LongMessage.GAME_DESCRIPTION.value, 
            option_1="COOL"
        ).get() # Value is dismissed, the method is used to resume execution ONLY after the box is closed
        print("Messagebox closed")

        self.inputNumberLabel = CTkLabel(
            master=self.controller.get_master(), 
            text="Input number",
            font=(self.font[0], 18)
        )
        self.inputNumberEntry = CTkEntry(
            master=self.controller.get_master(),
            font=self.font
        )

    def place(self):
        self.inputNumberLabel.place(relx=0.5, rely=0.1, anchor=N)
        self.inputNumberEntry.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.placed_elements = [
            self.inputNumberLabel, 
            self.inputNumberEntry,
        ]

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
            font=self.font
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

class LayoutController:
    # Head CTk instance (to apply layouts to)
    master: CTk
    
    current_layout: Layout | None = None

    ### CONTROLLER SETUP

    def set_master(self, master: CTk) -> Self:
        self.master = master

        return self
    
    def get_master(self) -> CTk:
        return self.master
  
    ### LAYOUTS

    def main_menu(self):
        self.set_layout(MainMenuLayout(self))

    def play(self):
        self.set_layout(GameLayout(self))

    def settings(self) -> MainMenuLayout:
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
        print('Shutting down...')
        self.get_master().quit()

class UiInitializer:
    ui: CTk
    
    def __init__(self):
        set_appearance_mode("light") # Modes: system (default), light, dark
        set_default_color_theme("blue") # Themes: blue (default), dark-blue, green

    def setup(self, width: int = 800, height: int = 600) -> CTk:
        self.ui = CTk() 

        self.ui.geometry(f'{width}x{height}')
        self.ui.maxsize(width, height)

        self.key_press_event_registration()

        return self.ui
    
    def key_press_event_registration(self):
        self.ui.bind('<Return>', self.key_pressed)

    def key_pressed(self, e):
        print('Key press event registered')
        print(type(e))
        print(f'{e.char} pressed')

    def mainloop(self):
        self.ui.mainloop()

# Because who wants to see such long strings in code, am I right?
class LongMessage(Enum):
    GAME_DESCRIPTION = "Spēles sākumā ir dots cilvēka-spēlētāja izvēlētais skaitlis diapazonā no 20 līdz 30. Kopīgs punktu skaits ir vienāds ar 0 (punkti netiek skaitīti katram spēlētājam atsevišķi). Turklāt spēlē tiek izmantota spēles banka, kura sākotnēji ir vienāda ar 0. Spēlētāji veic gājienus pēc kārtas, reizinot pašreizējā brīdī esošu skaitli ar 3, 4 vai 5. Ja reizināšanas rezultātā tiek iegūts pāra skaitlis, tad kopīgajam punktu skaitam tiek pieskaitīts 1 punkts, bet ja nepāra skaitlis – tad 1 punkts tiek atņemts. Savukārt, ja tiek iegūts skaitlis, kas beidzas ar 0 vai 5, tad bankai tiek pieskaitīts 1 punkts. Spēle beidzas, kad ir iegūts skaitlis, kas ir lielāks par vai vienāds ar 3000. Ja kopīgais punktu skaits ir pāra skaitlis, tad no tā atņem bankā uzkrātos punktus. Ja tas ir nepāra skaitlis, tad tam pieskaita bankā uzkrātos punktus. Ja kopīgā punktu skaita gala vērtība ir pāra skaitlis, uzvar spēlētājs, kas uzsāka spēli. Ja nepāra skaitlis, tad otrais spēlētājs."

ui = UiInitializer().setup()
layout_controller = LayoutController().set_master(ui)

layout_controller.main_menu()

ui.mainloop()