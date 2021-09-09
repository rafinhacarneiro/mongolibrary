# MongoLibrary

Biblioteca para utilização do MongoDB com Robot Framework.

## Passos iniciais usando PIPENV
- Instalar e atualizar o pipenv pelo repositório do github
```bash
pip install -e git+https://github.com/pypa/pipenv.git@master#egg=pipenv
```
- Link do SpeedtestLibrary para instalação via pipenv no seu ambiente.
```bash
pipenv install git+https://gitlab.com/rpa-automation/libraries/mongolibrary@master
```
- Pronto para uso importando desta forma.
```python
from MongoLibrary import MongoLibrary
```

## Usando RCC da Robocorp

- Seguir os passos para instalação do [RCC](https://github.com/robocorp/rcc#direct-downloads-for-signed-executables-provided-by-robocorp)

- Teste para ver se instalou corretamente.
```bash
rcc
```

- Caso não tenha um projeto Robocorp criado. Executar o comando.
```bash
rcc create name-project
```

- Acessar o projeto.
```bash
cd name-project
```

- Add Library no conda.yaml via comando.
```bash
rcc robot libs -a git+https://gitlab.com/rpa-automation/libraries/mongolibrary@master -p --conda conda.yaml
```

- Adicionar no arquivo conda.yaml de forma manual.
```yaml
channels:
- conda-forge
dependencies:
- python=3.7.5
- pip=20.1
- pip:
  - git+https://gitlab.com/rpa-automation/libraries/mongolibrary@master
```

- Executar o comanda para rodar o projeto e instalar dependências.
```bash
rcc run
```

## Exemplo com Robot

```robot
*** Settings ***
Library         MongoLibrary


*** Variables ***


*** Tasks ***
Exemplo
    Resgatar um registro


*** Keywords ***
Resgatar um registro

  Conectar Mongodb

  Selecionar Database
  ...    <minha_db>

  Selecionar Collection
  ...    <minha_collection>

  ${ID} =    Transformar Em Id
  ...    <string_com_id>

  ${QUERY} =    Create Dictionary
  ...    _id=${ID}

  ${REGISTRO} =    Selecionar Registros
  ...    ${QUERY}

  Log Many    &{REGISTRO}
```

## Keywords

### Conectar Mongodb

Realiza a conexão ao MongoDB

Args:
- server (str, optional): Endereço do servidor. Defaults to "localhost".
- port (int, optional): Porta do servidor. Defaults to 27017.
- user (str, optional): Usuário no servidor. Defaults to None.
- password (str, optional): Senha do usuário. Defaults to None.
- database (str, optional): Um banco de dados para realizar as operações. Defaults to None.

### Transformar Em Id
Transforma uma string com ID em um objeto de ID do MongoDB para realizar as operações

Args:
- id (str): String com uma ID do MongoDB

Returns:
- ObjectId: Objeto de ID do MongoDB

### Resgatar Databases

Retorna uma lista de banco de dados existentes

Returns:
- List[str]: Lista de banco de dados

### Resgatar Collections

Retorna uma lista de coleções existentes

Args:
- database (str, optional): Um banco de dados para efetuar a operação. Defaults to None.

Returns:
- List[str]: Lista de coleções


### Selecionar Database

Seleciona um banco de dados para realizar operações

Args:
- database (str): Um banco de dados do MongoDB

Returns:
- bool: Define se o banco de dados existia (True) ou foi criado (False)


### Selecionar Collection

Seleciona uma coleção para realizar operações

Args:
- collection (str): Uma coleção do MongoDB
- database (str, optional): Um banco de dados para efetuar a operação, caso não selecionado. Defaults to None.

Returns:
- bool: Define se a coleção existia (True) ou foi criado (False)


### Selecionar Registros
Seleciona registros em uma coleção

Args:
- filter (dict, optional): Dicionário com os filtros de busca do MongoDB. Defaults to ```{}```.
- fields (dict, optional): Filtro de campos do registro. Defaults to None.
- sort (List[tuple], optional): Dicionário com informações de ordenação da pesquisa. Defaults to None.
- limit (int, optional): Quantidade de registros que serão retornados. Defaults to 0.
- skip (int, optional): Quantidade de registros que serão pulados pela pesquisa. Defaults to 0.
- collection (str, optional): Uma coleção para realizar a operação, caso não selecionada. Defaults to None.
- kwargs: Outras opções de pesquisa aceitas em ```pymongo.database.collection.find()```

Returns:
    List[dict]: Lista de registros


### Inserir Registro
Cria um registro em uma coleção

Args:
- record (dict): Registro que será criado
- collection (str, optional): Uma coleção para realizar a operação, caso não selecionada. Defaults to None.

Returns:
- str: ID do registro inserido


### Inserir Multiplos Registros
Cria multiplos registros em uma coleção

Args:
- records (List[dict]): Lista de registros que serão criados
- collection (str, optional): Uma coleção para realizar a operação, caso não selecionada. Defaults to None.

Returns:
- List[str]: Lista de id dos registros inseridos


### Atualizar Registro
Atualiza um registro em uma coleção

Args:
- filter (dict): Dicionário com os filtros de busca do MongoDB
- values (dict): Valores que deverão ser atualizados
- sort (List[tuple], optional): Dicionário com informações de ordenação da pesquisa. Defaults to None.
- upsert (bool, optional): Informa se o registro deve ser criado caso não exista. Defaults to True.
- collection (str, optional): Uma coleção para realizar a operação, caso não selecionada. Defaults to None.
- kwargs: Outras opções de pesquisa aceitas em ```pymongo.database.collection.find_one_and_update()```

Returns:
- dict: Registro após a atualização


### Atualizar Multiplos Registros
Atualiza os registros em uma coleção

Args:
- filter (dict): Dicionário com os filtros de busca do MongoDB
- values (dict): Valores que deverão ser atualizados
- upsert (bool, optional): Informa se o registro deve ser criado caso não exista. Defaults to True.
- collection (str, optional): Uma coleção para realizar a operação, caso não selecionada. Defaults to None.

Returns:
- int: Registros afetados


### Deletar Registro
Deleta um registro em uma coleção.

Args:
- filter (dict): Dicionário com os filtros de busca do MongoDB
- sort (List[tuple], optional): Dicionário com informações de ordenação da pesquisa. Defaults to None.
- collection (str, optional): Uma coleção para realizar a operação, caso não selecionada. Defaults to None.
- kwargs: Outras opções de pesquisa aceitas em ```pymongo.database.collection.find_one_and_delete()```

Returns:
- dict: Registro deletado


### Deletar Multiplos Registros
Deleta múltiplos registro em uma coleção.

Args:
- filter (dict): Dicionário com os filtros de busca do MongoDB
- collection (str, optional): Uma coleção para realizar a operação, caso não selecionada. Defaults to None.

Returns:
- int: Registros deletados