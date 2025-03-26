import tkinter as tk
import ttkbootstrap as ttk
from gui.widgets import BotaoOrganico
from tkinter import messagebox, filedialog, scrolledtext
import database
import shutil
import os
import processador

class TelaEducarPersona(ttk.Frame):
    def __init__(self, master, app, persona_id=None):
        super().__init__(master)
        self.app = app
        self.master = master
        self.persona_id = persona_id
        self.conn = app.conn
        self.persona_nome = self.get_persona_nome()
        self.create_widgets()
        self.atualizar_lista_historicos()
        self.historico_selecionado = None

    def create_widgets(self):
        # Título
        self.titulo_label = ttk.Label(self, text=f"Educar {self.persona_nome}", font=("Helvetica", 24))
        self.titulo_label.pack(pady=20)

        # Botões
        self.adicionar_historico_button = BotaoOrganico(self, text="Adicionar Histórico", command=self.adicionar_historico, cursor="hand2")
        self.adicionar_historico_button.pack(pady=10)

        self.processar_historico_button = BotaoOrganico(self, text="Processar Histórico", command=self.processar_historico, cursor="hand2")
        self.processar_historico_button.pack(pady=10)

        # Frame para a lista
        self.lista_frame = ttk.Frame(self)
        self.lista_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        # Lista de Históricos
        self.lista_historicos_label = ttk.Label(self.lista_frame, text="Históricos Adicionados:", font=("Helvetica", 14))
        self.lista_historicos_label.pack(pady=(20, 5))

        self.lista_historicos = tk.Listbox(self.lista_frame, selectmode=tk.SINGLE, height=5)
        self.lista_historicos.pack(fill=tk.BOTH, expand=True)
        self.lista_historicos.bind("<<ListboxSelect>>", self.selecionar_historico)

        # Frame para as palavras censuradas
        self.palavras_frame = ttk.Frame(self)
        self.palavras_frame.pack(pady=10)

        # Palavras Censuradas
        self.palavras_censuradas_label = ttk.Label(self.palavras_frame, text="Palavras Censuradas:", font=("Helvetica", 14))
        self.palavras_censuradas_label.pack(side=tk.LEFT, padx=5)

        self.palavra_entry = ttk.Entry(self.palavras_frame)
        self.palavra_entry.pack(side=tk.LEFT, padx=5)

        self.adicionar_palavra_button = BotaoOrganico(self.palavras_frame, text="Adicionar", command=self.adicionar_palavra, cursor="hand2")
        self.adicionar_palavra_button.pack(side=tk.LEFT, padx=5)

        self.remover_palavra_button = BotaoOrganico(self.palavras_frame, text="Remover", command=self.remover_palavra, cursor="hand2")
        self.remover_palavra_button.pack(side=tk.LEFT, padx=5)

        # Lista de Palavras Censuradas
        self.lista_palavras_censuradas = tk.Listbox(self, selectmode=tk.SINGLE, height=5)
        self.lista_palavras_censuradas.pack(fill=tk.BOTH, expand=True, padx=10)
        self.atualizar_lista_palavras()

    def adicionar_historico(self):
        if self.persona_id:
            caminho_arquivo_original = filedialog.askopenfilename(title="Selecionar Arquivo de Histórico", filetypes=[("Arquivos de Texto", "*.txt")])
            if caminho_arquivo_original:
                # Criar a pasta "historicos" se ela não existir
                pasta_historicos = os.path.join(os.path.dirname(__file__), "..", "..", "historicos")
                os.makedirs(pasta_historicos, exist_ok=True)

                # Criar um novo nome de arquivo único
                nome_arquivo = os.path.basename(caminho_arquivo_original)
                novo_nome_arquivo = f"{self.persona_id}_{nome_arquivo}"
                caminho_arquivo_destino = os.path.join(pasta_historicos, novo_nome_arquivo)

                # Copiar o arquivo para a pasta "historicos"
                shutil.copy2(caminho_arquivo_original, caminho_arquivo_destino)

                # Salvar o novo caminho no banco de dados
                historico = (self.persona_id, caminho_arquivo_destino)
                database.create_historico(self.conn, historico)
                messagebox.showinfo("Sucesso", f"Histórico adicionado para a persona com ID {self.persona_id}.")
                self.atualizar_lista_historicos()
            else:
                messagebox.showerror("Erro", "Nenhum arquivo selecionado.")
        else:
            messagebox.showerror("Erro", "Nenhuma persona selecionada.")

    def processar_historico(self):
        if self.historico_selecionado:
            # Obter o caminho do arquivo selecionado
            caminho_arquivo = self.historico_selecionado[2]
            # Obter o nome e a descrição da persona
            persona = database.get_persona(self.conn, self.persona_id)
            persona_nome = persona[1]
            persona_descricao = persona[2]

            # Processar o histórico
            mensagens = processador.processar_historico(self.conn, caminho_arquivo, self.persona_id, persona_nome, "Nome — Timestamp")

            # Gerar o JSON
            nome_arquivo = os.path.basename(caminho_arquivo)
            nome_arquivo_sem_extensao = os.path.splitext(nome_arquivo)[0]
            caminho_json = os.path.join(os.path.dirname(__file__), "..", "..", "jsons", f"{nome_arquivo_sem_extensao}.json")
            processador.gerar_json(mensagens, persona_nome, persona_descricao, "interlocutor", caminho_json)

            messagebox.showinfo("Sucesso", f"Histórico processado e salvo em {caminho_json}")
        else:
            messagebox.showerror("Erro", "Nenhum histórico selecionado.")

    def get_persona_nome(self):
        persona = database.get_persona(self.conn, self.persona_id)
        return persona[1] if persona else "Persona"

    def atualizar_lista_historicos(self):
        # Limpa a lista
        self.lista_historicos.delete(0, tk.END)

        # Busca todos os historicos da persona do banco de dados
        historicos = database.get_historicos_by_persona_id(self.conn, self.persona_id)

        # Adiciona os historicos à lista
        for historico in historicos:
            self.lista_historicos.insert(tk.END, f"{historico[2]}")

    def selecionar_historico(self, event):
        # Obtém o índice do item selecionado
        try:
            index = self.lista_historicos.curselection()[0]
            # Obtém o texto do item selecionado
            historico_selecionado = self.lista_historicos.get(index)
            # Busca todos os historicos da persona do banco de dados
            historicos = database.get_historicos_by_persona_id(self.conn, self.persona_id)
            # Procura o historico selecionado
            for historico in historicos:
                if historico[2] == historico_selecionado:
                    self.historico_selecionado = historico
                    break
        except IndexError:
            pass

    def adicionar_palavra(self):
        palavra = self.palavra_entry.get().strip()
        if palavra:
            database.create_palavra_chave(self.conn, palavra)
            self.palavra_entry.delete(0, tk.END)
            self.atualizar_lista_palavras()
        else:
            messagebox.showerror("Erro", "Por favor, digite uma palavra.")

    def remover_palavra(self):
        try:
            index = self.lista_palavras_censuradas.curselection()[0]
            palavra = self.lista_palavras_censuradas.get(index)
            database.delete_palavra_chave(self.conn, palavra)
            self.atualizar_lista_palavras()
        except IndexError:
            messagebox.showerror("Erro", "Por favor, selecione uma palavra para remover.")

    def atualizar_lista_palavras(self):
        self.lista_palavras_censuradas.delete(0, tk.END)
        palavras = database.get_all_palavras_chave(self.conn)
        for palavra in palavras:
            self.lista_palavras_censuradas.insert(tk.END, palavra[1])
