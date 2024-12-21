from fastapi import UploadFile, HTTPException
import netCDF4
import io
import tempfile
import os

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


async def debug_import_data(files: list[UploadFile]):
    validated_netcdf_files = validate_uploaded_netcdf_files(files)

    observation_nc, o_tmp_file_name = await read_netcdf_as_dataset(validated_netcdf_files['observation_data'])
    geolocation_nc, g_tmp_file_name = await read_netcdf_as_dataset(validated_netcdf_files['geolocation_data'])

    print("---- Observation Data - NetCDF file ----")
    print(observation_nc)
    print("\n\n\n")
    print("---- Geolocation Data - NetCDF file ----")
    print(geolocation_nc)

    os.remove(o_tmp_file_name)
    os.remove(g_tmp_file_name)

    observation_nc.close()
    geolocation_nc.close()

    return {
        "observation data": validated_netcdf_files['observation_data'].filename,
        "geolocation data": validated_netcdf_files['geolocation_data'].filename
    }
