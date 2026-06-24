---
title: Up/Down Volume Ratio
description: Momentum and sentiment tool comparing buying vs. selling volume pressure.
category: indicator
---

# Up/Down Volume Ratio Indicator Analysis

## Overview

The **Up/Down Volume Ratio** is a momentum and market sentiment indicator that measures the relationship between buying pressure (up volume) and selling pressure (down volume) over a specified period. By comparing the volume on up bars versus down bars, this indicator reveals whether bulls or bears are in control and helps traders identify shifts in market sentiment before they become obvious in price action.

## Table of Contents

- [How This Indicator Works](#how-this-indicator-works)
  - [Core Calculation](#core-calculation)
  - [Ratio Interpretation](#ratio-interpretation)
  - [Visual Components](#visual-components)
- [How Traders Can Use This to Find an Edge](#how-traders-can-use-this-to-find-an-edge)
  - [Trend Confirmation and Strength](#1-trend-confirmation-and-strength)
  - [Divergence Detection](#2-divergence-detection)
  - [Market Regime Identification](#3-market-regime-identification)
  - [Entry and Exit Timing](#4-entry-and-exit-timing)
- [Complementary Indicators and Market Conditions](#complementary-indicators-and-market-conditions)
- [Trading Strategies](#trading-strategies)
- [Risk Warnings and Limitations](#risk-warnings-and-limitations)
- [Conclusion](#conclusion)

---

## How This Indicator Works

### Core Calculation

The indicator follows a simple but effective three-step process:

#### Step 1: Classify Volume by Bar Direction

```text
If Close > Previous Close:
    Up Volume = Current Bar Volume
    Down Volume = 0

If Close < Previous Close:
    Up Volume = 0
    Down Volume = Current Bar Volume

If Close = Previous Close:
    Up Volume = 0
    Down Volume = 0 (neutral bars excluded)
```

#### Step 2: Smooth with Moving Average

```text
Sum Up = SMA(Up Volume, 50 periods)  [default]
Sum Down = SMA(Down Volume, 50 periods)  [default]
```

#### Step 3: Calculate Ratio

```text
Up/Down Volume Ratio = Sum Up / Sum Down
```

### Ratio Interpretation

The ratio reveals the balance of power between buyers and sellers:

#### **Ratio < 1.0 (Bearish Zone)**

**Meaning:**

- Down volume exceeds up volume
- Sellers are more aggressive than buyers
- Distribution phase or downtrend
- Red/bearish pressure dominant

**Characteristics:**

- More volume occurs on down bars
- Participants selling into weakness
- Supply > Demand at current prices
- Potential downside momentum

**Examples:**

- Ratio = 0.5: Down volume is 2x up volume (strong selling)
- Ratio = 0.8: Down volume is 1.25x up volume (moderate selling)

#### **Ratio = 1.0 (Equilibrium)**

**Meaning:**

- Up volume equals down volume
- Balance between buyers and sellers
- Neutral market sentiment
- Transition or consolidation phase

**Characteristics:**

- No clear directional bias in volume flow
- Market indecision or balance
- Often seen during ranges or after major moves
- Can precede directional breakouts

#### **Ratio 1.0 - 2.0 (Mildly Bullish - Orange Zone)**

**Meaning:**

- Up volume exceeds down volume moderately
- Buyers slightly more aggressive
- Accumulation phase beginning
- Normal bullish conditions

**Characteristics:**

- More volume on up bars than down bars
- Healthy uptrend characteristics
- Demand > Supply, but not extreme
- Sustainable buying pressure

**Examples:**

- Ratio = 1.5: Up volume is 1.5x down volume (moderate buying)
- Ratio = 1.8: Up volume is 1.8x down volume (strong buying)

#### **Ratio ≥ 2.0 (Strongly Bullish - Green Zone)**

**Meaning:**

- Up volume significantly exceeds down volume
- Buyers overwhelmingly aggressive
- Strong accumulation or momentum phase
- Powerful bullish sentiment

**Characteristics:**

- Up volume at least 2x down volume
- Intense buying pressure
- Often accompanies strong uptrends
- Can indicate climactic buying (caution)

**Examples:**

- Ratio = 2.0: Up volume is 2x down volume
- Ratio = 3.0: Up volume is 3x down volume (extreme)
- Ratio > 4.0: Potential exhaustion/blow-off top

### Visual Components

#### 1. Ratio Line

- **Gray**: Ratio < 1.0 (bearish)
- **Orange**: Ratio 1.0 - 2.0 (mildly bullish)
- **Green**: Ratio ≥ 2.0 (strongly bullish)

#### 2. Reference Lines

- **1.0 Line** (white, faint): Equilibrium level
- **2.0 Line** (white, visible): Strong bullish threshold

#### 3. Background Highlighting

- **Light Green**: Ratio ≥ 2.0 (strong buying pressure)
- **Light White**: Ratio 1.0 - 2.0 (moderate buying)
- **No highlight**: Ratio < 1.0 (selling pressure)

---

## How Traders Can Use This to Find an Edge

### 1. **Trend Confirmation and Strength**

The Up/Down Volume Ratio confirms whether price trends are backed by genuine conviction or are simply technical moves with weak participation.

#### **Healthy Uptrend Characteristics:**

✅ **Price rising + Ratio > 1.0** = Confirmed uptrend

- Volume supports the move
- Buyers are in control
- Trend likely to continue
- Safe to hold long positions

✅ **Price rising + Ratio ≥ 2.0** = Very strong uptrend

- Exceptional buying pressure
- High-conviction move
- Consider holding until ratio weakens
- Can signal intermediate peak if sustained at extremes

#### **Weak/Suspect Uptrend:**

⚠️ **Price rising + Ratio < 1.0** = Unconfirmed rally

- Price going up but volume is down-biased
- Low conviction rally
- Likely to fail or consolidate
- Warning: Don't chase this rally
- Consider taking profits on longs

#### **Healthy Downtrend Characteristics:**

✅ **Price falling + Ratio < 1.0** = Confirmed downtrend

- Volume supports the decline
- Sellers are in control
- Downtrend likely to continue
- Stay defensive or short

#### **Weak/Suspect Downtrend:**

⚠️ **Price falling + Ratio > 1.0** = Unconfirmed decline

- Price going down but volume is up-biased
- Potential selling exhaustion
- Accumulation during pullback
- Look for reversal opportunities

### 2. **Divergence Detection**

Divergences between price and the Up/Down Volume Ratio are powerful reversal signals.

#### **Bullish Divergence**

**Setup:**

- Price makes lower low
- Up/Down Ratio makes higher low (or stays flat)
- Volume distribution improving even as price weakens

**Interpretation:**

- Selling pressure waning
- Buyers stepping in at lower levels
- Potential trend reversal approaching
- Distribution ending, accumulation beginning

**Action:**

- Watch for price reversal signals (bullish candle patterns, trendline breaks)
- Consider long entry on confirmation
- Place stops below the divergence low
- Target previous resistance levels

**Example:**

```text
Price:  100 → 95 → 90 (lower lows)
Ratio:  0.6 → 0.8 → 1.1 (improving)
Signal: Bullish divergence - buyers absorbing selling
```

#### **Bearish Divergence**

**Setup:**

- Price makes higher high
- Up/Down Ratio makes lower high (or declining)
- Volume distribution weakening even as price rises

**Interpretation:**

- Buying pressure waning
- Fewer participants supporting the rally
- Potential trend reversal approaching
- Accumulation ending, distribution beginning

**Action:**

- Watch for price reversal signals (bearish candle patterns, resistance rejection)
- Consider taking profits on longs or initiating shorts
- Place stops above the divergence high
- Target previous support levels

**Example:**

```text
Price:  100 → 105 → 110 (higher highs)
Ratio:  2.5 → 1.8 → 1.2 (declining)
Signal: Bearish divergence - buyers losing conviction
```

### 3. **Market Regime Identification**

Use the ratio to identify the current market regime and adjust strategy accordingly.

#### **Bullish Regime (Ratio sustained > 1.5)**

**Characteristics:**

- Consistent buying pressure
- Participants willing to buy dips
- Strong hands accumulating
- Uptrend environment

**Trading Approach:**

- Bias to long side
- Buy pullbacks to support
- Hold winners longer
- Be patient with entries
- Avoid fighting the tape with shorts

**Risk Management:**

- Wider stops acceptable
- Trail stops below moving averages
- Size up on best setups

#### **Bearish Regime (Ratio sustained < 0.8)**

**Characteristics:**

- Consistent selling pressure
- Participants selling rallies
- Weak hands distributing
- Downtrend environment

**Trading Approach:**

- Bias to short side or cash
- Sell rallies to resistance
- Exit longs quickly
- Be selective with longs
- Avoid "catching falling knives"

**Risk Management:**

- Tight stops on long positions
- Quick exits on failed bounces
- Reduce overall position size

#### **Neutral Regime (Ratio 0.8 - 1.3)**

**Characteristics:**

- Balanced buying and selling
- No clear directional bias
- Range-bound conditions likely
- Low conviction environment

**Trading Approach:**

- Range trading strategies
- Fade extremes
- Quick in-and-out trades
- Avoid trend-following
- Wait for regime change confirmation

### 4. **Entry and Exit Timing**

#### **Entry Signals:**

**Long Entry:**

1. **Ratio crosses above 1.0** (momentum shift to bulls)
   - Enter on pullback to support
   - Confirm with price action
2. **Ratio rises to ≥ 2.0** during uptrend (strength confirmation)
   - Add to existing longs
   - Stay with the momentum
3. **Bullish divergence confirmed** (reversal setup)
   - Enter on price confirmation
   - Initial reversal trade

**Short Entry (or Long Exit):**

1. **Ratio crosses below 1.0** (momentum shift to bears)
   - Exit longs or initiate shorts
   - Momentum has turned
2. **Ratio falls below 0.8** (strong selling)
   - Confirmed weakness
   - Short rallies to resistance
3. **Bearish divergence confirmed** (reversal setup)
   - Exit longs on price confirmation
   - Consider shorts if appropriate

#### **Exit Signals:**

**Exit Long When:**

- Ratio drops below 1.0 (losing momentum)
- Ratio spikes above 3.0-4.0 (possible exhaustion)
- Bearish divergence forms
- Price breaks key support with declining ratio

**Exit Short When:**

- Ratio rises above 1.0 (losing momentum)
- Bullish divergence forms
- Price breaks key resistance with rising ratio
- Ratio sustains above 1.5 (regime change)

---

## Complementary Indicators and Market Conditions

### 1. **Price Trend Indicators**

**Why:** Up/Down Ratio shows conviction; trend indicators show direction

**Best Combinations:**

**With Moving Averages:**

- Price above 50 MA + Ratio > 1.5 = Strong uptrend confirmation
- Price below 50 MA + Ratio < 0.8 = Strong downtrend confirmation
- Price above MA but Ratio < 1.0 = Weak rally, caution

**With Your MA High/Low Indicator:**

- Price above channel + Ratio ≥ 2.0 = Extremely strong long setup
- Price within channel + Ratio < 1.0 = Wait for direction
- Price below channel + Ratio < 0.8 = Strong short setup
- Price breakout + declining ratio = False breakout warning

### 2. **Volume Analysis Tools**

**Why:** Provides additional volume context beyond up/down classification

**With On-Balance Volume (OBV):**

- OBV rising + Ratio > 1.0 = Strong confirmation
- OBV falling + Ratio < 1.0 = Strong confirmation
- OBV rising + Ratio < 1.0 = Investigate further (mixed signals)

**With Volume Profile:**

- High Volume Node + Ratio improving = Strong support/accumulation zone
- High Volume Node + Ratio deteriorating = Strong resistance/distribution zone

**With Your Price/Volume Delta Indicators:**

- Positive delta + High ratio = Maximum bullish conviction
- Negative delta + Low ratio = Maximum bearish conviction
- Divergence between indicators = Early warning system

### 3. **Momentum Oscillators**

**Why:** Confirms momentum shifts alongside volume shifts

**With RSI:**

- RSI oversold + Ratio bottoming/rising = High-probability long
- RSI overbought + Ratio topping/falling = High-probability short
- RSI divergence + Ratio divergence = Very strong reversal signal

**With MACD:**

- MACD crossover bullish + Ratio > 1.0 = Confirmed trend change
- MACD crossover bearish + Ratio < 1.0 = Confirmed trend change

### 4. **Volatility Indicators**

**Why:** Volume behavior changes with volatility regimes

**With VEI (Volatility Expansion Index):**

- VEI < 1.0 + Ratio > 1.5 = Clean, strong uptrend (best conditions)
- VEI > 1.2 + Ratio > 2.0 = Potential climax/exhaustion
- VEI > 1.2 + Ratio unstable = Avoid trading (chaotic)

**With Bollinger Bands:**

- Price at lower BB + Ratio rising = Potential reversal
- Price at upper BB + Ratio falling = Potential reversal
- BB squeeze + Ratio shifting = Breakout direction hint

### 5. **Market Structure**

**Why:** Ratio signals more reliable at key structural levels

**At Support/Resistance:**

- Price at support + Ratio > 1.0 = Strong support likely to hold
- Price at support + Ratio < 1.0 = Support likely to break
- Price at resistance + Ratio > 2.0 = Resistance likely to break
- Price at resistance + Ratio declining = Resistance likely to hold

### 6. **Breadth Indicators (For Equity Indices)**

**Why:** Confirms whether volume distribution is market-wide or isolated

**With Advance/Decline Line:**

- A/D line rising + Ratio > 1.0 = Broad market strength
- A/D line falling + Ratio < 1.0 = Broad market weakness
- A/D line rising + Ratio < 1.0 = Narrow rally (caution)

### 7. **Session/Time Analysis**

**Why:** Volume patterns vary by trading session

**With Your ORB Indicator:**

- ORB breakout + Ratio > 1.5 = High-conviction breakout
- ORB breakout + Ratio < 1.0 = Likely false breakout
- Morning session: Ratio establishes daily bias
- Afternoon session: Ratio confirms/rejects morning move

### 8. **Optimal Market Conditions**

**Best Conditions for This Indicator:**

✅ **Liquid Markets:**

- High volume stocks, major indices
- Forex major pairs during active sessions
- Futures during pit hours
- Sufficient volume for meaningful statistics

✅ **Trending Markets:**

- Clear directional bias
- Sustained moves in one direction
- Ratio confirms trend strength effectively

✅ **Medium-to-High Volatility:**

- Enough price movement to generate meaningful up/down bars
- Better signal clarity

**Avoid Using When:**

❌ **Low Volume Markets:**

- After-hours trading
- Thinly traded stocks
- Holidays/light volume days
- Small sample size = unreliable ratio

❌ **Extremely Choppy Markets:**

- Many doji bars (close = previous close)
- Very small bars relative to normal
- High-frequency oscillation

❌ **Gap-Heavy Trading:**

- Overnight gaps dominate intraday movement
- Volume classification less meaningful

---

## Trading Strategies

### Strategy 1: **Volume-Confirmed Trend Following**

**Objective:** Only take trend trades when volume supports the move

**Long Entry Criteria:**

1. Price in uptrend (above 50 MA or in upward channel)
2. Up/Down Ratio > 1.3
3. Pullback to support (MA, trendline, or channel)
4. Entry on bounce with confirmation

**Management:**

- Hold while Ratio stays > 1.0
- Exit when Ratio crosses below 1.0
- Trail stops below support levels

**Short Entry Criteria:**

1. Price in downtrend (below 50 MA or in downward channel)
2. Up/Down Ratio < 0.8
3. Rally to resistance
4. Entry on rejection with confirmation

**Management:**

- Hold while Ratio stays < 1.0
- Exit when Ratio crosses above 1.0
- Trail stops above resistance levels

### Strategy 2: **Divergence Reversal Trading**

**Objective:** Catch trend reversals early using volume divergence

**Bullish Setup:**

1. Identify price making lower low
2. Confirm Up/Down Ratio making higher low
3. Wait for price reversal signal (bullish engulfing, trendline break, etc.)
4. Enter long with stop below divergence low

**Targets:**

- First target: Previous swing high
- Second target: Major resistance level
- Trail stop once Ratio > 1.5

**Bearish Setup:**

1. Identify price making higher high
2. Confirm Up/Down Ratio making lower high
3. Wait for price reversal signal (bearish engulfing, resistance rejection)
4. Enter short or exit longs with stop above divergence high

**Targets:**

- First target: Previous swing low
- Second target: Major support level

### Strategy 3: **Regime-Based Position Sizing**

**Objective:** Adjust exposure based on volume regime

**Position Sizing Rules:**

```text
Ratio ≥ 2.0 (Very Bullish):
- Long positions: 100-125% normal size
- Short positions: 0-25% normal size
- Bias: Aggressively long

Ratio 1.3 - 2.0 (Bullish):
- Long positions: 100% normal size
- Short positions: 50% normal size
- Bias: Moderately long

Ratio 0.8 - 1.3 (Neutral):
- Long positions: 50% normal size
- Short positions: 50% normal size
- Bias: Neutral, selective both sides

Ratio 0.5 - 0.8 (Bearish):
- Long positions: 25-50% normal size
- Short positions: 100% normal size
- Bias: Moderately short/defensive

Ratio < 0.5 (Very Bearish):
- Long positions: 0-25% normal size
- Short positions: 100-125% normal size
- Bias: Defensive or aggressively short
```

### Strategy 4: **Extreme Reading Mean Reversion**

**Objective:** Fade extremes when ratio reaches unsustainable levels

**Long Setup (Oversold):**

1. Ratio drops below 0.5 (extreme selling)
2. Price at major support level
3. RSI oversold (< 30)
4. Look for reversal candle
5. Enter long, targeting ratio return to 1.0

**Risk:** Very short stop below support; this is a reversal trade

**Short Setup (Overbought):**

1. Ratio rises above 3.0-4.0 (extreme buying)
2. Price at major resistance level
3. RSI overbought (> 70)
4. Look for reversal candle
5. Enter short or exit longs, targeting ratio return to 1.5-2.0

**Risk:** Very short stop above resistance; this is a reversal trade

---

## Risk Warnings and Limitations

### 1. **Neutral Bars Excluded**

**Issue:**

- When Close = Previous Close (doji, inside bars), no volume is assigned
- On very low volatility days, many bars may be excluded
- Can distort the ratio by ignoring significant volume

**Impact:**

- Less accurate during tight ranges
- Small sample size in low volatility
- Ratio may not reflect true volume distribution

**Mitigation:**

- Use longer lookback periods (50+ bars)
- Avoid relying on indicator during extreme low volatility
- Cross-reference with other volume indicators

### 2. **Smoothing Lag**

**Issue:**

- 50-period SMA creates significant lag
- Ratio slow to respond to sudden sentiment shifts
- May miss early reversal signals

**Impact:**

- Not ideal for very short-term trading (scalping)
- Regime changes confirmed late
- Fast momentum shifts may be delayed

**Mitigation:**

- Use shorter periods for faster response (trade-off: more noise)
- Combine with faster momentum indicators
- Watch for price action confirmation

### 3. **Extreme Readings Can Persist**

**Issue:**

- Ratio ≥ 2.0 or ≤ 0.5 can remain at extremes during strong trends
- Fading extremes prematurely = fighting strong trends
- "Overbought can stay overbought"

**Impact:**

- Contrarian signals may fail during momentum moves
- Extreme readings don't guarantee reversal
- Can lead to early exits from profitable trades

**Mitigation:**

- Don't automatically fade extremes
- Wait for price confirmation of reversal
- Use trend indicators to determine if in trending or mean-reverting regime

### 4. **Volume Quality Issues**

**Issue:**

- Not all volume is equal (retail vs institutional, aggressive vs passive)
- Large single trades can skew the ratio
- After-hours or pre-market volume may be distorted

**Impact:**

- Ratio may not reflect true buying/selling pressure
- One large trade can temporarily affect the indicator
- Quality of volume information varies

**Mitigation:**

- Focus on liquid, high-volume markets
- Avoid using in illiquid conditions
- Consider using order flow tools for deeper analysis

### 5. **Doesn't Show Position in Distribution**

**Issue:**

- Ratio only shows current balance, not absolute levels
- Can't tell if high ratio is sustainable or climactic
- No context for "normal" vs "extreme"

**Impact:**

- Need historical context to interpret readings
- Same ratio may mean different things in different markets
- Requires experience to gauge significance

**Mitigation:**

- Study historical ratio behavior for your specific market
- Use multiple timeframes for context
- Combine with price structure analysis

### 6. **Market-Specific Calibration**

**Issue:**

- Different markets have different "normal" ratio ranges
- Volatile stocks may regularly see extremes
- Conservative stocks may rarely exceed 1.5

**Impact:**

- Can't use same thresholds for all markets
- What's "extreme" in one market is normal in another
- Requires customization

**Mitigation:**

- Backtest threshold levels for your specific markets
- Adjust reference lines to your trading instruments
- Maintain separate profiles for different asset classes

---

## Conclusion

The Up/Down Volume Ratio is a powerful tool for understanding the **balance of power** between buyers and sellers through the lens of volume distribution. Unlike pure price indicators, it reveals the underlying conviction and participation that drives price movements.

### Key Takeaways

1. **Measures buying vs selling pressure**
   - Simple ratio: Up volume / Down volume
   - Smoothed over 50 periods (default)
   - Clear interpretation: > 1.0 bullish, < 1.0 bearish

2. **Three primary uses:**
   - **Trend confirmation**: Does volume support the price move?
   - **Divergence detection**: Is sentiment shifting before price?
   - **Regime identification**: What's the current market bias?

3. **Most powerful at extremes:**
   - Ratio ≥ 2.0: Strong bullish sentiment (stay long or add)
   - Ratio ≤ 0.5: Strong bearish sentiment (stay defensive)
   - Ratio near 1.0: Neutral (wait for clarity)

4. **Excels at preventing bad trades:**
   - Filters out weak rallies (price up, ratio < 1.0)
   - Warns of false breakdowns (price down, ratio > 1.0)
   - Identifies low-conviction moves to avoid

5. **Best used with confirmation:**
   - Combine with price trend indicators
   - Cross-reference with momentum oscillators
   - Integrate with your other volume tools
   - Use price action for entry/exit timing

### The Up/Down Volume Ratio Edge

Most traders focus exclusively on price. The Up/Down Volume Ratio adds a critical dimension: **Are participants committed to this move?** This allows you to:

- **Trade with conviction** when volume confirms price
- **Stay cautious** when volume contradicts price
- **Spot reversals early** through divergence
- **Adjust position sizing** based on market regime
- **Avoid traps** where price moves without volume support

**The real edge:** This indicator helps you distinguish between **sustainable moves backed by conviction** and **technical price movements lacking commitment**. In trading, knowing whether the crowd is truly behind a move is often more valuable than knowing where price is going.

---

**Best suited for:** Swing traders, day traders, and position traders in liquid markets. Particularly valuable for traders who want volume confirmation of price moves and early warning of sentiment shifts. Works well across all liquid markets—stocks, indices, forex (with appropriate volume data), and futures.

**Attribution:** This indicator is based on the "Up/Dn Vol Ratio" by @CarusoInsights with modifications by @teamtomkins23.
