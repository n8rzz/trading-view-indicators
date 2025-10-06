# ORB Strategy Options Pricing Implementation

## Overview

Implement real-time options pricing data retrieval for ORB strategy entry signals using Alpaca API. This replaces mock data with actual SPY options pricing for signal evaluation.

## Implementation Plan

### Phase 1: Enhance OptionPricer with Real Alpaca Data

**Goal**: Replace mock data with real Alpaca options data for entry signal evaluation only.

**Key Requirements**:

- Only fetch pricing when entry signals are detected
- SPY options only
- Single price check per signal (no real-time updates)
- Fail gracefully if data unavailable (no blind trading)

### Phase 2: Integration Points

**Entry Signal Flow**:

1. ORB signal detected → `ORBSignalManager.detect_entry_signals()`
2. Signal created → `_get_option_pricing_data()` called
3. Real pricing fetched → Log pricing data for evaluation
4. (Future) Use pricing data to decide whether to place order

**Exit Signal Flow**:

- Continue using underlying price (SPY) for exit decisions
- No options pricing needed for exits initially

## Implementation Checklist

### OptionPricer Class Updates

- [x] Replace mock data in `fetch_option_pricing()`
- [x] Add Alpaca options API calls
- [ ] Implement comprehensive error handling
- [ ] Add data validation and freshness checks
- [ ] Enhance logging with detailed pricing info

### Integration Updates

- [ ] Ensure `_get_option_pricing_data()` handles None returns gracefully
- [ ] Update signal metadata to include pricing data when available
- [ ] Add logging for pricing data retrieval success/failure

### Testing Strategy

- [ ] Test with valid SPY options data
- [ ] Test API failure scenarios
- [ ] Test with invalid strikes/expirations
- [ ] Verify logging output format

## Key Design Decisions

1. **Single API Call Per Signal**: No caching or real-time updates initially
2. **Fail-Safe Approach**: No trading if pricing data unavailable
3. **SPY Focus**: Optimize for SPY options only
4. **Entry-Only Pricing**: Exits use underlying price
5. **Comprehensive Logging**: Full visibility into pricing data quality

## Success Criteria

- [x] Real SPY options pricing data retrieved on entry signals
- [ ] Graceful handling of API failures
- [x] Clear logging of pricing data for evaluation
- [x] No mock data in production flow
- [ ] System fails safely when data unavailable

## Data Requirements

**Contract**: SPY options with target strikes
**Expiration**: Same-day expiration (0DTE)
**Data Points**: Price, Delta, Theta, IV, Open Interest, Volume
**Timing**: Fetch only when entry signal generated

## Error Handling Strategy

- If Alpaca API fails → Log error, return None
- If no options data found → Log warning, return None
- If data is stale/invalid → Log warning, return None
- **No fallback to mock data** - if real data unavailable, don't trade

## Monitoring Points

- API response times
- Data availability rates
- Pricing data quality metrics

## Progress Update

### ✅ Completed Tasks

1. **Replace mock data in `fetch_option_pricing()`** - Mock data completely removed and replaced with real Alpaca API calls
2. **Add Alpaca options API calls** - Implemented `_fetch_option_bars()` method using `OptionBarsRequest`
3. **Real SPY options pricing data retrieved** - System now fetches actual option data from Alpaca
4. **Clear logging of pricing data** - Enhanced logging with detailed option pricing information
5. **No mock data in production flow** - All mock data removed, system uses real API calls

### 🔧 Implementation Details

- **Option Symbol Creation**: Implemented `_create_option_symbol()` for proper Alpaca format (e.g., `SPY240105C00500000`)
- **Data Fetching**: Added `_fetch_option_bars()` to retrieve real option bars data
- **Data Parsing**: Created `_parse_option_data()` to convert raw API data to `OptionPricingData` structure
- **Error Handling**: Basic error handling implemented with logging at each step
- **Testing**: Verified option symbol generation and strike calculations work correctly

### 📝 Notes

- Open Interest data not available in Alpaca bars data (marked with FIXME comment)
- Greeks are currently placeholder values - would need real-time quotes or calculation library for accurate values
- System ready for testing with real market data
