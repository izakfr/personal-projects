import urllib
import urllib2
import json
import time
import hmac,hashlib

# Define a function to return a timestamp
def createTimeStamp(datestr, format="%Y-%m-%d %H:%M:%S"):
    return time.mktime(time.strptime(datestr, format))

class poloniex:
    def __init__(self, APIKey, Secret):
        self.APIKey = APIKey
        self.Secret = Secret

    def post_process(self, before):
        after = before
        return after
        # Format the timestamps correctly after recieving the json
        if('return' in after):
            if(isinstance(after['return'], list)):
                for x in xrange(0, len(after['return'])):
                    if(isinstance(after['return'][x], dict)):
                        if('datetime' in after['return'][x] and 'timestamp' not in after['return'][x]):
                            after['return'][x]['timestamp'] = float(createTimeStamp(after['return'][x]['datetime']))
        return after

    # This function will query the api based on the command given
    def api_query(self, command, req={}):
        # Different queries require different arguements, we try to clump them
        # into similar groups
        if(command == "returnTicker" or command == "return24hVolume"):
            data = urllib2.urlopen(urllib2.Request('https://poloniex.com/public?command=' + command))
            return self.post_process(json.load(data))

        elif(command == "returnOrderBook"):
            data = urllib2.urlopen(urllib2.Request('https://poloniex.com/public?command='
                                                   + command + "&currencyPair="
                                                   + str(req['currencyPair'])
                                                   + "&depth="
                                                   + str(req['depth'])))
            return self.post_process(json.load(data))

        elif(command == "returnTradeHistoryGlobal"):
            data = urllib2.urlopen(urllib2.Request('https://poloniex.com/public?command='
                                                   + "returnTradeHistory&currencyPair="
                                                   + str(req['currencyPair'])))
            return self.post_process(json.load(data))

        # All of the trading methods take the same form in respect to what we
        # send to poloniex
        else:
            # Do all the necessary work to use the private api through poloniex
            # poloniex requires a nonce to be used in each method, each nonce
            # larger than the previous, we use time to solve this issue
            req['nonce'] = int(time.time()*1000)
            req['command'] = command
            POST_data = urllib.urlencode(req)

            # The api requires a sign to be created using the users private key
            # and is generated using HMAC-SHA512
            sign = hmac.new(self.Secret, POST_data, hashlib.sha512).hexdigest()

            # There are two headers required, the sign and the api key
            headers = { 'Sign': sign, 'Key': self.APIKey }

            data = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi',
                                                    POST_data, headers))

            return self.post_process(json.load(data))

    # Define functions for all public queries below
    def returnTicker(self):
        return self.api_query("returnTicker")

    def return24hVolume(self):
        return self.api_query("return24hVolume")

    def returnOrderBook(self, currencyPair, depth):
        return self.api_query("returnOrderBook", {'currencyPair': currencyPair,
                                                  'depth': depth})

    def returnTradeHistoryGlobal(self, currencyPair):
        return self.api_query("returnTradeHistoryGlobal",
                              {'currencyPair': currencyPair})

    # Define functions for all private trading

    # Returns a list of balances
    # In the form: {"BTC":"XXXX.XX", "ETH":"XXXX.XX"...}
    def returnBalances(self):
        return self.api_query("returnBalances")

    # Returns a verbose list of all balances by also providing the availible
    # amount of each coin, the amount being used in orders and its equivalent
    # value in BTC
    def returnCompleteBalances(self):
        return self.api_query("returnCompleteBalances")

    # Returns the addresses to deposit cryptocurrency into poloniex
    def returnDepositAddresses(self):
        return self.api_query("returnDepositAddresses")

    # Returns a list of open orders with order number, type (sell or buy), rate,
    # amount and total for a given currency pair, if none is specified it does all
    def returnOpenOrders(self, currencyPair):
        return self.api_query("returnOpenOrders", {'currencyPair': currencyPair})

    # Returns personal trade history between two currencies, the limit decides
    # how many trades are returns
    def returnTradeHistory(self, currencyPair, limit):
        return self.api_query("returnTradeHistory", {'limit': limit})

    # Returns the chart data for the given currecy pair
    # This requires the following
    # period (candlestick length): 300, 900, 1800, 7200, 14400, or 86400
    # start: unix encoded date
    # end: unix encoded date
    def returnChartData(self, currencyPair, period, start, end):
        return self.api_query("returnChartData", {'currencyPair':currencyPair,
                                                  'period':period,
                                                  'start':start,
                                                  'end':end})
