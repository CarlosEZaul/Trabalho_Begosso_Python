ref_arq = open("pessoas.txt","r") 
for linha in ref_arq: 
itens = linha.split() 
print("Nome:", itens[0], itens[1]) 
print("Endereço: ", itens[2], itens[3], itens[4]) 
print("Documento de Identidade: ", itens[5]) 
print("Data de Nascimento: ", itens[6]) 
print("\n\n") ref_arq.close() 


pessoas.txt
Jose Santos Rua Alvarenga    311    232345-8    12/04/1973 
Carlos Dias Avenida Ipiranga 712-apto34    213453456-9    14/08/2000 
Ricardo Amaral Rua Andradas 356-casa7     894748-32    15.08.1934 
Maria Silva Av. Paulista 123-cj54   777888999-00    12/12/1912 
Casemiro Abreu Alameda Nothman 657        01203404-7    08/11/1984 
Antonio Alvarenga    Rua Servilio    65   43434343-43     09.08.2016 
