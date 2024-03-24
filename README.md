<hr/>

# Laboratório 02 - Python - Conectando com o banco de dados.

<hr/>

[Laboratório 01 - PL/pgSQL - Trabalhando com PostgreSQL e PL/pgSQL.](https://github.com/SkyArtur/Laboratorio-01-PLpgSQL)

<hr/>

Usaremos o banco de dados PostgreSQL que criamos no Laboratório 01, por isso, é importante que você tenha 
acompanhado o primeiro execício dos nossos laboratórios.

Vamos trabalhar em uma aplicação de linha de comando. Apesar de um visual nada moderno e atraente, uma aplicação desse 
tipo é mais trabalhosa de se produzir, mas, permite uma abordagem maior de assuntos relacionados a programação.

## Lendo arquivos

Em Python, como em outras linguagens de programação, nós temos as funções '*built-ins*', que são integradas a linguagem 
pelos desenvolvedores dela e ficam disponíveis nativamente. Uma destas funções é a *open()*, que podemos utilizar para 
abrir arquivos.
```python
#./main.py
arquivo = open('./arquivo.txt', 'r', encoding='utf-8')
print(arquivo.read())
arquivo.close()
```
``print:``
```shell
conteúdo do arquivo: 
Eu sou um texto dentro do arquivo.
```
A função *open()* recebe alguns parâmetros como o caminho do arquivo, o modo de abertura do arquivo ('r', 'w', 'a') e a 
codificação binária ('UTF-8') são as mais relevantes para o nosso trabalho aqui, mas se você quiser saber mais a respeito,
este [link](https://acervolima.com/funcao-python-open/) leva a um excelente artigo sobre a função *open()*.

Mas voltando ao nosso projeto, perceba que precisamos fechar o arquivo utilizando o método **close()**. Após trabalhar 
com o arquivo, é crucial fechá-lo. Isso libera recursos do sistema e garante que todas as alterações sejam salvas. 
Por isso vamos trabalhar com o gerenciador de contexto **with**. O gerenciador de contexto é uma ferramenta essencial em
Python para manipulação segura de recursos, como a abertura e fechamento de arquivos. Quando trabalhamos com arquivos, 
bancos de dados ou outros recursos, eles são limitados em quantidade. Por exemplo, um processo só pode abrir um número 
específico de arquivos simultaneamente. Se não liberarmos esses recursos adequadamente, ocorrerão vazamentos de recursos, 
o que pode afetar o desempenho do sistema. Ele garante que os recursos sejam liberados automaticamente após o uso, 
mesmo em caso de exceções.
```python
#./main.py
with open('./arquivo.txt', 'r', encoding='utf-8') as arquivo:
    print('conteúdo do arquivo: ', arquivo.read(), sep='\n')
```
``print:``
```shell
conteúdo do arquivo: 
Eu sou um texto dentro do arquivo.
```
## Trabalhando com bibliotecas

As bibliotecas no Python são conjuntos de módulos e funções pré-definidos que nos permitem realizar diversas tarefas 
sem a necessidade de escrever o código do zero. Elas são um componente essencial da linguagem de programação Python, 
pois fornecem funcionalidades adicionais que expandem as capacidades da linguagem base. 

Nós podemos utilizar as bibliotecas padrões ou instalar uma biblioteca externa disponível no Python Package Index (PyPI).

Em nosso projeto, nós utilizaremos basicamente bibliotecas padrões como *pathlib*, *json*, *datetime*, etc. A única 
biblioteca externa que iremos utilizar é a *psycopg2*, que nos oferecerá recursos para a nossa conexão com o banco de dados
e pode ser instalada com diretamente com o comando ``pip install psycopg2`` ou utilizando o arquivo requirements.txt 
deste repositório com o comando ``pip install -r requirements.txt``

## A primeira função do projeto

Vamos elaborar uma função que retorne o conteúdo de um arquivo. Ela será útil quando quisermos exibir nossos menus e tabelas
que serão carregados a partir de arquivos de texto.

Primeiramente vamos criar um diretório na raiz do nosso projeto com o nome `files`, nós utilizaremos este diretório como
raiz para todos os arquivos texto que utilizaremos. 

Vamos editar um arquivo json com os parâmetros do nosso banco de dados e nomeá-lo como *params.json*.
```json
{
    "database": "laboratorio",
    "user": "estudante",
    "password": "212223",
    "host": "localhost",
    "port": "5430"
}
```
Agora vamos criar um pacote python chamado *functions* na raiz do nosso projeto, lembrando que um pacote python é um diretório
como um arquivo __ init __.py, em seguida, vamos criar um dentro dele outro arquivo chamado *reader.py* e programar a nossa
função *reader()*. 
```python
#./functions/reader.py
from pathlib import Path
import json


def reader(filename):
    try:
        root = Path(__file__).resolve().parent.parent.joinpath('files')
        with open(root.joinpath(filename), encoding="utf-8") as file:
            if '.json' in filename:
                return json.load(file)
            else:
                return file.read()
    except (FileNotFoundError, TypeError) as error:
        return f'Error reading {filename}: {error}'
```

No arquivo __ init __.py do nosso pacote *functions*, vamos realizar o import desta função:
```python
#./functions/__init__.py
from .reader import reader
```
Agora podemos utilizar esta função a partir deste nosso pacote em qualquer outro ponto do nosso código.
```python
#./main.py
from functions import reader


content = reader('params.json')
print('conteúdo do arquivo params.json: ', content, sep='\n\n')
```
``print:``
```shell
conteúdo do arquivo params.json: 

{'database': 'laboratorio', 'user': 'estudante', 'password': '212223', 'host': 'localhost', 'port': '5430'}
```

## Partindo para os objetos

Nossa conexão com o banco de dados será feita através da biblioteca *psycopg2*, mas, ao invés de ficar importando essa 
biblioteca em todos os pontos do nosso código em que execute uma conexão com o banco de dados, nós vamos desenvolver um 
objeto que guardará essa lógica. 

Assim como podemos dizer que em Javascript, tudo é uma função, em Python, tudo é um objeto. Isso inclui números, strings, 
listas, funções e até mesmo os tipos de dados que você mesmo pode criar. Um objeto em Python é uma coleção de dados 
(variáveis) e métodos (funções) que atuam nesses dados. Em outras palavras, um objeto representa uma entidade ou conceito, 
com suas propriedades e ações que podem ser realizadas. Vamos definir aqui algumas nomenclaturas com base no exemplo a 
seguir:
```python
class Pessoa:
    __especie = 'Humano' # propriedade de classe
    
    def __init__(self, nome=None): # parâmetro 
        self.nome = nome # atributo de instância
    
    @property
    def especie(self):
        return self.__especie
        
    def apresentar(self): # método
        print(f'Olá eu sou {self.nome}')

    @staticmethod # método estático
    def falar(mensagem):
        print(mensagem)

    @classmethod # método de classe
    def super(cls):
        superhomen = cls('Clark Kent')
        cls.__especie = 'criptoniano'
        return superhomen
```
- Instância: Uma instância é um objeto específico criado a partir de uma classe. Cada instância compartilha o mesmo 
conjunto de atributos definidos pela classe, mas pode ter valores diferentes para esses atributos.
```python
#criando duas instâncias da classe Pessoa.
pessoa1 = Pessoa('Eduardo')
pessoa2 = Pessoa()
pessoa2.nome = 'Maria'
```
- Atributos: são variáveis que pertencem à classe, no nosso exemplo ambas as instâncias, *pessoa1* e *pessoa2*, compartilham 
o atributo nome, mas com valores diferentes.
```python
print(f'Pessoa 1: {pessoa1.nome}', f'Pessoa 2: {pessoa2.nome}', sep='\n\n')
```
``print:``
```shell
Pessoa 1: Eduardo

Pessoa 2: Maria
```
- Parâmetros: São dados passados para a classe (objeto) ou função para que ela realize alguma ação. Nossa classe *Pessoa()*
possui um parâmetro *nome*, que possui o valor padrão None, se esse parâmetro for passado para a classe no momento que ela
é instânciada, ele será repassado para o atributo *nome* da classe.
```python
pessoa3 = Pessoa('João')
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
- staticmethod: Em Python, métodos estáticos são funções que permitem que um método de classe executem ações, sem 
interagirem com qualquer atributo ou propriedade da classe.
```python
pessoa2.apresentar()
pessoa2.falar('e estou estudando programação!')
```
``print:``
```shell
Olá eu sou Maria
e estou estudando programação!
```
- classmethod: Um método de classe é um método que está vinculado à classe, não a uma instância específica da classe, portanto,
podem ser usados sem a necessidade de se instanciar a classe. Exemplos de uso incluem métodos de fábrica.
```python
pessoa4 = Pessoa.super()

print(f'{pessoa4.nome} : {pessoa4.especie}')
```
``print:``
```shell
Clark Kent : criptoniano
```
Agora que conhecemos um pouco sobre objetos em Python, que tal seguirmos adiante? 

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

Conceitos definidos, vamos continuar nosso trabalho. Primeiramente, vamos criar um pacote python com o nome *objects*
na raiz do nosso projeto e acrescentar a esse pacote um arquivo *connector.py*.
```python
#./objects/connector.py
import psycopg2
from functions import reader


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
            self.__conn = psycopg2.connect(**reader('params.json'))
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
Não vamos esquecer de importar o nosso Connector em __ init __.py.

Agora podemos utilizar as 'procedures' que criamos no nosso laboratorio de PL/pgSQL:
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
- buscando um produto
```python
produto = db.execute('SELECT * FROM selecionar_produto_em_estoque(%s);', ('abacate',), True)

print(produto)
```
``print:``
```shell
('abacate', 279, Decimal('455.00'), Decimal('22'), Decimal('1.85'))
```
- inserindo dados:
```python
print(db.execute(
        'SELECT * FROM registrar_produto_no_estoque(%s, %s, %s, %s, %s);',
        ('melancia', 150, 350, 35, datetime.today().strftime('%Y-%m-%d'))
    )
)
produtos = db.execute('SELECT * FROM selecionar_produto_em_estoque();')

for produto in produtos:
    print(produto)
```
``print:``
```shell
[(True,)]


('abacate', 279, Decimal('455.00'), Decimal('22'), Decimal('1.85'))
('banana', 226, Decimal('265.00'), Decimal('25'), Decimal('1.33'))
('laranja', 250, Decimal('440.00'), Decimal('15'), Decimal('2.02'))
('melancia', 150, Decimal('350.00'), Decimal('35'), Decimal('3.15'))
('tomate', 500, Decimal('732.00'), Decimal('25'), Decimal('1.83'))
```
Bom, ao que parece stá tudo funcionando como o esperado. Continuaremos em nossos próximos laboratórios a desenvolver 
a nossa aplicação.
