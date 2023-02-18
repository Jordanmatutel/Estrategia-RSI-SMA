#Este codigo fue hecho con el fin de hacer pruebas de programacion.
#El codigo no es necesariamente lucrativo.
#El error que se presenta se puede arreglar añadiendo tu API al codigo
#El creador del codigo no se hace responsable por las consecuencias que este codigo pueda traer
#Este codigo necesita un capital inicial de 100 dolares y re invierte la ganancia


import ccxt
import numpy as np


#Se crea la variable Ciclo para que se actualice continuamente
#Mientras querramos que el codigo se ejecute
Ciclo = True

while Ciclo:

    # Definir las longitudes para el RSI y el SMA
    rsiLargo = 289
    smaLargo = 369

    # Crear una conexión con el exchange
    exchange = ccxt.binance()

    # Datos de precios
    prices = exchange.fetch_ohlcv('BTC/USDT', '1m')
    closes = [price[4] for price in prices]

    #Calcular el SMA

    def calculate_sma(closes, smaLargo):
        sma = []
        for i in range(len(closes) - smaLargo + 1):
            sma.append(sum(closes[i:i + smaLargo]) / smaLargo)
        return sma


    sma = calculate_sma(closes, smaLargo)

    # Cálculo del RSI
    deltas = np.diff(closes)
    gain = [delta if delta > 0 else 0 for delta in deltas]
    Loss = [-delta if delta < 0 else 0 for delta in deltas]
    gain = np.array(gain)
    Loss = np.array(Loss)
    avg_gain = gain.mean()
    avg_loss = Loss.mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))


    # Establecer las claves de API
    exchange.apiKey = 'API_KEY'
    exchange.secret = 'API_SECRET'


    # Inversion inicial y cantidad de compra
    mercado = "BTC/USDT"
    cantidad_dolares = 100
    precio_actual = exchange.fetch_ticker(mercado)['last']
    cantidad_btc = cantidad_dolares / precio_actual



    # Hacer una comparación entre el RSI y el SMA
    if rsi > sma[0]:
        # Ejecutar una orden de compra
        exchange.create_order(symbol='BTC/USDT', type='limit', side='buy', amount=cantidad_btc, price=precio_actual)
        precioCompra = precio_actual
        print("Se ha comprado al siguiente precio ", precioCompra)
    elif rsi < sma[0]:
        # Ejecutar una orden de venta
        exchange.create_order(symbol='BTC/USDT', type='limit', side='sell', amount=cantidad_btc, price=precio_actual)
        precioVenta = precio_actual
        print("Se ha vendido al siguiente precio ", precioVenta)

    ganancia = precioVenta - precioCompra
    print("Se ha hecho un total de ganancia",ganancia)
    cantidad_dolares = cantidad_dolares + ganancia