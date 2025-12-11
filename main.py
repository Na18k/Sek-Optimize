from gui import GUI
from app import App
import tkinter as tk


def main():
    root = tk.Tk()

    app_instance = App(None)

    gui = GUI(root, app_instance.execute_button)
    app_instance.gui = gui

    root.mainloop()


if __name__ == "__main__":
    main()
