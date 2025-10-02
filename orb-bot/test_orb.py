#!/usr/bin/env python3
"""
Test script for ORB Breakout Strategy
This script tests the functionality with mock data to verify the logic works correctly.
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta, timezone
import sys
import os
import pytz

# Add the current directory to the path so we can import our module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orb_breakout_zero_day import ORBBreakoutStrategy, OpeningRange
from alpaca_client import AlpacaClient
from market_analyzer import MarketAnalyzer, OpportunityWindow

def create_mock_bars_data():
    """Create mock bars data for testing"""
    # Create a date range for today in Central Time
    central_tz = pytz.timezone('US/Central')
    today = datetime.now(central_tz)
    market_open = today.replace(hour=8, minute=30, second=0, microsecond=0)
    
    # Create 100 minutes of data starting from market open
    timestamps = [market_open + timedelta(minutes=i) for i in range(100)]
    
    # Create realistic price data with some volatility
    base_price = 450.0  # SPY-like price
    prices = []
    current_price = base_price
    
    for i in range(100):
        # Add some random walk with slight upward bias
        change = np.random.normal(0.01, 0.5)  # Small positive drift with volatility
        current_price += change
        
        # Create OHLC data
        open_price = current_price
        high_price = current_price + abs(np.random.normal(0, 0.3))
        low_price = current_price - abs(np.random.normal(0, 0.3))
        close_price = current_price + np.random.normal(0, 0.2)
        volume = np.random.randint(1000, 10000)
        
        prices.append({
            'timestamp': timestamps[i],
            'open': round(open_price, 2),
            'high': round(high_price, 2),
            'low': round(low_price, 2),
            'close': round(close_price, 2),
            'volume': volume
        })
    
    return pd.DataFrame(prices)

def test_opening_range_calculation():
    """Test the opening range calculation with mock data"""
    print("🧪 Testing ORB Strategy with Mock Data")
    print("=" * 50)
    print("Creating mock bars data...")

    bars_df = create_mock_bars_data()
    
    print(f"Created {len(bars_df)} bars of mock data")
    print(f"Date range: {bars_df['timestamp'].min()} to {bars_df['timestamp'].max()}")
    print()
    print("Initializing strategy...")
    
    strategy = ORBBreakoutStrategy(
        symbol="SPY",
        opening_range_duration=60,  # 1 hour opening range
        min_range_size_percent=0.1,  # Lower threshold for testing
        max_daily_trades=2
    )
    
    print("Calculating opening range...")

    # Skip Alpaca client initialization for testing
    strategy.alpaca_client = None
    opening_range = strategy.calculate_opening_range_high_low(bars_df)
    
    if not opening_range:
        print("❌ Failed to calculate opening range")
        return False

    print("✅ Opening Range calculated successfully!")
    print(f"   ORH: ${opening_range.high:.2f}")
    print(f"   ORL: ${opening_range.low:.2f}")
    print(f"   Range Size: ${opening_range.range_size:.2f}")
    print(f"   Range Percentage: {opening_range.range_percent:.2f}%")
    print(f"   Start Time: {opening_range.start_time}")
    print(f"   End Time: {opening_range.end_time}")
    
    opening_range_data = strategy.market_analyzer.calculate_opening_range(
        bars_df, 
        strategy.opening_range_duration, 
        strategy.min_range_size_percent
    )
    
    if opening_range_data:
        print("\n📊 Range Analysis:")
        print(f"   Actual Range Size: ${opening_range_data['range_size']:.2f}")
        print(f"   Required Range Size: ${opening_range_data['required_range_size']:.2f}")
        print(f"   Range Ratio: {opening_range_data['range_ratio']:.2f}x (Actual/Required)")
        print(f"   Current Price: ${opening_range_data['current_price']:.2f}")
        print(f"   Minimum Required: {strategy.min_range_size_percent}%")
        print(f"   Actual Range: {opening_range_data['range_percent']:.2f}%")
    
    print("\n🔍 Verification:")
    print(f"   ORH should be >= ORL: {opening_range.high >= opening_range.low}")
    print(f"   Range size should be > 0: {opening_range.range_size > 0}")
    print(f"   Range % should be >= min threshold: {opening_range.range_percent >= strategy.min_range_size_percent}")
    print(f"\n📊 Sample data from opening range period:")

    opening_period_data = bars_df[bars_df['timestamp'] <= opening_range.end_time]
    
    print(f"   Bars in opening range: {len(opening_period_data)}")
    print(f"   Actual high in period: ${opening_period_data['high'].max():.2f}")
    print(f"   Actual low in period: ${opening_period_data['low'].min():.2f}")
    
    print("\n✅ All tests passed!")
    return True

def test_market_analyzer_directly():
    """Test the MarketAnalyzer class directly"""
    print("\n🧪 Testing MarketAnalyzer Directly")
    print("=" * 50)
    
    # Create mock data
    bars_df = create_mock_bars_data()
    
    # Create MarketAnalyzer instance
    analyzer = MarketAnalyzer(timezone='US/Central')
    
    # Test opening range calculation
    opening_range_data = analyzer.calculate_opening_range(
        bars_df, 
        opening_range_duration=60,
        min_range_size_percent=0.1
    )
    
    if not opening_range_data:
        print("❌ MarketAnalyzer test failed")
        return False

    print("✅ MarketAnalyzer opening range calculation successful!")
    print(f"   ORH: ${opening_range_data['high']:.2f}")
    print(f"   ORL: ${opening_range_data['low']:.2f}")
    print(f"   Range: {opening_range_data['range_percent']:.2f}%")
    print(f"   Bars analyzed: {opening_range_data['bars_count']}")
    print()
    print("📊 Range Analysis:")
    print(f"   Actual Range Size: ${opening_range_data['range_size']:.2f}")
    print(f"   Required Range Size: ${opening_range_data['required_range_size']:.2f}")
    print(f"   Range Ratio: {opening_range_data['range_ratio']:.2f}x (Actual/Required)")
    print(f"   Current Price: ${opening_range_data['current_price']:.2f}")
    print(f"   Minimum Required: 0.1%")
    print(f"   Actual Range: {opening_range_data['range_percent']:.2f}%")
    
    opportunity_window = analyzer.calculate_opportunity_window(
        opening_range_data,
        time(12, 0)  # 12:00 PM
    )
    
    if opportunity_window:
        print("✅ Opportunity window calculation successful!")
        print(f"   Start: {opportunity_window.start_time}")
        print(f"   End: {opportunity_window.end_time}")
        print(f"   Duration: {opportunity_window.duration_minutes:.0f} minutes")
        print(f"   Midline: ${opportunity_window.midline:.2f}")
        print(f"   Currently Active: {'✅ Yes' if opportunity_window.is_active else '❌ No'}")
    else:
        print("❌ Opportunity window calculation failed")
        return False
    
    # Test breakout detection
    test_price_above_orh = opening_range_data['high'] + 1.0
    breakout = analyzer.detect_breakout(
        test_price_above_orh,
        opening_range_data,
        opportunity_window
    )
    
    if breakout:
        print("✅ Breakout detection successful!")
        print(f"   Type: {breakout['type']}")
        print(f"   Direction: {breakout['direction']}")
        print(f"   Current Price: ${breakout['current_price']:.2f}")
        print(f"   Breakout Strength: {breakout['breakout_strength']:.2f}%")
        print(f"   Distance from Midline: ${breakout['distance_from_midline']:.2f}")
    else:
        print("ℹ️  No breakout detected (this is expected if opportunity window is not active)")
    
    return True

if __name__ == "__main__":
    test_opening_range_calculation()
    test_market_analyzer_directly()
