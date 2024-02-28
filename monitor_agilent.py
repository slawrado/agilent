import PySimpleGUI as sg
import socket, time

# us2n.json -> {"port": 2, "baudrate": 9600, "bits": 8, "parity": null, "stop": 0}
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False 
def recv_basic(ag):
    total_data=[]
    while True:
        data = ag.recv(512).decode('ascii') #
        total_data.append(data)
        time.sleep(0.5)
        if '\r\n' in data: 
            break
    return ''.join(total_data) 

ag = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ag.connect(('192.168.5.12', 1234))
ag.sendall('ROUTe:SCAN?\r\n'.encode('ascii'))
ch_scan = recv_basic(ag)


ch_list = []
for i in range(101,121):
    if str(i) in ch_scan:
        ch_list.append(i)

def pomiar(ch):
    current_channel = 'ROUT:MON (@'+ch+')\r\n'
    ag.sendall(current_channel.encode('ascii'))
    ag.sendall('ROUT:MON:DATA?\r\n'.encode('ascii'))
    p = recv_basic(ag)
    return float(p) 
     
sg.theme('DarkTeal12')    
def make_window():
    layout = []
    for i in ch_list:
        layout.append([sg.Text(str(i)+ ' (C)'), sg.Text(justification='left',expand_x = True,key=str(i))])
    layout.append([sg.Button('Read', key='read'), ])
    return sg.Window('Agilent', layout, finalize=True)

window = make_window()      
while True:
    event, values = window.read()
    if event == 'read':
        window['read'].update(disabled=True) 
        for i in ch_list:
            window[str(i)].update(pomiar(str(i)))
            window.refresh()
        window['read'].update(disabled=False)    
    elif event == sg.WIN_CLOSED:
        break            
ag.close() 
window.close()           




