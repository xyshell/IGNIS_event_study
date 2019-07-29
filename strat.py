import backtrader as bt
import datetime
from CandleFmt import Candle4H
from utils import IGNIS_4H

class Strat(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.datetime(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.sma1 = bt.ind.SMA(period=5)  # fast moving average
        self.sma2 = bt.ind.SMA(period=10)  # slow moving average
        self.sma3 = bt.ind.SMA(period=20)  # slow moving average
        self.sma_cdl1 = bt.ind.CrossDown(self.sma1, self.sma2, plotname='sma_crossdown_level1')

        self.long_head0 = self.datas[0].close > self.sma1
        self.long_head1 = self.sma1 > self.sma2
        self.long_head2 = self.sma2 > self.sma3
        self.long_headl1 = bt.And(self.long_head0, self.long_head1)
        self.long_headl2 = bt.And(self.long_head0, self.long_head1, self.long_head2)
        bt.LinePlotterIndicator(self.long_headl2, name='long_head_level2')

        self.obv = bt.talib.OBV(self.datas[0].close, self.datas[0].volume)
        self.obv5 = bt.ind.SMA(self.obv, period=5)
        self.obv10 = bt.ind.SMA(self.obv, period=10)
        self.obv_cul1 = bt.ind.CrossOver(self.obv5, self.obv10, plotname='obv_crossup_level1')

        self.mom1= self.datas[0].close > self.datas[0].close (-1)
        self.mom2= self.datas[0].close (-1) > self.datas[0].close (-2)
        self.mom3= self.datas[0].close (-2) > self.datas[0].close (-3)
        self.moml1 = bt.And(self.mom1, self.mom2, self.mom3)

    def prenext(self):
        if self.datas[0].datetime.datetime(0) >= datetime.datetime(2019, 6, 6):
            self.buy()
            self.log('Long Position, %.4f' % self.datas[0].close[0])
    
    def next(self):
        close = self.datas[0].close[0]
        self.log('Price, %.4f' % close)

        if self.obv_cul1 > 0 and self.long_headl2:
            self.buy()

        elif self.long_headl2 and self.obv5 > self.obv10:
            self.buy()
        
        if self.sma_cdl1:
            self.close()

if __name__ == '__main__':

    # backtest from the best result
    cerebro = bt.Cerebro(stdstats=True)   
    data= Candle4H(
        dataname= IGNIS_4H, 
        dtformat= "%Y-%m-%d",
        tmformat= "%H:%M:%S",
        fromdate= datetime.datetime(2019, 6, 1),
        todate= datetime.datetime(2019, 7, 14),
    )
    cerebro.adddata(data)
    cerebro.addstrategy(Strat)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=95)
    cerebro.broker.set_cash(1000000)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.run()

    cerebro.plot(style='candlestick', barup='green', bardown='red')
    
