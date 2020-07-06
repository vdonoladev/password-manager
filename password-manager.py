import sqlite3
from hashlib import sha256

# Entre a sua senha aqui.
# Atenção essa senha, além de dar acesso a base de dados, será a chave de encriptção da mesma base de dados.
# Modificando esta senha, toda a informação na base dados não estará correta, somente se a senha original for restaurada neste campo
# você terá a informação original.

ADMIN_PASSWORD = "senhamuitoforte"

connect = input("Entre com a senha administrativa:\n")

while connect != ADMIN_PASSWORD:
	print('Senha incorreta. \nTente outra vez.')
	connect = input("Entre com a senha administrativa:\n")
	if connect == "q":
		break

conn = sqlite3.connect('gerenciador_senhas.db')

def create_password(pass_key, service, admin_pass):
	return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8')).hexdigest()

def get_password(admin_pass, service):
	secret_key = get_hex_key(admin_pass, service)
	cursor = conn.execute("SELECT * from KEYS WHERE PASS_KEY=" + '"' + secret_key + '"')

	file_string = ""
	for row in cursor:
		file_string = row[0]
	return create_password(file_string, service, admin_pass)

def add_password(service, admin_pass):
	secret_key = get_hex_key(admin_pass, service)

	command = 'INSERT INTO KEYS (PASS_KEY) VALUES (%s);' %('"' + secret_key +'"')
	conn.execute(command)
	conn.commit()
	return create_password(secret_key, service, admin_pass)

if connect == ADMIN_PASSWORD:
	try:
		conn.execute('''CREATE TABLE KEYS
			(PASS_KEY TEXT PRIMARY KEY NOT NULL); ''')
		print("Sua base de dados foi criada!\nQual senha você gostaria de guardar agora? ")
	except:
		print("Você já tem uma base de dados, o que você gostaria de fazer? ")


	while True:
		print("\n"+ "*"*15)
		print("Comandos: ")
		print("s = Sair do programa")
		print("v = Ver senha")
		print("c = Criar uma senha")
		print("*"*15)
		input = input(":")

		if input == "s":
			break
		if input == "c":
			service = input("Essa senha vai ser para qual serviço ou website?\n")
			print("\n" + service.capitalize() + " Senha criada:\n" + add_password(service, ADMIN_PASSWORD))
		if input == "v":
			service = input("Qual o nome do website/serviço?\n")
			print("\n" + service.capitalize() + " Senha:\n"+get_password(ADMIN_PASSWORD, service))
