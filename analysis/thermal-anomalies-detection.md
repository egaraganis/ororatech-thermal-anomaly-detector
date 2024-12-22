# Thermal Anomalies Detection

The **M13 band** of the VIIRS sensor, is a part of the mid-infrared or thermal infrared spectrum, which is sensitive to heat emmisions, as fire emmits strong radiation. Radiance is the measure of intensity of radiation emmited or reflected by a surface, measured in units *W/m²·sr·μm*. The Earth view radiance refers to the radiance detected by the satellite sensor as it looks down at Earth's surface.

A **band** refers to a spacific range og wavelengths of the electromagnetic spectrum that a satellite sensor is designed to detect. Each band collects information about the Earth's surface and atmosphere by measuring the energy (radiance) within its wavelength range. In **M13** band's case, potential fire pixels (hotspots) are pixels where the “Earth view radiance” in the spectral region between 3.973 μm and 4.128 μm.

## Idea

Identify and analyze the nonfire background and compare that radiance. A pixel will be flagged as a *hot pixel* or a potential fire spot/hotspot if its radiance exceeds a specific **threshold**, specified by the analysis and comparison with the nonfire background.

So, 1rst we need to come up with this threshold to filter the M13 band. We'll also need to some sort of extra validation or contextual info to identify false positives. Other filters ? Other important aspects? Bright surfaces, volcanic activity, industrial hotspots?

## Understanding assignment information about thermal anomaly detection

### Potential fire pixels (hotspots) are pixels where the “Earth view radiance” in the spectral region between 3.973 μm and 4.128 μm

This is the part of the mid-infrared (MIR) spectrum where hot objects, like fires, emit significant thermal energy. VIIRS M13 band captures ranges on between 3973 and 4128 that are highly sensitive to heat emmision. It's is measured in *W/m²·sr·μm*.

### Reading the paper: The New VIIRS 375 m active fire detection data product: Algorithm description and initial assessment

[Analysis Results]

The rest of paper's analysis can be found [here](./new-viirs-375-fire-detection.md).

## Thought process, initial approach

We have 4 overpasses:

- 1000: 20/08/2020 10:00 - 10:06
- 2118: 20/08/2020 21:18 - 21:24
- 0942: 21/08/2020 09:42 - 9:48
- 2100: 21/08/2020 21:00 - 21:06

In order to understand the data, I'll identify the MIN-MAX value of each overpass and color contour between that range, to understand how radiance varies across the globe.

### 1000

Min value: 0.0010805600322782993 at scan line 2761, pixel 3173  
Max value: 81.32862854003906 at scan line 1035, pixel 1514

![M13 Color Contour - 1](../img/p-color-contour-1000-m13-0.png)
![M13 Color Contour - 2](../img/p-color-contour-1000-m13-1.png)
![M13 Color Contour - 3](../img/p-color-contour-1000-m13-2.png)
![M13 Color Contour - 3](../img/p-color-contour-1000-m13-3.png)

### 2118

Min value: 0.009168829768896103 at scan line 1847, pixel 153  
Max value: 264.317626953125 at scan line 2925, pixel 1116

![M13 Color Contour - 1](../img/p-color-contour-2118-m13-0.png)
![M13 Color Contour - 2](../img/p-color-contour-2118-m13-1.png)
![M13 Color Contour - 3](../img/p-color-contour-2118-m13-2.png)
![M13 Color Contour - 3](../img/p-color-contour-2118-m13-3.png)

### 0942

Min value: 0.0010805600322782993 at scan line 1510, pixel 2420  
Max value: 16.404090881347656 at scan line 1075, pixel 1237

![M13 Color Contour - 1](../img/p-color-contour-0942-m13-0.png)
![M13 Color Contour - 2](../img/p-color-contour-0942-m13-1.png)
![M13 Color Contour - 3](../img/p-color-contour-0942-m13-2.png)
![M13 Color Contour - 3](../img/p-color-contour-0942-m13-3.png)

### 2100

Min value: 0.017257098108530045 at scan line 72, pixel 179  
Max value: 145.32301330566406 at scan line 2869, pixel 1418

![M13 Color Contour - 1](../img/p-color-contour-2100-m13-0.png)
![M13 Color Contour - 2](../img/p-color-contour-2100-m13-1.png)
![M13 Color Contour - 3](../img/p-color-contour-2100-m13-2.png)
![M13 Color Contour - 3](../img/p-color-contour-2100-m13-3.png)

### Initial observation

Let's observe and understand the initial data and diagrams:

#### 1000

Min value: 0.0010805600322782993 at scan line 2761, pixel 3173  
Max value: 81.32862854003906 at scan line 1035, pixel 1514

![1000 array](../img/1000-array.png)
![M13 Color Contour - 3](../img/p-color-contour-1000-m13-3.png)

Given the max value of 81.32, there's a visible surrounding increased radiance, at around 20-25.

That's around 25% of the max value and around 30 times bigger than the surround array.
That might be an indicator of first threshold. 

    It's wise to also count the median values, especially of what I assume to be nonfire backgrounds.

#### 2118

Min value: 0.009168829768896103 at scan line 1847, pixel 153  
Max value: 264.317626953125 at scan line 2925, pixel 1116

![1000 array](../img/2118-array.png)
![M13 Color Contour - 3](../img/p-color-contour-2118-m13-3.png)

Given the above estimates, the 25% of max value is around 65, which also is visible with plain eye and indicates a fire-background.

#### 0942

Min value: 0.0010805600322782993 at scan line 1510, pixel 2420  
Max value: 16.404090881347656 at scan line 1075, pixel 1237

![M13 Color Contour - 3](../img/0942-array.png)
![M13 Color Contour - 3](../img/p-color-contour-0942-m13-3.png)

In similar manner, the 25% of max value is around 4, which agains indicates the visible spectrum of the potential fire.

#### 2100

Min value: 0.017257098108530045 at scan line 72, pixel 179  
Max value: 145.32301330566406 at scan line 2869, pixel 1418

![M13 Color Contour - 3](../img/2100-array.png)
![M13 Color Contour - 3](../img/p-color-contour-2100-m13-3.png)

For one last time, the 25% of max value is 36.25.

That gives a first initial rough threshold at around the 25% of the max value. This will be our starting point for the implementation.

Details about the 25-percent threshold will be further elaborated [here](./25-percent-threshold.md).

## Geographical interpretation and correlation