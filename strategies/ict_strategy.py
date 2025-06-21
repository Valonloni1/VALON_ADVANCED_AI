# strategies/ict_strategy.py

import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from config import DEFAULT_SYMBOL, TIMEFRAME
from typing import Tuple, Optional

class ICTStrategy:
    def __init__(self, symbol: str = DEFAULT_SYMBOL, timeframe: str = TIMEFRAME, ema_period: int = 50) -> None:
        self.symbol: str = symbol
        self.timeframe: int = self._convert_tf(timeframe)
        self.ema_period: int = ema_period

    def _convert_tf(self, tf_str: str) -> int:
        tf_map = {
            "M5": mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "H1": mt5.TIMEFRAME_H1,
            "H4": mt5.TIMEFRAME_H4,
            "D1": mt5.TIMEFRAME_D1
        }
        return tf_map.get(tf_str.upper(), mt5.TIMEFRAME_M15)

    def get_candles(self, count: int = 200) -> pd.DataFrame:
        rates = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 0, count)
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df

    def calculate_ema(self, df: pd.DataFrame) -> pd.DataFrame:
        df['ema'] = df['close'].ewm(span=self.ema_period).mean()
        return df

    def detect_fvg(self, df: pd.DataFrame) -> Tuple[bool, bool]:
        fvg_up = df['low'].iloc[-1] > df['high'].iloc[-3]
        fvg_down = df['high'].iloc[-1] < df['low'].iloc[-3]
        return fvg_up, fvg_down

    def detect_bos(self, df: pd.DataFrame) -> Tuple[bool, bool]:
        high_2 = df['high'].iloc[-3]
        high_1 = df['high'].iloc[-2]
        close = df['close'].iloc[-1]
        low_2 = df['low'].iloc[-3]
        low_1 = df['low'].iloc[-2]

        bos_up = close > high_1 > high_2
        bos_down = close < low_1 < low_2
        return bos_up, bos_down

    def detect_liquidity_grab(self, df: pd.DataFrame) -> Tuple[bool, bool]:
        last = df.iloc[-1]
        high_prev = df['high'].iloc[-4:-1].max()
        low_prev = df['low'].iloc[-4:-1].min()

        grab_above = last['high'] > high_prev and last['close'] < high_prev
        grab_below = last['low'] < low_prev and last['close'] > low_prev
        return grab_above, grab_below

    def generate_signal(self) -> Optional[str]:
        df = self.get_candles()
        df = self.calculate_ema(df)

        bos_up, bos_down = self.detect_bos(df)
        fvg_up, fvg_down = self.detect_fvg(df)
        grab_above, grab_below = self.detect_liquidity_grab(df)

        price = df['close'].iloc[-1]
        ema = df['ema'].iloc[-1]

        if grab_below and fvg_up and bos_up and price > ema:
            return "BUY"
        elif grab_above and fvg_down and bos_down and price < ema:
            return "SELL"
        else:
            return None
