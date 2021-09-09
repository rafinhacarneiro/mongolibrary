from typing import List
from bson.objectid import ObjectId
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.collection import ReturnDocument

class MongoLibrary:
    
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    sort_options = {
        "asc": ASCENDING,
        "desc": DESCENDING
    }


    def __init__(
        self,
        server: str = None,
        port: int = None,
        user: str = None,
        password: str = None,
        database: str = None
    ):
        """Realiza a conexão implicitamente caso os valores sejam fornecido

        Args:
            server (str, optional): Endereço do servidor. Defaults to None.
            port (int, optional): Porta do servidor. Defaults to None.
            user (str, optional): Usuário no servidor. Defaults to None.
            password (str, optional): Senha do usuário. Defaults to None.
            database (str, optional): Um banco de dados para realizar as operações. Defaults to None.
        """

        if server and port:
            self.conectar_mongodb(server, port, user, password, database)


    def _sort(
        self,
        query: List[tuple]
    ) -> List[tuple]:
        """Realiza a troca de valores de ordenação nos atributos sort por propriedades do MongoDB

        Args:
            query (List[tuple]): Dicionário de sort recebido pela Keyword

        Returns:
            List[tuple]: O dicionário de sort com os valores traduzidos para o MongoDB
        """
        
        return [ ( field, self.sort_options[ value.strip().lower() ] ) for field, value in query ]


    def transformar_em_id(
        self,
        id: str
    ) -> ObjectId:
        """Transforma uma string com ID em um objeto de ID do MongoDB para realizar as operações

        Args:
            id (str): String com uma ID do MongoDB

        Returns:
            ObjectId: Objeto de ID do MongoDB
        """

        return ObjectId(id.strip())


    def conectar_mongodb(
        self,
        server: str = "localhost",
        port: int = 27017,
        user: str = None,
        password: str = None,
        database: str = None
    ):
        """Realiza a conexão ao MongoDB

        Args:
            server (str, optional): Endereço do servidor. Defaults to "localhost".
            port (int, optional): Porta do servidor. Defaults to 27017.
            user (str, optional): Usuário no servidor. Defaults to None.
            password (str, optional): Senha do usuário. Defaults to None.
            database (str, optional): Um banco de dados para realizar as operações. Defaults to None.
        """

        connection = "mongodb://"

        if user and password:
            user = user.strip()
            password = password.strip()

            if user and password:
                connection += f"{user}:{password}@"

        server = server.strip()
        port = int(port)

        connection += f"{server}:{port}/"

        self.mongodb = MongoClient(connection)

        if database:
            if database.strip():
                self.selecionar_database(database)

    
    def resgatar_databases(
        self,
    ) -> List[str]:
        """Retorna uma lista de banco de dados existentes

        Returns:
            List[str]: Lista de banco de dados
        """

        return self.mongodb.list_database_names()

    
    def selecionar_database(
        self,
        database: str
    ) -> bool:
        """Seleciona um banco de dados para realizar operações

        Args:
            database (str): Um banco de dados do MongoDB

        Returns:
            bool: Define se o banco de dados existia (True) ou foi criado (False)
        """

        database = database.strip()

        exists = database in self.mongodb.list_database_names()
        self.db = self.mongodb[database]

        return exists

    
    def resgatar_collections(
        self,
        database: str = None
    ) -> List[str]:
        """Retorna uma lista de coleções existentes

        Args:
            database (str, optional): Um banco de dados para efetuar a operação. Defaults to None.

        Returns:
            List[str]: Lista de coleções no banco de dados
        """

        db = self.db

        if database:
            database = database.strip()

            db = self.mongodb[database]

        return db.list_collection_names()

    
    def selecionar_collection(
        self,
        collection: str,
        database: str = None
    ) -> bool:
        """Seleciona uma coleção para realizar operações

        Args:
            collection (str): Uma coleção do MongoDB
            database (str, optional): Um banco de dados para efetuar a operação, caso não selecionado. Defaults to None.

        Returns:
            bool: Define se a coleção existia (True) ou foi criada (False)
        """
        
        if database:
            if database.strip():
                self.selecionar_database(database)

        collection = collection.strip()

        exists = collection in self.db.list_collection_names()
        self.collection = self.db[collection]

        return exists

    
    def selecionar_registros(
        self,
        filter: dict = None,
        fields: dict = None,
        sort: List[tuple] = None,
        limit: int = None,
        skip: int = None,
        collection: str = None,
        **kwargs
    ) -> List[dict]:
        """Seleciona registros em uma coleção

        Args:
            filter (dict, optional): Dicionário com os filtros de busca do MongoDB. Defaults to {}.
            fields (dict, optional): Filtro de campos do registro. Defaults to None.
            sort (List[tuple], optional): Dicionário com informações de ordenação da pesquisa. Defaults to None.
            limit (int, optional): Quantidade de registros que serão retornados. Defaults to 0.
            skip (int, optional): Quantidade de registros que serão pulados pela pesquisa. Defaults to 0.
            collection (str, optional): Uma coleção para realizar a operação, caso não selecionada. Defaults to None.
            kwargs: Outras opções de pesquisa aceitas em pymongo.database.collection.find()

        Returns:
            List[dict]: Lista de registros
        """

        if not filter:
            filter = {}

        if not limit or limit < 0:
            limit = 0

        if not skip or skip < 0:
            skip = 0

        if collection:
            if collection.strip():
                self.selecionar_collection(collection)

        if sort:
            sort = self._sort(sort)

        return list( self.collection.find(
            filter,
            fields,
            sort=sort,
            limit=limit,
            skip=skip,
            **kwargs
        ) )


    def inserir_registro(
        self,
        record: dict,
        collection: str = None,
    ) -> str:
        """Cria um registro em uma coleção

        Args:
            record (dict): Registro que será criado
            collection (str, optional): Uma coleção para realizar a operação, caso não selecionada. Defaults to None.

        Returns:
            str: ID do registro inserido
        """

        if collection:
            if collection.strip():
                self.selecionar_collection(collection)

        return self.collection.insert_one(record).inserted_id

    
    def inserir_multiplos_registros(
        self,
        records: List[dict],
        collection: str = None,
    ) -> List[str]:
        """Cria multiplos registros em uma coleção

        Args:
            records (List[dict]): Lista de registros que serão criados
            collection (str, optional): Uma coleção para realizar a operação, caso não selecionada. Defaults to None.

        Returns:
            List[str]: Lista de id dos registros inseridos
        """

        if collection:
            if collection.strip():
                self.selecionar_collection(collection)

        return self.collection.insert_many(records).inserted_ids


    def atualizar_registro(
        self,
        filter: dict,
        values: dict,
        sort: List[tuple] = None,
        upsert: bool = True,
        collection: str = None,
        **kwargs
    ) -> dict:
        """Atualiza um registro em uma coleção

        Args:
            filter (dict): Dicionário com os filtros de busca do MongoDB
            values (dict): Valores que deverão ser atualizados
            sort (List[tuple], optional): Dicionário com informações de ordenação da pesquisa. Defaults to None.
            upsert (bool, optional): Informa se o registro deve ser criado caso não exista. Defaults to True.
            collection (str, optional): Uma coleção para realizar a operação, caso não selecionada. Defaults to None.
            kwargs: Outras opções de pesquisa aceitas em pymongo.database.collection.find_one_and_update()

        Returns:
            dict: Registro após a atualização
        """

        if collection:
            if collection.strip():
                self.selecionar_collection(collection)

        if sort:
            sort = self._sort(sort)

        return self.collection.find_one_and_update(
            filter,
            values,
            upsert=upsert,
            sort=sort,
            return_document=ReturnDocument.AFTER,
            **kwargs
        )


    def atualizar_multiplos_registros(
        self,
        filter: dict,
        values: dict,
        upsert: bool = True,
        collection: str = None
    ) -> int:
        """Atualiza os registros em uma coleção

        Args:
            filter (dict): Dicionário com os filtros de busca do MongoDB
            values (dict): Valores que deverão ser atualizados
            upsert (bool, optional): Informa se o registro deve ser criado caso não exista. Defaults to True.
            collection (str, optional): Uma coleção para realizar a operação, caso não selecionada. Defaults to None.

        Returns:
            int: Registros afetados
        """

        if collection:
            if collection.strip():
                self.selecionar_collection(collection)
        
        return self.collection.update_many(
            filter,
            values,
            upsert
        ).modified_count

    
    def deletar_registro(
        self,
        filter: dict,
        sort: List[tuple] = None,
        collection: str = None,
        **kwargs
    ) -> dict:
        """Deleta um registro em uma coleção.

        Args:
            filter (dict): Dicionário com os filtros de busca do MongoDB
            sort (List[tuple], optional): Dicionário com informações de ordenação da pesquisa. Defaults to None.
            collection (str, optional): Uma coleção para realizar a operação, caso não selecionada. Defaults to None.
            kwargs: Outras opções de pesquisa aceitas em pymongo.database.collection.find_one_and_delete()

        Returns:
            dict: Registro deletado
        """

        if collection:
            if collection.strip():
                self.selecionar_collection(collection)

        if sort:
            sort = self._sort(sort)

        return self.collection.find_one_and_delete(
            filter,
            sort=sort,
            return_document=ReturnDocument.BEFORE,
            **kwargs
        )


    def deletar_multiplos_registros(
        self,
        filter: dict,
        collection: str = None
    ) -> int:
        """Deleta múltiplos registro em uma coleção.

        Args:
            filter (dict): Dicionário com os filtros de busca do MongoDB
            collection (str, optional): Uma coleção para realizar a operação, caso não selecionada. Defaults to None.

        Returns:
            int: Registros deletados
        """

        if collection:
            if collection.strip():
                self.selecionar_collection(collection)
        
        return self.collection.delete_many(filter).deleted_count
    