# This program calculates the total worth of all your coins
# Before running it, install the coinmarket api -> pip install coinmarketcap
# All your coins with their amounts should be put in a file coins.txt. An example file is given in this folder.
# Author: Hamid Mushtaq
import time
import coinmarketcap
import json, requests
import operator
import datetime
import webbrowser, os
import os.path

class Coin(object):
	def __init__(self, name, amount, price_usd):
		self.name = name
		self.amount = amount
		self.price_usd = price_usd
		self.worth = amount * price_usd
		
def imageStr(coinInfo):
	coinName = coinInfo.split(':')[0]
	if os.path.exists('images/' + coinName + '.png'):
		return " <img src=../images/%s.png alt=\"\" height=24 width=24></img>" % coinName  
	else:
		return ""
		
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
current_time = now.strftime("%d_%m_%Y-%H_%M") 

if not os.path.isdir('html'):
	os.makedirs('html')
html_fname = 'html/coinstable_%s.html' % current_time
print html_fname
f = open(html_fname, 'w')
f.write('<!DOCTYPE html>\n<html>\n<body>\n\n')
table_style="""
<style>
table {
    width:100%;
}
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
th, td {
    padding: 5px;
    text-align: left;
}
</style>"""
f.write(table_style + '\n')
f.write('<table>\n<tr>\n\t<th>Coin</th>\n \t<th>Coin price</th>\n \t<th>Coin amount</th>\n \t<th>Coin worth</th>\n')

i = 0
for coin in sorted_coins:
	i = i + 1
	name = "%d. %s" % (i, coin.name.upper())
	f.write('<tr>\n')
	if (coin.price_usd != 0):
		price = "$%0.3f (%0.6f BTC)" % (coin.price_usd, coin.price_usd / btc_usd)
		amount = "%0.3f" % coin.amount
		worth = "$%0.3f (%0.6f BTC)" % (coin.worth, coin.worth / btc_usd) 
		f.write("\t<td>%s%s</td>\n \t<td>%s</td>\n \t<td>%s</td>\n \t<td>%s</td>\n" % (name, imageStr(coin.name), price, amount, worth))
	else:
		err_msg = "|This coin doesn't exist"
		f.write("<td>\n%-25s</td><td>\n%s</td>\n" % (name, err_msg))
	f.write('</tr>\n\n')
f.write('</table>\n\n')
f.write("<p>Total = <b>$%.2f (%.6f BTC)</b></p>" % (total, total / btc_usd))
f.write('</body>\n</html>\n')
f.close()

webbrowser.open('file://' + os.path.realpath(html_fname))
