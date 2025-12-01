# Controlador de Agendamentos

# Imports
from flask import render_template, request, redirect
from flask import Blueprint
from classes.agendamento import Agendamento
import conectores.conector_agendamento as conector_agendamento
import conectores.conector_membro as conector_membro
import conectores.conector_atividade as conector_atividade
import conectores.conector_plano as conector_plano

# Cria blueprint (instância da classe)
agendamentos_blueprint = Blueprint("agendamentos", __name__)

# Rota para a página index.html 
@agendamentos_blueprint.route("/agendamentos")
def agendamentos_index():
    agendamentos = conector_agendamento.get_all()
    return render_template("agendamentos/index.html", agendamentos=agendamentos, title="Agendamentos")

# Rota para novo membro
@agendamentos_blueprint.route("/agendamentos/novo/membro/<id>")
def novo_membro_agendamento(id):
    membro      = conector_membro.get_one(id)
    atividades  = conector_atividade.get_all_active()
    return render_template("agendamentos/novo.html", membro=membro, atividades=atividades, title="Novo Agendamento")

# Rota para nova atividade
@agendamentos_blueprint.route("/agendamentos/novo/atividade/<id>")
def nova_atividade_agendamento(id):
    atividade   = conector_atividade.get_one(id)
    membros     = conector_membro.get_all_active()
    return render_template("agendamentos/novo.html", atividade=atividade, membros=membros, title="Novo Agendamento")

# Rota para criar agendamento a partir de atividade
@agendamentos_blueprint.route("/agendamentos/atividade", methods=["POST"])
def cria_agendamento_from_atividade():
    membro_id       = request.form["membro"]
    atividade_id    = request.form["atividade"]
    membro          = conector_membro.get_one(membro_id)
    atividade       = conector_atividade.get_one(atividade_id)
    plano_membro    = conector_plano.get_one(membro.tipo_plano.id)
    plano_atividade = conector_plano.get_one(atividade.tipo_plano.id)
    agendamentos_atuais = len(conector_atividade.get_members(atividade_id))
    atividades      = conector_atividade.get_all_active()

    if conector_agendamento.check_existing(atividade_id, membro_id) == True:
        error = "Agendamento já existe!"
        return render_template("agendamentos/novo-membro.html", atividades=atividades, membros=membro, error=error, title="Novo Agendamento")

    elif plano_membro.tipo_plano == "Mensal" and plano_atividade.tipo_plano == "Anual":
        error = "Plano do membro não permite agendamento para esta atividade!"
        return render_template("agendamentos/novo-atividade.html", atividades=atividades, membro=membro, error=error, title="Novo Agendamento")
    
    elif agendamentos_atuais >= atividade.capacidade:
        error = "Capacidade máxima da atividade atingida!"
        return render_template("agendamentos/novo-atividade.html", atividades=atividades, membro=membro, error=error, title="Novo Agendamento")
    
    else:
        novo_agendamento = Agendamento(atividade, membro)
        conector_agendamento.new(novo_agendamento)
        pagina_atividade = f"/atividades/{atividade_id}"
        return redirect(pagina_atividade)

# Rota para criar agendamento a partir de membro
@agendamentos_blueprint.route("/agendamentos/membro", methods=["POST"])
def cria_agendamento_from_membro():
    membro_id       = request.form["membro"]
    atividade_id    = request.form["atividade"]
    membro          = conector_membro.get_one(membro_id)
    atividade       = conector_atividade.get_one(atividade_id)
    plano_membro    = conector_plano.get_one(membro.tipo_plano.id)
    plano_atividade = conector_plano.get_one(atividade.tipo_plano.id)
    agendamentos_atuais = len(conector_atividade.get_members(atividade_id))
    atividades      = conector_atividade.get_all_active()

    if conector_agendamento.check_existing(atividade_id, membro_id) == True:
        error = "Agendamento já existe!"
        return render_template("agendamentos/novo-atividade.html", membro=membro, atividades=atividades, error=error, title="Novo Agendamento")

    elif plano_membro.tipo_plano == "Mensal" and plano_atividade.tipo_plano == "Anual":
        error = "Plano do membro não permite agendamento para esta atividade!"
        return render_template("agendamentos/novo-atividade.html", membro=membro, atividades=atividades, error=error, title="Novo Agendamento")
    
    elif agendamentos_atuais >= atividade.capacidade:
        error = "Capacidade máxima da atividade atingida!"
        return render_template("agendamentos/novo-atividade.html", membro=membro, atividades=atividades, error=error, title="Novo Agendamento")
    
    else:
        novo_agendamento = Agendamento(atividade, membro)
        conector_agendamento.new(novo_agendamento)
        pagina_membro = f"/membros/{membro_id}"
        return redirect(pagina_membro)
    
# Rota para deletar agendamento
@agendamentos_blueprint.route("/agendamentos/<id>/delete")
def deleta_agendamento(id):
    conector_agendamento.delete_one(id)
    return redirect("/agendamentos")

# Rota para deletar agendamento de membro
@agendamentos_blueprint.route("/agendamentos/delete/membro/<membro_id>/<atividade_id>")
def deleta_agendamento_membro(membro_id, atividade_id):
    conector_agendamento.delete_by_atividade_membro(atividade_id, membro_id)
    pagina_membro = f"/membros/{membro_id}"
    return redirect(pagina_membro)

# Rota para deletar agendamento de atividade
@agendamentos_blueprint.route("/agendamentos/delete/atividade/<membro_id>/<atividade_id>")
def deleta_agendamento_atividade(membro_id, atividade_id):
    conector_agendamento.delete_by_atividade_membro(atividade_id, membro_id)
    pagina_atividade = f"/atividades/{atividade_id}"
    return redirect(pagina_atividade)

