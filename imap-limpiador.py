# -*- coding: utf-8 -*-
import imaplib, re

# you want to connect to a server; specify which server
server= imaplib.IMAP4_SSL('imap.googlemail.com')
# after connecting, tell the server who you are
server.login('email@dominio.com', 'password')
# this will show you a list of available folders
# possibly your Inbox is called INBOX, but check the list of mailboxes
code, mailboxen= server.list()
# print mailboxen
# if it's called INBOX, then…
server.select("Rebotes")
r, data = server.search(None, "ALL")
lista = ""
mails=0
for num in data[0].split():
    mails += 1
    try:
        rs, mensaje = server.fetch(num, "(RFC822)")
    except:
        print "fuck... " + str(num)
        continue
    email =  mensaje[0][1]
    match = re.search("Failed-Recipients: .*?\r", email, re.MULTILINE|re.DOTALL)

    #Si hay match, es decir, si hay failed recipients
    if(match is not None):
        match = match.group(0).replace("Failed-Recipients: ", "").strip()
        #print match

        #Si no es un mail repetido, lo agregamos. 
        if(lista.find(match) == -1):
            lista += match + "\n"
        # Cada 50 mails, escribimos en el archivo y seguimos tranquilitos
        # <MoP> Supongo que esto lo haces para ir guardando eventualmente la informacion
        if(mails % 50 == 0): # esto funciona cuando tengas 39 mails por ejemplo?
            # <MoP> cuando abres el archivo, truncas el contenido y escribes de nuevo todo
            # <MoP> sabes lo que implica algo asi? imagina un archivo gigante de varios megas, matas la memoria del server
            # <MoP> y no se diga si es una app web
            # <MoP> podrias usar el "a" en lugar de "w" para solo ir agregando la informacion
            f = open("errores.txt", "w")
            # <MoP> si lista no se elimina, vas guardando toda la informacion en memoria
            f.write(lista)
            f.close()
            print str(mails) + " procesados [" + str(num) + "]"
# <MoP> sugiero que al final del ciclo, vuelvas a agregar la informacion de la lista
# <MoP> creo que cuando tu condicion de arriba no se cumpla, no vas a estar guardando la informacion
