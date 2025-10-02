# ORB Trading Bot Test Suite

This directory contains comprehensive tests for the ORB (Opening Range Breakout) trading bot.

## Test Files

### `test_market_analyzer.py`

Comprehensive unit tests for the `MarketAnalyzer` class, covering:

- **Opening Range Calculation**

  - Success scenarios with valid data
  - Empty data handling
  - Insufficient data scenarios
  - Missing column validation
  - Range size validation (too small ranges)
  - Range ratio calculations

- **Opportunity Window Analysis**

  - Window calculation with timezone handling
  - Active status detection
  - Duration calculations
  - Edge cases with timezone conversions

- **Breakout Detection**

  - Breakouts above ORH (Opening Range High)
  - Breakouts below ORL (Opening Range Low)
  - No breakout scenarios (price within range)
  - Window validation (only detect breakouts within opportunity window)

- **Utility Methods**
  - Current price extraction
  - Data validation and error handling
  - Timezone handling across different scenarios

### `test_orb.py`

Integration tests for the complete ORB strategy, including:

- Mock data generation and testing
- End-to-end strategy execution
- Real-time data integration with Alpaca API
- Range analysis and opportunity window validation

### `run_tests.py`

Test runner script that executes all test suites and provides a comprehensive summary.

## Running Tests

### Run All Tests

```bash
python run_tests.py
```

### Run Individual Test Files

```bash
# Market analyzer tests only
python test_market_analyzer.py

# Integration tests only
python test_orb.py
```

### Run with Verbose Output

```bash
python -m unittest test_market_analyzer.py -v
```

## Test Coverage

The test suite covers:

✅ **Core Functionality**

- Opening range calculation
- Opportunity window analysis
- Breakout detection
- Price analysis

✅ **Error Handling**

- Empty data scenarios
- Missing columns
- Invalid timezone data
- Network errors

✅ **Edge Cases**

- Market hours boundaries
- Timezone conversions
- Very small ranges
- Insufficient data

✅ **Integration**

- Alpaca API integration
- Real-time data processing
- End-to-end strategy execution

## Test Data

Tests use both:

- **Mock Data**: Generated realistic market data for unit testing
- **Real Data**: Live data from Alpaca paper trading API for integration testing

## Dependencies

Tests require the same dependencies as the main application:

- `pandas`
- `numpy`
- `alpaca-py`
- `python-dotenv`
- `pytz`

## Continuous Integration

The test suite is designed to run in CI/CD environments and provides:

- Clear pass/fail indicators
- Detailed error reporting
- Performance metrics
- Coverage reporting capabilities
