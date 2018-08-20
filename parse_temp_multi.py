import os 
import re
import sys
import json
import collections
from datetime import datetime
import numpy as np
temperature=collections.OrderedDict()


def parse_temp_filename(temp_log_filename):
    
    return re.split('[_ .]',temp_log_filename)

def print_temperature(temp_log_filename,temperature):
    
    my_dict = collections.OrderedDict()
    ts=[]
    lines = tuple(open('./temp_results/'+ temp_log_filename, 'r'))
    
    for line in lines:
    
     if re.search('MSK 2018$',line):
         cur_timestamp = datetime.strptime(''.join(line), '%a %b %d %H:%M:%S MSK %Y\n').strftime('%Y-%m-%d_%H:%M:%S')            
            
     if re.search('CPU\d\"',line) or re.search('MEMBUF\d+\"',line) or re.search('DIMM\d+\"',line): 
       
         cur_item = line.split()[:2]
         component_name=re.sub('\"','',cur_item[0])   # component name 
         if component_name not in my_dict:
             my_dict[component_name]=collections.OrderedDict()
         else:     
             my_dict[component_name][cur_timestamp]=re.sub('\.000','',cur_item[1])

    serial_number=parse_temp_filename(temp_log_filename)[2]
    file_timestamp=parse_temp_filename(temp_log_filename)[3]
    if not temperature.has_key(serial_number):
        temperature[serial_number]=collections.OrderedDict()

#    temperature[serial_number]['timestamp']=cur_timestamp
    temperature[serial_number][file_timestamp]=collections.OrderedDict()
    for part in my_dict:
        try:
            temperature[serial_number][file_timestamp][part]={}
            temperature[serial_number][file_timestamp][part]['max']=np.max(np.array(my_dict[part].values(),dtype=np.int)).round()
            temperature[serial_number][file_timestamp][part]['min']=np.min(np.array(my_dict[part].values(),dtype=np.int)).round()
            temperature[serial_number][file_timestamp][part]['mean']=np.mean(np.array(my_dict[part].values(),dtype=np.int)).round()
            temperature[serial_number][file_timestamp][part]['std']=np.std(np.array(my_dict[part].values(),dtype=np.int)).round()
        except:
            temperature[serial_number][file_timestamp][part]['max']='NA'
            temperature[serial_number][file_timestamp][part]['min']='NA'
            temperature[serial_number][file_timestamp][part]['mean']='NA'
            temperature[serial_number][file_timestamp][part]['std']='NA'
# print temperature
    print "Part\tMax\tMin\tMean\tstd"
    for part in my_dict:
        print part,"\t",temperature[serial_number][file_timestamp][part]['max'],"\t",temperature[serial_number][file_timestamp][part]['min'],"\t",temperature[serial_number][file_timestamp][part]['mean'],"\t",temperature[serial_number][file_timestamp][part]['std']
#print 'Serial: '+ parse_temp_filename(sys.argv[1])[2]
#print 'Timestamp: '+ datetime.strptime(parse_temp_filename(sys.argv[1])[3], '%Y%m%d%H%M').strftime('%d-%m-%Y %H:%M:%S')
#print_temperature(sys.argv[1],temperature)

for filename in os.listdir('./temp_results/'):
    if filename.endswith(".log"): 
        print filename
        print_temperature(filename,temperature)
    else:
        continue
with open('data.json', 'w') as outfile:
    json.dump(temperature, outfile)
