# Thermal Anomalies Detection

The **M13 band** of the VIIRS sensor, is a part of the mid-infrared or thermal infrared spectrum, which is sensitive to heat emmisions, as fire emmits strong radiation. Radiance is the measure of intensity of radiation emmited or reflected by a surface, measured in units *W/m²·sr·μm*. The Earth view radiance refers to the radiance detected by the satellite sensor as it looks down at Earth's surface.

A **band** refers to a spacific range og wavelengths of the electromagnetic spectrum that a satellite sensor is designed to detect. Each band collects information about the Earth's surface and atmosphere by measuring the energy (radiance) within its wavelength range. In **M13** band's case, potential fire pixels (hotspots) are pixels where the “Earth view radiance” in the spectral region between 3.973 μm and 4.128 μm. To further **clarify** this, all pixels captured by the M13 band measure radiance in the spectral region of 3.973 μm to 4.128 μm because that is the band’s designed wavelength range. What distinguishes "potential fire pixels" (hotspots) is not that their radiance falls within this range—since all captured radiances are within it—but rather that they exceed a specific radiance threshold within this spectral region. This threshold indicates anomalously high energy, which is often associated with fires or hotspots.

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

![1000 M13 Color Contour - 1](../img/p-color-contour-1000-m13-0.png)
![1000 M13 Color Contour - 2](../img/p-color-contour-1000-m13-1.png)
![1000 M13 Color Contour - 3](../img/p-color-contour-1000-m13-2.png)
![1000 M13 Color Contour - 3](../img/p-color-contour-1000-m13-3.png)

### 2118

Min value: 0.009168829768896103 at scan line 1847, pixel 153  
Max value: 264.317626953125 at scan line 2925, pixel 1116

![2118 M13 Color Contour - 1](../img/p-color-contour-2118-m13-0.png)
![2118 M13 Color Contour - 2](../img/p-color-contour-2118-m13-1.png)
![2118 M13 Color Contour - 3](../img/p-color-contour-2118-m13-2.png)
![2118 M13 Color Contour - 4](../img/p-color-contour-2118-m13-3.png)

### 0942

Min value: 0.0010805600322782993 at scan line 1510, pixel 2420  
Max value: 16.404090881347656 at scan line 1075, pixel 1237

![0942 M13 Color Contour - 1](../img/p-color-contour-0942-m13-0.png)
![0942 M13 Color Contour - 2](../img/p-color-contour-0942-m13-1.png)
![0942 M13 Color Contour - 3](../img/p-color-contour-0942-m13-2.png)
![0942 M13 Color Contour - 4](../img/p-color-contour-0942-m13-3.png)

### 2100

Min value: 0.017257098108530045 at scan line 72, pixel 179  
Max value: 145.32301330566406 at scan line 2869, pixel 1418

![2100 M13 Color Contour - 1](../img/p-color-contour-2100-m13-0.png)
![2100 M13 Color Contour - 2](../img/p-color-contour-2100-m13-1.png)
![2100 M13 Color Contour - 3](../img/p-color-contour-2100-m13-2.png)
![2100 M13 Color Contour - 4](../img/p-color-contour-2100-m13-3.png)

### Initial observation

Let's observe and understand the initial data and diagrams:

#### 1000

Min value: 0.0010805600322782993 at scan line 2761, pixel 3173  
Max value: 81.32862854003906 at scan line 1035, pixel 1514

![1000 array](../img/1000-array.png)
![1000 M13 Color Contour - 3](../img/p-color-contour-1000-m13-3.png)

Given the max value of 81.32, there's a visible surrounding increased radiance, at around 20-25.

That's around 25% of the max value and around 30 times bigger than the surround array.
That might be an indicator of first threshold. 

    It's wise to also count the median values, especially of what I assume to be nonfire backgrounds.

#### 2118

Min value: 0.009168829768896103 at scan line 1847, pixel 153  
Max value: 264.317626953125 at scan line 2925, pixel 1116

![2118 array](../img/2118-array.png)
![2118 Color Contour - 4](../img/p-color-contour-2118-m13-3.png)

Given the above estimates, the 25% of max value is around 65, which also is visible with plain eye and indicates a fire-background.

#### 0942

Min value: 0.0010805600322782993 at scan line 1510, pixel 2420  
Max value: 16.404090881347656 at scan line 1075, pixel 1237

![0942 array](../img/0942-array.png)
![0942 M13 Color Contour - 4](../img/p-color-contour-0942-m13-3.png)

In similar manner, the 25% of max value is around 4, which agains indicates the visible spectrum of the potential fire.

#### 2100

Min value: 0.017257098108530045 at scan line 72, pixel 179  
Max value: 145.32301330566406 at scan line 2869, pixel 1418

![2100 array](../img/2100-array.png)
![2100 M13 Color Contour - 4](../img/p-color-contour-2100-m13-3.png)

For one last time, the 25% of max value is 36.25.

That gives a first initial rough threshold at around the 25% of the max value. This will be our starting point for the implementation.

## Geographical interpretation and correlation

### Geolocating hotpixels

Since we have a first rough threshold, we can filter out the hotpixels candidates

```python
def apply_25_percent_threshold_and_return_geojson_points(observation_nc, geolocation_nc):
    M13 = observation_nc.groups["observation_data"].variables["M13"]
    data = M13[:]

    max_value = data.max()
    threshold = max_value * 0.25

    hotpixel_candidates = np.argwhere(data > threshold)

    return hotpixel_candidates_to_geojson_points(data, geolocation_nc, hotpixel_candidates)
```

We can now correlate our observation data with our geolocation data in the following way

```python
def hotpixel_candidates_to_geospatial_coords(geolocation_nc, hotpixel_candidates):
    lats = geolocation_nc.groups["geolocation_data"].variables["latitude"][:]
    longs = geolocation_nc.groups["geolocation_data"].variables["longitude"][:]

    hotpixel_candidates_as_geospatial_coords = []
    for pos in hotpixel_candidates:
        scan_line, pixel = pos
        longitude = longs[scan_line, pixel]
        latitude = lats[scan_line, pixel]

        geospatial_coords = (float(longitude), float(latitude))
        hotpixel_candidates_as_geospatial_coords.append(geospatial_coords)
    
    return hotpixel_candidates_as_geospatial_coords
```

and we can locate our hotpixel candidats across the globe.

#### 1000

![M13 Color Contour - 3](../img/p-color-contour-1000-m13-2.png)
![1000 GeoPoints](../img/1000-25percent-geopoints.png)

#### 2118

![2118 M13 Color Contour - 3](../img/p-color-contour-2118-m13-2.png)
![1000 GeoPoints](../img/2118-25percent-geopoints.png)

#### 0942

![2118 M13 Color Contour - 3](../img/p-color-contour-0942-m13-1.png)
![0942 GeoPoints](../img/0942-25percent-geopoints.png)

#### 2100

![2100 M13 Color Contour - 3](../img/p-color-contour-2100-m13-1.png)
![2100 GeoPoints](../img/2100-25percent-geopoints.png)

### Clustering, Convex and Concave

Since we have the list of geopoints, we can create clusters group fires together. I'll proceed with DBSCAN (Density-Based Spatial Clustering of Applications with Noise) algorithm to cluster geospatial coordinates based on their density. I could also use K-means, but I'll start with a density-based candidate, since it feels more appropriate in a fire scenario.

```python
def cluster_hotpixel_candidates_based_on_geospatial_coords(hotpixel_candidates_with_geospatial_coords):
    db = DBSCAN(eps=1, min_samples=3)
    labels = db.fit_predict(hotpixel_candidates_with_geospatial_coords)
        
    cluster_points_dictionary = {}

    for label, point in zip(labels, hotpixel_candidates_with_geospatial_coords):
        if label not in cluster_points_dictionary:
            cluster_points_dictionary[label] = []
        cluster_points_dictionary[label].append(point)

    for cluster_id, cluster_points in cluster_points_dictionary.items():
        print(f"Cluster {cluster_id}:")
        print(np.array(cluster_points))
        print()

    return cluster_points_dictionary
```

This will get us the following clusters:

```
Cluster 0:
[[-110.7358017    33.59133911]
 [-110.73579407   33.60146332]
 [-110.73025513   33.59639359]
 [-110.74247742   33.59550476]]

Cluster -1:
[[-118.62554932   34.64097595]
 [-118.6272583    34.64771652]
 [-118.44802094   36.16013336]
 [-121.5568924    36.08182144]
 [-122.31288147   38.58563232]
 [-122.42124939   38.69715118]
 [-114.42114258   40.05718994]
 [-114.43203735   40.0562439 ]]

Cluster 1:
[[-121.40475464   37.19813538]
 [-121.41491699   37.20340347]
 [-121.44151306   37.24637222]
 [-121.45319366   37.25822449]
 [-121.5871048    37.41403961]
 [-121.59572601   37.41272354]
 [-121.54870605   37.44037247]
 [-121.55734253   37.4390564 ]]

Cluster 2:
[[-120.86023712   39.86500168]
 [-120.86956787   39.86369324]
 [-120.87889862   39.90847397]
 [-120.7756958    40.26120758]
 [-120.7775116    40.26786041]
 [-120.78694916   40.2665596 ]
 [-120.68502808   40.3219986 ]
 [-120.6399765    40.34206009]
 [-120.64944458   40.34075546]
 [-120.64135742   40.34879303]
 [-120.74514771   40.33445358]
 [-120.7543869    40.33317184]
 [-120.74643707   40.34119034]
 [-120.18227386   41.01687622]
 [-120.19193268   41.01562119]
 [-120.18370819   41.02371216]]

Cluster 3:
[[-122.82202911   39.76302719]
 [-122.76828003   39.80564117]
 [-122.77716827   39.804245  ]
 [-122.83301544   39.91775131]]
```

Based on those clusters, we can start of forming initial rough polygons, without any transformation to convex or concave.

```python
def cluster_hotpixel_candidates_based_on_geospatial_coords_and_return_geojson_plain_polygon_for_each(hotpixel_candidates_with_geospatial_coords):
    cluster_points_dictionary = cluster_hotpixel_candidates_based_on_geospatial_coords(hotpixel_candidates_with_geospatial_coords)
    features = []
    
    for cluster_id, points in cluster_points_dictionary.items():
        if cluster_id == -1:
            points_as_geojson = [geojson.Point(point) for point in points]
            features.extend([geojson.Feature(geometry=point, properties={"cluster": str(cluster_id)}) for point in points_as_geojson])
        else:
            polygon = Polygon(points)
            feature = geojson.Feature(geometry=polygon, properties={"cluster": str(cluster_id)})
            features.append(feature)

    feature_collection = geojson.FeatureCollection(features)
    return feature_collection
```

For the following points for example in the 2100 case

![2100 GeoPoints](../img/2100-25percent-geopoints.png)

We will get the following rough clusters polygons:

![2100 Polygons](../img/2100-polygons.png)

#### Current clustering state

The current clustering implementation, although successfuly clusters suggested group of geopoints, it's far from perfect. 

For example, in 1000 overpass case (with the 25% threshold):

![1000 Geopoints using 25% threshold](../img/1000-25percent-geopoints.png)

The current implementation will produce only one cluster (the -1 cluster are unclustered points):

```
Cluster -1:
[[-120.71125793   40.34169769]
 [-120.9099884    39.86947632]
 [-122.13737488   37.09511185]
 [-122.1144104    37.04351044]]

Cluster 0:
[[-122.63578796   40.09431458]
 [-122.90533447   39.93113327]
 [-122.64936829   39.79103851]
 [-122.69385529   39.64148712]
 [-122.74889374   39.64290237]
 [-122.72521973   39.62568665]
 [-122.71636963   39.62435532]
 [-122.71795654   39.61776733]
 [-122.68000793   39.58473206]
 [-122.67118073   39.58339691]
 [-122.66231537   39.58205795]
 [-122.65348053   39.58071899]
 [-122.64465332   39.57938766]
 [-122.69702911   39.58108902]
 [-122.68821716   39.57975388]
 [-122.28173828   38.8516655 ]
 [-122.40023041   38.78129959]
 [-122.39141846   38.77993393]
 [-122.38262177   38.7785759 ]
 [-122.29696655   38.56147766]]
```

![1000 Convex Polygons using 25% threshold](../img/1000-25percent-convex-polygons.png)

I would expect this at least create 2 clusters, between the upper and lower parts of the geopoints in the center.

#### Convex

In the polygon formation above, the geopoints of each cluster are being dumped in a geojson polygon, without any prior transformation. That leads to invalid polygons. For e.g. in 0942 overpass case (with the 25% threshold):

![0942 Geopoints using 25% threshold](../img/0942-25percent-geopoints.png)

This is the resulted polygons for each cluster:

![0942 Plain Polygons using 25% threshold](../img/0942-25percent-plain-polygons.png)

In order to combat this, I used SciPy's ConvexHull:

```python
def cluster_hotpixel_candidates_based_on_geospatial_coords_and_return_geojson_convex_polygon_for_each(hotpixel_candidates_with_geospatial_coords):
    cluster_points_dictionary = cluster_hotpixel_candidates_based_on_geospatial_coords(hotpixel_candidates_with_geospatial_coords)

    features = []
    for cluster_id, points in cluster_points_dictionary.items():
        if cluster_id == -1:
            points_as_geojson = [geojson.Point(point) for point in points]
            features.extend([geojson.Feature(geometry=point, properties={"cluster": str(cluster_id)}) for point in points_as_geojson])
        else:
            points_np = np.array(points)
            if len(points_np) >= 3:
                hull = ConvexHull(points_np)
                hull_points = points_np[hull.vertices]
                polygon = Polygon(hull_points)
                feature = geojson.Feature(geometry=polygon, properties={"cluster": str(cluster_id)})
                features.append(feature)

    feature_collection = geojson.FeatureCollection(features)
    return feature_collection
```

which, calculated the convex hull on the potential hotpixel candidates:

![0942 Convex Polygons using 25% threshold](../img/0942-25percent-convex-polygons.png)

    For once again, the convex hull creation needs further experimentation and fine-tuning (See part of cluster's polygon being on the sea). The implementation above doesn't take into consideration the earth's curved surface.

#### Concave

Now, for the concave part we will use `alphashape` library, that computes the concave hull for the given points and then with the `alpha` parameter we are going to further experiment for boundary tightness in order to generate different concave hulls.

```python
def cluster_hotpixel_candidates_based_on_geospatial_coords_and_return_geojson_concave_polygon_for_each(hotpixel_candidates_with_geospatial_coords):
    cluster_points_dictionary = cluster_hotpixel_candidates_based_on_geospatial_coords(hotpixel_candidates_with_geospatial_coords)

    features = []
    alpha = 4.0

    for cluster_id, points in cluster_points_dictionary.items():
        if cluster_id == -1:
            points_as_geojson = [geojson.Point(point) for point in points]
            features.extend([geojson.Feature(geometry=point, properties={"cluster": str(cluster_id)}) for point in points_as_geojson])
        else:
            points_np = np.array(points)
            if len(points_np) >= 3:
                concave_hull = alphashape.alphashape(points_np, alpha)
                if isinstance(concave_hull, Polygon):
                    feature = geojson.Feature(geometry=mapping(concave_hull), properties={"cluster": str(cluster_id)})
                    features.append(feature)
                elif concave_hull.geom_type == "MultiPolygon":
                    for geom in concave_hull.geoms:
                        feature = geojson.Feature(geometry=mapping(geom), properties={"cluster": str(cluster_id)})
                        features.append(feature)

    feature_collection = geojson.FeatureCollection(features)
    return feature_collection
```

For 0942 overpass cases, the generated concaves looks like this:

![0942 Concave Polygons using 25% threshold](../img/0942-25percent-concave-polygons.png)

While for the 1000 overpass, these are the generate concaves:

![1000 Convex Concave using 25% threshold](../img/1000-25percent-concave-polygons.png)

Which improves the issue with our current clustering state, that generates only one cluster (see [above](#current-clustering-state)).

## Touchdown, recap and further steps

Have research and successfuly completed a first implementation circle, I can recap the process in the following steps:

1. Derive the apply the initial 25% threshold
2. Apply threshold to M13 filter and find hotspot candidates
3. Convert those hotspot candidates from scan and pixel to geospatial coordinates
4. Cluster those hotspot candidates
5. Create a convex or/and concave to get the geojson polygons

Further steps include experimenting with each one of the above steps, like applying other thresholds, clustering with different candidates, effectively creating convex or concave for each cluster.

## Beyond 25% rough threshold

### Planck's Law

Now that we have a rough threshold for detecting possible hotpixels candidates, we can further delve into the domain. Our current threshold is derived based on each overpass. But since our overpass is with a 48-hour span over the same spot, then we would expect the threshold to be
more of a fixed value, across overpasses.

The M13 filter on the VIIRS (Visible Infrared Imaging Radiometer Suite) sensor is part of its thermal infrared channels, specifically designed to measure emitted radiance from the Earth. Radiance measured by the M13 filter can be converted to temperature using Planck's law and the inverse Planck function.

Based on the following Python implementation, we will color contour the available overpasses:

```python
def calculate_celcius_with_plancks_equation(radiance):
    exponent_part = plancks_exponent_part_numerator / (radiance*10**6 * lamnda_m_5)
    T_kelvin = plancks_numerator / (plancks_denominator * math.log(1 + exponent_part))

    T_celsius = T_kelvin - 273.15
    return T_celsius

def apply_plancks_equation_to_observation_data_and_color_contour(observation_nc):
    M13 = observation_nc.groups["observation_data"].variables["M13"]
    data = M13[:]

    calculated_celcius_per_pixel = []

    for pixel_radiance in data.flatten():
        calculated_celcius_per_pixel.append(calculate_celcius_with_plancks_equation(pixel_radiance))

    calculated_celcius_data = np.array(calculated_celcius_per_pixel).reshape(data.shape)

    plt.figure(figsize=(8, 6))
    
    contour = plt.contourf(calculated_celcius_data, cmap='coolwarm', levels=20)
    plt.colorbar(contour)
    
    plt.title("Temperature Distribution (°C)")
    plt.xlabel("Pixel (X)")
    plt.ylabel("Scanline (Y)")
    
    plt.show()
```

Let's see how temperature varies across our overpasses

#### 1000

![1000-Color-Contour-Celcius-1](../img/1000-celcius-1.png)
![1000-Color-Contour-Celcius-2](../img/1000-celcius-2.png)
![1000-Color-Contour-Celcius-3](../img/1000-celcius-3.png)

#### 2118

![2118-Color-Contour-Celcius-1](../img/2118-celcius-1.png)
![2118-Color-Contour-Celcius-2](../img/2118-celcius-2.png)
![2118-Color-Contour-Celcius-3](../img/2118-celcius-3.png)

#### 0942

![0942-Color-Contour-Celcius-1](../img/0942-celcius-1.png)
![0942-Color-Contour-Celcius-2](../img/0942-celcius-2.png)
![0942-Color-Contour-Celcius-3](../img/0942-celcius-3.png)

#### 2100

![2100-Color-Contour-Celcius-1](../img/2100-celcius-1.png)
![2100-Color-Contour-Celcius-2](../img/2100-celcius-2.png)
![2100-Color-Contour-Celcius-3](../img/2100-celcius-3.png)

A brief research on fire temperature behavior suggests that:

- At temperatures around 200°C-600°C, the fire may be in the smoldering stage, where organic material, such as dead wood or leaf litter, slowly burns without producing visible flames. This can happen in the understory or the forest floor, and while it's not as intense as a full blaze, it can still cause damage and spread over time, especially in dry conditions.
- Crown Fire (High Intensity): Temperature: 800°C to 1,200°C (1,472°F to 2,192°F)
- Flaming Combustion (General Flames): Temperature: 600°C to 1,000°C (1,112°F to 1,832°F)
- Hot Spots/Intense Fires: Temperature: 1,200°C to 1,400°C (2,192°F to 2,552°F)

### The 60 W/m²·sr·μm* fixed threshold

Based on the above, we will apply a uniform fixed threshold over all overpasses that being at 60W/m²·sr·μm*, meaing 200.12°C, which can be an indicator of even smoldering fires.

#### 1000

![1000-60-Geopoints](../img/1000-60-geopoints.png)

#### 2118

![2118-60-Geopoints](../img/2118-60-geopoints.png)

#### 0942

No geopoints yielded, which is logical, since the max Celcius is just above 120°C.

#### 2100

![2100-60-Geopoints](../img/2100-60-geopoints.png)

### Comparison between the 25% dynamic threshold and the 60 W/m²·sr·μm* fixed one

The 25% of the max radiance captured threshold offers a uniform and dynamic approach in classifying hotpixels candidates. It offers a fast and immediate way to compare captured radiances for each pixel with the rest, implicitily comparing the nonfire background. While it provides a fast filtering over data, it can't be considered credible, given the dynamic nature of data its radiance variance. In contrast, a fixed 60 W/m²·sr·μm threshold that suggests a 200°C temperature, and a possible indicator of smaller fires, seems a more reliable approach on identifying potential fires. A possible combination of both thresholds, in a sense that considers the nonfire background and filters out pixels with radiance bellow 200°C, could provide more reliable results.

### Other fire-detection approaches

Of course both of the above proposed thresholds are rough and naive, that need further investigation both vertically and horizontally. Before conducting further research on current bibliography, I would also to explore the following factors and approaches:

1. Compare hotpixel candidates with the median of non-firebackground
2. Compare data and radiance with other days and time of the year
3. Experiment with other bands and filters (for example pixel lumens to Kelvin from other bands, if captured? What's the pixel saturation called so often in the paper). Contextual approach or combination of factors?
4. Validate data with real images
5. Consider other factors, like clouds, surface's, magnetic anomalies and more