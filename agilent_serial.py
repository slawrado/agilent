import serial, time, sys
#ag = serial.Serial(port="COM1", baudrate=9600, bytesize=8, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_TWO, timeout=1)

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False    
ag = serial.Serial(port="COM1", baudrate=9600, bytesize=8, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
#ag = serial.Serial('/dev/ttyS0', baudrate=9600, bytesize=8, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)

"""ag.write('*IDN?\r\n'.encode('ascii'))
print('id 1',ag.readline().decode('ascii'))
"""
ag.write('FORM:READ:UNIT OFF\n'.encode('ascii'))
time.sleep(0.1)
ag.write('FORM:READ:CHAN OFF\n'.encode('ascii'))
time.sleep(0.1)
ag.write('FORM:READ:ALAR OFF\n'.encode('ascii'))
time.sleep(0.1)
ag.write('FORM:READ:TIME OFF\n'.encode('ascii'))
for i in range(101,121):
    command3 = 'DATA:LAST? 4,(@'+str(i)+')\n'
    
    #command = 'ROUT:MON:CHAN (@'+str(i)+')\n'
    ag.write(command3.encode('ascii'))
    #ag.write('ROUT:MON:DATA?\n'.encode('ascii'))
    time.sleep(0.1)
    last = ag.readline().decode('ascii')#.split(' ')[0]
    k, l, m, n = [j for j in last.split(',')]
    if is_float(k):
        print('Chanel {} last four -> {:.2f}  {:.2f}  {:.2f}  {:.2f}'.format(i,float(k),float(l),float(m),float(n)))
    else:    
        print(i,'->',last[:-1])




"""    
ag.write('ROUT:SCAN:SIZE?\r\n'.encode('ascii'))
time.sleep(0.5)
print(ag.readline().decode('ascii'))
ag.write('FETC?\r\n'.encode('ascii'))
time.sleep(0.5)
s = ag.read_until().decode('ascii')
print(s)"""
