# Esri start of added imports
import sys, os, arcpy
# Esri end of added imports
# Esri start of added variables
g_ESRI_variable_3 = '/home/opc/arcgis/server/usr/directories/arcgissystem/arcgisinput/PIGA_GP/GpcreateGDB.GPServer/extracted/p30/temp'
g_ESRI_variable_2 = '/home/opc/arcgis/server/usr/directories/arcgissystem/arcgisinput/PIGA_GP/GpcreateGDB.GPServer/extracted/p30/copy'
# Esri end of added variables
import arcpy
import os
import uuid
from arcpy import FeatureClassToGeodatabase_conversion


def create_gdb(shp_path, service_name):
    try:
        arcpy.env.workspace = os.getcwd()
        folder_gdb = os.path.join(arcpy.env.workspace, g_ESRI_variable_3)
        folder_gdb_copy = os.path.join(arcpy.env.workspace, g_ESRI_variable_2)
        
        arcpy.AddMessage("Folder de la gdb : {}".format(folder_gdb))
        
        if not os.path.exists(folder_gdb):
            os.mkdir(folder_gdb)
        if not os.path.exists(folder_gdb_copy):
            os.mkdir(folder_gdb_copy)
            
        name_gdb = "{}_output_{}.gdb".format(service_name, uuid.uuid4())
        #name_gdb_copy = "{}_output_copy_{}.gdb".format(service_name, uuid.uuid4())
        path_gdb = os.path.join(os.path.abspath(folder_gdb), name_gdb)
        #path_gdb_copy = os.path.join(os.path.abspath(folder_gdb_copy), name_gdb_copy)
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
        arcpy.SetParameter(2, path_gdb)
    except arcpy.ExecuteError:
        arcpy.AddMessage("Error: {0}".format(arcpy.GetMessages()))
        print(arcpy.GetMessages())
 

if __name__ == '__main__':    
    param0 = arcpy.GetParameterAsText(0)
    param1 = arcpy.GetParameterAsText(1)
    arcpy.AddMessage("Param0: {0} Param1: {1}.".format(str(param0), str(param1)))
    create_gdb(param0, param1)
