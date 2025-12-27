# CryptoBear Grid Trading Bot - Complete Documentation

## Table of Contents
1. [Overview](#overview)
2. [Grid Trading Strategy](#grid-trading-strategy)
3. [Architecture](#architecture)
4. [File-by-File Explanation](#file-by-file-explanation)
5. [Complete Code Walkthrough](#complete-code-walkthrough)
6. [How Everything Works Together](#how-everything-works-together)
7. [Examples and Scenarios](#examples-and-scenarios)

---

## Overview

CryptoBear is an **automated grid trading bot** that trades cryptocurrency (BTC/USD) on Alpaca's paper trading platform. It uses a **grid strategy** to profit from price volatility by placing buy and sell orders at predetermined price levels.

### What the Bot Does
1. **Calculates a price grid** - Creates buy/sell levels spaced 0.5% apart
2. **Places initial buy orders** - 5 orders below current market price
3. **Monitors continuously** - Checks order status every 10 seconds
4. **Places counter-orders** - When buy fills → place sell; when sell fills → place buy
5. **Tracks profits** - Matches buy/sell pairs and calculates realized P&L
6. **Sends notifications** - Reports all activity via Telegram

---

## Grid Trading Strategy

### What is Grid Trading?

Grid trading is a strategy that profits from price oscillation within a range. Instead of predicting price direction, you:
- Place **BUY orders** at intervals below current price
- When they fill, place **SELL orders** above the buy price
- Capture profit from each price swing

### Visual Example

```
Price Range: $85,000 - $89,000 (centered at $87,000)

$89,000  |           SELL #5 (when corresponding buy fills)
         |
$88,500  |           SELL #4
         |
$88,000  |           SELL #3
         |
$87,500  |           SELL #2
         |
$87,435  |           SELL #1 ← Counter-order placed after buy fills
─────────|──────────────────────────────
$87,000  |  ← Current Market Price
─────────|──────────────────────────────
$86,565  |  BUY #1  ← Active order (0.5% below current)
         |
$86,130  |  BUY #2  ← Active order (1.0% below)
         |
$85,695  |  BUY #3  ← Active order (1.5% below)
         |
$85,260  |  BUY #4  ← Active order (2.0% below)
         |
$84,825  |  BUY #5  ← Active order (2.5% below)
```

### How Profits are Made

**Scenario:**
1. BTC price drops to **$86,565** → BUY order fills (buy 0.02 BTC)
2. Bot places SELL order at **$87,435** (0.5% above buy price)
3. BTC price rises to **$87,435** → SELL order fills (sell 0.02 BTC)
4. **Profit = ($87,435 - $86,565) × 0.02 BTC = $17.40**

The bot repeats this for every price swing, accumulating profits over time.

---

## Architecture

### Project Structure

```
CryptoBear/
├── bear/                      # Main package
│   ├── __init__.py           # Config loader & utilities
│   ├── alpaca_rest.py        # Alpaca API client
│   ├── telegram.py           # Telegram notifications
│   ├── grid.py               # Grid calculation logic
│   ├── logger.py             # Logging setup
│   └── trader.py             # Main bot orchestration
│
├── config/
│   └── settings.yaml         # Configuration file
│
├── logs/                     # Runtime logs (auto-created)
│   └── grid_bot_YYYYMMDD.log
│
├── .env                      # API keys (NOT in git)
├── main.py                   # Entry point
├── test_grid_init.py         # Test initialization
├── test_integration.py       # Test Alpaca + Telegram
├── check_orders.py           # View current orders
├── check_profits.py          # View profit history
├── check_price.py            # View market price
└── show_activity.py          # View bot activity log
```

### System Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                             │
│                    (Entry Point)                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ 1. Setup logger
                       │ 2. Initialize GridTradingBot
                       │ 3. Call bot.initialize()
                       │ 4. Call bot.run()
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   GridTradingBot                            │
│                   (trader.py)                               │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ initialize()                                        │  │
│  │  1. Get market price via AlpacaPaper                │  │
│  │  2. Calculate grid via GridCalculator               │  │
│  │  3. Place 5 buy orders                              │  │
│  │  4. Send Telegram notification                      │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ run() - Main Event Loop                            │  │
│  │  while True:                                        │  │
│  │    1. check_orders() → detect fills                 │  │
│  │    2. handle_fill() → place counter-orders          │  │
│  │    3. sleep(10 seconds)                             │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                       │
                       │ Uses:
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌──────────────┐ ┌──────────┐ ┌───────────────┐
│GridCalculator│ │AlpacaPaper│ │teddy_say()    │
│(grid.py)     │ │(alpaca_   │ │(telegram.py)  │
│              │ │rest.py)   │ │               │
│- Calculate   │ │           │ │- Send messages│
│  grid levels │ │- API calls│ │  to Telegram  │
│- Position    │ │  to Alpaca│ │               │
│  sizing      │ │- Get price│ │               │
│- Counter     │ │- Get orders│ │              │
│  order logic │ │- Place buy│ │               │
│              │ │- Place sell│ │              │
└──────────────┘ └──────────┘ └───────────────┘
```

---

## File-by-File Explanation

### 1. `config/settings.yaml`

**Purpose:** Central configuration file for all bot parameters

```yaml
exchange: alpaca          # Trading platform
pair: BTCUSD             # Trading pair (no dash)
sandbox: true            # Paper trading mode

grid:
  spread: 0.005          # 0.5% spacing between grid levels
  count: 10              # Total levels (5 buy + 5 sell)

risk:
  per_trade: 0.02        # 2% of balance per order

logging:
  level: INFO            # Log verbosity (DEBUG|INFO|WARNING)
```

**How it's used:**
- Loaded in `bear/__init__.py`
- Accessed throughout the bot as `config['grid']['spread']`, etc.

---

### 2. `.env`

**Purpose:** Store sensitive API credentials (NOT committed to git)

```bash
ALPACA_API_KEY=PK...your_key_id
ALPACA_API_SECRET=...your_secret
ALPACA_SANDBOX=true
TELEGRAM_TOKEN=8535783092:AAE...
TELEGRAM_CHAT_ID=5623951548
```

**How it's used:**
- Loaded by `python-dotenv` library
- Accessed via `os.getenv('ALPACA_API_KEY')`

---

### 3. `bear/__init__.py`

**Purpose:** Package initialization - loads config and provides utilities

```python
# bear/__init__.py
import yaml, os
from pathlib import Path
from datetime import datetime

# Load configuration from YAML file
_CONFIG_PATH = Path(__file__).parent.parent / "config" / "settings.yaml"
config = yaml.safe_load(_CONFIG_PATH.read_text())

# Utility function for timestamped messages
def tick():
    return f"🧸 CryptoBear tick {datetime.now():%X}"
```

**What this does:**
1. `Path(__file__).parent.parent` → Goes up two directories from `bear/__init__.py` to project root
2. Finds `config/settings.yaml`
3. Loads YAML into `config` dictionary
4. Exports `config` for use anywhere via `from bear import config`
5. Provides `tick()` helper for timestamped logs

---

### 4. `bear/logger.py`

**Purpose:** Centralized logging setup with file rotation and console output

```python
import logging
import sys
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

def setup_logger(name='CryptoBear', level='INFO'):
    """
    Configure logging with both file and console handlers

    Returns a logger that:
    - Writes to logs/grid_bot_YYYYMMDD.log (rotates daily)
    - Outputs to console with same format
    - Keeps 30 days of log files
    """

    # Create logger instance
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Prevent duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    # Create logs directory if it doesn't exist
    logs_dir = Path(__file__).parent.parent / 'logs'
    logs_dir.mkdir(exist_ok=True)

    # FILE HANDLER - writes to rotating log file
    log_file = logs_dir / f"grid_bot_{datetime.now():%Y%m%d}.log"
    file_handler = TimedRotatingFileHandler(
        log_file,           # File path
        when='midnight',    # Rotate at midnight
        interval=1,         # Every 1 day
        backupCount=30      # Keep 30 days
    )
    file_handler.setLevel(logging.DEBUG)  # Log everything to file

    # CONSOLE HANDLER - writes to stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))

    # FORMAT - how log messages look
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Apply formatter to both handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
```

**Key Concepts:**

1. **Logger vs Handler vs Formatter**
   - **Logger:** The main logging object you call (`logger.info()`)
   - **Handler:** Where logs go (file, console, network, etc.)
   - **Formatter:** How logs look (timestamp, level, message)

2. **TimedRotatingFileHandler**
   - Creates new file at midnight each day
   - Old files renamed with date suffix: `grid_bot_20251223.log.2025-12-24`
   - Automatically deletes files older than 30 days

3. **Log Levels**
   - DEBUG: Detailed diagnostic info
   - INFO: General informational messages
   - WARNING: Something unexpected but not critical
   - ERROR: Serious problem occurred
   - CRITICAL: Very serious error, program may crash

**Example Usage:**
```python
from bear.logger import setup_logger

logger = setup_logger(level='INFO')
logger.info("Bot started")           # Shows in console + file
logger.debug("Checking order X")     # Only in file (below INFO)
logger.error("API call failed")      # Shows in console + file
```

**Output:**
```
2025-12-23 14:05:17 | INFO     | CryptoBear | Bot started
2025-12-23 14:05:18 | ERROR    | CryptoBear | API call failed
```

---

### 5. `bear/telegram.py`

**Purpose:** Send notifications to Telegram

```python
import os, requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment
TOKEN   = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def teddy_say(text):
    """
    Send a message to Telegram with teddy bear emoji

    Args:
        text: Message to send

    Returns:
        True if sent successfully, False otherwise
    """
    # Construct Telegram Bot API URL
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    # Prepare message payload
    payload = {
        'chat_id': CHAT_ID,
        'text': f"🧸 {text}"  # Prepend teddy emoji
    }

    try:
        # Send POST request to Telegram API
        r = requests.post(url, json=payload, timeout=5)
        r.raise_for_status()  # Raise exception if status is 4xx/5xx
        return True
    except Exception as e:
        # Print error but don't crash the bot
        print(f"Telegram error: {e}")
        return False
```

**How Telegram Bot API Works:**

1. **Create a bot:**
   - Message @BotFather on Telegram
   - `/newbot` command
   - Get TOKEN like `8535783092:AAEg9XqTmRTqIYHpLTDAtjGV-rfGji464_I`

2. **Get your CHAT_ID:**
   - Message your bot
   - Visit `https://api.telegram.org/bot<TOKEN>/getUpdates`
   - Find `"chat":{"id":5623951548}` in JSON response

3. **Send messages:**
   - POST to `https://api.telegram.org/bot<TOKEN>/sendMessage`
   - Include `chat_id` and `text` in JSON body

**Example Usage:**
```python
from bear.telegram import teddy_say

teddy_say("Grid initialized!")
# Sends: "🧸 Grid initialized!" to your Telegram
```

---

### 6. `bear/alpaca_rest.py`

**Purpose:** REST API client for Alpaca trading platform

```python
import os, requests
from dotenv import load_dotenv
load_dotenv()

class AlpacaPaper:
    """
    Alpaca Paper Trading API Client

    Handles all communication with Alpaca's REST API for:
    - Getting market prices
    - Placing orders
    - Checking order status
    - Account information
    """

    def __init__(self):
        """Initialize API client with credentials"""
        # Load API credentials from environment
        self.key    = os.getenv('ALPACA_API_KEY')
        self.secret = os.getenv('ALPACA_API_SECRET')

        # API base URL for paper trading
        self.base   = 'https://paper-api.alpaca.markets'

        # Create persistent session with authentication headers
        self.session = requests.Session()
        self.session.headers.update({
            'APCA-API-KEY-ID':  self.key,
            'APCA-API-SECRET-KEY': self.secret
        })

    # ========== HELPER METHODS ==========

    def _norm(self, symbol):
        """
        Normalize symbol format for crypto API

        Args:
            symbol: Trading pair like "BTCUSD"

        Returns:
            "BTC/USD" format for crypto API

        Example:
            _norm("BTCUSD") → "BTC/USD"
            _norm("ETHUSD") → "ETH/USD"
        """
        if len(symbol) == 6:  # e.g., BTCUSD
            return f"{symbol[:3]}/{symbol[3:]}"
        return symbol  # Already formatted

    # ========== MARKET DATA ==========

    def get_price(self, symbol):
        """
        Get current market price for crypto pair

        Args:
            symbol: Trading pair (e.g., "BTCUSD")

        Returns:
            Current bid price as float

        Example:
            api.get_price("BTCUSD") → 87500.25
        """
        # Note: Crypto data uses different base URL!
        url = f"https://data.alpaca.markets/v1beta3/crypto/us/latest/quotes"
        params = {"symbols": self._norm(symbol)}

        r = self.session.get(url, params=params)
        r.raise_for_status()  # Throw error if request failed

        data = r.json()
        symbol_key = self._norm(symbol)

        # Extract bid price from response
        # Response format: {"quotes": {"BTC/USD": {"bp": 87500.25, ...}}}
        return float(data['quotes'][symbol_key]['bp'])

    # ========== ACCOUNT INFO ==========

    def get_balance(self):
        """
        Get available cash balance in account

        Returns:
            Cash balance as float

        Example:
            api.get_balance() → 100000.0
        """
        url = f"{self.base}/v2/account"

        r = self.session.get(url)
        r.raise_for_status()

        # Response format: {"cash": "100000.0", "buying_power": ..., ...}
        return float(r.json()['cash'])

    # ========== ORDER PLACEMENT ==========

    def buy(self, symbol, qty, price):
        """
        Place a limit BUY order

        Args:
            symbol: Trading pair (e.g., "BTCUSD")
            qty: Quantity to buy (e.g., 0.02)
            price: Limit price (e.g., 87000.00)

        Returns:
            Order confirmation dict with 'id', 'status', etc.

        Example:
            api.buy("BTCUSD", 0.02, 87000.00)
            → {"id": "abc123", "status": "new", ...}
        """
        url = f"{self.base}/v2/orders"

        data = {
            "symbol":      self._norm(symbol),  # "BTC/USD"
            "qty":         str(qty),            # "0.02"
            "side":        "buy",
            "type":        "limit",             # Not market order
            "limit_price": str(price),          # "87000.00"
            "time_in_force": "gtc"              # Good Till Canceled
        }

        r = self.session.post(url, json=data)
        r.raise_for_status()

        return r.json()  # Order details

    def sell(self, symbol, qty, price):
        """
        Place a limit SELL order

        Args:
            symbol: Trading pair (e.g., "BTCUSD")
            qty: Quantity to sell (e.g., 0.02)
            price: Limit price (e.g., 88000.00)

        Returns:
            Order confirmation dict
        """
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

    # ========== ORDER MANAGEMENT ==========

    def get_orders(self, status='open', limit=500):
        """
        Get list of orders by status

        Args:
            status: 'open', 'closed', or 'all'
            limit: Max number of orders to return

        Returns:
            List of order dicts

        Example:
            orders = api.get_orders('open')
            → [{"id": "abc", "side": "buy", ...}, ...]
        """
        url = f"{self.base}/v2/orders"
        params = {'status': status, 'limit': limit}

        r = self.session.get(url, params=params)
        r.raise_for_status()

        return r.json()  # List of orders

    def get_order(self, order_id):
        """
        Get single order by ID

        Args:
            order_id: Order ID string

        Returns:
            Order dict with current status

        Example:
            order = api.get_order("abc123")
            → {"id": "abc123", "status": "filled", ...}
        """
        url = f"{self.base}/v2/orders/{order_id}"

        r = self.session.get(url)
        r.raise_for_status()

        return r.json()

    def cancel_order(self, order_id):
        """
        Cancel a specific order

        Args:
            order_id: Order ID to cancel

        Returns:
            Cancellation confirmation
        """
        url = f"{self.base}/v2/orders/{order_id}"

        r = self.session.delete(url)
        r.raise_for_status()

        return r.json()

    def cancel_all_orders(self):
        """
        Cancel all open orders (emergency stop)

        Returns:
            List of canceled order IDs
        """
        url = f"{self.base}/v2/orders"

        r = self.session.delete(url)
        r.raise_for_status()

        return r.json()
```

**Key Concepts:**

1. **requests.Session()**
   - Reuses TCP connection for multiple requests (faster)
   - Automatically includes headers in all requests
   - Here: API key headers added once, used for all calls

2. **raise_for_status()**
   - Checks if HTTP status is 200-299 (success)
   - Throws exception if 400-599 (error)
   - Prevents silent failures

3. **Limit Orders vs Market Orders**
   - **Market:** Buy/sell immediately at current price (can be unpredictable)
   - **Limit:** Only execute at specified price or better (we use this)
   - Example: Limit buy @ $87,000 only fills if price drops to $87,000 or below

4. **GTC (Good Till Canceled)**
   - Order stays active until filled or manually canceled
   - Alternative: Day orders (canceled at market close)

---

### 7. `bear/grid.py`

**Purpose:** Pure calculation logic for grid trading levels

```python
class GridCalculator:
    """
    Calculate grid trading levels and position sizes

    This is a "pure" class - no side effects, just math.
    Given inputs, produces outputs. Easy to test.
    """

    def __init__(self, spread: float, count: int, risk_per_trade: float):
        """
        Initialize calculator with strategy parameters

        Args:
            spread: Percentage spacing between levels (0.005 = 0.5%)
            count: Total grid levels (10 = 5 buy + 5 sell)
            risk_per_trade: Fraction of balance per order (0.02 = 2%)

        Example:
            calc = GridCalculator(
                spread=0.005,        # 0.5% spacing
                count=10,            # 10 levels total
                risk_per_trade=0.02  # 2% position size
            )
        """
        self.spread = spread
        self.levels_per_side = count // 2  # 10 // 2 = 5
        self.risk_per_trade = risk_per_trade

    def calculate_grid_levels(self, current_price: float) -> dict:
        """
        Calculate buy and sell grid levels centered on current price

        Args:
            current_price: Current market price (e.g., 87000.00)

        Returns:
            Dictionary with:
                'buy_levels': [(price, level_index), ...]
                'sell_levels': [(price, level_index), ...]
                'center_price': current_price

        Example:
            levels = calc.calculate_grid_levels(87000.00)

            Result:
            {
                'buy_levels': [
                    (86565.00, -1),  # 87000 * (1 - 0.005*1)
                    (86130.00, -2),  # 87000 * (1 - 0.005*2)
                    (85695.00, -3),
                    (85260.00, -4),
                    (84825.00, -5)
                ],
                'sell_levels': [
                    (87435.00, 1),   # 87000 * (1 + 0.005*1)
                    (87870.00, 2),   # 87000 * (1 + 0.005*2)
                    (88305.00, 3),
                    (88740.00, 4),
                    (89175.00, 5)
                ],
                'center_price': 87000.00
            }
        """
        buy_levels = []
        sell_levels = []

        # Calculate buy levels (below current price)
        for i in range(1, self.levels_per_side + 1):
            # Formula: price * (1 - i * spread)
            # Example: 87000 * (1 - 1*0.005) = 86565
            price = current_price * (1 - i * self.spread)
            price = round(price, 2)  # Round to 2 decimals for USD

            # Store as (price, level_index)
            # Level index is negative for buys: -1, -2, -3, etc.
            buy_levels.append((price, -i))

        # Calculate sell levels (above current price)
        for i in range(1, self.levels_per_side + 1):
            # Formula: price * (1 + i * spread)
            # Example: 87000 * (1 + 1*0.005) = 87435
            price = current_price * (1 + i * self.spread)
            price = round(price, 2)

            # Level index is positive for sells: 1, 2, 3, etc.
            sell_levels.append((price, i))

        return {
            'buy_levels': buy_levels,
            'sell_levels': sell_levels,
            'center_price': current_price
        }

    def calculate_position_size(self, balance: float, price: float) -> float:
        """
        Calculate how much to buy/sell based on risk parameters

        Args:
            balance: Available account balance (e.g., 100000.00)
            price: Order price (e.g., 87000.00)

        Returns:
            Quantity to trade, rounded to 6 decimals

        Example:
            qty = calc.calculate_position_size(100000.00, 87000.00)

            Calculation:
            - Risk per trade = 2% of 100000 = 2000
            - Quantity = 2000 / 87000 = 0.022988

            Result: 0.022988 BTC

        Why 6 decimals?
            Bitcoin can be divided into 100,000,000 units (satoshis)
            For trading, 6 decimals is standard precision
        """
        # Calculate dollar amount to invest
        dollar_amount = balance * self.risk_per_trade

        # Convert to crypto quantity
        qty = dollar_amount / price

        # Round to 6 decimals
        return round(qty, 6)

    def get_counter_level(self, filled_price: float, side: str,
                          grid_levels: dict) -> float:
        """
        Determine counter-order price for a filled order

        This is the core grid logic: when a buy fills, where should
        we place the sell? When a sell fills, where's the buy?

        Args:
            filled_price: Price at which order filled
            side: 'buy' or 'sell'
            grid_levels: Grid structure from calculate_grid_levels()

        Returns:
            Price for counter-order

        Example 1: Buy filled
            filled_price = 86565.00
            side = 'buy'
            grid_levels = {
                'sell_levels': [(87435, 1), (87870, 2), ...]
            }

            Result: 87435.00
            (First sell level above the buy price)

        Example 2: Sell filled
            filled_price = 87435.00
            side = 'sell'
            grid_levels = {
                'buy_levels': [(86565, -1), (86130, -2), ...]
            }

            Result: 86565.00
            (First buy level below the sell price)
        """
        if side == 'buy':
            # Buy filled -> place sell at next level up
            sell_levels = grid_levels['sell_levels']

            # Find first sell level above filled price
            for price, _ in sell_levels:
                if price > filled_price:
                    return price

            # Fallback: use highest sell level
            # (shouldn't happen in normal operation)
            if sell_levels:
                return sell_levels[-1][0]
            else:
                # Emergency fallback: calculate on the fly
                return filled_price * (1 + self.spread)

        else:  # side == 'sell'
            # Sell filled -> place buy at next level down
            buy_levels = grid_levels['buy_levels']

            # Find first buy level below filled price
            # Note: reversed() because buy_levels are sorted low to high
            for price, _ in reversed(buy_levels):
                if price < filled_price:
                    return price

            # Fallback: use lowest buy level
            if buy_levels:
                return buy_levels[0][0]
            else:
                # Emergency fallback
                return filled_price * (1 - self.spread)
```

**Why This Design?**

1. **Separation of Concerns**
   - `GridCalculator` only does math
   - Doesn't know about Alpaca, Telegram, or logging
   - Easy to test: give inputs, check outputs
   - Can be reused for different exchanges

2. **Level Indexing System**
   - Buy levels: -5, -4, -3, -2, -1
   - Center: 0 (current price, no order)
   - Sell levels: +1, +2, +3, +4, +5
   - Helps track which "tier" an order belongs to

---

### 8. `bear/trader.py` (Part 1 of 3)

**Purpose:** Main bot orchestration - initialization and state management

```python
import logging
import time
from datetime import datetime
from bear.alpaca_rest import AlpacaPaper
from bear.grid import GridCalculator
from bear.telegram import teddy_say

class GridTradingBot:
    """
    Main grid trading bot orchestration

    Responsibilities:
    1. Initialize grid and place orders
    2. Monitor order status continuously
    3. Handle fills by placing counter-orders
    4. Track profits from completed cycles
    5. Log all activity
    6. Send Telegram notifications
    """

    def __init__(self, config: dict):
        """
        Initialize bot with configuration

        Args:
            config: Configuration dict from settings.yaml
                {
                    'pair': 'BTCUSD',
                    'grid': {'spread': 0.005, 'count': 10},
                    'risk': {'per_trade': 0.02}
                }
        """
        self.config = config

        # Initialize API client
        self.api = AlpacaPaper()

        # Initialize grid calculator with strategy params
        self.grid_calc = GridCalculator(
            spread=config['grid']['spread'],        # 0.005
            count=config['grid']['count'],          # 10
            risk_per_trade=config['risk']['per_trade']  # 0.02
        )

        # Setup logging
        self.logger = logging.getLogger('GridBot')

        # STATE TRACKING
        # This is the "memory" of the bot

        # Active orders: {order_id: order_metadata}
        # Example: {
        #   "abc123": {
        #     'side': 'buy',
        #     'price': 86565.00,
        #     'qty': 0.022988,
        #     'level': -1
        #   }
        # }
        self.active_orders = {}

        # Current inventory (how much BTC we're holding)
        # Updated when buys/sells fill
        self.inventory = 0.0

        # FIFO queue of buys waiting to be matched with sells
        # Format: [(buy_price, qty, timestamp), ...]
        # Example: [(86565.00, 0.02, datetime(...)), ...]
        self.buy_queue = []

        # Completed profit cycles
        # Format: [{'profit': 17.40, 'buy_price': ..., ...}, ...]
        self.completed_cycles = []

        # Grid structure (calculated during initialization)
        self.grid_levels = None

        # Trading pair
        self.pair = config['pair']
```

**State Management Explained:**

The bot needs to remember:
1. **active_orders**: Which orders are we waiting on?
2. **inventory**: How much BTC do we currently hold?
3. **buy_queue**: Which buys haven't been matched to sells yet?
4. **completed_cycles**: What profits have we realized?
5. **grid_levels**: What's our current grid structure?

This is like a human trader's notebook where they track all their positions.

---

### 8. `bear/trader.py` (Part 2 of 3)

**Purpose:** Initialization and order placement

```python
    def initialize(self):
        """
        Setup phase: calculate grid and place all initial orders

        This runs once when the bot starts:
        1. Get current market data (price, balance)
        2. Calculate grid levels
        3. Place initial buy orders
        4. Send Telegram notification
        """
        self.logger.info("Initializing grid trading bot...")

        # Step 1: Get current market data
        current_price = self.api.get_price(self.pair)
        balance = self.api.get_balance()

        self.logger.info(f"Current price: ${current_price:,.2f}")
        self.logger.info(f"Account balance: ${balance:,.2f}")

        # Step 2: Calculate grid levels
        # This creates the price ladder we'll trade on
        self.grid_levels = self.grid_calc.calculate_grid_levels(current_price)

        # Step 3: Calculate position size
        # All orders will be the same size
        qty = self.grid_calc.calculate_position_size(balance, current_price)

        self.logger.info(f"Grid center: ${self.grid_levels['center_price']:,.2f}")
        self.logger.info(f"Position size: {qty} per order")

        # Step 4: Place buy orders only
        # Note: We don't place sell orders initially because on Alpaca
        # paper trading, you can't sell crypto you don't own.
        # Sells will be placed when corresponding buys fill.

        for price, level in self.grid_levels['buy_levels']:
            self._place_initial_order('buy', qty, price, level)

        # Step 5: Send Telegram notification
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
        """
        Place an order during initialization

        Args:
            side: 'buy' or 'sell'
            qty: Quantity to trade
            price: Limit price
            level: Grid level index (-5 to +5)

        This is separated from place_order() because it:
        - Runs during initialization
        - Includes grid level tracking
        - Has different error handling
        """
        try:
            # Call Alpaca API
            if side == 'buy':
                response = self.api.buy(self.pair, qty, price)
            else:
                response = self.api.sell(self.pair, qty, price)

            # Track order in our state
            # response['id'] is the order ID from Alpaca
            self.active_orders[response['id']] = {
                'side': side,
                'price': price,
                'qty': qty,
                'level': level
            }

            self.logger.info(
                f"Placed {side} order: {qty} @ ${price} (level {level})"
            )

        except Exception as e:
            # If order fails during init, log but don't crash
            self.logger.error(f"Failed to place {side} order at ${price}: {e}")
            teddy_say(f"⚠️ Order failed: {side} {qty} @ ${price}")
```

**Initialization Flow:**

```
initialize()
    ↓
1. Get market data
   - Current BTC price: $87,000
   - Account balance: $100,000
    ↓
2. Calculate grid
   - Buy levels: $86,565, $86,130, $85,695, $85,260, $84,825
   - Sell levels: $87,435, $87,870, $88,305, $88,740, $89,175
    ↓
3. Calculate position size
   - 2% of $100,000 = $2,000 per order
   - $2,000 / $87,000 = 0.022988 BTC
    ↓
4. Place 5 buy orders
   - BUY 0.022988 @ $86,565 (level -1)
   - BUY 0.022988 @ $86,130 (level -2)
   - BUY 0.022988 @ $85,695 (level -3)
   - BUY 0.022988 @ $85,260 (level -4)
   - BUY 0.022988 @ $84,825 (level -5)
    ↓
5. Send Telegram notification
   - "Grid initialized! 5 BUY orders placed"
```

---

### 8. `bear/trader.py` (Part 3 of 3)

**Purpose:** Main event loop and order handling

```python
    def run(self, poll_interval=10):
        """
        Main event loop: monitor orders and handle fills

        Args:
            poll_interval: Seconds between order checks (default 10)

        This loop runs forever (until Ctrl+C):
        1. Check all active orders for fills
        2. Handle any fills found
        3. Sleep for poll_interval
        4. Repeat
        """
        self.logger.info(f"Starting main loop (polling every {poll_interval}s)")

        while True:
            try:
                # Check for filled orders
                filled_orders = self.check_orders()

                # Process each fill
                for order_data in filled_orders:
                    self.handle_fill(order_data)

                # Sleep before next check
                time.sleep(poll_interval)

            except KeyboardInterrupt:
                # User pressed Ctrl+C
                self.logger.info("Received shutdown signal")
                break

            except Exception as e:
                # Unexpected error - log but keep running
                self.logger.exception(f"Error in main loop: {e}")
                teddy_say(f"⚠️ Bot error: {e}")
                time.sleep(poll_interval)  # Wait before retrying

    def check_orders(self):
        """
        Poll Alpaca for order updates and detect fills

        Returns:
            List of filled order data dicts

        How it works:
        1. Loop through all active order IDs we're tracking
        2. Ask Alpaca for current status of each order
        3. If status is 'filled', add to results
        4. Remove filled orders from active tracking
        """
        filled_orders = []

        # Use list() to create a copy of keys, so we can modify
        # the dict while iterating
        for order_id in list(self.active_orders.keys()):
            try:
                # Ask Alpaca: what's the status of this order?
                order_data = self.api.get_order(order_id)

                # Check if order filled
                if order_data['status'] == 'filled':
                    # Attach our tracking metadata
                    order_data['_tracked'] = self.active_orders[order_id]

                    # Add to results
                    filled_orders.append(order_data)

                    # Remove from active tracking
                    # (we don't need to check this order anymore)
                    del self.active_orders[order_id]

            except Exception as e:
                # API error - log but continue checking other orders
                self.logger.error(f"Error checking order {order_id}: {e}")

        return filled_orders

    def handle_fill(self, order_data: dict):
        """
        React to order fill: update inventory, place counter-order, track P&L

        Args:
            order_data: Order dict from Alpaca with fill details
                {
                    'side': 'buy',
                    'filled_avg_price': '86565.00',
                    'filled_qty': '0.022988',
                    ...
                }

        This is the heart of the grid trading logic:
        1. Extract fill details
        2. Update inventory
        3. Match for P&L tracking
        4. Calculate counter-order price
        5. Place counter-order
        6. Send Telegram notification
        """
        # Extract fill details
        side = order_data['side']
        filled_price = float(order_data['filled_avg_price'])
        qty = float(order_data['filled_qty'])
        timestamp = datetime.now()

        self.logger.info(
            f"{side.upper()} order filled: {qty} @ ${filled_price:,.2f}"
        )

        # Update inventory
        if side == 'buy':
            # We bought BTC -> increase inventory
            self.inventory += qty

            # Add to buy queue for future profit matching
            self.buy_queue.append((filled_price, qty, timestamp))

            # Counter-order will be a sell
            counter_side = 'sell'

        else:  # side == 'sell'
            # We sold BTC -> decrease inventory
            self.inventory -= qty

            # Counter-order will be a buy
            counter_side = 'buy'

            # Match this sell to a previous buy for P&L
            if self.buy_queue:
                profit = self._match_sell_to_buy(filled_price, qty)
                if profit > 0:
                    self._send_profit_report(profit, filled_price, qty)

        # Determine counter-order price
        # If buy filled at $86,565 -> sell at $87,435
        # If sell filled at $87,435 -> buy at $86,565
        counter_price = self.grid_calc.get_counter_level(
            filled_price, side, self.grid_levels
        )

        # Place counter-order
        self.place_order(counter_side, qty, counter_price)

        # Send Telegram notification
        msg = f"""{"🟢" if side == 'buy' else "🔴"} Order Filled!
Side: {side.upper()}
Price: ${filled_price:,.2f}
Qty: {qty}
Total: ${filled_price * qty:,.2f}
Inventory: {self.inventory:.6f} {self.pair}"""

        teddy_say(msg)

    def place_order(self, side: str, qty: float, price: float):
        """
        Place a new order (during runtime, not initialization)

        Args:
            side: 'buy' or 'sell'
            qty: Quantity to trade
            price: Limit price

        This is called when placing counter-orders after fills.
        Different from _place_initial_order because:
        - No grid level tracking (counter-orders are dynamic)
        - Used during runtime
        """
        try:
            # Call Alpaca API
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

        Args:
            sell_price: Price at which we sold
            sell_qty: Quantity sold

        Returns:
            Total realized profit

        Example:
            buy_queue = [
                (86565.00, 0.02, datetime(...)),  # Oldest
                (86130.00, 0.01, datetime(...))
            ]

            _match_sell_to_buy(87435.00, 0.02)

            Logic:
            - Match sell of 0.02 to first buy of 0.02
            - Profit = (87435 - 86565) * 0.02 = 17.40
            - Remove matched buy from queue

            Result: 17.40
        """
        remaining_qty = sell_qty
        total_profit = 0.0

        # Match sells to buys in FIFO order
        while remaining_qty > 0 and self.buy_queue:
            # Get oldest buy
            buy_price, buy_qty, buy_time = self.buy_queue[0]

            # How much can we match?
            matched_qty = min(remaining_qty, buy_qty)

            # Calculate profit for this match
            profit = (sell_price - buy_price) * matched_qty
            total_profit += profit

            self.logger.info(
                f"Matched: Buy ${buy_price:,.2f} -> Sell ${sell_price:,.2f}, "
                f"Qty: {matched_qty:.6f}, Profit: ${profit:.2f}"
            )

            # Update queue
            if matched_qty == buy_qty:
                # Fully matched - remove buy from queue
                self.buy_queue.pop(0)
            else:
                # Partial match - reduce buy quantity
                self.buy_queue[0] = (buy_price, buy_qty - matched_qty, buy_time)

            # Reduce remaining quantity to match
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
        """
        Send Telegram notification for completed profit cycle

        Args:
            profit: Realized profit from this cycle
            sell_price: Price at which we sold
            qty: Quantity in this cycle
        """
        total_cycles = len(self.completed_cycles)
        total_profit = sum(c['profit'] for c in self.completed_cycles)

        msg = f"""✅ Profit Cycle Complete!
Sell Price: ${sell_price:,.2f}
Qty: {qty:.6f}
Profit: ${profit:.2f}

Total Cycles: {total_cycles}
Total Profit: ${total_profit:.2f}"""

        teddy_say(msg)
```

**Main Loop Flow:**

```
run(poll_interval=10)
    ↓
    │
    ├─── while True:
    │       │
    │       ├─ check_orders()
    │       │    ├─ For each active order:
    │       │    │    └─ api.get_order(id)
    │       │    │         └─ If status == 'filled'
    │       │    │              └─ Add to filled_orders[]
    │       │    └─ Return filled_orders
    │       │
    │       ├─ For each filled order:
    │       │    └─ handle_fill(order_data)
    │       │         ├─ Update inventory
    │       │         ├─ Match for P&L (if sell)
    │       │         ├─ Calculate counter-price
    │       │         ├─ place_order(counter)
    │       │         └─ teddy_say(notification)
    │       │
    │       └─ sleep(10 seconds)
    │
    └─── (repeat forever)
```

---

### 9. `main.py`

**Purpose:** Entry point - sets everything up and runs the bot

```python
from bear import config
from bear.logger import setup_logger
from bear.trader import GridTradingBot
from bear.telegram import teddy_say
import signal
import sys

def signal_handler(sig, frame):
    """
    Graceful shutdown on Ctrl+C

    Args:
        sig: Signal number
        frame: Current stack frame

    When user presses Ctrl+C:
    1. Send Telegram notification
    2. Exit gracefully
    """
    teddy_say("🛑 Grid bot shutting down...")
    sys.exit(0)

if __name__ == '__main__':
    # Setup logging
    # This creates the logger that all modules will use
    logger = setup_logger(level=config['logging']['level'])

    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Initialize bot with configuration
    bot = GridTradingBot(config)

    try:
        # Send startup notification
        teddy_say("🚀 Grid bot starting...")

        # Log startup
        logger.info("CryptoBear Grid Trading Bot")
        logger.info("=" * 50)

        # PHASE 1: Initialize grid and place orders
        bot.initialize()

        # PHASE 2: Start main monitoring loop
        # This runs forever until Ctrl+C or exception
        bot.run(poll_interval=10)

    except Exception as e:
        # Fatal error - log and notify
        logger.exception("Fatal error in main loop")
        teddy_say(f"💥 Bot crashed: {e}")
        sys.exit(1)
```

**What `if __name__ == '__main__':` means:**

```python
# When you run: python main.py
# __name__ is set to '__main__'
# So the code inside runs

# When you import: from main import something
# __name__ is set to 'main' (module name)
# So the code inside does NOT run
```

This pattern allows the file to be both:
1. A runnable script: `python main.py`
2. An importable module: `from main import GridTradingBot`

**Signal Handling:**

```python
signal.signal(signal.SIGINT, signal_handler)
```

- `SIGINT` = Ctrl+C signal
- When user presses Ctrl+C, call `signal_handler()`
- Allows graceful shutdown instead of abrupt crash

---

## How Everything Works Together

### Complete Execution Flow

```
1. USER STARTS BOT
   $ python main.py

2. MAIN.PY RUNS
   ├─ Setup logger
   ├─ Register Ctrl+C handler
   ├─ Create GridTradingBot
   └─ Call bot.initialize()

3. BOT.INITIALIZE()
   ├─ Get current BTC price ($87,000)
   ├─ Get account balance ($100,000)
   ├─ GridCalculator.calculate_grid_levels()
   │   ├─ Buy levels: $86,565, $86,130, $85,695, $85,260, $84,825
   │   └─ Sell levels: $87,435, $87,870, $88,305, $88,740, $89,175
   ├─ GridCalculator.calculate_position_size()
   │   └─ Qty: 0.022988 BTC per order
   ├─ For each buy level:
   │   └─ AlpacaPaper.buy() → Place order via API
   └─ teddy_say("Grid initialized!")

4. BOT.RUN() - MAIN LOOP
   ┌─────────────────────────────────────────────────────┐
   │ while True:                                         │
   │                                                     │
   │   ┌─ check_orders()                                │
   │   │   For each active order ID:                    │
   │   │     AlpacaPaper.get_order(id)                  │
   │   │     If status == 'filled':                     │
   │   │       Add to filled_orders[]                   │
   │   └─ Returns: filled_orders                        │
   │                                                     │
   │   ┌─ For each filled order:                        │
   │   │   handle_fill()                                │
   │   │     ├─ Extract: side, price, qty               │
   │   │     ├─ Update inventory                        │
   │   │     ├─ If buy: add to buy_queue                │
   │   │     ├─ If sell: match_sell_to_buy()            │
   │   │     │    ├─ Match to oldest buy (FIFO)         │
   │   │     │    ├─ Calculate profit                   │
   │   │     │    └─ teddy_say("Profit: $17.40")        │
   │   │     ├─ GridCalculator.get_counter_level()      │
   │   │     ├─ place_order(counter_side, ...)          │
   │   │     └─ teddy_say("Order filled!")              │
   │   └─                                                │
   │                                                     │
   │   sleep(10)                                         │
   │                                                     │
   └─────────────────────────────────────────────────────┘

5. USER STOPS BOT
   Press Ctrl+C
   ├─ signal_handler() called
   ├─ teddy_say("Shutting down...")
   └─ sys.exit(0)
```

---

## Examples and Scenarios

### Scenario 1: Normal Grid Operation

**Initial State:**
```
Price: $87,000
Balance: $100,000
Open orders: 5 buy orders
Inventory: 0 BTC
```

**Price drops to $86,565:**
```
EVENT: BUY order fills
  - Buy 0.022988 BTC @ $86,565
  - Cost: $1,989.26

BOT ACTION:
  1. inventory += 0.022988 → inventory = 0.022988
  2. buy_queue.append((86565, 0.022988, now))
  3. counter_price = get_counter_level(86565, 'buy', grid)
     → $87,435
  4. Place SELL 0.022988 @ $87,435
  5. Send Telegram: "🟢 BUY filled @ $86,565"

NEW STATE:
  Open orders: 4 buys + 1 sell
  Inventory: 0.022988 BTC
  Buy queue: [(86565, 0.022988, now)]
```

**Price rises to $87,435:**
```
EVENT: SELL order fills
  - Sell 0.022988 BTC @ $87,435
  - Revenue: $2,009.66

BOT ACTION:
  1. inventory -= 0.022988 → inventory = 0
  2. Match to oldest buy:
     - Buy: $86,565
     - Sell: $87,435
     - Profit: ($87,435 - $86,565) * 0.022988 = $19.99
  3. Remove matched buy from queue
  4. counter_price = get_counter_level(87435, 'sell', grid)
     → $86,565
  5. Place BUY 0.022988 @ $86,565
  6. Send Telegram: "✅ Profit Cycle Complete! Profit: $19.99"

NEW STATE:
  Open orders: 5 buys
  Inventory: 0 BTC
  Buy queue: []
  Completed cycles: 1
  Total profit: $19.99
```

---

### Scenario 2: Multiple Fills

**Initial State:**
```
Price: $87,000
Buy queue: []
```

**Price drops rapidly to $85,000 (multiple orders fill):**
```
FILLS:
  - BUY @ $86,565 → 0.022988 BTC
  - BUY @ $86,130 → 0.022988 BTC
  - BUY @ $85,695 → 0.022988 BTC

BOT ACTIONS:
  For each fill:
    1. Update inventory
    2. Add to buy_queue
    3. Place corresponding sell order

RESULT:
  Inventory: 0.068964 BTC (3 * 0.022988)
  Buy queue: [
    (86565, 0.022988, time1),
    (86130, 0.022988, time2),
    (85695, 0.022988, time3)
  ]
  New sell orders:
    - SELL @ $87,435
    - SELL @ $86,999
    - SELL @ $86,564
```

**Price rises to $87,500 (multiple sells fill):**
```
FILLS:
  - SELL @ $86,564 → 0.022988 BTC
  - SELL @ $86,999 → 0.022988 BTC
  - SELL @ $87,435 → 0.022988 BTC

BOT ACTIONS (FIFO matching):

  Fill 1: SELL @ $86,564
    Match to: BUY @ $86,565 (oldest)
    Profit: ($86,564 - $86,565) * 0.022988 = -$0.02 (small loss)

  Fill 2: SELL @ $86,999
    Match to: BUY @ $86,130 (next oldest)
    Profit: ($86,999 - $86,130) * 0.022988 = $19.98

  Fill 3: SELL @ $87,435
    Match to: BUY @ $85,695 (next oldest)
    Profit: ($87,435 - $85,695) * 0.022988 = $40.00

TOTAL PROFIT: $59.96
```

---

### Scenario 3: Error Handling

**API Error During Order Check:**
```python
def check_orders(self):
    for order_id in list(self.active_orders.keys()):
        try:
            order_data = self.api.get_order(order_id)
            # ... process order
        except Exception as e:
            # LOG ERROR BUT CONTINUE
            self.logger.error(f"Error checking order {order_id}: {e}")
            # Don't crash - keep checking other orders

# Result: One API error doesn't stop the entire bot
```

**Order Placement Fails:**
```python
def place_order(self, side, qty, price):
    try:
        response = self.api.buy(self.pair, qty, price)
        # ... track order
    except Exception as e:
        # LOG ERROR AND NOTIFY
        self.logger.error(f"Failed to place {side} order: {e}")
        teddy_say(f"⚠️ Order failed: {side} {qty} @ ${price}")
        # Don't add to active_orders (it didn't work)

# Result: User is notified, bot continues running
```

---

## Configuration Guide

### Adjusting Grid Strategy

**Make grid tighter (more frequent trades):**
```yaml
grid:
  spread: 0.003  # 0.3% instead of 0.5%
  count: 10

# Result:
# - Orders closer together
# - More fills (more active trading)
# - Smaller profit per cycle
```

**Make grid wider (less frequent trades):**
```yaml
grid:
  spread: 0.01   # 1.0% instead of 0.5%
  count: 10

# Result:
# - Orders farther apart
# - Fewer fills (less active)
# - Larger profit per cycle
```

**More grid levels:**
```yaml
grid:
  spread: 0.005
  count: 20      # 10 buy + 10 sell instead of 5+5

# Result:
# - Wider price range covered
# - More capital deployed
# - Better capture of large price swings
```

---

### Adjusting Position Size

**More aggressive (higher risk, higher potential profit):**
```yaml
risk:
  per_trade: 0.05  # 5% instead of 2%

# Result:
# - Larger position per order
# - Faster capital deployment
# - Higher profit per cycle
# - Less diversification
```

**More conservative (lower risk):**
```yaml
risk:
  per_trade: 0.01  # 1% instead of 2%

# Result:
# - Smaller position per order
# - More capital in reserve
# - Lower profit per cycle
# - More diversification
```

---

## Debugging and Monitoring

### Check Bot Status

```bash
# View current orders
python check_orders.py

# View profit history
python check_profits.py

# View bot activity log
python show_activity.py

# View current price and sell targets
python check_price.py
```

### Log Files

```bash
# Follow logs in real-time
tail -f logs/grid_bot_20251223.log

# Search for errors
grep ERROR logs/grid_bot_20251223.log

# Search for fills
grep "filled" logs/grid_bot_20251223.log
```

### Telegram Monitoring

All important events are sent to Telegram:
- Grid initialization
- Order fills
- Profit cycles
- Errors

---

## Safety Features

1. **Limit Orders Only**
   - Never market orders (prevents price slippage)
   - Orders only execute at specified price or better

2. **Error Isolation**
   - One failed API call doesn't crash the bot
   - Errors logged and reported, bot continues

3. **Graceful Shutdown**
   - Ctrl+C sends notification
   - Orders remain on exchange (not auto-canceled)

4. **Paper Trading**
   - Uses Alpaca paper account (fake money)
   - Test strategies risk-free

5. **No Auto-Push to Git**
   - .env file never committed (API keys protected)
   - logs/ directory ignored

---

## Next Steps and Enhancements

### Possible Improvements

1. **Grid Recentering**
   - Detect when price moves far from grid center
   - Cancel old orders and recalculate grid

2. **Dynamic Position Sizing**
   - Adjust order size based on volatility
   - Larger orders in stable markets, smaller in volatile

3. **Stop Loss**
   - Cancel all orders if loss exceeds threshold
   - Prevent runaway losses

4. **Multiple Pairs**
   - Trade BTC, ETH, SOL simultaneously
   - Diversify across assets

5. **Backtesting**
   - Test strategy on historical data
   - Optimize spread and count parameters

6. **Web Dashboard**
   - Real-time visualization of grid
   - Charts showing profit over time

---

## Glossary

**API (Application Programming Interface):** Interface for programs to communicate

**Grid Trading:** Strategy placing buy/sell orders at fixed price intervals

**Limit Order:** Order that only executes at specified price or better

**Market Order:** Order that executes immediately at current price

**FIFO (First In First Out):** Accounting method matching oldest buy to sell

**Paper Trading:** Simulated trading with fake money

**REST API:** Web API using HTTP requests (GET, POST, DELETE)

**Position Size:** Amount of asset to buy/sell per order

**Inventory:** Current holdings of an asset

**Bid Price:** Highest price buyer is willing to pay

**Ask Price:** Lowest price seller is willing to accept

**Spread (Price):** Difference between bid and ask

**Spread (Grid):** Percentage spacing between grid levels

**GTC (Good Till Canceled):** Order stays active until filled or canceled

---

## Summary

CryptoBear is a **grid trading bot** that:

1. **Calculates a price grid** using `GridCalculator`
2. **Places initial buy orders** via `AlpacaPaper` API
3. **Monitors continuously** in `bot.run()` loop
4. **Handles fills** by placing counter-orders
5. **Tracks profits** using FIFO matching
6. **Notifies via Telegram** for all events
7. **Logs everything** for debugging

**Key Files:**
- `main.py` - Entry point
- `trader.py` - Main orchestration
- `grid.py` - Grid calculations
- `alpaca_rest.py` - API client
- `telegram.py` - Notifications
- `logger.py` - Logging setup
- `settings.yaml` - Configuration

**Key Concepts:**
- **Grid strategy** = Profit from price oscillation
- **FIFO matching** = Match sells to oldest buys
- **State management** = Track orders, inventory, profits
- **Error handling** = Log errors, don't crash

You now have a complete understanding of how CryptoBear works! 🧸📈
