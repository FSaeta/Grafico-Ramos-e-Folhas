class Menu:
	def __init__(self, nome, id, msg, op_dict):
		self.nome = nome
		self.msg = msg
		self.opcoes = op_dict
		self.funcoes_params = self.get_funcoes_params()

	def get_funcoes_params(self):
		funcoes_parametros = {}
		for opcao in self.opcoes.keys():
			funcs_params = []
			for funcao_params in self.opcoes[opcao]:
				funcs_params.append(funcao_params)

			funcoes_parametros.update({opcao:funcs_params})
		return funcoes_parametros

	def exec_funcs(self, opcao):
		ret = {}
		for funcao, params in self.funcoes_params[opcao]:
			if len(params) != 0:
				ret_f = funcao(*params)
			else:
				ret_f = funcao()
			ret.update({funcao.__name__: ret_f})
		return ret
