
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-text-mining/resources/d9pwm) course resource._
# 
# ---

# # Assignment 1
# 
# In this assignment, you'll be working with messy medical data and using regex to extract relevant infromation from the data. 
# 
# Each line of the `dates.txt` file corresponds to a medical note. Each note has a date that needs to be extracted, but each date is encoded in one of many formats.
# 
# The goal of this assignment is to correctly identify all of the different date variants encoded in this dataset and to properly normalize and sort the dates. 
# 
# Here is a list of some of the variants you might encounter in this dataset:
# * 04/20/2009; 04/20/09; 4/20/09; 4/3/09
# * Mar-20-2009; Mar 20, 2009; March 20, 2009;  Mar. 20, 2009; Mar 20 2009;
# * 20 Mar 2009; 20 March 2009; 20 Mar. 2009; 20 March, 2009
# * Mar 20th, 2009; Mar 21st, 2009; Mar 22nd, 2009
# * Feb 2009; Sep 2009; Oct 2010
# * 6/2008; 12/2009
# * 2009; 2010
# 
# Once you have extracted these date patterns from the text, the next step is to sort them in ascending chronological order accoring to the following rules:
# * Assume all dates in xx/xx/xx format are mm/dd/yy
# * Assume all dates where year is encoded in only two digits are years from the 1900's (e.g. 1/5/89 is January 5th, 1989)
# * If the day is missing (e.g. 9/2009), assume it is the first day of the month (e.g. September 1, 2009).
# * If the month is missing (e.g. 2010), assume it is the first of January of that year (e.g. January 1, 2010).
# * Watch out for potential typos as this is a raw, real-life derived dataset.
# 
# With these rules in mind, find the correct date in each note and return a pandas Series in chronological order of the original Series' indices.
# 
# For example if the original series was this:
# 
#     0    1999
#     1    2010
#     2    1978
#     3    2015
#     4    1985
# 
# Your function should return this:
# 
#     0    2
#     1    4
#     2    0
#     3    1
#     4    3
# 
# Your score will be calculated using [Kendall's tau](https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient), a correlation measure for ordinal data.
# 
# *This function should return a Series of length 500 and dtype int.*

# In[2]:

import pandas as pd
doc = []
with open('dates.txt') as file:
    for line in file:
        doc.append(line)

df = pd.Series(doc)
df.head(10)


# In[3]:

import numpy as np
from datetime import datetime
def date_sorter():
    
    ## (1) 04/20/2009; 04/20/09; 4/20/09; 4/3/09
    a1_1 =df.str.extractall(r'(\d{1,2})[/-](\d{1,2})[/-](\d{2})\b')
    a1_2 =df.str.extractall(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b')
    a1 = pd.concat([a1_1,a1_2])
    a1.reset_index(inplace=True)
    a1_index = a1['level_0']

## (2)Mar-20-2009; Mar 20, 2009; March 20, 2009; Mar. 20, 2009; Mar 20 2009;
    a2 = df.str.extractall(r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[-.]* )((?:\d{1,2}[?:, -]*)\d{4})')
    a2.reset_index(inplace=True)
    a2_index = a2['level_0']
    
## (3) 20 Mar 2009; 20 March 2009; 20 Mar. 2009; 20 March, 2009
## (5) Feb 2009; Sep 2009; Oct 2010
    a3 = df.str.extractall(r'((?:\d{1,2} ))?((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[?:, -]* )(\d{4})')
    a3.reset_index(inplace=True)
    a3_index = a3['level_0']

    ## (4) Mar 20th, 2009; Mar 21st, 2009; Mar 22nd, 2009
#    a4 = df.str.extractall(r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z] )((?:\d{1,2}(?:st|nd|rd|th), )\d{4})')
#    a4.reset_index(inplace=True)
#    a4_index = a4['level_0']

    ## (6) 6/2008; 12/2009
    a6 = df.str.extractall(r'(\d{1,2})[/](\d{4})')
    a6.reset_index(inplace=True)
    a6_index = a6['level_0']
    save=[]
    for i in a6_index:
        if not(i in a1_index.values):
            save.append(i)
    save = np.asarray(save)
    a6 = a6[a6['level_0'].isin(save)]

    ## (7) 2009; 2010
    a7_1= df.str.extractall(r'[a-z]?[^0-9](\d{4})[^0-9]')
    a7_2 = df.str.extractall(r'^(\d{4})[^0-9]')
    a7 = pd.concat([a7_1,a7_2])
    a7.reset_index(inplace=True)

    a7_index = a7['level_0']
    save=[]
    for i in a7_index:
        if not((i in a2_index.values) | (i in a3_index.values) | (i in a6_index.values)):
            save.append(i)
    save = np.asarray(save)
    a7 = a7[a7['level_0'].isin(save)]
    
    s = a1.level_0.values.tolist()+a2.level_0.values.tolist()+a3.level_0.values.tolist()+a6.level_0.values.tolist()+a7.level_0.values.tolist()
    s = np.asarray(s)
#    print(diff(np.arange(500),s))
    
    a1.columns=['level_0','match','month','day','year']
    a1['year']=a1['year'].apply(str)
    a1['year']=a1['year'].apply(lambda x: '19'+x if len(x)<=2 else x)
   
    a2[1] = a2[1].apply(lambda x: x.replace(',',''))
    a2['day'] = a2[1].apply(lambda x:x.split(' ')[0])
    a2['year'] = a2[1].apply(lambda x:x.split(' ')[1])
    a2.columns=['level_0','match','month','day-year','day','year']
    a2.drop('day-year',axis=1,inplace=True) 
    
    a3.columns=['level_0','match','day','month','year']
    a3['day'] = a3['day'].replace(np.nan,-99)
    a3['day'] = a3['day'].apply(lambda x: 1 if int(x)==-99 else x)

    a3['month'] = a3.month.apply(lambda x: x[:3])
    a3['month'] = pd.to_datetime(a3.month, format='%b').dt.month
    
    a6.columns=['level_0','match','month','year']
    a6['day']=1
  
    a7.columns=['level_0','match','year']
    a7['day']=1
    a7['month']=1
   
    final = pd.concat([a1,a2,a3,a6,a7])
    final['date'] =pd.to_datetime(final['month'].apply(str)+'/'+final['day'].apply(str)+'/'+final['year'].apply(str))
    final = final.sort_values(by='level_0').set_index('level_0')

    myList = final['date']
    answer = pd.Series([i[0] for i in sorted(enumerate(myList), key=lambda x:x[1])],np.arange(500))
#    answer = pd.DataFrame([i[0] for i in sorted(enumerate(myList), key=lambda x:x[1])],np.arange(500)).reset_index()
#    answer.columns=['order','level_0']

#    answer= pd.DataFrame(final['date'].rank(ascending=1,method='first')).sort_values(by='date').reset_index()
#    answer.columns=['level_0','order']
#    answer['order']=answer['order']+1
    
#    final.reset_index(inplace=True)
#    real_final = pd.merge(final,answer,left_on='level_0',right_on='level_0',how='outer')
#    return real_final.order
    return answer

