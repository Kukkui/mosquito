import talib

from core.tradeaction import TradeAction
from .base import Base
from .enums import TradeState
from core.bots.enums import BuySellMode


class Ema(Base):
    """
    Ema strategy
    About: Buy when close_price > ema20, sell when close_price < ema20 and below death_cross
    """
    def __init__(self, args, verbosity=2, pair_delimiter='_'):
        super(Ema, self).__init__(args, verbosity, pair_delimiter)
        self.name = 'Ema'
        self.min_history_ticks = 30
        self.pair = 'BTC_ETH'
        self.buy_sell_mode = BuySellMode.all

    def calculate(self, look_back, wallet):
        """
        Main strategy logic (the meat of the strategy)
        """
        (dataset_cnt, pairs_count) = self.get_dataset_count(look_back, self.group_by_field)

        # Wait until we have enough data
        if dataset_cnt < self.min_history_ticks:
            print('dataset_cnt:', dataset_cnt)
            return self.actions

        self.actions.clear()

        # Calculate indicators
        df = look_back.tail(self.min_history_ticks)
        close = df['close'].values

        # ************** Calc EMA20
        ema20_period = 25
        ema20 = talib.EMA(close[-ema20_period:], timeperiod=ema20_period)[-1]
        close_price = self.get_price(TradeState.none, df.tail(), self.pair)

        print('close_price:', close_price, 'ema:', ema20)
        if close_price <= ema20:
            new_action = TradeState.sell
        else:
            new_action = TradeState.buy

        # ************** Calc EMA Death Cross
        ema_interval_short = 6
        ema_interval_long = 25
        ema_short = talib.EMA(close[-ema_interval_short:], timeperiod=ema_interval_short)[-1]
        ema_long = talib.EMA(close[-ema_interval_long:], timeperiod=ema_interval_long)[-1]
        if ema_short <= ema_long:  # If we are below death cross, sell
            new_action = TradeState.sell

        trade_price = self.get_price(new_action, df.tail(), self.pair)

        action = TradeAction(self.pair,
                             new_action,
                             amount=None,
                             rate=trade_price,
                             buy_sell_mode=self.buy_sell_mode)

        self.actions.append(action)
        return self.actions


