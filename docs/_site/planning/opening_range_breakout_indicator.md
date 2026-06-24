# Opening Range Breakout Indicator — Detailed Product & Technical Spec

## 1. Overview

This indicator is a multi-session **Opening Range Breakout (ORB)** tool for TradingView that combines:

- configurable opening ranges for multiple market sessions
- anchored VWAP context
- VWAP deviation band extension filters
- breakout quality filters
- breakout grading / labeling
- session performance statistics

The indicator is intended to help users evaluate whether a breakout from a session opening range is statistically and structurally valid, rather than simply detecting that price crossed ORH or ORL.

This spec incorporates the decisions finalized in the discovery phase.

---

## 2. Primary Goals

1. Plot opening ranges for up to 3 configurable sessions.
2. Detect bullish and bearish breakout events from those session ranges.
3. Score each breakout against a configurable set of 7 filters.
4. Visually label each breakout candle with a status, failed filters, grade, or score.
5. Provide anchored VWAP context with deviation-band extension zones.
6. Show per-session statistics such as range and post-break performance.
7. Work on any chart timeframe while optionally evaluating logic on a separate calculation timeframe.

---

## 3. Non-Goals (v1)

- No alert system
- No strategy entries/exits or backtesting engine
- No broker integration
- No persistence of trade history outside chart state
- No custom dashboard beyond on-chart plots, labels, and table

---

## 4. Supported Sessions

The indicator supports **3 user-defined sessions** with defaults prefilled.

### 4.1 Session Model

Each session should be configurable with:

- `enabled`
- `name`
- `session_start_time`
- `timezone`
- `or_duration_minutes`
- `display_color`
- `show_box`
- `show_labels`

### 4.2 Default Session Presets

Recommended default presets:

- **London Open**
- **New York**
- **Asia**

Users can rename these and change times/timezones.

### 4.3 Timezone Behavior

Each session has an explicit timezone input.

This allows:
- London to anchor in London time
- New York to anchor in New York time
- Asia to anchor in the relevant exchange/session timezone

---

## 5. Timeframe Architecture

### 5.1 Chart vs Calculation Timeframe

The indicator should run on **any chart timeframe**, but core logic should use an internal **calculation timeframe**.

#### Defaults
- default chart view use case: **15m**
- default calculation timeframe: **5m**

### 5.2 User Configurability

Users may select the internal calculation timeframe.

Recommended input:
- `calculation_tf` default = `5`

Examples:
- user views chart on 15m
- OR, filters, EMA, VWAP checks, and labels are still computed from 5m data
- plots are then rendered on the current chart

### 5.3 Rationale

This preserves consistent signal quality while allowing users to inspect the setup on higher or lower display timeframes.

---

## 6. Opening Range Logic

### 6.1 Opening Range Definition

For each enabled session:

- session begins at the configured `session_start_time`
- opening range spans from session start through `or_duration_minutes`
- opening range high = highest high during OR window
- opening range low = lowest low during OR window

### 6.2 Opening Range Duration

Opening range duration is configurable per session.

#### Input mode
- preset + manual override

Examples:
- London Open = 9 minutes
- New York = 20 minutes
- Asia = 12 minutes

Actual defaults can be changed later, but implementation must support:
- presets
- direct manual minute input

### 6.3 OR Finalization

Once the OR window ends:
- ORH and ORL are frozen for that session
- the OR box and boundary lines remain visible until session expiration or chart end, depending on display settings

### 6.4 Visual Components

Each session may draw:
- OR box
- ORH line
- ORL line
- session label

Styling should rely on TradingView’s default Style tab as much as possible rather than custom toggles.

---

## 7. Breakout Detection

### 7.1 Breakout Type

Breakout mode is user-selectable.

Supported modes:
- wick through ORH/ORL
- close beyond ORH/ORL

### 7.2 Default Breakout Mode

Default = **close beyond ORH/ORL**

### 7.3 Breakout Candle Definition

The breakout candle is:

> the **first candle that closes beyond ORH or ORL**

This is the candle evaluated by the filters.

### 7.4 Breakout Direction Rules

#### Bullish breakout
- breakout candle closes above ORH

#### Bearish breakout
- breakout candle closes below ORL

### 7.5 Duplicate Handling

Supported behavior:
- one breakout event per direction per session
- optional restriction to one total breakout per session

Default:
- **one breakout per direction per session**

This means a session may produce:
- one bullish breakout event
- one bearish breakout event

If the stricter toggle is enabled, only the first valid breakout of either direction is used.

### 7.6 Confirmation Behavior

Breakouts are confirmed **on bar close only**.

No intrabar confirmation is used.

---

## 8. Anchored VWAP Model

### 8.1 VWAP Basis

The white line is an **anchored VWAP**.

### 8.2 Anchor Source

Users may choose which opening anchors the VWAP.

Supported anchor source options:
- London Open
- New York Open
- Asia Open
- Session 1 / 2 / 3 generically if session names are changed

### 8.3 Default Anchor

Default = **London Open**

### 8.4 Reset Behavior

At each selected anchor event:
- VWAP resets
- associated deviation bands reset

### 8.5 Plot

- VWAP centerline plotted as **white** by default
- actual color should remain style-configurable through TradingView Style settings

---

## 9. VWAP Deviation Bands

### 9.1 Band Method

Use TradingView-style VWAP standard deviation band behavior.

This was explicitly chosen over a custom rolling-price standard deviation model.

### 9.2 Band Levels

The breakout filters reference:

- **Band 2 = ±2.01σ**
- **Band 3 = ±2.51σ**

### 9.3 Cloud Rendering

Display emphasis should be on the extension zone between Band 2 and Band 3 only.

#### Upper cloud
- region between +2.01σ and +2.51σ

#### Lower cloud
- region between -2.01σ and -2.51σ

### 9.4 Default Cloud Colors

- upper zone: red
- lower zone: teal/green

Colors should be style-editable.

### 9.5 Why This Matters

These zones represent statistically extended premium/discount areas. Breakouts that occur after price has already reached these zones are lower quality and more likely to be exhausted.

---

## 10. Breakout Filters

Every breakout is scored against 7 independent filters.

Each filter can be enabled or disabled individually.

### 10.1 Filter List

1. BODY
2. WICK
3. VOL
4. VWAP
5. EMA
6. VWAP Band 2
7. VWAP Band 3

---

## 11. Filter Specifications

### 11.1 BODY Filter

Purpose:
- reject dojis / weak-body candles
- require breakout conviction

#### Formula
`abs(close - open) / (high - low)`

#### Rule
Passes if:
- value >= user threshold

#### Edge Case
If `(high - low) == 0`, mark filter invalid and treat as failed or skipped based on implementation policy.

Recommended v1 behavior:
- treat zero-range breakout bars as failed for BODY and WICK

#### Default Threshold
Suggested default:
- 50%

Input example:
- `body_min_pct = 0.50`

---

### 11.2 WICK Filter

Purpose:
- reject rejection candles in breakout direction

#### Bullish formula
`(high - close) / (high - low)`

#### Bearish formula
`(close - low) / (high - low)`

#### Rule
Passes if:
- value <= user threshold

#### Edge Case
If `(high - low) == 0`, treat as failed

#### Default Threshold
Suggested default:
- 25%

Input example:
- `wick_max_pct = 0.25`

---

### 11.3 VOL Filter

Purpose:
- require participation
- reject low-participation breakouts

#### Rule
Breakout candle volume must be at or above a moving average of volume.

#### Configurable Settings
- MA type selectable
- MA length selectable
- timeframe selectable as part of calculation timeframe behavior

#### Defaults
- MA type = **EMA**
- length = **20**
- timeframe = **5m** by default, user selectable

#### Formula
`volume >= volume_ma`

Where `volume_ma` is the selected MA type/length computed on the selected filter timeframe.

---

### 11.4 VWAP Filter

Purpose:
- align breakouts with session value context

#### Bullish rule
Breakout candle close must be above anchored VWAP

#### Bearish rule
Breakout candle close must be below anchored VWAP

#### Default
Enabled by default

---

### 11.5 EMA Filter

Purpose:
- align breakouts with broader trend

#### Bullish rule
Breakout candle close must be above EMA

#### Bearish rule
Breakout candle close must be below EMA

#### Defaults
- EMA length = **20**
- source = `close`
- timeframe = default **5m**, user selectable

---

### 11.6 VWAP Band 2 Filter

Purpose:
- reject breakouts that are already statistically extended

#### Band
- ±2.01σ

#### Trigger Style
User-selectable:
- fail on touch
- fail on close beyond

#### Default
- **fail on touch**

#### Bullish interpretation
Fails if breakout candle reaches or exceeds upper Band 2

#### Bearish interpretation
Fails if breakout candle reaches or exceeds lower Band 2

“Reaches” should map to the selected trigger style:
- touch mode: use high/low
- close mode: use close

---

### 11.7 VWAP Band 3 Filter

Purpose:
- stronger extension/exhaustion filter

#### Band
- ±2.51σ

#### Trigger Style
User-selectable:
- fail on touch
- fail on close beyond

#### Default
- **fail on touch**

#### Bullish interpretation
Fails if breakout candle reaches or exceeds upper Band 3

#### Bearish interpretation
Fails if breakout candle reaches or exceeds lower Band 3

---

## 12. Filter Evaluation Model

### 12.1 Enabled/Disabled State

Each filter has an on/off toggle.

Only enabled filters count toward:
- pass/fail status
- score
- grade

### 12.2 Evaluation Timing

All filters are evaluated on the breakout candle only.

### 12.3 Internal Calculation Source

Filters should use the configured internal calculation timeframe, not necessarily the current chart timeframe.

Default:
- 5m

---

## 13. Labeling System

### 13.1 Purpose

The label on the breakout candle communicates the breakout quality result.

### 13.2 Supported Display Modes

Users can choose among:

1. **Status only**
   - `OK`
   - `FAIL`

2. **Failed filter codes**
   - e.g. `VOL, VWAP`

3. **Letter grade**
   - e.g. `A`, `B`, `C`, `D`

4. **Compact score**
   - e.g. `5/7`

### 13.3 Default Mode

Recommended default:
- `Status only` or `Failed filter codes`

If replicating the example screenshot:
- use `OK` for successful breakouts

### 13.4 Status Semantics

#### `OK`
Displayed when all enabled filters pass.

#### `FAIL`
Displayed when any enabled filters fail, if status mode is used.

#### Failed code mode
Display a comma-separated or compact list of failed filters.

Example:
- `VOL, B2`
- `BODY, WICK`

### 13.5 Grade Mapping

Grade model uses simple fail-count mapping.

Default mapping:
- `A` = 0 fails
- `B` = 1 fail
- `C` = 2 fails
- `D` = 3+ fails

This mapping should be configurable if possible, but fixed defaults are acceptable in v1.

### 13.6 Label Placement

Recommended:
- bullish breakout label above candle
- bearish breakout label below candle

Actual style/color should rely largely on TradingView defaults and style customization.

---

## 14. Session Statistics Table

### 14.1 Table Columns

The session stats table should show:

- Session
- Range
- Range %
- Max R▲
- Max R▼

### 14.2 Range

Formula:
`ORH - ORL`

Units:
- price points

### 14.3 Range %

Formula:
`range / session_open * 100`

Where:
- `session_open` = opening price of the session anchor candle or first bar in session

### 14.4 R Multiple Definition

`R = OR size = ORH - ORL`

### 14.5 Max R▲ / Max R▼ Interpretation

These measure post-break expansion in R multiples.

#### Bullish breakout
- favorable excursion:
  `(highest_price_after_breakout - ORH) / R`
- adverse excursion:
  `(ORH - lowest_price_after_breakout) / R`

#### Bearish breakout
- favorable excursion:
  `(ORL - lowest_price_after_breakout) / R`
- adverse excursion:
  `(highest_price_after_breakout - ORL) / R`

### 14.6 Display Semantics

To match the visual style seen in the reference:
- show one upward metric
- show one downward metric
- color-code for favorable vs adverse if desired

If multiple breakouts exist in a session, the implementation must decide whether:
- table reflects the first breakout
- best breakout
- separate bullish/bearish rows
- aggregate extremes

#### Recommended v1 behavior
Use the **first confirmed breakout per direction**, but since table space is limited:
- either show the first valid breakout outcome
- or show session-wide max expansion beyond OR boundaries independent of label events

This is an implementation detail to finalize during coding, but the formulas above are the intended base model.

---

## 15. Overlap and Visibility

### 15.1 Overlapping Sessions

If session visuals overlap:
- both display fully
- users may hide specific sessions manually

### 15.2 Visibility Controls

Use TradingView default style controls wherever possible.

Additional logical toggles may still be needed for:
- session enabled/disabled
- table enabled/disabled
- label mode
- historical visibility mode

### 15.3 Historical Display Mode

User-selectable:
- show historical sessions
- show current session only

Default may be historical, but this can be tuned in implementation.

---

## 16. Input Summary

Below is the recommended input set.

### 16.1 Core
- `calculation_tf` (default `5`)
- `breakout_mode` (`close` or `wick`, default `close`)
- `limit_to_one_breakout_total` (bool, default `false`)
- `show_historical_sessions` (bool)

### 16.2 Sessions (x3)
For each session:
- `session_enabled`
- `session_name`
- `session_start_time`
- `session_timezone`
- `or_duration_minutes`

### 16.3 VWAP
- `vwap_anchor_session` (default London Open)
- `show_vwap`
- `show_vwap_clouds`

### 16.4 Filter Toggles
- `use_body_filter`
- `use_wick_filter`
- `use_volume_filter`
- `use_vwap_filter`
- `use_ema_filter`
- `use_band2_filter`
- `use_band3_filter`

### 16.5 Filter Thresholds
- `body_min_pct`
- `wick_max_pct`
- `volume_ma_type` (default EMA)
- `volume_ma_length` (default 20)
- `volume_tf`
- `ema_length` (default 20)
- `ema_source`
- `ema_tf`
- `band_fail_mode` (`touch` or `close`, default `touch`)

### 16.6 Labeling
- `label_mode` (`status`, `failed_codes`, `grade`, `score`)
- `show_labels`

### 16.7 Table
- `show_stats_table`

---

## 17. Functional Requirements

### FR-1
The indicator shall support 3 independently configurable sessions.

### FR-2
The indicator shall calculate ORH and ORL for each enabled session using the configured OR duration.

### FR-3
The indicator shall freeze ORH/ORL after the OR window completes.

### FR-4
The indicator shall detect bullish/bearish breakouts using the selected breakout mode.

### FR-5
The indicator shall evaluate the first breakout candle beyond ORH/ORL.

### FR-6
The indicator shall score breakouts against 7 independently toggleable filters.

### FR-7
The indicator shall compute anchored VWAP from the selected anchor session.

### FR-8
The indicator shall compute Band 2 and Band 3 using TradingView-style VWAP deviation logic.

### FR-9
The indicator shall render cloud fills between Band 2 and Band 3 above and below VWAP.

### FR-10
The indicator shall label breakout candles according to the selected label mode.

### FR-11
The indicator shall provide a session stats table with Range, Range %, Max R▲, and Max R▼.

### FR-12
The indicator shall work on any chart timeframe while using a configurable internal calculation timeframe.

### FR-13
The indicator shall confirm breakouts on bar close only.

### FR-14
The indicator shall allow both overlapping session display and per-session visibility control.

---

## 18. Implementation Notes for Pine Script

### 18.1 Likely Technical Approach
Because logic may need to evaluate on a fixed lower timeframe while plotting on another timeframe, implementation will likely require careful use of:
- `request.security()`
- session boundary detection
- anchor reset logic
- state variables for breakout tracking
- line/box/label/table objects

### 18.2 Object Management
To avoid object overflow:
- cap retained historical sessions
- reuse labels/lines where practical
- provide a current-session-only mode

### 18.3 Multi-Timeframe Care
Special attention is required for:
- mapping 5m breakout events onto 15m or higher display bars
- avoiding duplicate labels when multiple lower-timeframe events compress into one higher-timeframe bar
- preserving correct OR timing across timezones

### 18.4 Repaint Policy
Since confirmation is on bar close and there are no alerts in v1:
- avoid intrabar logic
- compute confirmed states only
- ensure labels are emitted once per confirmed breakout event

---

## 19. Open Implementation Details Still Worth Confirming During Build

These are narrower coding details, not major product assumptions:

1. Whether the stats table should reflect:
   - first breakout only
   - first valid breakout only
   - session-wide max move regardless of breakout qualification

2. Exact default OR durations for London, New York, and Asia.

3. Exact default thresholds for:
   - BODY %
   - WICK %
   - EMA length
   - label mode default

4. Whether score mode should show:
   - passed/enabled filters
   - passed/total possible filters

5. Whether failed filter abbreviations should use:
   - `B2`, `B3`
   - `VWAP2`, `VWAP3`
   - shorter aliases

---

## 20. Recommended Default Configuration (v1)

- Sessions: London Open, New York, Asia
- Timezone: explicit per session
- OR duration: preset + manual override
- Breakout mode: close beyond ORH/ORL
- Breakout count: one per direction per session
- Calculation timeframe: 5m
- Default viewing context: 15m chart
- VWAP anchor: London Open
- VWAP band method: TradingView-style
- Band 2: 2.01σ
- Band 3: 2.51σ
- Band fail mode: touch
- Volume MA: EMA 20
- EMA filter: 20 EMA on close, default 5m
- Labels: support status / fail codes / grade / score
- Alerts: none
- Confirmation: bar close only
- Overlap handling: show both, allow manual hiding
- Styling: use TradingView style defaults where possible

---

## 21. Future Enhancements

Potential post-v1 additions:

- alerts and smart alert thresholds
- filter weighting instead of simple fail counts
- separate breakout grading for bullish vs bearish continuation potential
- strategy mode with entries/exits
- backtest statistics
- breakout retest logic
- session-specific threshold presets
- session-specific anchor VWAPs
- exportable analytics panel

---
