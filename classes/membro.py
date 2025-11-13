#Classe membro (usuário) da academia
class Membro:

    # Método construtor para inicialização dos atributos
    def __init__(self, nome, sobrenome, data_nascimento, endereco, telefone, email, tipo_plano, ativo, id = None):
        self.nome = nome
        self.sobrenome = sobrenome
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.telefone = telefone
        self.email = email
        self.tipo_plano = tipo_plano
        self.ativo = ativo
        self.id = id