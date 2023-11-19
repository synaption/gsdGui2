# import gmplot package
import gmplot


def map_hit(gmap3, sourcelat, sourcelon, color, size):
    gmap3.scatter( [sourcelat], [sourcelon], color,
                                  size = size, marker = False )
    return gmap3




def gmap(gmap3):
    latitude_list  = [ 41.784788, 41.784924, 41.784575 ]
    longitude_list = [ -88.211129, -88.210949, -88.210931 ]
    pi_numbers     = ['pi1', 'pi2', 'pi3' ]
      
      
    # scatter method of map object 
    # scatter points on the google map
    gmap3.scatter( latitude_list, longitude_list, 'blue',
                                  size = 4, marker = True, title=pi_numbers )

    gmap3.scatter( [41.784695], [-88.210954], 'yellow',
                                  size = 4, marker = False )
      
    # Plot method Draw a line in
    # between given coordinates
    #gmap3.plot(latitude_list, longitude_list, 
    #           'cornflowerblue', edge_width = 2.5)
      
    return gmap3





if __name__ == "__main__":
    gmap3 = gmplot.GoogleMapPlotter(41.784695,-88.210954, 16)
    gmap(gmap3)