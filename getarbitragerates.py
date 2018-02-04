# This program calculates the ask and bid rates at different exchanges, and tells you the best option for arbitrage trading.
# Author: Hamid Mushtaq
import sys
import json, requests
import datetime

rj_cryptopia = requests.get('https://www.cryptopia.co.nz/api/GetMarkets/BTC').json()['Data']
rj_poloniex = requests.get('https://poloniex.com/public?command=returnTicker').json()

first_time = True
EXCHANGES = ["Cryptopia", "Bittrex", "HitBTC", "Poloniex", "Binance"]

# https://www.cryptopia.co.nz/Forum/Thread/255
def getFromCryptopia(coin):
	for r in rj_cryptopia:
		if r['Label'] == (coin.upper() + '/BTC'):
			return (float(r['AskPrice']), float(r['BidPrice']))
	return (0,0)
	
# https://poloniex.com/support/api/
def getFromPoloniex(coin):
	try:
		r = rj_poloniex["BTC_" + coin.upper()]
		return (float(r['lowestAsk']), float(r['highestBid']))
	except:
		return (0,0)
			
# https://bittrex.com/home/api
def getFromBittrex(coin):
	try:
		r = requests.get('https://bittrex.com/api/v1.1/public/getmarketsummary?market=btc-' + coin.lower()).json()['result'][0]
		return (float(r['Ask']), float(r['Bid']))
	except:
		return (0,0)
	
# https://api.hitbtc.com/?python#rest-api-reference
def getFromHitBTC(coin):
	try:
		r = requests.get('https://api.hitbtc.com/api/2/public/ticker/' + coin.upper() + 'BTC').json()
		return (float(r['ask']), float(r['bid']))
	except:
		return (0,0)
		
# https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md
def getFromBinance(coin):
	try:
		r = requests.get('https://api.binance.com/api/v1/ticker/24hr?symbol=' + coin.upper() + 'BTC').json()
		return (float(r['askPrice']), float(r['bidPrice']))
	except:
		return (0,0)
		
def getBestRate(rasks, rbids):
	lowestAsk = float('inf')
	lowestAskIndex = -1
	highestBid = 0
	highestBidIndex = -1
	
	for i in range(len(EXCHANGES)):
		if rasks[i] != 0:
			if rasks[i] < lowestAsk:
				lowestAsk = rasks[i]
				lowestAskIndex = i
			if rbids[i] > highestBid:
				highestBid = rbids[i]
				highestBidIndex = i
	
	return (lowestAsk, highestBid, lowestAskIndex, highestBidIndex)
		
def getAskAndBidStr(r):
	if (r[0] == 0):
		return 'Coin not found'
	else:
		return 'Ask=%g, Bid=%g' % (r[0], r[1])
		
def getCoinSymbolAndAmount():
	global first_time 
	
	input_str = 'Enter symbol of the coin: ' if (first_time == True) else '\nEnter symbol of a coin again (q to exit): '
	first_time = False
	amount = 0
	
	if (sys.version_info > (3, 0)):
		coin = input(input_str)
		if coin != 'q':
			amount = float(input('Enter amount to trade: '))
	else:
		coin = raw_input(input_str)
		if coin != 'q':
			amount = float(input('Enter amount to trade: '))
	
	return (coin.strip(), amount)

rj = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/').json()[0]
btc_usd = float(rj["price_usd"])

while True:
	coin, amount = getCoinSymbolAndAmount() 
	if coin == 'q':
		sys.exit(1)
	
	rcryptopia = getFromCryptopia(coin)
	rbittrex = getFromBittrex(coin)
	rhitbtc = getFromHitBTC(coin)
	rpoloniex = getFromPoloniex(coin)
	rbinance = getFromBinance(coin)
	
	rasks = [rcryptopia[0], rbittrex[0], rhitbtc[0], rpoloniex[0], rbinance[0]]
	rbids = [rcryptopia[1], rbittrex[1], rhitbtc[1], rpoloniex[1], rbinance[1]]
	
	now = datetime.datetime.now()
	print(now.strftime("\nTime: %H:%M:%S"))
	print('%10s: %s' % ('Crytopia', getAskAndBidStr(rcryptopia)))
	print('%10s: %s' % ('Bittrex', getAskAndBidStr(rbittrex)))
	print('%10s: %s' % ('HitBTC', getAskAndBidStr(rhitbtc)))
	print('%10s: %s' % ('Poloniex', getAskAndBidStr(rpoloniex)))
	print('%10s: %s' % ('Binance', getAskAndBidStr(rbinance)))
	
	lowestAsk, highestBid, lowestAskIndex, highestBidIndex = getBestRate(rasks, rbids)
	if (lowestAskIndex != -1) and (highestBidIndex != -1):
		print("--------------------------------------------")
		print("Buy from %s at %g ($%g)" % (EXCHANGES[lowestAskIndex], lowestAsk, lowestAsk * btc_usd))
		print("Sell on %s at %g ($%g)" % (EXCHANGES[highestBidIndex], highestBid, highestBid * btc_usd))
		profit = amount * (highestBid - lowestAsk)
		print("Profit with %g coins = %g BTC ($%g)" % (amount, profit, profit * btc_usd))
		print("--------------------------------------------")