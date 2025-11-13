#Classe Plano de Assinatura
class Plano:

    # Método construtor para inicialização dos atributos
    def __init__(self, tipo_plano, id = None):
        self.tipo_plano = tipo_plano
        self.id = id