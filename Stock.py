import requests
import re
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


def price_Volum():

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    code = input("請輸入股票代碼:")
    rDate = input("請輸入查詢區間:")

    try:
        res = requests.get('http://jdata.yuanta.com.tw/Z/ZC/ZCW/ZCWG/ZCWG_{}_{}.djhtm'.format(code, rDate))
        if res.status_code == requests.codes.ok:
            match = re.findall(r'GetBcdData.*;', res.text)  # 原版 re.search('GetBcdData(.*)',res)
            # print(match)

            match = str(match)
            # print(match, type(match))

            match = re.sub('[ ]', ',', match)                       # 先去空白
            match = re.sub('[GetBcdData\[\]"\(\')\;]', '', match)   # 去除其他字元
            match = match.split(',')                                # 是完整清單
            # print(match,type(match))

            floatList = [float(x) for x in match]
            # print(floatList)

            # print('----------------------------------------------------')  # 取值進清單(價格)
            useList = int(len(floatList) / 2)

            priceList = []
            for price in floatList[:useList]:
                priceList.append(price)
            print("您所查詢區間的所有價格:\n", priceList)

            # print('----------------------------------------------------')  # 取值進清單(成交量)

            sumV = 0
            volumeList = []
            for volume in floatList[useList:]:
                volumeList.append(volume)
                sumV += volume
            print("您所查詢區間的所有成交量:\n", volumeList)
            # print(sumV)

            # print('----------------------------------------------------')

            priceList = np.array(priceList)
            volumeList = np.array(volumeList)
            p_v_List = priceList * volumeList
            # print(p_v_List)

            sumPriceMap = 0
            for priceMap in p_v_List:
                sumPriceMap += priceMap

            sumPriceMap = sumPriceMap / sumV
            print(f'您所查詢的股票: {code}，查詢區間: {rDate}日。\n分價平均為: {"%.2f" % sumPriceMap}元。')

    except:
        print("連線錯誤，請重新確認連線狀態。")

    return

def stock_Collector():

    headers={
       'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }

    url = 'https://www.tdcc.com.tw/smWeb/QryStockAjax.do'

    input_Date = input("請輸入欲查詢當週星期五，(格式範例20010101): ")
    input_Code = input("請輸入證券代號: ")

    res_data = {f'scaDate':{input_Date},'scaDate':{input_Date},'sqlMethod':'StockNo','stockNo':{input_Code},'radioStockNo':{input_Code},'REQ_OPR':'SELECT','clkStockNo':{input_Code}}
    html = requests.post(url, res_data, headers=headers)

    sp = BeautifulSoup(html.text, features="lxml")

    tbTitle = (sp.select('table')[6])
    print(tbTitle.select('td')[0].text,tbTitle.select('td')[1].text)

    tb = (sp.select('table')[7])

    trStart = tb.select('tr')[0]
    # trEnd = tb.select('tr')[0]

    print('%s      ' % trStart.select('td')[1].text, '%s    ' % trStart.select('td')[2].text, '%s   ' % trStart.select('td')[3].text, trStart.select('td')[4].text)

    for tr in tb.select('tr')[12:14]:
        print('%s       ' % tr.select('td')[1].text, '%s     ' % tr.select('td')[2].text, '%s               ' % tr.select('td')[3].text, tr.select('td')[4].text)

    trFourteen = tb.select('tr')[14]
    print('%s     ' % trFourteen.select('td')[1].text, '%s     ' % trFourteen.select('td')[2].text,
          '%s               ' % trFourteen.select('td')[3].text, trFourteen.select('td')[4].text)

    trFifteen = tb.select('tr')[15]
    print('%s        ' % trFifteen.select('td')[1].text, '%s  ' % trFifteen.select('td')[2].text,
          '%s              ' % trFifteen.select('td')[3].text, trFifteen.select('td')[4].text)

    return

def menu():
      print("-------------------------")
      print("1. 分價平均天數查詢。")
      print("2. 大戶持股占比查詢。")
      print("3. 結束使用。")
      print("-------------------------")


if __name__ == '__main__':

      while True:
          menu()
          choice = int(input("請選擇功能："))
          print()
          if choice == 1:
              price_Volum()
          elif choice == 2:
              stock_Collector()
          elif choice == 3:
                break
          else:
              break

      print("程式執行完畢！")