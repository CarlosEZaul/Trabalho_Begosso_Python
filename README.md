Documentação
https://customtkinter.tomschimansky.com/documentation/

Prototipo das telas (so pra organizar mais ou mneos como vai ser)
https://www.figma.com/design/L4DcA4jd65WRfwjTvDpnpK/Prototipo_telas_begs?node-id=0-1&t=StZ1Uo94dw049BFu-1


erro 
variavel tipo errado leitura exaustiva matricula

Adicionar viadagens
botão de limpar
icone 
logo
botao voltar pagina





ref_arq = open("pessoas.txt","r") 
for linha in ref_arq: 
itens = linha.split() 
print("Nome:", itens[0], itens[1]) 
print("Endereço: ", itens[2], itens[3], itens[4]) 
print("Documento de Identidade: ", itens[5]) 
print("Data de Nascimento: ", itens[6]) 
print("\n\n") ref_arq.close() 


