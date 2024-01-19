# Obtener todas las capas cargadas en el proyecto
capasRios = QgsProject.instance().mapLayers().values()
# Con esta lista establezco las palabras claves en el nombre de las capas
palabras_clave = ['rios', 'ríos', 'cauces', 'rivers', 'streams']



layer= None

for capa in capasRios:
    # Obtener el nombre de la capa en minúsculas para hacer la búsqueda sin distinción entre mayúsculas y minúsculas
    nombre_capa = capa.name().lower()
    
    # Verificar si alguna palabra clave está presente en el nombre de la capa
    if any(palabra in nombre_capa for palabra in palabras_clave):
        layer = capa
        break

if layer:
    print(f"Capa seleccionada: {layer.name()}")
    print("The lenght of the layer's rivers in selected layer are: ")
    features = layer.getFeatures()
    pr = layer.dataProvider()  # need to create a data provider

    # Obtener los nombres de los campos
    nombreLongCauce="LongCauce"
    nombres_campos = [field.name() for field in layer.fields()]
    # Comprobar si el campo existe y si no crearlo
    if nombreLongCauce not in nombres_campos:
        field = QgsField(nombreLongCauce, QVariant.Double)
        field.setPrecision(3)
        field.setLength(20)  # Definir la longitud del campo
        pr.addAttributes([field])
    layer.updateFields()
    idLCauce= layer.fields().indexFromName(nombreLongCauce)
    layer.startEditing()
    #Iterar sobre las features en busca de los ríos que se represetan como lineas
    for feature in features:
        geom= feature.geometry()   
        geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
        if geom.type() ==  QgsWkbTypes.LineGeometry:
            if geomSingleType:
                x = geom.asPolyline()
                print("Line: ", x, "length: ", geom.length())
                #Actualizar campo
                layer.changeAttributeValue(feature.id(), idLCauce, longCauce)
            else:
                x = geom.asMultiPolyline()
                print("MultiLine: ", x, "length: ", geom.length())
                longCauce= geom.length()
                #Actualizar campo
                layer.changeAttributeValue(feature.id(), idLCauce, longCauce)
# Guardar los cambios si la capa está en modo de edición
if layer.isEditable():
    layer.commitChanges()
