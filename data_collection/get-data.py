from __future__ import unicode_literals

import requests
import json
import csv
import time
import codecs
import sys
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

api_key= "476354554d3657c31371536f445c10"
per_page = 200
API_GROUPS  = "http://api.meetup.com/2/groups"
API_EVENTS  = "http://api.meetup.com/2/events"
API_MEMBERS = "http://api.meetup.com/2/members"
API_RSVP = "http://api.meetup.com/2/rsvps"
pause = 0.35

def main():
    file_groups = open('groups.csv', 'a')
    file_events = open('events.csv', 'a')
    file_members = open('members.csv', 'a')
    file_rsvp = open('rsvp.csv', 'a')
    dict_members = {}
    
    get_groups("Exeter", "CA",file_groups , file_events , file_members , file_rsvp, dict_members)

    file_groups.close()
    file_events.close()
    file_members.close()
    file_rsvp.close()
           
def get_groups(city , state,file_groups,file_events,file_members, file_rsvp, dict_members):
        results_we_got = per_page
        offset = 0
        params = {"sign":"true","country":"US", "city":city, "state":state, "radius": 10, "key":api_key, "page":per_page, "offset":offset }
        groups = []
        while (results_we_got == per_page):           
            response=get_results(API_GROUPS, params)
            time.sleep(pause)
            offset += 1
            results_we_got = response['meta']['count']            
            group = response['results']
            groups = groups + group
        writer_group = csv.writer(file_groups)

        for item in groups:
            # schema : id, name , members ,city , state , lat , lon            
            newrow = [item['id'] , item['name'].encode('utf-8'), item['members'] , item['city'] , item['state'], item['lat'] , item['lon']] 
            
            get_events(item['id'], file_events,file_rsvp)
            time.sleep(pause)
            
            get_members(item['id'],file_members, dict_members)
            time.sleep(pause)
            
            writer_group.writerow(newrow)    


def get_events(group_id,file_events,file_rsvp):
    offset = 0
    params_events = {"sign":"true","key":api_key, "page":per_page, "offset":offset, "group_id":group_id }
    results_we_got = per_page
    response_events = get_results(API_EVENTS, params_events)
    time.sleep(pause)
    events = response_events['results'] 
    writer_events = csv.writer(file_events)
    for item in events:
    # schema : id, name , yes_rsvp_count
        newrow = [item['id'] , item['name'].encode('utf-8'), item['yes_rsvp_count']] 
        get_rsvp(item['id'],file_rsvp)
        writer_events.writerow(newrow)    

def get_members(group_id,file_members, dict_members):
    offset = 0
    params_members = {"sign":"true","key":api_key, "page":per_page, "offset":offset, "group_id":group_id }
    results_we_got = per_page
    response_members = get_results(API_MEMBERS, params_members)
    time.sleep(pause)
    members = response_members['results'] 
    writer_members = csv.writer(file_members)
    for member in members:
    # schema : id, name , city , visited
        newrow = [member['id'] , member['name'].encode('utf-8'), member['city'].encode('utf-8'), member['visited']]                            
        if member['id'] not in dict_members:
            dict_members[member['id']] = 1
            writer_members.writerow(newrow)

def get_rsvp(event_id,file_rsvp):
    print "event_id : " + str(event_id)
    offset = 0
    params_rsvp = {"sign":"true","key":api_key, "page":per_page, "offset":offset, "event_id":event_id }
    results_we_got = per_page
    rsvps = get_results(API_RSVP, params_rsvp)
    time.sleep(pause)
    writer_rsvps = csv.writer(file_rsvp)
    for rsvp in rsvps['results']:
    # schema : rsvp_id, event_id , group_id, created, response ,guests ,member name, member id, mtime
        newrow = [rsvp['rsvp_id'], rsvp['event']['id'] , rsvp['group']['id'] , rsvp['created'] , rsvp['response'], rsvp['guests'], rsvp['member']['name'].encode('utf-8'),rsvp['member']['member_id'] , rsvp['mtime']]
        writer_rsvps.writerow(newrow)
        
def get_results(API_URL, params):
    request = requests.get(API_URL,params=params)
    data = request.json()
    return data 
 
if __name__=="__main__":
        main()
 
