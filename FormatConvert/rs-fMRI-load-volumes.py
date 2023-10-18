import os


def load_rsn_volumes(dialog,rsn_paths,tresh_value):
	max_values=[]
	for i in rsn_paths:
		#load volume i
		print('-- Subiendo: '+i)
		slicer.util.loadVolume(i)

		#get name of current node
		node_name = os.path.basename(i).split('.')[0]
		current_node=slicer.util.getNode(node_name)

		#get max_value of current volume
		max_value=round(current_node.GetImageData().GetScalarRange()[1])
		max_values.append(max_value)

		#calculate window/level values
		window=max_value-tresh_value
		level=round((max_value+tresh_value)*0.5)

		#configurate visualization of current volume
		display_node=current_node.GetDisplayNode()
		current_node.GetDisplayNode()
		display_node.ApplyThresholdOn()
		display_node.SetLowerThreshold(tresh_value)
		display_node.SetAndObserveColorNodeID('vtkMRMLColorTableNodeIron') #Color predefinido en Iron, evaluar si se requiere otro
		display_node.AutoWindowLevelOff()
		display_node.SetWindow(window)
		display_node.SetLevel(level)
	return current_node, max_values
		
#Valor predeterminado del umbral, evaluar el caso de que no se ponga ningun valor umbral.
tresh=4
#Inicializamos los cuadros de mensajes
b=qt.QMessageBox()
b.setText('Esta ejecutando el script rs-fMRI-process.py\n Suba la referencia anatómica (wT1.nii o wT1.nii.gz)')
b.exec()
a=qt.QFileDialog()

#GUI para pedir ruta de wT1
wT1_path=a.getOpenFileName(a,'Seleccione la referencia anatómica(wT1.nii o wT1.nii.gz)')
slicer.util.loadVolume(wT1_path)
node_name = os.path.basename(wT1_path).split('.')[0]
wT1_node=slicer.util.getNode(node_name)


#GUI para pedir ruta de vols NIfTI
b.setText('Seleccione los vols*.nii.gz que desee analizar')
b.exec()
rsn_paths=a.getOpenFileNames(a,'Seleccione los vols*.nii.gz que desee analizar')
current_node, max_values=load_rsn_volumes(a,rsn_paths,tresh)

slicer.util.setSliceViewerLayers(background=wT1_node, foreground=current_node,foregroundOpacity=1)
melodicIC_path=os.path.dirname(wT1_path)+'/ICA.ica/filtered_func_data.ica/melodic_IC.nii.gz'

#### parte fsleyes, aun queda evaluar.
#--- aqui viene la parte fsleyes.
####
#print('fsleyes --scene melodic --displaySpace '+melodicIC_path+' --nrows 2 --ncols 4 --movieSync '+wT1_path+' --interpolation linear '+melodicIC_path +' --cmap red-yellow --interpolation linear --displayRange '+str(tresh)+' '+str(max(max_values)))
#os.system('fsleyes --scene melodic --displaySpace '+melodicIC_path+' --nrows 2 --ncols 4 --movieSync '+wT1_path+' --interpolation linear '+melodicIC_path +' --cmap red-yellow --interpolation linear --displayRange '+str(tresh)+' '+str(max(max_values))+' &')


b.setText('Se ha ejecutado el proceso correctamente. \n Puede comenzar a clasificar RSNs')
b.exec()
