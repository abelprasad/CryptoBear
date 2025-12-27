from bear.alpaca_rest import AlpacaPaper
from datetime import datetime

api = AlpacaPaper()

print("\n" + "="*70)
print("GRID BOT ACTIVITY LOG")
print("="*70 + "\n")

# Get all orders (open and closed)
all_orders = api.get_orders(status='all', limit=50)

# Sort by creation time
all_orders_sorted = sorted(all_orders, key=lambda x: x.get('created_at', ''))

print(f"Total orders created: {len(all_orders)}\n")

# Group by status
statuses = {}
for order in all_orders:
    status = order['status']
    statuses[status] = statuses.get(status, 0) + 1

print("Order Status Summary:")
for status, count in sorted(statuses.items()):
    print(f"  {status:15s}: {count:3d}")

print("\n" + "-"*70)
print("ORDER TIMELINE (Most Recent Last)")
print("-"*70 + "\n")

for order in all_orders_sorted[-20:]:  # Last 20 orders
    created = order.get('created_at', 'N/A')[:16]
    filled = order.get('filled_at', '')
    filled_str = filled[:16] if filled else 'pending'

    side = order['side'].upper()
    qty = order['qty']
    price = float(order['limit_price'])
    status = order['status']

    status_symbol = {
        'filled': '[X]',
        'new': '[ ]',
        'accepted': '[ ]',
        'pending_new': '[~]',
        'canceled': '[-]',
        'rejected': '[!]'
    }.get(status, '[?]')

    print(f"{status_symbol} [{created}] {side:4s} {qty:>10s} @ ${price:>10,.2f}  [{status:12s}]")
    if filled:
        print(f"      -> Filled: {filled_str}")

print("\n" + "="*70)
print("CURRENT STATE")
print("="*70 + "\n")

# Current price
current_price = api.get_price('BTCUSD')
print(f"Current BTC Price: ${current_price:,.2f}")

# Account balance
balance = api.get_balance()
print(f"Account Balance:   ${balance:,.2f}")

# Open orders
open_orders = [o for o in all_orders if o['status'] in ['new', 'accepted', 'pending_new']]
open_buys = [o for o in open_orders if o['side'] == 'buy']
open_sells = [o for o in open_orders if o['side'] == 'sell']

print(f"\nOpen Orders: {len(open_orders)} ({len(open_buys)} buys, {len(open_sells)} sells)")

# Filled orders
filled_orders = [o for o in all_orders if o['status'] == 'filled']
filled_buys = [o for o in filled_orders if o['side'] == 'buy']
filled_sells = [o for o in filled_orders if o['side'] == 'sell']

print(f"Filled Orders: {len(filled_orders)} ({len(filled_buys)} buys, {len(filled_sells)} sells)")

if filled_buys:
    total_invested = sum(float(o['filled_qty']) * float(o['filled_avg_price']) for o in filled_buys)
    total_btc = sum(float(o['filled_qty']) for o in filled_buys)
    print(f"\nAccumulated Position: {total_btc:.6f} BTC (${total_invested:,.2f} invested)")

print()
