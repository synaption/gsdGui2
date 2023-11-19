import pickle
import datetime
import paho.mqtt.client as mqtt
import itertools
from map_hits import *
import gmplot
import cartopy.geodesic as gd
import numpy
from tdoa import *
from geo import *
import time
import traceback
import traceback

gmap3 = gmplot.GoogleMapPlotter(29.9610375, -90.0634532, 16)
gmap3 = gmap(gmap3)

def Average(lst):
    return sum(lst) / len(lst)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("locate/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global gmap3
    if msg.topic == 'locate':
        with open('group_of_first_hits_pickle', 'wb') as fd:
            fd.write(msg.payload)
        with open("group_of_first_hits_pickle", "rb") as fp:   # Unpickling
            group_of_first_hits = pickle.load(fp)
        # Create a list of dictionaries with all possible combinations of three dictionaries
        combinations = list(itertools.combinations(group_of_first_hits, 3))
        print(len(combinations))
        all_combinations_of_group_of_first_hits = []
        for combination in combinations[:]:
            print(combination)
            combination = list(combination)
            try: 
                result = geo(combination)
                data = {
                    'rone': result[0],
                    'rtwo': result[1],
                    'rthree': result[2],
                    'sourcelat': result[3],
                    'sourcelon': result[4],
                    'event_id': result[5],
                    'offby': result[6]
                }
                print("asdf")
                combination.append(data)
                print("asdf")
                all_combinations_of_group_of_first_hits.append(combination)  # Append data to the list
                print(data)
                print("asdf")
                
            except Exception as e:
                print("oops")
                traceback.print_exc()
        
        if len(all_combinations_of_group_of_first_hits) > 0:

            #print(msg.topic+" "+str(group_of_first_hits))
            #print(all_combinations_of_group_of_first_hits)
            sourcelat_list = []
            sourcelon_list = []
            for combination in all_combinations_of_group_of_first_hits[:]:
                print(combination)
                try: 
                    detected_location = combination[3]
                    sourcelat = detected_location['sourcelat']
                except:
                    all_combinations_of_group_of_first_hits.remove(combination)
    
            for combination in all_combinations_of_group_of_first_hits:
                try:
                    pi1 = combination[0]
                    e_id = pi1['event_id']
                    detected_location = combination[3]
                    sourcelat = detected_location['sourcelat']
                    sourcelon = detected_location['sourcelon']
                    gmap3 = map_hit(gmap3, float(sourcelat), float(sourcelon), "red", 4)
                    sourcelat_list.append(sourcelat)
                    sourcelon_list.append(sourcelon)
                except Exception as e:
                    # ... PRINT THE ERROR MESSAGE ... #
                    print(e)
                    pass
            
            while len(all_combinations_of_group_of_first_hits) > 1:
                avg_sourcelat = Average(sourcelat_list)
                avg_sourcelon = Average(sourcelon_list)
                sourcelat_list = []
                sourcelat_list = []
                cx = numpy.array([avg_sourcelon, avg_sourcelat])
                gmap3 = map_hit(gmap3, float(avg_sourcelat), float(avg_sourcelon), "cornflowerblue", 4)
                all_combinations_of_group_of_first_hits = sorted(all_combinations_of_group_of_first_hits, key=lambda x: x[3]['offby'])
                
                for combination in all_combinations_of_group_of_first_hits:
                    try:
                        k = gd.Geodesic() #defaults to WGS84
                        detected_location = combination[3]
                        sourcelat = detected_location['sourcelat']
                        sourcelon = detected_location['sourcelon']
                        cd = numpy.array([sourcelon, sourcelat])
                        offby = {'offby': abs(k.inverse(cx, cd).base[0,0])}
                        #print(offby)
                        detected_location.update(offby)
                        sourcelat_list.append(sourcelat)
                        sourcelon_list.append(sourcelon)
                    except Exception as e:
                        # ... PRINT THE ERROR MESSAGE ... #
                        #print(e)
                        pass
                all_combinations_of_group_of_first_hits.pop()
            print(all_combinations_of_group_of_first_hits)
            for combination in all_combinations_of_group_of_first_hits:
                try:
                    k = gd.Geodesic() #defaults to WGS84
                    ronex, rtwo, rthree, sourcelatx, sourcelonx, e_idx, offbyx= geo(combination)
                    pi1 = combination[0]
                    pi2 = combination[1]
                    pi3 = combination[2]
                    detected_location = combination[3]
                    sourcelat = detected_location['sourcelat']
                    sourcelon = detected_location['sourcelon']
                    cd = numpy.array([sourcelon, sourcelat])
                    cd1 = numpy.array([pi1['longitude'], pi1['latitude']]) 
    
                    rone = abs(k.inverse(cd1, cd).base[0,0])
                    gmap3 = map_hit(gmap3, float(sourcelat), float(sourcelon), "black", 5)
                    gmap3 = map_hit(gmap3, float(sourcelat), float(sourcelon), "white", rone)
                    gmap3 = map_hit(gmap3, pi1['latitude'], pi1['longitude'], "white", 4)
                    gmap3 = map_hit(gmap3, pi2['latitude'], pi2['longitude'], "white", rtwo)
                    gmap3 = map_hit(gmap3, pi3['latitude'], pi3['longitude'], "white", rthree)
                except Exception as e:
                    # ... PRINT THE ERROR MESSAGE ... #
                    #print(e)
                    pass
            try:
                try:
                    gmap3 = map_hit(gmap3, float(avg_sourcelat), float(avg_sourcelon), "green", 4)
                except:
                    pass
                map_name = "maps/"+str(e_id)+".html"
                print(map_name)
                gmap3.draw( map_name )
                sourcelat_list = []
                sourcelon_list = []
                gmap3 = gmplot.GoogleMapPlotter(29.9610375, -90.0634532, 16)
                gmap3 = gmap(gmap3)
            except Exception as e:
                        # ... PRINT THE ERROR MESSAGE ... #
                        print(e)
                        pass




            



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.jimihendrix.dev", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()