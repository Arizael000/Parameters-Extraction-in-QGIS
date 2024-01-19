from PIL import Image
from PyQt5.QtGui import QImage, QPixmap
from qgis.core import QgsRasterLayer, QgsProject

# Obtén la capa raster activa en QGIS
layer = iface.activeLayer()

# Verifica que la capa sea de tipo raster
if isinstance(layer, QgsRasterLayer):
    # Obtén la ruta al archivo raster
    raster_path = layer.source()

    # Carga la imagen raster con Pillow
    image = Image.open(raster_path)

    # Realiza alguna operación en la imagen, por ejemplo, cambiar los colores
    # Aquí, simplemente convertiremos la imagen a escala de grises
    image = image.convert("L")

    # Guarda la imagen en la carpeta temporal
    temp_path = 'D:/Temporal/image.png'
    image.save(temp_path)
    image.show()
    # Actualiza la capa raster en QGIS con la nueva imagen
    new_layer = QgsRasterLayer(temp_path, 'Modified Raster')
    new_layer.setCrs(QgsCoordinateReferenceSystem('EPSG:4326 - WGS 84'))
    QgsProject.instance().removeMapLayer(layer.id())
    QgsProject.instance().addMapLayer(new_layer)

    # Refresca la interfaz de usuario
    iface.mapCanvas().refreshAllLayers()

    # No es necesario limpiar la imagen temporal en este caso


