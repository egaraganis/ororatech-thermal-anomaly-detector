from fastapi import UploadFile, HTTPException

def validate_netcdf_files(files: list[UploadFile]):
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

def debug_import_data(files: list[UploadFile]):
    validated_netcdf_files = validate_netcdf_files(files)

    return {
        "observation data": validated_netcdf_files['observation_data'].filename,
        "geolocation data": validated_netcdf_files['geolocation_data'].filename
    }
