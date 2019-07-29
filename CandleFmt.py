import backtrader as bt

class Candle4H(bt.feeds.GenericCSVData):
  params = (
    ('timeframe', bt.TimeFrame.Minutes),
    ('compression', 60*4),

    ('datetime', 7),
    ('time', 4),
    ('open', 3),
    ('high', 1),
    ('low', 2),
    ('close', 0),
    ('volume', 6),
    ('openinterest', -1)
)
