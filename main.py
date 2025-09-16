import os

import customtkinter
import customtkinter as ctk




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
        if self.altura <= 0:
            return 0, "Altura inválida"
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
        arquivo= open("dados/cidades.txt", "r", encoding="utf-8")
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
    arquivo.close()
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
        open("dados/alunos.txt", "w", encoding="utf-8").close()

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
                continue

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
        arquivo.close()

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
    arquivo.close()
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

    arquivo.close()
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


#-------------------------Professor-----------------------------------#
def carregarIndiceProfessor():
    try:
        arquivo = open("dados/professor.txt", "r", encoding="utf-8")
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
                arvoreProfessores.inserir(codigo, posicao)
            except ValueError:
                continue
    except FileNotFoundError:
        open("dados/professor.txt", "w", encoding="utf-8").close()

def inserirProfessor():
    while True:
        try:
            cod = int(input("Digite o codigo do Professor (0 cancela): "))
        except:
            print("Apenas valor inteiro!")
            continue

        if cod == 0:
            print("Operação cancelada.")
            return
        if arvoreProfessores.buscar(cod) is not None:
            print("Codigo de professor já existe!")
            continue

        nome = input("Digite o nome do professor: ")

        while True:
            try:
                codCidade = int(input("Código da Cidade: "))
            except:
                print("Apenas valor inteiro!")
                continue

            if arvoreCidades.buscar(codCidade) is not None:
                break
            else:
                print("Código de cidade não encontrado")
                continue

        endereco = input("Endereço do professor: ")

        telefone = input("Telefone: ")


        professor = Professor( cod, nome, endereco, telefone, codCidade)

        linha = f"{professor.cod};{professor.nome};{professor.endereco};{professor.telefone};{professor.codCidade}\n"

        arquivo = open("dados/professor.txt", "a", encoding="utf-8")
        posicao = arquivo.tell()
        arquivo.write(linha)
        arvoreProfessores.inserir(cod, posicao)

        print("Professor salvo com sucesso!")
        break

def buscarProfessor():
    try:
        busca = int(input("Digite o codigo do Professor: "))
    except:
        print("Apenas valor inteiro!")
        return

    posicao = arvoreProfessores.buscar(busca)
    if posicao is None:
        print("Professor não encontrado no índice!")
        return

    arquivo = open("dados/professor.txt", "r", encoding="utf-8")
    arquivo.seek(posicao)
    linha = arquivo.readline()
    itens = linha.strip().split(";")
    professor = Professor(int(itens[0]), itens[1], itens[2], itens[3], int(itens[4]))
    codCidade = professor.codCidade
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

    print("Nome do Professor: ", professor.nome)
    print("Telefone: ", professor.telefone)
    print("Endereço: ", professor.endereco)
    print("Cidade: ", nomeCidade)
    print("Nome do Estado: ", nomeEstado)
    arquivo.close()
    print("\n\n")

def excluirProfessor():
    try:
        cod = int(input("Digite o código do professor para excluir (0 cancela): "))
    except:
        print("Apenas valor inteiro!")
        return

    if cod == 0:
        print("Operação cancelada.")
        return

    if arvoreProfessores.buscar(cod) is None:
        print("Professor não encontrado!")
        return

    arquivo = open("dados/professor.txt", "r", encoding="utf-8")
    linhas = arquivo.readlines()
    arquivo.close()

    arquivo = open("dados/professor.txt", "w", encoding="utf-8")
    arvoreProfessores.raiz = None
    for linha in linhas:
        itens = linha.strip().split(";")
        if int(itens[0]) != cod:
            professor = Professor(int(itens[0]), itens[1], itens[2], itens[3], int(itens[4]))
            posicao = arquivo.tell()
            linha = f"{professor.cod};{professor.nome};{professor.endereco};{professor.telefone};{professor.codCidade}\n"
            arquivo.write(linha)
            arvoreProfessores.inserir(professor.cod, posicao)

    arquivo.close()
    print("Professor excluído com sucesso!")


#-----------------------MODALIDADES_____________________________________#
def carregarIndiceModalidades():
    try:
        arquivo = open("dados/modalidades.txt", "r", encoding="utf-8")
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
                arvoreModalidades.inserir(codigo, posicao)
            except ValueError:
                continue
    except FileNotFoundError:
        open("dados/modalidades.txt", "w", encoding="utf-8").close()


def inserirModalidade():
    while True:
        try:
            cod = int(input("Digite o código da modalidade (0 cancela): "))
        except:
            print("Apenas valor inteiro!")
            continue

        if cod == 0:
            print("Operação cancelada.")
            return
        if arvoreModalidades.buscar(cod) is not None:
            print("Código de modalidade já existe!")
            continue

        descricao = input("Descrição da Modalidade: ")

        while True:
            try:
                codProfessor = int(input("Código do professor: "))
            except:
                print("Apenas valor inteiro!")
                continue

            posProfessor = arvoreProfessores.buscar(codProfessor)
            if posProfessor is not None:
                arquivoProf = open("dados/professor.txt", "r", encoding="utf-8")
                arquivoProf.seek(posProfessor)
                linhaProf = arquivoProf.readline().strip().split(";")
                nomeProfessor = linhaProf[1]
                cidadeProfessor = linhaProf[2]
                arquivoProf.close()
                break
            else:
                print("Código de professor não encontrado")

        while True:
            try:
                valor = input("Valor da aula: ")
                valor = float(valor.replace(",", "."))
                break
            except:
                print("Apenas valor real!")

        while True:
            try:
                limiteAlunos = int(input("Limite de alunos: "))
                break
            except:
                print("Apenas valor inteiro!")

        modalidade = Modalidade(cod, descricao, codProfessor, valor, limiteAlunos, 0)

        arquivo = open("dados/modalidades.txt", "a", encoding="utf-8")
        posicao = arquivo.tell()
        linha = f"{modalidade.cod};{modalidade.descricao};{modalidade.codProfessor};{modalidade.valor};{modalidade.limiteAlunos};{modalidade.totalAlunos}\n"
        arquivo.write(linha)
        arquivo.close()

        arvoreModalidades.inserir(cod, posicao)

        print("Modalidade cadastrada com sucesso!")
        print("Descricao: ",modalidade.descricao)
        print("Professor: ", nomeProfessor)
        print("Cidade do professor: ", cidadeProfessor)
        print(f"Valor da aula: R$ {modalidade.valor:.2f}")
        print("Limite de alunos: ", modalidade.limiteAlunos)
        print("Total de alunos: ", modalidade.totalAlunos)
        break

def buscarModalidade():
    while True:
        try:
            busca = int(input("Digite o codigo da Modalidade: "))
            break
        except:
            print("Apenas valor inteiro!")
            continue


    posicao = arvoreModalidades.buscar(busca)

    if posicao is None:
        print("Modalidade não encontrada no índice!")
        return

    arquivo = open("dados/modalidades.txt", "r", encoding="utf-8")
    arquivo.seek(posicao)
    linha = arquivo.readline()
    itens = linha.strip().split(";")
    modalidade = Modalidade(int(itens[0]), itens[1], int(itens[2]), float(itens[3]), int(itens[4]), int(itens[5]))
    codProfessor = modalidade.codProfessor
    posicaoProfessor = arvoreProfessores.buscar(codProfessor)
    arquivo.close()

    if posicaoProfessor is None:
        nomeProfessor = "Professor não encontrado!"
        nomeCidade = ""
    else:
        arquivo = open("dados/professor.txt", "r", encoding="utf-8")
        arquivo.seek(posicaoProfessor)
        linha = arquivo.readline()
        itens = linha.strip().split(";")
        nomeProfessor = itens[1]
        codCidade = int(itens[4])
        posicaoCidade = arvoreCidades.buscar(codCidade)

        if posicaoCidade is None:
            nomeCidade = "Cidade não encontrada!"
        else:
            arquivo = open("dados/cidades.txt", "r", encoding="utf-8")
            arquivo.seek(posicaoCidade)
            linha = arquivo.readline()
            itens = linha.strip().split(";")
            nomeCidade = itens[1]

    print("Descricão da Modalidade: ", modalidade.descricao)
    print("Professor: ",nomeProfessor)
    print("Cidade do Professor: ", nomeCidade)
    print("Valor da aula: ",modalidade.valor)
    print("Limite de alunos: ",modalidade.limiteAlunos)
    print("Total de alunos: ",modalidade.totalAlunos)
    arquivo.close()
    print("\n\n")

def excluirModalidade():
    try:
        cod = int(input("Digite o código da modalidade para excluir (0 cancela): "))
    except:
        print("Apenas valor inteiro!")
        return

    if cod == 0:
        print("Operação cancelada.")
        return

    if arvoreModalidades.buscar(cod) is None:
        print("Modalidade não encontrada!")
        return

    arquivo = open("dados/modalidades.txt", "r", encoding="utf-8")
    linhas = arquivo.readlines()
    arquivo.close()

    arquivo = open("dados/modalidades.txt", "w", encoding="utf-8")
    arvoreModalidades.raiz = None
    for linha in linhas:
        itens = linha.strip().split(";")
        if int(itens[0]) != cod:
            modalidade = Modalidade(
                int(itens[0]), itens[1], int(itens[2]),
                float(itens[3]), int(itens[4]), int(itens[5])
            )
            posicao = arquivo.tell()
            linha = f"{modalidade.cod};{modalidade.descricao};{modalidade.codProfessor};{modalidade.valor};{modalidade.limiteAlunos};{modalidade.totalAlunos}\n"
            arquivo.write(linha)
            arvoreModalidades.inserir(modalidade.cod, posicao)

    arquivo.close()
    print("Modalidade excluída com sucesso!")

#------------------------MATRÍCULA----------------------------#
def carregarIndiceMatriculas():
    try:
        arquivo = open("dados/matriculas.txt", "r", encoding="utf-8")
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
                arvoreMatriculas.inserir(codigo, posicao)
            except ValueError:
                continue
    except FileNotFoundError:
        open("dados/matriculas.txt", "w", encoding="utf-8").close()


def inserirMatricula():
    while True:
        try:
            cod = int(input("Código da matrícula (0 cancela): "))
        except:
            print("Apenas valor inteiro!")
            continue

        if cod == 0:
            print("Operação cancelada.")
            return

        if arvoreMatriculas.buscar(cod) is not None:
            print("Código de matrícula já existe!")
            continue

        while True:
            try:
                codAluno = int(input("Código do Aluno: "))
            except:
                print("Apenas valor inteiro!")
                continue

            posAluno = arvoreAlunos.buscar(codAluno)
            if posAluno is not None:
                arquivoAluno = open("dados/alunos.txt", "r", encoding="utf-8")
                arquivoAluno.seek(posAluno)
                linha = arquivoAluno.readline().strip().split(";")
                nomeAluno = linha[1]
                cidadeAluno = linha[2]
                arquivoAluno.close()
                break
            else:
                print("Aluno não encontrado.")

        while True:
            try:
                codModalidade = int(input("Código da Modalidade: "))
            except:
                print("Apenas valor inteiro!")
                continue

            posModalidade = arvoreModalidades.buscar(codModalidade)
            if posModalidade is not None:
                arquivoMod = open("dados/modalidades.txt", "r+", encoding="utf-8")
                arquivoMod.seek(posModalidade)
                itens = arquivoMod.readline().strip().split(";")
                descricaoModalidade = itens[1]
                valorDaAula = float(itens[3])
                limiteAlunos = int(itens[4])
                totalAlunos = int(itens[5])

                if totalAlunos >= limiteAlunos:
                    print(f"Limite de {limiteAlunos} alunos atingido.")
                    arquivoMod.close()
                    return

                totalAlunos += 1
                arquivoMod.seek(posModalidade)
                arquivoMod.write(f"{itens[0]};{itens[1]};{itens[2]};{itens[3]};{itens[4]};{totalAlunos}\n")
                arquivoMod.close()
                break
            else:
                print("Modalidade não encontrada.")

        while True:
            try:
                qtdeAulas = int(input("Quantidade de aulas: "))
                break
            except:
                print("Apenas valor inteiro!")

        matricula = Matricula(cod, codAluno, codModalidade, qtdeAulas)
        arquivo = open("dados/matriculas.txt", "a", encoding="utf-8")
        posicao = arquivo.tell()
        linha = f"{matricula.cod};{matricula.codAluno};{matricula.codModalidade};{matricula.qtdeAulas}\n"
        arquivo.write(linha)
        arquivo.close()
        arvoreMatriculas.inserir(matricula.cod, posicao)

        print("\nMatrícula cadastrada com sucesso!")
        print("Aluno: ", nomeAluno)
        print("Cidade do aluno: ", cidadeAluno)
        print("Modalidade: ",descricaoModalidade)
        print("Quantidade de aulas", qtdeAulas)
        print(f"Valor a pagar: R$ {valorDaAula * qtdeAulas:.2f}\n")
        break

def buscarMatricula():
    try:
        busca = int(input("Digite o codigo da Matrícula: "))
    except:
        print("Apenas valor inteiro!")


    posicao = arvoreMatriculas.buscar(busca)
    if posicao is None:
        print("Matrícula não encontrada no índice!")
        return

    arquivo = open("dados/matriculas.txt", "r", encoding="utf-8")
    arquivo.seek(posicao)
    linha = arquivo.readline()
    itens = linha.strip().split(";")
    matricula = Matricula(int(itens[0]), int(itens[1]), int(itens[2]), int(itens[3]))
    arquivo.close()
    codAluno = matricula.codAluno
    codModalidade= matricula.codModalidade

    posicaoAluno = arvoreAlunos.buscar(codAluno)
    if posicaoAluno is None:
        nomeAluno = "Aluno não encontrado"
        codCidade = None
        nomeCidade=""
    else:
        arquivo = open("dados/alunos.txt", "r", encoding="utf-8")
        arquivo.seek(posicaoAluno)
        linha = arquivo.readline()
        itens = linha.strip().split(";")
        nomeAluno = itens[1]
        codCidade = int(itens[2])
        arquivo.close()

    if codCidade is None:
        nomeCidade = ""
    else:
        posicaoCidade = arvoreCidades.buscar(codCidade)
        if posicaoCidade is None:
            nomeCidade = ""
        else:
            arquivo = open("dados/cidades.txt", "r", encoding="utf-8")
            arquivo.seek(posicaoCidade)
            linha = arquivo.readline()
            itens = linha.strip().split(";")
            nomeCidade = itens[1]
            arquivo.close()


    posicaoModalidade = arvoreModalidades.buscar(codModalidade)
    if posicaoModalidade is None:
        descricaoModalidade = "Modalidade não encontrada"
    else:
        arquivo = open("dados/modalidades.txt", "r", encoding="utf-8")
        arquivo.seek(posicaoModalidade)
        linha = arquivo.readline()
        itens = linha.strip().split(";")
        descricaoModalidade = itens[1]
        valorDaAula = float(itens[3])

    print("Nome do Aluno Cadastrado: ", nomeAluno)
    print("Cidade do aluno: ", nomeCidade)
    print("Modalidade: ", descricaoModalidade)
    print("Quantidade de aulas: ", matricula.qtdeAulas)
    print(f"Valor a pagar: R$ {matricula.qtdeAulas * valorDaAula:.2f}")

def excluirMatricula():
    try:
        cod = int(input("Digite o codigo da Matricula (0 cancela): "))
    except:
        print("Apenas valor inteiro!")

    if cod ==0:
        print("Operaço cancelada!")

    posicao = arvoreMatriculas.buscar(cod)
    if posicao is None:
        print("Código de matrícula não encontrado!")
        return

    arquivo = open("dados/matriculas.txt", "r", encoding="utf-8")
    arquivo.seek(posicao)
    linha = arquivo.readline()
    itens = linha.strip().split(";")
    codModalidade = int(itens[2])
    arquivo.close()


    arquivo = open("dados/matriculas.txt", "r", encoding="utf-8")
    linhas = arquivo.readlines()
    arquivo.close()

    arquivo = open("dados/matriculas.txt", "w", encoding="utf-8")
    arvoreMatriculas.raiz = None
    for linha in linhas:
        itens = linha.strip().split(";")
        if int(itens[0]) != cod:
            matricula = Matricula(int(itens[0]), int(itens[1]), int(itens[2]), int(itens[3]))
            posicao = arquivo.tell()
            linha = f"{matricula.cod};{matricula.codAluno};{matricula.codModalidade};{matricula.qtdeAulas}\n"
            arquivo.write(linha)
            arvoreMatriculas.inserir(matricula.cod, posicao)
    arquivo.close()

    arquivo = open("dados/modalidades.txt", "r", encoding="utf-8")
    linhas = arquivo.readlines()
    arquivo.close()

    arquivo = open("dados/modalidades.txt", "w", encoding="utf-8")
    arvoreMatriculas.raiz = None
    for linha in linhas:
        itens = linha.strip().split(";")
        modalidade = Modalidade(int(itens[0]), itens[1], int(itens[2]), float(itens[3]), int(itens[4]), int(itens[5]))
        if modalidade.cod == codModalidade:
            modalidade.totalAlunos = max(0, modalidade.totalAlunos -1)
        posicao = arquivo.tell()
        linha = f"{modalidade.cod};{modalidade.descricao};{modalidade.codProfessor};{modalidade.valor};{modalidade.limiteAlunos};{modalidade.totalAlunos}\n"
        arquivo.write(linha)
        arvoreModalidades.inserir(modalidade.cod, posicao)
    arquivo.close()

    print("Matricula excluida!")

def totalFaturado():
    while True:
        try:
            cod = int(input("Digite o codigo da Modalidade (0 cancela): "))
            break
        except:
            print("Apenas valor inteiro!")
            continue

    if cod == 0:
        print("Operação cancelada!")
        return

    posicao = arvoreModalidades.buscar(cod)
    if posicao is None:
        print("Modalidade não encontrada!")
        return

    arquivo = open("dados/modalidades.txt", "r", encoding="utf-8")
    arquivo.seek(posicao)
    itens = arquivo.readline().strip().split(";")
    arquivo.close()

    modalidade = Modalidade(int(itens[0]), itens[1], int(itens[2]), float(itens[3]), int(itens[4]), int(itens[5]))
    descricao = modalidade.descricao
    codProfessor = modalidade.codProfessor

    nomeProfessor = "Professor não encontrado!"
    cidadeProfessor = ""
    codCidade = None

    if codProfessor is not None:
        posicaoProfessor = arvoreProfessores.buscar(codProfessor)
        if posicaoProfessor is not None:
            arquivo = open("dados/professor.txt", "r", encoding="utf-8")
            arquivo.seek(posicaoProfessor)
            itens = arquivo.readline().strip().split(";")
            arquivo.close()
            nomeProfessor = itens[1]
            codCidade = int(itens[4])

    if codCidade is not None:
        posicaoCidade = arvoreCidades.buscar(codCidade)
        if posicaoCidade is not None:
            arquivo = open("dados/cidades.txt", "r", encoding="utf-8")
            arquivo.seek(posicaoCidade)
            itens = arquivo.readline().strip().split(";")
            arquivo.close()
            cidadeProfessor = itens[1]

    totalAlunos = 0
    valorFaturado = 0
    arquivo = open("dados/matriculas.txt", "r", encoding="utf-8")
    for linha in arquivo:
        itens = linha.strip().split(";")
        codModMatricula = int(itens[2])
        if codModMatricula == cod:
            qtdeAulas = int(itens[3])
            valorFaturado += qtdeAulas * modalidade.valor
            totalAlunos += 1
    arquivo.close()

    print("Modalidade: ", descricao)
    print("Professor: ", nomeProfessor)
    print("Cidade do professor: ", cidadeProfessor)
    print("Total alunos: ", totalAlunos)
    print(f"Valor faturado: R${valorFaturado:.2f}")


#----------------Leitura Exaustiva-----------------------------------#
def leituraExaustiva():
    print("Matrículas")
    print("---------------------------//------------------------")
    totalAlunos = 0
    valorTotal = 0
    matriculas = []

    arquivo = open("dados/matriculas.txt", "r", encoding="utf-8")
    for linha in arquivo:
        itens = linha.strip().split(";")
        matricula = Matricula(int(itens[0]), int(itens[1]), int(itens[2]), int(itens[3]))
        matriculas.append(matricula)
    arquivo.close()

    matriculas.sort(key=lambda matricula: matricula.cod)

    for matricula in matriculas:
        posicaoAluno = arvoreAlunos.buscar(matricula.codAluno)
        if posicaoAluno is None:
            nomeAluno = "Aluno não encontrado"
            codCidade = None
            nomeCidade = ""
        else:
            arquivo = open("dados/alunos.txt", "r", encoding="utf-8")
            arquivo.seek(posicaoAluno)
            linha = arquivo.readline()
            itens = linha.strip().split(";")
            nomeAluno = itens[1]
            codCidade = int(itens[2])
            arquivo.close()

        if codCidade is None:
            nomeCidade = ""
        else:
            posicaoCidade = arvoreCidades.buscar(codCidade)
            if posicaoCidade is None:
                nomeCidade = ""
            else:
                arquivo = open("dados/cidades.txt", "r", encoding="utf-8")
                arquivo.seek(posicaoCidade)
                linha = arquivo.readline()
                itens = linha.strip().split(";")
                nomeCidade = itens[1]
                arquivo.close()

        posicaoModalidade = arvoreModalidades.buscar(matricula.codModalidade)
        if posicaoModalidade is None:
            descricaoModalidade = "Modalidade não encontrada"
            valorAula = 0
            codProfessor = None
        else:
            arquivo = open("dados/modalidades.txt", "r", encoding="utf-8")
            arquivo.seek(posicaoModalidade)
            linha = arquivo.readline()
            itens = linha.strip().split(";")
            descricaoModalidade = itens[1]
            valorAula = float(itens[3])
            codProfessor = int(itens[2])
            arquivo.close()

        if codProfessor is None:
            nomeProfessor = "Professor não encontrado!"
        else:
            posicaoProfessor = arvoreProfessores.buscar(codProfessor)
            if posicaoProfessor is None:
                nomeProfessor = "Professor não encontrado!"
            else:
                arquivo = open("dados/professor.txt", "r", encoding="utf-8")
                arquivo.seek(posicaoProfessor)
                linha = arquivo.readline()
                itens = linha.strip().split(";")
                nomeProfessor = itens[1]
                arquivo.close()

        valorAPagar = matricula.qtdeAulas * valorAula
        totalAlunos += 1
        valorTotal += valorAPagar

        print("Código Matrícula: ", matricula.cod)
        print("Nome aluno: ", nomeAluno)
        print("Cidade: ", nomeCidade)
        print("Modalidade: ", descricaoModalidade)
        print("Professor: ", nomeProfessor)
        print("Quantidade de aulas: ", matricula.qtdeAulas)
        print(f"Valor a pagar: R$ {valorAPagar:.2f}")
        print("---------------------------//------------------------\n")

    print(f"Total de alunos matriculados: {totalAlunos}")
    print(f"Valor total a ser pago pelos alunos: R$ {valorTotal:.2f}\n")




#---------------------------MENU---------------------------------------#
def menu():
    while True:
        print("\n--- MENU ---")
        print("1 - Inserir")
        print("2 - Buscar")
        print("3 - Deletar")
        print("4- Total Faturado")
        print("5- Leitura Exaustiva")
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
            elif (opcao == "3"):
                inserirMatricula()
            elif (opcao == "4"):
                inserirModalidade()
            elif (opcao == "5"):
                inserirProfessor()
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
            elif (opcao == "3"):
                buscarMatricula()
            elif (opcao =="4"):
                buscarModalidade()
            elif (opcao == "5"):
                buscarProfessor()
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
            elif (opcao == "3"):
                excluirMatricula()
            elif (opcao == "4"):
                excluirModalidade()
            elif (opcao == "5"):
                excluirProfessor()
#--------------Valor faturado-------------#
        elif opcao == "4":
            totalFaturado()
#-------------Leitura exaustiva----------#
        elif opcao == "5":
            leituraExaustiva()
#-----------------SAIR---------------------#
        elif opcao == "0":
            print("Programa encerrado!")
            break
        else:
            continue

if not os.path.exists("dados"):
    os.mkdir("dados")

carregarIndiceCidades()
carregarIndiceAlunos()
carregarIndiceProfessor()
carregarIndiceModalidades()
carregarIndiceMatriculas()



#Front

#janela
app = customtkinter.CTk()
app.title("Trabalho Bagos")
customtkinter.set_appearance_mode("dark")
app.geometry("600x500")
app.resizable(width=False, height=False)

#inconify fecha a janela e deiconify reabre

#Menu Principal
label = ctk.CTkLabel(app, text="Menu", fg_color="blue")
label.configure(padx=100, pady=10)
btnins = ctk.CTkButton(app, text="Inserir", command=menu)
btnins.pack()
btnins.configure(width=11, height=1)

app.mainloop()
