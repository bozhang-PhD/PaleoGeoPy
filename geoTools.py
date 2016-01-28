"""
    Copyright (C) 2016  Michael G. Tetley
    EarthByte Group, University of Sydney
    Geological and Planetary Sciences, California Institute of Technology
    Contact email: michael.tetley@sydney.edu.au // mtetley@caltech.edu

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


    ## Geoscience Toolbox ##

    Set of tools to calculate useful things for geoscience and palaeomagnetics research
"""

# Import required libraries
import numpy as np
import pygplates as pgp


""" GEOSCIENCE """
"""
    haversine

    Module to calculate the great circle distance between two points on a sphere.
    Returns distances in kilometers.
"""
def haversine(lon1, lat1, lon2, lat2):

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))

    # Radius of the Earth
    km = 6371 * c

    return km


"""
    global_points_rand

    Module to generate a random distribution of lat / lon points on the Earth
    Returns length = samples list of latitudes and longitudes
"""
def global_points_rand(samples):

    lats = []
    lons = []

    for i in xrange(0, samples):

        theta = 2 * np.pi * np.random.random()
        phi = np.arccos(2 * np.random.random() - 1.0)
        
        x = np.cos(theta) * np.sin(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(phi)
        
        point = pgp.convert_point_on_sphere_to_lat_lon_point((x,y,z))
        lats.append(point.get_latitude())
        lons.append(point.get_longitude())

    return lats, lons


"""
    global_points_uniform

    Module to generate a uniform (even) distribution of lat / lon points on the Earth
    Returns length = samples list of latitudes and longitudes
"""
def global_points_uniform(samples):

    lats = []
    lons = []

    angle = np.pi * (3 - np.sqrt(5))
    theta = angle * np.arange(samples)
    z = np.linspace(1 - 1.0 / samples, 1.0 / samples - 1, samples)
    radius = np.sqrt(1 - z * z)
     
    points = np.zeros((samples, 3))
    points[:,0] = radius * np.cos(theta)
    points[:,1] = radius * np.sin(theta)
    points[:,2] = z

    for i in xrange(0, len(points)):
        
        point = pgp.convert_point_on_sphere_to_lat_lon_point((points[i][0], points[i][1], points[i][2]))
        lats.append(point.get_latitude())
        lons.append(point.get_longitude())

    return lats, lons



""" PALAEOMAGNETICS """
"""
    calcKfromA95

    Calculate koenigsberger ratio (k) from alpha 95 confidence limit (A95) and number of samples (n).
    Returns k 
"""
def calcKfromA95(alpha95, n):

    alpha95 = np.radians(alpha95)
    fac = 20.**(1. / (n - 1))
    r2 = 1. / (fac - np.cos(alpha95))
    r2 = r2 * n * (fac - 1.)
    k = (n - 1.) / (n - r2)

    return k