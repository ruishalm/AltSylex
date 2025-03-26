import tkinter as tk
import ttkbootstrap as ttk
from gui.widgets import BotaoOrganico
from tkinter import messagebox
import database

class TelaGerenciarPersonas(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.master = master
        self.conn = app.conn
        self.persona_selecionada_id = None
        self.create_widgets()
        self.atualizar_lista_personas()

    def create_widgets(self):
        # Título
        self.titulo_label = ttk.Label(self, text="Gerenciar Personas", font=("Helvetica", 24))
        self.titulo_label.pack(pady=20)

        # Frame para os botões
        self.botoes_frame = ttk.Frame(self)
        self.botoes_frame.pack(pady=10)

        # Botões - Esquerda
        self.criar_persona_button = BotaoOrganico(self.botoes_frame, text="Gerar Persona", command=self.criar_persona, cursor="hand2")
        self.criar_persona_button.pack(side=tk.LEFT, padx=5)

        self.educar_persona_button = BotaoOrganico(self.botoes_frame, text="Educar Persona", command=self.educar_persona, cursor="hand2")
        self.educar_persona_button.pack(side=tk.LEFT, padx=5)

        # Botões - Direita
        self.desviver_persona_button = BotaoOrganico(self.botoes_frame, text="Desviver Persona", command=self.desviver_persona, cursor="hand2")
        self.desviver_persona_button.pack(side=tk.RIGHT, padx=5)

        # Frame para a lista
        self.lista_frame = ttk.Frame(self)
        self.lista_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        # Lista de Personas
        self.lista_personas_label = ttk.Label(self.lista_frame, text="Personas Existentes:", font=("Helvetica", 14))
        self.lista_personas_label.pack(pady=(20, 5))

        self.lista_personas = tk.Listbox(self.lista_frame, selectmode=tk.SINGLE, height=5)
        self.lista_personas.pack(fill=tk.BOTH, expand=True)
        self.lista_personas.bind("<<ListboxSelect>>", self.selecionar_persona)

    def criar_persona(self):
        # Criar uma nova janela para inserir o nome e a descrição da persona
        self.criar_persona_window = ttk.Toplevel(self)
        self.criar_persona_window.title("Criar Persona")

        # Nome
        self.nome_label = ttk.Label(self.criar_persona_window, text="Nome:")
        self.nome_label.pack(pady=5)
        self.nome_entry = ttk.Entry(self.criar_persona_window)
        self.nome_entry.pack(pady=5)

        # Descrição
        self.descricao_label = ttk.Label(self.criar_persona_window, text="Descrição:")
        self.descricao_label.pack(pady=5)
        self.descricao_entry = ttk.Entry(self.criar_persona_window)
        self.descricao_entry.pack(pady=5)

        # Botão Criar
        self.criar_button = BotaoOrganico(self.criar_persona_window, text="Criar", command=self.salvar_persona, cursor="hand2")
        self.criar_button.pack(pady=10)

    def salvar_persona(self):
        nome = self.nome_entry.get()
        descricao = self.descricao_entry.get()

        if not nome or not descricao:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        if database.check_persona_exists(self.conn, nome):
            if not messagebox.askyesno("Aviso", f"Já existe uma persona com o nome '{nome}'. Deseja criar mesmo assim?"):
                return

        persona = (nome, descricao)
        persona_id = database.create_persona(self.conn, persona)
        messagebox.showinfo("Sucesso", f"Persona '{nome}' criada com ID {persona_id}.")
        self.criar_persona_window.destroy()
        self.atualizar_lista_personas()

    def atualizar_lista_personas(self):
        # Limpa a lista
        self.lista_personas.delete(0, tk.END)

        # Busca todas as personas do banco de dados
        personas = database.get_all_personas(self.conn)

        # Adiciona as personas à lista
        for persona in personas:
            self.lista_personas.insert(tk.END, f"ID: {persona[0]} - {persona[1]}")

    def selecionar_persona(self, event):
        # Obtém o índice do item selecionado
        try:
            index = self.lista_personas.curselection()[0]
            # Obtém o texto do item selecionado
            persona_selecionada = self.lista_personas.get(index)
            # Extrai o ID da persona do texto
            self.persona_selecionada_id = int(persona_selecionada.split(" - ")[0].split(": ")[1])
        except IndexError:
            pass

    def educar_persona(self):
        if self.persona_selecionada_id:
            self.app.educar_persona(self.persona_selecionada_id)
        else:
            messagebox.showerror("Erro", "Por favor, selecione uma persona.")

    def desviver_persona(self):
        if self.persona_selecionada_id:
            # Exibe uma mensagem de confirmação
            resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja desviver esta persona?")
            if resposta:
                database.delete_persona(self.conn, self.persona_selecionada_id)
                messagebox.showinfo("Sucesso", "Persona desvivida com sucesso.")
                self.atualizar_lista_personas()
                self.persona_selecionada_id = None
        else:
            messagebox.showerror("Erro", "Por favor, selecione uma persona.")
