# This program calculates the total worth of your steemit account in USD and BTC
# Before running it, install the coinmarket api -> pip install coinmarketcap
# Author: Hamid Mushtaq
import time
import coinmarketcap

print
steem = float(input("Enter the amount of STEEM you have: "))
sbds = float(input("Enter the amount of SBDs you have: "))

market = coinmarketcap.Market()

sbd_coin = market.ticker("steem-dollars")[0]
sbd_usd = float(sbd_coin["price_usd"])
sbd_btc = float(sbd_coin["price_btc"])

steem_coin = market.ticker("steem")[0]
steem_usd = float(steem_coin["price_usd"])
steem_btc = float(steem_coin["price_btc"])

steem_worth_usd = steem_usd * steem
steem_worth_btc = steem_btc * steem

sbd_worth_usd = sbd_usd * sbds
sbd_worth_btc = sbd_btc * sbds

total_worth_usd = steem_worth_usd + sbd_worth_usd
total_worth_btc = steem_worth_btc + sbd_worth_btc

print "\nPrice of SBD = $" + str(sbd_usd) + " (" + str(sbd_btc) + " BTC)"
print "Price of STEEM = $" + str(steem_usd) + " (" + str(steem_btc) + " BTC)\n"

print "The total worth of your SBDs = $" + str(sbd_worth_usd) + " (" + str(sbd_worth_btc) + " BTC)"
print "The total worth of your STEEM = $" + str(steem_worth_usd) + " (" + str(steem_worth_btc) + " BTC)\n"

print "The total worth of your Steemit account = $" + str(total_worth_usd) + " (" + str(total_worth_btc) + " BTC)"
