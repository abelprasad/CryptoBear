"""Test script to verify grid initialization without running the loop"""
from bear import config
from bear.logger import setup_logger
from bear.trader import GridTradingBot
from bear.telegram import teddy_say

if __name__ == '__main__':
    # Setup logging
    logger = setup_logger(level='INFO')

    # Initialize bot
    bot = GridTradingBot(config)

    try:
        print("\n" + "=" * 60)
        print("Testing Grid Trading Bot Initialization")
        print("=" * 60 + "\n")

        teddy_say("🧪 Testing grid bot initialization...")

        # Initialize grid and place orders
        bot.initialize()

        print("\n" + "=" * 60)
        print("INITIALIZATION COMPLETE")
        print("=" * 60)
        print(f"Active orders: {len(bot.active_orders)}")
        print(f"Grid center: ${bot.grid_levels['center_price']:,.2f}")
        print(f"Buy levels: {len(bot.grid_levels['buy_levels'])}")
        print(f"Sell levels: {len(bot.grid_levels['sell_levels'])}")
        print("\nOrders placed:")
        for order_id, order_info in bot.active_orders.items():
            print(f"  {order_info['side'].upper():4s} @ ${order_info['price']:>10,.2f} (level {order_info['level']:+2d})")

        teddy_say(f"✅ Test complete! {len(bot.active_orders)} orders placed successfully.")

    except Exception as e:
        logger.exception("Error during initialization test")
        teddy_say(f"❌ Test failed: {e}")
        raise
