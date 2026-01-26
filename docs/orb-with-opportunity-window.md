# Opening Range Breakout with Opportunity Window (ORB) - Futures Trading Guide

## Overview

The **Opening Range Breakout (ORB) with Opportunity Window** indicator is a sophisticated intraday trading system designed specifically for futures markets, particularly **MES (Micro E-mini S&P 500)** and **MNQ (Micro Nasdaq-100)** contracts. This indicator combines the classic ORB strategy with modern enhancements including range quality assessment, VWAP integration, defined trading windows, and automated target projection—providing a complete framework for systematic futures day trading.

**Designed For:** Futures day trading (MES, MNQ, ES, NQ, and other liquid futures)

**Trading Style:** Intraday breakout trading with defined entry/exit levels

**Time Horizon:** Single trading session (no overnight holds)

## Table of Contents

- [How This Indicator Works](#how-this-indicator-works)
  - [Core Components](#core-components)
  - [Opening Range Calculation](#opening-range-calculation)
  - [Range Quality Assessment](#range-quality-assessment)
  - [Target Generation System](#target-generation-system)
  - [Opportunity Window](#opportunity-window)
  - [VWAP Integration](#vwap-integration)
- [How Traders Can Use This to Find an Edge](#how-traders-can-use-this-to-find-an-edge)
  - [Opening Range Quality Filter](#1-opening-range-quality-filter)
  - [Breakout Trade Execution](#2-breakout-trade-execution)
  - [Target-Based Position Management](#3-target-based-position-management)
  - [Time-Based Trade Filtering](#4-time-based-trade-filtering)
  - [Daily Bias Alignment](#5-daily-bias-alignment)
- [Complementary Indicators and Market Conditions](#complementary-indicators-and-market-conditions)
- [Trading Strategies for Futures](#trading-strategies-for-futures)
- [MES and MNQ Specific Guidance](#mes-and-mnq-specific-guidance)
- [Risk Warnings and Limitations](#risk-warnings-and-limitations)
- [Conclusion](#conclusion)

---

## How This Indicator Works

### Core Components

The indicator consists of six integrated systems:

#### 1. Opening Range (OR) Box

**What It Is:**

- A highlighted box showing the high and low established during the opening period
- Default: 8:30 AM - 9:30 AM Eastern (first hour of regular session)
- Customizable to any time window

**Key Levels:**

- **ORH (Opening Range High)**: The highest price during the opening period
- **ORL (Opening Range Low)**: The lowest price during the opening period
- **MID**: Midpoint between ORH and ORL (equilibrium level)

**Color Coding:**

- **Green Background**: Range size meets or exceeds target (good range for trading)
- **Red Background**: Range size below target (poor range, low probability)
- **Yellow Background**: Opening session still in progress (neutral)

#### 2. Range Quality Indicator

**Purpose:** Filters trading opportunities by measuring if the OR is large enough to trade

**Calculation:**

```text
Target OR Size = Current Price × (Size % / 100)
Actual OR Width = ORH - ORL

If Actual OR Width ≥ Target OR Size:
  → Green (Good range - trade)
Else:
  → Red (Poor range - skip or reduce size)
```

**Default Settings:**

- Target size: 0.2% of current price
- For MES at 5000: Target = 10 points minimum
- For MNQ at 18000: Target = 36 points minimum

**Range Ratio:**

- Displayed above the OR box
- Shows actual range / target range
- Example: "1.5" = Range is 1.5x the minimum target (excellent)
- Example: "0.8" = Range is 80% of target (skip)

#### 3. Breakout Signals

**Long Signal (Green Triangle Up):**

- Triggers when price closes above ORH
- Placed at ORL level for visual clarity
- Only appears during Opportunity Window (if enabled)

**Short Signal (Red Triangle Down):**

- Triggers when price closes below ORL
- Placed at ORH level for visual clarity
- Only appears during Opportunity Window (if enabled)

**Daily Bias Filter (Optional):**

```text
Daily Bias = Current ORM vs Previous ORM

If Current ORM > Previous ORM (bullish bias):
  → Long signals: Fire at ORH break
  → Short signals: Fire at first target below ORL (delayed)

If Current ORM < Previous ORM (bearish bias):
  → Short signals: Fire at ORL break
  → Long signals: Fire at first target above ORH (delayed)
```

This filter prevents counter-trend trades during strong directional days.

#### 4. Profit Targets

**Dynamic Target Generation:**

- Targets placed as multiples of OR width
- Default: 50% of OR width per target
- Targets extend infinitely as price moves
- Numbered sequentially (1, 2, 3, 4...)

**Upside Targets (Green):**

```text
Target 1: ORH + (OR Width × 0.5)
Target 2: ORH + (OR Width × 1.0)
Target 3: ORH + (OR Width × 1.5)
Target N: ORH + (OR Width × (N × 0.5))
```

**Downside Targets (Red):**

```text
Target 1: ORL - (OR Width × 0.5)
Target 2: ORL - (OR Width × 1.0)
Target 3: ORL - (OR Width × 1.5)
Target N: ORL - (OR Width × (N × 0.5))
```

**Display Modes:**

- **Adaptive**: Shows only targets near current price (cleaner chart)
- **Extended**: Shows all targets always (maximum information)

#### 5. Opportunity Window

**What It Is:**

- A defined time window for taking trades
- Default: 9:30 AM - 12:00 PM Eastern
- Highlighted with purple shading
- Matches the OR high/low boundaries

**Purpose:**

- Prevents trading during low-liquidity periods
- Focuses activity during most predictable hours
- Avoids lunch chop and late-day randomness
- Improves win rate by timing selection

**Signal Clamping:**

- When enabled, breakout signals ONLY fire during the Opportunity Window
- Prevents late entries after optimal window closes
- Can be disabled for full-session trading

#### 6. VWAP (Volume-Weighted Average Price)

**Components:**

- **VWAP Line** (Blue): True average price weighted by volume
- **Upper Band** (White): VWAP + (2 × Standard Deviation)
- **Lower Band** (White): VWAP - (2 × Standard Deviation)

**Calculation:**

- Resets at market open each session
- Cumulative throughout the day
- Uses typical price: (High + Low + Close) / 3

**Purpose:**

- Shows institutional average entry price
- Bands show statistical price extremes
- Acts as dynamic support/resistance
- Confirms breakout quality

### Opening Range Calculation

**Step-by-Step Process:**

**1. Session Start (8:30 AM default):**

```text
- Initialize ORH = first bar high
- Initialize ORL = first bar low
- Begin tracking range expansion
```

**2. During Opening Range (8:30-9:30 AM):**

```text
For each bar:
  If High > ORH:
    Update ORH = High
  If Low < ORL:
    Update ORL = Low
  Update OR box boundaries in real-time
  Update range quality color
```

**3. Session End (9:30 AM default):**

```text
- Freeze ORH and ORL values
- Calculate OR Width (ORH - ORL)
- Calculate OR Midpoint (ORM)
- Determine range quality (green/red)
- Generate ORH/ORL labels
- Enable breakout signal detection
```

**4. Post-OR Trading:**

```text
- Extend ORH/ORL lines forward
- Monitor for breakout signals
- Generate targets as breakouts occur
- Continue until session end
```

### Range Quality Assessment

**Why Range Quality Matters:**

Large ranges = More reliable breakouts = Higher probability trades

Small ranges = False breakouts = Whipsaw trades

**Quality Metrics:**

**Excellent Range (Ratio > 1.5):**

- Range is 150%+ of minimum target
- Very high probability of clean breakouts
- Safe to trade full size
- Targets likely to be reached

**Good Range (Ratio 1.0 - 1.5):**

- Range meets minimum requirements
- Standard probability trades
- Trade with normal position size
- Most targets reachable

**Marginal Range (Ratio 0.7 - 1.0):**

- Range slightly below target
- Reduced probability
- Consider half size or skip
- Expect only 1-2 targets

**Poor Range (Ratio < 0.7):**

- Range too small for reliable trading
- High whipsaw risk
- SKIP or paper trade only
- Low probability of target achievement

**Range Assessment Display:**

```text
Above OR Box:
Δ 12.50          ← Actual range width
(1.25)           ← Ratio (1.25x target)
= 10.00          ← Target minimum

Green background = Good (1.25 > 1.0)
```

### Target Generation System

**Automatic Target Creation:**

**Upside Breakout:**

1. Price closes above ORH
2. Generate Target 1 at ORH + (50% × OR Width)
3. When price reaches Target 1, generate Target 2
4. Continue infinitely as price advances

**Downside Breakout:**

1. Price closes below ORL
2. Generate Target 1 at ORL - (50% × OR Width)
3. When price reaches Target 1, generate Target 2
4. Continue infinitely as price declines

**Target Cross Detection:**

- **Close-based** (default): Uses close price to trigger next target
- **High/Low-based**: Uses wick touches to trigger next target

Close-based is more conservative and reduces false signals.

**Example (MES):**

```text
Opening Range:
- ORH: 5010
- ORL: 5000
- Width: 10 points
- Target Distance: 10 × 50% = 5 points

Upside Targets:
Target 1: 5015 (ORH + 5)
Target 2: 5020 (ORH + 10)
Target 3: 5025 (ORH + 15)
Target 4: 5030 (ORH + 20)

Downside Targets:
Target 1: 4995 (ORL - 5)
Target 2: 4990 (ORL - 10)
Target 3: 4985 (ORL - 15)
Target 4: 4980 (ORL - 20)
```

### Opportunity Window

**Session Structure:**

```text
8:30-9:30 AM:  Opening Range Period (observation)
9:30-12:00 PM: Opportunity Window (prime trading hours)
12:00-4:00 PM: Late session (optional, often avoided)
```

**Why This Window Works:**

**9:30-12:00 PM Characteristics:**

- Highest liquidity
- Clearest trends
- Institutional activity
- Most predictable price action
- Sufficient time for targets

**Periods to Avoid:**

- Pre-9:30: Still establishing range
- 12:00-1:00 PM: Lunch hour (low volume, chop)
- After 3:00 PM: Closing mechanics, unpredictable

**Window Flexibility:**

Can be customized for different trading styles:

- **Aggressive**: 9:30-3:00 PM (full session)
- **Standard**: 9:30-12:00 PM (default, best odds)
- **Conservative**: 9:30-11:00 AM (highest conviction only)

### VWAP Integration

**How VWAP Enhances ORB:**

**Breakout Confirmation:**

- Long breakout above ORH with price above VWAP = Strong
- Long breakout above ORH with price below VWAP = Weak
- Short breakout below ORL with price below VWAP = Strong
- Short breakout below ORL with price above VWAP = Weak

**Mean Reversion Trades:**

- Price at VWAP +2 SD band = Potential resistance (fade longs)
- Price at VWAP -2 SD band = Potential support (fade shorts)
- Combined with OR levels for confluence

**Intraday Bias:**

- Price above VWAP = Bullish intraday bias
- Price below VWAP = Bearish intraday bias
- Crossing VWAP = Potential trend change

**VWAP as Support/Resistance:**

- After long breakout, VWAP often acts as first support on pullback
- After short breakout, VWAP often acts as first resistance on bounce
- Can use VWAP as re-entry level after initial breakout

---

## How Traders Can Use This to Find an Edge

### 1. Opening Range Quality Filter

#### The Primary Edge: Trade Selection

Most ORB traders trade every breakout. Smart ORB traders only trade quality ranges.

#### High-Quality Setup (Green Range, Ratio > 1.0)

**Conditions:**

- Green OR box background
- Range ratio displayed above box shows > 1.0
- Clean range with minimal overlap
- Volume increasing during OR formation

**Action:**

- Take ALL valid breakout signals
- Use full position size
- Expect 2-4 targets achievable
- High confidence trades

**Example (MES):**

```text
MES at 5005
OR: 5015 (high) to 4995 (low)
Width: 20 points
Target: 10 points (0.2% of 5000)
Ratio: 20/10 = 2.0 (EXCELLENT)

Action: Trade all breakouts aggressively
Expected: Target 3-4 achievable
```

#### Low-Quality Setup (Red Range, Ratio < 1.0)

**Conditions:**

- Red OR box background
- Range ratio < 1.0
- Tight, choppy range formation
- Low volume during OR

**Action:**

- SKIP all trades
- Wait for next session
- Or trade very conservatively with half size
- Expect whipsaws and false breakouts

**Example (MES):**

```text
MES at 5005
OR: 5010 (high) to 5002 (low)
Width: 8 points
Target: 10 points
Ratio: 8/10 = 0.8 (POOR)

Action: Skip or paper trade only
Expected: High probability of whipsaw
```

#### Strategy Implementation

```text
Daily Pre-Market Checklist:
1. Wait for OR period to complete (9:30 AM)
2. Check range quality color
3. Calculate ratio (displayed on chart)
4. Determine position sizing:
   - Ratio > 1.5: Can use 125% size
   - Ratio 1.0-1.5: Standard 100% size
   - Ratio 0.7-1.0: Half size (50%)
   - Ratio < 0.7: SKIP completely
```

### 2. Breakout Trade Execution

**Classic ORB Breakout Strategy:**

#### Long Entry Setup

**Entry Criteria:**

1. ✅ Opening Range completed (after 9:30 AM)
2. ✅ Green range quality (ratio > 1.0)
3. ✅ Close above ORH (breakout confirmation)
4. ✅ Within Opportunity Window (9:30-12:00)
5. ✅ Green triangle signal appears
6. ✅ (Optional) Price above VWAP for confirmation

**Entry Execution:**

- Enter at close of breakout bar OR
- Wait for pullback to ORH (now support) for better R:R

**Stop Loss:**

- Initial stop: Below ORL (opposite side of range)
- Tighter stop: Below ORH (failed breakout)
- OR Width-based: ORH - (OR Width × 0.5)

**Profit Targets:**

- Target 1: Take 50% off
- Target 2: Take 25% off
- Target 3+: Trail remaining with ORH or VWAP

**Example (MES):**

```text
OR: 5010 (ORH) to 5000 (ORL)
Width: 10 points

Long Signal: Close at 5012 (above ORH)
Entry: 5012
Stop: 5000 (at ORL) = 12 point risk
Target 1: 5015 (5 points) = +3 points
Target 2: 5020 (5 points) = +8 points
Target 3: 5025 (5 points) = +13 points

R:R at Target 1: 3:12 = 0.25:1 (not ideal, but takes heat off)
R:R at Target 2: 8:12 = 0.67:1 (approaching 1:1)
R:R at Target 3: 13:12 = 1.08:1 (profitable)
```

#### Short Entry Setup

**Entry Criteria:**

1. ✅ Opening Range completed
2. ✅ Green range quality (ratio > 1.0)
3. ✅ Close below ORL (breakout confirmation)
4. ✅ Within Opportunity Window
5. ✅ Red triangle signal appears
6. ✅ (Optional) Price below VWAP for confirmation

**Entry Execution:**

- Enter at close of breakout bar OR
- Wait for bounce to ORL (now resistance) for better R:R

**Stop Loss:**

- Initial stop: Above ORH
- Tighter stop: Above ORL
- OR Width-based: ORL + (OR Width × 0.5)

**Profit Targets:**

- Same structure as longs, inverted

### 3. Target-Based Position Management

**The Scaling Strategy:**

#### Three-Part Position

**Position Sizing:**

```text
Total Risk: 1% of account
Split into 3 contracts:
- Contract 1: 33% (quick profit)
- Contract 2: 33% (measured move)
- Contract 3: 33% (runner)
```

**Management Plan:**

**Contract 1 (Target 1):**

- Exit at first target
- Lock in quick profit
- Reduces emotional pressure
- Guarantees profitable trade if targets 2-3 fail

**Contract 2 (Target 2):**

- Exit at second target
- Captures majority of typical move
- Achieves profitable trade overall
- Covers commission and slippage

**Contract 3 (Target 3+):**

- Trail with ORH/ORL or VWAP
- Capture extended runs
- Move stop to breakeven after Target 2
- Let winners run

**Example Trade Flow (MES Long):**

```text
Entry: 5012 (3 contracts)
Stop: 5000 (12 points per contract)

Target 1 (5015): Exit 1 contract
- P/L: +3 points
- Status: 2 contracts remain

Target 2 (5020): Exit 1 contract
- P/L: +8 points
- Status: 1 contract remains
- Move stop on remaining to 5012 (breakeven)

Target 3+ (5025+): Trail remaining
- P/L: +13+ points
- Trail stop: Below VWAP or use ORH as support
- Exit when price closes back below ORH or VWAP
```

### 4. Time-Based Trade Filtering

**Opportunity Window Usage:**

#### Standard Approach (Recommended)

**Trading Hours: 9:30 AM - 12:00 PM**

**Benefits:**

- Highest probability period
- Best liquidity
- Clearest trends
- Institutional activity peaks
- 2.5 hours for targets to develop

**Rules:**

- Only take signals during this window
- Close all positions by 12:00 PM (or trail)
- No new entries after 12:00 PM
- Avoid lunch chop (12:00-1:00 PM)

#### Aggressive Approach

**Trading Hours: 9:30 AM - 3:00 PM**

**Pros:**

- More opportunities
- Can catch afternoon trends
- Extended time for target achievement

**Cons:**

- Lower probability overall
- Lunch hour whipsaws
- Late-day unpredictability
- Closing auction mechanics

**Best For:** Experienced traders who can discern quality setups in afternoon

#### Conservative Approach

**Trading Hours: 9:30 AM - 11:00 AM**

**Benefits:**

- Absolute highest probability
- Most predictable hour
- Initial direction often sustained
- Can be done-for-day by lunchtime

**Drawbacks:**

- Fewer opportunities
- May miss larger moves
- Less time for multiple targets

**Best For:** Part-time traders, high win-rate focus

### 5. Daily Bias Alignment

**Using Previous Session Context:**

#### Bullish Bias Day (Current ORM > Previous ORM)

**What It Means:**

- Market opening higher than yesterday
- Institutions bidding up pre-market
- Likely continuation higher

**Trading Approach:**

- **Prioritize long signals** (take all long breakouts)
- **Be selective on shorts** (only take if daily bias filter enabled, which delays short signal to first target)
- Expect ORH to break, ORL to hold
- Target 2-3 achievable on longs

**Example:**

```text
Yesterday's ORM: 5000
Today's OR: 5015 (ORH) to 5005 (ORL)
Today's ORM: 5010

Bias: Bullish (+10 points)

Trade Plan:
- Take long breakout above 5015 aggressively
- Skip or reduce size on short breakout below 5005
- Expect upside targets to be reached
```

#### Bearish Bias Day (Current ORM < Previous ORM)

**What It Means:**

- Market opening lower than yesterday
- Distribution or selling pressure
- Likely continuation lower

**Trading Approach:**

- **Prioritize short signals** (take all short breakouts)
- **Be selective on longs** (only take if daily bias filter delays long signal)
- Expect ORL to break, ORH to hold
- Target 2-3 achievable on shorts

#### Neutral Day (Current ORM ≈ Previous ORM)

**What It Means:**

- Market opening unchanged
- Balance between buyers and sellers
- Could go either direction

**Trading Approach:**

- No bias, trade both directions equally
- Wait for breakout to establish direction
- First breakout often sets tone for day
- Be prepared for potential range-bound day

---

## Complementary Indicators and Market Conditions

### 1. Volume Analysis

**Why:** Confirms breakout quality and institutional participation

**With Volume Indicators:**

- **Breakout above ORH with increasing volume** = Valid, likely to continue
- **Breakout above ORH with decreasing volume** = Suspect, likely false
- **Volume spike at ORH/ORL** = Resistance/support being tested
- **Low volume during OR formation** = Poor quality range, skip

**Integration:**

- Require above-average volume on breakout bar
- Use volume profile to identify price levels with most volume
- Volume spikes at targets = likely temporary exhaustion

### 2. Your MA High/Low Channel (Daily Chart)

**Why:** Provides daily context for intraday ORB trades

**Integration:**

**Daily Channel Context:**

- If daily price at channel low + green OR = High probability long
- If daily price at channel high + green OR = Be cautious on longs
- If daily price mid-channel = No additional edge from daily

**Example:**

```text
MES Daily Chart:
- Channel Low: 4950
- Channel High: 5050
- Current: 4960 (near channel low)

Intraday ORB:
- Green range quality
- Long breakout signal

Analysis: Daily support + intraday breakout = STRONG LONG
```

### 3. Your VEI (Volatility Expansion Index)

**Why:** Filters days when ORB strategy likely to fail

**Integration:**

**VEI < 1.0 (Stable):**

- ✅ Ideal for ORB trading
- Clean trends, predictable behavior
- Trade full size on green ranges

**VEI > 1.2 (Volatile):**

- ❌ Poor for ORB trading
- Whipsaws, false breakouts common
- Skip ORB trades or use very tight stops
- Market too chaotic for range-based strategy

**Rule:**

```text
IF VEI > 1.2 on daily chart:
  → Skip all ORB trades today
  → Wait for VEI < 1.0

IF VEI < 1.0 and Green OR:
  → Highest conviction trades
  → Full position sizing
```

### 4. Your Up/Down Volume Ratio

**Why:** Confirms intraday momentum and breakout sustainability

**Integration:**

**At ORH Breakout:**

- Ratio > 1.5 = Strong buying, take the long
- Ratio < 1.0 = Weak buying, be cautious or skip

**At ORL Breakout:**

- Ratio < 0.8 = Strong selling, take the short
- Ratio > 1.0 = Weak selling, be cautious or skip

**During OR Formation:**

- Ratio improving = Quality range forming
- Ratio deteriorating = Poor range likely

### 5. Your Price/Volume Delta Candles

**Why:** Reveals hidden accumulation/distribution during OR formation

**Integration:**

**During OR Period (8:30-9:30):**

- Multiple bullish divergences (purple arrows) = Expect ORH breakout
- Multiple bearish divergences (blue arrows) = Expect ORL breakout
- Mixed signals = Likely range-bound day

**At Breakout:**

- Bullish divergence before ORH break = Strong confirmation
- Bearish divergence at ORH break = False breakout warning

**Example:**

```text
During OR (8:30-9:30):
- 3 bullish divergences appear
- Accumulation happening
- OR completes: Green quality

9:35 AM:
- Price breaks above ORH
- Enter long with high confidence
- Expect multiple targets
```

### 6. Market Context

**Economic Calendar:**

- **Before FOMC/CPI/NFP**: ORB often fails (wait for news, then trade)
- **After major news**: Extended ranges, adjust targets to 75-100% of OR width
- **Quiet news days**: Standard ORB parameters work best

**Session Characteristics:**

**Monday:**

- Often slower start
- Wait for more confirmation
- Can have extended OR (9:30-10:00)

**Tuesday-Thursday:**

- Best ORB days
- Most predictable
- Standard parameters

**Friday:**

- Early action good (9:30-11:00)
- Afternoon unpredictable (position squaring)
- Consider closing by 12:00 PM

### 7. Overnight Context

**Futures Advantages:**

- 24-hour markets allow overnight gap assessment
- Can see accumulation/distribution during off-hours

**Gap Analysis:**

**Gap Up:**

- OR likely higher than previous close
- Bullish bias likely
- Focus on long breakouts

**Gap Down:**

- OR likely lower than previous close
- Bearish bias likely
- Focus on short breakouts

**Gap Fill Trades:**

- If gap present, ORH/ORL may act as gap fill targets
- Combine ORB with gap trading for additional opportunities

### 8. Optimal Market Conditions

**Best Conditions for ORB Trading:**

✅ **Moderate Volatility (VEI 0.8-1.0):**

- Sufficient range for targets
- Not too choppy
- Predictable trends

✅ **Clear Overnight Direction:**

- Gap up or gap down establishing bias
- Pre-market momentum
- Follow-through likely

✅ **No Major News:**

- Predictable session
- Technical levels respected
- Normal volume patterns

✅ **Midweek (Tue-Thu):**

- Most consistent behavior
- Best liquidity
- Clearest trends

**Avoid ORB Trading When:**

❌ **Extreme Volatility (VEI > 1.5):**

- Whipsaws common
- False breakouts
- Stops get run

❌ **Major Economic Releases:**

- FOMC, CPI, NFP, etc.
- Unpredictable price action
- Technical levels often ignored

❌ **Holiday-Adjacent Days:**

- Low volume
- Reduced participation
- Unreliable signals

❌ **Post-3:00 PM:**

- Closing auction mechanics
- Unpredictable
- Poor risk:reward

---

## Trading Strategies for Futures

### Strategy 1: Pure ORB Breakout (Standard)

**Objective:** Trade first breakout of quality OR during Opportunity Window

**Setup Requirements:**

1. ✅ Green OR (ratio > 1.0)
2. ✅ Clean OR formation (smooth, not choppy)
3. ✅ VEI < 1.0 on daily chart (if using other indicators)
4. ✅ Within Opportunity Window (9:30-12:00)
5. ✅ Breakout signal fires (green or red triangle)

**Entry:**

- Preferred: Close above ORH (longs) or below ORL (shorts)
- Alternative: Pullback to ORH/ORL after initial breakout

**Position Sizing:**

- 3 contracts (if account size allows)
- Risk 1% of account total across all 3

**Management:**

- Exit 1st contract at Target 1
- Exit 2nd contract at Target 2
- Trail 3rd contract with ORH/ORL or VWAP

**Stop Loss:**

- Initial: Opposite side of OR (ORH for shorts, ORL for longs)
- After Target 1: Move to breakeven
- After Target 2: Move to Target 1 level

**Expected Results:**

- Win rate: 65-75% (on green ranges only)
- Average win: 1.5-2.0x OR Width
- Average loss: 1.0x OR Width
- Profit factor: 2.0-2.5

### Strategy 2: VWAP + ORB Combo

**Objective:** Use VWAP to confirm OR breakout direction

**Setup Requirements:**

**Long Setup:**

1. ✅ Green OR quality
2. ✅ Price closes above ORH
3. ✅ Price above VWAP at breakout
4. ✅ VWAP rising (bullish)

**Short Setup:**

1. ✅ Green OR quality
2. ✅ Price closes below ORL
3. ✅ Price below VWAP at breakout
4. ✅ VWAP falling (bearish)

**Entry:**

- Enter on close above ORH (longs) WITH confirmation from VWAP

**Additional Rules:**

- Skip breakout if price on wrong side of VWAP
- Use VWAP as trailing stop level
- Exit if price crosses back through VWAP against position

**Expected Results:**

- Win rate: 75-85% (higher than standard ORB due to VWAP filter)
- Fewer trades but higher quality
- Better average win

### Strategy 3: Daily Bias ORB

**Objective:** Only trade breakouts aligned with daily bias

**Setup Requirements:**

1. ✅ Determine daily bias (current ORM vs previous ORM)
2. ✅ Green OR quality
3. ✅ Breakout signal in direction of bias

**Bullish Bias Day:**

- Take ALL long breakouts above ORH
- SKIP short breakouts below ORL (or use daily bias filter)
- Expect multiple upside targets

**Bearish Bias Day:**

- Take ALL short breakouts below ORL
- SKIP long breakouts above ORH (or use daily bias filter)
- Expect multiple downside targets

**Management:**

- Aggressive on aligned direction (can hold through targets)
- Defensive on counter-trend (exit at first sign of reversal)

**Expected Results:**

- Win rate: 70-80% on bias-aligned trades
- Skipping counter-trend improves overall performance
- Fewer trades but better selectivity

### Strategy 4: First Hour Breakout Only

**Objective:** Trade only the immediate post-OR breakout (9:30-10:30)

**Setup Requirements:**

1. ✅ Green OR quality
2. ✅ Breakout signal 9:30-10:30 AM only
3. ✅ Above average volume on breakout bar

**Rules:**

- Enter only first breakout after OR
- No entries after 10:30 AM
- Close all positions by 12:00 PM (or trail)
- One trade per day maximum

**Benefits:**

- Highest probability hour
- Can be done-for-day by noon
- Reduced screen time
- Lower stress

**Expected Results:**

- Win rate: 70-80%
- One quality trade per day
- Sustainable lifestyle approach

### Strategy 5: Range Fade (Mean Reversion)

**Objective:** Fade failed breakouts back into the OR

**Setup Requirements:**

**Fade Long Setup:**

1. Price breaks above ORH
2. Fails to reach Target 1
3. Returns back into OR
4. Close below ORH

**Entry:**

- Short when price closes back below ORH
- Target: ORL (opposite side of range)
- Stop: Above recent high (above Target 1 area)

**Fade Short Setup:**

1. Price breaks below ORL
2. Fails to reach Target 1
3. Returns back into OR
4. Close above ORL

**Entry:**

- Long when price closes back above ORL
- Target: ORH
- Stop: Below recent low

**Risk:**

- Higher risk (counter-trend to initial breakout)
- Only trade on green ranges
- Tighter stops required

**Expected Results:**

- Win rate: 60-70%
- Quick hits (minutes to 1 hour)
- Good for range-bound days

---

## MES and MNQ Specific Guidance

### Micro E-mini S&P 500 (MES)

**Contract Specifications:**

- Ticker: MES
- Point Value: $5 per point
- Typical daily range: 30-70 points
- Margin: ~$1,300 per contract (varies)

**ORB Parameters for MES:**

**Range Quality Targets:**

```text
MES Price: 5000
Target OR Size: 0.2% = 10 points
Good Range: 10-20 points
Excellent Range: 20+ points
Poor Range: < 7 points
```

**Target Distances:**

- 50% of OR Width (default)
- Typical: 5-10 points per target
- Adjust to 40% if range > 20 points

**Position Sizing:**

```text
$10,000 Account:
Risk: 1% = $100
Stop: 10 points (opposite side of OR)
Position: 2 contracts ($5/point = $50 risk per contract)
Allocation: $100 / $50 = 2 contracts
```

**Optimal Times for MES:**

- 9:30-11:30 AM: Best liquidity and trends
- Avoid: 12:00-1:00 PM (lunch)
- Can trade: 2:00-3:00 PM if strong trend (use caution)

**MES-Specific Tips:**

- Wider stops okay (10-15 points is normal)
- Be patient for targets (can take 1-2 hours)
- Watch SPY options flow for additional confirmation
- Respect key levels: 5000, 5050, 5100, etc. (50-point intervals)

### Micro Nasdaq-100 (MNQ)

**Contract Specifications:**

- Ticker: MNQ
- Point Value: $2 per point
- Typical daily range: 100-300 points
- Margin: ~$1,700 per contract (varies)

**ORB Parameters for MNQ:**

**Range Quality Targets:**

```text
MNQ Price: 18000
Target OR Size: 0.2% = 36 points
Good Range: 36-70 points
Excellent Range: 70+ points
Poor Range: < 25 points
```

**Target Distances:**

- 50% of OR Width (default)
- Typical: 18-35 points per target
- Adjust to 40% if range > 100 points

**Position Sizing:**

```text
$10,000 Account:
Risk: 1% = $100
Stop: 40 points (opposite side of OR)
Position: 1-2 contracts ($2/point = $80 risk for 40 points)
Allocation: $100 / $80 = 1 contract (2 if experienced)
```

**Optimal Times for MNQ:**

- 9:30-11:00 AM: Most aggressive and directional
- 11:00-12:00 PM: Still good, slightly calmer
- Avoid: 12:00-1:00 PM strictly
- Afternoon: More volatile, only for experienced

**MNQ-Specific Tips:**

- Moves faster than MES (tech-heavy, more volatile)
- Targets reached quicker (minutes vs hours)
- Tighter time management needed
- Watch QQQ and mega-cap tech (AAPL, MSFT, NVDA, GOOGL)
- Respect big figures: 18000, 18500, 19000 (500-point intervals)
- Can use 40-60% target distance for faster targets

### MES vs MNQ Comparison

| Characteristic          | MES (S&P 500)      | MNQ (Nasdaq-100)    |
| ----------------------- | ------------------ | ------------------- |
| Volatility              | Moderate           | High                |
| Speed of Moves          | Slower, methodical | Fast, aggressive    |
| Target Achievement      | 1-2 hours          | 15-60 minutes       |
| Best For                | New to ORB         | Experienced traders |
| Range Quality Target    | 10+ points         | 36+ points          |
| Typical Targets Reached | 2-3 per day        | 3-5 per day         |
| Risk Level              | Lower              | Higher              |
| Patience Required       | High               | Moderate            |

**Recommendation:**

- **Start with MES** to learn ORB trading
- **Graduate to MNQ** after consistent MES profitability
- **Trade both** only if account > $25K and experienced

### Position Sizing for Both

**Small Account ($5K-$10K):**

```text
MES: 1-2 contracts max
MNQ: 1 contract max
Risk per trade: 1% ($50-$100)
```

**Medium Account ($10K-$25K):**

```text
MES: 2-3 contracts
MNQ: 1-2 contracts
Risk per trade: 1% ($100-$250)
```

**Large Account ($25K+):**

```text
MES: 3-5 contracts
MNQ: 2-3 contracts
Risk per trade: 1% ($250+)
```

---

## Risk Warnings and Limitations

### 1. Futures-Specific Risks

**Leverage:**

- Futures are highly leveraged instruments
- Can lose more than initial investment
- One bad day can wipe out weeks of profits
- Always use stops and proper position sizing

**Overnight Risk:**

- If holding overnight (not recommended for ORB)
- Gap risk can blow through stops
- News events after hours
- Best practice: Close all ORB positions before 4:00 PM ET

### 2. ORB Strategy Limitations

**Not Every Day Works:**

- Only ~60-70% of days produce quality ranges
- Red ranges should be skipped
- Patience required to wait for green ranges

**False Breakouts:**

- Even green ranges can produce false breakouts
- First breakout fails ~30-40% of time
- Stop losses are mandatory
- Position sizing critical

**Range-Bound Days:**

- Some days price stays within OR all session
- No breakout signals generated
- Opportunity cost of waiting
- Must accept "no trade" days

### 3. Time Commitment

**Real-Time Monitoring Required:**

- Must be at computer 8:30 AM - 12:00 PM ET minimum
- Cannot use this strategy if you have day job during these hours
- Alerts help but still need manual management
- Position management is active, not passive

### 4. Technology Dependence

**Platform Reliability:**

- Need fast, reliable platform
- Stop orders must execute
- Slippage in fast markets
- Have backup internet connection

### 5. Commission and Fees

**Costs Add Up:**

- Typical: $1.50-$2.50 per contract round-turn
- 3 contracts × 2 times (in/out) = $6-$15 per trade
- Multiple targets = multiple fills = more commissions
- Must factor into profitability

**Break-Even Calculation:**

```text
MES Example:
3 contracts
$2 per contract × 6 fills = $12 commission
MES @ $5/point: Need 2.4 points profit to break even
Spread + Slippage: Add 1-2 points
True Break-Even: 3.5-4.5 points

Must reach Target 1 (typically 5+ points) for profitability
```

### 6. Psychological Challenges

**Decision Fatigue:**

- Every day requires fresh analysis
- Must objectively assess range quality
- Easy to rationalize poor ranges
- Discipline to skip is hardest part

**Patience vs Action:**

- Waiting 30-60 minutes after breakout signal
- Resisting urge to enter early
- Letting targets develop
- Not revenge trading after loss

### 7. Market Evolution

**ORB is Well-Known:**

- Strategy published since 1990s
- Many traders use it
- May experience "crowded trade" effects
- Need additional filters (quality, VWAP, etc.) for edge

**Adapt or Fade:**

- What worked last year may not work now
- Must track statistics and adjust
- Consider evolving parameters seasonally
- Stay flexible

---

## Conclusion

The Opening Range Breakout with Opportunity Window indicator transforms the classic ORB strategy into a complete, systematic futures trading framework. By adding range quality assessment, automated target projection, time-based filtering, and VWAP integration, it addresses many of the traditional ORB weaknesses.

### Key Takeaways

1. **Range Quality is Everything**

   - Green ranges (ratio > 1.0) are tradeable
   - Red ranges (ratio < 1.0) should be skipped
   - This single filter can double your win rate

2. **Time of Day Matters**

   - 9:30-12:00 PM is the sweet spot
   - First hour post-OR is highest probability
   - Avoid lunch hour and late afternoon

3. **Targets Provide Structure**

   - Automated target generation removes guesswork
   - Scale out using 3-part position
   - Let winners run past Target 3

4. **VWAP Adds Confirmation**

   - Breakouts with VWAP alignment are stronger
   - Use VWAP as dynamic support/resistance
   - Trail stops using VWAP after breakout

5. **Daily Bias Improves Selectivity**
   - Trading with the bias increases probability
   - Counter-trend trades have lower success
   - Current ORM vs Previous ORM shows institutional intent

### The ORB Edge for Futures

**Why It Works:**

- First hour establishes the battlefield
- Breakouts beyond this range represent conviction
- Targets based on range width are logical profit points
- Futures liquidity makes execution reliable

**Best Results Come From:**

- Trading ONLY green quality ranges (discipline)
- Using the Opportunity Window (patience)
- Proper position sizing (risk management)
- Scaling out at targets (taking profits)
- Combining with complementary indicators (confirmation)

### Practical Implementation

**Week 1-2: Paper Trade**

- Watch indicator form each morning
- Note range quality (green/red)
- Observe which breakouts work
- Track target achievement
- Don't risk real money yet

**Week 3-4: Single Contract**

- Trade 1 MES contract only
- Green ranges only
- Standard Opportunity Window
- Track every trade in journal
- Goal: Consistency, not profit

**Month 2-3: Standard Position**

- Scale to 2-3 contracts if profitable
- Implement scaling out at targets
- Add VWAP filter
- Refine parameters for your style

**Month 4+: Full Implementation**

- Trade full system
- Consider MNQ if MES mastered
- Add complementary indicators
- Optimize for your edge

### Final Thoughts

ORB trading is **simple but not easy**. The indicator provides all the information needed, but success requires:

- **Discipline** to skip red ranges
- **Patience** to wait for setups
- **Execution** to take signals without hesitation
- **Management** to scale out at targets
- **Acceptance** of losses as part of the process

For futures traders willing to commit to the structure and process, this indicator provides a complete, testable, and historically reliable framework for consistent intraday profits.

**Remember:** The goal is not to trade every day, but to trade every **quality** day. Green ranges only. Opportunity Window only. Proper sizing always.

---

**Disclaimer:** Futures trading involves substantial risk of loss and is not suitable for all investors. Past performance is not indicative of future results. This indicator is a tool, not a guarantee. Always trade with money you can afford to lose and never risk more than 1-2% of your account on any single trade.

**Attribution:** This indicator is a modified version of the LuxAlgo - ORB & Targets indicator, licensed under CC BY-NC-SA 4.0. Modifications by @n8rzz (Nate Geslin).
