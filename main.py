from objects import Connector
from datetime import datetime

db = Connector()

produtos = db.execute('SELECT * FROM selecionar_produto_em_estoque();')

for produto in produtos:
    print(produto)

# produto = db.execute('SELECT * FROM selecionar_produto_em_estoque(%s);', ('abacate',), True)
#
# print(produto)

# print(db.execute(
#         'SELECT * FROM registrar_produto_no_estoque(%s, %s, %s, %s, %s);',
#         ('melancia', 150, 350, 35, datetime.today().strftime('%Y-%m-%d'))
#     )
# )

