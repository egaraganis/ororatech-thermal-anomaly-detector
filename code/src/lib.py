from fastapi import UploadFile, HTTPException
from fastapi.responses import JSONResponse
import netCDF4
import io
import tempfile
import os
import numpy as np
import matplotlib.pyplot as plt
import geojson

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
    
    for file in files:
        if file.content_type != "application/x-netcdf":
            raise HTTPException(status_code=400, detail=f"Invalid file type: {file.filename}. Expecting: 'application/x-netcdf'.")
    
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

def apply_25_percent_threshold_and_return_geojson_points(observation_nc, geolocation_nc):
    M13 = observation_nc.groups["observation_data"].variables["M13"]
    data = M13[:]

    max_value = data.max()
    threshold = max_value * 0.25

    hotpixel_candidates = np.argwhere(data > threshold)
    return hotpixel_candidates_to_geojson_points(data, geolocation_nc, hotpixel_candidates)

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
    geojson_string = apply_25_percent_threshold_and_return_geojson_points(observation_nc, geolocation_nc)

    os.remove(o_tmp_file_name)
    os.remove(g_tmp_file_name)

    observation_nc.close()
    geolocation_nc.close()

    return JSONResponse(content=geojson_string, media_type="application/geo+json")
