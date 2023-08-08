import telepot


def readtoke(texto):
    f = open(texto, "r")
    texto = f.readline()
    print(texto)
    tokenizetext = texto.split()
    return tokenizetext[1]


def sendtxt(token, id, texto):
    bot = telepot.Bot(token)
    bot.sendMessage(id, texto)


urlToken = "E:\\resposGit\\FlaskAPIRaptor\\RaptorAlertBot\\teletoken.txt"
mensaje = "rapaz sector 45"
token = readtoke(urlToken)
miId = 6382769746
sendtxt(token, miId, mensaje)
