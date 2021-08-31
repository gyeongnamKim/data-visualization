import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# 데이터 로드
data06 = pd.read_csv("./data/인천광역시·산업·사업체구분별_사업체수__종사자수_20210825114344.csv", encoding="cp949")

# 종사자수 데이터 전처리
data_num = data06[["산업별", "2006종사자", "2007종사자"
    , "2008종사자", "2009종사자", "2010종사자", "2011종사자", "2012종사자"
    , "2013종사자", "2014종사자", "2015종사자", "2016종사자", "2017종사자"
    , "2018종사자", "2019종사자"]]

df_num = data_num.transpose()
df_num = df_num.drop(["산업별"])

df_num.columns = ['전체 산업', '농업, 임업 및 어업', '광업', '제조업',
       '전기, 가스, 증기 및 공기조절 공급업', '수도, 하수 및 폐기물 처리, 원료 재생업',
       '건설업', '도매 및 소매업', '운수 및 창고업',
       '숙박 및 음식점업', '정보통신업', '금융 및 보험업', '부동산업',
       '전문, 과학 및 기술 서비스업', '사업시설 관리, 사업 지원 및 임대 서비스업',
       '공공행정, 국방 및 사회보장 행정', '교육 서비스업', '보건업 및 사회복지 서비스업',
       '예술, 스포츠 및 여가관련 서비스업', '협회 및 단체, 수리 및 기타 개인 서비스업']

df_num.rename(index={"2006종사자" : "2006", "2007종사자" : "2007"
    , "2008종사자" : "2008" , "2009종사자" : "2009"
    , "2010종사자" : "2010" , "2011종사자" : "2011"
    , "2012종사자" : "2012" , "2013종사자" : "2013"
    , "2014종사자" : "2014" , "2015종사자" : "2015"
    , "2016종사자" : "2016" , "2017종사자" : "2017"
    , "2018종사자" : "2018" , "2019종사자" : "2019"},inplace=True)

#폰트 꺠짐현상 해결
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

#정규화
min_max_scaler = MinMaxScaler()
normalerize_df_num = min_max_scaler.fit(df_num)
output_num = min_max_scaler.transform(df_num)
output_num = pd.DataFrame(output_num, columns=df_num.columns, index = list(df_num.index.values))

# 종사자수 그래프 출력 함수
def display_num(i) :
    plt.plot(output_num[output_num.columns[i]])
    plt.ylabel("종사자수(비율)")
    plt.title(output_num.columns[i])
    plt.show()

# 0~19까지 산업별 그래프
#display_num(19)


# ---------------------------------------------------------------
# 사업체수 데이터 전처리
data_business = data06[["산업별", "2006사업체", "2007사업체"
    , "2008사업체", "2009사업체", "2010사업체", "2011사업체", "2012사업체"
    , "2013사업체", "2014사업체", "2015사업체", "2016사업체", "2017사업체"
    , "2018사업체", "2019사업체"]]



df_business = data_business.transpose()
df_business = df_business.drop(["산업별"])


df_business.columns = ['전체 산업', '농업, 임업 및 어업', '광업', '제조업',
       '전기, 가스, 증기 및 공기조절 공급업', '수도, 하수 및 폐기물 처리, 원료 재생업',
       '건설업', '도매 및 소매업', '운수 및 창고업',
       '숙박 및 음식점업', '정보통신업', '금융 및 보험업', '부동산업',
       '전문, 과학 및 기술 서비스업', '사업시설 관리, 사업 지원 및 임대 서비스업',
       '공공행정, 국방 및 사회보장 행정', '교육 서비스업', '보건업 및 사회복지 서비스업',
       '예술, 스포츠 및 여가관련 서비스업', '협회 및 단체, 수리 및 기타 개인 서비스업']


df_business.rename(index={"2006사업체" : "2006", "2007사업체" : "2007"
    , "2008사업체" : "2008" , "2009사업체" : "2009"
    , "2010사업체" : "2010" , "2011사업체" : "2011"
    , "2012사업체" : "2012" , "2013사업체" : "2013"
    , "2014사업체" : "2014" , "2015사업체" : "2015"
    , "2016사업체" : "2016" , "2017사업체" : "2017"
    , "2018사업체" : "2018" , "2019사업체" : "2019"},inplace=True)

# 정규화
normalerize_df_business = min_max_scaler.fit(df_business)
output_business = min_max_scaler.transform(df_business)
output_business = pd.DataFrame(output_business, columns=df_business.columns, index = list(df_business.index.values))

#output_business.plot()
# 사업체 수 그래프 출력 함수
def display_business(i) :
    plt.plot(output_business[output_business.columns[i]])
    plt.ylabel("사업체수(비율)")
    plt.title(output_business.columns[i])
    plt.show()

# 0~19 산업별 그래프 출력
#display_business(1)

# 종사자수, 사업체수 그래프 한번에 보기
def display_all(i):
    plt.subplot(211)
    display_num(i)
    plt.subplot(212)
    display_business(i)
    plt.show()

# display_all(0)

# 성장률 함수
def growth_rate(a,b):
    rate = round(((b/a) ** (1/13) -1) * 100,2)
    return rate

# 종사자수 성장률 구하기
growth_list_num=[]
for i in range(0,20) :
    growth_list_num.append(growth_rate(df_num.iloc[0,i],df_num.iloc[13,i]))
growth_list_num



data_growth_num = pd.DataFrame(index=df_num.columns)
data_growth_num["growth_num"] = growth_list_num
data_growth_num

data_growth_num.sort_values(by=["growth_num"],axis=0, ascending=False, inplace=True)
data_growth_num.loc[data_growth_num["growth_num"] >= data_growth_num["growth_num"]["전체 산업"]]
data_growth_num['구분'] = ['up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'standard', 'down', 'down', 'down', 'down', 'down',
             'down', 'down', 'down', 'down', 'down']
# 종사자수 그래프
x = data_growth_num["growth_num"]
y = data_growth_num.index
#plt.barh(y,x, color = ['r','r','r','r','r','r','r','r','r','black','b','b','b','b','b','b','b','b','b','b'])
#plt.title("종사자수별 성장률")
#plt.axvline(2.99,0,1,linestyle="--",color="gray")
#plt.show()



# 사업체수 성장률 함수
growth_list_business=[]
for i in range(0,20) :
    growth_list_business.append(growth_rate(df_business.iloc[0,i], df_business.iloc[13,i]))
growth_list_business

data_growth_business = pd.DataFrame(index=df_business.columns)
data_growth_business["growth_business"] = growth_list_business
data_growth_business

data_growth_business.sort_values(by=["growth_business"],axis=0, ascending=False, inplace=True)
data_growth_business.loc[data_growth_business["growth_business"] >= data_growth_business["growth_business"]["전체 산업"]]

data_growth_business['구분'] = ['up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'standard', 'down', 'down',
                  'down', 'down', 'down', 'down', 'down']
# 사업체 수 성장률 그래프
x = data_growth_business["growth_business"]
y = data_growth_business.index
#plt.barh(y,x, color = ['r','r','r','r','r','r','r','r','r','r','r','r','black','b','b','b','b','b','b','b'])
#plt.title("사업체수별 성장률")
#plt.axvline(2.20,0,1,linestyle="--",color="gray")
#plt.show()

