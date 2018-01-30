# This program calculates the total worth of all your coins
# All your coins with their amounts should be put in a file coins.txt. An example file is given in this folder.
# Author: Hamid Mushtaq
import time
import json, requests
import operator
import datetime
import webbrowser, os
import os.path
import locale

CURRENCY="usd" # If no currency is given in coins.txt, USD would be assumed as default.

class Coin(object):
	def __init__(self, name, amount, price_cur, change1h, change24h):
		self.name = name
		self.amount = amount
		self.price_cur = price_cur
		self.worth = amount * price_cur
		self.change1h = change1h
		self.change24h = change24h
		
def imageStr(coinInfo):
	coinName = coinInfo.split(':')[0]
	if os.path.exists('images/' + coinName + '.png'):
		return " <img src=../images/%s.png alt=\"\" height=24 width=24></img>" % coinName  
	else:
		return ""
		
# If no currency is given in coins.txt, USD would be assumed as default
btc_ratio = float(requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/').json()[0]["price_usd"])

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
	if coinInfo.lower() == "currency":
		CURRENCY = x[1].strip().lower()
		if CURRENCY.lower() != 'usd':
			try:
				btc_ratio = float(requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=' + CURRENCY).json()[0]["price_" + CURRENCY])
			except:
				CURRENCY = 'usd' # When an invalid currency is entered, revert back to the default usd.
		continue
	coinName = coinInfo.split(':')[0]
	coinAmount = x[1].strip()
	try:
		req_str = 'https://api.coinmarketcap.com/v1/ticker/' + coinName + '/?convert=' + CURRENCY
		rj = requests.get(req_str).json()[0]
		price = rj["price_" + CURRENCY]
		change1h = rj["percent_change_1h"]
		change24h = rj["percent_change_24h"]
		coin = Coin(coinInfo, float(coinAmount), float(price), float(change1h), float(change24h))  
	except:
		coin = Coin(coinInfo, float(coinAmount), 0, 0, 0)
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
#cointable {
    font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
    border-collapse: collapse;
    width: 100%;
}

#cointable td, #cointable th {
    border: 1px solid #ddd;
    padding: 8px;
}

#cointable tr:nth-child(even){background-color: #f2f2f2;}

#cointable th {
    padding-top: 12px;
    padding-bottom: 12px;
    text-align: left;
    background-color: darkblue;
    color: white;
}

h2 {
	font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
}

.green_cell {
    color: limegreen;
}
.red_cell {
    color: red;
}
colored_span {
	color: darkblue 
}
</style>"""
f.write(table_style + '\n')

f.write('<h2>Total worth = <colored_span>%.2f %s (%.4f BTC)</colored_span></h2>\n' % (total, CURRENCY.upper(), total / btc_ratio))

i = 0
f.write('<table id = cointable>\n<tr>\n\t<th>Coin</th>\n \t<th>Price</th>\n \t<th>Change in 1 hour</th>\n \t<th>Change in 24 hours</th>\n \t<th>Amount</th>\n \t<th>Worth</th>\n')
for coin in sorted_coins:
	i = i + 1
	name = "%d. <a href=\"https://coinmarketcap.com/currencies/%s/\" target=\"_blank\">%s</a>" % \
		(i, coin.name.split(':')[0].lower(), coin.name.upper())
	f.write('<tr>\n')
	if (coin.price_cur != 0):
		price = "%.4f %s (%0.8f BTC)" % (coin.price_cur, CURRENCY.upper(), coin.price_cur / btc_ratio)
		amount = "%g" % coin.amount
		worth = "%0.2f %s (%0.4f BTC)" % (coin.worth, CURRENCY.upper(), coin.worth / btc_ratio) 
		change1h = "<td class=\"%s\">%0.2f%%</td>" % ("green_cell" if (coin.change1h >= 0) else "red_cell", coin.change1h)
		change24h = "<td class=\"%s\">%0.2f%%</td>" % ("green_cell" if (coin.change24h >= 0) else "red_cell", coin.change24h)
		f.write("\t<td>%s%s</td>\n \t<td>%s</td>\n \t%s\n \t%s\n \t<td>%s</td>\n \t<td>%s</td>\n" % \
			(name, imageStr(coin.name), price, change1h, change24h, amount, worth))
	else:
		price = "This coin doesn't exist" 
		amount = "%0.4f" % coin.amount
		worth = "-" 
		change1h = "<td>-</td>"
		change24h = "<td>-</td>"
		f.write("\t<td>%s%s</td>\n \t<td>%s</td>\n \t%s\n \t%s\n \t<td>%s</td>\n \t<td>%s</td>\n" % \
			(name, imageStr(coin.name), price, change1h, change24h, amount, worth))
	f.write('</tr>\n\n')
f.write('</table>\n\n')
f.write('</body>\n</html>\n')
f.close()

webbrowser.open('file://' + os.path.realpath(html_fname))
