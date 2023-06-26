import geopandas as gpd
import requests
import json
import os


def to_shp(url_service: str, service_name: str, project: str):
    # URL del Feature Service
    url = url_service
    service_name = service_name

    if not url.endswith("/query"):
        url = f"{url}/query"

    # Parámetros de la consulta
    params = {
        "where": "1=1",  # Esto selecciona todos los registros
        "outFields": "*",  # Esto selecciona todos los campos
        "returnGeometry": "true",  # Esto asegura que la geometría esté incluida
        "f": "geojson",  # El formato de salida
        "resultOffset": 0,  # Desplazamiento inicial
        "resultRecordCount": 1000,  # Cantidad de registros por página
    }

    all_features = []  # Lista para almacenar todos los registros

    while True:
        try:
            # Realizar la consulta
            r = requests.get(url, params=params)
            # Convertir la respuesta a un GeoDataFrame
            data = json.loads(r.content)
            # Obtener los registros de la página actual
            features = data["features"]
            # Agregar los registros a la lista
            all_features.extend(features)
            # Verificar si hay más registros para recuperar
            if len(features) < params["resultRecordCount"]:
                break
            # Actualizar el desplazamiento para obtener la siguiente página
            params["resultOffset"] += params["resultRecordCount"]
        except Exception as e:
            print(e)

    try:
        print(f"Total de registros a procesar {len(all_features)}")
        gdf = gpd.GeoDataFrame.from_features(all_features)

        crs = "EPSG:4326" if project == None else project

        gdf.crs = crs

        # Acortar los nombres de columna si exceden los 10 caracteres
        #gdf = gdf.rename(columns=lambda x: f"{x}_p" if x == 'ENABLED' else x )

        output_folder = "temp"
        name_file = f"{service_name}.shp"
        output_shp =  os.path.join(os.path.abspath(output_folder), name_file)
        
        # Guardar el GeoDataFrame como un shapefile
        gdf.to_file(output_shp, crs=crs, driver='ESRI Shapefile')
        print(f"Ruta absoluta de shp generado: {output_shp}")

        return {"success": True, "response": output_shp}
        
    except Exception as e:
        print(e)
        return {"success": False, "message": "Proceso terminado con errores"}
