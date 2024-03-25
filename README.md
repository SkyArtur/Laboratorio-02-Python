<hr/>

Laboratórios:

[Laboratório 01 - Trabalhando com PostgreSQL e PL/pgSQL.](https://github.com/SkyArtur/Laboratorio-01-PLpgSQL)

[Laboratório 03 - Conectando com o banco de dados com Node JS.](https://github.com/SkyArtur/Laboratorio-03-Node)

<hr/>

# Laboratório 02 - Conectando com o banco de dados com Python.

Usaremos o banco de dados PostgreSQL que criamos no Laboratório 01, por isso, é importante que você tenha 
acompanhado o primeiro execício dos nossos laboratórios.

Vamos trabalhar em aplicações futuras que utilizem o banco de dados que desenvolvemos anteriormente. Neste segundo 
laboratório, desenvolveremos uma forma de estabelecer uma conexão com ele. Utilizaremos a linguagem Python, nesta experiència
e deixaremos pronto um objeto que possamos utilizar em nossos projetos futuros.

## Trabalhando com bibliotecas

As bibliotecas no Python são conjuntos de módulos e funções pré-definidos que nos permitem realizar diversas tarefas 
sem a necessidade de escrever o código do zero. Elas são um componente essencial da linguagem de programação Python, 
pois fornecem funcionalidades adicionais que expandem as capacidades da linguagem base. 

Nós podemos utilizar as bibliotecas padrões ou instalar uma biblioteca externa disponível no Python Package Index (PyPI).

Em nosso projeto, nós utilizaremos basicamente bibliotecas padrões como *pathlib*, *json*, *datetime*, etc. Mas também
instalaremos bibliotecas externas. A princípio, vamos utilizar as bibliotecas *psycopg2* e *python_dotenv*. A primeira 
nos oferecerá recursos para a nossa conexão com o banco de dados e a segunda carregará a variável de ambiente que editaremos
em um arquivo '.env' que conterá os dados do nosso banco de dados.  Elas podem ser instaladas diretamente com o comando 
``pip install psycopg2 python_dotenv`` ou utilizando o arquivo requirements.txt deste repositório com o comando 
``pip install -r requirements.txt``

## Editando arquivo *.env*

Primeiramente, iremos criar na raís do projeto um arquivo '.env'. Nele, editaremos uma variável de ambiente chamada
CONNECTION_STRING, onde atribuiremos os dados de conexão com o nosso banco de dados:
```dotenv
CONNECTION_STRING=postgresql://localhost:5430/laboratorio?user=estudante&password=212223
```
Essa metodologia, além de manter o código mais organizado, favorece a segurança e facilita o reuso do nosso objeto
de conexão. A string de conexão pode ser dividida da seguinte forma:
``
<driver_banco_de_dados>://<host_do_servidor:porta>/<nome_banco_de_dados>?user=<nome_usuario>&password=<senha_do_usuario>
``

## Um pouco sobre objetos

Nossa conexão com o banco de dados será feita através da biblioteca *psycopg2*, mas, ao invés de ficar importando essa 
biblioteca em todos os módulos do nosso código que execute uma conexão com o banco de dados, nós vamos desenvolver um 
objeto que guardará a lógica necessária. 

Em Javascript, podemos dizer que tudo é uma função, porém, em Python tudo é um objeto. Isso inclui números, strings, 
listas, funções e até mesmo os tipos de dados que você mesmo criar. Um objeto em Python é uma coleção de dados 
(variáveis) e métodos (funções) que atuam nesses dados. Em outras palavras, um objeto representa uma entidade ou conceito, 
com suas propriedades e ações que podem ser realizadas. Vamos dar uma olhadinha nos termos utilizados com um exemplo 
simplificado de um objeto:
```python
class Pessoa:
    __especie = None

    def __new__(cls, *args, **kwargs):
        if not cls.__especie or cls.__especie is None:
            cls.__especie = 'Humano'
        return super(Pessoa, cls).__new__(cls)

    def __init__(self, nome=None):  # parâmetro
        self.nome = nome  # atributo de instância

    @property
    def especie(self):
        return self.__especie

    def apresentar(self):  # método
        print(f'Olá eu sou {self.nome}')

    @staticmethod  # método estático
    def falar(mensagem):
        print(mensagem)

    @classmethod  # método de classe
    def super_homem(cls):
        clark = cls('Kal-el')
        clark._Pessoa__especie = 'Criptoniano'
        return clark
```
- Instância: Uma instância é um objeto específico criado a partir de uma classe. Cada instância compartilha o mesmo 
conjunto de atributos definidos pela classe, mas pode ter valores diferentes para esses atributos.
```python

if __name__ == '__main__':
    #criando duas instâncias da classe Pessoa.
    pessoa1 = Pessoa('Eduardo')
    pessoa2 = Pessoa('Maria')
```
``print:``
```shell
Pessoa 1: Eduardo

Pessoa 2: Maria
```
- Atributos: são variáveis que pertencem à classe, no nosso exemplo ambas as instâncias, *pessoa1* e *pessoa2*, compartilham 
o atributo nome, mas com valores diferentes.
```python
print(f'Pessoa 1: {pessoa1.nome}', f'Pessoa 2: {pessoa2.nome}', sep='\n\n')
```
``print:``
```shell
Pessoa 1 nome: Eduardo

Pessoa 2 nome: Maria
```
- Parâmetros: São dados passados para a classe (objeto) ou função para que ela realize alguma ação. Nossa classe *Pessoa()*
possui um parâmetro *nome*, que possui o valor padrão None, se esse parâmetro for passado para a classe no momento que ela
é instânciada, ele será repassado para o atributo *nome* da classe.
```python
pessoa3 = Pessoa('João')
```
``print:``
```shell
Pessoa 3: João
```
- Propriedade: Uma propriedade de classe é um atributo que pertence à própria classe, não a uma instância 
específica dessa classe. Isso significa que todos os objetos criados a partir dessa classe compartilham o mesmo valor 
para esse atributo.
```python
print(f'{pessoa1.nome} : {pessoa1.especie}', f'{pessoa2.nome} : {pessoa2.especie}', sep='\n\n')
```
``print:``
```shell
Eduardo : Humano

Maria : Humano
```
- Método: Os métodos de uma classe são funções que definem as ações ou comportamentos que o objeto criado a partir dessa
classe pode ter. Os métodos permitem que as instâncias (objetos) interajam com os atributos da classe e realizem operações
específicas. Nossa classe *Pessoa()*, pode apresentar-se interagindo com seu atributo *nome*.
```python
pessoa1.apresentar()
```
``print:``
```shell
Olá eu sou Eduardo
```
- staticmethod: Em Python, métodos estáticos são funções que permitem que um método de classe execute ações, sem 
interagir com qualquer atributo ou propriedade da classe.
```python
pessoa2.apresentar() # método
pessoa2.falar('e estou estudando programação!') # staticmethod
```
``print:``
```shell
Olá eu sou Maria
e estou estudando programação!
```
- classmethod: Um método de classe é um método que está vinculado à classe, não a uma instância específica da classe, portanto,
podem ser usados sem a necessidade de se instanciar a classe. Exemplos de uso incluem métodos de fábrica.
```python
if __name__ == '__main__':
    pessoa4 = Pessoa.super_homem()
    
    print(f'Pessoa 4: {pessoa4.nome} : {pessoa4.especie}')
```
``print:``
```shell
Pessoa 4: Kal-el : Criptoniano
```
Agora que conhecemos um pouco sobre objetos em Python, vamos falar um pouco sobre o design pattern do nosso objeto. 

## Falando um pouco sobre padrões de projetos

Os padrões de projeto (ou design patterns) são soluções generalistas para problemas recorrentes durante o desenvolvimento
de software. Eles não são um código pronto, mas sim conceitos que servem como soluções para problemas comuns da programação.
Podem ser definidos em:
- Padrões Criacionais: Lidam com a criação de objetos (exemplos: Singleton, Factory, Builder).
- Padrões Estruturais: Tratam da composição de classes e objetos (exemplos: Adapter, Decorator, Composite).
- Padrões Comportamentais: Definem como objetos interagem entre si (exemplos: Observer, Strategy, Command).

Nosso objeto *Connector()* atenderá ao padrão Singleton, neste padrão, apenas uma instância da classe existe durante toda
a execução do software, fornecendo um ponto global de acesso a essa instância.
```python
# ./objects/connector.py
class Connector:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance or cls.__instance is None:
            cls.__instance = super(Connector, cls).__new__(cls)
        return cls.__instance
    
    def __init__(self, params):
        self.conn = params
        
        
db1 = Connector('sqlite:///database.db')
db2 = Connector('sqlite:///sqlite.db')

print(
    f'memoria db1: {hex(id(db1))}\nmemoria db2: {hex(id(db2))}',
    f'conn db1: {db1.conn}\nconn db2: {db2.conn}',
    sep='\n\n'
)
```
``print:``
```shell
memoria db1: 0x1a1b4d15cd0
memoria db2: 0x1a1b4d15cd0

conn db1: sqlite:///sqlite.db
conn db2: sqlite:///sqlite.db
```
Perceba que mesmo que tenhamos duas instâncias com nomes diferentes, elas ocupam o mesmo endereço de memória. Além disso,
ao realizarmos uma segunda instância, com parâmetro diferente, o valor do atributo da primeira instância foi sobrescrito.

Conceitos definidos, vamos continuar nosso trabalho. 

## Partindo para o Connector

Primeiramente, vamos criar um pacote python com o nome *objects* na raiz do nosso projeto e acrescentar a esse pacote um 
arquivo *connector.py*. Lembrando que um pacote Python, nada mais é que um diretório com um arquivo '__ init __.py' dentro
dele.

Vamos importar em nosso arquivo *connector.py*, as bibliotecas, *os*, *dotenv* e *psycopg2* e em seguida, carregar a nossa
variável de ambiente com o método '.load_dotenv()':
```python
import os
import dotenv
import psycopg2

dotenv.load_dotenv()

```
Agora, usaremos dois Dunder Methods, que são comuns a todas as classes em Python. O método '__ new __()', é utilizado
para controlar a criação de novas instâncias de uma classe, e nós usaremos ele para manipular a propriedade '__instance'.

Lembre-se que definimos propriedades como sendo um atributo que pertence à classe, e por isso é compartilhada
por todas as instâncias da classe. É por essa razão que ao utilizarmos o método '__ new __()',
para atribuir à propriedade '__instance', uma instância da própria classe, criamos um objeto Singleton.

O método __ init __(), responsável por controlar a inicialização da classe, não recebe parâmetros e apenas inicia três 
atributos que serão manipulados pelo método '.execute()'.
```python
class Connector:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance or cls.__instance is None:
            cls.__instance = super(Connector, cls).__new__(cls)
        return cls.__instance

    def __init__(self, *args, **kwargs):
        self.__conn = None
        self.__cursor = None
        self.__response = None
```
O método '.execute()' é responsável por realizar a conexão com o banco de dados, executar a query e retornar os dados.
Ele possui três parâmetros: 
- query: Texto SQL.
- data: Tupla com os dados que se deseja repassar para o banco de dados, tanto para registro, como para busca.
- fetchone: Opcional para a realização de buscas unitárias.

Toda a lógica da função está definida em um bloco 'try-except', que está sendo usado não apenas para controle de exceções,
mas também como um gerenciador de contexto, pois, utilizamos a claúsula *finally*, para garantir que o banco de dados e 
o cursor serão fechados, mesmo que uma exceção ocorra.
```python
    def execute(self, query: str, data: tuple = None, fetchone: bool = False) -> tuple:
        try:
            self.__conn = psycopg2.connect(os.getenv('CONNECTION_STRING'))
            self.__cursor = self.__conn.cursor()
            self.__cursor.execute(query, data)
            self.__response = self.__cursor.fetchall() if not fetchone else self.__cursor.fetchone()
        except (TypeError, psycopg2.DatabaseError) as error:
            print(f'Error while connecting to PostgreSQL: {error}')
        else:
            self.__conn.commit()
            return self.__response
        finally:
            self.__cursor.close()
            self.__conn.close()
```
A estrutura completa do nosso objeto fica sendo a seguinte:
```python
import os
import dotenv
import psycopg2

dotenv.load_dotenv()


class Connector:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance or cls.__instance is None:
            cls.__instance = super(Connector, cls).__new__(cls)
        return cls.__instance

    def __init__(self, *args, **kwargs):
        self.__conn = None
        self.__cursor = None
        self.__response = None

    def execute(self, query: str, data: tuple = None, fetchone: bool = False) -> tuple:
        """
        Executa a query e retorna o resultado da consulta.
        :param query: consulta SQL.
        :param data: dados pra a consulta ou registro.
        :param fetchone: retornar único valor da consulta.
        :return: tupla de resultados da consulta.
        """
        try:
            self.__conn = psycopg2.connect(os.getenv('CONNECTION_STRING'))
            self.__cursor = self.__conn.cursor()
            self.__cursor.execute(query, data)
            self.__response = self.__cursor.fetchall() if not fetchone else self.__cursor.fetchone()
        except (TypeError, psycopg2.DatabaseError) as error:
            print(f'Error while connecting to PostgreSQL: {error}')
        else:
            self.__conn.commit()
            return self.__response
        finally:
            self.__cursor.close()
            self.__conn.close()
```
Não vamos esquecer de importar o nosso *Connector()* em __ init __.py do pacote *objects*.

## Realizando alguns testes

Agora podemos utilizar as funções que criamos no nosso laboratorio de PL/pgSQL:
- buscando todos os produtos:
```python
from objects import Connector


db = Connector()

produtos = db.execute('SELECT * FROM selecionar_produto_em_estoque();')

for produto in produtos:
    print(produto)
```
``print:``
```shell
('abacate', 279, Decimal('455.00'), Decimal('22'), Decimal('1.85'))
('banana', 226, Decimal('265.00'), Decimal('25'), Decimal('1.33'))
('laranja', 250, Decimal('440.00'), Decimal('15'), Decimal('2.02'))
('tomate', 500, Decimal('732.00'), Decimal('25'), Decimal('1.83'))
```
- buscando um produto por nome.
```python
from objects import Connector


db = Connector()

produto = db.execute('SELECT * FROM selecionar_produto_em_estoque(%s);', ('abacate',), True)

print(produto)
```
``print:``
```shell
('abacate', 279, Decimal('455.00'), Decimal('22'), Decimal('1.85'))
```
- inserindo dados no banco de dados:
```python
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
```
``print:``
```shell
Produto salvo: OK.


('abacate', 279, Decimal('455.00'), Decimal('22'), Decimal('1.85'))
('banana', 226, Decimal('265.00'), Decimal('25'), Decimal('1.33'))
('laranja', 250, Decimal('440.00'), Decimal('15'), Decimal('2.02'))
('limão', 450, Decimal('432.00'), Decimal('30'), Decimal('1.25'))
('manga', 500, Decimal('635.00'), Decimal('30'), Decimal('1.65'))
('morango', 602, Decimal('832.00'), Decimal('45'), Decimal('1.86'))
('tomate', 500, Decimal('732.00'), Decimal('25'), Decimal('1.83'))
```
- tentando salvar o mesmo produto novamente.
```python
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
```
``print:``
```shell
Produto salvo: Não.


('abacate', 279, Decimal('455.00'), Decimal('22'), Decimal('1.85'))
('banana', 226, Decimal('265.00'), Decimal('25'), Decimal('1.33'))
('laranja', 250, Decimal('440.00'), Decimal('15'), Decimal('2.02'))
('limão', 450, Decimal('432.00'), Decimal('30'), Decimal('1.25'))
('manga', 500, Decimal('635.00'), Decimal('30'), Decimal('1.65'))
('morango', 602, Decimal('832.00'), Decimal('45'), Decimal('1.86'))
('tomate', 500, Decimal('732.00'), Decimal('25'), Decimal('1.83'))
```
Bom, ao que parece está tudo funcionando como o esperado. Continuaremos em nossos próximos laboratórios a desenvolver 
a nossa aplicação. 
