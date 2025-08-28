class No:
    def __init__(self, codigo, endereco):
        self.codigo = codigo
        self.posicao = endereco
        self.esquerda = None
        self.direita = None

class ArvoreBinaria:
    def __init__(self):
        self.raiz = None

    def inserir(self, codigo, endereco):
        if self.raiz is None:
            self.raiz = No(codigo, endereco)
        else:
            self.inserirNo(self.raiz, codigo, endereco)

    def inserirNo(self, atual, codigo, endereco):
        if codigo < atual.codigo:
            if atual.esquerda is None:
                atual.esquerda = No(codigo, endereco)
            else:
                self.inserirNo(atual.esquerda, codigo, endereco)
        else:
            if atual.direita is None:
                atual.direita = No(codigo, endereco)
            else:
                self.inserirNo(atual.direita, codigo, endereco)

    def buscar(self, codigo):
        return self.buscarIndice(self.raiz, codigo)

    def buscarIndice(self, atual, codigo):
        if atual is None:
            return None
        if codigo == atual.codigo:
            return atual.posicao
        elif codigo < atual.codigo:
            return self.buscarIndice(atual.esquerda, codigo)
        else:
            return self.buscarIndice(atual.direita, codigo)

    def remover(self, codigo):
        self.raiz = self.removerNo(self.raiz, codigo)

    def removerNo(self, atual, codigo):
        if atual is None:
            return None

        if codigo < atual.codigo:
            atual.esquerda = self.removerNo(atual.esquerda, codigo)
        elif codigo > atual.codigo:
            atual.direita = self.removerNo(atual.direita, codigo)
        else:
            if atual.esquerda is None and atual.direita is None:
                return None
            elif atual.esquerda is None:
                return atual.direita
            elif atual.direita is None:
                return atual.esquerda
            else:
                menorNo = self.encontrarMenor(atual.direita)
                atual.codigo = menorNo.codigo
                atual.posicao = menorNo.posicao
                atual.direita = self.removerNo(atual.direita, menorNo.codigo)
        return atual

    def encontrarMenor(self, atual):
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def em_ordem(self, visitar):
            def percorrer(atual):
                if atual is not None:
                    percorrer(atual.esquerda)
                    visitar(atual)
                    percorrer(atual.direita)
            percorrer(self.raiz)
arvore = ArvoreBinaria()




class Cidade:
    def __init__(self, cod, descricao, estado):
        self.cod = cod
        self.descricao = descricao
        self.estado = estado
class Aluno:
    def __init__(self, cod, nome, codCidade, dataNascimento, peso, altura):
        self.cod = cod
        self.nome = nome
        self.codCidade = codCidade
        self.dataNascimento = dataNascimento
        self.peso = peso
        self.altura = altura
class Professor:
    def __init__(self, cod, nome, endereco, telefone, codCidade):
        self.cod = cod
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.codCidade = codCidade
class Modalidade:
    def __init__(self,codModalidade, descricao, codProfessor, valor, limiteAlunos, totalAlunos):
        self.cod = codModalidade
        self.descricao = descricao
        self.codProfessor = codProfessor
        self.valor = valor
        self.limiteAlunos = limiteAlunos
        self.totalAlunos = totalAlunos
class Matricula:
    def __init__(self, codMatricula, codAluno, codModalidade, qtdeAulas):
        self.cod = codMatricula
        self.codAluno = codAluno
        self.codModalidade = codModalidade
        self.qtdeAulas = qtdeAulas


def buscar():

def consultar():

def deletar():

def leituraExaustiva():





