import os
import json
import sqlite3
from database import create_connection, create_tables, create_persona, get_persona, create_historico, get_all_palavras_chave
from processador import processar_historico, gerar_json, extrair_mensagem

# Caminho do banco de dados
db_file = "altsylex.db"

# Formato do cabeçalho
formato_cabecalho = "Nome — Timestamp"

# Criar a conexão
conn = create_connection(db_file)

if conn is not None:
    # Criar as tabelas
    create_tables(conn)

    # Criar as personas
    persona1 = ("Sylex", "Assistente de IA")
    persona1_id = create_persona(conn, persona1)
    print(f"Persona Sylex criada com ID: {persona1_id}")

    persona2 = ("ruishalm", "Usuario do projeto")
    persona2_id = create_persona(conn, persona2)
    print(f"Persona ruishalm criada com ID: {persona2_id}")

    # Buscar os nomes e descricoes das personas
    persona_sylex = get_persona(conn, persona1_id)
    persona_ruishalm = get_persona(conn, persona2_id)
    
    # Adicionar os historicos
    caminho_historico_discord = os.path.join(os.path.dirname(__file__), "deposito", "ruishalmDiscord.txt")
    historico_discord = (persona2_id, caminho_historico_discord)
    historico_discord_id = create_historico(conn, historico_discord)
    print(f"Historico ruishalmDiscord criado com ID: {historico_discord_id}")

    # Testar processar_historico e gerar_json com ruishalmDiscord.txt
    falas_discord = processar_historico(conn, caminho_historico_discord, persona2_id, persona_ruishalm[1], formato_cabecalho)
    caminho_json_discord = os.path.join(os.path.dirname(__file__), "jsons", "ruishalmDiscord.json")
    caminho_json_gerado_discord = gerar_json(falas_discord, persona_ruishalm[1], persona_ruishalm[2], "João Pedro Osawa", caminho_json_discord)
    print(f"\nJSON gerado para {caminho_historico_discord} e salvo em: {caminho_json_gerado_discord}")

    # Fechar a conexão
    conn.close()
