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