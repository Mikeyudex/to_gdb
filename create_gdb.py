import arcpy
import base64
import zipfile
import os, shutil
import uuid
from io import BytesIO
import argparse
from arcpy import FeatureClassToGeodatabase_conversion

#Función optimizada para utilizarla como geoproceso de Arcgis PRO
def create_gdb(shp_path, service_name):
    try:
        arcpy.env.workspace = os.getcwd()
        folder_gdb = os.path.join(arcpy.env.workspace, "temp")
        folder_gdb_copy = os.path.join(arcpy.env.workspace, "copy")
        
        arcpy.AddMessage("Folder de la gdb : {}".format(folder_gdb))
        
        if not os.path.exists(folder_gdb):
            os.mkdir(folder_gdb)
        if not os.path.exists(folder_gdb_copy):
            os.mkdir(folder_gdb_copy)
            
        name_gdb = "{}_output_{}.gdb".format(service_name, uuid.uuid4())
        name_gdb_copy = "{}_output_{}_{}.gdb".format(service_name, "copy", uuid.uuid4())
        path_gdb = os.path.join(os.path.abspath(folder_gdb), name_gdb)
        path_gdb_copy = os.path.join(os.path.abspath(folder_gdb_copy), name_gdb_copy)
        arcpy.AddMessage("Path de la gdb : {}".format(path_gdb))
        print("Generando GDB...")
        arcpy.CreateFileGDB_management(folder_gdb, name_gdb, out_version='CURRENT')
        
        print("GDB generada exitosamente...")

        #adjuntar shp a GDB
        print("Importando shp a gdb...")
        response = FeatureClassToGeodatabase_conversion([shp_path], path_gdb)
        if response.status != 4:
            print('Ocurrio un error al realizar la conversion')
            return {"success": False, "file_base64": ""}
        del response
        
        #Copiar Gdb en carpeta copy
        arcpy.AddMessage("Copiando GDB...")
        arcpy.Copy_management(path_gdb, path_gdb_copy)
        
        path_zip = compress_file(os.path.join(folder_gdb_copy, "output_{}.zip".format(uuid.uuid4())), name_gdb_copy, path_gdb_copy, folder_gdb_copy)

        with open(path_zip, "rb") as file:
            zip_data = file.read()
        base64_data = base64.b64encode(zip_data).decode("utf-8")
        deleteAllFiles(folder_gdb)
        deleteAllFiles(folder_gdb_copy)
##        return {"success": True, "file_base64": base64_data}
        arcpy.SetParameter(2, base64_data)
    except arcpy.ExecuteError:
        arcpy.AddMessage("Error: {0}".format(arcpy.GetMessages()))
        print(arcpy.GetMessages())
##        deleteAllFiles("temp")
##        return {
##            "success": False,
##            "file_base64": "",
##            "error": "Ocurrio un error al intentar generar la gdb.",
##        }

def compress_file(zip_path, name_file, file_path, folder_gdb_copy):
    try:
        arcpy.AddMessage("Path recibido para generar zip: {}".format(file_path))
        zip_fle = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(folder_gdb_copy):
            if root == file_path:
                for f in files:
                    #arcpy.AddMessage("root folder: {} - file iterado {}".format(root, f))
                    zip_fle.write(os.path.join(root, f))
        print("Archivo ZIP creado en: " + zip_path)
        arcpy.AddMessage("Archivo ZIP creado en: {}".format(zip_path))
        return zip_path
    except arcpy.ExecuteError:
        arcpy.AddMessage("Error: {0}".format(arcpy.GetMessages()))

def descomprimirZip(file_zip, file_name):
    try:
        folder_temp = 'temp'
        path_file = "{}/{}.zip".format(folder_temp, file_name)
        file_zip.save(path_file)
        with zipfile.ZipFile(path_file, 'r') as zip_ref:
            zip_ref.extractall(folder_temp)
        os.remove(path_file)
        return 
    except Exception as e:
        print(e)
        return e
    
  
def deleteAllFiles(dir):
    print('Eliminando todos los archivos de la carpeta {}'.format(dir))
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)
    print('Archivos removidos correctamente de la carpeta {}'.format(dir))


def processBase64(base64_file, name_file):
    try:
        # Decodificar el archivo Base64 a un objeto de tipo Buffer
        archivo_buffer = BytesIO(base64.b64decode(base64_file))
        path_file = "temp/{}.zip".format(name_file)
        # Guardar el archivo en disco
        archivo_buffer.seek(0)  # Reiniciar el puntero del buffer al principio
        archivo_buffer.save(path_file)
        with open(path_file, "rb") as file:
            file_data = file.read()
        return file_data
    except Exception as e:
        print(e)
        return e

#create_gdb("temp/pozos.shp", "pozos")
##def run():
##    with daemon.DaemonContext():
##        if __name__ == "__main__":
##            param0 = arcpy.GetParameterAsText(0)
##            param1 = arcpy.GetParameterAsText(1)
##            parser = argparse.ArgumentParser()
##            parser.add_argument("arg1", type=str, help="shp path")
##            parser.add_argument("arg2", type=int, help="nombre del feature service")
##            args = parser.parse_args()
##            create_gdb(param0, param1)

if __name__ == '__main__':    
    param0 = arcpy.GetParameterAsText(0)
    param1 = arcpy.GetParameterAsText(1)
    arcpy.AddMessage("Param1: {0} Param2: {1}.".format(str(param0), str(param1)))
    create_gdb(param0, param1)
