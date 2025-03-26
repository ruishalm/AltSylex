import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
import database
import os
from gui.widgets import BotaoOrganico
from gui.telas.tela_inicial import TelaInicial
from gui.telas.tela_gerenciar_personas import TelaGerenciarPersonas
from gui.telas.tela_educar_persona import TelaEducarPersona
from gui.telas.tela_gerar_disco_persona import TelaGerarDiscoPersona


class AltSylexApp:
    def __init__(self, master, conn):
        self.master = master
        master.title("AltSylex")
        self.conn = conn

        # Estilo
        self.style = ttk.Style(theme="darkly")
        self.style.configure("NavFrame.TFrame", background="black")

        # Frame de navegação (Anterior e Home) - TOPO ABSOLUTO
        self.nav_frame = ttk.Frame(master, style="NavFrame.TFrame")
        self.nav_frame.pack(side=tk.TOP, fill=tk.X)

        # Botão Anterior (Unicode: ←)
        self.anterior_button = ttk.Button(
            self.nav_frame,
            text="←",
            command=self.anterior,
            state=tk.DISABLED,
            style="link",
            width=5
        )
        self.anterior_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Botão Home (Unicode: 🏠)
        self.home_button = ttk.Button(
            self.nav_frame,
            text="🏠",
            command=self.mostrar_tela_inicial,
            style="link",
            width=5
        )
        self.home_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Frame principal (Conteúdo das telas)
        self.main_frame = ttk.Frame(master, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame do botão Sair (Rodapé)
        self.sair_frame = ttk.Frame(master)
        self.sair_frame.pack(side=tk.BOTTOM, fill=tk.X, anchor=tk.SE)

        # Botão Sair
        self.sair_button = ttk.Button(self.sair_frame, text="Sair", command=self.sair)
        self.sair_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Histórico de Telas
        self.historico_telas = []

        # Tela Inicial
        self.mostrar_tela_inicial()

    def mostrar_tela_inicial(self):
        self.clear_frame()
        self.historico_telas = []
        self.anterior_button.config(state=tk.DISABLED, cursor="arrow")
        tela = TelaInicial(self.main_frame, self)
        tela.pack(fill=tk.BOTH, expand=True)

    def gerenciar_personas(self):
        self.clear_frame()
        self.historico_telas.append(self.gerenciar_personas)
        self.anterior_button.config(state=tk.NORMAL, cursor="hand2")
        tela = TelaGerenciarPersonas(self.main_frame, self)
        tela.pack(fill=tk.BOTH, expand=True)

    def educar_persona(self, persona_id=None):
        self.clear_frame()
        self.historico_telas.append(self.educar_persona)
        self.anterior_button.config(cursor="hand2")
        tela = TelaEducarPersona(self.main_frame, self, persona_id)
        tela.pack(fill=tk.BOTH, expand=True)

    def gerar_disco_persona(self): #removido o parametro persona_id
        self.clear_frame()
        self.historico_telas.append(self.gerar_disco_persona) #removido o parametro persona_id
        self.anterior_button.config(cursor="hand2")
        tela = TelaGerarDiscoPersona(self.main_frame, self) #removido o parametro persona_id
        tela.pack(fill=tk.BOTH, expand=True)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()

    def sair(self):
        self.master.destroy()

    def anterior(self):
        if self.historico_telas:
            self.historico_telas.pop()
            if self.historico_telas:
                tela_anterior = self.historico_telas[-1]
                if isinstance(tela_anterior, tuple):
                    tela_anterior[0](*tela_anterior[1])
                else:
                    tela_anterior()
            else:
                self.mostrar_tela_inicial()
