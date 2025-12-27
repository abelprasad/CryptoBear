from bear.alpaca_rest import AlpacaPaper

api = AlpacaPaper()
orders = api.get_orders('open')

print(f"\nOpen orders: {len(orders)}\n")
for o in orders[:15]:
    print(f"  {o['side'].upper():4s} {o['qty']:>10s} @ ${float(o['limit_price']):>10,.2f}  (ID: {o['id'][:8]}...)")
