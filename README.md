# gsuite-login-geoip

## About
A recent engagement required me to analyze geographic login activity for a GSuite domain. While Google makes several reports available on the Admin dashboard, there was not one that provided thorough geographic detail. I made a thing that would take the default Login Activity Report, enhance it to include GeoIP data and plot all of the data points on an interactive map.

Here's an [interactive sample map](https://htmlpreview.github.io/?https://raw.githubusercontent.com/ecapuano/gsuite-login-geoip/master/sample_map.html) containing fake data.
[![](https://i.imgur.com/4YmrAno.png)](https://htmlpreview.github.io/?https://raw.githubusercontent.com/ecapuano/gsuite-login-geoip/master/sample_map.html)

Marker color, opacity and size help emphasize noteworthy events. These values and their corresponding "keyword" triggers are defined in `geoip.py` https://github.com/ecapuano/gsuite-login-geoip/blob/master/geoip.py#L92-L111
![](https://i.imgur.com/PNWZLFM.png)

Geographic data can sometimes make quick work of detecting anomalous or malicious login activity. The image below is a real world example of this concept -- the overseas markers were connected to unauthorized access to a compromised account.
![](https://i.imgur.com/i6VT8L3.png)

## Prerequisites
- See `requirements.txt` for Python modules
- Download and unpack `GeoLiteCity.dat` from http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz

## Usage
1. Export a Login Activity report from https://admin.google.com/AdminHome?fral=1#Reports:subtab=login-audit
    1. ![](https://i.imgur.com/PAnYpwf.png)

2. `python geoip.py /path/to/AuditReport.csv /path/to/GeoLiteCity.dat`
