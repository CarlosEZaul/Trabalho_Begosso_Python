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

    def encontrarMenor(self, atual):
        if atual is None:
            return None
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def emOrdem(self, atual, lista):
        if atual is None:
            self.emOrdem(atual.esquerda, lista)
            lista.append(atual.codigo)
            self.emOrdem(atual.direita, lista)

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
    def __init__(self, cod, nome, codCidade,endereco, telefone):
        self.cod = cod
        self.nome = nome
        self.codCidade = codCidade
        self.endereco = endereco
        self.telefone = telefone
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

#-----------------CIDADES----------------------------#
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

def inserirCidade(cod, descCi, estado,  output=None):
    try:

        if arvoreCidades.buscar(cod) is not None:
            msg = f"Código de cidade {cod} já existe!"
            if output:
                output.insert("end", msg + "\n")
            else:
                print(msg)
            return False



        cidade = Cidade(cod, descCi, estado)


        linha = f"{cidade.cod};{cidade.descricao};{cidade.estado}\n"


        with open("dados/cidades.txt", "a", encoding="utf-8") as arquivo:
            posicao = arquivo.tell()
            arquivo.write(linha)
            arvoreCidades.inserir(cod, posicao)

        msg = (
            f"Cidade {descCi} salva com sucesso!\n"
        )

        if output:
            output.insert("end", msg + "\n\n")
        else:
            print(msg)

        return True

    except Exception as e:
        msg = f"Erro ao inserir cidade: {e}"
        if output:
            output.insert("end", msg + "\n")
        else:
            print(msg)
        return False

def buscarCidade(cod, output=None):
    try:
        with open("dados/cidades.txt", "r", encoding="utf-8") as arq:
            for linha in arq:
                partes = linha.strip().split(";")
                if int(partes[0]) == cod:
                    descricao = partes[1]
                    estado = partes[2]

                    msg = f"Cidade {descricao} (cód {cod}) - Estado: {estado}"
                    if output:
                        output.insert("end", msg + "\n")
                    else:
                        print(msg)
                    return True

        msg = f"Cidade com código {cod} não encontrada."
        if output:
            output.insert("end", msg + "\n")
        else:
            print(msg)
        return False
    except Exception as e:
        msg = f"Erro ao buscar cidade: {e}"
        if output:
            output.insert("end", msg + "\n")
        else:
            print(msg)
        return False

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

def leituraExaustivaCidade():
    if arvoreCidades.raiz is None:
        print("Nenhuma cidade registrada no indice!")
        return

    codigos = []

    arquivo = open("dados/cidades.txt", "r", encoding="utf-8")
    for linha in arquivo:
        linha = linha.strip()
        if not linha:
            continue
        itens = linha.strip().split(";")
        codigos.append(int(itens[0]))
    arquivo.close()

    arvoreCidades.emOrdem(arvoreCidades.raiz, codigos)

    if not codigos:
        print("Nenhuma cidade registrada")
        return

    codigos.sort()

    arquivo = open("dados/cidades.txt", "r", encoding="utf-8")
    print("Leitura Exaustiva da Cidade")
    print("=========================")
    for codigo in codigos:
        posicao = arvoreCidades.buscar(codigo)
        if posicao is not None:
            arquivo.seek(posicao)
            linha = arquivo.readline()
            itens = linha.strip().split(";")
            cidade = Cidade(int(itens[0]), itens[1], itens[2])
            print("Codigo: ", cidade.cod)
            print("Descricao: ", cidade.descricao)
            print("Estado: ", cidade.estado)
            print("=========================")
    arquivo.close()

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

def inserirAluno(cod, nome, codigoCidade, dataNascimento, peso, altura, output=None):
    try:

        if arvoreAlunos.buscar(cod) is not None:
            msg = f"Código de aluno {cod} já existe!"
            if output:
                output.insert("end", msg + "\n")
            else:
                print(msg)
            return False


        if arvoreCidades.buscar(codigoCidade) is None:
            msg = f"Código de cidade {codigoCidade} não encontrado!"
            if output:
                output.insert("end", msg + "\n")
            else:
                print(msg)
            return False


        aluno = Aluno(cod, nome, codigoCidade, dataNascimento, peso, altura)


        linha = f"{aluno.cod};{aluno.nome};{aluno.codCidade};{aluno.dataNascimento};{aluno.peso};{aluno.altura}\n"


        with open("dados/alunos.txt", "a", encoding="utf-8") as arquivo:
            posicao = arquivo.tell()
            arquivo.write(linha)
            arvoreAlunos.inserir(cod, posicao)


        nomeCidade, estado = "Desconhecida", "??"
        with open("dados/cidades.txt", "r", encoding="utf-8") as cidades:
            for linha_cidade in cidades:
                partes = linha_cidade.strip().split(";")
                if len(partes) >= 3 and int(partes[0]) == codigoCidade:
                    nomeCidade, estado = partes[1], partes[2]
                    break


        imc = peso / (altura ** 2)
        if imc < 18.5:
            diagnostico = "Abaixo do peso"
        elif imc < 25:
            diagnostico = "Peso normal"
        elif imc < 30:
            diagnostico = "Sobrepeso"
        else:
            diagnostico = "Obesidade"

        msg = (
            f"Aluno {nome} salvo com sucesso!\n"
            f"IMC: {imc:.2f} ({diagnostico})\n"
            f"Cidade: {nomeCidade} - {estado}"
        )

        if output:
            output.insert("end", msg + "\n\n")
        else:
            print(msg)

        return True

    except Exception as e:
        msg = f"Erro ao inserir aluno: {e}"
        if output:
            output.insert("end", msg + "\n")
        else:
            print(msg)
        return False

def buscarAluno(cod, output=None):
    try:
        with open("dados/alunos.txt", "r", encoding="utf-8") as arq:
            for linha in arq:
                partes = linha.strip().split(";")
                if int(partes[0]) == cod:
                    nome = partes[1]
                    codCidade = int(partes[2])
                    dataNascimento = partes[3]
                    peso = float(partes[4])
                    altura = float(partes[5])

                    imc = peso / (altura ** 2)

                    if imc < 18.5:
                        diag = "Abaixo do peso"
                    elif imc < 25:
                        diag = "Peso normal"
                    elif imc < 30:
                        diag = "Sobrepeso"
                    else:
                        diag = "Obesidade"


                    cidade = "Desconhecida"
                    estado = ""
                    with open("dados/cidades.txt", "r", encoding="utf-8") as arqCid:
                        for linhaCid in arqCid:
                            partesCid = linhaCid.strip().split(";")
                            if int(partesCid[0]) == codCidade:
                                cidade = partesCid[1]
                                estado = partesCid[2]
                                break

                    msg = (
                        f"Aluno {nome} (cód {cod})\n"
                        f"Data de Nascimento: {dataNascimento}\n"
                        f"Peso: {peso:.2f} kg - Altura: {altura:.2f} m\n"
                        f"IMC: {imc:.2f} ({diag})\n"
                        f"Cidade: {cidade}/{estado}\n"
                    )

                    if output:
                        output.insert("end", msg + "\n")
                    else:
                        print(msg)
                    return True

        msg = f"Aluno com código {cod} não encontrado."
        if output:
            output.insert("end", msg + "\n")
        else:
            print(msg)
        return False
    except Exception as e:
        msg = f"Erro ao buscar aluno: {e}"
        if output:
            output.insert("end", msg + "\n")
        else:
            print(msg)
        return False

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

def leituraExaustivaAluno():
    if arvoreAlunos.raiz is None:
        print("Nenhum aluno encontrado no indice")
        return

    codigos = []

    arquivo = open("dados/alunos.txt", "r", encoding="utf-8")

    for linha in arquivo:
        linha = linha.strip()
        if not linha:
            continue
        itens = linha.strip().split(";")
        codigos.append(int(itens[0]))
    arquivo.close()

    arvoreAlunos.emOrdem(arvoreAlunos.raiz, codigos)

    if not codigos:
        print("Nenhum aluno registrado")
        return

    codigos.sort()

    arquivo = open("dados/alunos.txt", "r", encoding="utf-8")
    print("Leitura Exaustiva de Alunos")
    print("=========================")
    for codigo in codigos:
        posicao = arvoreAlunos.buscar(codigo)
        if posicao is not None:
            arquivo.seek(posicao)
            linha = arquivo.readline()
            itens = linha.strip().split(";")
            aluno = Aluno(int(itens[0]), itens[1], int(itens[2]), itens[3], float(itens[4]), float(itens[5]))
            codCidade = aluno.codCidade
            posicaoCidade=  arvoreCidades.buscar(codCidade)
            if posicaoCidade is None:
                nomeCidade = "Cidade não encontrada"
                nomeEstado = ""
            else:
                arquivoCidade = open("dados/cidades.txt", "r", encoding="utf-8")
                arquivoCidade.seek(posicaoCidade)
                linha = arquivoCidade.readline()
                itens = linha.strip().split(";")
                nomeCidade = itens[1]
                nomeEstado = itens[2]
            print("Código: ", aluno.cod)
            print("Nome do aluno: ", aluno.nome)
            print("Cidade: ", nomeCidade)
            print("Nome do Estado: ", nomeEstado)
            print("Data de nascimento: ", aluno.dataNascimento)
            print("Peso: ", aluno.peso)
            print("Altura: ", aluno.altura)
            imc, diagnostico = aluno.imc()
            print(f"IMC: {imc:.2f}")
            print("Diagnostico: ", diagnostico)
            print("==========================\n")

    arquivo.close()
    arquivoCidade.close()

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

def inserirProfessor(cod, nome, codCidade, endereco, telefone, output=None):
    try:

        if arvoreProfessores.buscar(cod) is not None:
            msg = f"Código de professor {cod} já existe!"
            if output:
                output.insert("end", msg + "\n")
            else:
                print(msg)
            return False


        if arvoreCidades.buscar(codCidade) is None:
            msg = f"Código de cidade {codCidade} não encontrado!"
            if output:
                output.insert("end", msg + "\n")
            else:
                print(msg)
            return False


        professor = Professor(cod, nome, codCidade, endereco, telefone)


        linha = f"{professor.cod};{professor.nome};{professor.codCidade};{professor.endereco};{professor.telefone}\n"


        with open("dados/professor.txt", "a", encoding="utf-8") as arquivo:
            posicao = arquivo.tell()
            arquivo.write(linha)
            arvoreProfessores.inserir(cod, posicao)

        nomeCidade, estado = "Desconhecida", "??"
        with open("dados/cidades.txt", "r", encoding="utf-8") as cidades:
            for linha_cidade in cidades:
                partes = linha_cidade.strip().split(";")
                if len(partes) >= 3 and int(partes[0]) == codCidade:
                    nomeCidade, estado = partes[1], partes[2]
                    break

        msg = ( f"Professor {nome} salvo com sucesso!\n"
                f"Cidade: {nomeCidade} - {estado}")
        if output:
            output.insert("end", msg + "\n")
        else:
            print(msg)

        return True

    except Exception as e:
        msg = f"Erro ao inserir professor: {e}"
        if output:
            output.insert("end", msg + "\n")
        else:
            print(msg)
        return False

def buscarProfessor(cod, output=None):
    try:
        with open("dados/professor.txt", "r", encoding="utf-8") as arq:
            for linha in arq:
                partes = linha.strip().split(";")
                if int(partes[0]) == cod:
                    nome = partes[1]
                    codCidade = int(partes[2])


                    cidade, estado = "Desconhecida", "??"
                    with open("dados/cidades.txt", "r", encoding="utf-8") as arq_cid:
                        for linha_cid in arq_cid:
                            p = linha_cid.strip().split(";")
                            if int(p[0]) == codCidade:
                                cidade, estado = p[1], p[2]
                                break

                    msg = f"Professor {nome} (cód {cod}) - Cidade: {cidade}/{estado}"
                    if output:
                        output.insert("end", msg + "\n")
                    else:
                        print(msg)
                    return True

        msg = f"Professor com código {cod} não encontrado."
        if output:
            output.insert("end", msg + "\n")
        else:
            print(msg)
        return False
    except Exception as e:
        msg = f"Erro ao buscar professor: {e}"
        if output:
            output.insert("end", msg + "\n")
        else:
            print(msg)
        return False

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

def leituraExaustivaProfessor():
    if arvoreProfessores.raiz is None:
        print("Nenhum professor encontrado no indice")
        return

    codigos = []

    arquivo = open("dados/professor.txt", "r", encoding="utf-8")

    for linha in arquivo:
        linha = linha.strip()
        if not linha:
            continue
        itens = linha.strip().split(";")
        codigos.append(int(itens[0]))
    arquivo.close()

    arvoreProfessores.emOrdem(arvoreProfessores.raiz, codigos)

    if not codigos:
        print("Nenhum professor registrado")
        return

    codigos.sort()

    arquivo = open("dados/professor.txt", "r", encoding="utf-8")
    print("Leitura Exaustiva de Alunos")
    print("=========================")
    for codigo in codigos:
        posicao = arvoreProfessores.buscar(codigo)
        if posicao is not None:
            arquivo.seek(posicao)
            linha = arquivo.readline()
            itens = linha.strip().split(";")
            professor = Professor(int(itens[0]), (itens[1]), (itens[2]), (itens[3]), int(itens[4]))
            codCidade = professor.codCidade
            posicaoCidade=  arvoreCidades.buscar(codCidade)
            if posicaoCidade is None:
                nomeCidade = "Cidade não encontrada"
                nomeEstado = ""
            else:
                arquivoCidade = open("dados/cidades.txt", "r", encoding="utf-8")
                arquivoCidade.seek(posicaoCidade)
                linha = arquivoCidade.readline()
                itens = linha.strip().split(";")
                nomeCidade = itens[1]
                nomeEstado = itens[2]
            print("Código: ", professor.cod)
            print("Nome do professor: ", professor.nome)
            print("Cidade: ", nomeCidade)
            print("Nome do Estado: ", nomeEstado)
            print("==========================\n")

    arquivo.close()
    arquivoCidade.close()

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

def inserirModalidade(cod, descricao, codProf, valor, limite, output=None):
    try:

        if arvoreModalidades.buscar(cod) is not None:
            msg = f"Código de modalidade {cod} já existe!"
            if output:
                output.insert("end", msg + "\n")
            else:
                print(msg)
            return False

        if arvoreProfessores.buscar(codProf) is None:
            msg = f"Código de professor {codProf} não encontrado!"
            if output:
                output.insert("end", msg + "\n")
            else:
                print(msg)
            return False


        professor_nome = "Desconhecido"
        professor_codCidade = None
        with open("dados/professor.txt", "r", encoding="utf-8") as arq_prof:
            for linha_prof in arq_prof:
                partes = linha_prof.strip().split(";")
                if len(partes) >= 5 and int(partes[0]) == codProf:
                    professor_nome = partes[1]
                    professor_codCidade = int(partes[2])
                    break


        nomeCidade, estado = "Desconhecida", "??"
        if professor_codCidade is not None:
            with open("dados/cidades.txt", "r", encoding="utf-8") as arq_cidades:
                for linha_cidade in arq_cidades:
                    partes = linha_cidade.strip().split(";")
                    if len(partes) >= 3 and int(partes[0]) == professor_codCidade:
                        nomeCidade, estado = partes[1], partes[2]
                        break


        total_alunos = 0


        linha = f"{cod};{descricao};{codProf};{valor};{limite};{total_alunos}\n"


        with open("dados/modalidades.txt", "a", encoding="utf-8") as arquivo:
            posicao = arquivo.tell()
            arquivo.write(linha)
            arvoreModalidades.inserir(cod, posicao)


        msg = (
            f"Modalidade '{descricao}' salva com sucesso!\n"
            f"Professor: {professor_nome}\n"
            f"Cidade do professor: {nomeCidade} - {estado}\n"
            f"Total de alunos: {total_alunos}"
        )

        if output:
            output.insert("end", msg + "\n\n")
        else:
            print(msg)

        return True

    except Exception as e:
        msg = f"Erro ao inserir modalidade: {e}"
        if output:
            output.insert("end", msg + "\n")
        else:
            print(msg)
        return False

def buscarModalidade(cod, output=None):
    try:
        with open("dados/modalidades.txt", "r", encoding="utf-8") as arq:
            for linha in arq:
                partes = linha.strip().split(";")
                if int(partes[0]) == cod:
                    desc = partes[1]
                    codProf = int(partes[2])
                    valor = float(partes[3])
                    limite = int(partes[4])
                    total = int(partes[5])


                    nomeProf = "Desconhecido"
                    with open("dados/professor.txt", "r", encoding="utf-8") as arq_prof:
                        for linha_prof in arq_prof:
                            p = linha_prof.strip().split(";")
                            if int(p[0]) == codProf:
                                nomeProf = p[1]
                                break

                    msg = (
                        f"Modalidade {desc} (cód {cod})\n"
                        f"Professor: {nomeProf}\n"
                        f"Valor: R$ {valor:.2f}\n"
                        f"Limite: {limite}, Total atual: {total}"
                    )
                    if output:
                        output.insert("end", msg + "\n")
                    else:
                        print(msg)
                    return True

        msg = f"Modalidade com código {cod} não encontrada."
        if output:
            output.insert("end", msg + "\n")
        else:
            print(msg)
        return False
    except Exception as e:
        msg = f"Erro ao buscar modalidade: {e}"
        if output:
            output.insert("end", msg + "\n")
        else:
            print(msg)
        return False

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
            modalidade = Modalidade(int(itens[0]), itens[1], int(itens[2]),float(itens[3]), int(itens[4]), int(itens[5]))
            posicao = arquivo.tell()
            linha = f"{modalidade.cod};{modalidade.descricao};{modalidade.codProfessor};{modalidade.valor};{modalidade.limiteAlunos};{modalidade.totalAlunos}\n"
            arquivo.write(linha)
            arvoreModalidades.inserir(modalidade.cod, posicao)

    arquivo.close()
    print("Modalidade excluída com sucesso!")

def leituraExaustivaModalidade():
    if arvoreProfessores.raiz is None:
        print("Nenhuma Modalidade encontrada no indice")
        return

    codigos = []

    arquivo = open("dados/modalidades.txt", "r", encoding="utf-8")

    for linha in arquivo:
        linha = linha.strip()
        if not linha:
            continue
        itens = linha.strip().split(";")
        codigos.append(int(itens[0]))
    arquivo.close()

    arvoreModalidades.emOrdem(arvoreModalidades.raiz, codigos)

    if not codigos:
        print("Nenhum professor registrado")
        return

    codigos.sort()

    arquivo = open("dados/modalidades.txt", "r", encoding="utf-8")
    print("Leitura Exaustiva de Modalidades")
    print("=========================")
    for codigo in codigos:
        posicao = arvoreModalidades.buscar(codigo)
        if posicao is not None:
            arquivo.seek(posicao)
            linha = arquivo.readline()
            itens = linha.strip().split(";")
            modalidade = Modalidade(int(itens[0]), itens[1], int(itens[2]),float(itens[3]), int(itens[4]), int(itens[5]))
            codProfessor = modalidade.codProfessor
            posicaoProfessor=  arvoreCidades.buscar(codProfessor)
            if posicaoProfessor is None:
                nomeProfessor = "Professor não encontrado!"
            else:
                arquivoProfessor = open("dados/professor.txt", "r", encoding="utf-8")
                arquivoProfessor.seek(posicaoProfessor)
                linha = arquivoProfessor.readline()
                itens = linha.strip().split(";")
                nomeProfessor = itens[1]
            print("Código: ", modalidade.cod)
            print("Descrição da modalidade: ", modalidade.descricao)
            print("Professor da modalidade: ", nomeProfessor)
            print("Valor da aula: ",modalidade.valor)
            print("Limite de alunos: ",modalidade.limiteAlunos)
            print("Total de alunos: ", modalidade.totalAlunos)
            print("==========================\n")

    arquivo.close()
    arquivoProfessor.close()

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

def inserirMatricula(cod, codAluno, codModalidade, qtdaulas, output=None):
    try:

        if arvoreMatriculas.buscar(cod) is not None:
            msg = f"Código de matrícula {cod} já existe!"
            if output:
                output.insert("end", msg + "\n")
            else:
                print(msg)
            return False


        aluno_nome, aluno_codCidade = None, None
        with open("dados/alunos.txt", "r", encoding="utf-8") as arq_alunos:
            for linha_aluno in arq_alunos:
                partes = linha_aluno.strip().split(";")
                if len(partes) >= 6 and int(partes[0]) == int(codAluno):
                    aluno_nome = partes[1]
                    aluno_codCidade = int(partes[2])
                    break
        if aluno_nome is None:
            msg = f"Aluno {codAluno} não encontrado!"
            if output:
                output.insert("end", msg + "\n")
            else:
                print(msg)
            return False


        nomeCidade, estado = "Desconhecida", "??"
        with open("dados/cidades.txt", "r", encoding="utf-8") as arq_cidades:
            for linha_cidade in arq_cidades:
                partes = linha_cidade.strip().split(";")
                if len(partes) >= 3 and int(partes[0]) == aluno_codCidade:
                    nomeCidade, estado = partes[1], partes[2]
                    break


        desc, valor, limite, total_alunos = None, None, None, None
        linhas_modalidade = []
        with open("dados/modalidades.txt", "r", encoding="utf-8") as arq_mod:
            linhas_modalidade = arq_mod.readlines()

        for linha_mod in linhas_modalidade:
            partes = linha_mod.strip().split(";")
            if len(partes) >= 6 and int(partes[0]) == codModalidade:
                desc = partes[1]
                valor = float(partes[3])
                limite = int(partes[4])
                total_alunos = int(partes[5])
                break

        if desc is None:
            msg = f"Modalidade {codModalidade} não encontrada!"
            if output:
                output.insert("end", msg + "\n")
            else:
                print(msg)
            return False


        if total_alunos >= limite:
            msg = f"Modalidade {desc} atingiu o limite de alunos ({limite})!"
            if output:
                output.insert("end", msg + "\n")
            else:
                print(msg)
            return False


        valor_total = valor * float(qtdaulas)


        linha = f"{cod};{codAluno};{codModalidade};{qtdaulas}\n"
        with open("dados/matriculas.txt", "a", encoding="utf-8") as arq_mat:
            posicao = arq_mat.tell()
            arq_mat.write(linha)
            arvoreMatriculas.inserir(cod, posicao)


        with open("dados/modalidades.txt", "w", encoding="utf-8") as arq_mod:
            for linha_mod in linhas_modalidade:
                partes = linha_mod.strip().split(";")
                if int(partes[0]) == codModalidade:
                    partes[5] = str(total_alunos + 1)
                    linha_mod = ";".join(partes) + "\n"
                arq_mod.write(linha_mod)


        msg = (
            f"Matrícula salva com sucesso!\n"
            f"Aluno: {aluno_nome} - {nomeCidade} - {estado}\n"
            f"Modalidade: {desc}\n"
            f"Quantidade de aulas: {qtdaulas}\n"
            f"Valor a pagar: R$ {valor_total:.2f}\n"
            f"Total de alunos na modalidade agora: {total_alunos + 1}"
        )

        if output:
            output.insert("end", msg + "\n\n")
        else:
            print(msg)

        return True

    except Exception as e:
        msg = f"Erro ao inserir matrícula: {e}"
        if output:
            output.insert("end", msg + "\n")
        else:
            print(msg)
        return False

def buscarMatricula(cod, output=None):
    try:
        with open("dados/matriculas.txt", "r", encoding="utf-8") as arq:
            for linha in arq:
                partes = linha.strip().split(";")
                if int(partes[0]) == cod:
                    codAluno = int(partes[1])
                    codModalidade = int(partes[2])
                    qtdaulas = int(partes[3])


                    aluno_nome, cidade, estado = "?", "?", "?"
                    with open("dados/alunos.txt", "r", encoding="utf-8") as arq_al:
                        for l in arq_al:
                            p = l.strip().split(";")
                            if int(p[0]) == codAluno:
                                aluno_nome = p[1]
                                codCidade = int(p[2])
                                # busca cidade
                                with open("dados/cidades.txt", "r", encoding="utf-8") as arq_cid:
                                    for lc in arq_cid:
                                        pc = lc.strip().split(";")
                                        if int(pc[0]) == codCidade:
                                            cidade, estado = pc[1], pc[2]
                                            break
                                break


                    desc, valor = "?", 0
                    with open("dados/modalidades.txt", "r", encoding="utf-8") as arq_mod:
                        for l in arq_mod:
                            p = l.strip().split(";")
                            if int(p[0]) == codModalidade:
                                desc, valor = p[1], float(p[3])
                                break

                    valor_total = valor * qtdaulas
                    msg = (
                        f"Matrícula {cod}\n"
                        f"Aluno: {aluno_nome} - {cidade}/{estado}\n"
                        f"Modalidade: {desc}\n"
                        f"Aulas: {qtdaulas}, Valor a pagar: R$ {valor_total:.2f}"
                    )
                    if output:
                        output.insert("end", msg + "\n")
                    else:
                        print(msg)
                    return True

        msg = f"Matrícula {cod} não encontrada."
        if output:
            output.insert("end", msg + "\n")
        else:
            print(msg)
        return False
    except Exception as e:
        msg = f"Erro ao buscar matrícula: {e}"
        if output:
            output.insert("end", msg + "\n")
        else:
            print(msg)
        return False

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

def leituraExaustivaMatricula():
    if arvoreMatriculas.raiz is None:
        print("Nenhuma matrícula registrada!")
        return

    codigos = []
    arquivoMatriculas = open("dados/matriculas.txt", "r", encoding="utf-8")
    for linha in arquivoMatriculas:
        linha = linha.strip()
        if not linha:
            continue
        itens = linha.split(";")
        codigos.append(int(itens[0]))
    arquivoMatriculas.close()

    arvoreMatriculas.emOrdem(arvoreMatriculas.raiz, codigos)
    if not codigos:
        print("Nenhuma matrícula registrada!")
        return

    codigos.sort()

    arquivoMatriculas = open("dados/matriculas.txt", "r", encoding="utf-8")
    arquivoAlunos = open("dados/alunos.txt", "r", encoding="utf-8")
    arquivoCidades = open("dados/cidades.txt", "r", encoding="utf-8")
    arquivoModalidades = open("dados/modalidades.txt", "r", encoding="utf-8")
    arquivoProfessores = open("dados/professor.txt", "r", encoding="utf-8")

    totalAlunos = 0
    valorTotal = 0

    print("Leitura Exaustiva de Matrículas")
    print("==============================\n")

    for codigo in codigos:
        posMatricula = arvoreMatriculas.buscar(codigo)
        if posMatricula is None:
            continue
        arquivoMatriculas.seek(posMatricula)
        linha = arquivoMatriculas.readline()
        itens = linha.strip().split(";")
        matricula = Matricula(int(itens[0]), int(itens[1]), int(itens[2]), int(itens[3]))

        posAluno = arvoreAlunos.buscar(matricula.codAluno)
        if posAluno is None:
            nomeAluno = "Aluno não encontrado"
            codCidade = None
        else:
            arquivoAlunos.seek(posAluno)
            linha = arquivoAlunos.readline()
            itens = linha.strip().split(";")
            nomeAluno = itens[1]
            codCidade = int(itens[2])

        if codCidade is None:
            nomeCidade = ""
        else:
            posCidade = arvoreCidades.buscar(codCidade)
            if posCidade is None:
                nomeCidade = ""
            else:
                arquivoCidades.seek(posCidade)
                linha = arquivoCidades.readline()
                itens = linha.strip().split(";")
                nomeCidade = itens[1]

        posModalidade = arvoreModalidades.buscar(matricula.codModalidade)
        if posModalidade is None:
            descricaoModalidade = "Modalidade não encontrada"
            valorAula = 0
            codProfessor = None
        else:
            arquivoModalidades.seek(posModalidade)
            linha = arquivoModalidades.readline()
            itens = linha.strip().split(";")
            descricaoModalidade = itens[1]
            valorAula = float(itens[3])
            codProfessor = int(itens[2])

        if codProfessor is None:
            nomeProfessor = "Professor não encontrado!"
        else:
            posProfessor = arvoreProfessores.buscar(codProfessor)
            if posProfessor is None:
                nomeProfessor = "Professor não encontrado!"
            else:
                arquivoProfessores.seek(posProfessor)
                linha = arquivoProfessores.readline()
                itens = linha.strip().split(";")
                nomeProfessor = itens[1]

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

    arquivoMatriculas.close()
    arquivoAlunos.close()
    arquivoCidades.close()
    arquivoModalidades.close()
    arquivoProfessores.close()
#-------------------------TOTAL FATURADO---------------------#
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
app.title("PowerOn - Menu")
customtkinter.set_appearance_mode("dark")
app.geometry("1080x720")
app.resizable(width=False, height=False)
app.iconbitmap("icon_poweron.ico")

#inconify fecha a janela e deiconify reabre

#abas das telas - Inserir

def aba_inserir_alunos(tab):
    # Labels e entradas
    lbl_cod = ctk.CTkLabel(tab, text="Código:")
    lbl_cod.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    ent_cod = ctk.CTkEntry(tab)
    ent_cod.grid(row=0, column=1, padx=10, pady=5)

    lbl_nome = ctk.CTkLabel(tab, text="Nome:")
    lbl_nome.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    ent_nome = ctk.CTkEntry(tab)
    ent_nome.grid(row=1, column=1, padx=10, pady=5)

    lbl_cidade = ctk.CTkLabel(tab, text="Código Cidade:")
    lbl_cidade.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    ent_cidade = ctk.CTkEntry(tab)
    ent_cidade.grid(row=2, column=1, padx=10, pady=5)

    lbl_nasc = ctk.CTkLabel(tab, text="Data Nascimento:")
    lbl_nasc.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    ent_nasc = ctk.CTkEntry(tab)
    ent_nasc.grid(row=3, column=1, padx=10, pady=5)

    lbl_peso = ctk.CTkLabel(tab, text="Peso:")
    lbl_peso.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    ent_peso = ctk.CTkEntry(tab)
    ent_peso.grid(row=4, column=1, padx=10, pady=5)

    lbl_altura = ctk.CTkLabel(tab, text="Altura:")
    lbl_altura.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    ent_altura = ctk.CTkEntry(tab)
    ent_altura.grid(row=5, column=1, padx=10, pady=5)

    # Área de mensagens
    output = ctk.CTkTextbox(tab, height=150, width=400)
    output.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def salvar_aluno():
        try:
            cod = int(ent_cod.get())
            nome = ent_nome.get()
            codCidade = int(ent_cidade.get())
            nasc = ent_nasc.get()
            peso = float(ent_peso.get())
            altura = float(ent_altura.get())

            inserirAluno(cod, nome, codCidade, nasc, peso, altura, output)
        except Exception as e:
            output.insert("end", f"Erro: {e}\n")

    btn_salvar = ctk.CTkButton(tab, text="Salvar Aluno", command=salvar_aluno)
    btn_salvar.grid(row=6, column=0, columnspan=2, pady=10)

def aba_inserir_professores(tab):
    # Labels e entradas
    lbl_cod = ctk.CTkLabel(tab, text="Código:")
    lbl_cod.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    ent_cod = ctk.CTkEntry(tab)
    ent_cod.grid(row=0, column=1, padx=10, pady=5)

    lbl_nome = ctk.CTkLabel(tab, text="Nome:")
    lbl_nome.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    ent_nome = ctk.CTkEntry(tab)
    ent_nome.grid(row=1, column=1, padx=10, pady=5)

    lbl_endereco = ctk.CTkLabel(tab, text="Endereço:")
    lbl_endereco.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    ent_endereco = ctk.CTkEntry(tab)
    ent_endereco.grid(row=2, column=1, padx=10, pady=5)

    lbl_tel = ctk.CTkLabel(tab, text="Telefone:")
    lbl_tel.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    ent_tel = ctk.CTkEntry(tab)
    ent_tel.grid(row=3, column=1, padx=10, pady=5)

    lbl_codCi = ctk.CTkLabel(tab, text="Codigo da cidade:")
    lbl_codCi.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    ent_codCi = ctk.CTkEntry(tab)
    ent_codCi.grid(row=4, column=1, padx=10, pady=5)


    # Área de mensagens
    output = ctk.CTkTextbox(tab, height=150, width=400)
    output.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def salvar_prof():
        try:
            cod = int(ent_cod.get())
            nome = ent_nome.get()
            codCidade = int(ent_codCi.get())
            endereco = ent_endereco.get()
            telefone = float(ent_tel.get())



            inserirProfessor(cod, nome, codCidade, endereco, telefone, output)
        except Exception as e:
            output.insert("end", f"Erro: {e}\n")

    btn_salvar = ctk.CTkButton(tab, text="Salvar Professor", command=salvar_prof)
    btn_salvar.grid(row=6, column=0, columnspan=2, pady=10)

def aba_inserir_modalidade(tab):
    # Labels e entradas
    lbl_cod = ctk.CTkLabel(tab, text="Código:")
    lbl_cod.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    ent_cod = ctk.CTkEntry(tab)
    ent_cod.grid(row=0, column=1, padx=10, pady=5)

    lbl_desc = ctk.CTkLabel(tab, text="Descrição:")
    lbl_desc.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    ent_desc = ctk.CTkEntry(tab)
    ent_desc.grid(row=1, column=1, padx=10, pady=5)

    lbl_codProf = ctk.CTkLabel(tab, text="Código Do Professor:")
    lbl_codProf.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    ent_codProf = ctk.CTkEntry(tab)
    ent_codProf.grid(row=2, column=1, padx=10, pady=5)

    lbl_valor = ctk.CTkLabel(tab, text="Valor:")
    lbl_valor.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    ent_valor = ctk.CTkEntry(tab)
    ent_valor.grid(row=3, column=1, padx=10, pady=5)

    lbl_lima = ctk.CTkLabel(tab, text="Limite de alunos:")
    lbl_lima.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    ent_lima = ctk.CTkEntry(tab)
    ent_lima.grid(row=4, column=1, padx=10, pady=5)


    # Área de mensagens
    output = ctk.CTkTextbox(tab, height=150, width=400)
    output.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def salvar_moda():
        try:
            cod = int(ent_cod.get())
            desc = ent_desc.get()
            codProf = int(ent_codProf.get())
            valor = int(ent_valor.get())
            lima = int(ent_lima.get())



            inserirModalidade(cod, desc, codProf, valor, lima, output)
        except Exception as e:
            output.insert("end", f"Erro: {e}\n")

    btn_salvar = ctk.CTkButton(tab, text="Salvar Modalidade", command=salvar_moda)
    btn_salvar.grid(row=6, column=0, columnspan=2, pady=10)

def aba_inserir_matricula(tab):
    # Labels e entradas
    lbl_cod = ctk.CTkLabel(tab, text="Código:")
    lbl_cod.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    ent_cod = ctk.CTkEntry(tab)
    ent_cod.grid(row=0, column=1, padx=10, pady=5)

    lbl_codAlu = ctk.CTkLabel(tab, text="Código Do Aluno:")
    lbl_codAlu.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    ent_codAlu = ctk.CTkEntry(tab)
    ent_codAlu.grid(row=1, column=1, padx=10, pady=5)

    lbl_codModa = ctk.CTkLabel(tab, text="Código Da Modalidade:")
    lbl_codModa.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    ent_codModa = ctk.CTkEntry(tab)
    ent_codModa.grid(row=2, column=1, padx=10, pady=5)

    lbl_qtdaulas = ctk.CTkLabel(tab, text="Quantidade de Aulas:")
    lbl_qtdaulas.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    ent_qtdaulas = ctk.CTkEntry(tab)
    ent_qtdaulas.grid(row=3, column=1, padx=10, pady=5)


    # Área de mensagens
    output = ctk.CTkTextbox(tab, height=150, width=400)
    output.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def salvar_mat():
        try:
            cod = int(ent_cod.get())
            codAlu = int(ent_codAlu.get())
            codModa = int(ent_codModa.get())
            qtdaulas = ent_qtdaulas.get()

            inserirMatricula(cod, codAlu, codModa, qtdaulas, output)
        except Exception as e:
            output.insert("end", f"Erro: {e}\n")

    btn_salvar = ctk.CTkButton(tab, text="Salvar Matricula", command=salvar_mat)
    btn_salvar.grid(row=6, column=0, columnspan=2, pady=10)

def aba_inserir_cidade(tab):
    # Labels e entradas
    lbl_cod = ctk.CTkLabel(tab, text="Código:")
    lbl_cod.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    ent_cod = ctk.CTkEntry(tab)
    ent_cod.grid(row=0, column=1, padx=10, pady=5)

    lbl_descCi = ctk.CTkLabel(tab, text="Descrição/Nome da Cidade:")
    lbl_descCi.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    ent_descCi = ctk.CTkEntry(tab)
    ent_descCi.grid(row=1, column=1, padx=10, pady=5)

    lbl_estado = ctk.CTkLabel(tab, text="Estado:")
    lbl_estado.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    ent_estado = ctk.CTkEntry(tab)
    ent_estado.grid(row=2, column=1, padx=10, pady=5)


    # Área de mensagens
    output = ctk.CTkTextbox(tab, height=150, width=400)
    output.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def salvar_cid():
        try:
            cod = int(ent_cod.get())
            descCi = ent_descCi.get()
            estado = ent_estado.get()

            inserirCidade(cod, descCi, estado, output)
        except Exception as e:
            output.insert("end", f"Erro: {e}\n")

    btn_salvar = ctk.CTkButton(tab, text="Salvar Cidade", command=salvar_cid)
    btn_salvar.grid(row=6, column=0, columnspan=2, pady=10)

#abas das telas - Buscar

def aba_buscar_alunos(tab):
    lbl_cod = ctk.CTkLabel(tab, text="Código do Aluno:")
    lbl_cod.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    ent_cod = ctk.CTkEntry(tab)
    ent_cod.grid(row=0, column=1, padx=10, pady=5)

    output = ctk.CTkTextbox(tab, height=200, width=400)
    output.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def buscar():
        try:
            cod = int(ent_cod.get())
            output.delete("1.0", "end")
            buscarAluno(cod, output)
        except Exception as e:
            output.insert("end", f"Erro: {e}\n")

    btn = ctk.CTkButton(tab, text="Buscar Aluno", command=buscar)
    btn.grid(row=1, column=0, columnspan=2, pady=10)

def aba_buscar_professores(tab):
    lbl_cod = ctk.CTkLabel(tab, text="Código do Professor:")
    lbl_cod.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    ent_cod = ctk.CTkEntry(tab)
    ent_cod.grid(row=0, column=1, padx=10, pady=5)

    output = ctk.CTkTextbox(tab, height=200, width=400)
    output.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def buscar():
        try:
            cod = int(ent_cod.get())
            output.delete("1.0", "end")
            buscarProfessor(cod, output)
        except Exception as e:
            output.insert("end", f"Erro: {e}\n")

    btn = ctk.CTkButton(tab, text="Buscar Professor", command=buscar)
    btn.grid(row=1, column=0, columnspan=2, pady=10)

def aba_buscar_modalidade(tab):
    lbl_cod = ctk.CTkLabel(tab, text="Código da Modalidade:")
    lbl_cod.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    ent_cod = ctk.CTkEntry(tab)
    ent_cod.grid(row=0, column=1, padx=10, pady=5)

    output = ctk.CTkTextbox(tab, height=200, width=400)
    output.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def buscar():
        try:
            cod = int(ent_cod.get())
            output.delete("1.0", "end")
            buscarModalidade(cod, output)
        except Exception as e:
            output.insert("end", f"Erro: {e}\n")

    btn = ctk.CTkButton(tab, text="Buscar Modalidade", command=buscar)
    btn.grid(row=1, column=0, columnspan=2, pady=10)

def aba_buscar_matricula(tab):
    lbl_cod = ctk.CTkLabel(tab, text="Código da Matrícula:")
    lbl_cod.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    ent_cod = ctk.CTkEntry(tab)
    ent_cod.grid(row=0, column=1, padx=10, pady=5)

    output = ctk.CTkTextbox(tab, height=200, width=400)
    output.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def buscar():
        try:
            cod = int(ent_cod.get())
            output.delete("1.0", "end")
            buscarMatricula(cod, output)
        except Exception as e:
            output.insert("end", f"Erro: {e}\n")

    btn = ctk.CTkButton(tab, text="Buscar Matrícula", command=buscar)
    btn.grid(row=1, column=0, columnspan=2, pady=10)

def aba_buscar_cidade(tab):
    lbl_cod = ctk.CTkLabel(tab, text="Código da Cidade:")
    lbl_cod.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    ent_cod = ctk.CTkEntry(tab)
    ent_cod.grid(row=0, column=1, padx=10, pady=5)

    output = ctk.CTkTextbox(tab, height=200, width=400)
    output.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def buscar():
        try:
            cod = int(ent_cod.get())
            output.delete("1.0", "end")
            buscarCidade(cod, output)
        except Exception as e:
            output.insert("end", f"Erro: {e}\n")

    btn = ctk.CTkButton(tab, text="Buscar Cidade", command=buscar)
    btn.grid(row=1, column=0, columnspan=2, pady=10)


#novas telas

def tela_inserir():
    app.withdraw()
    tela_inserir= ctk.CTkToplevel(app)
    tela_inserir.geometry("1080x720")
    tela_inserir.title("PowerOn - Inserir")
    tela_inserir.resizable(width=False, height=False)
    tela_inserir.iconbitmap("icon_poweron.ico")

    # Restaura a janela principal
    def fechar_tela_inserir():
        tela_inserir.destroy()
        app.deiconify()

    tela_inserir.protocol("WM_DELETE_WINDOW", fechar_tela_inserir)

    #Seleção de quem vai ser/navbar
    tabview = ctk.CTkTabview(tela_inserir, height=1080, width=720, corner_radius=20)
    tabview.pack(fill="both")
    tabview.add("Alunos")
    tabview.add("Professores")
    tabview.add("Matricula")
    tabview.add("Modalidade")
    tabview.add("Cidade")
    tabview.tab("Alunos").grid_columnconfigure(0, weight=1 )
    tabview.tab("Professores").grid_columnconfigure(0, weight=1)
    tabview.tab("Matricula").grid_columnconfigure(0, weight=1)
    tabview.tab("Modalidade").grid_columnconfigure(0, weight=1)
    tabview.tab("Cidade").grid_columnconfigure(0, weight=1)

    aba_inserir_alunos(tabview.tab("Alunos"))
    aba_inserir_professores(tabview.tab("Professores"))
    aba_inserir_modalidade(tabview.tab("Modalidade"))
    aba_inserir_matricula(tabview.tab("Matricula"))
    aba_inserir_cidade(tabview.tab("Cidade"))

def tela_buscar():
    app.withdraw()
    tela_buscar= ctk.CTkToplevel(app)
    tela_buscar.geometry("1080x720")
    tela_buscar.title("PowerOn - Buscar")
    tela_buscar.resizable(width=False, height=False)
    tela_buscar.iconbitmap("icon_poweron.ico")

    # Restaura a janela principal
    def fechar_tela_buscar():
        tela_buscar.destroy()
        app.deiconify()

    tela_buscar.protocol("WM_DELETE_WINDOW", fechar_tela_buscar)

    # Seleção de quem vai ser
    tabview = ctk.CTkTabview(tela_buscar, height=1080, width=720, corner_radius=20)
    tabview.pack(fill="both")
    tabview.add("Alunos")
    tabview.add("Professores")
    tabview.add("Matricula")
    tabview.add("Modalidade")
    tabview.add("Cidade")
    tabview.tab("Alunos").grid_columnconfigure(0, weight=1)
    tabview.tab("Professores").grid_columnconfigure(0, weight=1)
    tabview.tab("Matricula").grid_columnconfigure(0, weight=1)
    tabview.tab("Modalidade").grid_columnconfigure(0, weight=1)
    tabview.tab("Cidade").grid_columnconfigure(0, weight=1)

    aba_buscar_alunos(tabview.tab("Alunos"))
    aba_buscar_professores(tabview.tab("Professores"))
    aba_buscar_modalidade(tabview.tab("Modalidade"))
    aba_buscar_matricula(tabview.tab("Matricula"))
    aba_buscar_cidade(tabview.tab("Cidade"))

def tela_deletar():
    app.withdraw()
    tela_deletar= ctk.CTkToplevel(app)
    tela_deletar.geometry("1080x720")
    tela_deletar.title("PowerOn - Deletar")
    tela_deletar.resizable(width=False, height=False)
    tela_deletar.iconbitmap("icon_poweron.ico")

    # Restaura a janela principal
    def fechar_tela_deletar():
        tela_deletar.destroy()
        app.deiconify()

    tela_deletar.protocol("WM_DELETE_WINDOW", fechar_tela_deletar)

    # Seleção de quem vai ser
    tabview = ctk.CTkTabview(tela_deletar, height=1080, width=720, corner_radius=20)
    tabview.pack(fill="both")
    tabview.add("Alunos")
    tabview.add("Professores")
    tabview.add("Matricula")
    tabview.add("Modalidade")
    tabview.add("Cidade")
    tabview.tab("Alunos").grid_columnconfigure(0, weight=1)
    tabview.tab("Professores").grid_columnconfigure(0, weight=1)
    tabview.tab("Matricula").grid_columnconfigure(0, weight=1)
    tabview.tab("Modalidade").grid_columnconfigure(0, weight=1)
    tabview.tab("Cidade").grid_columnconfigure(0, weight=1)

def tela_totalFaturado():
    app.withdraw()
    tela_totalFaturado= ctk.CTkToplevel(app)
    tela_totalFaturado.geometry("1080x720")
    tela_totalFaturado.title("PowerOn - Total Faturado")
    tela_totalFaturado.resizable(width=False, height=False)
    tela_totalFaturado.iconbitmap("icon_poweron.ico")

    # Restaura a janela principal
    def fechar_tela_totalFaturado():
        tela_totalFaturado.destroy()
        app.deiconify()

    tela_totalFaturado.protocol("WM_DELETE_WINDOW", fechar_tela_totalFaturado)

def tela_leituraExaustiva():
    app.withdraw()
    tela_leituraExaustiva= ctk.CTkToplevel(app)
    tela_leituraExaustiva.geometry("1080x720")
    tela_leituraExaustiva.title("PowerOn - Leitura Exaustiva")
    tela_leituraExaustiva.resizable(width=False, height=False)
    tela_leituraExaustiva.iconbitmap("icon_poweron.ico")

    # Restaura a janela principal
    def fechar_tela_leituraExaustiva():
        tela_leituraExaustiva.destroy()
        app.deiconify()

    tela_leituraExaustiva.protocol("WM_DELETE_WINDOW", fechar_tela_leituraExaustiva)

    # Seleção de quem vai ser
    tabview = ctk.CTkTabview(tela_leituraExaustiva, height=1080, width=720, corner_radius=20)
    tabview.pack(fill="both")
    tabview.add("Alunos")
    tabview.add("Professores")
    tabview.add("Matricula")
    tabview.add("Modalidade")
    tabview.add("Cidade")
    tabview.tab("Alunos").grid_columnconfigure(0, weight=1)
    tabview.tab("Professores").grid_columnconfigure(0, weight=1)
    tabview.tab("Matricula").grid_columnconfigure(0, weight=1)
    tabview.tab("Modalidade").grid_columnconfigure(0, weight=1)
    tabview.tab("Cidade").grid_columnconfigure(0, weight=1)


#Menu Principal
frameteste = ctk.CTkFrame(app, width=540, height=360, corner_radius=30).place(x=310, y=200)
btn_inserir= ctk.CTkButton(master=app, text="Inserir", command=tela_inserir).place(x=400, y=260)
btn_buscar= ctk.CTkButton(master=app, text="Buscar", command=tela_buscar).place(x=600, y=260)
btn_deletar= ctk.CTkButton(master=app, text="Deletar", command=tela_deletar).place(x=400, y=360)
btn_leitura= ctk.CTkButton(master=app, text="Leitura Exaustiva", command=tela_leituraExaustiva).place(x=600, y=360)
btn_fatura= ctk.CTkButton(master=app, text="Total Faturado", command=tela_totalFaturado).place(x=500, y=460)

#rodadpe
rodape = ctk.CTkFrame(app, height=40, fg_color="#2e2e2e")
rodape.pack(side="bottom", fill="x")
label_rodape = ctk.CTkLabel(rodape, text="© 2025 Sistema Academia PowerOn - Arthur M. Rieger e Carlos E. Zaul ", text_color="white")
label_rodape.pack(pady=10)


app.mainloop()



