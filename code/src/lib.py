from fastapi import UploadFile, HTTPException
import netCDF4
import io
import tempfile
import os
import numpy as np
import matplotlib.pyplot as plt

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

def analyze_observation_data(observation_nc):
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

async def debug_import_data(files: list[UploadFile]):
    validated_netcdf_files = validate_uploaded_netcdf_files(files)

    observation_nc, o_tmp_file_name = await read_netcdf_as_dataset(validated_netcdf_files['observation_data'])
    geolocation_nc, g_tmp_file_name = await read_netcdf_as_dataset(validated_netcdf_files['geolocation_data'])

    print("---- Observation Data - NetCDF file ----")
    print(observation_nc)

    print("\n\n\n")
    
    print("---- Geolocation Data - NetCDF file ----")
    print(geolocation_nc)

    analyze_observation_data(observation_nc)

    os.remove(o_tmp_file_name)
    os.remove(g_tmp_file_name)

    observation_nc.close()
    geolocation_nc.close()

    return {
        "observation data": validated_netcdf_files['observation_data'].filename,
        "geolocation data": validated_netcdf_files['geolocation_data'].filename
    }
