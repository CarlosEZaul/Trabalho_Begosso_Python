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

arvoreCidades = ArvoreBinaria()
arvoreAlunos = ArvoreBinaria()
arvoreProfessores = ArvoreBinaria()
arvoreModalidades = ArvoreBinaria()
arvoreMatriculas = ArvoreBinaria()


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
    def imc(self):
        imc = self.peso / (self.altura**2)
        if imc < 18.5:
            diagnostico = "Abaixo do peso"
        elif imc < 25:
            diagnostico = "Peso normal"
        elif imc < 30:
            diagnostico = "Sobrepeso"
        else:
            diagnostico = "Obesidade"
        return imc, diagnostico

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

#-----------------CIDADES-----------------------------#
def carregarIndiceCidades():
    try:
        with open("dados/cidades.txt", "r", encoding="utf-8") as arquivo:
            while True:
                posicao = arquivo.tell()
                linha = arquivo.readline()
                if not linha:
                    break
                itens = linha.strip().split(";")
                if len(itens) < 1:
                    continue
                try:
                    codigo = int(itens[0])
                    arvoreCidades.inserir(codigo, posicao)
                except ValueError:
                    continue
    except FileNotFoundError:
        open("dados/cidades.txt", "w", encoding="utf-8").close()

def inserirCidade():
    while True:
        try:
            cod = int(input("Digite o codigo da cidade (0 cancela): "))
        except:
            print("Apenas valor inteiro!")
            continue

        if cod == 0:
            print("Operação cancelada.")
            break

        if arvoreCidades.buscar(cod) is not None:
            print("Codigo de cidade já existe!")
            continue

        descricao = input("Digite a descricao da cidade: ")
        estado = input("Digite o estado da cidade: ")

        cidade = Cidade(cod, descricao, estado)

        linha = f"{cidade.cod};{cidade.descricao};{cidade.estado}\n"

        arquivo = open("dados/cidades.txt", "a", encoding="utf-8")
        posicao = arquivo.tell()
        arquivo.write(linha)
        arvoreCidades.inserir(cod, posicao)

        print("Cidade salva com sucesso!")
        break

def buscarCidade():
    try:
        busca = int(input("Digite o codigo da cidade: "))
    except:
        print("Apenas valor inteiro!")
        return

    posicao = arvoreCidades.buscar(busca)
    if posicao is None:
        print("Cidade não encontrada no índice!")
        return

    arquivo= open("dados/cidades.txt", "r", encoding="utf-8")
    arquivo.seek(posicao)
    linha = arquivo.readline()
    itens = linha.strip().split(";")
    cidade = Cidade(int(itens[0]), itens[1], itens[2])
    print("Codigo: ", cidade.cod)
    print("Descricao: ", cidade.descricao)
    print("Estado: ", cidade.estado)
    print("\n\n")

def excluirCidade():
    try:
        cod = int(input("Digite o código da cidade para excluir (0 cancela): "))
    except:
        print("Apenas valor inteiro!")
        return

    if cod == 0:
        print("Operação cancelada.")
        return

    if arvoreCidades.buscar(cod) is None:
        print("Cidade não encontrada!")
        return

    arquivo= open("dados/cidades.txt", "r", encoding="utf-8")
    linhas = arquivo.readlines()

    arquivo= open("dados/cidades.txt", "w", encoding="utf-8")
    arvoreCidades.raiz = None
    for linha in linhas:
        itens = linha.strip().split(";")
        if int(itens[0]) != cod:
            cidade = Cidade(int(itens[0]), itens[1], itens[2])
            posicao = arquivo.tell()
            arquivo.write(f"{cidade.cod};{cidade.descricao};{cidade.estado}\n")
            arvoreCidades.inserir(cidade.cod, posicao)

    print("Cidade excluída com sucesso!")


#------------------------------------------------------------------#

#-------------------------ALUNOS-----------------------------------#
def carregarIndiceAlunos():
    try:
        arquivo=open("dados/alunos.txt", "r", encoding="utf-8")
        while True:
            posicao = arquivo.tell()
            linha = arquivo.readline()
            if not linha:
                break
            itens = linha.strip().split(";")
            if len(itens) < 1:
                continue
            try:
                codigo = int(itens[0])
                arvoreAlunos.inserir(codigo, posicao)
            except ValueError:
                continue
    except FileNotFoundError:
        open("dados/cidades.txt", "w", encoding="utf-8").close()

def inserirAluno():
    while True:
        try:
            cod = int(input("Digite o codigo do aluno (0 cancela): "))
        except:
            print("Apenas valor inteiro!")
            continue

        if cod == 0:
            print("Operação cancelada.")
            return
        if arvoreAlunos.buscar(cod) is not None:
            print("Codigo de aluno já existe!")
            continue

        nome = input("Digite o nome do aluno: ")

        while True:
            try:
                codigoCidade = int(input("Código da Cidade: "))
            except:
                print("Apenas valor inteiro!")
                continue

            if arvoreCidades.buscar(codigoCidade) is not None:
                break
            else:
                print("Código de cidade não encontrado")
                return

        dataNascimento = input("Data de Nascimento: ")
        while True:
            try:
                peso = float(input("Digite o peso do aluno(kg): "))
                altura = float(input("Digite o altura do aluno (m): "))
                break
            except:
                print('peso e altura devem ser valor reais!')
                continue

        aluno = Aluno(cod, nome, codigoCidade, dataNascimento, peso, altura)

        linha = f"{aluno.cod};{aluno.nome};{aluno.codCidade};{aluno.dataNascimento};{aluno.peso};{aluno.altura}\n"

        arquivo = open("dados/alunos.txt", "a", encoding="utf-8")
        posicao = arquivo.tell()
        arquivo.write(linha)
        arvoreAlunos.inserir(cod, posicao)

        print("Aluno salvo com sucesso!")
        break

def buscarAluno():
    try:
        busca = int(input("Digite o codigo do Aluno: "))
    except:
        print("Apenas valor inteiro!")
        return

    posicao = arvoreAlunos.buscar(busca)
    if posicao is None:
        print("Aluno não encontrado no índice!")
        return

    arquivo= open("dados/alunos.txt", "r", encoding="utf-8")
    arquivo.seek(posicao)
    linha = arquivo.readline()
    itens = linha.strip().split(";")
    aluno = Aluno(int(itens[0]), itens[1], int(itens[2]), itens[3], float(itens[4]), float(itens[5]))
    codCidade = aluno.codCidade
    posicaoCidade = arvoreCidades.buscar(codCidade)
    if posicaoCidade is None:
        nomeCidade = "Cidade não encontrada!"
        nomeEstado = ""
    else:
        arquivo = open("dados/cidades.txt", "r", encoding="utf-8")
        arquivo.seek(posicaoCidade)
        linha = arquivo.readline()
        itens = linha.strip().split(";")
        nomeCidade = itens[1]
        nomeEstado = itens[2]

    print("Nome do aluno: ", aluno.nome)
    print("Data de Nascimento: ", aluno.dataNascimento)
    print("Nome da Cidade: ", nomeCidade)
    print("Nome do Estado: ", nomeEstado)
    print("Peso: ", aluno.peso)
    print("Altura: ", aluno.altura)
    imc, diagnostico = aluno.imc()
    print(f"IMC: {imc:.2f}")
    print("Diagnostico: ", diagnostico)

    print("\n\n")

def excluirAluno():
    try:
        cod = int(input("Digite o código do aluno para excluir (0 cancela): "))
    except:
        print("Apenas valor inteiro!")
        return

    if cod == 0:
        print("Operação cancelada.")
        return

    if arvoreAlunos.buscar(cod) is None:
        print("Aluno não encontrada!")
        return

    arquivo= open("dados/alunos.txt", "r", encoding="utf-8")
    linhas = arquivo.readlines()

    arquivo= open("dados/alunos.txt", "w", encoding="utf-8")
    arvoreAlunos.raiz = None
    for linha in linhas:
        itens = linha.strip().split(";")
        if int(itens[0]) != cod:
            aluno = Aluno(int(itens[0]), itens[1], int(itens[2]), itens[3], float(itens[4]), float(itens[5]))
            posicao = arquivo.tell()
            linha = f"{aluno.cod};{aluno.nome};{aluno.codCidade};{aluno.dataNascimento};{aluno.peso};{aluno.altura}\n"
            arquivo.write(linha)
            arvoreAlunos.inserir(aluno.cod, posicao)

    print("Aluno excluída com sucesso!")

#------------------------------------------------------------------#
def menu():
    while True:
        print("\n--- MENU ---")
        print("1 - Inserir")
        print("2 - Buscar")
        print("3 - Deletar")
        print("4- Leitura Exaustiva")
        print("0 - Sair")
        opcao = input("Escolha: ")
#---------------INSERIR---------------------------#
        if opcao == "1":
            opcao= input("1- Inserir Aluno \n"
                         "2- Inserir Cidade \n"
                         "3- Inserir Matricula \n"
                         "4- Inserir Modalidade \n"
                         "5- Inserir Professores\n Escolha: ")
            if(opcao == "1"):
                inserirAluno()
            elif (opcao == "2"):
                inserirCidade()
#----------------BUSCAR----------------------#
        elif opcao == "2":
            opcao = input("1- Buscar Aluno \n"
                          "2- Buscar Cidade \n"
                          "3- Buscar Matricula \n"
                          "4- Buscar Modalidade \n"
                          "5- Buscar Professores\n Escolha: ")
            if(opcao == "1"):
                buscarAluno()
            elif (opcao == "2"):
                buscarCidade()
# ----------------DELETAR----------------------#
        elif opcao == "3":
            opcao = input("1- Deletar Aluno \n"
                          "2- Deletar Cidade \n"
                          "3- Deletar Matricula \n"
                          "4- Deletar Modalidade \n"
                          "5- Deletar Professores\n Escolha: ")
            if(opcao == "1"):
                excluirAluno()
            elif (opcao == "2"):
                excluirCidade()
#-----------------SAIR---------------------#
        elif opcao == "0":
            break
        else:
            continue
carregarIndiceCidades()
carregarIndiceAlunos()
menu()






