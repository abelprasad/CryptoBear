import logging
import time
from datetime import datetime
from bear.alpaca_rest import AlpacaPaper
from bear.grid import GridCalculator
from bear.telegram import teddy_say


class GridTradingBot:
    """
    Grid trading bot that places orders in a grid pattern
    and manages fills by placing counter-orders
    """

    def __init__(self, config: dict):
        self.config = config
        self.api = AlpacaPaper()
        self.grid_calc = GridCalculator(
            spread=config['grid']['spread'],
            count=config['grid']['count'],
            risk_per_trade=config['risk']['per_trade']
        )
        self.logger = logging.getLogger('GridBot')

        # State tracking
        self.active_orders = {}  # {order_id: {'side', 'price', 'qty', 'level'}}
        self.inventory = 0.0  # Current crypto holdings
        self.buy_queue = []  # FIFO queue: [(price, qty, timestamp)]
        self.completed_cycles = []  # List of profit dicts
        self.grid_levels = None  # Grid structure
        self.pair = config['pair']

    def initialize(self):
        """
        Setup phase: calculate grid and place all initial orders
        """
        self.logger.info("Initializing grid trading bot...")

        # Get current market data
        current_price = self.api.get_price(self.pair)
        balance = self.api.get_balance()

        self.logger.info(f"Current price: ${current_price:,.2f}")
        self.logger.info(f"Account balance: ${balance:,.2f}")

        # Calculate grid levels
        self.grid_levels = self.grid_calc.calculate_grid_levels(current_price)

        # Calculate position size
        qty = self.grid_calc.calculate_position_size(balance, current_price)

        self.logger.info(f"Grid center: ${self.grid_levels['center_price']:,.2f}")
        self.logger.info(f"Position size: {qty} per order")

        # Place buy orders only (sell orders will be placed when buys fill)
        # This is required for crypto paper trading since you can't sell what you don't own
        for price, level in self.grid_levels['buy_levels']:
            self._place_initial_order('buy', qty, price, level)

        # Send notification
        buy_count = len([o for o in self.active_orders.values() if o['side'] == 'buy'])
        msg = f"""Grid initialized!
Price: ${current_price:,.2f}
Initial orders: {buy_count} BUY orders
Size: {qty} {self.pair} per order
Balance: ${balance:,.2f}

Sell orders will be placed as buys fill."""
        teddy_say(msg)

        self.logger.info(f"Grid initialized with {len(self.active_orders)} buy orders")
        self.logger.info("Sell orders will be placed when corresponding buys fill")

    def _place_initial_order(self, side: str, qty: float, price: float, level: int):
        """Place an order during initialization"""
        try:
            if side == 'buy':
                response = self.api.buy(self.pair, qty, price)
            else:
                response = self.api.sell(self.pair, qty, price)

            # Track order
            self.active_orders[response['id']] = {
                'side': side,
                'price': price,
                'qty': qty,
                'level': level
            }

            self.logger.info(f"Placed {side} order: {qty} @ ${price} (level {level})")

        except Exception as e:
            self.logger.error(f"Failed to place {side} order at ${price}: {e}")
            teddy_say(f"⚠️ Order failed: {side} {qty} @ ${price}")

    def run(self, poll_interval=10):
        """
        Main event loop: monitor orders and handle fills
        """
        self.logger.info(f"Starting main loop (polling every {poll_interval}s)")

        while True:
            try:
                # Check for filled orders
                filled_orders = self.check_orders()

                # Process each fill
                for order_data in filled_orders:
                    self.handle_fill(order_data)

                # Sleep
                time.sleep(poll_interval)

            except KeyboardInterrupt:
                self.logger.info("Received shutdown signal")
                break
            except Exception as e:
                self.logger.exception(f"Error in main loop: {e}")
                teddy_say(f"⚠️ Bot error: {e}")
                time.sleep(poll_interval)

    def check_orders(self):
        """
        Poll Alpaca for order updates and detect fills
        """
        filled_orders = []

        for order_id in list(self.active_orders.keys()):
            try:
                order_data = self.api.get_order(order_id)

                if order_data['status'] == 'filled':
                    # Add our tracking metadata
                    order_data['_tracked'] = self.active_orders[order_id]
                    filled_orders.append(order_data)

                    # Remove from active tracking
                    del self.active_orders[order_id]

            except Exception as e:
                self.logger.error(f"Error checking order {order_id}: {e}")

        return filled_orders

    def handle_fill(self, order_data: dict):
        """
        React to order fill: update inventory, place counter-order, track P&L
        """
        side = order_data['side']
        filled_price = float(order_data['filled_avg_price'])
        qty = float(order_data['filled_qty'])
        timestamp = datetime.now()

        self.logger.info(f"{side.upper()} order filled: {qty} @ ${filled_price:,.2f}")

        # Update inventory
        if side == 'buy':
            self.inventory += qty
            self.buy_queue.append((filled_price, qty, timestamp))
            counter_side = 'sell'
        else:  # sell
            self.inventory -= qty
            counter_side = 'buy'

            # Match sell to buy for P&L tracking
            if self.buy_queue:
                profit = self._match_sell_to_buy(filled_price, qty)
                if profit > 0:
                    self._send_profit_report(profit, filled_price, qty)

        # Determine counter-order price
        counter_price = self.grid_calc.get_counter_level(
            filled_price, side, self.grid_levels
        )

        # Place counter-order
        self.place_order(counter_side, qty, counter_price)

        # Send fill notification
        msg = f"""{"🟢" if side == 'buy' else "🔴"} Order Filled!
Side: {side.upper()}
Price: ${filled_price:,.2f}
Qty: {qty}
Total: ${filled_price * qty:,.2f}
Inventory: {self.inventory:.6f} {self.pair}"""
        teddy_say(msg)

    def place_order(self, side: str, qty: float, price: float):
        """
        Place a new order and add to tracking
        """
        try:
            if side == 'buy':
                response = self.api.buy(self.pair, qty, price)
            else:
                response = self.api.sell(self.pair, qty, price)

            # Track order
            self.active_orders[response['id']] = {
                'side': side,
                'price': price,
                'qty': qty,
                'level': None  # Counter-orders don't have grid levels
            }

            self.logger.info(f"Placed {side} order: {qty} @ ${price:,.2f}")

        except Exception as e:
            self.logger.error(f"Failed to place {side} order: {e}")
            teddy_say(f"⚠️ Order failed: {side} {qty} @ ${price}")

    def _match_sell_to_buy(self, sell_price: float, sell_qty: float) -> float:
        """
        Match sell to oldest buy(s) using FIFO and calculate profit
        """
        remaining_qty = sell_qty
        total_profit = 0.0

        while remaining_qty > 0 and self.buy_queue:
            buy_price, buy_qty, buy_time = self.buy_queue[0]
            matched_qty = min(remaining_qty, buy_qty)

            # Calculate profit
            profit = (sell_price - buy_price) * matched_qty
            total_profit += profit

            self.logger.info(
                f"Matched: Buy ${buy_price:,.2f} -> Sell ${sell_price:,.2f}, "
                f"Qty: {matched_qty:.6f}, Profit: ${profit:.2f}"
            )

            # Update queue
            if matched_qty == buy_qty:
                self.buy_queue.pop(0)  # Fully matched, remove
            else:
                # Partial match, update quantity
                self.buy_queue[0] = (buy_price, buy_qty - matched_qty, buy_time)

            remaining_qty -= matched_qty

        # Store completed cycle
        if total_profit > 0:
            self.completed_cycles.append({
                'profit': total_profit,
                'sell_price': sell_price,
                'qty': sell_qty - remaining_qty,
                'timestamp': datetime.now()
            })

        return total_profit

    def _send_profit_report(self, profit: float, sell_price: float, qty: float):
        """Send Telegram notification for completed profit cycle"""
        total_cycles = len(self.completed_cycles)
        total_profit = sum(c['profit'] for c in self.completed_cycles)

        msg = f"""✅ Profit Cycle Complete!
Sell Price: ${sell_price:,.2f}
Qty: {qty:.6f}
Profit: ${profit:.2f}

Total Cycles: {total_cycles}
Total Profit: ${total_profit:.2f}"""
        teddy_say(msg)
