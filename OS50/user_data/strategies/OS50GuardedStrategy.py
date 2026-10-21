"""OS50 research-only strategy example; no demonstrated edge and no real-money authorization."""
from pandas import DataFrame
import talib.abstract as ta
from freqtrade.strategy import IStrategy


class OS50GuardedStrategy(IStrategy):
    INTERFACE_VERSION = 3
    can_short = False
    timeframe = "1h"
    startup_candle_count = 100
    process_only_new_candles = True
    stoploss = -0.02
    minimal_roi = {"0": 0.035}
    use_exit_signal = True
    trailing_stop = False

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["ema9"] = ta.EMA(dataframe, timeperiod=9)
        dataframe["ema21"] = ta.EMA(dataframe, timeperiod=21)
        dataframe["ema50"] = ta.EMA(dataframe, timeperiod=50)
        dataframe["rsi14"] = ta.RSI(dataframe, timeperiod=14)
        dataframe["atr14"] = ta.ATR(dataframe, timeperiod=14)
        dataframe["volume_mean20"] = dataframe["volume"].rolling(20).mean()
        # A prior-candle resistance level avoids peeking into future candles.
        dataframe["prior_high20"] = dataframe["high"].shift(1).rolling(20).max()
        dataframe["atr_relative"] = dataframe["atr14"] / dataframe["close"]
        votes = (
            (dataframe["ema9"] > dataframe["ema21"]).astype(int)
            + ((dataframe["rsi14"] > 52) & (dataframe["rsi14"] < 70)).astype(int)
            + (dataframe["close"] > dataframe["prior_high20"]).astype(int)
            + (dataframe["atr_relative"] < 0.025).astype(int)
        )
        dataframe["votes"] = votes
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        permitted = (
            (dataframe["votes"] >= 3)
            & (dataframe["close"] > dataframe["ema50"])
            & (dataframe["volume"] > 0)
            & (dataframe["volume"] > dataframe["volume_mean20"] * 0.6)
        )
        dataframe.loc[permitted, ["enter_long", "enter_tag"]] = (1, "os50_3_votes")
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        should_exit = (
            (dataframe["ema9"] < dataframe["ema21"])
            | (dataframe["rsi14"] > 76)
        ) & (dataframe["volume"] > 0)
        dataframe.loc[should_exit, ["exit_long", "exit_tag"]] = (1, "trend_or_rsi")
        return dataframe
