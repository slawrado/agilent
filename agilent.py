import PySimpleGUI as sg
from os.path import exists
import sys, shelve
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
plt.style.use('seaborn-v0_8-whitegrid')  
lb = {'101 (C)':'',
          '102 (C)':'',
          '103 (C)':'',
          '104 (C)':'',
          '105 (C)':'',
          '106 (C)':'',
          '107 (C)':'',
          '108 (C)':'', 
          '109 (C)':'',
          '110 (C)':'',
          '111 (C)':'',
          '112 (C)':'',
          '113 (C)':'',
          '114 (C)':'',
          '115 (C)':'',
          '116 (C)':'',
          '117 (C)':'',
          '118 (C)':'',
          '119 (C)':'',
          '120 (C)':'',
          #'121 (C)':'Wilgotność w szafie'  
}
if exists('gfg.dat'):
    shelve_file = shelve.open("gfg")
else:
    shelve_file = shelve.open("gfg")
    for i in lb:
        shelve_file[i] = ''
    shelve_file['csvfile'] = ''
    shelve_file['title'] = ''
    
sg.theme('DarkTeal12')    
    
event, values = sg.Window('Agilent',
        [ [sg.Text('CSV file', size=(9, 1)), sg.InputText(size=(16, 1),default_text=shelve_file['csvfile'], key='csvfile'), sg.FileBrowse(size=(7, 1), file_types=(("Csv files", "*.csv"),))],
        [sg.Text('Chart title:', size=(9, 1)),sg.Input(size=(25,1),default_text=shelve_file['title'], justification='left',expand_x = True,key='title',enable_events=False)],
        [sg.Checkbox('101 (C)',default=False,key='101'),
        sg.Input(size=(25,1),default_text=shelve_file['101 (C)'], justification='left',expand_x = True,key='101 (C)',enable_events=False)],
        [sg.Checkbox('102 (C)',default=False,key='102'),
        sg.Input(size=(25,1),default_text=shelve_file['102 (C)'], justification='left',expand_x = True,key='102 (C)',enable_events=False)],
        [sg.Checkbox('103 (C)',default=False,key='103'),
        sg.Input(size=(25,1),default_text=shelve_file['103 (C)'], justification='left',expand_x = True,key='103 (C)',enable_events=False)],
        [sg.Checkbox('104 (C)',default=False,key='104'),
        sg.Input(size=(25,1),default_text=shelve_file['104 (C)'], justification='left',expand_x = True,key='104 (C)',enable_events=False)],
        [sg.Checkbox('105 (C)',default=False,key='105'),
        sg.Input(size=(25,1),default_text=shelve_file['105 (C)'], justification='left',expand_x = True,key='105 (C)',enable_events=False)],
        [sg.Checkbox('106 (C)',default=False,key='106'),
        sg.Input(size=(25,1),default_text=shelve_file['106 (C)'], justification='left',expand_x = True,key='106 (C)',enable_events=False)],
        [sg.Checkbox('107 (C)',default=False,key='107'),
        sg.Input(size=(25,1),default_text=shelve_file['107 (C)'], justification='left',expand_x = True,key='107 (C)',enable_events=False)],
        [sg.Checkbox('108 (C)',default=False,key='108'),
        sg.Input(size=(25,1),default_text=shelve_file['108 (C)'], justification='left',expand_x = True,key='108 (C)',enable_events=False)],
        [sg.Checkbox('109 (C)',default=False,key='109'),
        sg.Input(size=(25,1),default_text=shelve_file['109 (C)'], justification='left',expand_x = True,key='109 (C)',enable_events=False)],
        [sg.Checkbox('110 (C)',default=False,key='110'),
        sg.Input(size=(25,1),default_text=shelve_file['110 (C)'], justification='left',expand_x = True,key='110 (C)',enable_events=False)],
        [sg.Checkbox('111 (C)',default=False,key='111'),
        sg.Input(size=(25,1),default_text=shelve_file['111 (C)'], justification='left',expand_x = True,key='111 (C)',enable_events=False)],
        [sg.Checkbox('112 (C)',default=False,key='112'),
        sg.Input(size=(25,1),default_text=shelve_file['112 (C)'], justification='left',expand_x = True,key='112 (C)',enable_events=False)],
        [sg.Checkbox('113 (C)',default=False,key='113'),
        sg.Input(size=(25,1),default_text=shelve_file['113 (C)'], justification='left',expand_x = True,key='113 (C)',enable_events=False)],
        [sg.Checkbox('114 (C)',default=False,key='114'),
        sg.Input(size=(25,1),default_text=shelve_file['114 (C)'], justification='left',expand_x = True,key='114 (C)',enable_events=False)],
        [sg.Checkbox('115 (C)',default=False,key='115'),
        sg.Input(size=(25,1),default_text=shelve_file['115 (C)'], justification='left',expand_x = True,key='115 (C)',enable_events=False)],
        [sg.Checkbox('116 (C)',default=False,key='116'),
        sg.Input(size=(25,1),default_text=shelve_file['116 (C)'], justification='left',expand_x = True,key='116 (C)',enable_events=False)],
        [sg.Checkbox('117 (C)',default=False,key='117'),
        sg.Input(size=(25,1),default_text=shelve_file['117 (C)'], justification='left',expand_x = True,key='117 (C)',enable_events=False)],
        [sg.Checkbox('118 (C)',default=False,key='118'),
        sg.Input(size=(25,1),default_text=shelve_file['118 (C)'], justification='left',expand_x = True,key='118 (C)',enable_events=False)],
        [sg.Checkbox('119 (C)',default=False,key='119'),
        sg.Input(size=(25,1),default_text=shelve_file['119 (C)'], justification='left',expand_x = True,key='119 (C)',enable_events=False)],
        [sg.Checkbox('120 (C)',default=False,key='120'),
        sg.Input(size=(25,1),default_text=shelve_file['120 (C)'], justification='left',expand_x = True,key='120 (C)',enable_events=False)],        
        [sg.Checkbox('Zerowanie daty i czasu', key='czas', enable_events=False, )],
        [sg.Checkbox('Marker w punktach pomiaru', key='marker', enable_events=False, )],
        [sg.Checkbox('Eksport pomiarów do Excela', key='excel', enable_events=False, )],
        [sg.Button('OK'), ]]).read(close=True)        

if event == sg.WINDOW_CLOSED:
        sys.exit()
    
for i in lb:
    lb[i] = values[i] 
    shelve_file[i] = values[i]
shelve_file['title'] = values['title']
shelve_file['csvfile'] = values['csvfile']        
shelve_file.close()
head_name = ['Time', '101 (C)', '102 (C)', '103 (C)', '104 (C)', '105 (C)', '106 (C)', '107 (C)', '108 (C)', '109 (C)', '110 (C)', '111 (C)', '112 (C)', '113 (C)', '114 (C)', '115 (C)', '116 (C)', '117 (C)', '118 (C)', '119 (C)', '120 (C)']

file = open(values['csvfile'], encoding='utf-16le')
count = 0
line = ''
 
while not line.startswith('Scan  Control'):
    count += 1 
    # Get next line from file
    line = file.readline()


df = pd.read_csv(values['csvfile'], skiprows=count, encoding='utf-16le')#

df['Time'] = pd.to_datetime(df['Time'].str[:-4])# + timedelta(minutes=68)
if values['czas']:
    df['Time'] = df['Time'] - df['Time'][0]

    
bad_columns = []
for i in df.columns:
    if i not in head_name:
        bad_columns.append(i)
df = df.drop(columns=bad_columns) #Usunięcie kolumn alarmowych



#print (df.head())
df = df.iloc[:, :23] #Usunięcie kolumn powyżej 22  

ax = plt.gca()

wybrane = []

for i in lb:
    if values[i.split()[0]] and i in df.columns:
        wybrane.append(int(i.split()[0])-101)
        
for i in wybrane:
    if values['marker']:
        df.plot(marker='o', kind='line',x='Time',y=str(101+i)+' (C)',label=lb[str(101+i)+' (C)'], ax=ax)
    else: 
        df.plot(kind='line',x='Time',y=str(101+i)+' (C)',label=lb[str(101+i)+' (C)'], ax=ax)

plt.ylabel('Temperatura')
plt.title(values['title'])
#Splt.scatter(x, y)
plt.grid(True) 

plt.show()
if values['excel']:
    df = df.append(lb, ignore_index=True)
    new_row = pd.DataFrame(lb,index =[0])
    df = pd.concat([new_row, df]).reset_index(drop = True)
    if values['title']:
        name = values['title']
    else:
        name ='xxx'
    df.to_excel(values['csvfile'].split('/')[-1].replace('csv', 'xlsx'),sheet_name=name)
else:
    pass