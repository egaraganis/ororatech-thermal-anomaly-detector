# Orora Technical Assignment

Topic: Rudimentary fire detection algorithm for the VIIRS sensor onboard Suomi-NPP satellite

## Theoretical Prerequisites

The **VIIRS** instrument observes and collects global satellite observations that span the visible and infrared wavelengths across land, ocean, and atmosphere.
VIIRS is one of five instruments onboard the **Suomi National Polar-orbiting Partnership (NPP)**. SNPP serves as a bridge between the Earth Observing System (EOS)
satellites and the next-generation of NASA-NOAA Joint Polar Satellite System (JPSS) series of satellites (renamed to NOAA-series).  Climatologists use VIIRS data 
to improve our understanding of global climate change.

**NetCDF** (Network Common Data Form) is a set of software libraries and machine-independent data formats that support the creation, access, and sharing of array-oriented 
scientific data. It is also a community standard for sharing scientific data. It is a widely used file format and set of software libraries designed to store and manage 
large scientific datasets. It is especially popular in Earth sciences, including fields like meteorology, oceanography, and remote sensing, due to its ability to handle 
multi-dimensional data efficiently.

The **M13 band** of the VIIRS sensor, is a part of the mid-infrared or thermal infrared spectrum, whichi is sensitive to heat emmisions, as fire emmits strong radiation. 
Radiance is the measure of intensity of radiation emmited or reflected by a surface, measured in units *W/m²·sr·μm*. The Earth view radiance refers to the radiance detected 
by the satellite sensor as it looks down at Earth's surface. VIIRS has 22 spectral bands, which are categorized as Visible, Neaf-Infrared and more.

A **band** refers to a spacific range og wavelengths of the electromagnetic spectrum that a satellite sensor is designed to detect. Each band collects information about the
Earth's surface and atmosphere by measuring the energy (radiance) within its wavelength range. In **M13** band's case, potential fire pixels (hotspots) are pixels where the 
“Earth view radiance” in the spectral region between 3.973 μm and 4.128 μm.

VIIRS sensor collects data by sweeping (or scanning) across the Earth's surface as the satellite moves along its orbital path. Each sweep or scan captures a slice of the 
Earth's surface called a scan line. The number of lines on the X-axis represents the sequential order of these scans as the satellite moves forward.

## Assignment Analysis

### Input: Satellite Data - VIIRS images

We have 4 sample satellite overpasses. Each overpass consists of two NetCDF files, that can be explored using [Panoply](https://www.giss.nasa.gov/tools/panoply/)

1. File starting with *VNP02* contains observation data (radiance recorded by the sensor)
2. File starting with *VNP03* contains geolocation data (the geographical coordinates of each pixel in the observation data file)

Analysis for the input data can be found [here](./input-data.md).

### Function: Python service that detects thermal anomalies (hot pixels or hotspots)

Potential fire pixels (hotspots) are pixels where the “Earth view radiance” in the spectral region between 3.973 μm and 4.128 μm, which is recorded in the M13 band of the VIIRS 
sensor, is significantly higher than the nonfire background.

Analysis about the fire / thermal anomalies detection can be found [here](./thermal-anomalies-detection.md)

### Output: GeoJSON of fire detections

GeoJSON response to the REST API call.

## In a few words

Create a Python REST service that let's a user upload a **netcd file** and gets a GeoJSON file of the fire detections.

## References

1. https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/viirs/
2. https://search.earthdata.nasa.gov/search
3. https://drive.google.com/drive/folders/10A4opHjdt99LrdI_IhKglB3d1G2jWa0X
4. https://www.unidata.ucar.edu/software/netcdf/
5. https://www.giss.nasa.gov/tools/panoply/
6. https://geojson.org/
