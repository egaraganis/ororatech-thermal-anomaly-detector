from fastapi import UploadFile, HTTPException
from fastapi.responses import JSONResponse
import netCDF4
import io
import tempfile
import os
import numpy as np
import matplotlib.pyplot as plt
import geojson
from shapely.geometry import Polygon
from sklearn.cluster import DBSCAN
import math
from constants import plancks_exponent_part_numerator, lamnda_m_5, plancks_numerator, plancks_denominator

def debug_hotpixes_candidates(hotpixel_candidates):
    for pos in hotpixel_candidates:
        scan_line, pixel = pos
        value = data[scan_line, pixel]
        print(f"  Scan line {scan_line}, Pixel {pixel}: Value = {value}")  

def debug_nc_files(observation_nc, geolocation_nc):
    print("---- Observation Data - NetCDF file ----")
    print(observation_nc)

    print("\n\n\n")
    
    print("---- Geolocation Data - NetCDF file ----")
    print(geolocation_nc)

def validate_uploaded_netcdf_files(files: list[UploadFile]):
    if len(files) != 2:
        raise HTTPException(status_code=400, detail="You must upload exactly two files.")
    
    # for file in files:
    #     if file.content_type != "application/x-netcdf":
    #         raise HTTPException(status_code=400, detail=f"Invalid file type: {file.filename}. Expecting: 'application/x-netcdf'.")
    
    file1_first_token = files[0].filename[:5]
    file1_second_token = files[0].filename[5:]
    file2_first_token = files[1].filename[:5]
    file2_second_token = files[1].filename[5:]

    if file1_second_token != file2_second_token:
        raise HTTPException(status_code=400, detail="Ensure you have selected the observation and geolocation nc file of the same overpass.")
    
    elif sorted([file1_first_token, file2_first_token]) != ["VNP02", "VNP03"]:
        raise HTTPException(status_code=400, detail="Ensure you have selected the observation and geolocation nc file of the same overpass.")

    if(file1_first_token == "VNP02"):
        return {
            'observation_data': files[0],
            'geolocation_data': files[1],
        }
    else:
        return {
            'observation_data': files[1],
            'geolocation_data': files[0],
        }  

async def read_netcdf_as_dataset(file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        try:
            tmp.write(await file.read())
            tmp.flush()
            nc_dataset = netCDF4.Dataset(tmp.name, 'r')

            return [nc_dataset, tmp.name]
        
        except Exception as e:
            raise ValueError(f"Error reading NetCDF file: {str(e)}")
        
        finally:
            tmp.close()

def find_mix_max_and_contour_plot(observation_nc):
    print("\n\n\n")

    M13 = observation_nc.groups["observation_data"].variables["M13"]
    #print(M13)

    data = M13[:]
    #print(data)

    min_value = data.min()
    max_value = data.max()

    min_position = np.unravel_index(data.argmin(), M13.shape)
    max_position = np.unravel_index(data.argmax(), M13.shape)

    print(f"Minimum value: {min_value} at scan line {min_position[0]}, pixel {min_position[1]}")
    print(f"Maximum value: {max_value} at scan line {max_position[0]}, pixel {max_position[1]}")

    plt.figure(figsize=(10, 6))
    plt.contourf(data, levels=100, cmap='viridis')
    plt.colorbar(label='Radiance (Watts/m^2/sr/μm)')
    plt.title(f'Color Contour Plot of M13')
    plt.xlabel('Pixel')
    plt.ylabel('Scan Line')
    plt.show()

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

def apply_25_percent_threshold_and_return_geojson_points(observation_nc, geolocation_nc):
    M13 = observation_nc.groups["observation_data"].variables["M13"]
    data = M13[:]

    max_value = data.max()
    threshold = max_value * 0.25

    hotpixel_candidates = np.argwhere(data > threshold)

    return hotpixel_candidates_to_geojson_points(data, geolocation_nc, hotpixel_candidates)

def apply_25_percent_threshold_and_return_geojson_convex(observation_nc, geolocation_nc):
    M13 = observation_nc.groups["observation_data"].variables["M13"]
    data = M13[:]

    max_value = data.max()
    threshold = max_value * 0.25

    hotpixel_candidates = np.argwhere(data > threshold)

    hotpixel_candidates_with_geospatial_coords = hotpixel_candidates_to_geospatial_coords(geolocation_nc, hotpixel_candidates)

    geojson = cluster_hotpixel_candidates_based_on_geospatial_coords_and_return_geojson_convex_for_each(hotpixel_candidates_with_geospatial_coords)

    return geojson

def apply_60_fixed_radiance_threshold_and_return_geojson_points(observation_nc, geolocation_nc):
    M13 = observation_nc.groups["observation_data"].variables["M13"]
    data = M13[:]

    max_value = data.max()
    threshold = 60

    hotpixel_candidates = np.argwhere(data > threshold)

    if not hotpixel_candidates.size > 0:
        return {}

    return hotpixel_candidates_to_geojson_points(data, geolocation_nc, hotpixel_candidates)

def apply_60_fixed_radiance_threshold_and_return_geojson_convex(observation_nc, geolocation_nc):
    M13 = observation_nc.groups["observation_data"].variables["M13"]
    data = M13[:]

    max_value = data.max()
    threshold = 60

    hotpixel_candidates = np.argwhere(data > threshold)

    if not hotpixel_candidates.size > 0:
        return {}

    hotpixel_candidates_with_geospatial_coords = hotpixel_candidates_to_geospatial_coords(geolocation_nc, hotpixel_candidates)

    geojson = cluster_hotpixel_candidates_based_on_geospatial_coords_and_return_geojson_convex_for_each(hotpixel_candidates_with_geospatial_coords)

    return geojson

def cluster_hotpixel_candidates_based_on_geospatial_coords_and_return_geojson_convex_for_each(hotpixel_candidates_with_geospatial_coords):
    db = DBSCAN(eps=1, min_samples=3)
    labels = db.fit_predict(hotpixel_candidates_with_geospatial_coords)
    
    #print("Cluster labels for each point:", labels)
    
    cluster_points_dict = {}

    for label, point in zip(labels, hotpixel_candidates_with_geospatial_coords):
        if label not in cluster_points_dict:
            cluster_points_dict[label] = []
        cluster_points_dict[label].append(point)

    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }

    for cluster_id, cluster_points in cluster_points_dict.items():
        print(f"Cluster {cluster_id}:")
        print(np.array(cluster_points))
        print()

    features = []
    
    for cluster_id, points in cluster_points_dict.items():
        if cluster_id == -1:
            points_as_geojson = [geojson.Point(point) for point in points]
            features.extend([geojson.Feature(geometry=point, properties={"cluster": str(cluster_id)}) for point in points_as_geojson])
        else:
            polygon = Polygon(points)
            feature = geojson.Feature(geometry=polygon, properties={"cluster": str(cluster_id)})
            features.append(feature)

    feature_collection = geojson.FeatureCollection(features)

    return feature_collection

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

def hotpixel_candidates_to_geojson_points(observation_data, geolocation_nc, hotpixel_candidates):
    lats = geolocation_nc.groups["geolocation_data"].variables["latitude"][:]
    longs = geolocation_nc.groups["geolocation_data"].variables["longitude"][:]

    features = []
    for pos in hotpixel_candidates:
        scan_line, pixel = pos
        value = observation_data[scan_line, pixel]
        longitude = longs[scan_line, pixel]
        latitude = lats[scan_line, pixel]
        
        feature = geojson.Feature(
            geometry=geojson.Point((float(longitude), float(latitude))),
            properties={
                "value": float(value),
                "scan_line": int(scan_line),
                "pixel": int(pixel)
            }
        )
        features.append(feature)
    
    feature_collection = geojson.FeatureCollection(features)
    return feature_collection

async def detect_thermal_anomalies(files: list[UploadFile]):
    validated_netcdf_files = validate_uploaded_netcdf_files(files)

    observation_nc, o_tmp_file_name = await read_netcdf_as_dataset(validated_netcdf_files['observation_data'])
    geolocation_nc, g_tmp_file_name = await read_netcdf_as_dataset(validated_netcdf_files['geolocation_data'])

    #find_mix_max_and_contour_plot(observation_nc)
    
    geojson_points = apply_25_percent_threshold_and_return_geojson_points(observation_nc, geolocation_nc)
    geojson_convex = apply_25_percent_threshold_and_return_geojson_convex(observation_nc, geolocation_nc)

    #apply_plancks_equation_to_observation_data_and_color_contour(observation_nc)

    # geojson_points = apply_60_fixed_radiance_threshold_and_return_geojson_points(observation_nc, geolocation_nc)
    # geojson_convex = apply_60_fixed_radiance_threshold_and_return_geojson_convex(observation_nc, geolocation_nc)

    os.remove(o_tmp_file_name)
    os.remove(g_tmp_file_name)

    observation_nc.close()
    geolocation_nc.close()

    geojson = {
        "points": geojson_points,
        "convex": geojson_convex
    }

    # geojson = ""

    return JSONResponse(content=geojson, media_type="application/geo+json")
