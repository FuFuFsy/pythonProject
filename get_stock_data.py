# Import the modules you need to use
import urllib
import re
import pandas as pd
import pymysql
import os


# Crawler functions for crawling web pages
def getHtml(url):
    html = urllib.request.urlopen(url).read()
    html = html.decode('gbk')
    return html


# Crawl stock code function
def getStackCode(html):
    s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    pat = re.compile(s)
    code = pat.findall(html)
    return code


#####################################################
Url = 'http://quote.eastmoney.com/stocklist.html'  # Eastern wealth network stock data link
filepath = 'C:\\Users\\Lenovo\\Desktop\\data\\'  # Define the data file save path
code = getStackCode(getHtml(Url))
# Get a collection of all stock codes (starting with 6, should be Shanghai market data)
CodeList = []
for item in code:
    if item[0] == '6':
        CodeList.append(item)
        # Capture data and save to a local csv file
        for code in CodeList:
            print('Stock%s data being acquired' % code)
            url = 'http://quotes.money.163.com/service/chddata.html?code=0' + code + \
                  '&end=20161231&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
            urllib.request.urlretrieve(url, filepath + code + '.csv')

        ##########################put stock data into the database###########################

        # Database name and password
        name = 'fsy'
        password = '12345'
        # Establish a local database connection (you need to open the database service first)
        db = pymysql.connect('localhost', name, password, charset='utf8')
        cursor = db.cursor()
        # Create database stockDataBase
        sqlSentence1 = "create database stockDataBase"
        cursor.execute(sqlSentence1)  # Select to use the current database
        sqlSentence2 = "use stockDataBase;"
        cursor.execute(sqlSentence2)

        # Get a list of local documents
        fileList = os.listdir(filepath)
        # Store each data file
        for fileName in fileList:
            try:
                data = pd.read_csv(filepath + fileName, encoding="gbk")
                # Create the data table, if the data table already exists it will be skipped to continue with the following steps print('Create data table stock_%s'% fileName[0:6])
                sqlSentence3 = "create table stock_%s" % fileName[0:6] + "(trade_date date, \
                               open0 float,    high0  float, low0 float, close0 float, vol0 float, open1  float, \
                               high1 float, close1 float, low1 float, vol1 float, open2 float, high2 float,close2 float,low2 float,vol float)"
                cursor.execute(sqlSentence3)
            except:
                print('The data sheet already exists!')
            # Iteratively read each row of the table and store it in turn (whole table storage has not been attempted)
            print('Being stored stock_%s' % fileName[0:6])
            length = len(data)
            for i in range(0, length):
                record = tuple(data.loc[i])
                # Insert data statements
                try:
                    sqlSentence4 = "insert into stock_%s" % fileName[0:6] + "(trade_date, open0, high0, low0, close0, vol0, open1, high1, close1, low1, vol1, \
                        open2, high2, close2, low2,vol) values ('%s',%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % record
                    # The data obtained from the table is messy, containing missing values, Nnone, none, etc., and needs to be processed into null values for insertion into the database
                    sqlSentence4 = sqlSentence4.replace('nan', 'null').replace('None', 'null').replace('none', 'null')
                    cursor.execute(sqlSentence4)
                except:
                    #If there is an error in the above insert process, skip this data record and continue on
                    break

        # Close cursor, commit, close database connection
        cursor.close()
        db.commit()
        db.close()


