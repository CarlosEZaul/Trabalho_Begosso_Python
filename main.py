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


def inserirCidade():
        arquivo= open("dados/cidades.txt", "r")
        for linha in arquivo:
            item = linha.split()
            while True:
                item = linha.split()
                cod = int(input("Digite o codigo da cidade (0 cancela): "))
                if int(item[0]) == cod:
                    print("Codigo de cidade já existe!")
                    continue
                else:
                    break
            arquivo = open("dados/cidades.txt", "a", encoding="utf-8")
            descricao = input("Digite o descricao da cidade: ")
            estado = input("Digite o estado da cidade: ")

            cidade = Cidade(cod, descricao, estado)

            linha = f"{cidade.cod} {cidade.descricao} {cidade.estado}\n"
            arquivo.write(linha)
            print("Arquivo salvo com sucesso!")


def buscarCidade():
    arquivo = open("dados/cidades.txt", "r")
    busca = int(input("Digite o codigo da cidade: "))
    for linha in arquivo:
        itens = linha.split()
        if(busca == int(itens[0])):
            print("Codigo: ", itens[0])
            print("Descricao: ", itens[1])
            print("Estado: ", itens[2])
            print("\n\n")
            return
    arquivo.close()


def menu():
    while True:
        print("\n--- MENU ---")
        print("1 - Inserir")
        print("2 - Listar")
        print("3 - Buscar")
        print("0 - Sair")
        opcao = input("Escolha: ")

        if opcao == "1":
            opcao= input("1- Inserir Aluno \n2- Inserir Cidade \n3- Inserir Matricula \n4- Inserir Modalidade \n5- Professores\n Escolha: ")
            if(opcao == "1"):
                return
            elif (opcao == "2"):
                inserirCidade()

        if opcao == "3":
            buscarCidade()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

menu()






