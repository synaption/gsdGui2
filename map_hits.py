# import gmplot package
import gmplot


def map_hit(gmap3, sourcelat, sourcelon, color, size):
    gmap3.scatter( [sourcelat], [sourcelon], color,
                                  size = size, marker = False )
    return gmap3




def gmap(gmap3):
    latitude_list  = [ 29.9615253, 29.9628034, 29.959351, 29.9576154, 29.9591371, 29.9622686, 29.9639093 ]
    longitude_list = [ -90.0640593, -90.0632169, -90.0610071, -90.0651099, -90.0682524, -90.0595782, -90.0673286 ]
    pi_numbers     = ['pi1', 'pi2', 'pi3', 'pi4', 'pi5', 'pi6', 'pi7' ]
      
      
    # scatter method of map object 
    # scatter points on the google map
    gmap3.scatter( latitude_list, longitude_list, 'blue',
                                  size = 4, marker = True, title=pi_numbers )

    gmap3.scatter( [29.9610375], [-90.0634532], 'yellow',
                                  size = 4, marker = False )
      
    # Plot method Draw a line in
    # between given coordinates
    #gmap3.plot(latitude_list, longitude_list, 
    #           'cornflowerblue', edge_width = 2.5)
      
    return gmap3





if __name__ == "__main__":
    gmap3 = gmplot.GoogleMapPlotter(29.9610375, -90.0634532, 16)
    gmap(gmap3)