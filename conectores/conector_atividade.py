# Módulo de conexão entre a classe e o banco de dados

# Imports
from classes.atividade import Atividade
import conectores.conector_plano as plano 
from classes.membro import Membro
from database.run_sql import run_sql


# Função que retorna todas as atividades
def get_all():

    atividades = []

    sql = "SELECT * FROM WEBUSER.TB_ATIVIDADES ORDER BY DATA ASC"
    results = run_sql(sql)

    for row in results:

        tipo_plano = plano.get_one(row["tipo_plano"])

        atividade = Atividade(row["nome"], 
                              row["instrutor"],
                              row["data"],
                              row["duracao"],
                              row["capacidade"],
                              tipo_plano,
                              row["ativo"],
                              row["id"])
        atividades.append(atividade)

    return atividades

# Função que retorna uma atividade
def get_one(id):

    sql = "SELECT * FROM WEBUSER.TB_ATIVIDADES WHERE ID = %s"
    value = [id]

    result = run_sql(sql, value)[0]

    tipo_plano = plano.get_one(result["tipo_plano"])

    if result is not None:
        atividade = Atividade(result["nome"], 
                              result["instrutor"],
                              result["data"],
                              result["duracao"],
                              result["capacidade"],
                              tipo_plano,
                              result["ativo"],
                              result["id"])

    return atividade

# Função que insere uma atividade
def new(atividade):

    sql = "INSERT INTO WEBUSER.TB_ATIVIDADES SET ( nome, " \
    "instrutor, data, duracao, capacidade, tipo_plano, ativo )"
    " VALUES ( %s, %s, %s, %s, %s, %s, %s ) RETURNING *;"
    values = [atividade.nome,
              atividade.instrutor,
              atividade.data,
              atividade.duracao,
              atividade.capacidade,
              atividade.tipo_plano,
              atividade.ativo]

    results = run_sql(sql, values)

    atividade.id = results[0]["id"]

    return atividade

# Função que altera uma atividade
def edit(atividade):

    sql = "INSERT INTO WEBUSER.TB_ATIVIDADES SET ( nome, " \
    "instrutor, data, duracao, capacidade, tipo_plano, ativo )" \
    " = ( %s, %s, %s, %s, %s, %s, %s ) WHERE ID = %s;"
    values = [atividade.nome,
              atividade.instrutor,
              atividade.data,
              atividade.duracao,
              atividade.capacidade,
              atividade.tipo_plano,
              atividade.ativo,
              atividade.id]

    run_sql(sql, values)

# Função que deleta uma atividade
def delete_one(id):

    sql = "DELETE FROM WEBUSER.TB_ATIVIDADES WHERE ID = %s"
    value = [id]

    run_sql(sql, value)

# Função que lista membros de um atividade
def get_members(id):

    membros = []

    sql = "SELECT * FROM WEBUSER.TB_MEMBROS WHERE ATIVIDADE = %s"
    value = [id]

    results = run_sql(sql, value)

    for row in results:
        membro = Membro(row["nome"],
                        row["sobrenome"],
                        row["data_nascimento"],
                        row["endereco"],
                        row["telefone"],
                        row["email"],
                        row["tipo_plano"],
                        row["data_inicio"],
                        row["ativo"],
                        row["id"])
        membros.append(membro)

    return membros

# Função que lista atividades ativas
def get_all_active():

    atividades = []

    sql = "SELECT * FROM WEBUSER.TB_ATIVIDADES WHERE ATIVO = TRUE ORDER BY DATA ASC"
    results = run_sql(sql)

    for row in results:

        tipo_plano = plano.get_one(row["tipo_plano"])

        atividade = Atividade(row["nome"], 
                              row["instrutor"],
                              row["data"],
                              row["duracao"],
                              row["capacidade"],
                              tipo_plano,
                              row["ativo"],
                              row["id"])
        
        atividades.append(atividade)

    return atividades

# Função que lista atividades inativas
def get_all_active():

    atividades = []

    sql = "SELECT * FROM WEBUSER.TB_ATIVIDADES WHERE ATIVO = FALSE ORDER BY DATA ASC"
    results = run_sql(sql)

    for row in results:

        tipo_plano = plano.get_one(row["tipo_plano"])

        atividade = Atividade(row["nome"], 
                              row["instrutor"],
                              row["data"],
                              row["duracao"],
                              row["capacidade"],
                              tipo_plano,
                              row["ativo"],
                              row["id"])
        
        atividades.append(atividade)

    return atividades