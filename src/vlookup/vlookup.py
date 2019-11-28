# Import libraries
import pandas as pd
import csv
import os

# directories and paths
currentdirectory = os.path.dirname(os.path.abspath(__file__))
dataDirectory = '/data'
resultDirectory = '/data/result'
dataPath = currentdirectory + dataDirectory
resultPath = currentdirectory + resultDirectory

if not os.path.exists(dataPath):
    os.makedirs(dataPath)
if not os.path.exists(resultPath):
    os.makedirs(resultPath)

# Import CSV in text form
haystack = pd.read_csv(dataPath + '/haystack.csv', sep=',', converters={'needle': str, 'value':str})
needles = pd.read_csv(dataPath + '/needles.csv', sep=',', converters={'needle': str})

# Drop non-usable needles
# needles = needles.drop(needles[needles['needle'] == None].index)
# haystack = haystack.drop(haystack[haystack['needle'] == None].index)
haystack = haystack.dropna(subset=['needle'])
needles = needles.dropna(subset=['needle'])

# Create mapping dictionary
haystackDict = haystack.set_index('needle')['value'].to_dict()

# Match needle
def matchNeedle(needle):
    try:
        x = haystackDict[needle]
    except:
        x = None
    return x

# Manipulate result dataset to include the found value
needles['valueFound'] = needles['needle'].apply(matchNeedle)
needles = needles.dropna(subset=['valueFound']).drop(needles[needles['valueFound'] == None].index)

# export result files
needles.tail(100).to_csv(resultPath + '/needles-100.csv', index = False, sep=",", quoting=csv.QUOTE_ALL)
needles.to_csv(resultPath + '/needles-all.csv', index = False, sep=",", quoting=csv.QUOTE_ALL)