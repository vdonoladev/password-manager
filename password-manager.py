import sqlite3
from hashlib import sha256

# Enter your password here.
# Attention this password, in addition to giving access to the database, will be the encryption key of the same database.
# Changing this password, all information in the database will not be correct, only if the original password is restored in this field
# you will have the original information.

ADMIN_PASSWORD = "verystrongpassword"

connect = input("Enter the administrative password:\n")

while connect != ADMIN_PASSWORD:
    print('Incorrect password!\nTry again.')
    connect = input("Enter the administrative password:\n")
    if connect == "q":
        break

conn = sqlite3.connect('password_generator.db')


def create_password(pass_key, service, admin_pass):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8') + pass_key.encode('utf-8')).hexdigest()[:15]


def get_hex_key(admin_pass, service):
    return sha256(admin_pass.encode('utf-8') + service.lower().encode('utf-8')).hexdigest()


def get_password(admin_pass, service):
    secret_key = get_hex_key(admin_pass, service)
    cursor = conn.execute(
        "SELECT * from KEYS WHERE PASS_KEY=" + '"' + secret_key + '"')

    file_string = ""
    for row in cursor:
        file_string = row[0]
    return create_password(file_string, service, admin_pass)


def add_password(service, admin_pass):
    secret_key = get_hex_key(admin_pass, service)

    command = 'INSERT INTO KEYS (PASS_KEY) VALUES (%s);' % (
        '"' + secret_key + '"')
    conn.execute(command)
    conn.commit()
    return create_password(secret_key, service, admin_pass)


if connect == ADMIN_PASSWORD:
    try:
        conn.execute('''CREATE TABLE KEYS
            (PASS_KEY TEXT PRIMARY KEY NOT NULL);''')
        print("Your database has been created!\nWhat password would you like to keep now?")
    except:
        print("You already have a database, what would you like to do?")

    while True:
        print("\n" + "*"*15)
        print("Commands:")
        print("e = Exit the program")
        print("v = View password")
        print("c = Create a password")
        print("*"*15)
        input_ = input(":")

        if input_ == "e":
            break
        if input_ == "c":
            service = input(
                "Which service or website will this password be for?\n")
            print("\n" + service.capitalize() + " password created:\n" +
                  add_password(service, ADMIN_PASSWORD))
        if input_ == "v":
            service = input("What is the name of the site/service?\n")
            print("\n" + service.capitalize() + " password:\n" +
                  get_password(ADMIN_PASSWORD, service))
