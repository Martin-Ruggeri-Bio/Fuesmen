import os
import pydicom
import nibabel as nib
from os import getenv
from dotenv import load_dotenv


#obtener variables de entorno
load_dotenv() # Get env variables

# Ruta de la carpeta DICOM
carpeta_dicom = getenv('DICOM')

# Carpeta de salida para los archivos NIfTI
carpeta_nifti = getenv('NifTI')


# Función para convertir una serie DICOM a NIfTI
def convertir_dicom_a_nifti(serie_dicom, carpeta_paciente_nifti, nombre_estudio):
    try:
        # Crear una lista de objetos DICOM
        dicom_files = [pydicom.dcmread(os.path.join(serie_dicom, archivo)) for archivo in os.listdir(serie_dicom)]
        
        # Comprobar si hay archivos DICOM válidos en la serie
        if not any(dicom_files):
            print(f"No se encontraron archivos DICOM válidos en {serie_dicom}")
            return False

        # Obtener información de píxeles y metadatos del primer archivo DICOM
        primera_imagen = dicom_files[0]
        pixel_array = primera_imagen.pixel_array
        # verificar si la orientacion esta definida
        orientacion = None

        # Crear una imagen NIfTI
        imagen_nifti = nib.Nifti1Image(pixel_array, orientacion)

        # Generar un nombre de archivo único
        nombre_archivo = f"{nombre_estudio}.nii.gz"

        # Guardar la imagen en formato NIfTI
        nib.save(imagen_nifti, os.path.join(carpeta_paciente_nifti, nombre_archivo))
        return True
    except Exception as e:
        print(f"Error al convertir {serie_dicom} a NIfTI: {str(e)}")
        return False

# Recorre las carpetas de pacientes y estudios
for paciente in os.listdir(carpeta_dicom):
    carpeta_paciente = os.path.join(carpeta_dicom, paciente)
    # Crear la carpeta del paciente en la carpeta de salida
    carpeta_paciente_nifti = os.path.join(carpeta_nifti, paciente)
    os.makedirs(carpeta_paciente_nifti, exist_ok=True)
    if os.path.isdir(carpeta_paciente):
        for estudio in os.listdir(carpeta_paciente):
            carpeta_estudio = os.path.join(carpeta_paciente, estudio)
            if os.path.isdir(carpeta_estudio):
                # Convertir las imágenes DICOM a NIfTI y guardarlas en la carpeta del paciente de nifti
                convertir_dicom_a_nifti(carpeta_estudio, carpeta_paciente_nifti, estudio)