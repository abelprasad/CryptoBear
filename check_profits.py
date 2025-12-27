from bear.alpaca_rest import AlpacaPaper
from datetime import datetime, timedelta

api = AlpacaPaper()

# Get all filled orders from today
filled_orders = api.get_orders(status='closed', limit=100)

# Filter for filled orders only (not cancelled)
filled_orders = [o for o in filled_orders if o['status'] == 'filled']

print(f"\n{'='*70}")
print(f"FILLED ORDERS ANALYSIS")
print(f"{'='*70}\n")

if not filled_orders:
    print("No filled orders yet.\n")
else:
    print(f"Total filled orders: {len(filled_orders)}\n")

    # Separate buys and sells
    buys = [o for o in filled_orders if o['side'] == 'buy']
    sells = [o for o in filled_orders if o['side'] == 'sell']

    print(f"Filled BUYs:  {len(buys)}")
    print(f"Filled SELLs: {len(sells)}\n")

    # Show recent fills
    print("Recent Filled Orders:")
    print("-" * 70)
    for order in filled_orders[:10]:
        side = order['side'].upper()
        qty = float(order['filled_qty'])
        price = float(order['filled_avg_price'])
        total = qty * price
        filled_at = order.get('filled_at', 'N/A')

        print(f"{side:4s} {qty:>10.6f} @ ${price:>10,.2f} = ${total:>10,.2f}  [{filled_at[:16] if filled_at != 'N/A' else 'N/A'}]")

    # Calculate potential profits (simple FIFO matching)
    if buys and sells:
        print(f"\n{'='*70}")
        print("PROFIT ANALYSIS (FIFO Matching)")
        print(f"{'='*70}\n")

        # Sort by fill time
        buys_sorted = sorted(buys, key=lambda x: x.get('filled_at', ''))
        sells_sorted = sorted(sells, key=lambda x: x.get('filled_at', ''))

        total_profit = 0
        matched_cycles = 0

        for sell in sells_sorted:
            if not buys_sorted:
                break

            sell_price = float(sell['filled_avg_price'])
            sell_qty = float(sell['filled_qty'])
            remaining_qty = sell_qty

            while remaining_qty > 0 and buys_sorted:
                buy = buys_sorted[0]
                buy_price = float(buy['filled_avg_price'])
                buy_qty = float(buy['filled_qty'])

                matched_qty = min(remaining_qty, buy_qty)
                profit = (sell_price - buy_price) * matched_qty
                profit_pct = ((sell_price - buy_price) / buy_price) * 100

                print(f"Cycle #{matched_cycles + 1}:")
                print(f"  Buy:  {matched_qty:.6f} @ ${buy_price:,.2f}")
                print(f"  Sell: {matched_qty:.6f} @ ${sell_price:,.2f}")
                print(f"  Profit: ${profit:.2f} ({profit_pct:+.2f}%)")
                print()

                total_profit += profit
                matched_cycles += 1
                remaining_qty -= matched_qty

                if matched_qty >= buy_qty:
                    buys_sorted.pop(0)
                else:
                    # Partial match, update buy quantity
                    buys_sorted[0] = {**buy, 'filled_qty': str(buy_qty - matched_qty)}

        print(f"{'='*70}")
        print(f"TOTAL REALIZED PROFIT: ${total_profit:.2f}")
        print(f"Completed Cycles: {matched_cycles}")
        print(f"{'='*70}\n")
    else:
        print("\nNo completed buy->sell cycles yet.")
        print("(Waiting for sells to fill to realize profits)\n")

print()
