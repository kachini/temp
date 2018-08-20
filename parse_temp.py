import re
import sys
import json
import collections
from datetime import datetime
import numpy as np

my_dict = collections.OrderedDict()
ts=[]
lines = tuple(open(sys.argv[1], 'r'))
a=0

for line in lines:

    
    if re.search('MSK 2018$',line):
        cur_timestamp = datetime.strptime(''.join(line), '%a %b %d %H:%M:%S MSK %Y\n').strftime('%Y-%m-%d_%H:%M:%S')            
            
    if re.search('CPU\d\"',line) or re.search('MEMBUF\d+\"',line):
#    or re.search('DIMM\d+\"',line): 
        cur_item = line.split()[:2]
        component_name=re.sub('\"','',cur_item[0])   # component name 
        if component_name not in my_dict:
            my_dict[component_name]=collections.OrderedDict()
        else:     
            my_dict[component_name][cur_timestamp]=re.sub('\.000','',cur_item[1])
                              

# remove empty values 
# my_dict=collections.OrderedDict( (k,v) for k,v in my_dict.items() if len(v)>0)
# print my_dict['CPU3'].values()
temperature=collections.OrderedDict()
temperature['timestamp']=cur_timestamp
for part in my_dict:
    temperature[part]={}
    temperature[part]['max']=np.max(np.array(my_dict[part].values(),dtype=np.int)).round()
    temperature[part]['min']=np.min(np.array(my_dict[part].values(),dtype=np.int)).round()
    temperature[part]['mean']=np.mean(np.array(my_dict[part].values(),dtype=np.int)).round()
    temperature[part]['std']=np.std(np.array(my_dict[part].values(),dtype=np.int)).round()

#write json file 

#with open('data.json', 'w') as json_outfile:
#    json.dump( my_dict,json_outfile)
#json_outfile.close()

#with open('temperature.json', 'w') as json_outfile:
#    json.dump( temperature,json_outfile)
#json_outfile.close()

# print temperature
print "filename:",sys.argv[1]
print "Part\tMax\tMin\tMean\tstd"
for part in my_dict:
    print part,"\t",temperature[part]['max'],"\t",temperature[part]['min'],"\t",temperature[part]['mean'],"\t",temperature[part]['std']


