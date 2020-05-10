import numpy as np 
import os
import pandas as pd
import matplotlib.pyplot as plt

csvFileNames = []

for fileName in os.listdir('data/routeCSV'):
    if fileName.endswith(".csv"):
    	csvFileNames.append(fileName)

fittedCurves = []

for route in csvFileNames:
	routeData = pd.read_csv('data/routeCSV/' + route)
	distance = routeData['Distance']
	elevation = routeData['Elevation']
	elevation = (elevation - elevation.min())/(elevation.max() - elevation.min())
	distance = distance/(distance.iloc[-1])

	elevProfileFit = np.polyfit(distance, elevation, 11)
	fittedCurves.append(np.poly1d(elevProfileFit))

routeDifferences = []

for index1, curve1 in enumerate(fittedCurves):
	for index2, curve2 in enumerate(fittedCurves[index1:]):
		if curve1 != curve2:
			cDifferenceFunc = np.poly1d.integ(curve2 - curve1)
			cDifference = np.round(cDifferenceFunc(1) - cDifferenceFunc(0), 6)

			routeDifferences.append([csvFileNames[index1][:-4], csvFileNames[index2][:-4], cDifference])

routeDifferences = np.transpose(routeDifferences)

routeSimDF = pd.DataFrame(columns = ['Route 1', 'Route 2', 'Difference Raw', 'Difference Score'])
routeSimDF['Route 1'] = routeDifferences[0]
routeSimDF['Route 2'] = routeDifferences[1]
routeSimDF['Difference Raw'] = [float(rawDiff) for rawDiff in routeDifferences[2]]
routeSimDF['Difference Score'] = [abs(float(rawDiff)) for rawDiff in routeDifferences[2]]

routeSimDF = routeSimDF.sort_values(by = ['Difference Score']).drop_duplicates(subset = 'Difference Score')

routeSimDF.to_csv('data/scoredDifferences.csv', index = False)