import pandas as pd
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

class StockFetcher(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.stocks = []
        self.reqId = 1
        self.done = False

    def contractDetails(self, reqId, contractDetails):
        symbol = contractDetails.contract.symbol
        print(f"Symbol received: {symbol}")
        self.stocks.append(symbol)

    def contractDetailsEnd(self, reqId):
        print("All contract details received.")
        self.stop()

    def error(self, reqId, errorCode, errorString):
        print(f"Error {errorCode}: {errorString}")

    def stop(self):
        df = pd.DataFrame(self.stocks, columns=['Symbol'])
        df.to_csv("lse_stocks.csv", index=False)
        print("Stock list saved to lse_stocks.csv.")
        self.done = True
        self.disconnect()

    def start(self):
        print("Starting stock fetch...")
        contract = Contract()
        contract.symbol = "BARC"  # Barclays as an example
        contract.secType = "STK"
        contract.exchange = "LSE"
        contract.currency = "GBP"
        self.reqContractDetails(self.reqId, contract)
        self.reqId += 1

def main():
    app = StockFetcher()
    print("Connecting to TWS...")
    app.connect("127.0.0.1", 7496, 0)  # Use the correct port for your setup
    app.run()

if __name__ == "__main__":
    main()
