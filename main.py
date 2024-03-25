from objects import Connector
from datetime import datetime

db = Connector()

salvar = db.execute(
    'SELECT * FROM registrar_produto_no_estoque(%s, %s, %s, %s, %s);',
    ('limão', 450, 432, 30, datetime.today().strftime('%Y-%m-%d')),
    True
)
print(f'Produto salvo: {"OK" if salvar[0] else "Não"}.\n\n')

for produto in db.execute('SELECT * FROM selecionar_produto_em_estoque();'):
    print(produto)


