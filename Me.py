import graph
import trade
import multiprocessing
import interval

global Invested
global totalProfit

Invested=False
totalProfit=0


Coin="USDT-XRP"

Triggers={
    "minPurchaseDecline":.97,
    "tempDecline":.97,
    "minPurchaseRebound":.01,
    "minProfit":.0225,
    "tempProfit":.0225,
    "minProfitDecline":.0025,
    "buy":False,
    "sell":False,
    "safety":-.15,
    "buyIn":0
}

def buyMessage(coinPair,amount,receipt):
    print("\n",flush=True)
    print("$" * 20,flush=True)
    print('BOUGHT:', str(amount) + " " + coinPair + " at " + str(trade.buyIn(coinPair)),flush=True)
    print("RECEIPT:",receipt)        
    print("$" * 20,flush=True)
    print("\n",flush=True)

def sellMessage(coinPair,amount,receipt):
    print("\n",flush=True)
    print("$" * 20,flush=True)
    print("SOLD:", str(amount) + " " + coinPair + " at " + str(trade.sellOut(coinPair)),flush=True)
    print("RECEIPT:",receipt)
    print("$" * 20,flush=True)
    print("\n",flush=True)

def wholeSaleMessage(coinPair,amount,receipt):
    print("\n",flush=True)
    print("$" * 20,flush=True)
    print('WholeSale:', str(amount) + " " + coinPair + " at " + str(trade.sellOut(coinPair)),flush=True)
    print("RECEIPT:",receipt)        
    print("$" * 20,flush=True)
    print("\n",flush=True)

def buy(coinPair,amount,FoK=False):
    receipt=trade.buy(coinPair,amount,FoK)
    buyMessage(coinPair,amount,receipt)
    global Invested
    Invested=True

def sell(coinPair,amount,FoK=False):
    receipt=trade.sell(coinPair,amount,FoK)
    sellMessage(coinPair,amount,receipt)
    global Invested
    Invested=False
    graph.clear()

def wholeSale(coinPair):
    receipt=sell(coinPair,trade.maxSell(coinPair),FoK=False)
    wholeSaleMessage(coinPair,trade.maxSell(coinPair),receipt)
    global Invested
    Invested=False

def In(chart):
    buyIn=Triggers["buyIn"]
    percProfit=((chart["price"] - buyIn) / buyIn)
    profitDecline=Triggers["tempProfit"] - percProfit

    print('DECISION:','SELL',flush=True)
    print('BUY IN:',buyIn,flush=True)
    print('PRICE:',chart["price"],flush=True)
    print('PROFIT (PERC):',percProfit,flush=True)
    print('PROFIT GOAL:',Triggers["tempProfit"],flush=True)
    print('DUMP (PERC):',profitDecline,flush=True)
    print('DUMP GOAL:',Triggers["minProfitDecline"],flush=True)
    print("\n",flush=True)

    if(percProfit >= Triggers["tempProfit"]):
        Triggers["tempProfit"]=percProfit
        Triggers["sell"]=True
    if(Triggers["sell"] and profitDecline >= Triggers["minProfitDecline"] and percProfit >= Triggers["minProfit"]):
        owned=trade.wallet(Coin)
        profit=percProfit * owned
        if(trade.toUSD(Coin,profit)<20):
            profit=trade.fromUSD(Coin,20)
        sell(Coin,profit)
        Triggers["tempProfit"]=Triggers["minProfit"]
    if(percProfit <= Triggers["safety"]):
        wholeSale(Coin)
        Triggers["tempProfit"]=Triggers["minProfit"]

def Out(chart):
    rebound=chart["relativePrice"] - Triggers["tempDecline"]

    print('DECISION:', 'BUY',flush=True)
    print("PRICE:",chart['price'],flush=True)
    print("HIGHEST PRICE:",chart['highestPrice'],flush=True)
    print('RELATIVE PRICE:',chart["relativePrice"],flush=True)
    print('RELATIVE PRICE (GOAL):',Triggers["tempDecline"],flush=True)
    print('PRICE REBOUND',rebound,flush=True)
    print('PRICE REBOUND (GOAL):',Triggers["minPurchaseRebound"],flush=True)
    print("\n",flush=True)

    if(chart["relativePrice"] <= Triggers["tempDecline"] and chart["relativePrice"]!=0):
        Triggers["tempDecline"]=chart["relativePrice"]
        Triggers["buy"]=True
    if(Triggers["buy"] and rebound >= Triggers["minPurchaseRebound"] and chart["relativePrice"] <= Triggers["minPurchaseDecline"]):
        Triggers["buyIn"]=trade.buyIn(Coin)        
        maxBuy=trade.maxBuy(Coin)
        buy(Coin,maxBuy)
        Triggers["tempDecline"]=Triggers["minPurchaseDecline"]

def GodSpeed():
        chart=graph.draw(Coin)
        if(Invested): In(chart)
        if(not Invested): Out(chart)
        # print( chart,'\n')

print("tradeCoin:",Coin,"\n")
interval.setInterval(GodSpeed,.33)
