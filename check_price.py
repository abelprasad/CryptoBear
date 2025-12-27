from bear.alpaca_rest import AlpacaPaper

api = AlpacaPaper()

# Get current price
price = api.get_price('BTCUSD')
print(f"\nCurrent BTC Price: ${price:,.2f}\n")

# Get open sell orders
orders = api.get_orders('open')
sells = [o for o in orders if o['side'] == 'sell']
sells_sorted = sorted(sells, key=lambda x: float(x['limit_price']))

print(f"Open SELL orders: {len(sells)}")
print(f"{'='*60}\n")

for sell in sells_sorted[:10]:
    sell_price = float(sell['limit_price'])
    distance = ((sell_price - price) / price) * 100
    print(f"SELL {sell['qty']:>10s} @ ${sell_price:>10,.2f}  (needs +{distance:.2f}%)")

print()
