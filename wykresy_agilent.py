# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import sys

csv = sys.argv[1]
b_niekrytyczne = 300.0/60.0*1000
b_krytyczne = 15.0/60.0*1000
b_bateria = 200.0/50*1000

lb = {'101 (C)':'Otoczenie rozdzielni',
          '102 (C)':'Wlot prostownika',
          '103 (C)':'Miedzy bateriami p2',
          '104 (C)':'Czujnik urządzeń',
          '105 (C)':'Przestrzeń użytkownika pp',
          '106 (C)':'Miedzy bateriami p1',
          '107 (C)':'Górna perforacja',
          '108 (C)':'Czujnik baterii', 
          '109 (C)':'Dolna perforacja',
          '110 (C)':'Drzwi na zewnatrz',
          '111 (C)':'Pod sufitem',
          '112 (C)':'Przy podłodze',
          '113 (C)':'Wylot prostowniki',
          '114 (C)':'Tył szafy na zewnatrz',
          '115 (C)':'Wylot grzałki u',
          '116 (C)':'Zewnetrzna 0.5m',
          '117 (C)':'Zewnetrzna 1.0m',
          '118 (C)':'Zewnętrzna 2.0m',
          '119 (C)':'Przestrzeń uzytkownika zp',
          '120 (C)':'Wylot grzałki bat.',
          '203 (KDC)':'Idc - odbiory krytyczne',
          '209 (NDC)':'Idc - odbiory niekrytyczne',
          '211 (VDC)':'Idc - prąd baterii',
          '206 (VAC)':'Vac - faza 1',
          '208 (VAC)':'Vac - faza 2',
          '204 (VAC)':'Vac - faza 3',
          '214 (VDC)':'Vdc - odbiory krytyczne', 
          '213 (VDC)':'Vdc - odbiory niekrytyczne',
          '215 (VDC)':'Vdc - napięcie baterii',
          '212 (VAC)':'Vac - grzałka baterii',
          '210 (VAC)':'Vac - grzałka urządzeń użytkownika',
          '202 (HZ)' :'Hz - sterowanie wentylatora'            
}
df = pd.read_csv(csv, skiprows=40,encoding='utf-16le')
print(list(df.columns.values))

df['Time'] = pd.to_datetime(df['Time'].str[:-4])
d = []
for i in range(20):
    d.append('Alarm '+str(101+i))
for i in range(1,15):
    if i not in (4, 6,):
        d.append('Alarm '+str(201+i))
df = df.drop(columns=d) 
df = df.iloc[:, :40]

df['203 (KDC)'] = df['203 (KDC)'].multiply(b_krytyczne) 
df['209 (NDC)'] = df['209 (NDC)'].multiply(b_niekrytyczne)
df['211 (VDC)'] = df['211 (VDC)'].multiply(b_bateria)
#df['109 (C)'] = df['109 (C)']+0.7
"""
praca_wentylatora = pd.Series([])
for i in range(len(df)): 
    if df['202 (HZ)'][i] < 700.0 and df['202 (HZ)'][i] > 650.0:        
        praca_wentylatora[i] = -10.0
    else:
        praca_wentylatora[i] = None
df.insert(35, 'praca_wentylatora', praca_wentylatora)

praca_gb = pd.Series([])
for i in range(len(df)): 
    if df['212 (VAC)'][i] > 200.0:        
        praca_gb[i] = 15.0
    else:
        praca_gb[i] = None
df.insert(36, 'praca_gb', praca_gb)

praca_gu = pd.Series([])
for i in range(len(df)): 
    if df['210 (VAC)'][i] > 200.0:        
        praca_gu[i] = 17.0
    else:
        praca_gb[i] = None
df.insert(37, 'praca_gu', praca_gu)"""

if sys.argv[1] == 'warming_to_40.csv':
    wentylator = pd.Series([])
    for i in range(len(df)): 
        if df['Scan'][i] > 595 and df['Scan'][i] < 655:        
            wentylator[i] = -12.0
        else:
            wentylator[i] = None
    df.insert(38, 'wentylator', wentylator)

    gb = pd.Series([])
    for i in range(len(df)): 
        if df['Scan'][i] > 85 and df['Scan'][i] < 145:        
            gb[i] = 19.0
        else:
            gb[i] = None
    df.insert(39, 'gb', gb)

    gu = pd.Series([])
    for i in range(len(df)): 
        if df['Scan'][i] > 147 and df['Scan'][i] < 210:        
            gu[i] = 21.0
        else:
            gu[i] = None
    df.insert(40, 'gu', gu)
        

ax = plt.gca()
"""for i in (6,8,19):
    df.plot(kind='line',x='Time',y=str(101+i)+' (C)',label=lb[str(101+i)+' (C)'], ax=ax)"""
df.plot(kind='line',x='Time',y=str(101+6)+' (C)',label=lb[str(101+6)+' (C)'],color='yellow', ax=ax)
df.plot(kind='line',x='Time',y=str(101+8)+' (C)',label=lb[str(101+8)+' (C)'],color='darkorange', ax=ax)
df.plot(kind='line',x='Time',y=str(101+19)+' (C)',label=lb[str(101+19)+' (C)'],color='g', ax=ax)
#df.plot(kind='line',x='Time',y='207 (VDC)', label='Vdc - odb. krytyczne [V]',ax=ax)
df.plot(kind='line',x='Time',y='214 (VDC)', label='Napięcie odbiorów [V]', color='salmon',ax=ax)
df.plot(kind='line',x='Time',y='215 (VDC)', label='Napięcie baterii [V]',color ='red',ax=ax)
df.plot(kind='line',x='Time',y='203 (KDC)', label='Prąd odb. krytycznych [A]',color ='rosybrown',ax=ax)
df.plot(kind='line',x='Time',y='209 (NDC)', label='Prąd odb. niekrytycznych [A]',color ='lightcoral',ax=ax)
df.plot(kind='line',x='Time',y='211 (VDC)', label='Prąd baterii [A]',color ='brown',ax=ax)
"""try:
    df.plot(kind='line',x='Time',y='praca_wentylatora', label='Praca wentylatorów',color ='b',ax=ax)
except TypeError:
    pass
try:
    df.plot(kind='line',x='Time',y='praca_gu', label='Praca grzałek urządzeń',color='greenyellow',ax=ax)
except TypeError:
    pass
try:
    df.plot(kind='line',x='Time',y='praca_gb', label='Praca grzałkek baterii',color='darkviolet',ax=ax)
 
except TypeError:
    pass"""

if sys.argv[1] == 'warming_to_40.csv':
    df.plot(kind='line',x='Time',y='wentylator', label='Uszkodzenie wentylatora',color='c',ax=ax)
    df.plot(kind='line',x='Time',y='gb', label='Uszkodzenie grzałki baterii',color='plum',ax=ax)
    df.plot(kind='line',x='Time',y='gu', label='Uszkodzenie grzałki urzadzeń',color='olive',ax=ax)




 
#plt.ylabel('Temperatura')
#plt.title('System off')
#Splt.scatter(x, y)
plt.grid(True)
#df.to_excel("60-90.xlsx",sheet_name='60 90')
plt.show()

