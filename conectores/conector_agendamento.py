# Módulo de conexão entre a classe e o banco de dados

# Imports
#from classes.atividade import Atividade
#from classes.membro import Membro
from classes.agendamento import Agendamento
import conectores.conector_atividade as atividade
import conectores.conector_membro as membro
from database.run_sql import run_sql


# Função que retorna todos os agendamentos
def get_all():

    agendamentos = []

    sql = "SELECT * FROM WEBUSER.TB_AGENDAMENTOS"
    results = run_sql(sql)

    for row in results:

        membro = membro.get_one(row["membro"])
        atividade = atividade.get_one(row["atividade"])

        agendamento = Agendamento(atividade,
                                  membro,
                                  row["id"])
        agendamentos.append(agendamento)

    return agendamentos

# Função que retorna um agendamento
def get_one(id):

    sql = "SELECT * FROM WEBUSER.TB_AGENDAMENTOS WHERE ID = %s"
    value = [id]

    result = run_sql(sql, value)[0]

    membro = membro.get_one(result["membro"])
    atividade = atividade.get_one(result["atividade"])

    if result is not None:
        agendamento = Agendamento(atividade,
                                  membro,
                                  result["id"])

    return agendamento

# Função que insere um agendamento
def new(agendamento):

    sql = "INSERT INTO WEBUSER.TB_AGENDAMENTOS SET ( nome, " \
    "instrutor, data, duracao, capacidade, tipo_plano, ativo )"
    " VALUES ( %s, %s, %s, %s, %s, %s, %s ) RETURNING *;"
    values = [agendamento.atividade,
              agendamento.membro]

    results = run_sql(sql, values)

    agendamento.id = results[0]["id"]

    return agendamento


# Função que deleta um agendamento
def delete_one(id):

    sql = "DELETE FROM WEBUSER.TB_AGENDAMENTOS WHERE ID = %s"
    value = [id]

    run_sql(sql, value)





