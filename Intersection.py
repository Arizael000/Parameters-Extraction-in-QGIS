import processing
from qgis.core import QgsGeometry
from qgis.core import QgsFeature, QgsField, QgsVectorDataProvider
from shapely.geometry import shape, mapping
import uuid

# Obtén todas las capas
capasTODAS = QgsProject.instance().mapLayers().values()
# OBTENER CAPA DE CUENCAS
palabras_claveC = ['cuencas', 'cuenca', 'basins', 'basin']
capa_cuencas = None
for capa in capasTODAS:
    nombre_capa = capa.name().lower()
    if any(palabra in nombre_capa for palabra in palabras_claveC):
        capa_cuencas = capa
        print("La capa de cuencas es: " + capa_cuencas.name())
        break
# OBTENER CAPA DE RIOS
palabras_claveR = ['rios', 'ríos', 'cauces', 'rivers', 'streams']
capa_rios = None
for capa in capasTODAS:
    nombre_capa = capa.name().lower()
    if any(palabra in nombre_capa for palabra in palabras_claveR):
        capa_rios = capa
        print("La capa de ríos es: " + capa_rios.name())
        break

# Verifica que las capas se hayan cargado correctamente
if not capa_cuencas or not capa_rios:
    print("Error al cargar las capas.")
else:
    # Crear una capa vectorial en memoria para el resultado
    result_layer_path = 'C:/QGIS_ShapeFile/output/layers/result_' + str(uuid.uuid4()) + '.shp'
    result_layer = QgsVectorLayer('Polygon?crs=epsg:4326', 'ResultLayer', 'memory')
    # Verificar si la capa es editable y, si no lo es, iniciar la edición
    if not capa_cuencas.isEditable():
        capa_cuencas.startEditing()
    
    # Crear una lista para almacenar las features actualizadas
    features_actualizadas = []

    # Simplificar geometrías no válidas en la capa de cuencas
    for feature in capa_cuencas.getFeatures():
        original_geometry = feature.geometry()
        shapely_geometry = shape(mapping(original_geometry))

        if not shapely_geometry.is_valid:
            print(f"La geometría de la feature {feature.id()} de la capa de cuencas no es válida.")
            print(f"Explicación: {explain_validity(shapely_geometry)}")

            # Crear una copia de la feature para modificarla
            feature_auxiliar = QgsFeature(feature)

            # Simplificar la geometría de la copia
            simplified_geometry = QgsGeometry.fromWkt(shapely_geometry.simplify(0.1).to_wkt())
            feature_auxiliar.setGeometry(simplified_geometry)

            # Agregar la feature actualizada a la lista
            features_actualizadas.append(feature_auxiliar)

            # Eliminar la feature original
            capa_cuencas.deleteFeature(feature.id())

    # Agregar las features actualizadas a la capa
    capa_cuencas.addFeatures(features_actualizadas)
    
    # Finalizar la edición después de realizar todas las actualizaciones
    capa_cuencas.commitChanges()
    with edit(capa_cuencas):
            for feature in capa_cuencas.getFeatures():
               # Aplicar un buffer pequeño de 0.000001 unidades
                original_geometry = feature.geometry()
                buffered_geometry = original_geometry.buffer(0.000001, 5)
                feature.setGeometry(buffered_geometry)
                capa_cuencas.updateFeature(feature)

    # Verificar la validez después de la simplificación
    for feature in capa_cuencas.getFeatures():
        shapely_geometry = shape(mapping(feature.geometry()))
        if not shapely_geometry.is_valid:
            print(f"La geometría de la feature {feature.id()} de la capa de cuencas no es válida después de la simplificación y buffer.")
            print(f"Explicación: {explain_validity(shapely_geometry)}")

     # Continuar con el código original para la operación de intersección
    algorithm_params = {
        'INPUT': capa_rios.source(),
        'OVERLAY': capa_cuencas,
        'OUTPUT': 'memory:',
    }
    
    try:
        algorithm_output = processing.run(
            "qgis:intersection",
            algorithm_params
        )
    except Exception as e:
        print("Error durante la ejecución del algoritmo:")
        print(str(e))
        if 'algorithm_output' in locals():
            print("Mensaje de advertencia:", algorithm_output['log'])
        else:
            print("No hay logs")
    
    # Obtener la capa resultante en memoria
    result_layer = algorithm_output['OUTPUT']
    
    # Cargar el resultado en la capa vectorial en memoria
    result_layer.loadNamedStyle("path/to/your/style.qml")  # Opcional: cargar un estilo predefinido
    result_layer.setCrs(capa_rios.crs())
    
    # Obtener los campos de la capa de ríos
    campos_rios = capa_rios.fields()
    
    # Definir los campos de la nueva capa resultante
    result_layer.dataProvider().addAttributes(campos_rios)
    
    # Actualizar los campos de la nueva capa
    result_layer.updateFields()
    
    # Eliminar features que no sean segmentos de ríos
    with edit(result_layer):
        for feature in result_layer.getFeatures():
            # Obtener la geometría de la feature de la capa de cuencas correspondiente
            cuenca_geometry = None
            for cuenca_feature in capa_cuencas.getFeatures():
                if feature.geometry().intersects(cuenca_feature.geometry()):
                    cuenca_geometry = cuenca_feature.geometry()
                    break
                
            # Si se encuentra la geometría de la cuenca, eliminar la feature si no es un segmento de río
            if cuenca_geometry:
                if not feature.geometry().intersects(cuenca_geometry):
                    result_layer.deleteFeature(feature.id())
    
    # Agregar la capa resultante como capa temporal en memoria
    QgsProject.instance().addMapLayer(result_layer)
    print("Operación de intersección completada. Resultados en una capa temporal en memoria.")


#    # Obtén la feature que deseas editar (por ejemplo, la feature con ID 11)
#    feature_id_to_edit = 54
#    feature_auxiliar = None
#
#    # Guarda la geometría original en la variable auxiliar
#    for feature in capa_cuencas.getFeatures():
#        if feature.id() == feature_id_to_edit:
#            feature_auxiliar = QgsFeature(feature)
#            break
#
#    # Elimina la feature original
#    capa_cuencas.startEditing()
#    capa_cuencas.deleteFeature(feature_id_to_edit)
#    capa_cuencas.commitChanges()
#
#    # Simplifica la geometría auxiliar
#    if feature_auxiliar is not None:
#        geometry = feature_auxiliar.geometry()
#        simplified_geometry = QgsGeometry.fromWkt(geometry.asWkt()).simplify(0.1)  # Ajusta el factor de simplificación según sea necesario
#        feature_auxiliar.setGeometry(simplified_geometry)
#
#        # Agrega la geometría auxiliar simplificada a la capa
#        capa_cuencas.startEditing()
#        capa_cuencas.addFeature(feature_auxiliar)
#        capa_cuencas.commitChanges()