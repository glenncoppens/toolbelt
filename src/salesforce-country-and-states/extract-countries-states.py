import copy, pprint, csv, json
from bs4 import BeautifulSoup

# config pretty print
pp = pprint.PrettyPrinter(indent=4)

# read Address settings metadata from Salesforce
bsoup = BeautifulSoup(open("data/Address.settings","r"), features='lxml')

# get all the countries in the xml file
countries = bsoup.find_all('countries')

# method to format the xml country to a `dict`
def formatCountry(bsXml):
    return {
        'active' : bool(bsXml.active.text) if bsXml.active != None else None,
        'integrationValue' : bsXml.integrationvalue.text if bsXml.integrationvalue != None else None,
        'isoCode' : bsXml.isocode.text if bsXml.isocode != None else None,
        'label' : bsXml.label.text if bsXml.label != None else None,
        'orgDefault' : bool(bsXml.orgdefault.text) if bsXml.orgdefault != None else None,
        'standard' : bool(bsXml.standard.text) if bsXml.standard != None else None,
        'visible' : bool(bsXml.visible.text) if bsXml.visible != None else None
    }

# method to format the xml state to a `dict`
def formatState(bsXmlState, bsXmlCountry):
    return {
        'active' : bool(bsXmlState.active.text) if bsXmlState.active != None else None,
        'integrationValue' : bsXmlState.integrationvalue.text if bsXmlState.integrationvalue != None else None,
        'isoCode' : bsXmlState.isocode.text if bsXmlState.isocode != None else None,
        'label' : bsXmlState.label.text if bsXmlState.label != None else None,
        'orgDefault' : bool(bsXmlState.orgdefault.text) if bsXmlState.orgdefault != None else None,
        'standard' : bool(bsXmlState.standard.text) if bsXmlState.standard != None else None,
        'visible' : bool(bsXmlState.visible.text) if bsXmlState.visible != None else None,
        'countryIsoCode' : bsXmlCountry.isocode.text if bsXmlCountry.isocode != None else None,
        'countryIntegrationValue' : bsXmlCountry.integrationvalue.text if bsXmlCountry.integrationvalue != None else None
    }


includeNonActiveCountries = True

countriesCsv = []
countriesCsv.append(['integrationValue', 'isoCode', 'label', 'active'])
for country in countries:
    countryJson = formatCountry(country)
    countryCsvLine = []
    countryCsvLine.append(countryJson['integrationValue'])
    countryCsvLine.append(countryJson['isoCode'])
    countryCsvLine.append(countryJson['label'])
    countryCsvLine.append(countryJson['active'])
    countriesCsv.append(countryCsvLine)

statesCsv = []
statesCsv.append(['integrationValue', 'isoCode', 'label', 'active', 'countryIsoCode', 'countryIntegrationCode', 'countryLabel', 'countryActive'])
for country in countries:
    countryJson = formatCountry(country)
    
    for state in country.find_all('states'):
        stateJson = formatState(state, country)
        stateCsvLine = []
        stateCsvLine.append(stateJson['integrationValue'])
        stateCsvLine.append(stateJson['isoCode'])
        stateCsvLine.append(stateJson['label'])
        stateCsvLine.append(stateJson['active'])
        stateCsvLine.append(countryJson['integrationValue'])
        stateCsvLine.append(countryJson['isoCode'])
        stateCsvLine.append(countryJson['label'])
        stateCsvLine.append(countryJson['active'])
        statesCsv.append(stateCsvLine)

# write csv for countries
with open('data/result/countries.csv', 'w') as csvfileCountries:
    filewriter = csv.writer(csvfileCountries, delimiter=',', quoting=csv.QUOTE_ALL)
    for csvLine in countriesCsv:
        filewriter.writerow(csvLine)

# write csv for countries
with open('data/result/states.csv', 'w') as csvfileStates:
    filewriter = csv.writer(csvfileStates, delimiter=',', quoting=csv.QUOTE_ALL)
    for csvLine in statesCsv:
        filewriter.writerow(csvLine)