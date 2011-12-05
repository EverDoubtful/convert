from sys import argv

__author__ = 'Alex'
import string
filein = open('navi.txt','r')
fileout = open('han.txt','w')

#fileInput = open(&argv, 'r')
#print fileInput.readline()
#fileInput.close()

cntPack = 0
mask = 0
cntDisCoincidence = 0
packPrev = 0
fileout.write("Packet_N GL GP  Date    Time   Lat        Long      Mil Spd Course \n \n")

for line in filein:

    if(line.split(',')[0] == '$PGIO'):
        packet = line.split(',')[3]
        #print "packPrev = ", packPrev, "Packet = ",int(packet)
        if( (packPrev !=0 ) & ((packPrev + 1) != int(packet)) ):
            cntDisCoincidence = cntDisCoincidence + 1
            print "Packet #: ", packet
        packPrev = int(packet)
        mask = mask | 0x01
    elif(line.split(',')[0] == '$GPRMC'):
        time = line.split(',')[1]
        time = time.split('.')[0]
        #time = int(float(time))
        lat = line.split(',')[3]+line.split(',')[4]
        long = line.split(',')[5]+line.split(',')[6]
        course = line.split(',')[8]
        date =  line.split(',')[9]
        mask = mask | 0x02
    elif(line.split(',')[0] == '$GNGSA'):
        gln = line.split(',')[1]
        gps = line.split(',')[2][:-4]
        mask = mask | 0x04
    elif(line.split(',')[0] == '$MLG'):
        mileage = line.split(',')[1]
        speed = line.split(',')[2][:-4]
        mask = mask | 0x08
    if(mask == 0x0f):
        mask = 0
        cntPack = cntPack+1
        #result = "Packet =",packet,"gln=",gln,"gps=",gps,"Mileage=",mileage,"speed=",speed,\
#"date=",date,"time=",time,"lat=",lat,"long=",long,"course=",course
        #print result
        #if(date == '301111'):
        fileout.write(' '.join([packet,gln,gps,date,time,lat,long,mileage,speed,course])+'\n')

print "Packets = ",cntPack, "Missed : ",cntDisCoincidence

#filein = open('han.txt','r')
#filein.seek(0)
#for line in filein:
    


filein.close()
fileout.close()

