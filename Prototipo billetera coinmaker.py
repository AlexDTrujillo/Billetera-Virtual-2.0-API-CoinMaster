from datetime import datetime
import requests

#Credenciales coinmarket
COINMARKET_API_KEY = "b0c4871a-3c0a-4072-b988-34cff5951ccb"
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': COINMARKET_API_KEY
}

#consultar valor de la criptomoneda definida
def valorCripto(symbol):
    parametros = {"symbol": symbol}#estructura de precioUSD que va a devolver el servidor
    valor=requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest",headers=headers,params=parametros).json()
    return valor["data"][symbol]["quote"]["USD"]["price"]

#verificacion de criptomoneda a usar
def esCriptomoneda(symbol): 
    criptos = ["BTC","BCC","LTC","ETH","ETC","XRP"]
    if symbol in criptos:
        return True
    else:
        return False


estado1="Realizada"
estado2="Rechazada"
symbol=""
seleccionMenu=""
estadoTranferencia=""
contenidoBilletera={"BTC":1,"BCC":1,"LTC":0,"ETH":0,"ETC":0,"XRP":0}
cantCriptoEnviar=0
cantCriptoRecivir=0
cantCriptofondear=0
totalDolares=0
historiaSalida=[]
historiaEntrada=[]
historiaFondeo=[]

#inicio solicitando codigo
codigoPropietario=input("para iniciar, por favor ingrese su codigo de usuario: ")
#Cuerpo del programa (continuo hasta que se elija el 7)
while not seleccionMenu=="7":
    seleccionMenu=input("\nElija una opcion, marcando un numero del siguiente Menu: \n1-Recibir Transferencia \n2-Hacer Tranferencia  \n3-Conoce tu balance de una criptomoneda \n4-Balance general \n5-historial de transacciones \n6-Agregar fondos a tu billetera \n7-salir del programa \n")

    #Recibir Cripto
    if seleccionMenu=="1":
        codigoRemitente=input("Codigo de quien envia las criptomonedas: ")
        if codigoRemitente!=codigoPropietario:
            while not esCriptomoneda(symbol):
                symbol= input("¿criptomoneda a recibir?,\npor favor usar las siguientes abreviaciones BTC, BCC,LTC,ETH,ETC,XRP: ")
            cantCriptoRecivir=float(input("Cantidad de la criptomoneda a recibir: "))
            contenidoBilletera[symbol] = contenidoBilletera[symbol] + cantCriptoRecivir
            estadoTranferencia=estado1
            ahora= datetime.now (tz = None)
            fecha=ahora.strftime("%A, %d de %B de %Y a las %I:%M:%S%p")
        historiaEntrada.append([codigoRemitente,symbol,cantCriptoRecivir,estadoTranferencia,fecha])
        symbol=False

    #Enviar symbol
    if seleccionMenu=="2":
        codigoDestinatario=input("Codigo de quien recibe las criptomonedas: ")
        if codigoDestinatario!=codigoPropietario:
            while not esCriptomoneda(symbol):
                symbol = input("¿criptomoneda a Enviar?,\npor favor usar las siguientes abreviaciones BTC, BCC,LTC,ETH,ETC,XRP: ")
            cantCriptoEnviar=float(input("Cantidad de la criptomoneda a Enviar: "))
            if  cantCriptoEnviar>contenidoBilletera[symbol]:
                print("Error: No cuentas con fondos suficientes para esta transferencia\n")
                estadoTranferencia=estado2
            else:
                contenidoBilletera[symbol] = contenidoBilletera[symbol] - cantCriptoEnviar
                estadoTranferencia=estado1
            ahora= datetime.now (tz = None)
            fecha=ahora.strftime("%A, %d de %B de %Y a las %I:%M:%S%p")
            historiaSalida.append([codigoDestinatario,symbol,cantCriptoEnviar,estadoTranferencia,fecha])
            symbol=False

    #Balance una Moneda
    if seleccionMenu=="3":
        while not esCriptomoneda(symbol):
            symbol = input("¿Criptomoneda a ver en tu Balance?,\npor favor usar las siguientes abreviaciones (BTC, BCC,LTC,ETH,ETC,XRP: ")
        precioUSD = valorCripto(symbol)
        print("Actualmente tienes ",contenidoBilletera[symbol], symbol,"\n")
        print("El Valor en dolares de",symbol,"es",precioUSD,"\n")
        cambio=float (precioUSD)
        valorDolares=contenidoBilletera[symbol]*cambio
        print("Tus ",symbol," te representan un saldo de ", valorDolares,"dolares\n")

    #Balance General
    if seleccionMenu=="4":
        print("Actualmente tienes en tu billetera: \n",contenidoBilletera)
        for symbol in contenidoBilletera:
            precioUSD = valorCripto(symbol)
            print("El Valor en dolares de",symbol,"es",precioUSD)
            cambio=float (precioUSD)
            valorDolares=contenidoBilletera[symbol]*cambio
            totalDolares=totalDolares+ valorDolares        
        print("Tus criptomonedas te representan un saldo total de ", totalDolares,"dolares\n")

    #Historial de transacciones
    if seleccionMenu=="5":
        print("Has Hecho las siguientes tranferencias de salida desde tu billetera: ")
        for salidas in historiaSalida:
            print(salidas)
        print("Has recibido las siguientes tranferencias a tu billetera: ")
        for entradas in historiaEntrada:
            print(entradas)
        print("Has realizado los siguientes depositos de tu parte a tu billetera: ")
        for fondos in historiaFondeo:
            print(fondos)
    
    #agregar fondos
    if  seleccionMenu=="6":
        while not esCriptomoneda(symbol):
            symbol = input("¿criptomoneda a agregar fondos?,\npor favor usar las siguientes abreviaciones BTC, BCC,LTC,ETH,ETC,XRP: ")
        cantCriptoFondear=float(input("Cantidad de la criptomoneda para agregar a tu billetera: "))
        contenidoBilletera[symbol] = contenidoBilletera[symbol] + cantCriptoFondear
        estadoTranferencia=estado1
        ahora= datetime.now (tz = None)
        fecha=ahora.strftime("%A, %d de %B de %Y a las %I:%M:%S%p")
        historiaFondeo.append(["Fondos Agregados",symbol,cantCriptoFondear,estadoTranferencia,fecha])
        symbol=False

    #Salida del programa
    if seleccionMenu=="7":
        exit()