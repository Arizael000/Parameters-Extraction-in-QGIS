import processing

# Obtén la capa vectorial o geometría que deseas verificar
# En este ejemplo, asumiré que tienes una capa llamada 'capa_cuencas' con geometrías de polígonos
nombre_capa = 'Cuencas_Enc'
capa_cuencas = QgsProject.instance().mapLayersByName(nombre_capa)[0]

# Configura los parámetros para el algoritmo "Check validity"
params = {
    'INPUT_LAYER': capa_cuencas,
    'METHOD': 0,  # 0 para validar la geometría
    'OUTPUT': 'memory:'
}
feedback = QgsProcessingFeedback()
# Ejecuta el algoritmo "Check validity"
resultado = processing.run("qgis:checkvalidity", params, feedback=feedback)
print("Para la capa: ",nombre_capa,resultado)
## Verifica si la validación fue exitosa
#for msg in feedback.getFeedback():
#    print(msg)
