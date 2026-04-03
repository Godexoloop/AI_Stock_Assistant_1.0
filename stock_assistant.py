# ================================
# 📦 IMPORT LIBRARIES
# ================================
import yfinance as yf
import matplotlib.pyplot as plt


# ================================
# 🧑‍💻 USER INPUT
# ================================
user_stock = input("Enter stock name (e.g. TCS, RELIANCE): ")
stock = user_stock.upper() + ".NS"

timeframe = input("Choose timeframe (5d, 1mo, 3mo, 6mo, 1y): ").strip().lower()

valid_timeframes = ["5d", "1mo", "3mo", "6mo", "1y"]

if timeframe not in valid_timeframes:
    print("Invalid timeframe ❌")
    print("Choose from: 5d, 1mo, 3mo, 6mo, 1y")
    exit()


try:
    # ================================
    # 📊 FETCH DATA
    # ================================
    data = yf.download(stock, period=timeframe)

    if data.empty:
        print("Invalid stock name ❌")
        exit()

    print(f"\n--- Analysis for {stock} ({timeframe}) ---")

    # Extract close prices
    close_prices = data["Close"][stock]


    # ================================
    # 📈 ADAPTIVE MOVING AVERAGES
    # ================================
    # Adjust MA based on timeframe
    if timeframe == "5d":
        ma_short = 3
        ma_long = 5
    elif timeframe == "1mo":
        ma_short = 5
        ma_long = 10
    else:
        ma_short = 20
        ma_long = 50

    data["MA_short"] = close_prices.rolling(window=ma_short).mean()
    data["MA_long"] = close_prices.rolling(window=ma_long).mean()

    calc_data = data.dropna()

    # ================================
    # 📉 TREND DETECTION
    # ================================
    latest_price = close_prices.iloc[-1]
    latest_ma_short = calc_data["MA_short"].iloc[-1]
    latest_ma_long = calc_data["MA_long"].iloc[-1]

    print("\nLatest Price:", latest_price)

    # Short-term direction
    recent_prices = close_prices.tail(5)

    if recent_prices.iloc[-1] > recent_prices.iloc[0]:
        short_trend = "Uptrend 📈"
    else:
        short_trend = "Downtrend 📉"

    print("Short-Term Trend:", short_trend)

    # Combined trend
    if latest_price > latest_ma_short and latest_ma_short > latest_ma_long:
        print("Trend: Strong Uptrend 🚀")
    elif latest_price < latest_ma_short and latest_ma_short < latest_ma_long:
        print("Trend: Strong Downtrend 🔻")
    else:
        print("Trend: Mixed / Sideways ⚖️")


    # ================================
    # ⚖️ VOLATILITY
    # ================================
    volatility = close_prices.pct_change().std()

    print("\nVolatility:", volatility)

    if volatility < 0.01:
        risk = "Low 🟢"
    elif volatility < 0.02:
        risk = "Medium 🟡"
    else:
        risk = "High 🔴"

    print("Risk Level:", risk)


    # ================================
    # 📊 RSI (Adaptive)
    # ================================
    if len(close_prices) >= 14:
        delta = close_prices.diff()

        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        data["RSI"] = rsi
        latest_rsi = data["RSI"].iloc[-1]

        print("\nRSI:", latest_rsi)

        if latest_rsi > 70:
            rsi_status = "Overbought ⚠️"
        elif latest_rsi < 30:
            rsi_status = "Oversold 💡"
        else:
            rsi_status = "Normal ✅"

        print("RSI Status:", rsi_status)

    else:
        print("\nRSI: Not enough data ❌")
        latest_rsi = None
    if latest_rsi is None:
        print("Note: RSI not available for this timeframe ⚠️")

    # ================================
    # 🧠 SMART ADVICE
    # ================================
    print("\n--- Smart Investment Advice ---")

    # Strong Uptrend
    if latest_price > latest_ma_short and latest_ma_short > latest_ma_long:
        print("Strong uptrend, good opportunity 👍")

    # Strong Downtrend
    elif latest_price < latest_ma_short and latest_ma_short < latest_ma_long:
        print("Strong downtrend ❗ Avoid or wait")

    # RSI conditions (ONLY if RSI exists)
    elif latest_rsi is not None and latest_rsi > 70:
        print("Overbought ⚠️ Wait")

    elif latest_rsi is not None and latest_rsi < 30:
        print("Oversold 💡 Opportunity")

    # High risk
    elif volatility > 0.02:
        print("High risk ❗ Not for beginners")

    # Default
    else:
        print("Mixed signals 🤔 Analyze carefully")


    # ================================
    # 🎯 FINAL DECISION
    # ================================
    print("\n--- Final Decision ---")

    if latest_price > latest_ma_short and latest_ma_short > latest_ma_long:
        print("Signal: BUY 🟢")
    elif latest_price < latest_ma_short and latest_ma_short < latest_ma_long:
        print("Signal: AVOID 🔴")
    else:
        print("Signal: HOLD 🟡")


    # ================================
    # 📈 GRAPH
    # ================================
    plt.figure()

    plt.plot(close_prices.loc[data.index], label="Close Price", linewidth=2, marker='o')
    plt.plot(data["MA_short"], label=f"{ma_short}-Day MA", linewidth=2)
    plt.plot(data["MA_long"], label=f"{ma_long}-Day MA", linewidth=2)

    if timeframe == "5d":
        plt.title(f"{stock} (5-Day View - Limited Data)")
    else:
        plt.title(f"{stock} Analysis ({timeframe})")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.legend()

    plt.show()

except Exception as e:
    print("Error:", e)