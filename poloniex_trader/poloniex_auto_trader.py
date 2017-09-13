# The trader class will be a object that makes recomendations of what to do with
# a currency pair. It can analyze candelstick data to recommend to hold or sell.
class trader:
    def __init__(self, api):
        self.api = api

    # This function will check the price at which you made a previous trade and
    # recommend whether you should hold or sell it based on what margin you want
    # to make. If you would gain the margin or if the coin is on a
    # downward trend and should be dumped then it will recommend to sell
    def should_sell(self, api, currencyPair, margin, loss):
        trade_data = self.api.returnTradeHistory('all')
        currency_price = (self.api.returnTicker())[currencyPair]['last']
        trade_margin = float((trade_data[currencyPair][0]['rate']))
        loss_margin = float((trade_data[currencyPair][0]['rate']))
        trade_margin *= float((1 + margin))
        loss_margin *= float((1 + loss))

        if(trade_margin <= currency_price):
            return 1

        elif(loss_margin <= trade_data[currencyPair][0]['rate']):
            return 1

        else:
            return 0

    def return_balances(self, pair, currency):
        return (self.api.returnBalances())[currency]
