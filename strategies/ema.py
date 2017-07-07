from .base import Base
from .enums import TradeState as ts
from .tradeaction import TradeAction
import talib


class Ema(Base):
    """
    ema strategy
    """

    actions = []

    def __init__(self, args):
        super(Ema, self).__init__(args)
        self.name = 'ema'

    def calculate(self, look_back, wallet):
        """
        Main strategy logic (the meat of the strategy)
        """
        if len(look_back) < 10:
            action = TradeAction('BTC_ETH', ts.none, None, False)
            self.actions.append(action)
            return self.actions

        """
        Returns list of pairs and their corresponding actions
        """
        # print('----running strategy ema')

        close = look_back['close'].values
        volume = look_back['volume'].values
        obv = talib.OBV(close, volume)[-1]
        new_action = ts.none
        if obv >= 500:
            new_action = ts.buy

        if obv <= 400:
            new_action = ts.sell

        # print('obv:', obv, ', action: ', new_action)

        action = TradeAction('BTC_ETH', new_action, None, True)
        self.actions.append(action)
        return self.actions



