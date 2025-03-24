import database
import os
import re
import json

def processar_historico(conn, caminho_arquivo, persona_id, persona_nome, interlocutor_nome, identificador_interlocutor=None):
    caminho_absoluto = os.path.join(os.path.dirname(__file__), caminho_arquivo)
    palavras_chave = database.get_all_palavras_chave(conn)
    palavras_censuradas = [palavra[1] for palavra in palavras_chave]
    try:
        with open(caminho_absoluto, "r", encoding="utf-8") as f:
            falas = []
            cabecalho_atual = None
            corpo_mensagem = ""
            nome_interlocutor_atual = None
            palavras_censuradas_atual = []
            for linha in f:
                linha = linha.strip()
                if identificador_interlocutor and re.match(identificador_interlocutor, linha):
                    nome_interlocutor_atual = re.match(identificador_interlocutor, linha).group(1)
                    if cabecalho_atual:
                        tipo = "persona" if nome_interlocutor_atual == persona_nome else "interlocutor"
                        falas.append({
                            "cabecalho": cabecalho_atual,
                            "fala": corpo_mensagem.strip(),
                            "tipo": tipo,
                            "interlocutor": nome_interlocutor_atual,
                            "palavras_censuradas": palavras_censuradas_atual
                        })
                    cabecalho_atual = linha
                    corpo_mensagem = ""
                    palavras_censuradas_atual = []
                elif re.match(r"(.*?) — (.*?)", linha) or re.match(r"(.*?):", linha) or re.match(r"(.*?)\s", linha) or re.match(r"(.*)", linha):
                    if cabecalho_atual:
                        tipo = "persona" if nome_interlocutor_atual == persona_nome else "interlocutor"
                        falas.append({
                            "cabecalho": cabecalho_atual,
                            "fala": corpo_mensagem.strip(),
                            "tipo": tipo,
                            "interlocutor": nome_interlocutor_atual,
                            "palavras_censuradas": palavras_censuradas_atual
                        })
                    cabecalho_atual = linha
                    corpo_mensagem = ""
                    palavras_censuradas_atual = []
                    if re.match(r"(.*?) — (.*?)", linha):
                        nome_interlocutor_atual = re.match(r"(.*?) — (.*?)", linha).group(1)
                    elif re.match(r"(.*?):", linha):
                        nome_interlocutor_atual = re.match(r"(.*?):", linha).group(1)
                    elif re.match(r"(.*?)\s", linha):
                        nome_interlocutor_atual = re.match(r"(.*?)\s", linha).group(1)
                    elif re.match(r"(.*)", linha):
                        nome_interlocutor_atual = re.match(r"(.*)", linha).group(1)
                else:
                    corpo_mensagem += linha + "\n"
                    for palavra in palavras_censuradas:
                        if palavra in linha:
                            palavras_censuradas_atual.append(palavra)
                        corpo_mensagem = corpo_mensagem.replace(palavra, "[CENSURADO]")
            if cabecalho_atual:
                tipo = "persona" if nome_interlocutor_atual == persona_nome else "interlocutor"
                falas.append({
                    "cabecalho": cabecalho_atual,
                    "fala": corpo_mensagem.strip(),
                    "tipo": tipo,
                    "interlocutor": nome_interlocutor_atual,
                    "palavras_censuradas": palavras_censuradas_atual
                })
            return falas
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {caminho_absoluto}")
        return []
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        return []

def gerar_json(falas, persona_nome, persona_descricao, interlocutor_nome, caminho_arquivo):
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
