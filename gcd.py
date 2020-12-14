### GREAT CIRCLE DISTANCE

import math

#Define functions
### Great Circle Distance #1: Spherical Law of Cosines
def gc1_sloc(coordinate_1,coordinate_2,radius):
    lon1,lat1 = coordinate_1
    lon2,lat2 = coordinate_2
    lonrat1 = lon1/(180/math.pi)
    lonrat2 = lon2/(180/math.pi)
    latrat1 = lat1/(180/math.pi)
    latrat2 = lat2/(180/math.pi)
    difflonrat = lonrat1-lonrat2
    difflatrat = latrat1-latrat2
    inner_cent_ang = math.sin(latrat1)*math.sin(latrat2) + math.cos(latrat1)*math.cos(latrat2)*math.cos(difflonrat)
    cent_ang = math.acos(inner_cent_ang)
    dist_sloc = radius*cent_ang
    return round(dist_sloc,2)

### Great Circle Distance #2: Haversine Formula
def gc2_hf(coord1,coord2,radius):
    lon1,lat1 = coord1
    lon2,lat2 = coord2
    lonrat1 = lon1/(180/math.pi)
    lonrat2 = lon2/(180/math.pi)
    latrat1 = lat1/(180/math.pi)
    latrat2 = lat2/(180/math.pi)
    difflonrat = lonrat1-lonrat2
    difflatrat = latrat1-latrat2
    inner_cent_ang = math.sqrt((math.sin(difflatrat/2)**2)+math.cos(latrat1)*math.cos(latrat2)*(math.sin(difflonrat/2)**2))
    cent_ang = 2*math.asin(inner_cent_ang)
    dist_hav = radius*cent_ang
    return round(dist_hav,2)
