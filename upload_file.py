import urllib3
import certifi
import json
from configs import URL_SERVICE_S3

def upload_file(file_base64: str, filename: str):
    try:
        params = {
            "namespace": "arqocidevsqadem",
            "bucketName": "pliga-bucket",
            "fileName": filename,
            "phoenix": True,
            "urlExpirationTimeHours": "24",
            "fileBase64": file_base64,
        }
        # Realizar petición a servicio web externo
        print("Subiendo archivo a s3...")

        http = urllib3.PoolManager(
            cert_reqs="CERT_NONE",
            ca_certs=certifi.where()
        )
        r = http.request(
            "POST",
            URL_SERVICE_S3,
            body=json.dumps(params),
            headers={"Content-Type": "application/json"}
        )
        
        if r.status == 200:
            # Convertir la respuesta a un GeoDataFrame
            data = r.json()
            if "accessUri" in data:
                print("Archivo cargado en s3 exitosamente.")
                return {"success": True, "url_file": data["accessUri"]}
        else:
            return {"success": False, "url_file": "", "error": r.data}
    except Exception as e:
        print(e)
        return {
            "success": False,
            "url_file": "",
            "error": "Ocurrió un error al intentar subir archivo en S3."
        }
