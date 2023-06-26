import os, shutil


def deleteAllFiles(dir):
    print(f'Eliminando todos los archivos de la carpeta {dir}')
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)
    print(f'Archivos removidos correctamente de la carpeta {dir}')