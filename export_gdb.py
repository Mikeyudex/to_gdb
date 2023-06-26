from export_shp import to_shp
from configs import URL_GEOPROCESO_REST
import certifi
import urllib3
import uuid
from urllib.parse import quote, urlencode
from upload_file import upload_file

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
                    gdb_base64 = data['results'][0]['value']
                    response_file = upload_file(gdb_base64, f"{service_name}_{uuid.uuid4()}", ".zip")
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
         
        
""" to_gdb(
    "https://arcgis-pliga-dev.is.arqbs.com/arcgis/rest/services/PIGA/PIGA_ALL_GEODB/MapServer/0/query",
    "pozos",
    "EPSG:4326"
)  """
