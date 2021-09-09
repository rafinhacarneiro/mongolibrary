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