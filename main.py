import ttkbootstrap as ttk
import database
import os
from gui.app import AltSylexApp

# Caminho do banco de dados
db_file = os.path.join(os.path.dirname(__file__), "altsylex.db")

# Criar conexão com o banco de dados
conn = database.create_connection(db_file)

# Criar as tabelas
if conn is not None:
    database.create_tables(conn)
else:
    print("Erro! Não foi possível criar a conexão com o banco de dados.")

# Criar a pasta "historicos" se ela não existir
pasta_historicos = os.path.join(os.path.dirname(__file__), "historicos")
os.makedirs(pasta_historicos, exist_ok=True)

root = ttk.Window()
root.state('zoomed') #maximizar a tela
root.configure(background="black") #mudar a cor de fundo
app = AltSylexApp(root, conn)
root.mainloop()
