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

coins = {}
total_worth = {}
total = 0.0

class Coin(object):
	def __init__(self, coin_info, amount, price_cur, change1h, change24h):
		context = "other"
		coin_and_context = coin_info.split(':')
		if len(coin_and_context) > 1:
			context = coin_and_context[1].strip()
		if context not in coins:
			coins[context] = []
			total_worth[context] = 0.0
		
		self.name = coin_and_context[0].strip()
		self.context = context
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
rj = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/').json()[0]
btc_ratio = float(rj["price_usd"])
btc_change1h = float(rj["percent_change_1h"])
btc_change4h = float(rj["percent_change_24h"])

filepath = 'coins.txt'
now = datetime.datetime.now()
current_time = now.strftime("%d_%m_%Y-%H_%M")   

if not os.path.isdir('html'):
		os.makedirs('html')
html_fname = 'html/coinstable_%s.html' % current_time
f = open(html_fname, 'w')
f.write('<!DOCTYPE html>\n<html>\n<body bgcolor=lavender>\n\n')
table_style="""
<style>
#cointable {
	font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
	border-collapse: collapse;
	background-color: white;
	width: 100%;
}

#cointable td, #cointable th {
	border: 1px solid #ddd;
	padding: 8px;
}

#cointable tr:nth-child(even){background-color: whitesmoke;}

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

with open(filepath) as fp:  
		lines = fp.readlines()

for line in lines:
	x = line.split('=')
	if len(x) < 2:
		continue
	coin_info = x[0].strip()
	coin_name = coin_info.split(':')[0].strip()
	if coin_info.lower() == "currency":
		CURRENCY = x[1].strip().lower()
		if CURRENCY.lower() != 'usd':
			try:
				rj = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=' + CURRENCY).json()[0]
				btc_ratio = float(rj["price_" + CURRENCY])
				btc_change1h = float(rj["percent_change_1h"])
				btc_change4h = float(rj["percent_change_24h"])
			except:
				CURRENCY = 'usd' # When an invalid currency is entered, revert back to the default usd.
		continue
	coin_amount = x[1].strip()
	
	try:
		req_str = 'https://api.coinmarketcap.com/v1/ticker/' + coin_name + '/?convert=' + CURRENCY
		rj = requests.get(req_str).json()[0]
		price = rj["price_" + CURRENCY]
		change1h = rj["percent_change_1h"]
		change24h = rj["percent_change_24h"]
		coin = Coin(coin_info, float(coin_amount), float(price), float(change1h), float(change24h))  
	except:
		coin = Coin(coin_info, float(coin_amount), 0, 0, 0)
	coins[coin.context].append(coin)
	total_worth[coin.context] = total_worth[coin.context] + coin.worth
	total = total + coin.worth

def drawTable(context):
	sorted_coins = sorted(coins[context], key=operator.attrgetter('change1h'), reverse=True)

	f.write('<h2>Total worth %s = <colored_span>%.2f %s (%.4f BTC)</colored_span></h2>\n' % \
		("for rest" if context == "other" else "at " + context, total_worth[context], CURRENCY.upper(), total_worth[context] / btc_ratio))

	i = 0
	f.write('<table id = cointable>\n<tr>\n\t<th>Coin</th>\n \t<th>Amount</th>\n \t<th>Worth</th> \t<th>Price</th>\n \t<th>Change in 1 hour</th>\n \t<th>Change in 1 hour w.r.t BTC</th>\n \t<th>Change in 24 hours</th>\n \t<th>Change in 24 hours w.r.t BTC</th>\n \n')
	for coin in sorted_coins:
		i = i + 1
		name = "%d. <a href=\"https://coinmarketcap.com/currencies/%s/\" target=\"_blank\">%s</a>" % (i, coin.name.lower(), coin.name.upper())
		f.write('<tr>\n')
		if (coin.price_cur != 0):
			price = "%.4f %s (%0.8f BTC)" % (coin.price_cur, CURRENCY.upper(), coin.price_cur / btc_ratio)
			amount = "%g" % coin.amount
			worth = "%0.2f %s (%0.4f BTC)" % (coin.worth, CURRENCY.upper(), coin.worth / btc_ratio)
			change1h_td = "<td class=\"%s\">%0.2f%%</td>" % ("green_cell" if (coin.change1h >= 0) else "red_cell", coin.change1h)
			change24h_td = "<td class=\"%s\">%0.2f%%</td>" % ("green_cell" if (coin.change24h >= 0) else "red_cell", coin.change24h)
			# Changes with respect to BTC
			change1h_wrt_btc = coin.change1h - btc_change1h
			change24h_wrt_btc = coin.change24h - btc_change4h
			change1h_wrt_btc_td = "<td class=\"%s\">%0.2f%%</td>" % ("green_cell" if (change1h_wrt_btc >= 0) else "red_cell", change1h_wrt_btc)
			change24h_wrt_btc_td = "<td class=\"%s\">%0.2f%%</td>" % ("green_cell" if (change24h_wrt_btc >= 0) else "red_cell", change24h_wrt_btc)
			f.write("\t<td>%s%s</td>\n \t<td>%s</td>\n \t<td>%s</td>\n \t<td>%s</td>\n \t%s\n \t%s\n \t%s\n \t%s\n" % \
				(name, imageStr(coin.name), amount, worth, price, change1h_td, change1h_wrt_btc_td, change24h_td, change24h_wrt_btc_td))
		else:
			price = "This coin doesn't exist" 
			amount = "%0.4f" % coin.amount
			worth = "-" 
			change = "<td>-</td>"
			f.write("\t<td>%s%s</td>\n  \t<td>%s</td>\n \t<td>%s</td>\n \t<td>%s</td>\n \t%s\n \t%s\n \t%s\n \t%s\n" % \
				(name, imageStr(coin.name), amount, worth, price, change, change, change, change))
		f.write('</tr>\n\n')
	f.write('</table>\n<br/>\n')

f.write('<h2>Total worth = <colored_span>%.2f %s (%.4f BTC)</colored_span></h2>\n<hr>\n' % (total, CURRENCY.upper(), total / btc_ratio))
sorted_total_worth = sorted(total_worth.items(), key=operator.itemgetter(1), reverse=True)
for e in sorted_total_worth:
	drawTable(e[0])
f.write('</body>\n</html>\n')

f.close()
webbrowser.open('file://' + os.path.realpath(html_fname))
