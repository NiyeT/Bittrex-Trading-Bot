import postPolo
import re
from threading import Timer
from time import time

polo=postPolo.bittrex

bitcoin="USDT-BTC"

global bigO
bigO=polo.returnTicker()

def setBigO():
	global bigO
	bigO=polo.returnTicker()
	return True

def coinData(coin):
	for dataSet in bigO:
		if(dataSet["MarketName"]==coin):
			return dataSet

def buyIn(coin):
	return float(coinData(coin)['Ask'])

def sellOut(coin):
	return float(coinData(coin)['Bid'])

def toUSD(coinPair,amount):
	coinPrice=buyIn(coinPair)
	return amount * coinPrice	
	# split=re.findall("[^-]+",coinPair)
	# coin=split[1]
	# market="USDT-"+split[0]
	# coinPrice=buyIn(coinPair)
	# marketPrice=buyIn(market)
	# coinPriceUSD=coinPrice * marketPrice
	# return coinPriceUSD * amount

def fromUSD(coinPair,amount):
	price=toUSD(coinPair,1)
	relativePrice=amount / price
	return relativePrice

def exchangeGoal(ordered,received,percSold=.95):
	goalCheck=(ordered - received) / ordered
	print('goalCheck:',goalCheck)
	if(goalCheck>=percSold):return True
	return False

def withinPercentage(val1,val2,percCheck=.98):
	perc=val1 / val2
	if(perc>=percCheck): return True
	return False

def maxBuy(coin):
	split=re.findall("[^-]+",coin)
	market=split[0]
	currency=wallet(market)
	price=buyIn(coin)
	afterFee=currency - (fee(currency))
	maxP= afterFee / price
	return maxP

def maxSell(coin):
	split=re.findall("[^-]+",coin)
	target=split[1]
	return wallet(target)

def FillorKill(coin,amountOrdered,receipt,deadLine=3):
	def wrapper():
		amountReceived=float(receipt["resultingTrades"][0]["total"])
		goalMet=exchangeGoal(amountOrdered,amountReceived)
		if(not goalMet): polo.cancel(coin,receipt["uuid"])
	try:
		wrapper()
		return receipt
	except Exception:
		init=time()
		while(time()-init<deadLine):
			continue
		wrapper()
		return receipt
	else:
		polo.cancel(coin,receipt["orderNumber"])
		return {}

def buy(coinPair,amount,FoK=True):
	# amountCrypto=fromUSD(coinPair,amount)
	rate=buyIn(coinPair)
	receipt=polo.buy(coinPair,amount,rate)
	if(FoK): return FillorKill(coinPair,amount,receipt)
	return receipt

def sell(coinPair,amount,FoK=True):
	# amountCrypto=fromUSD(coinPair,amount)
	rate=sellOut(coinPair)
	receipt=polo.sell(coinPair,amount,rate)
	if(FoK): return FillorKill(coinPair,amount,receipt)
	return receipt

def wallet(coin):
	underscore=coin.find("-",0,len(coin))
	if(underscore!=-1): coin=re.findall("[^-]+",coin)[1]
	balances=polo.returnBalances()
	for balance in balances:
		if(balance['Currency'] == coin):
			return float(balance['Balance'])

def fee(amount,perc=.0025):
	return amount * perc

def percentageChange(oldPrice,newPrice):
	dif = newPrice - oldPrice
	change = dif / oldPrice
	return change

def lastPurchased(coin):
	# return float(polo.returnTradeHistory(coin)[0]["rate"])
	tradeHistory=polo.returnTradeHistory(coin)
	tradeHistoryLen=len(tradeHistory)
	counter=tradeHistoryLen
	for trade in range(tradeHistoryLen):
		trade=tradeHistory[counter]
		if(trade["type"]=="buy"): return float(trade["rate"])

def removeUSD(coin,amount,decrease):
	usd=toUSD(coin,amount)
	usdRemoved=usd - decrease
	return fromUSD(coin,usdRemoved)