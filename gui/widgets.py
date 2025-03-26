import tkinter as tk
import ttkbootstrap as ttk

class BotaoOrganico(ttk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, style="success", **kwargs)
