import json
from cryptography.fernet import Fernet

# Generate a key (do this only once and save it securely)
key = Fernet.generate_key()
with open('secret.key', 'wb') as key_file:
   key_file.write(key)

# Load the key
def load_key():
    with open('secret.key', 'rb') as key_file:
        return key_file.read()

key = load_key()
cipher_suite = Fernet(key)

def encrypt_password(password):
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password.encode()).decode()

def add():
    service = input("Add the service of the password: ")
    username = input("Add a username: ")
    password = input("Add your password: ")
    encrypted_password = encrypt_password(password)
    with open('passwords.json','r') as file:
        data = json.load(file)
    data[service] = {'username': username, 'password': encrypted_password}
    with open('passwords.json', 'w') as file:
        json.dump(data, file, indent=4)
    print("Password added!\n")

def delete():
    service = input("Enter the service you want to delete: ")
    with open('passwords.json','r') as file:
        data = json.load(file)
    if data.get(service):
        del data[service]
        with open('passwords.json', 'w') as file:
            json.dump(data, file, indent=4)
        print("Password deleted!\n")
    else:
        print("No such service\n")

def update():
    service = input("Enter the service you want to update: ")
    with open('passwords.json','r') as file:
        data = json.load(file)
    if data.get(service):
        password = input('Enter new password: ')
        encrypted_password = encrypt_password(password)
        data[service]['password'] = encrypted_password
        with open('passwords.json', 'w') as file:
            json.dump(data, file, indent=4)
        print(f"{service}'s password updated!\n")
    else:
        print("No such service\n")

def view():
    with open('passwords.json','r') as file:
        data = json.load(file)
    for k in data.keys():
        username = data[k]['username']
        password = decrypt_password(data[k]['password'])
        print(f"{k}: username -> {username}, password -> {password}")
    print('\n')

while True:
    print("Welcome to my python password manager!")
    print("Do you want to see, add, delete or update a password?")

    """
    data = {}

    with open('passwords.json', 'w') as file:
        json.dump(data, file, indent=4)
    """
    choice = input()
    if choice.lower() == 'add':
        add()
    elif choice.lower() == 'delete':
        delete()
    elif choice.lower() == 'q':
        print('I am happy you used my app!')
        break
    elif choice.lower() == 'update':
        update()
    else:
        view()
