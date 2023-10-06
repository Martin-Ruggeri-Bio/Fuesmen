#!/bin/bash

# Verificar que se proporcionó un directorio como argumento
if [ $# -ne 1 ]; then
  echo "Uso: $0 <directorio>"
  exit 1
fi

# Obtener el directorio de origen a partir del argumento
origin_path="$1"

# Iterar a través de las carpetas en el directorio de origen
for dir in "$origin_path"/*/; do
  # Obtener el nombre de la carpeta actual (último elemento del camino)
  dir_name=$(basename "$dir")

  # Construir el camino final
  final_path="$origin_path/$dir_name"

  # Ejecutar el comando dcm2niix para convertir las imágenes
  dcm2niix -f "$dir_name" -p y -z y -o "$final_path" "$final_path"
  bet2 "$final_path/$dir_name"".nii.gz" "$final_path"/brain -o -m -s -e

done

echo "Proceso completado."
