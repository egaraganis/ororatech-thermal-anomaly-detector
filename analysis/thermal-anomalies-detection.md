# Thermal Anomalies Detection

The **M13 band** of the VIIRS sensor, is a part of the mid-infrared or thermal infrared spectrum, which is sensitive to heat emmisions, 
as fire emmits strong radiation. Radiance is the measure of intensity of radiation emmited or reflected by a surface, measured in units
*W/m²·sr·μm*. The Earth view radiance refers to the radiance detected by the satellite sensor as it looks down at Earth's surface.

A **band** refers to a spacific range og wavelengths of the electromagnetic spectrum that a satellite sensor is designed to detect. Each band collects information about the
Earth's surface and atmosphere by measuring the energy (radiance) within its wavelength range. In **M13** band's case, potential fire pixels (hotspots) are pixels where the 
“Earth view radiance” in the spectral region between 3.973 μm and 4.128 μm.

## Idea

Identify and analyze the nonfire background and compare that radiance. A pixel will be flagged as a *hot pixel* or a potential fire spot/
hotspot if its radiance exceeds a specific **threshold**, specified by the analysis and comparison with the nonfire background.

So, 1rst we need to come up with this threshold to filter the M13 band. We'll also need to some sort of extra validation or contextual info
to identify false positives. Other filters ? Other important aspects? Bright surfaces, volcanic activity, industrial hotspots?

## Understanding assignment information about thermal anomaly detection

### Potential fire pixels (hotspots) are pixels where the “Earth view radiance” in the spectral region between 3.973 μm and 4.128 μm

This is the part of the mid-infrared (MIR) spectrum where hot objects, like fires, emit significant thermal energy. VIIRS M13 band captures ranges on between 3973 and 4128
that highly sensitive to heat emmision. It's is measured in *W/m²·sr·μm*.

### Reading the paper: The New VIIRS 375 m active fire detection data product: Algorithm description and initial assessment

[Analysis Results]

The rest of paper's analysis can be found [here](./new-viirs-375-fire-detection.md).
