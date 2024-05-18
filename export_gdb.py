import base64
import os
from export_shp import to_shp
from configs import URL_GEOPROCESO_REST
import certifi
import urllib3
import uuid
import zipfile
from urllib.parse import quote, urlencode
from upload_file import upload_file
from logger_setup import logger

def to_gdb(url_service: str, service_name: str, project: str):
    # URL del Feature Service
    try:
        print(f'Generando archivo SHP...')
        response_toshp = to_shp(url_service, service_name, project)
        print(f'SHP generado exitosamente...')
        response_togdb = request_service_create_gdb(service_name, response_toshp['response'])
        return response_togdb
    except Exception as e:
            print(e)
            return {"success": False, "message": "Proceso terminado con errores"}
    
def request_service_create_gdb(service_name:str, path_shp:str):
    try:
        encoded_args = urlencode({"param0": quote(path_shp), "param1": service_name, "returnFeatureCollection": "false", "f": "pjson" })

        http = urllib3.PoolManager(
            cert_reqs="CERT_NONE",
            ca_certs=certifi.where()
        )
        print(f"Enviando petición a geoproceso {URL_GEOPROCESO_REST}?{encoded_args}")
        response = http.request(
            "POST",
            f"{URL_GEOPROCESO_REST}?{encoded_args}",
            headers={"Content-Type": "application/json"}
        )
        if response.status == 200:
            data = response.json()
            
            if "results" in data:
                if "value" in data['results'][0]:
                    path_gdb = data['results'][0]['value']
                    tmp_folder = "temp"
                    name_file_zip = "{}_outputgdb_{}.zip".format(service_name, uuid.uuid4())
                    zip_path = os.path.join(tmp_folder, name_file_zip)
                    folder_gdb = os.path.dirname(path_gdb)
                    compress_file(zip_path=zip_path, file_path=path_gdb, folder_gdb=folder_gdb)
                    with open(zip_path, "rb") as file:
                        zip_data = file.read()
                    base64_data = base64.b64encode(zip_data).decode("utf-8")
                    response_file = upload_file(base64_data, name_file_zip)
                    return response_file
                else:
                    return {"success": False, "url_file": "", "error": "error al intentar crear GDB."}
            else:
                return {"success": False, "url_file": "", "error": "error al intentar crear GDB."}
        else:
            return {"success": False, "url_file": "", "error": response.data}
        
    except Exception as e:
        print(e)
        return {"success": False, "url_file": "", "error": "Error : error al invocar geoproceso."}


def compress_file(zip_path, file_path, folder_gdb)-> str:
    try:
        logger.info('Path recibido para generar zip: {}'.format(file_path))
        zip_fle = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(folder_gdb):
            if root == file_path:
                for f in files:
                    #arcpy.AddMessage("root folder: {} - file iterado {}".format(root, f))
                    zip_fle.write(os.path.join(root, f))
        logger.info("Archivo ZIP creado en: {}".format(zip_path))
        return zip_path
    except Exception as e:
        logger.error("Error: {}".format(e))


""" to_gdb(
    "https://arcgis-pliga-dev.is.arqbs.com/arcgis/rest/services/PIGA/PIGA_ALL_GEODB/MapServer/0/query",
    "pozos",
    "EPSG:4326"
)  """
