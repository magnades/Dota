from Recommender import DotaHeroRecommender
# from utils.functions import update_hero_images
from Functions import *

#
# # get_hero_from_id(84)  ## Rubick
# # get_item_from_id(235)    ## Octarine Core
# #
# # get_match_details(8197456312) ## Partida Pro Team Spirit vs Parivision
#
# # get_match_details(8107511870)
# # get_item_popularity(26)
#
# # get_hero_statistics(26)
#
#
# hero_id = 74  # ID del héroe
# region = 1  # Región de la partida
# is_win = True  # Buscar partidas ganadas (True) o perdidas (False)
# min_date = '2025-01-01T00:00:00.000Z'  # Fecha mínima (en formato ISO)
# lane_role = 2  # Rol de línea del jugador
# limit = 200  # Límite de registros a retornar
# patch = "7.38"                  # Límite superior para el parche
#
#
# # result = query_custom(hero_id, region, patch, is_win, min_date, lane_role, limit)
#
# # update_matchup_list()
#
recommender = DotaHeroRecommender()
# Supongamos que tenemos a Phantom Lancer (ID 20) como aliado y Anti-Mage (ID 1) como enemigo.
allies = [20]
enemies = [1]
position = 1  # Buscamos un Carry

# recommendations = recommender.recommend_heroes(allies, enemies, position, 5)
# print(f"Recomendaciones para {recommender.positions[position]}:")
# for hero_id in recommendations:
#     hero_name = recommender.hero_data.get(hero_id, {}).get("localized_name", f"ID {hero_id}")
#     print(f"- {hero_name}")



print('done')
steam_id_dict = {
    'Magnades': 98074348,
    'Takenori': 100134035,
    'Leggna': 21366207,
    'Hanamichi': 62733348,
    'Lucifer': 215954950,
    'Rukawa': 82333867,
    'Ryota': 91492101,
    'Vash': 122599950,
}

save_json(steam_id_dict, "players_information.json")


# player_id = steam_id_dict.get('Leggna')
#
# data = get_player_heroes(player_id)

update_players_heroes_strengths()

recommendations = recommender.recommend_heroes_for_player(allies, enemies, position, 'Magnades',5 )


for name, id_player in steam_id_dict.items():
    get_player_information(id_player)


