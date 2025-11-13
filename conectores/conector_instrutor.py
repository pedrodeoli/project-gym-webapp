# Módulo de conexão entre a classe e o banco de dados

# Imports
from classes.instrutor import Instrutor
from classes.atividade import Atividade
from database.run_sql import run_sql


# Função que retorna todos os instrutores
def get_all():

    instrutores = []

    sql = "SELECT * FROM WEBUSER.TB_INSTRUTORES"
    results = run_sql(sql)

    for row in results:
        instrutor = Instrutor(row["nome"], 
                              row["sobrenome"],
                              row["data_nascimento"],
                              row["endereco"],
                              row["telefone"],
                              row["id"])
        instrutores.append(instrutor)

    return instrutores

# Função que retorna um instrutor
def get_one(id):

    sql = "SELECT * FROM WEBUSER.TB_INSTRUTORES WHERE ID = %s"
    value = [id]

    result = run_sql(sql, value)[0]

    if result is not None:
        instrutor = Instrutor(result["nome"], 
                              result["sobrenome"],
                              result["data_nascimento"],
                              result["endereco"],
                              result["telefone"],
                              result["id"])

    return instrutor

# Função que insere um instrutor
def new(instrutor):

    sql = "INSERT INTO WEBUSER.TB_INSTRUTORES SET ( nome, " \
    "sobrenome, data_nascimento, endereco, telefone )"
    " VALUES ( %s, %s, %s, %s, %s ) RETURNING *;"
    values = [instrutor.nome,
              instrutor.sobrenome,
              instrutor.data_nascimento,
              instrutor.endereco,
              instrutor.telefone]

    results = run_sql(sql, values)

    instrutor.id = results[0]["id"]

    return instrutor

# Função que altera um instrutor
def edit(instrutor):

    sql = "UPDATE FROM WEBUSER.TB_INSTRUTORES SET ( nome, " \
    "sobrenome, data_nascimento, endereco, telefone )" \
    " = (%s, %s, %s, %s, %s) WHERE ID = %s;"
    values = [instrutor.nome,
              instrutor.sobrenome,
              instrutor.data_nascimento,
              instrutor.endereco,
              instrutor.telefone,
              instrutor.id]

    run_sql(sql, values)

# Função que deleta um instrutor
def delete_one(id):

    sql = "DELETE FROM WEBUSER.TB_INSTRUTORES WHERE ID = %s"
    value = [id]

    run_sql(sql, value)

# Função que lista todas as atividades de um instrutor
def get_activities(id_instrutor):

    atividades = []

    sql = "SELECT * FROM WEBUSER.TB_ATIVIDADES WHERE INSTRUTOR = %s"
    value = [id_instrutor]

    results = run_sql(sql, value)

    for row in results:
        atividade = Atividade(row["nome"],
                              row["instrutor"],
                              row["data"],
                              row["duracao"],
                              row["capacidade"],
                              row["tipo_plano"],
                              row["ativo"],
                              row["id"])
        
        atividades.append(atividade)

    return atividades