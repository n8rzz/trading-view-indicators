---
title: Short Put
description: Options strategy documentation.
category: strategy
---

# Cash-Secured Put Strategy Guide

## Overview

This document outlines a systematic approach to selling cash-secured puts using a multi-indicator framework that combines trend structure, volume analysis, market stability, and institutional flow detection. The strategy leverages technical analysis to identify high-probability support zones where selling puts offers favorable risk:reward characteristics.

**Strategy Type:** Income generation with defined risk

**Capital Requirement:** Cash secured (100% collateral required)

**Ideal Outcome:** Collect premium while avoiding assignment, or accept assignment at favorable prices with accumulation signals

**Time Horizon:** 30-45 days to expiration (DTE) for optimal theta decay

## Table of Contents

- [The Multi-Timeframe Setup](#the-multi-timeframe-setup)
- [Indicator Integration Framework](#indicator-integration-framework)
- [Entry Criteria](#entry-criteria)
- [Position Sizing Rules](#position-sizing-rules)
- [Strike Selection](#strike-selection)
- [Risk Management](#risk-management)
- [Exit and Adjustment Strategies](#exit-and-adjustment-strategies)
- [Trade Evaluation Checklist](#trade-evaluation-checklist)
- [Example Trade Scenarios](#example-trade-scenarios)
- [Advanced Techniques](#advanced-techniques)
- [Common Mistakes to Avoid](#common-mistakes-to-avoid)

---

## The Multi-Timeframe Setup

### Chart Configuration

**Daily Chart (Primary - Strategic View):**

- **Purpose:** Identify weekly/monthly support zones and trend context
- **Indicators:**
  - MA High/Low Channel
  - Price/Volume Delta Candles (divergence arrows)
  - Up/Down Volume Ratio
  - Volume Profile (right side)
- **Usage:** Determines WHERE to sell puts (support levels)

**15-Minute Chart (Secondary - Tactical View):**

- **Purpose:** Time intraday entries and confirm stabilization
- **Indicators:**
  - MA High/Low Channel (intraday structure)
  - VEI (Volatility Expansion Index)
  - Up/Down Volume Delta
- **Usage:** Determines WHEN to sell puts (optimal timing)

### Why This Combination Works

1. **Daily chart** shows institutional accumulation zones (where smart money is buying)
2. **15-minute chart** confirms short-term stability (VEI) and momentum shifts
3. **Volume analysis** reveals conviction behind support levels
4. **Multi-timeframe confluence** dramatically increases probability of success

---

## Indicator Integration Framework

### 1. MA High/Low Channel (Trend Structure)

**Daily Chart Usage:**

**At Channel Low (Bullish Signal):**

- Price touching or near the lower channel boundary = structural support
- Historical price has bounced here repeatedly
- Best zone to sell puts (support likely to hold)

**At Channel Mid-Point (Neutral):**

- Price in middle of channel = less defined support
- Can sell puts but require stronger volume confirmation
- Use wider strike margins

**Below Channel Low (Bearish Warning):**

- Price broken below channel = structural breakdown
- AVOID selling puts until reclaim of channel
- High risk of continued decline

**Strike Selection Guide:**

- Sell puts at or just below channel low for maximum safety
- If price is mid-channel, sell puts at previous channel low test

### 2. VEI - Volatility Expansion Index (Market Stability Filter)

#### The Master Gate - Check This FIRST

**VEI < 0.8 (Ideal - Very Stable):**

- ✅ Extremely favorable conditions
- Market structure clean and predictable
- Sell full position sizes
- Tighten strike selections (can be more aggressive)

**VEI 0.8 - 1.0 (Good - Stable):**

- ✅ Favorable conditions
- Normal trading environment
- Sell standard position sizes
- Use normal strike selection criteria

**VEI 1.0 - 1.2 (Caution - Transitional):**

- ⚠️ Proceed with caution
- Market becoming less predictable
- Reduce position size by 50%
- Widen strike selections (more conservative)
- Only take highest-conviction setups

**VEI > 1.2 (AVOID - Volatile):**

- ❌ Unfavorable conditions
- High risk of blowing through strikes
- Sell 0-25% position size OR skip entirely
- Premiums attractive but extremely dangerous
- Wait for VEI to drop below 1.2

**Your Screenshot Shows VEI = 0.9391 = EXCELLENT CONDITIONS** ✅

### 3. Price/Volume Delta Candles (Institutional Flow)

#### Bullish Divergence Signals (Purple Arrows)

**What It Means:**

- Price closing down BUT volume delta positive
- Institutions buying while price appears weak
- Hidden accumulation happening
- Support likely to form/hold

**How to Use for Put Selling:**

**Single Purple Arrow:**

- Mild accumulation signal
- Confirms support level
- Good for conservative put sales

**2-3 Consecutive Purple Arrows:**

- Strong accumulation signal
- Institutions aggressively buying dips
- IDEAL setup for put selling
- Support very likely to hold

**Purple Arrows at Support Level:**

- Highest probability setup
- Support + accumulation = maximum safety
- Can sell puts at or near current price
- Low assignment risk

#### Bearish Divergence Signals (Blue Arrows)

**What It Means:**

- Price closing up BUT volume delta negative
- Institutions selling while price appears strong
- Hidden distribution happening
- Resistance likely to form/reject

**How to Use for Put Selling:**

**Blue Arrows Below Your Strike:**

- WARNING: Distribution happening at lower prices
- Support may not hold
- Skip the trade or select much lower strike
- High assignment risk

**Blue Arrows at Resistance Above:**

- Normal distribution at resistance
- Doesn't affect put selling below
- Can be ignored if far above your strike

### 4. Up/Down Volume Ratio (Momentum and Sentiment)

#### The Regime Filter

**Ratio > 1.5 (Very Bullish):**

- ✅ Strong buying pressure
- Uptrend firmly established
- Can sell puts at current prices
- Low assignment risk
- High win rate expected

**Ratio 1.0 - 1.5 (Mildly Bullish):**

- ✅ Moderate buying pressure
- Healthy environment
- Sell puts at normal strikes
- Standard risk/reward

**Ratio 0.8 - 1.0 (Neutral to Slightly Bearish):**

- ⚠️ Balanced to slightly negative
- Be more selective
- Sell puts further out of the money
- Require additional confirmation

**Ratio < 0.8 (Bearish):**

- ❌ Selling pressure dominant
- High risk environment
- Only sell puts well below current price
- Consider skipping altogether

**Ratio < 0.5 (Very Bearish):**

- ❌ Strong selling pressure
- DO NOT sell puts
- Wait for ratio to improve above 0.8

**Your Screenshot Shows Ratio Rising Toward 1.0+ = IMPROVING CONDITIONS** ✅

### 5. Volume Profile (Support/Resistance Zones)

#### High-Volume Nodes

- Areas with significant historical volume
- Act as strong support/resistance
- Institutions have positions at these levels

**How to Use for Put Selling:**

**High-Volume Node Nearby (Within 3-5%):**

- ✅ Strong support likely
- Institutions will defend these levels
- Ideal strike selection zone
- Very low assignment risk

**Low-Volume Area (Gap in profile):**

- ⚠️ Weak support
- Price can fall quickly through these zones
- Avoid setting strikes in low-volume areas
- Price will seek next high-volume node below

**Strike Selection Using Volume Profile:**

- Identify nearest high-volume node below current price
- Sell puts at or just above this node
- This is where institutions will provide support

---

## Entry Criteria

### The Perfect Setup (All Criteria Met)

#### Score: 7/7 Points = Excellent Trade

1. ✅ **Daily MA Channel:** Price at or near channel LOW (structural support)
2. ✅ **VEI < 1.0:** Market stability confirmed (15-min chart)
3. ✅ **Bullish Divergence:** 2-3 purple arrows on daily chart (accumulation)
4. ✅ **Up/Dn Ratio > 0.8:** Buying pressure present or improving
5. ✅ **Volume Profile:** High-volume node within 3-5% below current price
6. ✅ **15-Min Stabilization:** Selling pressure stopped, no further downside momentum
7. ✅ **Stock Quality:** Company you'd be happy owning at strike price

**Action:** Sell puts aggressively with full position size

### Good Setup (5-6 Points)

#### Score: 5-6/7 Points = Good Trade

- Most criteria met, minor weaknesses present
- Acceptable for standard put selling
- Use normal position sizing
- May need to widen strikes for extra safety

**Action:** Sell puts with standard position size

### Marginal Setup (3-4 Points)

#### Score: 3-4/7 Points = Marginal Trade

- Several criteria missing or weak
- Only for experienced traders
- Reduce position size significantly
- Require very wide strike margins

**Action:** Consider skipping OR sell with 25-50% position size

### Poor Setup (< 3 Points)

#### Score: < 3/7 Points = Skip Trade

- Too many criteria missing
- High risk of assignment
- Low probability of success

**Action:** SKIP - Wait for better setup

---

## Position Sizing Rules

### Base Position Size Formula

```text
Standard Position = (Account Size × Risk %) / (Stock Price × 100)

Example:
- Account: $100,000
- Risk per trade: 5%
- Stock price: $50
- Standard size: ($100,000 × 5%) / ($50 × 100) = 1 contract
```

### VEI-Based Position Sizing Adjustments

**VEI < 0.8 (Very Stable):**

```text
Position Size: 100-125% of standard

Example: If standard = 2 contracts, can sell 2-3 contracts
Reasoning: Market very stable, low risk of volatility expansion
```

**VEI 0.8 - 1.0 (Stable):**

```text
Position Size: 100% of standard

Example: If standard = 2 contracts, sell 2 contracts
Reasoning: Normal conditions, standard risk
```

**VEI 1.0 - 1.2 (Transitional):**

```text
Position Size: 50-75% of standard

Example: If standard = 2 contracts, sell 1 contract
Reasoning: Market less stable, higher risk
```

**VEI > 1.2 (Volatile):**

```text
Position Size: 0-25% of standard or skip

Example: If standard = 2 contracts, sell 0-1 contract or skip
Reasoning: Dangerous conditions, high assignment risk
```

### Setup Quality-Based Adjustments

**7/7 Point Setup (Perfect):**

- Multiply position size by 1.0-1.25x
- High confidence warranted

**5-6 Point Setup (Good):**

- Use standard 1.0x position size
- Normal confidence

**3-4 Point Setup (Marginal):**

- Multiply position size by 0.25-0.5x
- Low confidence, high caution

### Diversification Rules

**Maximum Allocation:**

- No more than 10-15% of account in any single underlying
- Maximum 3-5 positions at once (depending on account size)
- Limit sector concentration (no more than 30% in single sector)

**Example Portfolio (100K Account):**

```text
Position 1: AAPL - 2 contracts ($10K exposure) = 10%
Position 2: MSFT - 2 contracts ($10K exposure) = 10%
Position 3: SPY  - 2 contracts ($10K exposure) = 10%
Position 4: XLF  - 1 contract ($5K exposure) = 5%
Total: 7 contracts, ~$35K exposure, 35% deployed

Remaining: $65K cash for:
- New opportunities
- Potential assignments
- Rolling/adjustments
```

---

## Strike Selection

### Conservative Approach (Recommended for Most Traders)

**Target:** 2-5% out of the money (OTM)

**Benefits:**

- Higher win rate (80-90%+)
- Lower stress
- Assignment less likely
- Still decent premium

**Strike Selection Process:**

1. Identify daily MA channel LOW on chart
2. Find nearest volume profile high-volume node
3. Select strike 2-3 points below these levels
4. Confirm strike is 30-45 DTE

**Example:**

```text
Stock: XYZ trading at $50
Daily Channel Low: $48
Volume Profile Node: $47.50
Conservative Strike: $45 or $46 put
Distance: 8-10% OTM
Premium: $0.50 - 0.75 per share
```

### Moderate Approach (Experienced Traders)

**Target:** At the money (ATM) to 2% OTM

**Benefits:**

- Higher premium collection
- Still reasonable win rate (70-80%)
- Good if willing to own stock

**Strike Selection Process:**

1. Use current price or daily channel low as reference
2. Sell puts at or slightly below
3. Ensure bullish divergences present
4. Confirm VEI < 1.0

**Example:**

```text
Stock: XYZ trading at $50
Daily Channel Low: $48
Volume Profile Node: $47.50
Moderate Strike: $48 or $49 put
Distance: ATM to 4% OTM
Premium: $1.00 - 1.50 per share
```

### Aggressive Approach (High Risk)

**Target:** In the money (ITM) or current price

**Benefits:**

- Maximum premium
- Likely assignment
- Using put sale as stock accumulation strategy

**Strike Selection Process:**

1. Only use if wanting to own stock at current price
2. Require perfect 7/7 setup
3. Multiple bullish divergences essential
4. VEI must be < 1.0

**Example:**

```text
Stock: XYZ trading at $50
Daily Channel Low: $48
Volume Profile Node: $47.50
Aggressive Strike: $50 or $51 put
Distance: ATM to ITM
Premium: $2.00 - 3.00 per share

Outcome: Likely assignment, but at favorable level with accumulation
```

### Strike Selection by Setup Quality

**7/7 Point Setup:**

- Can use moderate to aggressive strikes
- ATM to 2% OTM acceptable
- High confidence in support

**5-6 Point Setup:**

- Use conservative to moderate strikes
- 2-5% OTM recommended
- Standard safety margins

**3-4 Point Setup:**

- Use very conservative strikes
- 5-10% OTM required
- Only if taking trade at all

---

## Risk Management

### Pre-Trade Risk Assessment

**Before Selling ANY Put:**

1. **Would you be happy owning 100 shares at this strike?**
   - If NO → Don't sell the put
   - If YES → Proceed with analysis

2. **Do you have the full cash available?**
   - Must have 100% of strike price × 100 shares
   - Cannot use margin for cash-secured puts (defeats purpose)

3. **Is this a good stock/ETF fundamentally?**
   - Don't sell puts on junk just for premium
   - Quality companies only
   - Know the business and sector

4. **Can you handle assignment?**
   - Assignment means tying up capital
   - Emotional ability to hold underwater position
   - Plan for what to do if assigned

### Position-Level Stop Loss Rules

**Hard Rules:**

**VEI Spike Rule:**

```text
IF VEI crosses above 1.5:
  → Close or roll ALL positions immediately
  → Market regime has changed to dangerous
  → Don't wait for further deterioration
```

**Bearish Divergence Rule:**

```text
IF 2+ bearish divergences (blue arrows) appear BELOW your strike:
  → Distribution happening at lower prices
  → Support likely to fail
  → Close or roll down/out for credit
```

**Channel Break Rule:**

```text
IF price closes below daily channel low:
  → Structural support broken
  → Roll down/out OR close position
  → Don't hold and hope
```

**Up/Dn Ratio Rule:**

```text
IF ratio drops below 0.5:
  → Extreme selling pressure
  → Roll or close position
  → Wait for ratio to improve above 0.8
```

### Profit-Taking Rules

**The 50-70% Rule (Recommended):**

```text
When position shows 50-70% of max profit:
  → Close the position
  → Don't wait for expiration
  → Free up capital for new trades
  → Reduces tail risk

Example:
- Sold put for $1.00 credit
- Position now worth $0.30
- Profit: $0.70 = 70% of max
- BUY TO CLOSE at $0.30
```

**Time-Based Rule:**

```text
At 7-10 days to expiration (DTE):
  → If profit > 50%, close position
  → If profit < 50% but stock above strike, hold
  → If profit < 50% and stock near/below strike, roll out
```

### Maximum Loss Tolerance

**Per Position:**

- Never risk more than 5-10% of account on single position
- If loss exceeds 2x the premium received, evaluate closing
- Don't let single loss spiral out of control

**Portfolio Level:**

- If multiple positions showing losses simultaneously
- Reassess overall market conditions
- Likely VEI spike or regime change
- Close or adjust entire portfolio if needed

---

## Exit and Adjustment Strategies

### Profit-Taking Exits (The Good Scenario)

**50% Rule (Conservative):**

- Close when profit reaches 50% of maximum
- Typically 15-20 days after entry
- High win rate, rapid capital turnover

**70% Rule (Balanced):**

- Close when profit reaches 70% of maximum
- Typically 7-10 days after entry
- Balance of win rate and capital efficiency

**Let It Expire (Aggressive):**

- Hold until expiration for maximum profit
- Only if VEI stable and no warning signs
- Highest profit per trade but ties up capital

### Rolling Strategies (Defensive Adjustments)

**Roll Down and Out (Stock Moving Against You):**

**Trigger:**

- Price approaching your strike
- Bearish signals appearing
- Want to collect more premium and avoid assignment

**Process:**

```text
Original Position:
- Short $50 put, 15 DTE, currently $0.80 debit to close
- Stock at $51 (getting close)

Roll:
- BUY TO CLOSE $50 put at $0.80 (loss)
- SELL TO OPEN $48 put, 30-45 DTE at $1.20 (credit)
- Net credit: $0.40
- New strike 4% lower, new time 30 days out
```

**Benefits:**

- Collect additional premium
- Lower strike = more safety margin
- More time for recovery

**Drawbacks:**

- Lock in unrealized loss
- Lower strike = less income if repeated

**Roll Out (Time Extension):**

**Trigger:**

- Price near strike but bullish signals improving
- Don't want assignment yet
- Believe support will hold with more time

**Process:**

```text
Original Position:
- Short $50 put, 5 DTE, currently $1.50 debit to close
- Stock at $49.75 (right at strike)

Roll:
- BUY TO CLOSE $50 put at $1.50 (loss)
- SELL TO OPEN $50 put, 30 DTE at $2.00 (credit)
- Net credit: $0.50
- Same strike, more time
```

**Benefits:**

- Collect additional premium
- Give thesis more time to work
- Avoid assignment this cycle

**Drawbacks:**

- Still exposed at same strike
- Kicking the can down the road

**Roll Up (Stock Moving in Your Favor):**

**Trigger:**

- Stock rallied significantly above your strike
- Want to capture more upside potential
- Can collect more premium at higher strike

**Process:**

```text
Original Position:
- Short $50 put, 20 DTE, currently $0.10 to close
- Stock at $55 (well above strike)

Roll:
- BUY TO CLOSE $50 put at $0.10
- SELL TO OPEN $53 put, 30-45 DTE at $1.00
- Net credit: $0.90
- Higher strike, more premium
```

**Benefits:**

- Capture additional premium
- Higher strike = better if assigned
- Participate in upside move

**Drawbacks:**

- Higher assignment risk (but that's okay here)
- May miss opportunity to deploy capital elsewhere

### Assignment Management

**If You Get Assigned (You Now Own 100 Shares):**

**Scenario 1: Assignment at Good Level (With Bullish Signals):**

```text
- You sold $48 put on XYZ
- Assigned 100 shares at $48
- Stock currently at $47
- Bullish divergences appearing
- VEI stable
- Up/Dn Ratio improving

Action:
→ HOLD the shares
→ Begin selling covered calls at $50-52 strike
→ Collect premium while waiting for recovery
→ "Wheel strategy" in action
```

**Scenario 2: Assignment at Bad Level (Bearish Breakdown):**

```text
- You sold $48 put on XYZ
- Assigned 100 shares at $48
- Stock currently at $44
- Bearish divergences continuing
- VEI > 1.2 (volatile)
- Up/Dn Ratio < 0.5 (bearish)

Action:
→ SELL the shares immediately (take the loss)
→ Don't hold and hope in broken structure
→ Preserve capital for better opportunities
→ This is why we only sell puts on quality stocks
```

**Scenario 3: Assignment in Neutral Market:**

```text
- You sold $48 put on XYZ
- Assigned 100 shares at $48
- Stock currently at $47.50
- No clear signals either direction
- VEI stable

Action:
→ HOLD the shares
→ Sell covered calls 2-5% OTM
→ Collect premium to reduce cost basis
→ Wait for next clear signal (bullish divergence or bearish break)
```

---

## Trade Evaluation Checklist

### Pre-Trade Checklist

Print this and use for EVERY trade:

```text
TICKER: ___________  DATE: ___________

Daily Chart Analysis:
[ ] Price at/near daily MA channel low
[ ] Volume profile support within 5% below
[ ] 2-3 bullish divergences (purple arrows) present
[ ] No bearish divergences below potential strike

15-Minute Chart Analysis:
[ ] VEI < 1.2 (preferably < 1.0)
[ ] Price stabilizing or reversing
[ ] No major downside momentum continuing

Volume Analysis:
[ ] Up/Dn Ratio > 0.8 (preferably > 1.0)
[ ] Ratio improving or stable
[ ] Volume supporting current price level

Fundamental Check:
[ ] Stock/ETF I'd be happy to own
[ ] Company fundamentals solid
[ ] No major negative catalysts upcoming (earnings, etc.)

Risk Management:
[ ] Full cash available for assignment
[ ] Position size within limits (max 10-15% of account)
[ ] Strike selected based on support levels
[ ] Total portfolio exposure under 50%

TOTAL SCORE: _____ / 12

Scoring:
10-12: Excellent trade - full size
7-9:   Good trade - standard size
5-6:   Marginal trade - reduced size or skip
< 5:   Poor trade - SKIP

TRADE DECISION: [ ] Sell Puts  [ ] Skip

If Selling:
Strike: _______  DTE: _______  Premium: _______  Qty: _______
```

---

## Example Trade Scenarios

### Example 1: Perfect 7/7 Setup

**Ticker:** AAPL
**Date:** January 25, 2026
**Current Price:** $185

**Daily Chart:**

- Price: $185 (at channel low of $184-186)
- MA Channel: Low at $184, High at $195
- Bullish Divergences: 3 purple arrows in last 5 days
- Volume Profile: Massive node at $180-182
- Up/Dn Ratio: 1.15 (buyers in control)

**15-Minute Chart:**

- VEI: 0.88 (very stable)
- Price: Stabilized after pullback
- Volume Delta: Positive intraday

**Fundamental:**

- AAPL = quality company
- No earnings for 3 weeks
- Happy to own at $180

**Setup Score: 7/7** ✅

**Trade Execution:**

```text
Action: SELL TO OPEN
Contract: AAPL Feb 28, 2026 $180 Put
Premium: $2.10 per share = $210 per contract
Quantity: 2 contracts (within 10% allocation limit)
Capital Required: $36,000
Potential Profit: $420 (2.3% return in 34 days)

Strike Rationale:
- $180 is 2.7% below current price
- Sits at major volume profile support
- Well below channel low ($184)
- Conservative given perfect setup

Position Sizing:
- VEI < 1.0 = can use full size
- 7/7 setup = high confidence
- 2 contracts = reasonable for account size
```

**Management Plan:**

```text
Profit Target: Close at 50-70% profit ($0.60-0.90 buyback)
Stop Loss: If VEI > 1.2 OR price breaks below $180
Roll Decision: If price at $182 with 10 days left, consider roll
Assignment Plan: Happy to own at $180, will sell covered calls
```

**Outcome Scenarios:**

**Scenario A (Most Likely - 85% probability):**

- AAPL stays above $180
- Close at 50% profit in 2 weeks
- Profit: $210 in 14 days

**Scenario B (Possible - 10% probability):**

- AAPL drops to $182 near expiration
- Roll down to $178 for next month, collect $0.80 credit
- Net credit: $2.90 total, continue trade

**Scenario C (Unlikely - 5% probability):**

- AAPL breaks down below $180
- Assigned 200 shares at $180 ($36,000)
- Sell $185 covered calls next cycle
- Begin "wheel strategy"

### Example 2: Marginal 4/7 Setup (Should Skip)

**Ticker:** TSLA
**Date:** January 25, 2026
**Current Price:** $210

**Daily Chart:**

- Price: $210 (mid-channel, not at low) ❌
- MA Channel: Low at $200, High at $230
- Bullish Divergences: Only 1 purple arrow ❌
- Volume Profile: Node at $195, but that's 7% away ⚠️
- Up/Dn Ratio: 0.75 (slightly bearish) ❌

**15-Minute Chart:**

- VEI: 1.15 (transitional, approaching caution zone) ⚠️
- Price: Still showing downside momentum ❌
- Volume Delta: Mixed signals

**Fundamental:**

- TSLA = volatile, okay to own but risky
- Earnings in 2 weeks ❌

**Setup Score: 4/7** ❌

#### Decision: SKIP THIS TRADE

**Why Skip:**

1. Price not at support (mid-channel)
2. Only one weak divergence signal
3. Up/Dn Ratio bearish
4. VEI approaching danger zone
5. Earnings catalyst upcoming
6. Still showing downside momentum

**Better Plan:**

- Wait for price to reach $200 (channel low)
- Wait for VEI to drop below 1.0
- Wait for 2-3 bullish divergences to appear
- Wait for Up/Dn Ratio to improve above 0.8
- Wait until after earnings
- THEN re-evaluate

**Lesson:** Sometimes the best trade is no trade. Be patient.

### Example 3: Good 6/7 Setup (Tradeable)

**Ticker:** SPY
**Date:** January 25, 2026
**Current Price:** $580

**Daily Chart:**

- Price: $580 (near channel low of $578) ✅
- MA Channel: Low at $578, High at $595
- Bullish Divergences: 2 purple arrows ✅
- Volume Profile: Node at $575 ✅
- Up/Dn Ratio: 0.95 (neutral, improving) ⚠️

**15-Minute Chart:**

- VEI: 0.92 (stable) ✅
- Price: Stabilized ✅
- Volume Delta: Positive

**Fundamental:**

- SPY = highest quality, diversified
- Happy to own ✅

**Setup Score: 6/7** ✅ (Good Trade)

**Trade Execution:**

```text
Action: SELL TO OPEN
Contract: SPY Feb 21, 2026 $575 Put
Premium: $4.50 per share = $450 per contract
Quantity: 1 contract (SPY high price = limit qty)
Capital Required: $57,500
Potential Profit: $450 (0.78% return in 27 days)

Strike Rationale:
- $575 is 0.86% below current price
- Sits at volume profile support
- Just below channel low ($578)
- Conservative given SPY less volatile than stocks

Position Sizing:
- 6/7 setup = standard size
- Only 1 contract due to high capital requirement
- Leaves room for other positions
```

**Management Plan:**

```text
Profit Target: Close at 50% profit ($2.25 buyback)
Stop Loss: If VEI > 1.2 OR breaks below $575
Expected Hold Time: 10-15 days
```

---

## Advanced Techniques

### The Stacking Strategy

**Concept:** Sell multiple contracts at different strikes to diversify assignment risk

**Example:**

```text
Stock: XYZ at $50
Channel Low: $48
Volume Nodes: $47, $45

Instead of selling 3 contracts at $47:
- Sell 1 contract at $49 (close to current, higher premium)
- Sell 1 contract at $47 (at channel low, medium premium)
- Sell 1 contract at $45 (at volume node, lower premium)

Benefits:
- Diversified risk
- Average down if assigned
- Different profit targets
- More flexible management
```

### The Earnings Play (Advanced)

**Setup:** Sell puts AFTER earnings announcement on quality stocks

**Why:**

- IV crush after earnings = cheaper put prices
- Uncertainty removed
- If earnings good + your signals align = very high probability

**Example:**

```text
Day Before Earnings:
- MSFT trading at $420
- $410 put (30 DTE) trading at $8.00
- Don't sell yet (IV too high)

Day After Earnings:
- MSFT reports good earnings, stock at $425
- $410 put (29 DTE) now trading at $3.50
- Your signals all bullish (7/7 setup)

Action:
- SELL $410 put at $3.50
- Lower premium but much lower risk
- Probability very high
```

### The Pair Trade

**Concept:** Sell puts on two correlated instruments for diversification

**Example:**

```text
Both setups are 6/7 quality:

Position 1:
- Sell QQQ $450 put

Position 2:
- Sell TQQQ $80 put (leveraged QQQ)

Rationale:
- Both track Nasdaq
- But price differently
- If QQQ holds, TQQQ likely holds
- Diversified strikes and names
```

### The Ladder Approach (Time Diversification)

**Concept:** Sell puts at different expiration cycles

**Example:**

```text
Stock: XYZ at $50

Week 1:
- Sell 1 contract, 30 DTE

Week 2:
- Sell 1 contract, 30 DTE (if setup still good)

Week 3:
- Sell 1 contract, 30 DTE (if setup still good)

Result:
- 3 positions at different DTE
- Weekly profits as positions expire
- Continuous income stream
- Diversified timing risk
```

---

## Common Mistakes to Avoid

### 1. Selling Puts When VEI > 1.2

**Mistake:** "The premium is so high, I have to take it!"

**Reality:**

- Premium high BECAUSE risk is high
- Volatile markets blow through strikes
- Assignment risk skyrockets
- One bad trade can wipe out months of profits

**Fix:** Be patient. Wait for VEI < 1.0. Boring markets make money.

### 2. Ignoring Bearish Divergences

**Mistake:** Seeing blue arrows but selling puts anyway

**Reality:**

- Blue arrows = distribution
- Smart money selling
- Support likely to fail
- You're fighting institutions

**Fix:** When you see bearish divergences, SKIP THE TRADE. Wait for bullish divergences.

### 3. Selling Puts on Junk for High Premium

**Mistake:** "This penny stock has $2 premium on a $10 strike!"

**Reality:**

- High premium = high risk
- Junk stocks can go to zero
- Assignment = stuck with garbage
- Illiquid options = can't exit

**Fix:** Only sell puts on stocks you'd be HAPPY to own. Quality over premium.

### 4. Holding to Expiration for Last 10%

**Mistake:** "I want every penny of profit"

**Reality:**

- Tying up capital for minimal gain
- Tail risk of late market move
- Opportunity cost of new trades
- Stress not worth it

**Fix:** Close at 50-70% profit. Redeploy capital to new trades. Compound faster.

### 5. Not Having Cash Secured

**Mistake:** Using margin or "I'll find the money if assigned"

**Reality:**

- Assignment can happen anytime
- Forced liquidation if no cash
- Defeats "cash-secured" purpose
- Margin call risk

**Fix:** Have 100% of the strike value in cash BEFORE selling the put. No exceptions.

### 6. Over-Concentration

**Mistake:** Selling 10 contracts on single stock

**Reality:**

- One bad setup = huge loss
- All eggs in one basket
- Sector risk extreme
- Recovery difficult

**Fix:** Max 10-15% per position. Diversify across 3-5 names. Different sectors.

### 7. Ignoring the Daily Chart

**Mistake:** Only looking at 15-minute chart for entries

**Reality:**

- Missing big picture
- Don't see major support/resistance
- Higher timeframe structure matters more
- Intraday noise misleads

**Fix:** ALWAYS check daily chart first. It's your strategic view. 15-min is just for timing.

### 8. Falling in Love with a Position

**Mistake:** "I sold the put, so the stock MUST go up"

**Reality:**

- Market doesn't care about your position
- Confirmation bias blinds you
- Ignore warning signals
- Turn small loss into big loss

**Fix:** Be objective. If VEI spikes, bearish divergences appear, or structure breaks = EXIT.

### 9. Revenge Trading After Assignment

**Mistake:** "I got assigned, now I'll sell closer puts to make it back faster"

**Reality:**

- Emotional decision making
- Increased risk when already down
- Compound losses
- Death spiral

**Fix:** After assignment, take a break. Reassess with clear head. Quality setups only.

### 10. Not Using a Checklist

**Mistake:** Trading on "feel" or "looks good"

**Reality:**

- Inconsistent results
- Forget to check key indicators
- Emotional decisions
- Can't improve without data

**Fix:** Use the checklist EVERY TIME. Track your results. Learn from data, not feelings.

---

## Final Thoughts

### The Three Pillars of Success

**1. Discipline:**

- Only trade 5-7/7 setups
- Use the checklist religiously
- Take profits at 50-70%
- Cut losses when signals turn

**2. Patience:**

- Wait for VEI < 1.0
- Wait for bullish divergences
- Wait for price at support
- Sometimes best trade is no trade

**3. Risk Management:**

- Position sizing by VEI and setup quality
- Diversification across names
- Never risk more than can afford
- Capital preservation > premium collection

### The Reality of Cash-Secured Puts

**Expectations:**

- Win rate: 70-90% (if selective)
- Average return: 1-3% per month
- Occasional assignments: Normal
- Drawdowns: 5-15% (well-managed account)

**Time Commitment:**

- 15-30 minutes per day for chart review
- Check VEI and key indicators
- Manage existing positions
- Scan for new opportunities

**Psychological Requirements:**

- Patience to wait for setups
- Discipline to follow rules
- Emotional control during drawdowns
- Willingness to take small losses

### Success Metrics to Track

#### Monthly

- Total premium collected
- Number of trades (quality over quantity)
- Win rate %
- Average days in trade
- Assignments (how many, at what quality levels)

#### Quarterly

- Return on deployed capital
- Average VEI of trades taken
- Setup quality distribution (how many 7/7 vs 5/7, etc.)
- Sharpe ratio
- Maximum drawdown

#### Annually

- Total return
- Comparison to buy-and-hold
- Lessons learned
- Strategy refinements

### Continuous Improvement

**Weekly Review:**

- What worked this week?
- What didn't work?
- Did I follow my rules?
- What can I do better?

**Monthly Review:**

- Review all trades
- Calculate actual probabilities by setup score
- Adjust thresholds if needed
- Refine checklist

**Quarterly Review:**

- Deep dive into performance
- Compare to benchmarks
- Adjust position sizing if needed
- Identify blind spots

---

## Quick Reference Card

**Print this and keep by your computer:**

```text
═══════════════════════════════════════════════════
  CASH-SECURED PUT QUICK REFERENCE
═══════════════════════════════════════════════════

PRE-TRADE CHECKS:
☐ VEI < 1.0 (MANDATORY)
☐ Price at daily channel low
☐ 2-3 bullish divergences (purple arrows)
☐ Up/Dn Ratio > 0.8
☐ Volume profile support nearby
☐ Stock I'd own

SETUP SCORING:
7/7 points = Full size, aggressive strikes
5-6 points = Standard size, normal strikes
3-4 points = Half size OR skip
< 3 points = SKIP

POSITION SIZING:
Max per position: 10-15% of account
Max total deployed: 50% of account
Max positions: 3-5 concurrent

STRIKE SELECTION:
Conservative: 2-5% OTM (at volume nodes)
Moderate: ATM to 2% OTM
Aggressive: ITM (only on 7/7 setups)

PROFIT TAKING:
Close at 50-70% max profit
Don't hold for last 20-30%

STOP LOSSES:
VEI > 1.5 → Close ALL positions
Bearish divergences below strike → Roll or close
Price breaks channel low → Roll or close
Up/Dn Ratio < 0.5 → Roll or close

DTE TARGET:
Entry: 30-45 days
Exit: 7-10 days (if profitable)

═══════════════════════════════════════════════════
When in doubt, DON'T TRADE. Patience pays.
═══════════════════════════════════════════════════
```

---

## Additional Resources

### Related Strategy Documents

- See `../ma-high-low.md` for MA Channel analysis
- See `../volatility-expansion-index.md` for VEI deep dive
- See `../price-volume-delta-candles.md` for divergence patterns
- See `../up-down-volume-ratio.md` for volume regime analysis

### Recommended Reading Order for New Traders

1. Read VEI document first (understand market stability filter)
2. Read MA High/Low document (understand support/resistance structure)
3. Read Price/Volume Delta document (understand accumulation/distribution)
4. Read Up/Down Volume Ratio document (understand momentum regimes)
5. Read this strategy document (put it all together)
6. Practice on paper for 1-2 months before using real money
7. Start with 1-2 positions maximum when going live
8. Scale up only after 3 months of profitable results

### Study Resources

**Paper Trading:**

- Practice entries on TradingView with replay feature
- Track hypothetical P&L in spreadsheet
- Follow all rules as if real money
- Goal: 20+ paper trades with 70%+ win rate before live

**Backtesting:**

- Review historical charts for setup quality
- Mark where you would have entered/exited
- Calculate hypothetical returns
- Identify patterns in winners vs losers

**Position Tracking Template:**

```text
Create spreadsheet with columns:
- Date Opened
- Ticker
- Strike
- DTE
- Premium Received
- Setup Score (1-7)
- VEI at Entry
- Up/Dn Ratio at Entry
- Date Closed
- Days Held
- Profit/Loss
- % Return
- Notes (what worked/didn't)
```

---

**Remember:** The goal is not to sell puts on every ticker, every day. The goal is to sell high-quality puts on high-quality setups, at high-quality prices, with favorable market conditions. Quality over quantity. Patience over action. Discipline over greed.

**Trade safely, trade smart, and let the indicators guide you.**
