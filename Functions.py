import requests


def update_item_list():

    import json

    # URL del endpoint de ítems de OpenDota
    url = "https://api.opendota.com/api/constants/items"

    try:
        # Realizar la solicitud GET
        response = requests.get(url)
        response.raise_for_status()  # Verificar si hubo errores en la solicitud

        # Convertir la respuesta a formato JSON
        items = response.json()
        print(items)

        # Iterar sobre los ítems y mostrar información básica
        print("Lista de ítems:")
        for item_name, item_details in items.items():
            print(f"Nombre interno: {item_name}")
            print(f"  id: {item_details.get('id', 'N/A')}")
            print(f"  Nombre visible: {item_details.get('dname', 'N/A')}")
            print(f"  Costo: {item_details.get('cost', 'N/A')}")
            print(f"  Descripción: {item_details.get('description', 'N/A')}")
            print("-" * 40)

        save_json(items, "items.json")# Guardar la variable 'items' en un archivo JSON

        print("Datos guardados en items.json.")
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")

def update_item_images():
    import os

    items = load_json("items.json")

    # Base URL para construir la URL completa de la imagen
    base_image_url = "https://cdn.cloudflare.steamstatic.com"

    # Crear un directorio para guardar las imágenes (si no existe)
    os.makedirs("item_images", exist_ok=True)

    # Iterar sobre los ítems y mostrar información básica + descargar imágenes
    print("Lista de ítems y descarga de imágenes:")
    for item_name, item_details in items.items():
        dname = item_details.get("dname", "N/A")
        cost = item_details.get("cost", "N/A")
        # description = item_details.get("description", "N/A")
        print(f"Nombre interno: {item_name}")
        print(f"  Nombre visible: {dname}")
        print(f"  Costo: {cost}")
        # print(f"  Descripción: {description}")

        # Si existe la clave 'img', construir la URL y descargar la imagen
        img_path = item_details.get("img")
        if img_path:
            # Construir la URL completa de la imagen
            full_img_url = base_image_url + img_path
            try:
                img_response = requests.get(full_img_url, stream=True)
                img_response.raise_for_status()
                # Definir el path para guardar la imagen (puedes ajustar la extensión si es necesario)
                image_file = os.path.join("item_images", f"{item_name}.png")
                with open(image_file, "wb") as f:
                    for chunk in img_response.iter_content(1024):
                        f.write(chunk)
                print(f"  Imagen descargada y guardada en: {image_file}")
            except requests.exceptions.RequestException as e:
                print(f"  Error al descargar la imagen de {item_name}: {e}")
        else:
            print("  No se encontró imagen para este ítem.")

        print("-" * 40)

def load_json(filename: str):
    import json

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"El archivo '{filename}' no existe.")
        data = None

    return data

def save_json(data, filename: str):
    import json

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error al guardar el archivo '{filename}': {e}")


def get_item_from_id(item_id: int):
    items = load_json("items.json")
    for item_name, item_details in items.items():
        if item_details.get("id") == item_id:
            # print(f'Item encontrado: {item_name}')
            return item_name, item_details
    return None, None

def get_hero_from_id(hero_id: int):
    heroes = load_json("heroes.json")
    for hero_name, hero_details in heroes.items():
        if hero_details.get("id") == hero_id:
            # print(f'Heroe encontrado: {hero_name}')
            return hero_name, hero_details

    return None, None


def update_hero_list():
    # URL del endpoint de héroes de OpenDota
    url = "https://api.opendota.com/api/heroes"

    try:
        # Realizar la solicitud GET
        response = requests.get(url)
        response.raise_for_status()  # Verificar si hubo errores en la solicitud

        # Convertir la respuesta a formato JSON
        heroes = response.json()
        heroes_dict = {}
        for hero_details in heroes:
            name = hero_details.get('localized_name', 'N/A')
            heroes_dict[name] = hero_details
            print(f"Nombre interno: {hero_details.get('localized_name', 'N/A')}")
            print(f"  Hero Id: {hero_details.get('id', 'N/A')}")
            print(f"  Attribute: {hero_details.get('primary_attr', 'N/A')}")
            print(f"  Roles: {hero_details.get('roles', 'N/A')}")
            print("-" * 40)

        save_json(heroes_dict, "heroes.json")# Guardar la variable 'items' en un archivo JSON

        print("Datos guardados en heroes.json.")
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")

def get_match_details(match_id: int):
    url = f"https://api.opendota.com/api/matches/{match_id}"
    teams_dict = {0: "Radiant", 1: "Dire"}
    try:
        response = requests.get(url)
        response.raise_for_status()
        match_details = response.json()
        print(f"Match ID: {match_details.get('match_id', 'N/A')}")
        print(f"  Duración: {match_details.get('duration', 'N/A')}")
        print(f"  Modo de juego: {match_details.get('game_mode', 'N/A')}")
        print(f"  Radiant: {match_details.get('radiant_win', 'N/A')}")
        print(f"  Jugadores:")
        for number_player, player in enumerate(match_details.get('players', [])):
            hero_name, _ = get_hero_from_id(player.get('hero_id'))
            print(f"    {player.get('account_id', f'Player {number_player}')}: {hero_name}")
            team = player.get('team_number', 'N/A')
            print(f"    Equipo: {teams_dict.get(team, 'N/A')}")
            print_items_list(player)
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")

def print_items_list(player):
    for slot in range(6):
        item_id = player.get(f'item_{slot}', 0)
        print(f"      Slot {slot + 1}: {get_item_from_id(item_id)[0]}")

    for slot in range(3):
        item_id = player.get(f'backpack_{slot}', 0)
        print(f"      Mochila {slot + 1}: {get_item_from_id(item_id)[0]}")

    item_id = player.get(f'item_neutral', 0)
    print(f"      Neutral 1: {get_item_from_id(item_id)[0]}")

    item_id = player.get(f'item_neutral2', 0)
    print(f"      Neutral 2: {get_item_from_id(item_id)[0]}")


def get_item_popularity(hero_id: int):
    """
    Llama al endpoint de OpenDota para obtener la popularidad de ítems para un héroe dado.

    Parámetros:
      - hero_id: ID del héroe (entero) para el cual se desea obtener la popularidad de ítems.

    Retorna:
      - Diccionario con los datos de popularidad de ítems para el héroe, o None si ocurre algún error.
    """
    url = f"https://api.opendota.com/api/heroes/{hero_id}/itemPopularity"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error para códigos de estado HTTP que indiquen fallo
        popularity_data = response.json()
        if popularity_data:
            print("Datos de popularidad de ítems:")

            for time_game, items in popularity_data.items():
                print(f"Tiempo de juego: {time_game}")
                items_sorted = dict(sorted(items.items(), key=lambda item: item[1], reverse=True))
                for item_id, item_data in items_sorted.items():
                    item_name, _ = get_item_from_id(int(item_id))
                    print(f"  {item_name}: {item_data}")

        else:
            print("No se pudo obtener la información.")
    except requests.RequestException as e:
        print(f"Error al llamar a la API: {e}")
        return None


def get_hero_statistics(hero_id:int):

    url = f"https://api.opendota.com/api/heroStats/"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error para códigos de estado HTTP que indiquen fallo
        popularity_data = response.json()
        if popularity_data:
            print("Datos de popularidad de ítems:")

            for hero_info in popularity_data:
                hero_id = hero_info.get('id')
                hero_name = get_hero_from_id(hero_id)[0]
                print(f"Estadisticas Heroe: {hero_name}")
                print(f"  Roles: {hero_info.get('roles', 'N/A')}")
                print(f"  1_pick: {hero_info.get('1_pick', 'N/A')}")
        else:
            print("No se pudo obtener la información.")
    except requests.RequestException as e:
        print(f"Error al llamar a la API: {e}")
        return None




def query_custom(hero_id: int, region: int, patch: str, is_win: bool, min_date: str, lane_role: int, limit: int = 200):
    """
        Ejecuta una consulta SQL en OpenDota para obtener estadísticas de partidas filtradas por:
          - hero_id: ID del héroe (player_matches.hero_id)
          - region: Región de la partida (matches.region)
          - is_win: Resultado de la partida (True: ganadas, False: perdidas)
          - min_date: Fecha mínima en formato ISO (por ejemplo, '2025-01-01T00:00:00.000Z')
          - lane_role: Rol de línea del jugador (player_matches.lane_role)
          - limit: Límite de registros a retornar (por defecto 200)

        La consulta realiza uniones entre varias tablas (matches, match_patch, leagues, player_matches, heroes, etc.)
        y calcula el winrate (además de aplicar el intervalo de confianza de Wilson) a partir de la condición:
          - Si is_win es True, se seleccionan partidas en las que la condición de victoria del jugador
            (determinada comparando si está en Radiant y matches.radiant_win) es verdadera.
          - Si is_win es False, se seleccionan las partidas en las que el jugador perdió.

        Retorna:
          Un objeto JSON con el resultado de la consulta.
        """

    import requests
    import urllib.parse
    import json
    # Convertir la fecha mínima a una condición SQL utilizando la función extract(epoch from timestamp ...)
    min_date_condition = f"extract(epoch from timestamp '{min_date}')"

    # Condición para el resultado de la partida:
    # Si se busca ganar, la condición es que el booleano (player_matches.player_slot < 128) sea igual a matches.radiant_win.
    # Si se busca perder, se invierte la condición.
    if is_win:
        result_condition = "((player_matches.player_slot < 128) = matches.radiant_win) = true"
    else:
        result_condition = "((player_matches.player_slot < 128) != matches.radiant_win)"

    # Condición para la región: se asume que matches.region es numérico.
    region_condition = f"AND matches.region = {region}"

    # Construir la consulta SQL con los filtros proporcionados.
    sql_query = f"""
    SELECT
        matches.match_id,
        matches.start_time,
        ((player_matches.player_slot < 128) = matches.radiant_win) AS win,
        player_matches.hero_id,
        player_matches.account_id,
        leagues.name AS leaguename
    FROM matches
    JOIN match_patch USING(match_id)
    JOIN leagues USING(leagueid)
    JOIN player_matches USING(match_id)
    JOIN heroes ON heroes.id = player_matches.hero_id
    LEFT JOIN notable_players ON notable_players.account_id = player_matches.account_id
    LEFT JOIN teams USING(team_id)
    WHERE TRUE
      -- Filtrar por parche: se consideran partidas con patch menor o igual al indicado
      AND match_patch.patch <= '{patch}'
      -- Filtrar por el héroe especificado
      AND (player_matches.hero_id = {hero_id})
      -- Asegurar que el jugador ganó la partida, según su posición (Radiant)
      AND ((player_matches.player_slot < 128) = matches.radiant_win) = true
      -- Filtrar por el rol de línea del jugador
      AND (player_matches.lane_role = {lane_role})
      -- Filtrar partidas a partir de la fecha mínima (convertida a epoch)
      AND matches.start_time >= extract(epoch from timestamp '{min_date}')
    ORDER BY matches.match_id NULLS LAST
    LIMIT {limit}
    """

    # Codificar la consulta para que pueda enviarse en una URL (URL Encoding)
    encoded_query = urllib.parse.quote(sql_query)

    # Construir la URL final para llamar al endpoint de OpenDota Explorer
    url = f"https://api.opendota.com/api/explorer?sql={encoded_query}"

    # Realizar la solicitud GET a la API de OpenDota
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error al obtener datos: {response.status_code} - {response.text}")

    # Retornar el resultado en formato JSON
    return response.json()










