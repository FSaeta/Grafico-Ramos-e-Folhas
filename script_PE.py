import datetime
import os
import sys
from menu import Menu

import pdb


def limpar_tela():
	os.system('cls' if os.name == 'nt' else 'clear')
path_atual = os.getcwd()

limpar_tela()
print('\nBem Vindo ao meu programa! :)')

def valida_numero(num):
	spl_num = num.split(',')
	if ',' not in num or len(spl_num) > 2 or len(spl_num[1]) != 1:
		raise TypeError
	int(spl_num[0])
	int(spl_num[1])

def valida_opcao(opcao, menu_id):
	menu = menus[menu_id]
	op_permitidas = list(menu.opcoes.keys())
	if opcao not in op_permitidas:
		raise ValueError

def escreve_recovery(nums):
	with open('recovery.txt', 'a') as arquivo:
		arquivo.write(f"\n------------------\n"\
					  f"Data: {datetime.datetime.now().strftime('%d/%m/%Y')}\n"\
					  f"Hora: {datetime.datetime.now().strftime('%Hh-%Mm-%Ss')}\n")
		for num in nums:
			arquivo.write(f"{num}\n")

R = '\033[31m' # vermelho
G = '\033[01;32m' # verde
Y = '\033[01;33m' # amarelo
C = '\033[36m' # ciano
W = '\033[0m'  # branco

boas_vindas = f"""-----------------------------------------
__ GERADOR DE GRÁFICO RAMOS E FOLHAS __

{Y}[1]{W} Instruções (* Recomendado para primeira vez)
{Y}[2]{W} Criar Novo Gráfico

{Y}[0]{W} Sair
-----------------------------------------
"""
menu_criar_graf = f"""-----------------------------------------
>> {G}CRIANDO GRÁFICO{W}

Selecione a forma de inserir os dados:

{Y}[1]{W} Inserir Números Manualmente
{Y}[2]{W} Ler Números de um arquivo .txt

{Y}[0]{W} Voltar
-----------------------------------------
"""
menu_instrucoes = f"""-----------------------------------------
INSTRUÇÕES A SEREM PROGRAMADAS
-----------------------------------------
{Y}[0]{W} Voltar
"""
msg_nums_txt = f"""-----------------------------------------
>> {G}CRIANDO GRÁFICO{W} >> {G}LER ARQUIVO .TXT{W}

- Digite o caminho absoluto do arquivo ou apenas o nome 
dele se estiver na mesma pasta desse programa.

Exemplos:
Windows:  C:\\Users\\Fernando\\arquivo.txt
Linux:    /home/fernando/arquivo.txt
___
"""
def mudar_id(novo_id):
	global id_menu
	id_menu = novo_id
	return id_menu

def muda_pede():
	global pede
	pede = not pede

menus = {1: Menu(nome="Menu Inicial", id=1,
				 msg=boas_vindas,
				 op_dict={0:((sys.exit,[]),), 1:((mudar_id,[3]),), 2:((mudar_id,[2]),)}
				 ),
		 2: Menu(nome="Menu Criando Grafico", id=2,
				 msg=menu_criar_graf, 
				 op_dict={0: ((mudar_id,[1]),), 1: ((muda_pede,[]),), 2: ((muda_pede,[]),)}
				 ), 
		 3: Menu(nome="Menu Instuções", id=3, 
		 		 msg=menu_instrucoes, 
		 		 op_dict={0: ((mudar_id,[1]),)}
		 		 )}

id_menu = 1

def mostra_menu(menu_id):
	# pdb.set_trace()
	global id_menu, pede
	menu = menus[id_menu]
	try:
		print(menu.msg)
		opcao = int(input("Digite a opcão: "))
		valida_opcao(opcao, menu_id)
		ret = menu.exec_funcs(opcao)
		#if 'mudar_id' in ret.keys():
		#	id_menu = ret['mudar_id']

		limpar_tela()
		return opcao

	except SystemExit:
		sys.exit()
	except Exception:
		try:
			print(f"Opcão [{opcao}] Inválida !")
		except:
			print("Você deve digitar uma opção válida !")

nums = []
def pedir_numeros():
	pede_num = True
	while pede_num:
		try:
			numero = str(input("Numero: "))
			valida_numero(numero)
			nums.append(numero)
		except KeyboardInterrupt:
			confirmar = input("Deseja finalizar? S/N: ")
			confirmar = confirmar.upper()
			if confirmar == 'S':
				pede_num = False
				escreve_recovery(nums)
			if confirmar == 'N':
				pede = True
		except Exception:
			print("! X ! X ! X ! X ! X ! X !\nParece que você cometeu algum Erro!\n! X ! X ! X ! X ! X ! X !")

def ler_nums_txt():
	path = input("Digite o caminho do arquivo: ")
	with open(path, 'r') as arquivo:
		lines = arquivo.readlines()
		for num in lines:
			num = num.replace('\n', '')
			try:
				valida_numero(num)
			except (TypeError, ValueError) as e:
				print(f"Elemento <{num}> não foi adicionado devido ao formato dele.")
pede = True
while pede:
	id_anterior = id_menu
	selected = mostra_menu(id_anterior)

	if id_anterior == 2 and id_menu == 2:
		if selected == 1:
			pedir_numeros()
		elif selected == 2:
			limpar_tela()
			print(msg_nums_txt)
			try:
				ler_nums_txt()
			except FileNotFoundError as e:
				print(f"\n{R}ERRO: Arquivo não foi encontrado no caminho especificado!{W}")
				pede = True
				id_menu = 2


def criar_dict_graf(numeros):
	dict_graf = {}
	for n in numeros:
		num_split = n.split(',')
		try:
			data = {num_split[0]: dict_graf[num_split[0]] + num_split[1]}
		except KeyError:
			data = {num_split[0]: num_split[1]}
		dict_graf.update(data)
	return dict_graf

def montar_graf(data):
	grafico = ""

	for r, f in data.items():
		mod_data_r = list(data[r])
		mod_data_r.sort()
		msg = ''
		for n in mod_data_r:
			msg += n+' '
		data[r] = msg

	ramos = list(data.keys())
	ramos.sort()
	aux = []	

	for i in ramos:
		if len(i) == 2:
			if i[0] != ' ':
				aux.append(i)
	aux.sort()
	for i in aux:
		ramos.remove(i)
	aux.sort()
	for i in aux:
		ramos.append(i)
	for i in ramos:
		if len(i) == 1:
			linha = f" {i}|{data[i]}"
		else:
			linha = f"{i}|{data[i]}"
		grafico += linha + '\n'
	return grafico


graf_data = criar_dict_graf(nums)
print(f"Data : {graf_data}")
grafico = montar_graf(graf_data)
print("\nGRAFICO MONTADO EM PYTHON\nFernando Saeta\n\n")
print(grafico)

