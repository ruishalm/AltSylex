import tkinter as tk
import ttkbootstrap as ttk
from gui.widgets import BotaoOrganico
from tkinter import messagebox, filedialog
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
        self.historico_selecionado = None
        self.historico_processado_selecionado = None
        self.create_widgets()
        self.atualizar_lista_historicos()
        self.atualizar_lista_historicos_processados()
        self.atualizar_lista_palavras()

    def create_widgets(self):
        self.titulo_label = ttk.Label(self, text=f"Educar {self.persona_nome}", font=("Helvetica", 24))
        self.titulo_label.grid(row=0, column=0, columnspan=3, pady=20)

        # --- Coluna 1: Adicionar Histórico e Conteúdos Sensíveis ---
        self.coluna1_frame = ttk.Frame(self, borderwidth=2, relief="groove")
        self.coluna1_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.adicionar_historico_button = BotaoOrganico(self.coluna1_frame, text="Adicionar Histórico", command=self.adicionar_historico, cursor="hand2")
        self.adicionar_historico_button.grid(row=0, column=0, pady=10, padx=5, sticky="ew")

        # --- Frame para Conteúdos Sensíveis ---
        self.conteudos_frame = ttk.Frame(self.coluna1_frame)
        self.conteudos_frame.grid(row=1, column=0, sticky="ew")

        self.conteudos_sensiveis_label = ttk.Label(self.conteudos_frame, text="Conteúdos Sensíveis:", font=("Helvetica", 14)) #renomeado
        self.conteudos_sensiveis_label.grid(row=0, column=0, pady=(5, 0), sticky="w") #renomeado

        self.palavra_entry = ttk.Entry(self.conteudos_frame)
        self.palavra_entry.grid(row=1, column=0, pady=(0, 5), sticky="ew")

        self.adicionar_palavra_button = BotaoOrganico(self.conteudos_frame, text="Adicionar Conteúdo Sensível", command=self.adicionar_palavra, cursor="hand2") #renomeado
        self.adicionar_palavra_button.grid(row=2, column=0, pady=(0, 10), padx=5, sticky="ew")
        # --- Fim do Frame para Conteúdos Sensíveis ---

        self.processar_historico_button = BotaoOrganico(self.coluna1_frame, text="Processar Histórico", command=self.processar_historico, cursor="hand2")
        self.processar_historico_button.grid(row=2, column=0, pady=10, padx=5, sticky="ew")

        # --- Coluna 2: Listas ---
        self.coluna2_frame = ttk.Frame(self, borderwidth=2, relief="groove")
        self.coluna2_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.lista_historicos_label = ttk.Label(self.coluna2_frame, text="Históricos Adicionados:", font=("Helvetica", 14))
        self.lista_historicos_label.grid(row=0, column=0, pady=(20, 5), sticky="w")

        self.lista_historicos = tk.Listbox(self.coluna2_frame, selectmode=tk.SINGLE, height=5)
        self.lista_historicos.grid(row=1, column=0, padx=5, sticky="nsew")
        self.lista_historicos.bind("<<ListboxSelect>>", self.selecionar_historico)

        self.palavras_a_remover_label = ttk.Label(self.coluna2_frame, text="Conteúdos a serem removidos:", font=("Helvetica", 14)) #renomeado
        self.palavras_a_remover_label.grid(row=2, column=0, pady=(20, 0), sticky="w") #renomeado

        self.lista_palavras_censuradas = tk.Listbox(self.coluna2_frame, selectmode=tk.SINGLE, height=5)
        self.lista_palavras_censuradas.grid(row=3, column=0, pady=5, sticky="nsew")

        self.lista_historicos_processados_label = ttk.Label(self.coluna2_frame, text="Históricos Processados:", font=("Helvetica", 14))
        self.lista_historicos_processados_label.grid(row=4, column=0, pady=(20, 5), sticky="w")

        self.lista_historicos_processados = tk.Listbox(self.coluna2_frame, selectmode=tk.SINGLE, height=5)
        self.lista_historicos_processados.grid(row=5, column=0, padx=5, sticky="nsew")
        self.lista_historicos_processados.bind("<<ListboxSelect>>", self.selecionar_historico_processado)

        # --- Coluna 3: Botões de Remoção ---
        self.coluna3_frame = ttk.Frame(self, borderwidth=2, relief="groove")
        self.coluna3_frame.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")

        self.remover_historico_button = BotaoOrganico(self.coluna3_frame, text="Remover Histórico", command=self.remover_historico, cursor="hand2")
        self.remover_historico_button.grid(row=0, column=0, pady=10, padx=5, sticky="ew")

        self.remover_palavra_button = BotaoOrganico(self.coluna3_frame, text="Remover", command=self.remover_palavra, cursor="hand2")
        self.remover_palavra_button.grid(row=1, column=0, pady=5, padx=5, sticky="ew")

        self.deletar_historico_processado_button = BotaoOrganico(self.coluna3_frame, text="Deletar Processado", command=self.deletar_historico_processado, cursor="hand2")
        self.deletar_historico_processado_button.grid(row=2, column=0, pady=10, padx=5, sticky="ew")

        # Configurar o redimensionamento das linhas e colunas
        self.columnconfigure(0, weight=1, minsize=150)
        self.columnconfigure(1, weight=3, minsize=300)
        self.columnconfigure(2, weight=1, minsize=150)
        self.rowconfigure(1, weight=1)

        # Configurar o redimensionamento das linhas e colunas dos frames internos
        self.coluna1_frame.columnconfigure(0, weight=1)
        self.coluna1_frame.rowconfigure(0, weight=1)
        self.coluna1_frame.rowconfigure(1, weight=0)
        self.coluna1_frame.rowconfigure(2, weight=1)

        self.conteudos_frame.columnconfigure(0, weight=1) #renomeado
        for i in range(3):
            self.conteudos_frame.rowconfigure(i, weight=1) #renomeado

        self.coluna2_frame.columnconfigure(0, weight=1)
        for i in range(6):
            self.coluna2_frame.rowconfigure(i, weight=1)

        self.coluna3_frame.columnconfigure(0, weight=1)
        for i in range(3):
            self.coluna3_frame.rowconfigure(i, weight=1)

    def adicionar_historico(self):
        if self.persona_id:
            caminho_arquivo_original = filedialog.askopenfilename(title="Selecionar Arquivo de Histórico", filetypes=[("Arquivos de Texto", "*.txt")])
            if caminho_arquivo_original:
                pasta_historicos = os.path.join(os.path.dirname(__file__), "..", "..", "historicos")
                os.makedirs(pasta_historicos, exist_ok=True)
                nome_arquivo = os.path.basename(caminho_arquivo_original)
                novo_nome_arquivo = f"{self.persona_id}_{nome_arquivo}"
                caminho_arquivo_destino = os.path.join(pasta_historicos, novo_nome_arquivo)
                shutil.copy2(caminho_arquivo_original, caminho_arquivo_destino)
                historico = (self.persona_id, caminho_arquivo_destino)
                database.create_historico(self.conn, historico)
                messagebox.showinfo("Sucesso", f"Histórico adicionado para a persona com ID {self.persona_id}.")
                self.atualizar_lista_historicos()
            else:
                messagebox.showerror("Erro", "Nenhum arquivo selecionado.")
        else:
            messagebox.showerror("Erro", "Nenhuma persona selecionada.")

    def remover_historico(self):
        if self.historico_selecionado:
            resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja remover este histórico?")
            if resposta:
                cur = self.conn.cursor()
                cur.execute("DELETE FROM historico WHERE id=?", (self.historico_selecionado[0],))
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Histórico removido com sucesso.")
                self.atualizar_lista_historicos()
                self.historico_selecionado = None
        else:
            messagebox.showerror("Erro", "Por favor, selecione um histórico.")

    def processar_historico(self):
        if self.historico_selecionado:
            caminho_arquivo = self.historico_selecionado[2]
            persona = database.get_persona(self.conn, self.persona_id)
            persona_nome = persona[1]
            persona_descricao = persona[2]
            mensagens = processador.processar_historico(self.conn, caminho_arquivo, self.persona_id, persona_nome, "Nome — Timestamp")
            nome_arquivo = os.path.basename(caminho_arquivo)
            nome_arquivo_sem_extensao = os.path.splitext(nome_arquivo)[0]
            caminho_json = os.path.join(os.path.dirname(__file__), "..", "..", "jsons", f"{nome_arquivo_sem_extensao}.json")
            processador.gerar_json(mensagens, persona_nome, persona_descricao, "interlocutor", caminho_json)
            messagebox.showinfo("Sucesso", f"Histórico processado e salvo em {caminho_json}")
            self.atualizar_lista_historicos_processados()
        else:
            messagebox.showerror("Erro", "Nenhum histórico selecionado.")

    def deletar_historico_processado(self):
        if self.historico_processado_selecionado:
            resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja remover este histórico processado?")
            if resposta:
                caminho_json = self.historico_processado_selecionado
                os.remove(caminho_json)
                messagebox.showinfo("Sucesso", "Histórico processado removido com sucesso.")
                self.atualizar_lista_historicos_processados()
                self.historico_processado_selecionado = None
        else:
            messagebox.showerror("Erro", "Por favor, selecione um histórico processado.")

    def get_persona_nome(self):
        persona = database.get_persona(self.conn, self.persona_id)
        return persona[1] if persona else "Persona"

    def atualizar_lista_historicos(self):
        self.lista_historicos.delete(0, tk.END)
        historicos = database.get_historicos_by_persona_id(self.conn, self.persona_id)
        for historico in historicos:
            self.lista_historicos.insert(tk.END, f"{historico[2]}")

    def selecionar_historico(self, event):
        try:
            index = self.lista_historicos.curselection()[0]
            historico_selecionado = self.lista_historicos.get(index)
            historicos = database.get_historicos_by_persona_id(self.conn, self.persona_id)
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

    def atualizar_lista_historicos_processados(self):
        self.lista_historicos_processados.delete(0, tk.END)
        pasta_jsons = os.path.join(os.path.dirname(__file__), "..", "..", "jsons")
        arquivos_json = [f for f in os.listdir(pasta_jsons) if os.path.isfile(os.path.join(pasta_jsons, f)) and f.endswith(".json")]
        for arquivo_json in arquivos_json:
            self.lista_historicos_processados.insert(tk.END, os.path.join(pasta_jsons, arquivo_json))

    def selecionar_historico_processado(self, event):
        try:
            index = self.lista_historicos_processados.curselection()[0]
            self.historico_processado_selecionado = self.lista_historicos_processados.get(index)
        except IndexError:
            pass
