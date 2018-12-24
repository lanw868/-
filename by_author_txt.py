#%%
import pandas as pd
import numpy as np


author_dict = {
'李白': [1, 981],'岑參': [3,385], '張九齡': [5,199], '王維': [6,407],'白居易': [8, 2741],
'杜甫': [10,1174], '李商隱': [11,536], '李頎': [140,125], '杜牧': [22,514], '陳子昂': [151,139], 
'高適': [23,205], '王勃': [25,76], '溫庭筠': [27,374], '韓愈': [28,359], '孟浩然': [30,321], 
'孟郊': [31,384], '賀知章': [32,26], '劉禹錫': [42,722], '柳宗元': [50,155], '王之渙': [51,6],
'崔顥': [180,45], '駱賓王': [53,123], '王昌齡': [56,210], '劉長卿': [57,502], '韋應物': [60,549],
'賈島': [62,396]}

data = pd.read_csv('./2018-12-24 data.csv')

for key in author_dict.keys():
    print('key:', key)

    txt_file = open('./big data contest/by_author/' + key + '.txt', 'w', encoding = 'UTF-8')
    poem = data[data['author']==key]['content'].values

    for e in poem:
        txt_file.write(e)

    print('key:', key, 'done')
