homepage = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OroraTech Assesement</title>
    <style>
        body {
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #13212c;
        }

        input[type="file"] {
            margin-top: 20px;
            margin-bottom: 20px;
            padding: 10px;
            border: 1px solid #D11F38;
            border-radius: 5px;
            width: 100%;
            color: white;
        }

        input[type="submit"] {
            padding: 10px 20px;
            background-color: #D11F38;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
        }

    </style>
</head>
<body>
    <div>
        <img src="https://ororatech.com/wp-content/uploads/2021/12/orora_logo.svg" alt="Orota Tech Logo">
        <form action="/detect_thermal_anomalies/" enctype="multipart/form-data" method="post">
            <input name="files" type="file" accept="application/x-netcdf" multiple id="fileInput">
            <input type="submit" value="Upload Satellite Overpass Files">
        </form>
    </div>
</body>
</html>
"""