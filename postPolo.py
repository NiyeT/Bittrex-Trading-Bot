import re
import json
import api

key=""
secret=""

bittrex=api.bittrex(key,secret)

#Outputs
#raw coin data
def rawData():
	return bittrex.returnTicker()

#Inputs
#raw Coin Data
#Outputs
#bittrex coin pairs
def coinPairs(coinData):
	bigCoinData=rawData()
	stringCoinData=str(bigCoinData)
	coins=re.findall("[\'\"](\w+)[\'\"]: {",stringCoinData)
	return coins

#Inputs
#coin pairs
#Outputs
#coin markets and the coins they can be traded for
def coinMarkets():
	pairs=coinPairs(rawData())
	markets={"coins":[]}
	for coinPair in pairs:
		coin=re.search("[^\_]+",coinPair).group(0)
		pairedCoin=re.search("_(.+)",coinPair).group(1)
		try:
			markets['coins'].index(coin)
		except Exception:
			markets['coins'].append(coin)
		try:
			markets[coin].append(pairedCoin)
		except Exception:
			markets[coin]=[]
			markets[coin].append(pairedCoin)
	return markets

def staticMarkets():
	return {'coins': ['BTC', 'USDT', 'XMR', 'ETH'], 'BTC': ['BCN', 'BELA', 'BLK', 'BTCD', 'BTM', 'BTS', 'BURST', 'CLAM', 'DASH', 'DGB', 'DOGE', 'EMC2', 'FLDC', 'FLO', 'GAME', 'GRC', 'HUC', 'LTC', 'MAID', 'OMNI', 'NAV', 'NEOS', 'NMC', 'NXT', 'PINK', 'POT', 'PPC', 'RIC', 'STR', 'SYS', 'VIA', 'XVC', 'VRC', 'VTC', 'XBC', 'XCP', 'XEM', 'XMR', 'XPM', 'XRP', 'ETH', 'SC', 'BCY', 'EXP', 'FCT', 'RADS', 'AMP', 'DCR', 'LSK', 'LBC', 'STEEM', 'SBD', 'ETC', 'REP', 'ARDR', 'ZEC', 'STRAT', 'NXC', 'PASC', 'GNT', 'GNO', 'BCH', 'ZRX', 'CVC', 'OMG', 'GAS', 'STORJ'], 'USDT': ['BTC', 'DASH', 'LTC', 'NXT', 'STR', 'XMR', 'XRP', 'ETH', 'ETC', 'REP', 'ZEC', 'BCH'], 'XMR': ['BCN', 'BLK', 'BTCD', 'DASH', 'LTC', 'MAID', 'NXT', 'ZEC'], 'ETH': ['LSK', 'STEEM', 'ETC', 'REP', 'ZEC', 'GNT', 'GNO', 'BCH', 'ZRX', 'CVC', 'OMG', 'GAS']}
