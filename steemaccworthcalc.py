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

print "\nPrice of SBD = $%.2f (%.4f BTC)" % (sbd_usd, sbd_btc)
print "Price of STEEM = $%.2f (%.4f BTC)\n" % (steem_usd, steem_btc)

print "The total worth of your SBDs = $%.2f (%.4f BTC)" % (sbd_worth_usd, sbd_worth_btc)
print "The total worth of your STEEM = $%.2f (%.4f BTC)" % (steem_worth_usd, steem_worth_btc)

print "The total worth of your Steemit account = $%.2f (%.4f BTC)" % (total_worth_usd, total_worth_btc)
