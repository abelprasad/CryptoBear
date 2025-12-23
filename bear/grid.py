class GridCalculator:
    """
    Calculate grid trading levels and position sizes
    """

    def __init__(self, spread: float, count: int, risk_per_trade: float):
        """
        Args:
            spread: Percentage per level (e.g., 0.005 for 0.5%)
            count: Total grid levels (e.g., 10 = 5 buy + 5 sell)
            risk_per_trade: Fraction of balance per order (e.g., 0.02 for 2%)
        """
        self.spread = spread
        self.levels_per_side = count // 2  # 5 for count=10
        self.risk_per_trade = risk_per_trade

    def calculate_grid_levels(self, current_price: float) -> dict:
        """
        Calculate buy and sell grid levels centered on current price

        Args:
            current_price: Current market price

        Returns:
            {
                'buy_levels': [(price, level_index), ...],  # level_index: -5 to -1
                'sell_levels': [(price, level_index), ...], # level_index: 1 to 5
                'center_price': float
            }
        """
        buy_levels = []
        sell_levels = []

        # Buy levels: below current price
        for i in range(1, self.levels_per_side + 1):
            price = current_price * (1 - i * self.spread)
            price = round(price, 2)  # 2 decimals for USD pairs
            buy_levels.append((price, -i))  # Negative index for buy levels

        # Sell levels: above current price
        for i in range(1, self.levels_per_side + 1):
            price = current_price * (1 + i * self.spread)
            price = round(price, 2)  # 2 decimals for USD pairs
            sell_levels.append((price, i))  # Positive index for sell levels

        return {
            'buy_levels': buy_levels,
            'sell_levels': sell_levels,
            'center_price': current_price
        }

    def calculate_position_size(self, balance: float, price: float) -> float:
        """
        Calculate quantity to buy/sell based on risk parameters

        Args:
            balance: Available account balance
            price: Order price

        Returns:
            Quantity rounded to 6 decimals for crypto precision
        """
        qty = (balance * self.risk_per_trade) / price
        return round(qty, 6)

    def get_counter_level(self, filled_price: float, side: str, grid_levels: dict) -> float:
        """
        Determine counter-order price for a filled order

        Args:
            filled_price: Price at which order was filled
            side: 'buy' or 'sell'
            grid_levels: Grid structure from calculate_grid_levels()

        Returns:
            Counter-order price (sell price if buy filled, buy price if sell filled)
        """
        if side == 'buy':
            # Buy filled -> place sell at next level up
            # Find the closest sell level above the filled price
            sell_levels = grid_levels['sell_levels']
            for price, _ in sell_levels:
                if price > filled_price:
                    return price
            # If no level found, use highest sell level
            return sell_levels[-1][0] if sell_levels else filled_price * (1 + self.spread)

        else:  # sell
            # Sell filled -> place buy at next level down
            # Find the closest buy level below the filled price
            buy_levels = grid_levels['buy_levels']
            for price, _ in reversed(buy_levels):
                if price < filled_price:
                    return price
            # If no level found, use lowest buy level
            return buy_levels[0][0] if buy_levels else filled_price * (1 - self.spread)
