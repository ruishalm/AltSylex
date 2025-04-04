import os
import shutil
import json

class GerenciadorArquivos:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.historicos_dir = os.path.join(self.base_dir, "historicos")
        self.jsons_dir = os.path.join(self.base_dir, "jsons")
        self.criar_pasta(self.historicos_dir)
        self.criar_pasta(self.jsons_dir)

    def criar_pasta(self, pasta):
        """Cria uma pasta se ela não existir."""
        os.makedirs(pasta, exist_ok=True)

    def copiar_arquivo(self, origem, destino):
        """Copia um arquivo de origem para o destino."""
        shutil.copy2(origem, destino)

    def listar_arquivos(self, pasta, extensao=None):
        """Lista todos os arquivos em uma pasta, opcionalmente filtrando por extensão."""
        arquivos = []
        try:
            for arquivo in os.listdir(pasta):
                if os.path.isfile(os.path.join(pasta, arquivo)):
                    if extensao is None or arquivo.endswith(extensao):
                        arquivos.append(os.path.join(pasta, arquivo))
        except FileNotFoundError:
            print(f"Pasta não encontrada: {pasta}")
        return arquivos

    def excluir_arquivo(self, caminho):
        """Exclui um arquivo."""
        try:
            os.remove(caminho)
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {caminho}")

    def ler_arquivo(self, caminho):
        """Lê o conteúdo de um arquivo."""
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {caminho}")
            return None

    def escrever_arquivo(self, caminho, conteudo):
        """Escreve o conteúdo em um arquivo."""
        try:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(conteudo)
        except Exception as e:
            print(f"Erro ao escrever no arquivo: {e}")

    def gerar_caminho_json(self, nome_arquivo_sem_extensao):
        """Gera o caminho completo para um arquivo JSON."""
        return os.path.join(self.jsons_dir, f"{nome_arquivo_sem_extensao}.json")

    def ler_json(self, caminho):
        """Lê o conteúdo de um arquivo JSON."""
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Arquivo JSON não encontrado: {caminho}")
            return None
        except json.JSONDecodeError:
            print(f"Erro ao decodificar JSON: {caminho}")
            return None

    def escrever_json(self, caminho, dados):
        """Escreve dados em um arquivo JSON."""
        try:
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao escrever no arquivo JSON: {e}")

