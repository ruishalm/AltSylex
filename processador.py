import re
import json
from database import get_all_palavras_chave
from gerenciador_arquivos import GerenciadorArquivos  # Importando o GerenciadorArquivos

def extrair_mensagem(linha, persona_nome):
    """Extrai o nome do orador e o conteúdo da mensagem de uma linha."""
    # Padrão para encontrar o timestamp no formato HH:MM ou DD/MM/AAAA
    padrao_timestamp = r"(\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}|\d{2}:\d{2})"
    # Remove o timestamp da linha, se existir
    linha_sem_timestamp = re.sub(padrao_timestamp, "", linha).strip()

    # Divide a linha no primeiro ": " (dois pontos seguido de um espaço)
    partes = linha_sem_timestamp.split(": ", 1)

    if len(partes) == 2:
        orador = partes[0].strip()
        mensagem = partes[1].strip()
        # Remove o "-" se ele estiver no final do nome do orador
        if orador.endswith("-"):
            orador = orador[:-1].strip()
        # Remove o "-" se ele estiver no meio do nome do orador
        orador = orador.replace("-", "").strip()
        return {
            "orador": orador,
            "mensagem": mensagem
        }
    else:
        # Divide a linha no primeiro ":"
        partes = linha_sem_timestamp.split(":", 1)
        if len(partes) == 2:
            orador = partes[0].strip()
            mensagem = partes[1].strip()
            # Remove o "-" se ele estiver no final do nome do orador
            if orador.endswith("-"):
                orador = orador[:-1].strip()
            # Remove o "-" se ele estiver no meio do nome do orador
            orador = orador.replace("-", "").strip()
            return {
                "orador": orador,
                "mensagem": mensagem
            }
        else:
            return {
                "orador": persona_nome,
                "mensagem": linha.strip()
            }

def processar_historico(conn, conteudo_arquivo, persona_id, persona_nome):
    """Processa um conteúdo de histórico, linha por linha."""
    palavras_chave = get_all_palavras_chave(conn)
    palavras_censuradas = [palavra[1] for palavra in palavras_chave]
    mensagens = []
    try:
        for linha in conteudo_arquivo.splitlines():  # Processa o conteúdo linha por linha
            linha = linha.strip()
            dados_mensagem = extrair_mensagem(linha, persona_nome)
            if dados_mensagem:
                orador = dados_mensagem["orador"]
                mensagem = dados_mensagem["mensagem"].strip()
                palavras_censuradas_atual = []
                for palavra in palavras_censuradas:
                    if palavra in mensagem:
                        palavras_censuradas_atual.append(palavra)
                        mensagem = mensagem.replace(palavra, "[CENSURADO]")

                mensagens.append({
                    "orador": orador,
                    "mensagem": mensagem,
                    "palavras_censuradas": palavras_censuradas_atual
                })
            else:
                if mensagens:
                    mensagens[-1]["mensagem"] += "\n" + linha
        return mensagens
    except Exception as e:
        print(f"Erro ao processar o conteúdo: {e}")
        return []

def gerar_json(falas, persona_nome, persona_descricao, interlocutor_nome, caminho_arquivo, gerenciador_arquivos):
    """Gera um arquivo JSON com as conversas."""
    estrutura_json = {
        "persona": {
            "nome": persona_nome,
            "descricao": persona_descricao
        },
        "interlocutor": interlocutor_nome,
        "conversas": falas
    }
    gerenciador_arquivos.escrever_json(caminho_arquivo, estrutura_json) # Usa o gerenciador para escrever o JSON

    return caminho_arquivo

def processar_historico_completo(conn, caminho_arquivo, persona_id, persona_nome, persona_descricao, gerenciador_arquivos):
    """Processa um histórico completo e gera o arquivo JSON."""
    conteudo_arquivo = gerenciador_arquivos.ler_arquivo(caminho_arquivo)
    if conteudo_arquivo is None:
        return None  # Retorna None se o arquivo não puder ser lido

    mensagens = processar_historico(conn, conteudo_arquivo, persona_id, persona_nome)
    nome_arquivo = os.path.basename(caminho_arquivo)
    nome_arquivo_sem_extensao = os.path.splitext(nome_arquivo)[0]
    caminho_json = gerenciador_arquivos.gerar_caminho_json(nome_arquivo_sem_extensao)
    gerar_json(mensagens, persona_nome, persona_descricao, "interlocutor", caminho_json, gerenciador_arquivos)
    return caminho_json
