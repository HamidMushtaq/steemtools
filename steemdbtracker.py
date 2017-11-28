# Simple bot tracker which uses web crawling of the steemdb site
# Author: Hamid Mushtaq
import time
import sys
import urllib

bots = [
	"boomerang",
	"sneaky-ninja", 
	"voter", 
	"pushup", 
	"lovejuice", 
	"buildawhale", 
	"minnowhelper", 
	"booster", 
	"discordia",
	"upgoater",
	"appreciator",
	"sleeplesswhale"
]

def getStats(bot):
	power = ""
	list_of_transfers = []
	total_transfered = 0.0
	site = "https://steemd.com/@" + bot
	f = urllib.urlopen(site)
	content = f.read()
	lines = content.split("\n")
	steem_power = 0
	#
	#with open(bot + ".txt", "w") as text_file:
	#	text_file.write(content)

	line_ctr = 0
	last_line = ""
	for line in lines:
		if line_ctr > 0:
			line_ctr = line_ctr + 1
			if ("transfer " in line) and (" SBD" in line) and (bot in line) and (bot not in last_line):
				s = line.split()
				user_name = last_line.split('>')[-2].split('<')[0]
				post_url = line.split('<')[-2].split('>')[-1]
				list_of_transfers.append(user_name + ": " + s[1] + " SBD for " + post_url)
				total_transfered = total_transfered + float(s[1].strip())
			if ("upvote " in line) and (bot in last_line):
				line_ctr = 0
				return steem_power, power, list_of_transfers, total_transfered
		if (line_ctr == 0) and ("Voting Weight</h5>" in line) and (steem_power == 0):
			line_ctr = 1
		if (line_ctr == 3) and (steem_power == 0):
			s = line.strip().replace(",", "")
			steem_power = int(s) 
			line_ctr = 0
		if (line_ctr == 0) and ("Voting Power</h5>" in line):
			line_ctr = 1
		if line_ctr == 4:
			power = line.strip()
		last_line = line
	
start_time = time.time()

slist = []
for bot in bots:
	(steem_power, a, b, c) = getStats(bot)
	power = a.split('%')[0]
	element = (bot, steem_power / 1e4, power, b, c)
	slist.append(element)
	
sorted_list = sorted(slist, key=lambda x:float(x[2]))

for stats in sorted_list:
	bot_name, bot_worth, power, list_of_transfers, total_transfered = stats
	print bot_name + ": " + power + "%",
	perc_of_total = str(int(total_transfered * 100 / bot_worth))
	print "\t" + str(total_transfered) + "/" + str(bot_worth) + " (" + perc_of_total + " %) SBD transfered"
	for t in list_of_transfers:
		print "\t" + t
	print "\n"
	
time_in_secs = int(time.time() - start_time)
print "|| Time taken = " + str(time_in_secs / 60) + " mins " + str(time_in_secs % 60) + " secs ||"
