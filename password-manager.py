import sqlite3
from hashlib import sha256

ADMIN_PASSWORD = "senhamuitoforte"

connect = input("Digite a senha administrativa:\n")

while connect != ADMIN_PASSWORD:
    print ('Senha incorreta!\nTente outra vez.')
    connect = input("Digite a senha administrativa:\n")
    if connect == "q":
        break

conn = sqlite3.connect('gerenciador_senhas.db')

def create_password(pass_key, service, admin_pass):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8') + pass_key.encode('utf-8')).hexdigest()[:15]

def get_hex_key(admin_pass, service):
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
            (PASS_KEY TEXT PRIMARY KEY NOT NULL);''')
        print("Sua base de dados foi criada!\nQual senha você gostaria de guardar agora?")
    except:
        print("Voce já tem uma base de dados, o que você gostaria de fazer?")
    
    
    while True:
        print("\n"+ "*"*15)
        print("Comandos:")
        print("s = Sair do programa")
        print("v = Ver senha")
        print("c = Criar uma senha")
        print("*"*15)
        input_ = input(":")

        if input_ == "s":
            break
        if input_ == "c":
            service = input("Essa senha vai ser para qual servico ou site?\n")
            print("\n" + service.capitalize() + " senha criada:\n" + add_password(service, ADMIN_PASSWORD))
        if input_ == "v":
            service = input("Qual o nome do site/servico?\n")
            print("\n" + service.capitalize() + " senha:\n"+get_password(ADMIN_PASSWORD, service))
