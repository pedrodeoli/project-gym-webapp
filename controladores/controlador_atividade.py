# Controlador de Atividades

# Imports
from flask import render_template, request, redirect
from flask import Blueprint
from classes.atividade import Atividade
import conectores.conector_atividade as conector_atividade
import conectores.conector_instrutor as conector_instrutor
import conectores.conector_plano as conector_plano

# Cria blueprint (instância da classe)
atividades_blueprint = Blueprint("atividades", __name__)

# Rota para a página index.html com atividades ativas
@atividades_blueprint.route("/atividades")
def atividades_index():
    atividades = conector_atividade.get_all_active()
    return render_template("atividades/index.html", atividades=atividades, title="Atividades")

# Rota para a página index.html com atividades inativas
@atividades_blueprint.route("/atividades/inativo")
def inactive_atividades():
    atividades = conector_atividade.get_all_inactive()
    return render_template("atividades/index.html", atividades=atividades, title="Atividades")

# Rota para a página de cadastro de atividade
@atividades_blueprint.route("/atividades/novo")
def nova_atividade():
    instrutores = conector_instrutor.get_all()
    tipos_planos = conector_plano.get_all()
    return render_template("atividades/novo.html", instrutores=instrutores, tipos_planos=tipos_planos, title="Nova Atividade")

# Método POST para criar uma nova atividade
@atividades_blueprint.route("/atividades", methods=["POST"])
def cria_instrutor():
    nome            = request.form["nome"]
    instrutor       = request.form["instrutor"]
    data            = request.form["data"]
    duracao         = request.form["duracao"]
    capacidade      = request.form["capacidade"]
    tipo_plano      = request.form["tipo_plano"]
    ativo           = request.form["ativo"]
    plano           = conector_plano.get_one(tipo_plano)
    instrutor       = conector_instrutor.get_one(instrutor)
    nova_atividade = Atividade(nome, instrutor, data, duracao, capacidade, plano, ativo)
    conector_atividade.new(nova_atividade)

    return redirect("/atividades")

# Rota para a página de edição de uma atividade
@atividades_blueprint.route("/instrutores/<id>/editar")
def editar_atividade(id):
    instrutores = conector_instrutor.get_all()
    tipos_planos = conector_plano.get_all()
    atividade = conector_atividade.get_one(id)
    instrutor = conector_instrutor.get_one(atividade.instrutor)
    plano = conector_plano.get_one(atividade.tipo_plano.id)

    return render_template("atividades/editar.html", 
                           atividade=atividade, 
                           instrutores=instrutores, 
                           tipos_planos=tipos_planos, 
                           instrutor=instrutor, 
                           plano=plano, 
                           title="Editar Detalhes da Atividade")

# Método POST para atualizar um instrutor
@atividades_blueprint.route("/instrutores/<id>", methods=["POST"])
def atualiza_atividade(id):
    nome            = request.form["nome"]
    instrutor       = request.form["instrutor"]
    data            = request.form["data"]
    duracao         = request.form["duracao"]
    capacidade      = request.form["capacidade"]
    tipo_plano      = request.form["tipo_plano"]
    ativo           = request.form["ativo"]
    plano           = conector_plano.get_one(tipo_plano)
    instrutor       = conector_instrutor.get_one(instrutor)
    atualiza_atividade = Atividade(nome, instrutor, data, duracao, capacidade, plano, ativo, id)
    conector_atividade.edit(atualiza_atividade)

    return redirect("/atividades")


# Rota para a página de detalhes de um instrutor
@atividades_blueprint.route("/atividades/<id>")
def mostra_atividade(id):
    atividade = conector_atividade.get_one(id)
    instrutor = conector_instrutor.get_one(atividade.instrutor)
    tipo_plano = conector_plano.get_one(atividade.tipo_plano.id)
    membros_atividade = conector_atividade.get_members(id)
    num_membros = len(membros_atividade)
    return render_template("atividades/mostrar.html",
                            atividade=atividade, 
                            instrutor=instrutor, 
                            tipo_plano=tipo_plano, 
                            membros_atividade=membros_atividade,
                            num_membros=num_membros,
                            title="Detalhes da Atividade")

# Rota para deletar um instrutor
@atividades_blueprint.route("/atividades/<id>/deletar")
def deleta_atividades(id):
    conector_atividade.delete_one(id)
    return redirect("/atividades")