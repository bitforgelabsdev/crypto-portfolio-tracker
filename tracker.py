import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

BINANCE_API = "https://api.binance.com/api/v3"
CONFIG_FILE = "config.json"


# ─── Config ───────────────────────────────────────────────────────────────────

def load_config() -> dict:
    """Load portfolio config from config.json."""
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


# ─── Binance helpers ──────────────────────────────────────────────────────────

def get_price(symbol: str) -> float:
    """Fetch current price from Binance."""
    r = requests.get(f"{BINANCE_API}/ticker/price", params={"symbol": symbol}, timeout=10)
    r.raise_for_status()
    return float(r.json()["price"])


def get_24h_change(symbol: str) -> float:
    """Fetch 24h price change percentage from Binance."""
    r = requests.get(f"{BINANCE_API}/ticker/24hr", params={"symbol": symbol}, timeout=10)
    r.raise_for_status()
    return float(r.json()["priceChangePercent"])


# ─── Telegram ─────────────────────────────────────────────────────────────────

def send_telegram(message: str):
    """Send a message to Telegram."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }, timeout=10)


def format_telegram_report(results: list, total_invested: float, total_value: float) -> str:
    """Format portfolio report for Telegram."""
    total_pnl = total_value - total_invested
    total_pnl_pct = (total_pnl / total_invested * 100) if total_invested > 0 else 0
    pnl_emoji = "🟢" if total_pnl >= 0 else "🔴"

    lines = [
        "💼 <b>PORTFOLIO REPORT</b>",
        f"🕐 {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}",
        ""
    ]

    for r in results:
        pnl_emoji_coin = "🟢" if r["pnl"] >= 0 else "🔴"
        change_emoji = "📈" if r["change_24h"] >= 0 else "📉"
        lines.append(
            f"{pnl_emoji_coin} <b>{r['symbol']}</b>\n"
            f"   💰 ${r['price']:,.4f}  |  Value: ${r['value']:,.2f}\n"
            f"   PnL: {'+' if r['pnl'] >= 0 else ''}{r['pnl']:,.2f}$  "
            f"{change_emoji} 24h: {r['change_24h']:+.2f}%"
        )

    lines += [
        "",
        f"📊 <b>Total Invested:</b> ${total_invested:,.2f}",
        f"💰 <b>Total Value:</b> ${total_value:,.2f}",
        f"{pnl_emoji} <b>Total PnL:</b> {'+' if total_pnl >= 0 else ''}{total_pnl:,.2f}$ ({total_pnl_pct:+.2f}%)"
    ]

    return "\n".join(lines)


# ─── Display helpers ──────────────────────────────────────────────────────────

def color(value: float, text: str) -> str:
    """Apply ANSI color based on positive/negative value."""
    GREEN, RED, RESET = "\033[92m", "\033[91m", "\033[0m"
    return f"{GREEN}{text}{RESET}" if value >= 0 else f"{RED}{text}{RESET}"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_portfolio(results: list, total_invested: float, total_value: float, next_report_in: int):
    """Print formatted portfolio table to terminal."""
    total_pnl = total_value - total_invested
    total_pnl_pct = (total_pnl / total_invested * 100) if total_invested > 0 else 0

    clear_screen()
    print("=" * 75)
    print("  💼  CRYPTO PORTFOLIO TRACKER")
    print(f"  🕐  {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    print("=" * 75)
    print(f"  {'COIN':<12} {'AMOUNT':<12} {'PRICE':<14} {'VALUE':<14} {'PNL':<14} {'24H'}")
    print("-" * 75)

    for r in results:
        pnl_str = color(r["pnl"], f"${r['pnl']:>+,.2f}")
        change_str = color(r["change_24h"], f"{r['change_24h']:>+.2f}%")
        print(
            f"  {r['symbol']:<12} "
            f"{r['amount']:<12} "
            f"${r['price']:<13,.4f} "
            f"${r['value']:<13,.2f} "
            f"{pnl_str:<23} "
            f"{change_str}"
        )

    print("=" * 75)
    print(f"  {'Total Invested:':<30} ${total_invested:>12,.2f}")
    print(f"  {'Total Value:':<30} ${total_value:>12,.2f}")
    pnl_line = color(total_pnl, f"${total_pnl:>+,.2f}  ({total_pnl_pct:+.2f}%)")
    print(f"  {'Total PnL:':<30} {pnl_line}")
    print("=" * 75)
    print(f"  📲 Next Telegram report in: {next_report_in}s")
    print(f"  ⏳ Refreshing every 30s... (Ctrl+C to stop)\n")


# ─── Main loop ────────────────────────────────────────────────────────────────

def run():
    print("💼 Crypto Portfolio Tracker starting...")
    last_report_time = 0

    while True:
        # Reload config every cycle — edit config.json anytime, no restart needed
        config = load_config()
        portfolio = config.get("portfolio", {})
        refresh_interval = config.get("refresh_interval", 30)
        report_interval = config.get("telegram_report_interval", 300)

        results = []
        total_invested = 0
        total_value = 0

        for symbol, data in portfolio.items():
            try:
                price = get_price(symbol)
                change_24h = get_24h_change(symbol)
                value = price * data["amount"]
                invested = data["avg_buy"] * data["amount"]
                pnl = value - invested

                results.append({
                    "symbol": symbol.replace("USDT", ""),
                    "amount": data["amount"],
                    "price": price,
                    "value": value,
                    "pnl": pnl,
                    "change_24h": change_24h,
                })

                total_invested += invested
                total_value += value

            except Exception as e:
                print(f"  ❌ Error fetching {symbol}: {e}")

        now = time.time()
        next_report_in = max(0, int(report_interval - (now - last_report_time)))

        print_portfolio(results, total_invested, total_value, next_report_in)

        # Send Telegram report at configured interval
        if now - last_report_time >= report_interval:
            msg = format_telegram_report(results, total_invested, total_value)
            send_telegram(msg)
            last_report_time = now
            print("  📲 Telegram report sent!")

        time.sleep(refresh_interval)


if __name__ == "__main__":
    run()