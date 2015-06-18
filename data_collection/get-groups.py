from __future__ import unicode_literals

import requests
import json
import csv
import time
import codecs
import sys
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)
 
def main():
        get_groups("San Francisco", "CA")
        
def get_groups(city , state):        
#        (city , state) = ("San Francisco" , "CA")
        api_key= "476354554d3657c31371536f445c10"
        per_page = 200
        results_we_got = per_page
        offset = 0
        groups = []
        while (results_we_got == per_page):           
            params = {"sign":"true","country":"US", "city":city, "state":state, "radius": 10, "key":api_key, "page":per_page, "offset":offset }
            response=get_results(params)
            time.sleep(1)
            offset += 1
            results_we_got = response['meta']['count']            
            group = response['results']
            groups = groups + group
            time.sleep(1)

        file = open('groups.csv', 'a');
        writer = csv.writer(file)

        for item in groups:
            # schema : id, name , members ,city , state , lat , lon
            newrow = [item['id'] , item['name'].encode('utf-8'), item['members'] , item['city'] , item['state'], item['lat'] , item['lon']] 
            writer.writerow(newrow)    
        file.close()
             
def get_results(params):
    request = requests.get("http://api.meetup.com/2/groups",params=params)
    data = request.json()
    return data 
 
if __name__=="__main__":
        main()
 
