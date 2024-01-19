from shapely.geometry import shape, mapping
from shapely.validation import explain_validity
from qgis.core import QgsProject

# Para la capa de ríos
capa_rios = QgsProject.instance().mapLayersByName('Rios_Enc(RGC)')[0]
for feature in capa_rios.getFeatures():
    shapely_geometry = shape(mapping(feature.geometry()))
    if not shapely_geometry.is_valid:
        print(f"La geometría de la feature {feature.id()} de la capa de ríos no es válida.")
        print(f"Explicación: {explain_validity(shapely_geometry)}")

# Para la capa de cuencas
capa_cuencas = QgsProject.instance().mapLayersByName('Simplified')[0]
for feature in capa_cuencas.getFeatures():
    shapely_geometry = shape(mapping(feature.geometry()))
    if not shapely_geometry.is_valid:
        print(f"La geometría de la feature {feature.id()} de la capa de cuencas no es válida.")
        print(f"Explicación: {explain_validity(shapely_geometry)}")