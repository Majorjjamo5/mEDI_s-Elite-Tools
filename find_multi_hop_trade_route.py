# -*- coding: UTF8

import timeit
import sys
from datetime import datetime, date, time, timedelta
import elite

start = timeit.default_timer()

mydb = elite.db()

startSystem = "ltt 9810"

tradingHops = 4  # +1 for the back hop
maxDist = 43  # max distace for B system
maxJumpDistance = 23
maxSearchRange = 60  # on start search used
maxStarDist = 1300
maxAge = 14  # max data age in days
minTradeProfit = 1000  # only to minimize results (speedup)
minStock = 150000  # > 10000 = stable route > 50000 = extrem stable route and faster results
resultLimit = 50

maxAgeDate = datetime.utcnow() - timedelta(days=maxAge)

elitetime = elite.elitetime(mydb, maxJumpDistance)



# mydb.calcSystemDistanceTableForSystem(2)
deals = []

start2 = timeit.default_timer()

startdeals = mydb.getBestDealsinDistance(startSystem, maxDist, maxSearchRange, maxAgeDate, maxStarDist, minTradeProfit, minStock, resultLimit)

print("getBestDealsinDistance", round(timeit.default_timer() - start2, 2))

print("startdeals", len(startdeals))

#sys.exit()

for deal in startdeals:
    deals.append({ "profit":0, "time":0 , "path":[deal] })


for deep in range(1, tradingHops):
    print("deep", deep+1)
    for deal in deals[:]:
        if deep == len(deal["path"]):
            delsX = mydb.getBestDealsFromStationInDistance(deal["path"][ len(deal["path"])-1 ]["StationBID"], maxDist, maxAgeDate, maxStarDist, minTradeProfit, minStock, resultLimit)
            for dealX in delsX:
                
                dealnew = deal.copy()
                dealnew["path"] = list(deal["path"]) #deepcopy do not work
                 
                dealnew["path"].append(dealX)
                deals.append(dealnew)

#back to start deal?
for deal in deals:
    backdeals = mydb.getDealsFromTo( deal["path"][ len(deal["path"])-1 ]["StationBID"],  deal["path"][0]["StationAID"])
    if backdeals:
        deal["backToStartDeal"] = backdeals[0]
    else:
        deal["backToStartDeal"] = None 


# calc profit and rating
for deal in deals:
    Systembefore = None
    for i, step in enumerate(deal["path"]):
        deal["profit"] += step["profit"]

        if i == 0:
            deal["time"] += elitetime.calcTimeFromTo(step["SystemAID"], step["StationBID"], step["SystemBID"])
            Systembefore = step["SystemBID"]
        else:
            deal["time"] += elitetime.calcTimeFromTo(Systembefore , step["StationBID"], step["SystemBID"])
            Systembefore = step["SystemBID"]

    # add back to start time
    deal["time"] += elitetime.calcTimeFromTo(Systembefore , deal["path"][0]["StationAID"], deal["path"][0]["SystemAID"])
    if deal["backToStartDeal"]:
        deal["profit"] += deal["backToStartDeal"]["profit"]

    lapsInHour = int(3600 / deal["time"])  # round down

    profitHour = int(3600.0 / deal["time"] * deal["profit"]) #hmm mit lapsInHour oder mit hochrechnung rechnen?

    deal["profitHour"] = profitHour
    deal["lapsInHour"] = lapsInHour
    

deals = sorted(deals , key=lambda deal: deal["profitHour"], reverse=True)

print("totaldeals", len(deals))

for i, deal in enumerate(deals):
    if i >= 40: break 

    timeT = "%s:%s" % (divmod(deal["time"] * deal["lapsInHour"], 60))
    timeL = "%s:%s" % (divmod(deal["time"], 60))

    print("%d. profit: %d profit/h:%d Laps/h: %d/%s LapTime: %s" % (i + 1, deal["profit"], deal["profitHour"], deal["lapsInHour"], timeT, timeL)) 


    before = { "StationB":deal["path"][0]["StationA"], "SystemB":deal["path"][0]["SystemA"], "StarDist":deal["path"][0]["stationA.StarDist"], "refuel":deal["path"][0]["stationA.refuel"]  }

    for d in deal["path"]:
        #print(d.keys())
        print("\t%s : %s (%d ls) (%s buy:%d) (%s ly)-> %s : %s (%d ls) (sell:%d profit:%d)" % (before["SystemB"], before["StationB"], before["StarDist"] , d["itemName"],d["StationSell"], d["dist"], d["SystemB"], d["StationB"],d["StarDist"], d["StationBuy"],  d["profit"] ) )
        if before["refuel"] != 1:
            print("\t\tWarning: %s have no refuel!?" % before["StationB"])
        
        before = d

    backdist = mydb.getDistanceFromTo(deal["path"][0]["SystemAID"] , deal["path"][ len(deal["path"])-1 ]["SystemBID"])

    if deal["backToStartDeal"]:
        #print(deal["backToStartDeal"].keys())
        print("\t%s : %s (%d ls) (%s buy:%d) (%s ly)-> %s : %s sell:%d profit:%d" % (before["SystemB"], deal["backToStartDeal"]["fromStation"] , before["StarDist"], deal["backToStartDeal"]["itemName"], deal["backToStartDeal"]["StationSell"], backdist, deal["path"][0]["SystemA"], deal["backToStartDeal"]["toStation"],deal["backToStartDeal"]["StationBuy"],  deal["backToStartDeal"]["profit"] ) )
    else:
        print("\tno back deal (%s ly) ->%s : %s" % (backdist, deal["path"][0]["SystemA"], deal["path"][0]["StationA"]  ))





print(round(timeit.default_timer() - start, 3))
print(sys.version)
