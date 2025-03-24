add# AltSylex

## Descrição

AltSylex é um projeto que visa criar um aplicativo capaz de treinar uma Inteligência Artificial (IA) para imitar a forma de falar e responder de uma pessoa específica. O treinamento da IA é baseado em históricos de conversas, permitindo que ela aprenda e replique o estilo de comunicação da pessoa.

## Funcionalidades Principais

*   **Gerenciamento de Personas:** O aplicativo permite criar, educar e desviver (remover) diferentes personas. Cada persona representa uma identidade que a IA pode imitar.
*   **Upload e Processamento de Históricos:** É possível adicionar múltiplos arquivos de histórico de conversas para cada persona. O sistema processa esses históricos, identificando as falas da persona e do interlocutor.
*   **Censura de Palavras-Chave:** O usuário pode definir palavras-chave para serem censuradas nos históricos, garantindo a privacidade e evitando o vazamento de informações sensíveis.
*   **Preparação para a IA:** O sistema gera um arquivo JSON contendo o contexto das conversas, pronto para ser utilizado no treinamento de um modelo de IA.
* **Persistencia de memoria:** O arquivo `projeto_memoria.json` eh o responsavel pela persistencia de memoria.

## Tecnologias Utilizadas

*   **Linguagem de Programação:** Python
*   **Banco de Dados:** SQLite (sem o uso de Django)
*   **Interface Gráfica:** ttkbootstrap (planejado para o futuro)
* **Regex:** Para identificacao de falas.

## Estrutura do Projeto

*   **`main.py`:** Arquivo principal do projeto. Responsável pela inicialização do banco de dados e pela execução dos testes.
*   **`database.py`:** Contém as funções de interação com o banco de dados (CRUD).
*   **`processador.py`:** Contém a função `processar_historico` para analisar os arquivos de histórico e a funcao `gerar_json` para gerar o json.
*   **`deposito/`:** Pasta que contém os arquivos de histórico (`sylex_historico.txt`, `ruishalm_historico.txt`, `ruishalmDiscord.txt`).
*   **`projeto_memoria.json`:** Arquivo de memória do projeto, que armazena informações sobre o estado atual do projeto, decisões tomadas, próximos passos, etc.
* **`README.md`:** Arquivo de documentação do projeto.
* **`altsylex.db`:** Arquivo do banco de dados.

## Como Executar

1.  Certifique-se de ter o Python instalado em seu sistema.
2.  Clone o repositório: `git clone https://github.com/ruishalm/AltSylex.git`
3.  Navegue até o diretório do projeto: `cd AltSylex`
4.  Execute o arquivo `main.py`: `python main.py`

## Próximos Passos

*   Implementar a lógica para salvar e carregar a memória dos checkpoints.
*   Modificar `processador.py` para retornar mais dados.
*   Criar a funcao `gerar_json` em `processador.py`.
*   Modificar `main.py` para testar a funcao `gerar_json`.
*   Começar a desenvolver a interface gráfica usando `ttkbootstrap`.

## Decisões Tomadas

*   Usar SQLite diretamente (sem Django).
*   Substituição simples de palavras-chave por `[CENSURADO]`.
*   Gerar JSON com o contexto da conversa.
*   Usar `ttkbootstrap` para a interface gráfica.
*   Criar checkpoints de memória.
*   Criar a persona `Sylex` como a primeira persona de IA.
*   Os arquivos de histórico (ruishalm_historico.txt e sylex_historico.txt e ruishalmDiscord.txt) ficarão na pasta `deposito`.
*   Quando solicitado, reenviar textos exatamente como estão, sem alterações.
*   Quando a resposta for muito longa, dividi-la em partes e adicionar a mensagem: `A code sample in this response was truncated because it exceeded the maximum allowable output. Please use the response carefully. You may also try your question again, selecting a smaller block of code as the context`.
*   Não incluir o conteúdo dos arquivos de histórico no arquivo de memória, apenas as referências aos arquivos.
*   O usuário está usando o sistema operacional Windows e o editor de código VS Code.
*   O arquivo `projeto_memoria.json` eh o responsavel pela persistencia de memoria.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença

Este projeto está sob a licença MIT.
