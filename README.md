# gsuite-login-geoip

## About
A recent engagement required me to analyze geographic login activity for a GSuite domain. While Google makes several reports available on the Admin dashboard, there was not one that provided thorough geographic detail. I made a thing that would take the default Login Activity Report, enhance it to include GeoIP data and plot all of the data points on an interactive map.

## Prerequisites
- See `requirements.txt` for Python modules
- Download and unpack `GeoLiteCity.dat` from http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz

## Usage
1. Export a Login Activity report from https://admin.google.com/AdminHome?fral=1#Reports:subtab=login-audit
    1. ![](https://i.imgur.com/PAnYpwf.png)

2. `python geoip.py /path/to/AuditReport.csv /path/to/GeoLiteCity.dat`

3. Profit.
