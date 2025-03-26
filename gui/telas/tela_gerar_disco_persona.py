import tkinter as tk
import ttkbootstrap as ttk

class TelaGerarDiscoPersona(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Título
        self.titulo_label = ttk.Label(self, text="Gerar Disco de Persona", font=("Helvetica", 24))
        self.titulo_label.pack(pady=20)
