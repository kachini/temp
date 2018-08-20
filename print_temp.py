import json
from datetime import datetime

f = open("data.json")
data = json.load(f)
for serial, temp_data  in data.iteritems():
    for timestamp, part in temp_data.iteritems():
        line=serial+ '\t'
        line+=str(datetime.strptime(timestamp, '%Y%m%d%H%M').strftime('%d-%m-%Y %H:%M:%S'))
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
