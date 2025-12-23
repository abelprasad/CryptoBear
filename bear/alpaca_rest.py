import os, requests, json, time
from dotenv import load_dotenv
load_dotenv()

class AlpacaPaper:
    def __init__(self):
        self.key    = os.getenv('ALPACA_API_KEY')
        self.secret = os.getenv('ALPACA_API_SECRET')
        self.base   = 'https://paper-api.alpaca.markets'
        self.session = requests.Session()
        self.session.headers.update({
            'APCA-API-KEY-ID':  self.key,
            'APCA-API-SECRET-KEY': self.secret
        })

    # --------- helpers ----------
    def _norm(self, symbol):
        """BTCUSD -> BTC/USD for crypto API"""
        if len(symbol) == 6:  # e.g., BTCUSD
            return f"{symbol[:3]}/{symbol[3:]}"
        return symbol  # already formatted

    # --------- price ------------
    def get_price(self, symbol):
        # Alpaca crypto uses data API, not paper-api
        url = f"https://data.alpaca.markets/v1beta3/crypto/us/latest/quotes"
        params = {"symbols": self._norm(symbol)}
        r = self.session.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        symbol_key = self._norm(symbol)
        return float(data['quotes'][symbol_key]['bp'])   # bid price

    # --------- balance ----------
    def get_balance(self):
        url = f"{self.base}/v2/account"
        r = self.session.get(url)
        r.raise_for_status()
        return float(r.json()['cash'])

    # --------- orders -----------
    def buy(self, symbol, qty, price):
        url = f"{self.base}/v2/orders"
        data = {
            "symbol":      self._norm(symbol),
            "qty":         str(qty),
            "side":        "buy",
            "type":        "limit",
            "limit_price": str(price),
            "time_in_force": "gtc"
        }
        r = self.session.post(url, json=data)
        r.raise_for_status()
        return r.json()

    def sell(self, symbol, qty, price):
        url = f"{self.base}/v2/orders"
        data = {
            "symbol":      self._norm(symbol),
            "qty":         str(qty),
            "side":        "sell",
            "type":        "limit",
            "limit_price": str(price),
            "time_in_force": "gtc"
        }
        r = self.session.post(url, json=data)
        r.raise_for_status()
        return r.json()

    # --------- order management -----------
    def get_orders(self, status='open', limit=500):
        """Get orders by status"""
        url = f"{self.base}/v2/orders"
        params = {'status': status, 'limit': limit}
        r = self.session.get(url, params=params)
        r.raise_for_status()
        return r.json()

    def get_order(self, order_id):
        """Get single order by ID"""
        url = f"{self.base}/v2/orders/{order_id}"
        r = self.session.get(url)
        r.raise_for_status()
        return r.json()

    def cancel_order(self, order_id):
        """Cancel a specific order"""
        url = f"{self.base}/v2/orders/{order_id}"
        r = self.session.delete(url)
        r.raise_for_status()
        return r.json()

    def cancel_all_orders(self):
        """Cancel all open orders"""
        url = f"{self.base}/v2/orders"
        r = self.session.delete(url)
        r.raise_for_status()
        return r.json()