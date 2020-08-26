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
    
    # 1,2 破线&拐头
    if closeT > sma20T:
        score = positive_status.BrokenLine
        print(score)
        if sma20T > sma20Y:
            score = positive_status.TurnHead
            print(score)
    else:
        # 空方. 1,2 破线&拐头
        score = negative_status.BrokenLine
        print(score)
        if sma20T < sma20Y:
            score = negative_status.TurnHead
            print(score)

     # 3交叉；满足2为前提
    if sma20T > sma20Y:
        if sma20T > sma60T:
            score = positive_status.Cross
            print(score)
        else:
            score = positive_status.TurnHead
            print(score+0.5)
    else:
        # 空方
        if sma20T < sma60T:
            score = negative_status.Cross
            print(score)
        else:
            score = negative_status.TurnHead
            print(score+(-0.5))
    # 4排列；满足3为前提
    if sma20T > sma60T:
        if sma60T > sma120T:
            score = positive_status.Arrange
            print(score)
        else:
            score = positive_status.Cross
            print(score+0.5)
    else:
        # 空方
        if sma60T < sma120T:
            score = negative_status.Arrange
            print(score)
        else:
            score = negative_status.Cross
            print(score+(-0.5))
    # 5 乖离；满足4为前提
    if sma60T > sma120T:
        bias=(sma60T-sma120T)/sma120T
        if bias > 0.03:
            score = positive_status.Bias
            print(score)
        else:
            score = positive_status.Arrange
            print(score + 0.5)
    else:
        # 空方
        bias = (sma60T - sma120T) / sma120T
        if bias < -0.03:
            score = negative_status.Bias
            print(score)
        else:
            score = negative_status.Arrange
            print(score+(-0.5))

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
