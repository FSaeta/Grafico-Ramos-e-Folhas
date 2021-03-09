import datetime
import os
import sys

def limpar_tela():
	os.system('cls' if os.name == 'nt' else 'clear')
path_atual = os.getcwd()

limpar_tela()
print('\nBem Vindo ao meu programa! :)')

def valida_numero(num):
	if ',' not in num or len(num) > 3:
		raise TypeError
	int(num[0])
	int(num[2])

def valida_opcao(opcao, menu_id):
	if menu_id in (1,2):
		if opcao not in [0, 1, 2]:
			raise ValueError
	elif menu_id == 3:
		if opcao != 0:
			raise ValueError

def escreve_recovery(nums):
	with open('recovery.txt', 'a') as arquivo:
		arquivo.write(f"\n------------------\n"\
					  f"Data: {datetime.datetime.now().strftime('%d/%m/%Y')}\n"\
					  f"Hora: {datetime.datetime.now().strftime('%Hh-%Mm-%Ss')}\n")
		for num in nums:
			arquivo.write(f"{num}\n")

R = '\033[31m' # vermelho
G = '\033[32m' # verde
Y = '\033[01;33m' # amarelo
C = '\033[36m' # ciano
W = '\033[0m'  # branco

boas_vindas = f"""-----------------------------------------
__ GERADOR DE GRÁFICO RAMOS E FOLHAS __

{Y}[1]{W} Instruções (* Recomendado para primeira vez)
{Y}[2]{W} Criar Novo Gráfico

{R}[0]{W} Sair
-----------------------------------------
"""
menu_criar_graf = f"""-----------------------------------------
>> CRIANDO GRÁFICO

Selecione a forma de inserir os dados:

{Y}[1]{W} Inserir Números Manualmente
{Y}[2]{W} Ler Números de um arquivo .txt

{R}[0]{W} Voltar
-----------------------------------------
"""
menu_instrucoes = """-----------------------------------------
INSTRUÇÕES A SEREM PROGRAMADAS
-----------------------------------------
[0] Voltar
"""
msg_nums_txt = """-----------------------------------------
>> CRIANDO GRÁFICO >> LER ARQUIVO .TXT

- Digite o caminho absoluto do arquivo ou apenas o nome 
dele se estiver na mesma pasta desse programa.

Exemplos:
Windows:  C:\\Users\\Fernando\\arquivo.txt
Linux:    /home/fernando/arquivo.txt
___
"""
menu = {1: boas_vindas, 2: menu_criar_graf, 3: menu_instrucoes}
id_menu = 1

def mostra_menu(menu_id):
	global id_menu, pede
	sair = False
	try:
		print(menu[id_menu])
		opcao = int(input("Digite a opcão: "))
		valida_opcao(opcao, menu_id)

		if menu_id == 1:
			if opcao == 1:
				id_menu = 3
				limpar_tela()
			elif opcao == 2:
				id_menu = 2
				limpar_tela()
			else:
				sair = True

		elif menu_id == 2:
			if opcao in (1, 2):
				pede = False
				return opcao
			elif opcao == 0:
				id_menu = 1
				limpar_tela()

		elif menu_id == 3:
			if opcao == 0:
				id_menu = 1

	except:
		try:
			print(f"Opcão [{opcao}] Inválida !")
		except:
			print("Você deve digitar uma opção válida !")
	if sair:
		sys.exit()

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
def ler_nums_txt(nums):
	path = input("Digite o caminho do arquivo: ")
	with open(path, 'r') as arquivo:
		lines = arquivo.readlines()
		for num in lines:
			try:
				valida_numero(num)
			except TypeError:
				print(f"Elemento <{num}> não foi adicionado devido ao formato dele.")

pede = True
while pede:
	selected = mostra_menu(id_menu)

	if selected == 1:
		pedir_numeros()
	elif selected == 2:
		limpar_tela()
		print(msg_nums_txt)
		try:
			ler_nums_txt(nums)
		except FileNotFoundError as e:
			print(f"\nERRO: Arquivo não foi encontrado no caminho especificado!")
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
		elif len(i) == 2:
			linha = f"{i}|{data[i]}"
		grafico += linha + '\n'
	print(ramos)
	return grafico


graf_data = criar_dict_graf(nums)
print(f"Data : {graf_data}")
grafico = montar_graf(graf_data)
print("\nGRAFICO MONTADO EM PYTHON\nFernando Saeta\n\n")
print(grafico)

