import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#파일 읽기
drink = pd.read_csv('./drinks.csv')
#beer 와 spirit으로 상관계수 구하기
ex_corr1 = drink[['beer_servings','spirit_servings']]
corr_result1 = ex_corr1.corr(method='pearson')
print(corr_result1)

ex_corr2 = drink[['beer_servings','spirit_servings','total_litres_of_pure_alcohol']]
corr_result2 = ex_corr2.corr(method='pearson')
print(corr_result2)
view = ['BEER','SPIRIT','TOTAL']

heat_map = sns.heatmap(corr_result2.values,
        cmap = 'Blues',
        cbar = True,
        annot = True,
        square = True,
        fmt = '.2f',
        annot_kws = {'size' : 15},
        xticklabels = view,
        yticklabels = view)

#그래프 및 히트맵 구성
sns.set(style = 'darkgrid', context='notebook')
sns.pairplot(corr_result2,height=2.5)
plt.show()