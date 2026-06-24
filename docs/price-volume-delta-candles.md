---
title: Price/Volume Delta Candles
description: Divergence detection between price action and volume delta.
category: indicator
---

# Price/Volume Delta Candles Indicator Analysis

## Overview

The **Price/Volume Delta Candles** indicator is a sophisticated divergence detection tool that reveals hidden accumulation and distribution by comparing what price is doing versus what volume is doing. By analyzing lower timeframe data to calculate volume delta and comparing it to the closing direction, this indicator identifies moments when "smart money" is acting contrary to the obvious price action—often signaling potential reversals or continuation patterns before they become apparent.

## Table of Contents

- [How This Indicator Works](#how-this-indicator-works)
  - [Core Calculation](#core-calculation)
  - [Divergence Logic](#divergence-logic)
  - [Visual Components](#visual-components)
- [How Traders Can Use This to Find an Edge](#how-traders-can-use-this-to-find-an-edge)
  - [Reversal Signal Detection](#1-reversal-signal-detection)
  - [Trend Continuation Confirmation](#2-trend-continuation-confirmation)
  - [Smart Money Tracking](#3-smart-money-tracking)
  - [Entry Timing Refinement](#4-entry-timing-refinement)
- [Complementary Indicators and Market Conditions](#complementary-indicators-and-market-conditions)
- [Trading Strategies](#trading-strategies)
- [Risk Warnings and Limitations](#risk-warnings-and-limitations)
- [Conclusion](#conclusion)

---

## How This Indicator Works

### Core Calculation

The indicator uses a multi-step process to identify price/volume divergences:

#### **Step 1: Lower Timeframe Volume Analysis**

The indicator examines lower timeframe bars within each current timeframe bar to classify volume with higher precision:

```text
For each lower timeframe bar:

  If Close > Open (green candle):
    → Add volume to Up Volume

  If Close < Open (red candle):
    → Add volume to Down Volume (as negative)

  If Close = Open (doji) but Close >= Previous Close:
    → Add volume to Up Volume

  If Close = Open (doji) but Close < Previous Close:
    → Add volume to Down Volume (as negative)
```

**Why Lower Timeframe?**

- More accurate volume classification
- Captures intra-bar dynamics
- Reveals accumulation/distribution hidden in higher timeframe bars
- Example: A 5-minute bar that closes down might contain 4 minutes of buying and 1 minute of selling—this would show in the delta

#### **Step 2: Aggregate to Current Timeframe**

```text
Up Volume = Sum of all positive volume from lower TF bars
Down Volume = Sum of all negative volume from lower TF bars
Volume Delta = Up Volume + Down Volume
```

Since Down Volume is negative, the delta reveals net pressure:

- **Delta > 0**: Net buying pressure (up volume exceeded down volume)
- **Delta < 0**: Net selling pressure (down volume exceeded up volume)
- **Delta ≈ 0**: Balanced buying and selling

#### **Step 3: Calculate Delta Strength**

```text
Delta Percentage = (|Volume Delta| / Total Volume) × 100
```

This normalizes the delta relative to the bar's total volume:

- **High %**: Strong conviction in one direction
- **Low %**: Weak or balanced volume distribution

#### **Step 4: Apply Threshold Filter**

```text
Meets Threshold = Delta Percentage >= Threshold Setting (default 20%)
```

Only divergences with sufficient strength trigger signals, filtering out noise.

### Divergence Logic

The indicator identifies two types of divergences:

#### **Bullish Divergence (Purple Arrow Down/Bar)**

**Condition:**

```text
Price closes DOWN (Close < Previous Close)
BUT
Volume Delta is POSITIVE (Net buying pressure)
AND
Delta strength >= Threshold
```

**What This Means:**

- Price appears weak (closing down)
- But volume shows buyers were more aggressive
- Accumulation happening during the down move
- "Smart money" buying while price drops
- Potential bullish reversal or trend continuation

**Visual Signals:**

- Purple arrow pointing DOWN above the bar
- OR purple candle (if candle coloring enabled)

**Why "arrow down" for bullish?** The arrow points to where you might want to buy (down at the bar), not the direction of the prediction.

#### **Bearish Divergence (Blue Arrow Up/Bar)**

**Condition:**

```text
Price closes UP (Close > Previous Close)
BUT
Volume Delta is NEGATIVE (Net selling pressure)
AND
Delta strength >= Threshold
```

**What This Means:**

- Price appears strong (closing up)
- But volume shows sellers were more aggressive
- Distribution happening during the up move
- "Smart money" selling while price rises
- Potential bearish reversal or exhaustion

**Visual Signals:**

- Blue arrow pointing UP below the bar
- OR white candle (if candle coloring enabled)

**Why "arrow up" for bearish?** The arrow points to where selling occurred (up at the bar), warning of distribution.

### Visual Components

#### 1. Shape Markers (Default)

- **Purple arrow down** (above bar): Bullish divergence detected
- **Blue arrow up** (below bar): Bearish divergence detected
- Small size, non-intrusive
- Can be toggled off

#### 2. Candle Coloring (Optional)

- **Purple candle**: Bullish divergence
- **White candle**: Bearish divergence
- Overrides normal candle colors
- More visually prominent than arrows
- Can be toggled on/off

#### 3. Delta Threshold Setting

- Adjustable from 0% to 100%
- Default: 20%
- Higher = fewer but stronger signals
- Lower = more signals but more noise

#### 4. Lower Timeframe Settings

- **Auto mode** (default): Automatically selects appropriate lower TF
  - Intraday charts → 1-minute bars
  - Daily charts → 5-minute bars
  - Weekly+ charts → 60-minute bars
- **Custom mode**: Manually specify lower timeframe
  - Higher TF = more history, less precision
  - Lower TF = more precision, less history

---

## How Traders Can Use This to Find an Edge

### 1. **Reversal Signal Detection**

The primary edge of this indicator is catching reversals before they're obvious in price.

#### **Bullish Reversal Setup**

**Classic Bottom Formation:**

1. **Downtrend in progress** or price pulling back
2. **Multiple bullish divergence signals** appear
3. Price making lower lows BUT delta consistently positive
4. Each down bar shows hidden accumulation

**Interpretation:**

- Sellers pushing price down
- But buyers absorbing all selling pressure
- Accumulation phase
- Reversal likely imminent

**Action:**

- Look for bullish divergence cluster at support levels
- Enter long on first bullish price confirmation (higher high, bullish engulfing, etc.)
- Stop loss below the divergence low
- Target: Previous resistance or measured move

**Example Scenario:**

```text
Bar 1: Close down, Delta +60% → Bullish divergence (purple arrow)
Bar 2: Close down, Delta +45% → Bullish divergence (purple arrow)
Bar 3: Close down, Delta +75% → Bullish divergence (purple arrow)
Bar 4: Bullish engulfing → ENTRY SIGNAL

Interpretation: Three consecutive down bars with strong buying pressure.
Smart money accumulated the entire decline. Rally likely.
```

#### **Bearish Reversal Setup**

**Classic Top Formation:**

1. **Uptrend in progress** or price rallying
2. **Multiple bearish divergence signals** appear
3. Price making higher highs BUT delta consistently negative
4. Each up bar shows hidden distribution

**Interpretation:**

- Buyers pushing price up
- But sellers more aggressive underneath
- Distribution phase
- Reversal likely imminent

**Action:**

- Look for bearish divergence cluster at resistance levels
- Exit longs or enter short on first bearish price confirmation
- Stop loss above the divergence high
- Target: Previous support or measured move

**Example Scenario:**

```text
Bar 1: Close up, Delta -55% → Bearish divergence (blue arrow)
Bar 2: Close up, Delta -70% → Bearish divergence (blue arrow)
Bar 3: Close up, Delta -40% → Bearish divergence (blue arrow)
Bar 4: Bearish rejection → EXIT/SHORT SIGNAL

Interpretation: Three consecutive up bars with strong selling pressure.
Smart money distributed into the rally. Decline likely.
```

### 2. **Trend Continuation Confirmation**

Divergence signals can also confirm that pullbacks in trends are opportunities, not reversals.

#### **Uptrend Pullback (Buying Opportunity)**

**Setup:**

1. Established uptrend
2. Price pulls back or consolidates
3. **Bullish divergence appears on down bars** during the pullback
4. Shows accumulation happening during the dip

**Interpretation:**

- Healthy pullback, not reversal
- Buyers stepping in at better prices
- Institutions adding to positions
- Trend likely to resume

**Action:**

- Enter long when bullish divergence appears during pullback
- Stop below pullback low
- Target: Trend continuation to new highs

#### **Downtrend Rally (Selling Opportunity)**

**Setup:**

1. Established downtrend
2. Price rallies or consolidates
3. **Bearish divergence appears on up bars** during the rally
4. Shows distribution happening during the bounce

**Interpretation:**

- Dead-cat bounce, not reversal
- Sellers using rally to exit or add shorts
- Institutions distributing into strength
- Downtrend likely to resume

**Action:**

- Enter short or exit longs when bearish divergence appears during rally
- Stop above rally high
- Target: Trend continuation to new lows

### 3. **Smart Money Tracking**

The divergence signals reveal institutional behavior hidden from pure price analysis.

#### **Accumulation Detection**

##### Bullish Divergence = Accumulation Evidence

When you see bullish divergence, it means:

- Large players are **buying aggressively** on down bars
- They're willing to absorb all available supply
- They're using price weakness to build positions
- They expect higher prices ahead

**Where to Watch:**

- At major support levels (accumulation zones)
- After extended declines (capitulation bottoms)
- During consolidation patterns (preparation for breakout)
- At the end of pullbacks in uptrends (adding to winners)

**Trading Implication:**
Join the institutions—buy when they're buying (even if price looks weak).

#### **Distribution Detection**

##### Bearish Divergence = Distribution Evidence

When you see bearish divergence, it means:

- Large players are **selling aggressively** on up bars
- They're willing to sell into any buying pressure
- They're using price strength to exit positions
- They expect lower prices ahead

**Where to Watch:**

- At major resistance levels (distribution zones)
- After extended rallies (exhaustion tops)
- During consolidation patterns (preparation for breakdown)
- During rallies in downtrends (selling into strength)

**Trading Implication:**
Follow the institutions—sell when they're selling (even if price looks strong).

### 4. **Entry Timing Refinement**

Use divergence signals to fine-tune entry points for existing setups.

#### **Enhancing Support/Resistance Trades**

**At Support:**

- Price reaches support level (your setup)
- Wait for bullish divergence (confirmation)
- Entry: On divergence + bullish price action
- Confidence: Much higher than support alone

**At Resistance:**

- Price reaches resistance level (your setup)
- Wait for bearish divergence (confirmation)
- Entry: On divergence + bearish price action
- Confidence: Much higher than resistance alone

#### **Improving Breakout Trades**

**Valid Breakout:**

- Price breaks resistance
- No bearish divergence on breakout bar
- Shows genuine buying pressure
- Trade the breakout with confidence

**False Breakout Warning:**

- Price breaks resistance
- **Bearish divergence on breakout bar** (selling into the breakout)
- Shows distribution, not accumulation
- Avoid or fade the breakout

**Example:**

```text
Scenario 1 (Valid):
- Price breaks above $100 resistance
- Volume delta +65% (strong buying)
- No divergence → Trade the breakout

Scenario 2 (False):
- Price breaks above $100 resistance
- Volume delta -40% (selling pressure)
- Bearish divergence signal → Avoid or short

The divergence saved you from a bull trap!
```

---

## Complementary Indicators and Market Conditions

### 1. **Support and Resistance**

**Why:** Divergence signals most powerful at key structural levels

**Integration:**

- **Bullish divergence at major support** = Highest probability long setup
- **Bearish divergence at major resistance** = Highest probability short setup
- **Divergence in middle of nowhere** = Lower priority, wait for structure
- **Multiple divergences testing same level** = Level very likely to hold

**Enhanced Setup:**

```text
Support Level + Bullish Divergence + Bullish Candle Pattern =
STRONG BUY SIGNAL

Resistance Level + Bearish Divergence + Bearish Candle Pattern =
STRONG SELL SIGNAL
```

### 2. **Trend Indicators**

**Why:** Context determines whether divergence is reversal or continuation

**With Your MA High/Low Indicator:**

**Uptrend (Price above channel):**

- Bullish divergence on pullback = Buy signal (continuation)
- Bearish divergence at channel high = Take profit warning (exhaustion)

**Downtrend (Price below channel):**

- Bearish divergence on rally = Sell signal (continuation)
- Bullish divergence at channel low = Cover shorts warning (exhaustion)

**Neutral (Price in channel):**

- Divergence at channel boundaries = Direction hint for breakout
- Multiple same-direction divergences = Breakout preparation

**With Moving Averages:**

- Divergence above rising 50 MA = Pullback buy opportunity
- Divergence below falling 50 MA = Rally sell opportunity
- Divergence at MA crossovers = Confirms trend change

### 3. **Volume Indicators**

**Why:** Volume context strengthens divergence interpretation

**With Your Up/Down Volume Ratio:**

**Powerful Combinations:**

- Bullish divergence + Ratio rising above 1.0 = Strong buy
- Bearish divergence + Ratio falling below 1.0 = Strong sell
- Bullish divergence + Ratio < 1.0 = Weaker signal, use caution
- Bearish divergence + Ratio > 1.0 = Weaker signal, use caution

**Regime Filter:**

- Only trade bullish divergences when ratio > 0.8
- Only trade bearish divergences when ratio < 1.2
- Divergences more reliable in appropriate volume regimes

**With Volume Profile:**

- Bullish divergence at high-volume node = Strong support confirmation
- Bearish divergence at high-volume node = Strong resistance confirmation
- Divergence at low-volume area = Less reliable, needs more confirmation

### 4. **Volatility Indicators**

**Why:** Divergence reliability varies with volatility regime

**With Your VEI (Volatility Expansion Index):**

**Best Conditions (VEI < 1.0):**

- Divergence signals clean and reliable
- Structure respected
- High probability trades
- Full confidence in signals

**Caution Conditions (VEI > 1.2):**

- Divergence signals may fail
- Market chaotic and unpredictable
- Reduce position size or skip
- Require additional confirmation

**Integration Rule:**

```text
IF Divergence Signal + VEI < 1.0:
  → Take the trade with standard size

IF Divergence Signal + VEI > 1.2:
  → Skip or reduce size 50%+
```

### 5. **Momentum Oscillators**

**Why:** Adds momentum context to volume divergence

**With RSI:**

- Bullish divergence + RSI oversold (< 30) = Extremely high probability
- Bearish divergence + RSI overbought (> 70) = Extremely high probability
- Bullish divergence + RSI > 50 = Weaker signal
- Bearish divergence + RSI < 50 = Weaker signal

**With MACD:**

- Bullish divergence + MACD bullish crossover = Strong confirmation
- Bearish divergence + MACD bearish crossover = Strong confirmation
- Divergence before MACD cross = Early warning system

**Double Divergence (Holy Grail):**

```text
Price making lower lows
+ Bullish volume divergence (this indicator)
+ RSI making higher lows
= EXTREMELY HIGH PROBABILITY REVERSAL
```

### 6. **Price Action Patterns**

**Why:** Divergence signals best used with price confirmation

**Candlestick Confirmation:**

**For Bullish Divergence:**

- Hammer or bullish engulfing after divergence
- Pin bar rejection off support with divergence
- Morning star pattern with divergence on first candle

**For Bearish Divergence:**

- Shooting star or bearish engulfing after divergence
- Pin bar rejection at resistance with divergence
- Evening star pattern with divergence on first candle

**Chart Pattern Integration:**

- Bullish divergence in right shoulder of inverse H&S = High probability
- Bearish divergence in right shoulder of H&S = High probability
- Divergence at apex of triangle = Breakout direction hint

### 7. **Market Context**

**Why:** Broader market conditions affect signal reliability

**Order Flow Context:**

- Divergence + supportive tape reading = Stronger signal
- Divergence + order book showing size at level = Confirmation
- Divergence + market depth aligned = Institutional interest

**Correlation Analysis:**

- Divergence in stock + divergence in sector = Stronger signal
- Divergence in stock vs sector strength = Weaker signal (swim against current)
- Divergence across multiple correlated instruments = Market-wide shift

### 8. **Time and Session Analysis**

**Why:** Timing affects divergence signal quality

**With Your ORB Indicator:**

- Bullish divergence during ORB = Likely upside break
- Bearish divergence during ORB = Likely downside break
- Divergence at ORB boundaries = Direction confirmation

**Session-Based:**

- Divergence during high-volume sessions (London open, NY open) = More reliable
- Divergence during low-volume periods (Asia session, lunch) = Less reliable
- Divergence in first hour = Sets tone for day
- Divergence in last hour = Institutional positioning for next day

### 9. **Optimal Market Conditions**

**Best Conditions for This Indicator:**

✅ **Liquid, High-Volume Markets:**

- Sufficient volume for meaningful delta calculation
- Accurate up/down volume classification
- Major stocks, indices, futures during active hours

✅ **Trending or Mean-Reverting Markets:**

- Clear structure for context
- Defined support/resistance levels
- Predictable behavior after signals

✅ **Normal Volatility (VEI < 1.2):**

- Signals reliable and actionable
- Stop losses reasonable
- Structure respected

**Avoid Using When:**

❌ **Low Volume Conditions:**

- After hours, pre-market
- Holidays, summer doldrums
- Thinly traded instruments
- Small sample = unreliable delta

❌ **Extreme Volatility (VEI > 1.5):**

- Chaotic price action
- Signals may fail immediately
- Institutional flow overwhelmed by panic/euphoria

❌ **News Events:**

- During major economic releases
- Earnings announcements
- Central bank decisions
- Volume delta meaningless in panic/euphoria

---

## Trading Strategies

### Strategy 1: **Pure Divergence Reversal**

**Objective:** Trade reversals signaled by divergence clusters

**Entry Rules:**

**Long Setup:**

1. Identify downtrend or pullback
2. Wait for 2-3 consecutive bullish divergence signals
3. Divergence must occur at or near support level
4. Enter on first bullish candle after divergence cluster
5. Stop loss: Below divergence low

**Short Setup:**

1. Identify uptrend or rally
2. Wait for 2-3 consecutive bearish divergence signals
3. Divergence must occur at or near resistance level
4. Enter on first bearish candle after divergence cluster
5. Stop loss: Above divergence high

**Position Sizing:**

- Single divergence bar: 50% normal size
- 2 divergence bars: 75% normal size
- 3+ divergence bars: 100% normal size

**Profit Targets:**

- T1: 1.5R (50% position)
- T2: 3R (25% position)
- T3: Trail stop (25% position)

### Strategy 2: **Trend Pullback Entry**

**Objective:** Use divergence to time entries in established trends

**Long Setup (Uptrend):**

1. Confirm uptrend (price above 50 MA, or in upward channel)
2. Wait for pullback (price retraces 38-62%)
3. Bullish divergence appears during pullback
4. Enter long when divergence triggers
5. Stop: Below pullback low
6. Target: Trend continuation to previous high or beyond

**Short Setup (Downtrend):**

1. Confirm downtrend (price below 50 MA, or in downward channel)
2. Wait for rally (price retraces 38-62%)
3. Bearish divergence appears during rally
4. Enter short when divergence triggers
5. Stop: Above rally high
6. Target: Trend continuation to previous low or beyond

**Advantages:**

- Entering with trend (higher win rate)
- Divergence confirms pullback is opportunity, not reversal
- Better risk:reward (entering at retracement)

### Strategy 3: **Divergence + Structure Confluence**

**Objective:** Only trade divergences at key structural levels

**Setup Requirements (All Must Be Present):**

**For Longs:**

1. ✅ Major support level (previous low, Fibonacci, round number)
2. ✅ Bullish divergence signal (purple arrow)
3. ✅ Additional confirmation (RSI oversold, or Up/Down Ratio rising, or VEI < 1.0)
4. ✅ Bullish price action (engulfing, hammer, etc.)

**For Shorts:**

1. ✅ Major resistance level (previous high, Fibonacci, round number)
2. ✅ Bearish divergence signal (blue arrow)
3. ✅ Additional confirmation (RSI overbought, or Up/Down Ratio falling, or VEI < 1.0)
4. ✅ Bearish price action (shooting star, engulfing, etc.)

**If ANY criterion missing: Skip the trade.**

**Risk Management:**

- Tight stops (just beyond structural level)
- Large position size acceptable (high probability)
- Target: Opposite structural level

### Strategy 4: **Divergence Cluster Accumulation/Distribution**

**Objective:** Identify major accumulation/distribution zones

**Accumulation Zone (Bottom Building):**

1. Price in downtrend or after large decline
2. Multiple bullish divergences over several bars/days
3. Each attempt down shows buying pressure
4. Zone of accumulation being established

**Action:**

- Begin scaling into longs across the zone
- Average down as divergences appear
- Wide stop below entire zone
- Hold for major reversal and trend change
- Target: Previous highs or measured move

**Distribution Zone (Top Building):**

1. Price in uptrend or after large rally
2. Multiple bearish divergences over several bars/days
3. Each attempt up shows selling pressure
4. Zone of distribution being established

**Action:**

- Begin scaling into shorts or exiting longs across the zone
- Average up as divergences appear
- Wide stop above entire zone
- Hold for major reversal and trend change
- Target: Previous lows or measured move

**Note:** This is a position trading strategy, not day trading. Requires patience.

---

## Risk Warnings and Limitations

### 1. **Lower Timeframe Data Limitations**

**Issue:**

- Requires access to lower timeframe data
- Some data vendors don't provide sufficient granularity
- Historical data may be limited when using very low timeframes
- Higher timeframe charts have less precision (daily uses 5-min, not 1-min)

**Impact:**

- Indicator may not work on all instruments or time periods
- Historical backtesting limited by data availability
- Precision varies by chart timeframe

**Mitigation:**

- Use on liquid instruments with complete data
- Test custom timeframe settings if issues arise
- Verify data quality before relying on signals

### 2. **Not All Divergences Lead to Reversals**

**Issue:**

- Divergence shows institutions acting contrary to price
- But they might be wrong (institutions lose too)
- Or they might be too early (reversal takes time)
- Strong trends can override divergence signals

**Impact:**

- Some divergence signals will fail
- Especially in very strong momentum environments
- Need risk management and confirmation

**Mitigation:**

- Wait for price confirmation before entry
- Use stop losses consistently
- Require multiple signals or additional confirmation
- Filter with VEI and other indicators

### 3. **Threshold Setting Critical**

**Issue:**

- Default 20% threshold is general guidance
- Too low = too many signals (noise)
- Too high = too few signals (missing opportunities)
- Optimal threshold varies by instrument and timeframe

**Impact:**

- Default settings may not be optimal for your trading
- Need customization and testing

**Mitigation:**

- Backtest different threshold levels
- Start with 20% and adjust based on results
- Higher volatility instruments may need higher thresholds
- Lower volatility instruments may need lower thresholds

### 4. **Lagging Nature**

**Issue:**

- Signal appears after the bar closes
- By then, price may have already moved significantly
- Can't catch the absolute low/high

**Impact:**

- Entry may be several points away from optimal
- Risk:reward ratio reduced if chasing
- Need to wait for pullback after signal

**Mitigation:**

- Use limit orders at logical levels
- Wait for price to come back to you
- Don't chase—let the setup develop
- Consider entering partial position and adding on confirmation

### 5. **False Signals in Choppy Markets**

**Issue:**

- During consolidation or range-bound conditions
- Many small divergences back and forth
- No meaningful trend to confirm or reverse
- Noise overwhelming signal

**Impact:**

- Win rate drops in choppy conditions
- Whipsaw trades
- Frustration and losses

**Mitigation:**

- Filter with VEI (avoid trading when VEI > 1.2)
- Require trend context or structural level
- Increase threshold during choppy periods
- Consider sitting out during consolidation

### 6. **Delta Calculation Approximation**

**Issue:**

- True delta requires tick-by-tick order flow data
- This indicator approximates using lower timeframe bars
- Not as accurate as professional order flow tools
- Classification method (close vs open, close vs previous) is simplified

**Impact:**

- Delta may not perfectly reflect true institutional flow
- Some aggressive buying/selling may be misclassified
- Professional traders with Level 2 data have an edge

**Mitigation:**

- Understand this is an approximation, not perfect data
- Use as one tool among many
- Combine with price action and other confirmations
- Consider upgrading to professional order flow tools if serious

### 7. **Instrument-Specific Behavior**

**Issue:**

- Different instruments have different volume characteristics
- Crypto: 24/7 trading, different session dynamics
- Forex: No centralized volume (tick volume used)
- Stocks: Different behaviors by sector and market cap
- Futures: Roll dates and contract specifics matter

**Impact:**

- Signal quality varies by instrument type
- Some markets more reliable than others

**Mitigation:**

- Test thoroughly on your specific instruments
- Understand the quirks of your market
- Adjust settings per instrument if necessary

---

## Conclusion

The Price/Volume Delta Candles indicator provides a window into **hidden institutional behavior** by revealing when the "smart money" is acting contrary to obvious price action. This edge is invaluable for avoiding traps and catching reversals early.

### Key Takeaways

1. **Reveals hidden accumulation and distribution**
   - Bullish divergence: Buying pressure on down bars (accumulation)
   - Bearish divergence: Selling pressure on up bars (distribution)
   - Shows what institutions are doing vs. what price suggests

2. **Two primary applications:**
   - **Reversal detection**: Catching turns before they're obvious
   - **Continuation confirmation**: Verifying pullbacks are opportunities

3. **Most powerful at structural levels:**
   - Divergence at support = High probability long
   - Divergence at resistance = High probability short
   - Divergence in middle of nowhere = Lower priority

4. **Requires confirmation:**
   - Wait for price action confirmation (candle patterns)
   - Combine with volume regime (Up/Down Ratio)
   - Filter with volatility (VEI < 1.2 preferred)
   - Use multiple signals for highest confidence

5. **Cluster signals are strongest:**
   - Single divergence bar = Possible
   - 2-3 consecutive divergences = Probable
   - Multiple divergences at same level = Highly probable

### The Price/Volume Delta Edge

Most traders only see what price is doing. This indicator reveals what **volume is doing underneath**, often telling a completely different story:

- **Price drops, delta positive** = Institutions accumulating (bullish)
- **Price rallies, delta negative** = Institutions distributing (bearish)

This "under the hood" view allows you to:

- **Avoid bull traps** (price up, but selling underneath)
- **Avoid bear traps** (price down, but buying underneath)
- **Front-run reversals** (accumulation/distribution before obvious turn)
- **Join institutional flow** (trade with the big players)
- **Improve entry timing** (wait for divergence at key levels)

**The real edge:** While retail traders are reacting to price, you're seeing what institutions are doing—and institutions move markets. By following their flow revealed through volume delta divergence, you're aligning your trades with the players who have the power to move price in your favor.

---

**Best suited for:** Day traders, swing traders, and position traders in liquid markets who want to improve entry timing and catch reversals early. Essential for traders who understand that volume reveals truth while price can deceive. Works best in stocks, futures, and major indices with reliable volume data.

**Technical Note:** This indicator uses lower timeframe data (request.security_lower_tf) to approximate order flow. True institutional order flow requires Level 2/Time & Sales data, but this approximation is sufficient for most retail trading applications and provides significant edge over price-only analysis.
