# 💼 Crypto Portfolio Tracker

A terminal-based cryptocurrency portfolio tracker that shows your holdings, current values, and PnL in real-time using the Binance public API.

---

## ✨ Features

- 📊 **Real-time portfolio value** — live prices from Binance
- 💰 **PnL tracking** — profit/loss per coin and total
- 📈 **24h change** — see which coins are up or down today
- 🎨 **Color-coded output** — green for profit, red for loss
- ⚡ **No API key required** — uses Binance public endpoints
- 🔁 **Auto-refresh** — updates every 30 seconds

---

## 📸 Preview

```
===========================================================================
  💼  CRYPTO PORTFOLIO TRACKER
  🕐  2024-11-01 14:32:10 UTC
===========================================================================
  COIN         AMOUNT       PRICE          VALUE          PNL            24H
---------------------------------------------------------------------------
  BTC          0.05         $70,316.91     $3,515.85      +$515.85       +2.31%
  ETH          1.2          $2,058.57      $2,470.28      -$889.72       -1.45%
  BNB          5.0          $651.66        $3,258.30      +$1,258.30     +3.12%
===========================================================================
  Total Invested:                $        8,350.00
  Total Value:                   $        9,244.43
  Total PnL:                     +$894.43  (+10.71%)
===========================================================================
```

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/crypto-portfolio-tracker.git
cd crypto-portfolio-tracker
```

### 2. Install dependencies
```bash
pip install requests python-dotenv
```

### 3. Configure your portfolio

Edit the `PORTFOLIO` dictionary in `tracker.py`:
```python
PORTFOLIO = {
    "BTCUSDT":  {"amount": 0.05,  "avg_buy": 60000},
    "ETHUSDT":  {"amount": 1.2,   "avg_buy": 2800},
}
```

### 4. Run the tracker
```bash
python tracker.py
```

---

## ⚙️ Configuration

| Variable | Description |
|----------|-------------|
| `PORTFOLIO` | Your holdings with amount and average buy price |
| `REFRESH_INTERVAL` | How often to refresh prices in seconds (default: 30) |

---

## 📦 Tech Stack

- **Python 3.8+**
- **Binance Public API** — live price data
- **ANSI colors** — terminal color output (no extra libraries)

---

## 📄 License

MIT License

---

## 👨‍💻 Author

Built by **IronScript** — Full Stack & Crypto Bot Developer
> Available for freelance projects on Fiverr & Upwork