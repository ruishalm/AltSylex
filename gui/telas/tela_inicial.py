import tkinter as tk
import ttkbootstrap as ttk
from gui.widgets import BotaoOrganico

class TelaInicial(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Título
        self.titulo_label = ttk.Label(self, text="AltSylex", font=("Helvetica", 30))
        self.titulo_label.pack(pady=20)

        # Botões
        self.gerenciar_personas_button = BotaoOrganico(self, text="Gerenciar Personas", command=self.app.gerenciar_personas, cursor="hand2")
        self.gerenciar_personas_button.pack(pady=10)

        self.gerar_disco_persona_button = BotaoOrganico(self, text="Gerar Disco de Persona", command=self.app.gerar_disco_persona, cursor="hand2") #removido o parametro
        self.gerar_disco_persona_button.pack(pady=10)
