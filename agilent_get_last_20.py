# -*- coding: utf-8 -*-
import socket
import time, sys, datetime
import colorama
from colorama import Fore, Back, Style

names = ['Otoczenie rozdzielni', 'Wlot prostownika', 'Miedzy bateriami pg', 'Czujnik urządzeń', 'Przestrzeń użytkownika pp', 'Miedzy bateriami pd', 'Górna perforacja',
'Czujnik baterii', 'Dolna perforacja', 'Drzwi na zewnatrz', 'Pod sufitem', 'Przy podłodze', 'Wylot prostowniki', 'Tył szafy na zewnatrz', 'Wylot grzałki u', 'Zewnetrzna 0.5m',
'Zewnetrzna 1.0m', 'Zewnętrzna 2.0m', 'Przestrzeń uzytkownika zp', 'Wylot grzałki bat.', 'Prąd went. 1', 'Prąd krytyczne', 'Faza 3', 'Faza 1','Faza 2', 'Prąd went. 2',
'Zailanie grzałka u.', 'Prąd baterii', 'Zasilanie grzałka bat.', 'Napiecie niekrytyczne', 'Napiecie krytyczne', 'Napięcie baterii'   ]

get_last = 10
chanel_filtr = None
if len(sys.argv) > 1:
    get_last , chanel_filtr =  int(sys.argv[1]), sys.argv[2:]

        
 
colorama.init(autoreset=True)

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        print(string)
        return False 
def recv_basic(ag):
    total_data=[]
    while True:
        data = ag.recv(512)
        #print(data)
        data = data.decode('ascii')    #
        total_data.append(data)
        time.sleep(0.5)
        if '\r\n' in data: 
            break
    return ''.join(total_data) 

         
                  
ag = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#ag.settimeout(3)
ag.connect(('192.168.4.74', 1234))
#print(dir(ag))
#ag.settimeout(None)
#ag.sendall('*IDN?\r\n'.encode('ascii'))
#ag.sendall(b'\x03')

#ag.sendall('SYSTem:LOCal\r\n'.encode('ascii'))
#sys.exit()

ag.sendall('DATA:POINTS?\r\n'.encode('ascii'))
data_number = recv_basic(ag)
#print(data_number)
ag.sendall('ROUTe:SCAN?\r\n'.encode('ascii'))
ch_scan = recv_basic(ag)
#czas_odczytu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
ag.sendall('TRIGger:TIMer?\r\n'.encode('ascii'))
time_scan = recv_basic(ag)

ch_scan = ch_scan.split('(')[1]
#print('ch_scan', ch_scan, type(ch_scan))
#sys.exit()
ch_list = [str(i) for i in range(101, 222) if str(i) in ch_scan]
#print(ch_list)
opis = dict(zip(ch_list, names))

scan_number = int(data_number) // len(ch_list)

print('Agilent status', end=' -> ')
print('| Data number:', data_number[:-2], end=' | ')
print('Scan number:', scan_number, end=' | ')
time_scan = int(float(time_scan))
ag.sendall('FORM:READ:TIME ON\n'.encode('ascii'))
time.sleep(0.2)
ag.sendall('FORM:READ:TIME:TYPE ABS\n'.encode('ascii'))
time.sleep(0.2)
ag.sendall('DATA:LAST? 1,(@101)\n'.encode('ascii'))
czas_odczytu = recv_basic(ag).split(',')
godzina_minuta = czas_odczytu[4] + ':' + czas_odczytu[5]

def przelicz_czas(sekundy):
    dni = int(sekundy // 86400 )
    godziny = int((sekundy % 86400) // 3600)
    minuty = int((sekundy % 3600) // 60)
    sekundy = int(sekundy % 60)
    napis = '-'
    if dni:
        napis += str(dni)+ 'dni '
    if godziny:
        napis += str(godziny)+'h '
    if minuty:
        napis += str(minuty)+'m '
    if sekundy:
        napis += str(sekundy)+'s '
    if napis == '-':
        napis = godzina_minuta           
    
    return f'| {napis:^11s}' 
to_overload = przelicz_czas((50000 // len(ch_list) - scan_number) * time_scan)
print(f'Time to overload: {to_overload[3:]} |')
def pomiar(ch):
    current_channel = 'ROUT:MON (@'+ch+')\r\n'
    ag.sendall(current_channel.encode('ascii'))
    ag.sendall('ROUT:MON:DATA?\r\n'.encode('ascii'))
    p = recv_basic(ag)
    return float(p) 
"""
run = True        
while run:
    try:
        for i in ch_list:
            print ('kanał: {} -> {:.3f} °C'.format(i, pomiar(i)))
        print (25*'-')    
        time.sleep(30)         
    except KeyboardInterrupt:
        run = False
        ag.close()
ag.close()
"""
ag.sendall('FORM:READ:UNIT OFF\n'.encode('ascii'))
time.sleep(0.2)
ag.sendall('FORM:READ:CHAN OFF\n'.encode('ascii'))
time.sleep(0.2)
ag.sendall('FORM:READ:ALAR OFF\n'.encode('ascii'))
time.sleep(0.2)
ag.sendall('FORM:READ:TIME OFF\n'.encode('ascii'))

if scan_number < get_last:
    get_last = scan_number


p = [x * time_scan for x in range(get_last)]
n = ''.join(map(str, [przelicz_czas(i) for i in p]))


green = True 
start_time = time.time()
nr, op, de = 'Nr', 'Opis', 'Delta'
print((48+get_last*13)*'_') 
print(Back.WHITE+Fore.BLUE+f'| {nr:^3s} | {op:^25s} | {de:^10s} {n}|')
#print((38+get_last*14)*'-') 
last ={}
if chanel_filtr and list(set(ch_list).intersection(chanel_filtr)):
    ch_list = chanel_filtr

for i in ch_list:
    command = f'DATA:LAST? {get_last},(@{i})\n'
    
    #command = 'ROUT:MON:CHAN (@'+str(i)+')\n'
    ag.sendall(command.encode('ascii'))
    #ag.write('ROUT:MON:DATA?\n'.encode('ascii'))
    time.sleep(0.2)
    lasts = recv_basic(ag).split(',')   #.split(' ')[0]
    last[i] = round(float(lasts[-1]))
    if i == '203':
        measurement = [('{:+.3f}'.format(float(j)*5000)).rjust(10, ' ') for j in lasts] 
    elif i == '211':
        measurement = [('{:+.3f}'.format(float(j)*4000)).rjust(10, ' ') for j in lasts]
    elif i == '209':    
        measurement = [('{:+.3f}'.format(float(j)*125)).rjust(10, ' ') for j in lasts] 
    elif i == '202':    
        measurement = [('{:+.3f}'.format(float(j)*125)).rjust(10, ' ') for j in lasts]                  
    else:
        measurement = [('{:+.3f}'.format(float(j))).rjust(10, ' ') for j in lasts]        
    measurement.reverse()
    

    if is_float(measurement[0]) and is_float(measurement[-1]):
        delta = ('{:+.2f}'.format(float(measurement[0]) - float(measurement[-1]))).rjust(10, ' ')
    else:
        delta = 'eeeee'    
    m = ' | '.join(measurement)
    if green:
        print(Back.LIGHTBLUE_EX+f'| {i} | {opis[i]:<25s} | {delta} | {m} |')
        green = False
    else:
        print(Back.BLUE+f'| {i} | {opis[i]:<25s} | {delta} | {m} |')
        green = True 
print((48+get_last*13)*chr(8254))              

print(f'{" "*40} {czas_odczytu[1]}-{czas_odczytu[2]}-{czas_odczytu[3]} {czas_odczytu[4]}:{czas_odczytu[5]}')
end_time = time.time()
execution_time = end_time - start_time
#print("Execution_time: ", execution_time, "sekund")
print((48+get_last*13)*'_')

last = dict(sorted(last.items(), key=lambda item: item[1], reverse=True)) #sortowanie słownika wg wartości
yellow = True
for i in last:
    if i.startswith('1'):
        if last[i] >= 0:
            if yellow:
                print(f"{Back.BLACK+(32-len(opis[i]))*' '} {opis[i]} {str(last[i]).rjust(4)}°C {Back.MAGENTA +i}  {Back.MAGENTA + last[i]*' '}")
                yellow = False
            else:
                print(f"{Back.BLACK+(32-len(opis[i]))*' '} {opis[i]} {str(last[i]).rjust(4)}°C {Back.LIGHTMAGENTA_EX +i}  {Back.LIGHTMAGENTA_EX + last[i]*' '}")
                yellow = True
        elif last[i] < 0:
            if yellow:
                print(Back.BLACK+(39+last[i])*' ', f"{Back.BLUE+last[i]*(-1)*' '} {Back.BLUE+i}", f'{str(last[i]).rjust(4)}°C  {opis[i]}')
                yellow = False
            else:
                print(Back.BLACK+(39+last[i])*' ',f"{Back.LIGHTBLUE_EX+last[i]*(-1)*' '} {Back.LIGHTBLUE_EX+i}", f'{str(last[i]).rjust(4)}°C  {opis[i]}') 
                yellow = True               
print((48+get_last*13)*chr(8254))