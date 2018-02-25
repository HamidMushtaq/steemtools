# This program calculates the total worth of your steemit account in USD and BTC
# At the moment, it works with only Python 2.7 (not Python 3)
# Author: Hamid Mushtaq
import time
import coinmarketcap
import sys
import requests # if its not installed already, install it using "pip install requests"
import json
import urllib
import re

currency = "usd" # default is usd
		
def get_steem_per_mvests():
	site = "https://steemd.com/"
	print("Communicating with site " + site + " to find the value of steem_per_mvests...")
	f = urllib.urlopen(site)
	content = f.read()
	lines = content.split("\n")
	data = ""
	for line in lines:
		if 'steem_per_mvests' in line:
			# See reg exp examples at https://www.tutorialspoint.com/python/python_reg_expressions.htm
			matchObj = re.match( r'(.*)steem_per_mvests</samp></th></tr><tr><td><i>(.*?)</i>', line, re.I)
			steem_per_mvests = matchObj.group(2)
			print("\tsteem_per_mvests = " + steem_per_mvests)
			return float(steem_per_mvests)
			
def get_btc_price():
	rj = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=' + currency).json()[0]
	return float(rj["price_" + currency])
	
def get_sbd_price_in_btc():
	req_str = 'https://api.coinmarketcap.com/v1/ticker/steem-dollars/'
	rj = requests.get(req_str).json()[0]
	return float(rj["price_btc"])

def get_steem_price_in_btc():
	req_str = 'https://api.coinmarketcap.com/v1/ticker/steem/'
	rj = requests.get(req_str).json()[0]
	return float(rj["price_btc"])
	
def get_user_data(user):
	url = 'https://api.steemit.com'
	
	data = {
		"jsonrpc": "2.0",
		"method": "get_accounts",
		"params": [[user]],
		"id": 1
	}
	
	resp = requests.post(url, json=data)
	data = json.loads(resp.content)['result'][0]
	# split()[0] to remove the currency's name
	steem =  float(data['balance'].split()[0])
	sbd = float(data['sbd_balance'].split()[0])
	vests = float(data['vesting_shares'].split()[0])
	
	return steem, sbd, vests

if len(sys.argv) > 1:
	username = sys.argv[1]
	if len(sys.argv) > 2:
		currency = sys.argv[2]
else:
	username = raw_input('username:')
	
if username[0] == '@':
	username = username[1:]
	
try:
	steem_per_mvests = get_steem_per_mvests()
except:
	print("Error getting steem_per_vests. Maybe the site is down or its interface has changed.")
	sys.exit(1)
	
print("\nGetting the prices of BTC, STEEM and SBD...")
try:
	btc_price = get_btc_price()
	steem_btc = get_steem_price_in_btc()
	sbd_btc = get_sbd_price_in_btc()
except:
	print("Error getting the prices. Maybe you are using an invalid currency.")
	sys.exit(1)
	
currency_symbol = currency.upper()
print("\t* BTC price = %s %s" % (btc_price, currency_symbol))
print("\t* STEEM price = %g %s (%g BTC)" % (steem_btc * btc_price, currency_symbol, steem_btc))
print("\t* SBD price = %s %s (%g BTC)\n" % (sbd_btc * btc_price, currency_symbol, sbd_btc))

try:
	steem, sbd, vests = get_user_data(username)
except:
	print("User %s is not found!" % username)
	sys.exit(1)
steem_power = vests * steem_per_mvests / 1e6

steem_worth = steem * steem_btc
steem_power_worth = steem_power * steem_btc
sbd_worth = sbd * sbd_btc
total_worth = steem_worth + steem_power_worth + sbd_worth

print(username + " has:")
print("\t* %g STEEM worth %g %s (%g BTC)" % (steem, steem_worth * btc_price, currency_symbol, steem_worth))
print("\t* %g STEEM POWER worth %g %s (%g BTC)" % (steem_power, steem_power_worth * btc_price, currency_symbol, steem_power_worth))
print("\t* %g SBDs worth %g %s (%g BTC)" % (sbd, sbd_worth * btc_price, currency_symbol, sbd_worth))
print("\n\t* Total steemit worth of %g %s (%g BTC)" % (total_worth * btc_price, currency_symbol, total_worth))
