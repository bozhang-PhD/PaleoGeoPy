# Copyright (C) 2014  Michael Tetley
# EarthByte Group, University of Sydney
# Contact email: michael.tetley@sydney.edu.au
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.



#### GPML Tools ####

# Description:  Sequentially filters all features within GPML data files by user defined search parameters.

# Usage:        Currently can only be used from within python. Either add it to your PYTHONPATH or copy
#               GPMLTools.py to working folder.

#               import GPMLTools
#               GPMLTools.filterGPML(args)


# Basic Arguments (args):

#       Name:   Input file name
#       Desc:   Filename for GPML data input file (the file to be filtered)
#       var:    inputFile
#       Type:   string
#       Usage:  inputFile="myInputFile.gpml" - can be relative path to GPMLTools.py

#       Name:   Output file name
#       Desc:   Filename to be saved containing filtered data. Only use if GPML file is required. All files are by
#               default saved to an "output" folder generated in the same folder as GPMLTools.py
#       var:    outputFile
#       Type:   string
#       Usage:  outputFile="myOutputFile.gpml"

#       Name:   Filter sequence
#       Desc:   Describes the sequential order of the specified filters to process data. Each subsequent filter added
#               to this list treats the output from the immediately previous filter as its input data. Filters can be
#               added to filterSequence in any order and more than once. Each filter (listed below) can be called by
#               its filter number (e.g. [1] is Reconstruction plate ID, and [2] is Conjugate plate ID).
#       var:    filterSequence
#       Type:   list of integers (length = inf)
#       Usage:  filterSequence=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].


# Filter types (numbered) and usage:

# 1.    Name:   Reconstruction plate ID
#       var:    rPlateID
#       Type:   list of integers (length = inf)
#       Usage:  Single parameter:   rPlateID=[801]
#               Multi parameter:    rPlateID=[801,701,101]

# 2.    Name:   Conjugate plate ID
#       var:    cPlateID
#       Type:   list of integers (length = inf)
#       Usage:  Single parameter:   cPlateID=[801]
#               Multi parameter:    cPlateID=[801,701,101]

# 3.    Name:   Age of appearance window
#       Desc:   Finds features the appear within (and including) a specified time period or 'window'.
#               Age windows are defined [oldest, youngest]. Values can be integers or floats.
#       var:    ageAppearWindow
#       Type:   list of integers or floats (length = 2)
#       Usage:  ageAppearWindow=[oldest, youngest]

# 4.    Name:   Age of disappearance window
#       Desc:   Finds features that disappear within (and including) a specified time period or 'window'.
#               Age windows are defined [oldest, youngest]. Values can be integers or floats.
#       var:    ageDisappearWindow
#       Type:   list of integers or floats (length = 2)
#       Usage:  ageDisappearWindow=[oldest, youngest]

# 5.    Name:   Age of existence window
#       Desc:   Finds features that exists within (and including) a specified time period or 'window'.
#               Age windows are defined [oldest, youngest]. Values can be integers or floats.
#       var:    ageExistsWindow
#       Type:   list of integers or floats (length = 2)
#       Usage:  ageExistsWindow=[oldest, youngest]

# 6.    Name:   Geographic bounding box
#       Desc:   Finds all features that are located all or in part within the specified geographic bounding box.
#               Bounding boxes are defined [Longitude 1, Longitude 2, Latitude 1, Latitude 2]. Longitude 1 is the
#               easternmost limit (max 0), Longitude 2 is the westernmost limit (max 360), Latitude 1 is the
#               southernmost limit (max -90), and Latitude 2 is the northernmost limit (max 90)of geographic region.
#               Values are in degrees.
#       var:    boundingBox
#       Type:   list of integers or floats (length = 4)
#       Usage:  boundingBox=[0, 360, -90, 90]

# 7.    Name:   Feature type
#       Desc:   Finds all features of specified feature type. Currently supported feature types:
#                   "ISO" (Isochron)
#                   "MOR" (Mid-ocean ridge)
#                   "PCB" (PassiveContinentalBoundary)
#                   - others will be added in over time or upon request!
#               A wildcard search can be performed using "ALL", which returns all of the above feature types.
#       var:    featureType
#       Type:   list of strings (length = inf)
#       Usage:  Single parameter:   featureType=["ISO"]
#               Multi parameter:    featureType=["ISO", "MOR", "PCB"]

# 8.    Name:   Geometry type
#       Desc:   Finds all features of a specified geometry type. Currently supported geometry types:
#                   "PointOnSphere"
#                   "MultiPointOnSphere"
#                   "PolyLineOnSphere"
#                   "PolygonOnSphere"
#               A wildcard search can be performed using "ALL", which returns all of the above geometry types.
#       var:    geometryType
#       Type:   list of strings (length = inf)
#       Usage:  Single parameter:   geometryType=["PointOnSphere"]
#               Multi parameter:    geometryType=["PointOnSphere", "MultiPointOnSphere", "PolyLineOnSphere"]

# 9.    Name:   Feature ID
#       Desc:   Finds all features with specified feature ID. ID's are case insensitive.
#       var:    featureID
#       Type:   string
#       Usage:  featureID="GPlates-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

# 10.   Name:   Feature name
#       Desc:   Finds all features containing some or all of specified feature name string. Names are case insensitive.
#       var:    featureName
#       Type:   list of strings (length = inf)
#       Usage:  Single parameter:   featureName=["name1"]
#               Multi parameter:    featureName=["name1", "name2", "name3"]


##### Examples filter queries #####

#   Example 1:  Filter for features with reconstruction plate IDs [801, 701] that appear between 60 - 50 Ma within the bounding box
#               long 100 - long 130 and lat -90 and lat 20.

#               GPMLTools.filterGPML(inputFile=inputFile, filterSequence=[1, 3, 5], rPlateID=[801], ageAppearWindow=[60, 50], boundingBox=[100, 130, -90, 20])


#   Example 2:  Filter for features that existed between 100 - 90 Ma that have feature names containing either "pacific", "cocos", or "australia".

#               GPMLTools.filterGPML(inputFile=inputFile, outputFile=outputFile, filterSequence=[6, 10], ageExistsWindow=[100, 90], featureName=["pacific", "cocos", "australia"])


#   Example 3:  Filter for features of all feature types with a feature geometry of "PolylineOnSphere" and with a conjugate plate ID of 101.

#               GPMLTools.filterGPML(inputFile=inputFile, outputFile=outputFile, filterSequence=[7, 8, 2], featureType=["ALL"], geometryType=["PolylineOnSphere"], cPlateID=[101])




import pygplates as pgp
import datetime
import time
import os


# Filter GPML by selected criteria and output new GPML file of filtered data
def filterGPML(**kwargs):

    # Start the clock
    start = time.time()

    filterProperties = ["inputFile", "outputFile", "filterSequence", "rPlateID", "cPlateID", "ageAppearWindow", "ageDisappearWindow",
                        "ageExistsWindow", "boundingBox", "featureType", "geometryType", "featureID", "featureName"]

    # Process supplied arguments and assign values to variables
    for parameter, value in kwargs.items():

        if parameter in filterProperties:
            if parameter == filterProperties[0]:
                inputFile = value
            elif parameter == filterProperties[1]:
                outputFile = value
            elif parameter == filterProperties[2]:
                filterSequence = value
            elif parameter == filterProperties[3]:
                rPlateID = value
            elif parameter == filterProperties[4]:
                cPlateID = value
            elif parameter == filterProperties[5]:
                ageAppearWindow = value
            elif parameter == filterProperties[6]:
                ageDisappearWindow = value
            elif parameter == filterProperties[7]:
                ageExistsWindow = value

                if ageExistsWindow[1] > ageExistsWindow[0]:
                    print " "
                    print "ERROR - Age exists window end age older than begin age: " + str(ageExistsWindow[1])
                    exit(0)

            elif parameter == filterProperties[8]:
                boundingBox = value

                if pgp.LatLonPoint.is_valid_longitude(boundingBox[0]) is False:
                    print " "
                    print "ERROR - Bounding box longitude is not valid: " + str(boundingBox[0])
                    exit(0)
                if pgp.LatLonPoint.is_valid_longitude(boundingBox[1]) is False:
                    print " "
                    print "ERROR - Bounding box longitude is not valid: " + str(boundingBox[1])
                    exit(0)
                if pgp.LatLonPoint.is_valid_latitude(boundingBox[2]) is False:
                    print " "
                    print "ERROR - Bounding box latitude is not valid: " + str(boundingBox[2])
                    exit(0)
                if pgp.LatLonPoint.is_valid_latitude(boundingBox[3]) is False:
                    print " "
                    print "ERROR - Bounding box latitude is not valid: " + str(boundingBox[3])
                    exit(0)

            elif parameter == filterProperties[9]:
                featureTemp = value
                featureType = []

                if "ALL" in featureTemp:
                    featureType = ["Isochron", "MidOceanRidge", "PassiveContinentalBoundary"]
                if "ISO" in featureTemp:
                    featureType.append("Isochron")
                if "MOR" in featureTemp:
                    featureType.append("MidOceanRidge")
                if "PCB" in featureTemp:
                    featureType.append("PassiveContinentalBoundary")

            elif parameter == filterProperties[10]:
                geometryType = value

                if "ALL" in geometryType:
                    geometryType = ["PolylineOnSphere", "PolygonOnSphere", "PointOnSphere", "MultiPointOnSphere"]

            elif parameter == filterProperties[11]:
                featureID = value
            elif parameter == filterProperties[12]:
                featureName = value


        else:
            print " "
            print "ERROR - Filter criteria not found: " + str(parameter)
            print " "
            exit(0)


    date = datetime.date.today()

    #if inputFile != "none":
        #output = pgp.FeatureCollection()

    featureCollection = pgp.FeatureCollectionFileFormatRegistry()

    print " "
    print "--------------------------------------------"
    print " ### GPMLTools - filterGPML ###"

    # Check for existing output directory and create it if not found
    if not os.path.exists("output"):
        os.makedirs("output")
        print " "
        print "Housekeeping:"
        print "    No output folder found. Folder 'output' created."

    # Check for existing output file with same name and remove if found
    if os.path.isfile("output/output.gpml"):
        os.remove("output/output.gpml")
        print " "
        print "Housekeeping:"
        print "    Previous 'output.gpml' found in destination folder. File removed for new filter sequence."


    try:
        feature = featureCollection.read(inputFile)
        print " "
        print "Data handling:"
        print "    Successfully loaded data file:  '" + str(inputFile) + "'"
        print "       - File contains " + str(len(feature)) + " features."

    except pgp.OpenFileForReadingError:
        print " "
        print("    ERROR - File read error in: '" + inputFile + "'. Is this a valid GPlates file?")
        exit(0)
    except pgp.FileFormatNotSupportedError:
        print " "
        print("    ERROR - File format not supported: '" + inputFile + "'. Please check the file name and try again")
        exit(0)



    #Filter data

    print " "
    print "Filter sequence:"

    previousFilter = 0

    f1_result = pgp.FeatureCollection()
    f2_result = pgp.FeatureCollection()
    f3_result = pgp.FeatureCollection()
    f4_result = pgp.FeatureCollection()
    f5_result = pgp.FeatureCollection()
    f6_result = pgp.FeatureCollection()
    f7_result = pgp.FeatureCollection()
    f8_result = pgp.FeatureCollection()
    f9_result = pgp.FeatureCollection()
    f10_result = pgp.FeatureCollection()


    for filter_ in filterSequence:

        if previousFilter == 0:
            data_ = feature
        elif previousFilter == 1:
            data_ = f1_result
        elif previousFilter == 2:
            data_ = f2_result
        elif previousFilter == 3:
            data_ = f3_result
        elif previousFilter == 4:
            data_ = f4_result
        elif previousFilter == 5:
            data_ = f5_result
        elif previousFilter == 6:
            data_ = f6_result
        elif previousFilter == 7:
            data_ = f7_result
        elif previousFilter == 8:
            data_ = f8_result
        elif previousFilter == 9:
            data_ = f9_result
        elif previousFilter == 10:
            data_ = f10_result



        # Filter by reconstruction plate ID
        if filter_ == 1:

            for feature in data_:
                for property in feature:

                    filter_property = property.get_name()

                    if filter_property.get_name() == "reconstructionPlateId":
                        selected_filter_property = property.get_value()

                        # Isolate criteria match and process
                        for plateID in rPlateID:
                            if str(selected_filter_property) == str(plateID):

                                # Append filtered data to associated Feature Collection
                                f1_result.add(feature)

            print "    1. Filtering data by reconstruction plate ID(s): " + str(rPlateID)
            print "       - Found " + str(len(f1_result)) + " feature(s)."
            print " "

            previousFilter = 1


        # Filter by conjugate plate ID
        if filter_ == 2:

            for feature in data_:
                for property in feature:

                    filter_property = property.get_name()

                    if filter_property.get_name() == "conjugatePlateId":
                        selected_filter_property = property.get_value()

                        # Isolate criteria match and process
                        for plateID in cPlateID:
                            if str(selected_filter_property) == str(plateID):

                                # Append filtered data to associated Feature Collection
                                f2_result.add(feature)

            print "    2. Filtering data by conjugate plate ID(s): " + str(cPlateID)
            print "       - Found " + str(len(f2_result)) + " feature(s)."
            print " "

            previousFilter = 2



        # Filter by age of appearance
        if filter_ == 3:

            if ageAppearWindow[0] == "DP":
                ageAppearWindow[0] = float("inf")

            for feature in data_:

                begin_time, end_time = feature.get_valid_time()

                if begin_time <= ageAppearWindow[0] and begin_time >= ageAppearWindow[1]:
                    f3_result.add(feature)

            print "    3. Filtering data by age of appearance window: " + str(ageAppearWindow[0]) + " - " + str(ageAppearWindow[1]) + " Ma"
            print "       - Found " + str(len(f3_result)) + " feature(s)."
            print " "

            previousFilter = 3



        # Filter by age of disappearance
        if filter_ == 4:

            if ageDisappearWindow[1] == "DF":
                    ageDisappearWindow[1] = float("-inf")

            for feature in data_:

                begin_time, end_time = feature.get_valid_time()

                if end_time <= ageDisappearWindow[0] and end_time >= ageDisappearWindow[1]:
                    f4_result.add(feature)

            print "    4. Filtering data by age of disappearance window: " + str(ageDisappearWindow[0]) + " - " + str(ageDisappearWindow[1]) + " Ma"
            print "       - Found " + str(len(f4_result)) + " feature(s)."
            print " "

            previousFilter = 4



        # Filter by geographic selection / polygon
        if filter_ == 5:

            for feature in data_:
                for property in feature:

                    filter_property = property.get_name()

                    if filter_property.get_name() == "centerLineOf":
                        selected_filter_property = property.get_value()

                        points = selected_filter_property.get_value().get_base_curve().get_polyline().get_points_view()

                        for point in points:
                            point_latlong = pgp.convert_point_on_sphere_to_lat_lon_point(point)

                            if point_latlong.get_longitude() >= float(boundingBox[0]) and point_latlong.get_longitude() <= float(boundingBox[1])\
                                    and point_latlong.get_latitude() >= float(boundingBox[2]) and point_latlong.get_latitude() <= float(boundingBox[3]):

                                # If point is found within bounding box, add feature and break loop (search next feature)
                                f5_result.add(feature)
                                break

            print "    5. Filtering data by geographic bounding box: " + str(boundingBox[0]) + "/" + str(boundingBox[1]) + "/" + str(boundingBox[2]) + "/" + str(boundingBox[3])
            print "       - Found " + str(len(f5_result)) + " feature(s)."
            print " "

            previousFilter = 5



        # Filter by age exists window
        if filter_ == 6:

            for feature in data_:

                begin_time, end_time = feature.get_valid_time()

                if begin_time >= ageExistsWindow[0] and end_time <= ageExistsWindow[1]:
                    f6_result.add(feature)
                elif begin_time >= ageExistsWindow[0] and end_time <= ageExistsWindow[0] and end_time >= ageExistsWindow[1]:
                    f6_result.add(feature)
                elif begin_time <= ageExistsWindow[0] and end_time >= ageExistsWindow[1]:
                    f6_result.add(feature)
                elif begin_time <= ageExistsWindow[0] and end_time >= ageExistsWindow[1] and end_time <= ageExistsWindow[1]:
                    f6_result.add(feature)

            print "    6. Filtering data by age of existence window: " + str(ageExistsWindow[0]) + " - " + str(ageExistsWindow[1]) + " Ma"
            print "       - Found " + str(len(f6_result)) + " feature(s)."
            print " "

            previousFilter = 6



        # Filter by feature type
        if filter_ == 7:

            iso_count = 0
            mor_count = 0
            pcb_count = 0

            for feature in data_:

                if "Isochron" in featureType:
                    if str(feature.get_feature_type()) == "gpml:Isochron":
                        f7_result.add(feature)
                        iso_count += 1
                if "MidOceanRidge" in featureType:
                    if str(feature.get_feature_type()) == "gpml:MidOceanRidge":
                        f7_result.add(feature)
                        mor_count += 1
                if "PassiveContinentalBoundary" in featureType:
                    if str(feature.get_feature_type()) == "gpml:PassiveContinentalBoundary":
                        f7_result.add(feature)
                        pcb_count += 1


            print "    7. Filtering data by feature type(s): " + str(featureType)

            if "Isochron" in featureType:
                print "       - Found " + str(iso_count) + " Isochron(s)."
            if "MidOceanRidge" in featureType:
                print "       - Found " + str(mor_count) + " MidOceanRidge(s)."
            if "PassiveContinentalBoundary" in featureType:
                print "       - Found " + str(pcb_count) + " PassiveContinentalBoundary(s)."

            print " "

            previousFilter = 7



        # Filter by geometry type
        if filter_ == 8:

            polylineCount = 0
            polygonCount = 0
            pointCount = 0
            multiPointCount = 0

            for feature in data_:

                geometries = feature.get_geometry()

                for geometry in geometryType:

                    if str(geometry) in str(geometries):
                        f8_result.add(feature)

                        if str(geometry) == "PolylineOnSphere":
                            polylineCount += 1
                        if str(geometry) == "PolygonOnSphere":
                            polygonCount += 1
                        if str(geometry) == "PointOnSphere":
                            pointCount += 1
                        if str(geometry) == "MultiPointOnSphere":
                            multiPointCount += 1

            print "    8. Filtering data by feature geometries present: " + str(geometryType)

            if "PolylineOnSphere" in geometryType:
                print "       - Found " + str(polylineCount) + " PolylineOnSphere(s)."
            if "PolygonOnSphere" in geometryType:
                print "       - Found " + str(polygonCount) + " PolygonOnSphere(s)."
            if "PointOnSphere" in geometryType:
                print "       - Found " + str(pointCount) + " PointOnSphere(s)."
            if "MultiPointOnSphere" in geometryType:
                print "       - Found " + str(multiPointCount) + " MultiPointOnSphere(s)."

            print " "

            previousFilter = 8



        # Filter by feature ID
        if filter_ == 9:

            for feature in data_:

                for id in featureID:
                    if str(feature.get_feature_id()).lower() == str(id).lower():
                        f9_result.add(feature)

            print "    9. Filtering data by feature ID: " + str(featureID)
            print "       - Found " + str(len(f9_result)) + " feature(s)."
            print " "

            previousFilter = 9



        # Filter by feature name (case insensitive)
        if filter_ == 10:

            for feature in data_:

                feature_name = feature.get_name()

                for names in featureName:

                    if names.lower() in feature_name.lower():
                        f10_result.add(feature)

            print "    10. Filtering data by feature name: " + str(featureName)
            print "       - Found " + str(len(f10_result)) + " feature(s)."
            print " "

            previousFilter = 10




    # output new feature collection from filtered data to file
    iso_output = eval("f" + str(previousFilter) + "_result")

    if len(iso_output) != 0:

        outputFeatureCollection = pgp.FeatureCollectionFileFormatRegistry()
        outputFeatureCollection.write(iso_output, "output/" + str(outputFile))

        print "Output file:"
        print "    ../output/" + str(outputFile)
        print " "
        print "Process took " + str(round(time.time() - start, 2)) + " seconds."
        print "--------------------------------------------"