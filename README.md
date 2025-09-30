# TradingView Indicators

A collection of custom Pine Script indicators for TradingView, designed for various trading strategies and market analysis.

## Indicators

### 1. ITM Probability Bands

**File:** `itm-probability-bands.pine`

An options-focused indicator that calculates In-The-Money (ITM) probability bands using Black-Scholes methodology. Features:

- **Probability Bands**: Shows 68% and 95% confidence intervals converging to strike price
- **ITM Calculations**: Displays call and put ITM probabilities in the data window
- **Customizable Parameters**: Strike price, expiration date, implied volatility, risk-free rate
- **Time Window**: Configurable lookback period (1-8 weeks)
- **Visual Elements**: Color-coded bands, strike price line, and current price tracking

### 2. MA High/Low

**File:** `ma-high-low.pine`

A moving average channel indicator with trend analysis capabilities. Features:

- **Channel System**: Uses EMA of highs and lows to create dynamic support/resistance levels
- **Trend Identification**: Color-coded channel fills (bullish/neutral/bearish)
- **Multi-Timeframe**: Supports different timeframes for channel and moving average calculations
- **ADX Integration**: Includes ADX for trend strength confirmation
- **Strategy Table**: Real-time display of channel direction, moving average status, ADX, and ATR values

### 3. On Balance Volume Squeeze

**File:** `on-balance-volume-squeeze.pine`

A volume-based indicator that identifies potential breakout opportunities using OBV and Bollinger Bands. Features:

- **OBV Calculation**: Standard On Balance Volume with cumulative volume tracking
- **Bollinger Bands**: Applied to OBV to identify squeeze conditions
- **Squeeze Detection**: Highlights periods of low volatility (orange bands)
- **Multiple MA Types**: SMA, EMA, SMMA, WMA, and VWMA options
- **Volume Validation**: Error handling for missing volume data

### 4. Opening Range with Opportunity Window

**File:** `orb-with-opportunity-window.pine`

A comprehensive opening range breakout system with advanced features. Features:

- **Opening Range**: Configurable time periods (default: 60 minutes)
- **Custom Sessions**: Support for custom trading hours with timezone selection
- **Opportunity Window**: Defined trading window with visual highlighting
- **Breakout Signals**: Directional signals with bias filtering
- **Target System**: Multiple price targets based on range percentage
- **Size Analysis**: Color-coded range size validation
- **Alerts**: Configurable alerts for breakouts above/below range
- **Moving Average**: Session-based MA that resets daily

### 5. Probability Bands V2

**File:** `probability-bands-v2.pine`

An enhanced version of probability bands with improved visualization. Features:

- **Log-Normal Distribution**: Proper options pricing methodology
- **Time Decay**: Bands converge to strike price as expiration approaches
- **Lookback Window**: Configurable display period (1-52 weeks)
- **Future Projection**: Lines extend to expiration date
- **Clean Visualization**: Simplified display focusing on key levels

## Usage

1. Copy the desired Pine Script code from any `.pine` file
2. Open TradingView and navigate to the Pine Editor
3. Paste the code and click "Add to Chart"
4. Configure the input parameters according to your trading strategy
5. Apply the indicator to your chart

## Requirements

- TradingView account with Pine Script access
- Basic understanding of technical analysis concepts
- For options indicators: Knowledge of options pricing and Greeks

## Customization

All indicators include extensive input parameters allowing you to:

- Adjust timeframes and periods
- Modify colors and visual styles
- Enable/disable various features
- Set custom values for calculations

## License

Please refer to individual file headers for specific licensing information. Some indicators are based on or modified from existing open-source implementations.

## Contributing

Feel free to modify and improve these indicators for your own trading needs. Consider sharing improvements back to the community.

---

_Note: These indicators are for educational and analysis purposes. Always conduct your own research and consider your risk tolerance before making trading decisions._
