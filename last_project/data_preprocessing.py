import pandas as pd
import matplotlib.pyplot as plt
import re
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

#데이터 프레임 소수점 2자리까지만 표시
pd.options.display.float_format = '{:.2f}'.format

#데이터 불러오기
incheon_data = pd.read_csv('./data/project_data.csv',encoding="cp949")
incheon_data.info()
incheon_data.describe()

#결측치 확인
pd.isnull(incheon_data).sum()
incheon_data

#데이터 전처리
incheon_data.drop(['행정구역별'],axis=1,inplace=True)
incheon_data.drop(index=[0],axis=0,inplace=True)
incheon_data.reset_index(drop=True,inplace=True)
incheon_data.columns = ['산업별','2016사업체수','2016종사자수','2016매출액',
                        '2017사업체수','2017종사자수','2017매출액',
                        '2018사업체수','2018종사자수','2018매출액',
                        '2019사업체수','2019종사자수','2019매출액']
incheon_data['산업별'] = incheon_data['산업별'].apply(lambda x:re.sub('[^A-Za-z가-힣]', '', x))
incheon_data[['2016사업체수','2016종사자수','2016매출액',
                        '2017사업체수','2017종사자수','2017매출액',
                        '2018사업체수','2018종사자수','2018매출액',
                        '2019사업체수','2019종사자수','2019매출액']] = incheon_data[['2016사업체수','2016종사자수','2016매출액',
                        '2017사업체수','2017종사자수','2017매출액',
                        '2018사업체수','2018종사자수','2018매출액',
                        '2019사업체수','2019종사자수','2019매출액']].apply(pd.to_numeric)
incheon_data_2016 = incheon_data.loc[:,['2016사업체수','2016종사자수','2016매출액']]
incheon_data_2017 = incheon_data.loc[:,['2017사업체수','2017종사자수','2017매출액']]
incheon_data_2018 = incheon_data.loc[:,['2018사업체수','2018종사자수','2018매출액']]
incheon_data_2019 = incheon_data.loc[:,['2019사업체수','2019종사자수','2019매출액']]
#성장률 계산 함수 정의
def growth_rate(a,b):
    return (b-a) / a * 100

incheon_data["2017매출액증가율"] = growth_rate(incheon_data["2016매출액"],incheon_data["2017매출액"])
incheon_data["2018매출액증가율"] = growth_rate(incheon_data["2017매출액"],incheon_data["2018매출액"])
incheon_data["2019매출액증가율"] = growth_rate(incheon_data["2018매출액"],incheon_data["2019매출액"])

incheon_data["2017종사자수증가율"] = growth_rate(incheon_data["2016종사자수"],incheon_data["2017종사자수"])
incheon_data["2018종사자수증가율"] = growth_rate(incheon_data["2017종사자수"],incheon_data["2018종사자수"])
incheon_data["2019종사자수증가율"] = growth_rate(incheon_data["2018종사자수"],incheon_data["2019종사자수"])

incheon_data["2017사업체수증가율"] = growth_rate(incheon_data["2016사업체수"],incheon_data["2017사업체수"])
incheon_data["2018사업체수증가율"] = growth_rate(incheon_data["2017사업체수"],incheon_data["2018사업체수"])
incheon_data["2019사업체수증가율"] = growth_rate(incheon_data["2018사업체수"],incheon_data["2019사업체수"])
incheon_data.set_index('산업별',inplace=True)

#전처리 완료된 데이터프레임 csv파일로 저장
incheon_data.to_csv('./data/result_data.csv',encoding='cp949')

incheon_data_t = incheon_data.reset_index()
incheon_data_t = incheon_data_t.iloc[:,1:]
incheon_data_t
x = incheon_data[['2016사업체수', '2016종사자수']]
y = incheon_data[['2016매출액']]

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, test_size=0.2)
mlr = LinearRegression()
mlr.fit(x_train, y_train)

y_predict = mlr.predict(x_test)
len(x)
a = []
type(a)
for i in range(0,len(x)):
    my_apartment = [[x.iloc[i,:][0],x.iloc[i,:][1]]]
    my_predict = mlr.predict(my_apartment)
    a.append(my_predict[0][0])

a[0][0][0]
a
plt.scatter(y_test, y_predict)
plt.xlabel("Actual Rent")
plt.ylabel("Predicted Rent")
plt.title("MULTIPLE LINEAR REGRESSION")
plt.show()

