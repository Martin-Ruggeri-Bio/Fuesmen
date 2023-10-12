from zipfile import ZipFile
from mayo_code_v1 import mayo
import pydicom
import os
from pydicom import dcmread


path_origen = "/home/daniel/Documents/Pacientes_Neuro/descargas"
path_destino = "/home/daniel/Documents/Pacientes_Neuro/test_unzip"

for archivo in os.listdir(path_origen):
    path_file = os.path.join(path_origen , archivo)
    print(path_file)
    with ZipFile(path_file,'r') as estudio:
        estudio.extractall(path=path_destino)
        print("descomprimido")
    
    mayo(path_destino)







# fileNames = []
# destino = "./test_unzip"


# with ZipFile(f"./descargas/{fileNames}",'r') as estudio:
#     estudio.extractall(path=destino)
#     print("descomprimido")

# mayo(destino)

# ds = dcmread("./test_unzip/96205358/20230520/na/ax_dti-16/MR.1.2.840.113619.2.363.10499743.3637646.25026.1684513445.969.1.dcm")
# for element in ds:
#     print(element)