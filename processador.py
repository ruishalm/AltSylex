import os
import re
import json
from database import get_all_palavras_chave

def extrair_mensagem(linha, formato_cabecalho, persona_nome):
    """Extrai o nome do orador e o conteúdo da mensagem de uma linha."""
    if formato_cabecalho == "Nome — Timestamp":
        padrao = r"^(.*?) — (.*?)$"  # Padrão para "Nome — Timestamp"
        match = re.match(padrao, linha)
        if match:
            orador = match.group(1)
            resto = match.group(2)
            # Tenta encontrar o timestamp no formato HH:MM ou DD/MM/AAAA
            padrao_timestamp = r"(\d{2}/\d{2}/\d{4}|\d{2}:\d{2})"
            mensagem = re.sub(padrao_timestamp, "", resto)
            return {
                "orador": orador,
                "mensagem": mensagem.strip()
            }
        else:
            return None
    else:
        return {
            "orador": persona_nome,
            "mensagem": linha.strip()
        }

def processar_historico(conn, caminho_arquivo, persona_id, persona_nome, formato_cabecalho):
    """Processa um arquivo de histórico, linha por linha."""
    caminho_absoluto = os.path.join(os.path.dirname(__file__), caminho_arquivo)
    palavras_chave = get_all_palavras_chave(conn)
    palavras_censuradas = [palavra[1] for palavra in palavras_chave]
    mensagens = []
    try:
        with open(caminho_absoluto, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                dados_mensagem = extrair_mensagem(linha, formato_cabecalho, persona_nome)
                if dados_mensagem:
                    orador = dados_mensagem["orador"]
                    mensagem = dados_mensagem["mensagem"].strip()
                    # Nova lógica para definir a fonte
                    fonte = "persona" if orador.lower() == persona_nome.lower() else "interlocutor"
                    palavras_censuradas_atual = []
                    for palavra in palavras_censuradas:
                        if palavra in mensagem:
                            palavras_censuradas_atual.append(palavra)
                            mensagem = mensagem.replace(palavra, "[CENSURADO]")
                    
                    mensagens.append({
                        "orador": orador,
                        "mensagem": mensagem,
                        "fonte": fonte,
                        "palavras_censuradas": palavras_censuradas_atual
                    })
                else:
                    if mensagens:
                        mensagens[-1]["mensagem"] += "\n" + linha
        return mensagens
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {caminho_absoluto}")
        return []
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        return []

def gerar_json(falas, persona_nome, persona_descricao, interlocutor_nome, caminho_arquivo):
    """Gera um arquivo JSON com as conversas."""
    estrutura_json = {
        "persona": {
            "nome": persona_nome,
            "descricao": persona_descricao
        },
        "interlocutor": interlocutor_nome,
        "conversas": falas
    }
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(estrutura_json, f, indent=4, ensure_ascii=False)

    return caminho_arquivo
