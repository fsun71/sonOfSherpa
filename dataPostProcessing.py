import numpy as np 
import os
import xml.etree.ElementTree as ET
import pandas as pd

gpxFileNames = []

for fileName in os.listdir('data/gpx'):
    if fileName.endswith(".gpx"):
    	gpxFileNames.append(fileName)

def greatCircleCalc(lat1, lon1, lat2, lon2, imperialUnits = False):
	earthR = 6371e3
	phi_1 = lat1 * np.pi/180
	phi_2 = lat2 * np.pi/180
	delPhi = phi_2 - phi_1
	delLambda = (lon2 -lon1) * np.pi/180

	a = np.sin(delPhi/2)**2 + (np.cos(phi_1)*np.cos(phi_2)) * np.sin(delLambda/2)**2
	c = 2*np.arctan2(np.sqrt(a), np.sqrt(1-a))
	distance = earthR * c

	if imperialUnits == True:
		distance = distance * 0.000621371

	return np.round(distance, 2)

def parseGPX(fileName, imperialUnits = False):
	gpxDF = pd.DataFrame(columns = ['Elevation', 'Distance', 'Delta Elevation',  'Delta Distance'])
	tree = ET.parse('data/gpx/' + fileName)

	lattitudes = []
	longitudes = []
	elevations = []
	distances = [0]
	deltaElevation = [0]
	deltaDistance = [0]

	root = tree.findall('./')[-1]
	wayPtLen = len(tree.findall('./')[-1])

	for wayPt in range(2, wayPtLen):
		lattitudes.append(float(root[wayPt].attrib['lat']))
		longitudes.append(float(root[wayPt].attrib['lon']))

		if imperialUnits == True:
			elevations.append(float(root[wayPt][0].text) * 3.28084)
		else:
			elevations.append(float(root[wayPt][0].text))

	for i in range(1, len(lattitudes)):
		distance = greatCircleCalc(lattitudes[i-1], longitudes[i-1], lattitudes[i], longitudes[i], imperialUnits)
		cdistance = distance + np.sum(distances[i-1])

		distances.append(cdistance)
		deltaDistance.append(distance)
		deltaElevation.append(elevations[i] - elevations[i-1])


	gpxDF['Delta Elevation'] = deltaElevation
	gpxDF['Delta Distance'] = deltaDistance
	gpxDF['Elevation'] = elevations
	gpxDF['Distance'] = distances

	gpxDF.to_csv('data/routeCSV/' + fileName[:-4] + '.csv', index = False)

for fileName in gpxFileNames:
	parseGPX(fileName, True)
	




