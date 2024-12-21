# Orora Technical Assignment

Topic: Rudimentary fire detection algorithm for the VIIRS sensor onboard Suomi-NPP satellite

## Assumptions

Based on my research, and the fact the VIIRS sensor data provided uses M-bands, I assume that we are using the 750-meter resolution data from the sensors.

## Assignment Analysis

### Input: Satellite Data - VIIRS images

We have 4 sample satellite overpasses. Each overpass consists of two NetCDF files, that can be explored using [Panoply](https://www.giss.nasa.gov/tools/panoply/)

1. File starting with *VNP02* contains observation data (radiance recorded by the sensor)
2. File starting with *VNP03* contains geolocation data (the geographical coordinates of each pixel in the observation data file)

Analysis for the input data can be found [here](./input-data.md).

### Function: Python service that detects thermal anomalies (hot pixels or hotspots)

Potential fire pixels (hotspots) are pixels where the “Earth view radiance” in the spectral region between 3.973 μm and 4.128 μm, which is recorded in the M13 band of the VIIRS sensor, is significantly higher than the nonfire background. 

You need to come up with a threshold to apply on the M13 band filter, in order to identify those hot pixels (and their geolocation).

Analysis about the fire / thermal anomalies detection can be found [here](./thermal-anomalies-detection.md)

### Output: GeoJSON of fire detections

GeoJSON response to the REST API call, that contains the geolocation (lat, long) of the hot pixels.

## In a few words

Create a Python REST service that let's a user upload a **netcd file** and gets a GeoJSON file of the fire detections.
