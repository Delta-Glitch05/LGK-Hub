import registro

def controllo(scelta, username, password):
    username = "username:" + username + "\n"
    password = "password:" + password + "\n"
    autenticato = False
    if(scelta == "docente"):
        file_docenti = open("Users/docenti.txt","r").readlines()
        for linea in file_docenti:
            if(linea == username):
                i = file_docenti.index(linea)
                if(password == file_docenti[i + 1]):
                    autenticato = True
                    break
                else:
                    print("Password errata!")
                    break
            elif(linea != username and linea == file_docenti[-1]):
                print("Username errato!")
                break
                    
    elif(scelta == "studente"):
        file_studenti = open("Users/studenti.txt","r").readlines()
        for linea in file_studenti:
            if(linea == username):
                i = file_studenti.index(linea)
                if(password == file_studenti[i + 1]):
                    autenticato = True
                    break
                else:
                    print("Password errata!")
                    break
            elif(linea != username and linea == file_docenti[-1]):
                print("Username errato!")
                break
    return autenticato

def menù(genere, username, password):
    print("""Scegli un'opzione:
    1. Apri il registro;
    2. Apri compiti;
    3. Apri test.""")
    scelta = input("Inserisci il numero della scelta: ")
    scelta = scelta.lower()
    if(scelta == "1" or scelta == "1." or scelta == "registro"):
        registro.Registro(genere, username)
    elif(scelta == "2" or scelta == "2." or scelta == "compiti" or scelta == "compito"):
        pass
    elif(scelta == "3" or scelta == "3." or scelta == "test"):
        pass
    else:
        print("Non hai inserito una scelta valida!")

while True:
    genere = input("Sei un docente o uno studente? ")
    genere = genere.lower()
    if(genere != "docente" and genere != "studente"):
        print("Non hai inserito una scelta valida!")
    else:
        break;

username = input("Inserisci il tuo username: ")
password = input("Inserisci la tua password: ")
auth = controllo(genere, username, password)
if(auth == True):
    print(f"Ti sei autenticato/a come {username}!")
    menù(genere, username, password)
else:
    print("Riprova più tardi!")
