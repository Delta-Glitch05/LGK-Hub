def Registro(genere, username):
    print("""Scegli un'opzione: 
    1. Argomenti lezione;
    2. Compiti assegnati;
    3. Voti;
    4. Pagella.""")
    scelta = input("Inserisci il numero della scelta: ")
    scelta = scelta.lower()
    if(scelta == "1" or scelta == "1." or scelta == "argomenti lezione" or scelta == "argomenti"):
        pass
    elif(scelta == "2" or scelta == "2." or scelta == "compiti assegnati" or scelta == "compiti" or scelta == "compito"):
        pass
    elif(scelta == "3" or scelta == "3." or scelta == "voti" or scelta == "voto"):
        pass
    elif(scelta == "4" or scelta == "4." or scelta == "pagella"):
        pass
    else:
        print("Non hai inserito una scelta valida!")
