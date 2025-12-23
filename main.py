from bear import config
from bear.logger import setup_logger
from bear.trader import GridTradingBot
from bear.telegram import teddy_say
import signal
import sys


def signal_handler(sig, frame):
    """Graceful shutdown on Ctrl+C"""
    teddy_say("🛑 Grid bot shutting down...")
    sys.exit(0)


if __name__ == '__main__':
    # Setup logging
    logger = setup_logger(level=config['logging']['level'])
    signal.signal(signal.SIGINT, signal_handler)

    # Initialize bot
    bot = GridTradingBot(config)

    try:
        teddy_say("🚀 Grid bot starting...")
        logger.info("CryptoBear Grid Trading Bot")
        logger.info("=" * 50)

        # Initialize grid and place orders
        bot.initialize()

        # Start main monitoring loop
        bot.run(poll_interval=10)

    except Exception as e:
        logger.exception("Fatal error in main loop")
        teddy_say(f"💥 Bot crashed: {e}")
        sys.exit(1)