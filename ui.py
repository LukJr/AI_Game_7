from __future__ import annotations
import customtkinter
from CTkMessagebox import CTkMessagebox
from typing_extensions import Self, Any

class Layout: 
    controller: LayoutController

    def __init__(self, controller: LayoutController):
        self.controller = controller

    def create(self):
        self.initialize()
        self.place()

    def initialize(self):
        pass

    def place(self):
        pass

    def destroy(self):
        pass

class MainMenuLayout(Layout):
    label: customtkinter.CTkLabel
    startButton: customtkinter.CTkButton
    settingsButton: customtkinter.CTkButton
    exitButton: customtkinter.CTkButton    

    def initialize(self):
        self.label = customtkinter.CTkLabel(
            master=self.controller.get_master(), 
            text="CTkButton"
        )
        self.startButton = customtkinter.CTkButton(
            master=self.controller.get_master(), 
            text="CTkButton", 
            command=self.button_start
        )
        self.settingsButton = customtkinter.CTkButton(
            master=self.controller.get_master(), 
            text="Settings",
            command=self.button_settings
        )
        self.exitButton = customtkinter.CTkButton(
            master=self.controller.get_master(), 
            text="CTkButton", 
            command=self.button_settings
        )

    def place(self):
        self.label.place(relx=0.5, rely=0.1, anchor=customtkinter.N)
        self.startButton.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        self.settingsButton.place(relx=0.5, rely=0.6, anchor=customtkinter.CENTER)
        self.exitButton.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

    def destroy(self):
        self.label.destroy()
        self.startButton.destroy()
        self.settingsButton.destroy()
        self.exitButton.destroy()

    def button_start(self):

        # print("button pressed")
        # print(entry.get(), type(entry.get()))
        
        # if not entry.get().isnumeric():
        #     CTkMessagebox(master=self.master, icon="cancel", message="cringe")
        #     entry.destroy()
        pass

    def button_settings(self):
        self.controller.settings()

    def button_exit(self):
        pass

class SettingsLayout(Layout):
    def initialize(self):
        self.label = customtkinter.CTkLabel(
            master=self.controller.get_master(), 
            text="Settings"
        )
        self.mainMenuButton = customtkinter.CTkButton(
            master=self.controller.get_master(), 
            text="Main Menu", 
            command=self.switch_to_main_menu
        )

    def place(self):
        self.label.place(relx=0.5, rely=0.1, anchor=customtkinter.N)
        self.mainMenuButton.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

    def destroy(self):
        self.label.destroy()

    def switch_to_main_menu(self):
        self.controller.main_menu()

class LayoutController:
    # Head CTk instance (to apply layouts to)
    master: customtkinter.CTk
    
    current_layout: Layout | None = None

    ### CONTROLLER SETUP

    def set_master(self, master: customtkinter.CTk) -> Self:
        self.master = master

        return self
    
    def get_master(self) -> customtkinter.CTk:
        return self.master
  
    ### LAYOUTS

    def main_menu(self):
        self.set_layout(MainMenuLayout(self))

    def settings(self) -> MainMenuLayout:
        self.set_layout(SettingsLayout(self)) # TODO: settings layout
        
    ### HELPERS

    def set_layout(self, layout: Layout) -> Any:
        if not self.current_layout:
            layout.create()

            return
        
        layout.initialize()
        self.current_layout.destroy()
        layout.place()

class UiInitializer:
    ui: customtkinter.CTk
    
    def __init__(self):
        customtkinter.set_appearance_mode("light") # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue") # Themes: blue (default), dark-blue, green

    def setup(self, width: int = 400, height: int = 240) -> customtkinter.CTk:
        self.ui = customtkinter.CTk() 
        self.ui.geometry(f'{width}x{height}')

        return self.ui
    
    def mainloop(self):
        self.ui.mainloop()

ui = UiInitializer().setup()
layout_controller = LayoutController().set_master(ui)

main_menu = layout_controller.main_menu()

ui.mainloop()