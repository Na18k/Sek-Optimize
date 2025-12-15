import tkinter as tk
from gui import GUI
from app import App

def main():
    root = tk.Tk()

    app_instance = App(None)
    gui = GUI(root, app_instance.execute_button)

    app_instance.set_gui(gui)
    app_instance.on_gui_ready(gui)

    root.mainloop()


if __name__ == "__main__":
    main()
