# First select the active vectorial layer
layer = iface.activeLayer()
features = layer.getFeatures()

pr = layer.dataProvider()  # need to create a data provider

# Obtener los nombres de los campos
nombres_campos = [field.name() for field in layer.fields()]

# Nombre de los campos a comprobar
nombre_campoA = "NuevaArea"
nombre_campoP = "NuevoPerim"
nombre_CampoKc = "IndiceComp"
nombre_CampoLC = "LongCuenca"

# Comprobar los campos existen y si no crearlos
if nombre_campoA not in nombres_campos:
    field = QgsField(nombre_campoA, QVariant.Double)
    field.setPrecision(3)
    field.setLength(20)  # Definir la longitud del campo
    pr.addAttributes([field])

if nombre_campoP not in nombres_campos:
    field = QgsField(nombre_campoP, QVariant.Double)
    field.setPrecision(3)
    field.setLength(20)
    pr.addAttributes([field])

if nombre_CampoKc not in nombres_campos:
    field = QgsField(nombre_CampoKc, QVariant.Double)
    field.setPrecision(3)
    field.setLength(10)
    pr.addAttributes([field])

layer.updateFields()  # tell the vector layer to fetch changes from the provider

# Obtener los índices de los campos
idArea = layer.fields().indexFromName('NuevaArea')
idPerim = layer.fields().indexFromName('NuevoPerim')
idIcomp = layer.fields().indexFromName('IndiceComp')
layer.startEditing()

# Iterar sobre las features
for feature in features:
    geom = feature.geometry()
    geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
    if geom.type() == QgsWkbTypes.PolygonGeometry:
        if geomSingleType:
            x = geom.asPolygon()
            print("Polygon: ", x, "Area: ", geom.area(), "Perimeter:", geom.length())
            area_value = geom.area()
            length_value = geom.length()
            indice_compacidad = 0.28 * (length_value / (area_value**0.5))
            # Actualizar los campos
            layer.changeAttributeValue(feature.id(), idArea, area_value)  # Area
            layer.changeAttributeValue(feature.id(), idPerim, length_value)  # Perimetro
            layer.changeAttributeValue(feature.id(), idIcomp, indice_compacidad)  # Indice de Compacidad
        else:
            x = geom.asMultiPolygon()
            print("MultiPolygon: ", "Area: ", geom.area(), "Perimeter:", geom.length())
            area_value = geom.area()
            length_value = geom.length()
            indice_compacidad = 0.28 * (length_value / (area_value**0.5))
            print("Indice de compacidad:", indice_compacidad)
            # Actualizar los campos
            layer.changeAttributeValue(feature.id(), idArea, area_value)  # Area
            layer.changeAttributeValue(feature.id(), idPerim, length_value)  # Perimetro
            layer.changeAttributeValue(feature.id(), idIcomp, indice_compacidad)  # Indice de Compacidad

# Guardar los cambios si la capa está en modo de edición
if layer.isEditable():
    layer.commitChanges()
