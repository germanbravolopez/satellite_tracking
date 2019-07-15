import time
import serial
import csv
import binascii

import socket
import pickle
#import sensors

#host = '172.16.1.9'
host = '138.4.9.56'
port = 2003
size = 1024
trama = []
data  = []

ser = serial.Serial(port='/dev/ttyAMA0',
                    baudrate=1200,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=0.1)


time.sleep(1)

# SERVER TRANSFER
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
try:
    print("UART INIT\r\n")
    start = 0
    while True:

        if ser.inWaiting > 0:

            dataRX = ser.read(size=1)
            hex_data = binascii.hexlify(dataRX)

            if ((hex_data == '0f') and (start == 0)):
                start = 1
                i = 0
                error = 0
                print("START")

            if (start == 1):
                #print hex_data
                if (i < 9):
                    if (i == 0):
                        pass
                    elif (i != 5):
                        data.insert(i-1, hex_data)
                    else:
                        try:
                            data.insert(i-1, chr(int(hex_data, 16)))
                        except ValueError:
                            error = 1
                            pass   
                    i += 1

                elif (i == 9):

                    if (hex_data == '0a' and error == 0):
                        for x in range(0, 4):
                            data[x] = bin(int(data[x], 16))
                            data[x] = int(data[x], 2)
                            # print(data[x])
                            # print(type(data[x]))
                        for x in range(6, 8):
                            data[x] = int(data[x], 16)
                        
                        #tiempo = (data[0] << 24)+(data[1] << 16)+(data[2] << 8)+data[3]
                        #tipo = data[4]
                        #subtipo = data[5].decode('hex')
                        print(str(data[6]))
                        print(str(data[7]))

                        tipo    = str(data[4])
                        print(tipo)
                        subtipo = str(data[5].decode('hex'))
                        print(subtipo)
                        #valor   = str( (data[6] << 8) + data[7])
                        valor   = str(data[6]*2**8 + data[7])
                        tiempo  = str(int(time.time()))

                        if (tipo == 'T'):                      
                            direc  = "visualizee.greencpd.lsel03.temperatura"
                            valor   = str(data[7])

                        elif (tipo == 'A'):
                            if (subtipo == 'X'):
                                direc  = "visualizee.greencpd.lsel03.acelerometro.x"
                            if (subtipo == 'Y'):
                                direc  = "visualizee.greencpd.lsel03.acelerometro.y"
                            if (subtipo == 'Z'):
                                direc  = "visualizee.greencpd.lsel03.acelerometro.z"

                        elif (tipo == 'B'):
                            direc  = "visualizee.greencpd.lsel03.boton"

                        elif(tipo == 'C'): 
                            direc  = "visualizee.greencpd.lsel03.brujula"

                        elif(tipo == 'G'):
                            if (subtipo == 'X'):
                                direc  = "visualizee.greencpd.lsel03.giroscopo.x"
                            if (subtipo == 'Y'):
                                direc  = "visualizee.greencpd.lsel03.giroscopo.y"
                            if (subtipo == 'Z'):
                                direc  = "visualizee.greencpd.lsel03.giroscopo.z"

                        espa   = " "

                        # print(tiempo)
                        dato =  direc + espa + valor + espa + tiempo
                        print(dato)
                        
                        # SERVER TRANSFER                       
                        s.send(dato)
                        #s.close()
                    else:
                        error = 0
                    i = 0
                    start = 0
                    print("FIN")
                else:
                    print("NO!")
        else:
            time.sleep(0.1)

# except KeyboardInterrupt:
#    print "Existing Program"

except serial.SerialException as e:
    None

# except:
#    print "ERROR, Existing Program"

finally:
    ser.close()
    pass
