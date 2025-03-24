import database
import processador
import os
import json

# Caminho do banco de dados
db_file = "altsylex.db"

# Criar a conexão
conn = database.create_connection(db_file)

if conn is not None:
    # Criar as personas
    persona1 = ("Sylex", "Assistente de IA")
    persona1_id = database.create_persona(conn, persona1)
    print(f"Persona Sylex criada com ID: {persona1_id}")

    persona2 = ("ruishalm", "Usuario do projeto")
    persona2_id = database.create_persona(conn, persona2)
    print(f"Persona ruishalm criada com ID: {persona2_id}")

    # Buscar os nomes e descricoes das personas
    persona = database.get_persona(conn, persona2_id)
    interlocutor_nome = persona[1]
    interlocutor_descricao = persona[2]

    # Adicionar os historicos
    caminho_absoluto_historico = os.path.join(os.path.dirname(__file__), "deposito", "ruishalmDiscord.txt")
    historico3 = (persona2_id, caminho_absoluto_historico)
    historico3_id = database.create_historico(conn, historico3)
    print(f"Historico criado com ID: {historico3_id}")

    # Testar processar_historico e gerar_json com ruishalmDiscord.txt
    caminho_absoluto = os.path.join(os.path.dirname(__file__), "deposito", "ruishalmDiscord.txt")
    falas = processador.processar_historico(conn, caminho_absoluto, persona2_id, interlocutor_nome, "João Pedro Osawa", identificador_interlocutor=r"\[(.*?) — (.*?)\]")
    
    # Definir o caminho do arquivo JSON
    caminho_json = os.path.join(os.path.dirname(__file__), "jsons", "ruishalmDiscord.json")
    
    # Gerar o JSON e salvar no arquivo
    caminho_json_gerado = processador.gerar_json(falas, interlocutor_nome, interlocutor_descricao, "João Pedro Osawa", caminho_json)
    print(f"\nJSON gerado para {caminho_absoluto} e salvo em: {caminho_json_gerado}")

    # Fechar a conexão
    conn.close()
