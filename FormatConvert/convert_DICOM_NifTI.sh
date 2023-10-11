#!/bin/bash

# Verificar que se proporcionó un directorio como argumento
if [ $# -ne 1 ]; then
  echo "Uso: $0 <directorio>"
  exit 1
fi

# Obtener el directorio de origen a partir del argumento
origin_path="$1"

# Obtener la lista de carpetas en el directorio de origen
folders=("$origin_path"/*/)

# Calcular el número total de puntos de progreso
total_folders="${#folders[@]}"
total_points=$((total_folders * 3))  # 3 comandos por cada carpeta

# Inicializar la variable de progreso
progress=0

# Función para imprimir una barra de carga
show_progress() {
  local current=$1
  local total=$2
  local progress=$((current * 100 / total))
  local bar_length=$((progress / 2))
  local spaces=$((50 - bar_length))

  printf "["
  for ((i = 0; i < bar_length; i++)); do
    printf "="
  done

  for ((i = 0; i < spaces; i++)); do
    printf " "
  done

  printf "] %d%%\r" "$progress"
}


# Iterar a través de las carpetas en el directorio de origen
for dir in "$origin_path"/*/; do
  # Obtener el nombre de la carpeta actual (último elemento del camino)
  dir_name=$(basename "$dir")

  # Construir el camino final
  final_path="$origin_path/$dir_name"

  # Ejecutar el comando dcm2niix para convertir las imágenes
  dcm2niix -f "$dir_name" -p y -z y -o "$final_path" "$final_path"
  ((progress++))
  show_progress "$progress" "$total_points"
  
  bet2 "$final_path/$dir_name"".nii.gz" "$final_path"/brain -o -m -s -e
  ((progress++))
  show_progress "$progress" "$total_points"

  fast -g "$final_path/brain.nii.gz"
  ((progress++))
  show_progress "$progress" "$total_points"

  echo "Proceso completado para $final_path"
done

echo "Proceso completado."