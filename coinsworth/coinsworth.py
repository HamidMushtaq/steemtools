# This program calculates the total worth of all your coins
# Before running it, install the coinmarket api -> pip install coinmarketcap
# All your coins with their amounts should be put in a file coins.txt. An example file is given in this folder.
# Author: Hamid Mushtaq
import time
import coinmarketcap
import json, requests
import operator
import datetime

class Coin(object):
	def __init__(self, name, amount, price_usd):
		self.name = name
		self.amount = amount
		self.price_usd = price_usd
		self.worth = amount * price_usd
		
market = coinmarketcap.Market()
btc_usd = float(market.ticker("bitcoin")[0]["price_usd"])

filepath = 'coins.txt'  
coins = []
total = 0.0

with open(filepath) as fp:  
	lines = fp.readlines()

for line in lines:
	x = line.split('=')
	if len(x) < 2:
		continue
	coinInfo = x[0].strip()
	coinName = coinInfo.split(':')[0]
	coinAmount = x[1].strip()
	try:
		coin = Coin(coinInfo, float(coinAmount), float(market.ticker(coinName)[0]["price_usd"]))  
	except:
		coin = Coin(coinInfo, 0, 0)
	coins.append(coin)
	total = total + coin.worth
	
sorted_coins = sorted(coins, key=operator.attrgetter('worth'))
now = datetime.datetime.now()
horiz_line = "-" * 120
print now.strftime("Time: %Y-%m-%d %H:%M")
print horiz_line
i = 0
for coin in sorted_coins:
	i = i + 1
	name = "%d. %s" % (i, coin.name.upper())
	if (coin.price_usd != 0):
		price = "|price = $%0.3f (%0.6f BTC)" % (coin.price_usd, coin.price_usd / btc_usd)
		amount = "|amount = %0.3f" % coin.amount
		worth = "|worth = $%0.3f (%0.6f BTC)" % (coin.worth, coin.worth / btc_usd) 
		print "%-25s %-40s %-20s %-40s" % (name, price, amount, worth)
	else:
		err_msg = "|This coin doesn't exist"
		print "%-25s %s " % (name, err_msg)
	print horiz_line
print "Total = $%.2f (%.6f BTC)" % (total, total / btc_usd)
print horiz_line + '\n'
