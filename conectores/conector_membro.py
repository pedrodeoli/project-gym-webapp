# Módulo de conexão entre a classe e o banco de dados

# Imports
from classes.membro import Membro
from classes.agendamento import Agendamento
import conector_plano as plano
from database.run_sql import run_sql


# Função que retorna todos os membros
def get_all():

    membros = []

    sql = "SELECT * FROM WEBUSER.TB_MEMBROS ORDER BY NOME ASC"
    results = run_sql(sql)

    for row in results:
        
        tipo_plano = plano.get_one(row["tipo_plano"])

        membro = Membro(row["nome"], 
                        row["sobrenome"],
                        row["data_nascimento"],
                        row["endereco"],
                        row["telefone"],
                        row["email"],
                        tipo_plano,
                        row["data_inicio"],
                        row["ativo"],
                        row["id"])
        membros.append(membro)

    return membros

# Função que retorna um membro
def get_one(id):

    sql = "SELECT * FROM WEBUSER.TB_MEMBROS WHERE ID = %s"
    value = [id]

    result = run_sql(sql, value)[0]

    if result is not None:

        tipo_plano = plano.get_one(result["tipo_plano"])

        membro = Membro(result["nome"], 
                        result["sobrenome"],
                        result["data_nascimento"],
                        result["endereco"],
                        result["telefone"],
                        result["email"],
                        tipo_plano,
                        result["data_inicio"],
                        result["ativo"],
                        result["id"])

    return membro

# Função que insere um membro
def new(membro):

    sql = "INSERT INTO WEBUSER.TB_MEMBROS SET ( nome, " \
    "sobrenome, data_nascimento, endereco, telefone, email," \
    "tipo_plano, data_inicio, ativo )"
    " VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s ) RETURNING *;"
    values = [membro.nome,
              membro.sobrenome,
              membro.data_nascimento,
              membro.endereco,
              membro.telefone,
              membro.email,
              membro.tipo_plano,
              membro.data_inicio,
              membro.ativo]

    results = run_sql(sql, values)

    membro.id = results[0]["id"]

    return membro

# Função que altera um membro
def edit(membro):

    sql = "UPDATE FROM WEBUSER.TB_MEMBROS SET ( nome, " \
    "sobrenome, data_nascimento, endereco, telefone, email," \
    "tipo_plano, data_inicio, ativo )" \
    " = (%s, %s, %s, %s, %s, %s, %s, %s, %s) WHERE ID = %s;"
    values = [membro.nome,
              membro.sobrenome,
              membro.data_nascimento,
              membro.endereco,
              membro.telefone,
              membro.email,
              membro.tipo_plano,
              membro.data_inicio,
              membro.ativo,
              membro.id]

    run_sql(sql, values)

# Função que deleta um membro
def delete_one(id):

    sql = "DELETE FROM WEBUSER.TB_MEMBROS WHERE ID = %s"
    value = [id]

    run_sql(sql, value)

# Função que lista todas os agendamentos de um membro
def get_activities(id_membro):

    agendamentos = []

    sql = "SELECT * FROM WEBUSER.TB_AGENDAMENTOS WHERE MEMBRO = %s"
    value = [id_membro]

    results = run_sql(sql, value)

    for row in results:
        agendamento = Agendamento(row["atividade"],
                                  row["membro"],
                                  row["id"])
        
        agendamentos.append(agendamento)

    return agendamentos

# Função que lista membros ativos
def get_all_active():

    membros = []

    sql = "SELECT * FROM WEBUSER.TB_MEMBROS WHERE ATIVO = TRUE ORDER BY NOME ASC"
    results = run_sql(sql)

    for row in results:

        tipo_plano = plano.get_one(row["tipo_plano"])

        membro = Membro(row["nome"], 
                        row["sobrenome"],
                        row["data_nascimento"],
                        row["endereco"],
                        row["telefone"],
                        row["email"],
                        tipo_plano,
                        row["data_inicio"],
                        row["ativo"],
                        row["id"])
        
        membros.append(membro)

    return membros

# Função que lista membros ativos
def get_all_active():

    membros = []

    sql = "SELECT * FROM WEBUSER.TB_MEMBROS WHERE ATIVO = FALSE ORDER BY NOME ASC"
    results = run_sql(sql)

    for row in results:

        tipo_plano = plano.get_one(row["tipo_plano"])

        membro = Membro(row["nome"], 
                        row["sobrenome"],
                        row["data_nascimento"],
                        row["endereco"],
                        row["telefone"],
                        row["email"],
                        tipo_plano,
                        row["data_inicio"],
                        row["ativo"],
                        row["id"])
        
        membros.append(membro)

    return membros