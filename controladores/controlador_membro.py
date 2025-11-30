# Controlador de Membros

# Imports
from flask import render_template, request, redirect
from flask import Blueprint
from classes.membro import Membro
import conectores.conector_membro as conector_membro
import conectores.conector_plano as conector_plano

# Cria blueprint (instância da classe)
membros_blueprint = Blueprint("membros", __name__)

# Rota para a página index.html para buscar membros ativos
@membros_blueprint.route("/membros")
def membros_index():
    membros = conector_membro.get_all_active()
    return render_template("membros/index.html", membros=membros, title="Membros Ativos")

# Rota para a página index.html para buscar membros inativos
@membros_blueprint.route("/membros/inativo")
def membros_inativos():
    membros = conector_membro.get_all_inactive()
    return render_template("membros/index.html", membros=membros, title="Membros Inativos")

# Rota para a página de cadastro de membro
@membros_blueprint.route("/membros/novo")
def novo_membro():
    tipos_planos = conector_plano.get_all()
    return render_template("membros/novo.html", tipos_planos=tipos_planos, title="Novo Membro")

# Método POST para criar um novo membro
@membros_blueprint.route("/membros", methods=["POST"])
def cadastra_membro():
    nome            = request.form["nome"]
    sobrenome       = request.form["sobrenome"]
    data_nascimento = request.form["data_nascimento"]
    email           = request.form["email"]
    endereco        = request.form["endereco"]
    telefone        = request.form["telefone"]
    tipo_plano      = request.form["tipo_plano"]
    data_inicio     = request.form["data_inicio"]
    ativo           = request.form["ativo"]
    plano           = conector_plano.get_one(tipo_plano)
    novo_membro = Membro(nome, sobrenome, data_nascimento, email, endereco, telefone, plano, data_inicio, ativo)
    conector_membro.new(novo_membro)

    return redirect("/membros")

# Rota para a página de edição de um membro
@membros_blueprint.route("/membros/<id>/editar")
def editar_membro(id):
    membro = conector_membro.get_one(id)
    tipos_planos = conector_plano.get_all()
    return render_template("membros/editar.html", membro=membro, tipos_planos=tipos_planos, title="Editar Detalhes do Membro")

# Método POST para atualizar um membro
@membros_blueprint.route("/membros/<id>", methods=["POST"])
def atualiza_membro(id):
    nome            = request.form["nome"]
    sobrenome       = request.form["sobrenome"]
    data_nascimento = request.form["data_nascimento"]
    email           = request.form["email"]
    endereco        = request.form["endereco"]
    telefone        = request.form["telefone"]
    tipo_plano      = request.form["tipo_plano"]
    data_inicio     = request.form["data_inicio"]
    ativo           = request.form["ativo"]
    plano           = conector_plano.get_one(tipo_plano)

    membro_atualizado = Membro(nome, sobrenome, data_nascimento, email, endereco, telefone, plano, data_inicio, ativo, id)
    conector_membro.edit(membro_atualizado)

    return redirect("/membros")

# Rota para a página de detalhes de um membro
@membros_blueprint.route("/membros/<id>")
def mostra_membro(id):
    membro_atividades = conector_membro.get_activities(id)
    membro = conector_membro.get_one(id)
    tipo_plano = conector_plano.get_one(membro.tipo_plano.id)
    return render_template("membros/mostrar.html",
                            membro=membro, membro_atividades=membro_atividades,
                            tipo_plano=tipo_plano,
                             title="Detalhes do Membro")

# Rota para deletar um membro
@membros_blueprint.route("/membros/<id>/deletar")
def deleta_membro(id):
    conector_membro.delete_one(id)
    return redirect("/membros")