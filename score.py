# -*- coding:utf-8 -*-
import akshare as ak
import talib as ta
import numpy as np
from prettytable import PrettyTable


def BIAS(close, timeperiod=20):
    if isinstance(close,np.ndarray):
        pass
    else:
        close = np.array(close)
    MA = ta.SMA(close, timeperiod=timeperiod)
    return (close-MA)/MA

class positive_status(object):
    BrokenLine=1
    TurnHead=2
    Cross=3
    Arrange=4
    Bias=5

class negative_status(object):
    BrokenLine = -1
    TurnHead = -2
    Cross = -3
    Arrange = -4
    Bias = -5

def GetScore(index_code):
    sw_index_df = ak.sw_index_daily(index_code=index_code, start_date="2019-8-1", end_date="2020-8-25")
    close_str = sw_index_df["close"].values
    close = close_str.astype(np.float)
    closeT = close[0]

    sma20 = ta.SMA(close, 20)

    sma20T = sma20[-1:][0]
    sma20Y = sma20[-2:-1][0]

    sma60 = ta.SMA(close, 60)
    sma60T = sma60[-1:][0]

    sma120 = ta.SMA(close, 120)
    sma120T = sma120[-1:][0]
    
    if closeT > sma20T:
        if sma20T > sma20Y:
            if sma20T > sma60T:
                if sma60T > sma120T:
                    bias=(sma60T-sma120T)/sma120T
                    if bias > 0.03:
                        score = positive_status.Bias
                    else:
                        score = positive_status.Arrange
                else:
                    score = positive_status.Cross
            else:
                score = positive_status.TurnHead
        else:
            score = positive_status.BrokenLine
    else:
         if sma20T < sma20Y:
             if sma20T < sma60T:
                 if sma60T < sma120T:
                     bias=(sma60T-sma120T)/sma120T
                     if bias < 0.03:
                         score = negative_status.Bias
                     else:
                         score = negative_status.Arrange
                 else:
                     score = negative_status.Cross
             else:
                 score = negative_status.TurnHead
         else:
             score = negative_status.BrokenLine

    return score

if __name__ == '__main__':

    sw_index_spot_df = ak.sw_index_spot()

    table = PrettyTable(["code","Trend","Score"])

    for i in sw_index_spot_df[["指数代码","指数名称"]].values:
        print(i[0])
        score=GetScore(i[0])
        # # print("{}--->score:{}".format(i,score))
        table.add_row([i[1],"L" if score>0 else "S",score])
    print(table)
