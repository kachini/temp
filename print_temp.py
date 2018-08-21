import json
from datetime import datetime
head=['serial\t','timestamp\t','CPU0','CPU1','CPU2','CPU3','MEM0','MEM','MEM2','MEM3','MEM4','MEM5','MEM6','MEM7','MEM8','MEM9','MEM10','MEM11','MEM12','MEM13','MEM14','MEM15']

f = open("data.json")
data = json.load(f)
old_serial=''
head_line=''
for item in head:
    head_line+='\t' + item 
    

for serial, temp_data  in data.iteritems():
    if old_serial != serial: 
        print '\n'
        print head_line
        old_serial=serial

    for timestamp, part in temp_data.iteritems():
        line=serial+'\t'
        line+=str(datetime.strptime(timestamp, '%Y%m%d%H%M').strftime('%d-%b-%Y %H:%M:%S'))
        for cpu in range(4):
            try:
                line+='\t' + str(part['CPU'+str(cpu)]['max'])
                if part['CPU'+str(cpu)]['max'] > 84:
                    line+='*'
            except:
                line+='\t-'


        for membuf in range(16):
            try:
                line+='\t' + str(part['MEMBUF'+str(membuf)]['max'])
                if part['MEMBUF'+str(membuf)]['max'] > 84:
                    line+='*'
            except:
                line+='\t-'

        print '\t' + line
