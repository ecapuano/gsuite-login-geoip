import pygeoip
import pandas as pd
import re
import numpy
import argparse
import plotly
import time
import progressbar
import random

def main():
    # count records
    with open(infile) as f:
        rec_count = sum(1 for _ in f) - 1
    print("Processing %i log entries... Please wait." % rec_count)

    # regex for ipv4 identification
    ipv4 = re.compile("([1-9][0-9]{0,2}\.[0-9]{0,3}\.[0-9]{0,3}\.[0-9]{0,3})")

    df = pd.read_csv(
            infile,
            encoding='utf-8',
            header=0,
            usecols=["Event Description", "IP Address", "Date"],
            parse_dates=["Date"]
            )

    attributes = [
        'latitude',
        'longitude',
        'city',
        'region_code',
        'metro_code',
        'country_code3',
        'country_name',
        'postal_code',
        'dma_code',
        'area_code'
        ]

    i = 0
    totalrows = len(df.index)
    print(totalrows)
    bar = progressbar.ProgressBar(max_value=totalrows).start()
    for idx,row in df.iterrows():
        i += 1
        bar.update(i)
        ipAddress = row["IP Address"]
        if ipv4.match(ipAddress):
            geodata = geoip_city(ipAddress)

            for attribute in attributes:
                if geodata[attribute]:
                    try:
                        if numpy.isnan(geodata[attribute]):
                            df.ix[idx, attribute] = "None"
                        else:
                            df.ix[idx, attribute] = geodata[attribute]
                    except:
                        pass
                    df.ix[idx, attribute] = geodata[attribute]
                else:
                    df.ix[idx, attribute] = "None"

            long_desc = str(row["Date"]) + ' - ' + \
                        row["Event Description"] + ' from ' + \
                        df.ix[idx, "city"] + ', ' + \
                        str(df.ix[idx, "region_code"]) + ', ' + \
                        df.ix[idx, "country_name"]

            df.ix[idx, "long_desc"] = long_desc

            for coord in ['latitude','longitude']:
                df.ix[idx, coord] = scatterlatlong(df.ix[idx, coord])


    bar.finish()
    buildmap(df)

def scatterlatlong(coord):
    # neccesary to prevent overlapping coords
    coordmax = coord + 0.05
    coordmin = coord - 0.05
    return random.uniform(coordmin,coordmax)

def geoip_city(ipAddress):
    gic = pygeoip.GeoIP(GeoLiteCity)
    return gic.record_by_addr(ipAddress)

def getColor(eventType,returnType):

    levels = {
        'warning': {
            'color': "Red",
            'opacity': 1,
            'size': 8,
            'triggers': ["failed"]
            },
        'caution': {
            'color': "Orange",
            'opacity': 0.8,
            'size': 7,
            'triggers': ["challenge"]
            },
        'common': {
            'color': "Blue",
            'opacity': 0.6,
            'size': 6,
            'triggers': ["logged in", "logged out"]
            },
        }

    for level in levels:
        for trigger in levels[level]['triggers']:
            if trigger in eventType:
                for availableType in ['color','opacity','size']:
                    if returnType == availableType:
                        return levels[level][availableType]
            else:
                pass # worst error handler ever

    return "Black" # worst error handler ever

def buildmap(df):
    for idx,row in df.iterrows():
        eventType = row["Event Description"]
        if eventType:
            for markerattr in ['color','opacity','size']:
                df.ix[idx, markerattr] = getColor(eventType,markerattr)
        else: # shouldn't happen
            df.ix[idx, "color"] = "Pink"
            df.ix[idx, "opacity"] = 0.5
            df.ix[idx, "size"] = 6

    data = [ dict(
            type = 'scattergeo',
            lon = df['longitude'],
            lat = df['latitude'],
            text = df['long_desc'],
            mode = 'markers',
            marker = dict(
                size = df['size'],
                opacity = df['opacity'],
                reversescale = True,
                autocolorscale = False,
                symbol = 'circle',
                line = dict(
                    width=1,
                    color='rgba(102, 102, 102)'
                    ),
                color = df['color'],
                )
            )
        ]

    layout = dict(
            title = maptitle,
            colorbar = False,
            geo = dict(
                scope='world',
                projection=dict( type='equirectangular' ),
                showland = True,
                showcountries = True,
                showsubunits = True,
                showcoastlines = True,
                landcolor = "rgb(250, 250, 250)",
                subunitcolor = "rgb(217, 217, 217)",
                countrycolor = "rgb(217, 217, 217)",
                coastlinecolor = "rgb(220, 220, 220)",
                countrywidth = 0.5,
                subunitwidth = 0.5,
                showframe = False
            ),
        )

    fig = dict( data=data, layout=layout )
    plotly.offline.plot( fig, validate=False, filename='map.html' )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", help="The CSV export from GSuite Login \
                                            Activity Report")
    parser.add_argument("geocitydb", help="Path to the GeoLiteCity.dat \
                                            database")
    parser.add_argument("--maptitle", help="Title to be displayed on the map")
    args = parser.parse_args()
    infile = args.inputfile
    GeoLiteCity = args.geocitydb
    if args.maptitle:
        maptitle = args.maptitle
    else:
        maptitle = "GSuite Login Activity"
    main()
