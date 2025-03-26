import tkinter as tk
import ttkbootstrap as ttk
from gui.widgets import BotaoOrganico
import database
import processador
from tkinter import messagebox, filedialog  # Importado o filedialog
import os
import json

class TelaGerarDiscoPersona(ttk.Frame):
    def __init__(self, master, app, persona_id=None):
        super().__init__(master)
        self.app = app
        self.master = master
        self.conn = app.conn
        self.persona_id = persona_id
        self.persona_selecionada_id = None
        self.create_widgets()
        self.atualizar_lista_personas()

    def create_widgets(self):
        # Título
        self.titulo_label = ttk.Label(self, text="Gerar Disco de Persona", font=("Helvetica", 24))
        self.titulo_label.pack(pady=20)

        # Lista de Personas
        self.lista_personas_label = ttk.Label(self, text="Selecione a Persona:", font=("Helvetica", 14))
        self.lista_personas_label.pack(pady=(20, 5))

        self.lista_personas = tk.Listbox(self, selectmode=tk.SINGLE, height=5)
        self.lista_personas.pack(fill=tk.BOTH, expand=True, padx=10)
        self.lista_personas.bind("<<ListboxSelect>>", self.selecionar_persona)

        # Botão Gerar Disco de Persona
        self.gerar_disco_button = BotaoOrganico(self, text="Gerar Disco de Persona", command=self.gerar_disco, cursor="hand2")
        self.gerar_disco_button.pack(pady=20)

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

    def gerar_disco(self):
        if self.persona_selecionada_id:
            # Obter o nome e a descrição da persona
            persona = database.get_persona(self.conn, self.persona_selecionada_id)
            persona_nome = persona[1]
            persona_descricao = persona[2]

            # Buscar todos os arquivos JSON na pasta "jsons" que correspondam à persona
            pasta_jsons = os.path.join(os.path.dirname(__file__), "..", "..", "jsons")
            arquivos_json = [f for f in os.listdir(pasta_jsons) if os.path.isfile(os.path.join(pasta_jsons, f)) and f.startswith(f"{persona_nome}")]

            # Concatenar as conversas de todos os arquivos JSON
            todas_conversas = []
            for arquivo_json in arquivos_json:
                caminho_json = os.path.join(pasta_jsons, arquivo_json)
                with open(caminho_json, "r", encoding="utf-8") as f:
                    dados_json = json.load(f)
                    todas_conversas.extend(dados_json["conversas"])

            # Instruções detalhadas para a IA
            instrucoes = f"""
            Você está recebendo um conjunto de dados que representa um 'disco' de uma persona chamada '{persona_nome}'. Este disco contém conversas que foram coletadas e processadas para capturar o estilo de comunicação e a personalidade da persona.

            Aqui estão as diretrizes para interpretar e usar esses dados:

            1.  **Objetivo:** O objetivo principal é que você, como IA, aprenda e imite o estilo de comunicação e a personalidade da persona '{persona_nome}'.
            2.  **Falas da Persona:** As falas marcadas com a fonte 'persona' são as mais importantes. Elas representam a forma como a persona se expressa, suas preferências de linguagem, seu tom e sua personalidade. Use essas falas como base para moldar sua própria comunicação.
            3.  **Falas do Interlocutor:** As falas marcadas com a fonte 'interlocutor' estão incluídas apenas para fornecer contexto. Elas mostram como a persona interage com outras pessoas e como ela responde a diferentes estímulos. Não use as falas do interlocutor para definir seu próprio estilo de comunicação.
            4.  **Conteúdos Sensíveis:** Alguns dados foram substituídos por '[CENSURADO]'. Isso indica que a conversa continha informações sensíveis, como endereços, senhas ou outros dados privados. Você deve evitar o uso desses dados, a menos que seja explicitamente instruído a fazê-lo.
            5.  **Contexto:** Preste atenção ao contexto das conversas. Como a persona responde a perguntas? Como ela inicia conversas? Como ela expressa suas opiniões? Como ela reage a diferentes emoções?
            6.  **Formato:** O formato do arquivo é um JSON. Ele contém uma lista de conversas, onde cada conversa tem um orador, uma mensagem, uma fonte e uma lista de conteúdos sensíveis.
            7.  **Nome e Descrição:** O nome e a descrição da persona estão no topo do arquivo. Use essas informações para entender melhor a identidade da persona.

            Lembre-se: Seu objetivo é se tornar uma extensão da persona '{persona_nome}', imitando seu estilo de comunicação e personalidade. Use as falas da persona como seu guia principal e as falas do interlocutor apenas para entender o contexto.
            """

            # Estrutura do JSON final
            json_final = {
                "persona": {
                    "nome": persona_nome,
                    "descricao": persona_descricao
                },
                "instrucoes": instrucoes,
                "conversas": todas_conversas
            }

            # Salvar o JSON final
            nome_arquivo = f"AltSylex de {persona_nome}"
            caminho_json_final = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("Arquivos JSON", "*.json")],
                initialfile=nome_arquivo,
                title="Salvar Disco de Persona"
            )

            if caminho_json_final:
                with open(caminho_json_final, "w", encoding="utf-8") as f:
                    json.dump(json_final, f, indent=4, ensure_ascii=False)
                messagebox.showinfo("Sucesso", f"Disco de persona gerado e salvo em {caminho_json_final}")
            else:
                messagebox.showinfo("Aviso", "Geração de disco cancelada.")
        else:
            messagebox.showerror("Erro", "Por favor, selecione uma persona.")
