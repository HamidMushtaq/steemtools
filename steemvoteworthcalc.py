# This program calculates the total worth of your steemit upvote
# At the moment, it works with only Python 2.7 (not Python 3)
# Author: Hamid Mushtaq
import time
import sys
import requests # if its not installed already, install it using "pip install requests"
import json
import urllib
import re

upvote_weight = 100.0

def get_steem_per_mvests():
	site = 'https://steemdb.com/api/props'
	print("Communicating with " + site + " to find the value of steem_per_mvests...")
	rj = requests.get(site)
	steem_per_mvests = rj.json()[0]["steem_per_mvests"]
	print("* steem_per_mvests = " + str(steem_per_mvests))
	return steem_per_mvests
			
def get_reward_stats():
	site = "https://steemd.com/"
	print("\nCommunicating with site " + site + " to find the reward stats...")
	f = urllib.urlopen(site)
	content = f.read()
	lines = content.split("\n")
	for line in lines:
		if 'feed_price' in line:
			matchObj = re.match( r'(.*)feed_price(.*?)<i>(.*?) SBD(.*)', line, re.I)
			feed_price = matchObj.group(3)
			print("* feed_price = " + feed_price)
		if 'reward_balance' in line:
			matchObj = re.match( r'(.*)reward_balance(.*?)<i>(.*?) STEEM(.*?)recent_claims(.*?)<i>(.*?)</i>', line, re.I)
			reward_balance = matchObj.group(3).replace(',', '')
			recent_claims = matchObj.group(6).replace(',', '')
			print("* reward_balance = " + reward_balance)
			print("* recent_claims = " + recent_claims)
	
	return float(feed_price), float(reward_balance), float(recent_claims)
	
def get_total_vests(user):
	url = 'https://api.steemit.com'
	
	data = {
		"jsonrpc": "2.0",
		"method": "get_accounts",
		"params": [[user]],
		"id": 1
	}
	
	print("\nCommunicating with " + url + " to find the total_vests for " + user)
	resp = requests.post(url, json=data)
	data = json.loads(resp.content)['result'][0]
	
	vests = float(data['vesting_shares'].split()[0])
	received_vests = float(data['received_vesting_shares'].split()[0])
	delegated_vests = float(data['delegated_vesting_shares'].split()[0])
	total_vests = vests + received_vests - delegated_vests
	print "* total vests = " + str(total_vests)
	
	return total_vests

if len(sys.argv) > 1:
	username = sys.argv[1]
	if len(sys.argv) > 2:
		upvote_weight = float(sys.argv[2])
else:
	username = raw_input('username:')
	
if username[0] == '@':
	username = username[1:]
	
try:
	steem_per_mvests = get_steem_per_mvests()
except:
	print("Error getting steem_per_vests. Maybe the steemdb.com site is down.")
	sys.exit(1)
	
try:
	total_vests = get_total_vests(username)
except:
	print("User %s is not found!" % username)
	sys.exit(1)
	
try:
	feed_price, reward_balance, recent_claims = get_reward_stats()
except:
	print("Error getting the reward stats. Maybe the steemd.com site is down.")
	sys.exit(1)

X1 = (total_vests * 1e6 / recent_claims)
X2 = X1 * reward_balance
X3 = X2 * feed_price
upvote_worth = X3 * 2/100
print("\n%s has %g%% upvote worth of %g" % (username, upvote_weight, upvote_worth * upvote_weight / 100.0))
