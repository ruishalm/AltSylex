import os
import database
import processador
from gerenciador_arquivos import GerenciadorArquivos

def testar_processador(conn, gerenciador_arquivos, caminho_historico, persona_id, persona_nome, persona_descricao):
    """Testa o processador com um arquivo de histórico."""
    print(f"\nTestando com o arquivo: {caminho_historico}")

    # Ler o conteúdo do arquivo
    conteudo_arquivo = gerenciador_arquivos.ler_arquivo(caminho_historico)
    if conteudo_arquivo is None:
        print(f"Erro: Não foi possível ler o arquivo {caminho_historico}")
        return

    # Processar o histórico
    mensagens = processador.processar_historico(conn, conteudo_arquivo, persona_id, persona_nome)

    # Verificar se o processamento retornou mensagens
    if not mensagens:
        print(f"Erro: O processamento do arquivo {caminho_historico} não retornou mensagens.")
        return

    # Imprimir as mensagens processadas
    print("Mensagens processadas:")
    for mensagem in mensagens:
        print(f"  Orador: {mensagem['orador']}")
        print(f"  Mensagem: {mensagem['mensagem']}")
        print(f"  Palavras Censuradas: {mensagem['palavras_censuradas']}")
        print("-" * 20)

    # Gerar o JSON
    nome_arquivo = os.path.basename(caminho_historico)
    nome_arquivo_sem_extensao = os.path.splitext(nome_arquivo)[0]
    caminho_json = gerenciador_arquivos.gerar_caminho_json(nome_arquivo_sem_extensao)
    processador.gerar_json(mensagens, persona_nome, persona_descricao, "interlocutor", caminho_json, gerenciador_arquivos)
    print(f"Arquivo JSON gerado em: {caminho_json}")

def main():
    # Configurações
    base_dir = os.path.dirname(__file__)
    db_file = os.path.join(base_dir, "altsylex.db")
    gerenciador_arquivos = GerenciadorArquivos(base_dir)
    persona_id = 1  # ID da persona para teste
    persona_nome = "Teste"
    persona_descricao = "Persona para teste"

    # Criar conexão com o banco de dados
    conn = database.create_connection(db_file)

    # Criar as tabelas
    if conn is not None:
        database.create_tables(conn)
    else:
        print("Erro! Não foi possível criar a conexão com o banco de dados.")
        return

    # Caminhos dos arquivos de histórico
    caminho_historico_discord = os.path.join(base_dir, "deposito", "test_simples_Discord.txt")
    caminho_historico_wpp = os.path.join(base_dir, "deposito", "teste_simples_Wpp.txt")

    # Testar com o arquivo do Discord
    testar_processador(conn, gerenciador_arquivos, caminho_historico_discord, persona_id, persona_nome, persona_descricao)

    # Testar com o arquivo do WhatsApp
    testar_processador(conn, gerenciador_arquivos, caminho_historico_wpp, persona_id, persona_nome, persona_descricao)

    # Fechar a conexão com o banco de dados
    conn.close()

if __name__ == "__main__":
    main()
