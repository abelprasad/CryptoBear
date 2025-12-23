from bear import config
from bear.alpaca_rest import AlpacaPaper
from bear.telegram import teddy_say

# Initialize Alpaca
api = AlpacaPaper()
pair = config['pair']

# Get current data
price = api.get_price(pair)
balance = api.get_balance()

# Send status to Telegram
message = f"""
CryptoBear Status Report
━━━━━━━━━━━━━━━━━━━━
💰 {pair}: ${price:,.2f}
💵 Balance: ${balance:,.2f}
📊 Exchange: Alpaca Paper
✅ All systems operational
"""

if teddy_say(message.strip()):
    print("[OK] Status report sent to Telegram")
else:
    print("[ERROR] Failed to send to Telegram")

print(f"\n{pair} Price: ${price:,.2f}")
print(f"Account Balance: ${balance:,.2f}")
