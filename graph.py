import trade

graph={
	"numAttrs":["initialPrice","price","highestPrice","lowestPrice","average","relativePrice","margin"],
	"coin":"",
	"initialPrice":0,
	"price":0,
	"highestPrice":0,
	"lowestPrice":0,
	"average":0,
	"relativePrice":0,
	"margin":0
}

global clearCanvas
clearCanvas=True

def clear():
	for attr in graph["numAttrs"]:
		graph[attr]=0
	global clearCanvas
	clearCanvas=True

def setBase():
	graph["initialPrice"]=graph["price"]
	global clearCanvas
	clearCanvas=False

def draw(Coin):
	trade.setBigO()
	graph["coin"]=Coin
	graph["price"]=trade.sellOut(Coin)
	if(clearCanvas): setBase()
	if(graph["highestPrice"] < graph["price"]): graph["highestPrice"]=graph["price"]
	if(graph["lowestPrice"] > graph["price"] or graph["lowestPrice"]==0): graph["lowestPrice"]=graph["price"]
	graph["average"]=((graph["highestPrice"] + graph["lowestPrice"]) / 2)
	graph["relativePrice"]=graph["price"] / graph["highestPrice"]
	graph["margin"]=graph["lowestPrice"] / graph["highestPrice"]
	return graph