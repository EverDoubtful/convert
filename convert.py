import sys

__author__ = 'Alex'

#filein = open('navi.txt','r')
#=ЕСЛИ( ABS(((H$4:H$12298)-H3)>1);"+";"") - EXCEL MACROS


#try:
#    print "args = ",sys.argv[0], "   ", sys.argv[1]
#except IndexError:
#    print "no args"

try:
    filein = open(sys.argv[1], 'r')
except IOError:
    print "No file were entered"
fileOutName = sys.argv[1].split('.')[0]+'han'+'.'+ sys.argv[1].split('.')[1]
#finally:
#    print 'bye ...'
#print fileInput.readline()
#fileInput.close()
fileout = open(fileOutName,'w')
cntPack = 0
mask = 0
cntDisCoincidence = 0
packPrev = 0

for line in filein:

    if(line.split(',')[0] == '$PGIO'):
        packet = line.split(',')[3]
        #print "packPrev = ", packPrev, "Packet = ",int(packet)
        #if( (packPrev !=0 ) & ((packPrev + 1) != int(packet)) ):
        #    cntDisCoincidence = cntDisCoincidence + 1
        #    print "Packet #: ", packet
        #packPrev = int(packet)
        mask = mask | 0x01
    elif(line.split(',')[0] == '$GPRMC'):
        time = line.split(',')[1]
        time = time.split('.')[0]
        time = time[0:2]+':'+time[2:4]+':'+time[4:]
        lat = line.split(',')[3]+line.split(',')[4]
        long = line.split(',')[5]+line.split(',')[6]
        course = line.split(',')[8]
        date =  line.split(',')[9]
        date = date[0:2]+'/'+date[2:4]+'/'+date[4:]
        mask = mask | 0x02
    elif(line.split(',')[0] == '$GNGSA'):
        gln = line.split(',')[1]
        gps = line.split(',')[2][:-4]
        mask = mask | 0x04
    elif(line.split(',')[0] == '$MLG'):
        mileage = line.split(',')[1].zfill(3)
        speed = line.split(',')[2][:-4].zfill(3)

        mask = mask | 0x08
    if(mask == 0x0f):
        mask = 0
        cntPack = cntPack+1
        #result = "Packet =",packet,"gln=",gln,"gps=",gps,"Mileage=",mileage,"speed=",speed,\
#"date=",date,"time=",time,"lat=",lat,"long=",long,"course=",course
        #print result
        #fileout.write(' '.join([packet,gln,gps,mileage,speed,date,time,lat,long,course])+'\n')
        if(date == '02/12/11'):
            fileout.write(' '.join([packet,gln,gps,date,time,lat,long,mileage,speed,course])+'\n')

#print "Packets = ",cntPack, "Missed : ",cntDisCoincidence

#fileout.seek(0)
#fileout = open('han.txt','r')

fileout = open(fileOutName,'r')
strList = []
for line in fileout:
    strList.append(line)
strList.sort()
#print strList
#fileout = open('han.txt','w')
fileout = open(fileOutName,'w')
packPrev = 0
cntDisCoincidence = 0
fileout.write("Packet_N GL GP  Date     Time    Lat         Long       Mil Spd Course \n \n")

for line in strList:
    fileout.write(line)
    packet = line.split(' ')[0]
    if( (packPrev !=0 ) & ((packPrev + 1) != int(packet)) ):
            cntDisCoincidence = cntDisCoincidence + 1
            print "Packet #: ", packet
    packPrev = int(packet)

print "Packets = ",cntPack, "Missed after sort: ",cntDisCoincidence

filein.close()
fileout.close()

