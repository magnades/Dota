import requests
from Functions import *

# get_hero_from_id(84)  ## Rubick
# get_item_from_id(235)    ## Octarine Core
#
# get_match_details(8197456312) ## Partida Pro Team Spirit vs Parivision

get_match_details(8107511870)
# get_item_popularity(36)
# get_hero_statistics(36)


hero_id = 74  # ID del héroe
region = 1  # Región de la partida
is_win = True  # Buscar partidas ganadas (True) o perdidas (False)
min_date = '2025-01-01T00:00:00.000Z'  # Fecha mínima (en formato ISO)
lane_role = 2  # Rol de línea del jugador
limit = 200  # Límite de registros a retornar
patch = "7.38"                  # Límite superior para el parche


result = query_custom(hero_id, region, patch, is_win, min_date, lane_role, limit)

print('done')


