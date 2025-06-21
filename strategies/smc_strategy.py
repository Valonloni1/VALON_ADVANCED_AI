# strategies/smc_strategy.py

import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from config import DEFAULT_SYMBOL, TIMEFRAME
from typing import Tuple, Optional

class SMCStrategy:
    def __init__(self, symbol: str = DEFAULT_SYMBOL, timeframe: str = TIMEFRAME, ema_period: int = 50) -> None:
        self.symbol: str = symbol
        self.timeframe: int = self._convert_tf(timeframe)
        self.ema_period: int = ema_period

    def _convert_tf(self, tf_str: str) -> int:
        tf_map = {
            "M1": mt5.TIMEFRAME_M1,
            "M5": mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "H1": mt5.TIMEFRAME_H1,
            "H4": mt5.TIMEFRAME_H4,
            "D1": mt5.TIMEFRAME_D1
        }
        return tf_map.get(tf_str.upper(), mt5.TIMEFRAME_M15)

    def get_candles(self, count: int = 100) -> pd.DataFrame:
        rates = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 0, count)
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df

    def calculate_ema(self, df: pd.DataFrame) -> pd.DataFrame:
        df['ema'] = df['close'].ewm(span=self.ema_period).mean()
        return df

    def detect_bos(self, df: pd.DataFrame) -> Tuple[bool, bool]:
        bos_up = df['close'].iloc[-1] > df['high'].iloc[-2] > df['high'].iloc[-3]
        bos_down = df['close'].iloc[-1] < df['low'].iloc[-2] < df['low'].iloc[-3]
        return bos_up, bos_down

    def detect_order_block(self, df: pd.DataFrame) -> Tuple[bool, bool]:
        last = df.iloc[-2]
        current = df.iloc[-1]
        ob_buy = last['close'] < last['open'] and current['close'] > current['open']
        ob_sell = last['close'] > last['open'] and current['close'] < current['open']
        return ob_buy, ob_sell

    def generate_signal(self) -> Optional[str]:
        df = self.get_candles()
        df = self.calculate_ema(df)

        bos_up, bos_down = self.detect_bos(df)
        ob_buy, ob_sell = self.detect_order_block(df)
        price = df['close'].iloc[-1]
        ema = df['ema'].iloc[-1]

        if bos_up and ob_buy and price > ema:
            return "BUY"
        elif bos_down and ob_sell and price < ema:
            return "SELL"
        else:
            return None
