import time
import json
from lxml import etree
import re
import random
import datetime
import datetime
import sys
import os
import asyncio
import time, random
import requests
import os, time, random

requests.packages.urllib3.disable_warnings()
import time
from certify_code_vip_test_v1 import main
from pymysql import *

# 时间
nowTime = datetime.datetime.now().strftime('%Y_%m_%d')  # 现在
conn = connect(host='localhost', port=3306, database='tcpj_data_from_pachong', user='root', password='123456',
               charset='utf8')
# 获得Cursor对象
cs1 = conn.cursor()


def get_data_from_tcpj(pt_keywords, pt_tradestatus, pt_bid, pageIdx_client):
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh - CN, zh;q =0.9",
        "content-length": "309",
        "content - type": "application/x-www-form-urlencoded",
        "cookie": "_uab_collina=155710764840181703453248; acw_tc=77a7fa9915676518330222517ec49a8abacc9709a8c9a7581c5a9a1716; NewUserCookie=x/0ZjgxwrC3BpTI/uMstsZkSgxjYFwiylA9PZJ9IDe4wOFHOMNXlVzQUKfdV5u+ZuR3xRTWH0p9BELN+Xz4J6+EMZT/2KDCPS2zoiFsGuqQOjXaayxLIMqRgpNYKYyoYgJ7LbXi70U4xygYSCqZgPodjKP0aRQpkR557HG5qzHb2FmBJ4rqMAcclI16qWp5UKv+w+v0YNRWfMCxmSD4k4FsQuFMBTukx/y0VCKkx2n8dDf7QvGIvNg/0um9Noy2hFJOxWGLQRvND/3H9nFjIDAf0E/FNM+9o",
        # "cookie": "_uab_collina=155710764840181703453248; acw_tc=77a7faa415597160258384479eca57a735df4a746d72874024353c894a; NewUserCookie=x/0ZjgxwrC3BpTI/uMstsZkSgxjYFwiya39OHdOgT5G1vHfmqDd6KAsR8s0OUV/thXejTQ/RJWjKGBbD3mOmVSbZ2JjHtArsX4ceeif6sxRyEr3tAVGfype4oLBq89Beavs9rNM/6NASpPxBXhd8D3m8EqNkML4piXLOwtUpH7SmtMplSwiMjxQsbBn9q/vfBLzhYoLz3vd5UuNca1WqhKkJ++rmXUZdLU3wt748v0YrBTMHSCkPymSrRkp12OEJ7OXVQh2S6zwVeqspNpPT/kwdeX5SHaL6",
        "origin": "https://www.tcpjw.com",
        "referer": "https://www.tcpjw.com/OrderList/TradingCenter",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
        'X-Requested-With': 'XMLHttpRequest'
    }

    data = {
        # 搜索
        "pt_keywords": "%s" % pt_keywords,
        # 交易状态
        "pt_tradestatus": "%s" % pt_tradestatus,
        # 银行类型
        "pt_bid": "%s" % pt_bid,
        # 页码
        "pageIdx_client": "%s" % pageIdx_client,
        "X-Requested-With": "XMLHttpRequest",

    }
    try:

        response = requests.post("https://www.tcpjw.com/OrderList/TradingCenter",
                                 headers=headers, data=data, verify=False)
        print(response.status_code)
        # if pt_tradestatus=="22":
        # print(response.text)

        # 判断请求状态 切换I
        # print("----------------------请求成功-----------------------------------------------------------------")
        time.sleep(random.random() * 3)
        response.encoding = "utf-8"
        Html = response.text
        # print(Html)
        html = etree.HTML(Html)
        #

        for i in range(1, 16):

            # print(pt_tradestatus)
            # print(pt_bid)
            # band_type judgement_basis 赋值

            # 1 时间
            item_time = html.xpath('//tr[%s]/td[1]' % i)[0].text.strip("\n")

            if item_time:
                item_publish_time = "2019-" + item_time.replace('.', '-') + ":00"
                # print(item_publish_time)
                publish_time = int(time.mktime(time.strptime(item_publish_time, '%Y-%m-%d %H:%M:%S')))
            else:
                break
            # print(publish_time)
            # 2 person
            item_person = html.xpath('//tr[%s]/td[2]/span' % i)[0].text.strip("\n")

            # print(item_person)
            # 3 amount
            item_amount = html.xpath('//tr[%s]/td[3]' % i)[0].text.strip("\n")
            # print(item_amount)
            # amount = int(item_amount)
            # 4 expire_date
            expire_date = html.xpath('//tr[%s]/td[4]' % i)[0].text.replace('\n', '').replace('\t', '').replace(' ',
                                                                                                               '')
            if expire_date[-6] == "剩":
                days_to_expire_date = int(expire_date[-5:-2])
            elif expire_date[-5] == "剩":
                days_to_expire_date = int(expire_date[-4:-2])
            elif expire_date[-4] == "剩":
                days_to_expire_date = int(expire_date[-3:-2])
            # print(expire_date)
            # print(days_to_expire_date)
            # 5 interest_every_100_thousand
            interest_every_100_thousand = html.xpath('//tr[%s]/td[5]/span' % i)[0].text.strip("\n")
            # print(type(interest_every_100_thousand))
            # 十万扣息 为竞价不是数字
            # if "竞" in interest_every_100_thousand:
            #     interest_every_100_thousand_ = interest_every_100_thousand
            # else:
            #     interest_every_100_thousand_ = int(interest_every_100_thousand)
            if "竞" not in interest_every_100_thousand:
                interest_every_100_thousand_ = int(interest_every_100_thousand)
            # print(interest_every_100_thousand)
            # 6 annual_interest
            annual_interest = html.xpath('//tr[%s]/td[6]' % i)[0].text.strip("\n")
            # 7 defect_spot% i)% i)
            defect_spot = html.xpath('//tr[%s]/td[7]/span' % i)[0].text.strip("\n")
            # print(defect_spot)
            if "无" in defect_spot:
                defect_spot = "无"
            else:
                defect_spot = "有"

            # #判断订单状态
            if pt_tradestatus == "00":
                operation = "接单"
            elif pt_tradestatus == "22":
                operation = "交易完成"

            if pt_bid == "2":
                band_type = "城商"
                judgement_basis = pt_bid
                if "完成" in operation:
                    # print("-------------------------------查看状态，接单中搜索，如果有，更新状态位订单完成---------------------------")
                    try:
                        # 更新
                        cs1.execute(
                            'update tcpj_csdata set operation="交易完成" where bank_type=%s and judgement_basis=%s and publish_time =%s and person=%s and amount=%s and expire_date=%s and interest_every_100_thousand=%s and annual_interest=%s and defect_spot=%s',
                            (band_type, judgement_basis, publish_time, item_person, float(item_amount),
                             int(days_to_expire_date), interest_every_100_thousand_, annual_interest, defect_spot))
                        print("-------------update------------------------------")
                    except (IndexError, Exception) as e:
                        print(e)
                        pass

                params = [band_type,
                          judgement_basis,
                          publish_time,
                          item_time,
                          item_person,
                          float(item_amount),
                          int(days_to_expire_date),
                          interest_every_100_thousand_,
                          annual_interest,
                          defect_spot,
                          operation]
                # cs1.execute('insert into tcpj_csdata values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', params)
                #
                #
                cs1.execute(
                    'insert into tcpj_csdata(band_type,judgement_basis,publish_time,item_time,person,amount,expire_date,interest_every_100_thousand,annual_interest,defect_spot,operation) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    params)
                # cs1.close()
                conn.commit()
                print("Data into database")

                print("---------爬取第%s行数据--------------------------------------------------------" % i)
                print("银行类型：%s" % band_type)
                print("判断依据：%s" % judgement_basis)
                print("非时间戳类型，发布时间: %s" % publish_time)
                print("时间戳类型，发布时间: %s" % item_time)
                print("承兑人: %s" % item_person)
                print("金额（万元）: %s" % float(item_amount))
                print("到期日: %s" % int(days_to_expire_date))
                print("每十万扣息: %s" % interest_every_100_thousand_)
                print(" 年息: %s" % annual_interest)
                print("瑕疵: %s" % defect_spot)
                print("操作: %s" % operation)

            elif pt_bid == "1":
                band_type = "国股"
                judgement_basis = pt_bid
                params_ = [band_type,
                           judgement_basis,
                           publish_time,
                           item_person,
                           float(item_amount),
                           int(days_to_expire_date),
                           interest_every_100_thousand_,
                           annual_interest,
                           defect_spot,
                           ]
                if "完成" in operation:
                    # print("-------------------------------查看状态，接单中搜索，如果有，更新状态位订单完成---------------------------")
                    try:
                        # 更新
                        cs1.execute(
                            'update tcpj_ggdata set operation="交易完成" where bank_type=%s and judgement_basis=%s and publish_time=%s and person=%s and amount=%s and expire_date=%s and interest_every_100_thousand=%s and annual_interest=%s and defect_spot=%s',
                            params_)
                        print("-------------update------------------------------")

                    except (IndexError, Exception) as e:
                        print(e)
                        pass

                # 1指 待接单  0 订单完成
                params = [band_type,
                          judgement_basis,
                          publish_time,
                          item_time,
                          item_person,
                          float(item_amount),
                          int(days_to_expire_date),
                          interest_every_100_thousand_,
                          annual_interest,
                          defect_spot,
                          operation]

                cs1.execute(
                    'insert into tcpj_ggdata(band_type,judgement_basis,publish_time,item_time,person,amount,expire_date,interest_every_100_thousand,annual_interest,defect_spot,operation) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    params)
                # cs1.close()
                conn.commit()
                print("Data into database")

                print("---------爬取第%s行数据--------------------------------------------------------" % i)
                print("银行类型：%s" % band_type)
                print("判断依据：%s" % judgement_basis)
                print("非时间戳类型，发布时间: %s" % publish_time)
                print("时间戳类型，发布时间: %s" % item_time)
                print("承兑人: %s" % item_person)
                print("金额（万元）: %s" % float(item_amount))
                print("到期日: %s" % int(days_to_expire_date))
                print("每十万扣息: %s" % interest_every_100_thousand_)
                print(" 年息: %s" % annual_interest)
                print("瑕疵: %s" % defect_spot)
                print("操作: %s" % operation)



            elif pt_bid == "3":
                band_type = "三农"
                judgement_basis = pt_bid
                if "完成" in operation:
                    # print("-------------------------------查看状态，接单中搜索，如果有，更新状态位订单完成---------------------------")
                    try:
                        # 更新
                        cs1.execute(
                            'update tcpj_sndata set operation="交易完成" where bank_type=%s and judgement_basis=%s and publish_time=%s and person=%s and amount=%s and expire_date=%s and interest_every_100_thousand=%s and annual_interest=%s and defect_spot=%s',
                            (band_type, judgement_basis, publish_time, item_person, float(item_amount),
                             int(days_to_expire_date), interest_every_100_thousand_, annual_interest, defect_spot))
                        print("-------------update------------------------------")

                    except (IndexError, Exception) as e:
                        print(e)
                        pass

                params = [band_type,
                          judgement_basis,
                          publish_time,
                          item_time,
                          item_person,
                          float(item_amount),
                          int(days_to_expire_date),
                          interest_every_100_thousand_,
                          annual_interest,
                          defect_spot,
                          operation]

                cs1.execute(
                    'insert into tcpj_sndata(band_type,judgement_basis,publish_time,item_time,person,amount,expire_date,interest_every_100_thousand,annual_interest,defect_spot,operation) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    params)
                # cs1.close()
                conn.commit()
                print("Data into database")

                print("---------爬取第%s行数据--------------------------------------------------------" % i)
                print("银行类型：%s" % band_type)
                print("判断依据：%s" % judgement_basis)
                print("非时间戳类型，发布时间: %s" % publish_time)
                print("时间戳类型，发布时间: %s" % item_time)
                print("承兑人: %s" % item_person)
                print("金额（万元）: %s" % float(item_amount))
                print("到期日: %s" % int(days_to_expire_date))
                print("每十万扣息: %s" % interest_every_100_thousand_)
                print(" 年息: %s" % annual_interest)
                print("瑕疵: %s" % defect_spot)
                print("操作: %s" % operation)


            elif pt_bid == "6":
                band_type = "村镇"
                judgement_basis = pt_bid
                if "完成" in operation:
                    # print("-------------------------------查看状态，接单中搜索，如果有，更新状态位订单完成---------------------------")
                    try:
                        # 更新
                        cs1.execute(
                            'update tcpj_tcpj_czdata set operation="交易完成" where bank_type=%s and judgement_basis=%s and publish_time=%s and person=%s and amount=%s and expire_date=%s and interest_every_100_thousand=%s and annual_interest=%s and defect_spot=%s',
                            (band_type, judgement_basis, publish_time, item_person, float(item_amount),
                             int(days_to_expire_date), interest_every_100_thousand_, annual_interest, defect_spot))
                        print("-------------update------------------------------")

                    except (IndexError, Exception) as e:
                        print(e)
                        pass
                params = [band_type,
                          judgement_basis,
                          publish_time,
                          item_time,
                          item_person,
                          float(item_amount),
                          int(days_to_expire_date),
                          interest_every_100_thousand_,
                          annual_interest,
                          defect_spot,
                          operation]

                cs1.execute(
                    'insert into tcpj_czdata(band_type,judgement_basis,publish_time,item_time,person,amount,expire_date,interest_every_100_thousand,annual_interest,defect_spot,operation) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    params)
                # cs1.close()
                conn.commit()
                print("Data into database")

                print("---------爬取第%s行数据--------------------------------------------------------" % i)
                print("银行类型：%s" % band_type)
                print("判断依据：%s" % judgement_basis)
                print("非时间戳类型，发布时间: %s" % publish_time)
                print("时间戳类型，发布时间: %s" % item_time)
                print("承兑人: %s" % item_person)
                print("金额（万元）: %s" % float(item_amount))
                print("到期日: %s" % int(days_to_expire_date))
                print("每十万扣息: %s" % interest_every_100_thousand_)
                print(" 年息: %s" % annual_interest)
                print("瑕疵: %s" % defect_spot)
                print("操作: %s" % operation)



            elif pt_bid == "7":
                band_type = "外资"
                judgement_basis = pt_bid
                if "完成" in operation:
                    # print("-------------------------------查看状态，接单中搜索，如果有，更新状态位订单完成---------------------------")
                    try:
                        # 更新
                        cs1.execute(
                            'update tcpj_wzdata set operation="交易完成" where bank_type=%s and judgement_basis=%s and publish_time=%s and person=%s and amount=%s and expire_date=%s and interest_every_100_thousand=%s and annual_interest=%s and defect_spot=%s',
                            (band_type, judgement_basis, publish_time, item_person, float(item_amount),
                             int(days_to_expire_date), interest_every_100_thousand_, annual_interest, defect_spot))
                        print("-------------update------------------------------")

                    except (IndexError, Exception) as e:
                        print(e)
                        pass
                params = [band_type, judgement_basis, publish_time, item_time,
                          item_person, float(item_amount),
                          int(days_to_expire_date), interest_every_100_thousand_, annual_interest,
                          defect_spot, operation]

                cs1.execute(
                    'insert into tcpj_wzdata(band_type,judgement_basis,publish_time,item_time,person,amount,expire_date,interest_every_100_thousand,annual_interest,defect_spot,operation) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    params)
                # cs1.close()
                conn.commit()
                print("Data into database")
                print("---------爬取第%s行数据--------------------------------------------------------" % i)
                print("银行类型：%s" % band_type)
                print("判断依据：%s" % judgement_basis)
                print("非时间戳类型，发布时间: %s" % publish_time)
                print("时间戳类型，发布时间: %s" % item_time)
                print("承兑人: %s" % item_person)
                print("金额（万元）: %s" % float(item_amount))
                print("到期日: %s" % int(days_to_expire_date))
                print("每十万扣息: %s" % interest_every_100_thousand_)
                print(" 年息: %s" % annual_interest)
                print("瑕疵: %s" % defect_spot)
                print("操作: %s" % operation)








    # UnboundLocalError: local variable 'pic_link' referenced before assignment
    except (IndexError, UnboundLocalError, Exception) as e:
        # raise e
        print(e)
        pass

        # username = '13213242228'  # 用户名
        # pwd = 'yy123456'  # 密码
        # # username = '15638749981'  #
        # # pwd = 'syf11140725com'  # 密码
        # url = 'https://www.tcpjw.com/Account/Login?rUrl=https%3A%2F%2Fwww.tcpjw.com%2F'
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(main(username, pwd, url))


if __name__ == '__main__':
    # conn = connect(host='localhost', port=3306, database='tcpj_data_from_pachong', user='root', password='123456', charset='utf8')
    # 获得Cursor对象
    # cs1 = conn.cursor()

    while True:
        # gg 国股
        # print(
        # "*************************************国股**待接单状态******************************************************************************************")
        for pageIdx_client_gg_jiedan in range(1, 6):
            # print(
            #     "--------------------爬取第%s页数据-----------------------------------------------------------" % pageIdx_client_gg_jiedan)
            time.sleep(1)

            # 国股 参数依次为 订单状态，类型，页码
            get_data_from_tcpj("", "00", "1", pageIdx_client_gg_jiedan)

        time.sleep(random.random() * 3)
        # time.sleep(5)
        # print(
        #     "*************************************国股**订单完成状态******************************************************************************************")
        for pageIdx_client_gg_wancheng in range(1, 3):
            # print(
            #     "--------------------爬取第%s页数据-----------------------------------------------------------" % pageIdx_client_gg_wancheng)
            time.sleep(1)

            # 国股 参数依次为 订单状态，类型，页码
            get_data_from_tcpj("", "22", "1", pageIdx_client_gg_wancheng)

        time.sleep(5)
        # cs 城商
        # print(
        #     "*************************************城商**待接单状态******************************************************************************************")
        for pageIdx_client_cs_jiedan in range(1, 6):
            # print(
            #     "--------------------爬取第%s页数据-----------------------------------------------------------" % pageIdx_client_cs_jiedan)
            time.sleep(1)

            # 城商 参数依次为 订单状态，类型，页码
            get_data_from_tcpj("", "00", "2", pageIdx_client_cs_jiedan)

        time.sleep(random.random() * 3)
        # print(
        #     "*************************************城商**订单完成状态******************************************************************************************")
        for pageIdx_client_cs_wancheng in range(1, 3):
            # print(
            #     "--------------------爬取第%s页数据-----------------------------------------------------------" % pageIdx_client_cs_wancheng)
            time.sleep(1)

            # 城商 参数依次为 订单状态，类型，页码
            get_data_from_tcpj("", "22", "2", pageIdx_client_cs_wancheng)

        time.sleep(5)
        # sn 三农ss

        # print(
        #     "*************************************三农**待接单状态******************************************************************************************")
        for pageIdx_client_sn_jiedan in range(1, 6):
            # print(
            #     "--------------------爬取第%s页数据-----------------------------------------------------------" % pageIdx_client_sn_jiedan)
            time.sleep(1)

            # 三农 参数依次为 订单状态，类型，页码
            get_data_from_tcpj("", "00", "3", pageIdx_client_sn_jiedan)

        time.sleep(random.random() * 3)
        # print(
        #     "*************************************三农**订单完成状态******************************************************************************************")
        for pageIdx_client_sn_wancheng in range(1, 3):
            # print(
            #     "--------------------爬取第%s页数据-----------------------------------------------------------" % pageIdx_client_sn_wancheng)
            time.sleep(1)

            # 三农 参数依次为 订单状态，类型，页码
            get_data_from_tcpj("", "22", "3", pageIdx_client_sn_wancheng)

        time.sleep(5)
        # cz 村镇
        # print(
        #     "*************************************村镇**待接单状态******************************************************************************************")
        for pageIdx_client_cz_jiedan in range(1, 3):
            # print(
            #     "--------------------爬取第%s页数据-----------------------------------------------------------" % pageIdx_client_cz_jiedan)
            time.sleep(1)

            # 村镇 参数依次为 订单状态，类型，页码
            get_data_from_tcpj("", "00", "6", pageIdx_client_cz_jiedan)

        time.sleep(random.random() * 3)
        # print(
        #     "*************************************村镇**订单完成状态******************************************************************************************")
        # for pageIdx_client_cz_wancheng in range(1, 2):
        #     # print(
        #     #     "--------------------爬取第%s页数据-----------------------------------------------------------" % pageIdx_client_cz_wancheng)
        #     time.sleep(1)
        #
        #     # 村镇 参数依次为 订单状态，类型，页码
        #     get_data_from_tcpj("", "22", "6", pageIdx_client_cz_wancheng)

        time.sleep(5)
        # wz 外资
        # print(
        #     "*************************************外资**待接单状态******************************************************************************************")
        for pageIdx_client_wz_jiedan in range(1, 2):
            # print(
            #     "--------------------爬取第%s页数据-----------------------------------------------------------" % pageIdx_client_wz_jiedan)
            time.sleep(1)

            # 外资 参数依次为 订单状态，类型，页码
            get_data_from_tcpj("", "00", "7", pageIdx_client_wz_jiedan)
        time.sleep(random.random() * 3)
        # print(
        #     "*************************************外资**订单完成状态******************************************************************************************")
        # for pageIdx_client_wz_wancheng in range(1, 2):
        #     # print(
        #     #     "--------------------爬取第%s页数据-----------------------------------------------------------" % pageIdx_client_wz_wancheng)
        #     time.sleep(1)
        #
        #     # 外资 参数依次为 订单状态，类型，页码
        #     get_data_from_tcpj("", "22", "7", pageIdx_client_wz_wancheng)

# 13213242228
# yy123456
"""
band_type,judgement_basis,publish_time,item_person,float(item_amount),
                          int(days_to_expire_date),interest_every_100_thousand_,annual_interest,
                          defect_spot,operation



band_type,judgement_basis,publish_time,person,amount,expire_date,interest_every_100_thousand,annual_interest,defect_spot,operation                          


create table tcpj_wzdata
(
  id                          int auto_increment primary key,
  band_type                   varchar(50) null,
  judgement_basis             varchar(50) null,
  publish_time                       int         null,
  person                      varchar(50) null,
  amount                     double      null,
  expire_date                 int         null,
  interest_every_100_thousand int         null,
  annual_interest             varchar(50) null,
  defect_spot                 varchar(50) null,
  operation                   varchar(50) null
);
alter table tcpj_ggdata add item_time varchar(20) null;
"""







