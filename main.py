import tkinter as tk
from gui import GUI
from app import App

def main():
    root = tk.Tk()

    app_instance = App()
    gui = GUI(root, app_instance)

    app_instance.set_gui(gui)

    app_instance.show_fetch()

    root.mainloop()

if __name__ == "__main__":
    main()
