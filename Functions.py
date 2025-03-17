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

        save_json(items, "../Data/items.json")# Guardar la variable 'items' en un archivo JSON

        print("Datos guardados en items.json.")
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")

def update_hero_attributes():

    import requests

    # URL del endpoint de ítems de OpenDota
    url = "https://api.opendota.com/api/constants/heroes"

    try:
        # Realizar la solicitud GET
        response = requests.get(url)
        response.raise_for_status()  # Verificar si hubo errores en la solicitud

        # Convertir la respuesta a formato JSON
        items = response.json()
        # print(items)

        # Iterar sobre los ítems y mostrar información básica
        print("Lista de ítems:")
        for item_name, item_details in items.items():
            # hero_name = get_hero_from_id(item_name)
            print(f"Nombre interno: {item_details.get('localized_name', 'N/A')}")
            print(f"  id: {item_details.get('id', 'N/A')}")
            print(f"  Rolees: {item_details.get('roles', 'N/A')}")
            print(f"  Tipo de Ataque: {item_details.get('attack_type', 'N/A')}")
            print("-" * 40)

        save_json(items, "heroes_attributes.json")# Guardar la variable 'items' en un archivo JSON

        print("Datos guardados en items.json.")
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")


def update_matchup_list():
    """
    Actualiza la lista de matchups para cada héroe utilizando la API de OpenDota.
    Para cada héroe contenido en 'heroes.json', se obtiene la lista de héroes contra los que es fuerte y débil,
    y se guarda el resultado en 'matchups.json'.

    Se asegura de no superar 59 llamadas por minuto introduciendo un retraso de 1.1 segundos entre cada llamada.
    """
    import time
    heroes = load_json("../Data/heroes.json")
    matchup_dict = {}

    for hero_name, values in heroes.items():
        hero_id = int(values["id"])
        try:
            strong_against, weak_against = get_hero_counters(hero_id)
            matchup_dict[hero_id] = {"strong_against": strong_against, "weak_against": weak_against}
            print(f"Héroe: {hero_name} (ID: {hero_id}), matchup procesado.")
        except Exception as e:
            print(f"Error procesando el matchup para el héroe {hero_name} (ID: {hero_id}): {e}")
        # Pausa para asegurar no superar 59 llamadas por minuto
        time.sleep(1.1)

    save_json(matchup_dict, "../Data/matchups.json")
    print("Datos de matchups guardados en 'matchups.json'.")

def update_players_heroes_strengths():

    import time
    players = load_json("players_information.json")

    matchup_dict = {}

    for player_name, player_id in players.items():

        try:
            weak, strong, strong_against, weak_against, strong_with, weak_with = get_player_hero_strengths(player_id)
            matchup_dict[player_id] = {
                "strong": strong,
                "weak": weak,
                "strong_against": strong_against,
                "weak_against": weak_against,
                "strong_with": strong_with,
                "weak_with": weak_with,
            }
            print(f"Heroes del Jugador: {player_name} (ID: {player_id}), infor de fortalezas procesada.")
        except Exception as e:
            print(f"Error procesando el fortalezas para el jugador {player_name} (ID: {player_id}): {e}")
        # Pausa para asegurar no superar 59 llamadas por minuto
        time.sleep(1.1)

    save_json(matchup_dict, "players_heroes_strengths.json")
    print("Datos de fortalezas de los jugadores guardados en 'players_heroes_strengths.json'.")



def update_item_images():
    import os

    items = load_json("../Data/items.json")

    # Base URL para construir la URL completa de la imagen
    base_image_url = "https://cdn.cloudflare.steamstatic.com"

    # Crear un directorio para guardar las imágenes (si no existe)
    os.makedirs("../../frontend/frontend/public/item_images", exist_ok=True)

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
                image_file = os.path.join("../../frontend/frontend/public/item_images", f"{item_name}.png")
                with open(image_file, "wb") as f:
                    for chunk in img_response.iter_content(1024):
                        f.write(chunk)
                print(f"  Imagen descargada y guardada en: {image_file}")
            except requests.exceptions.RequestException as e:
                print(f"  Error al descargar la imagen de {item_name}: {e}")
        else:
            print("  No se encontró imagen para este ítem.")

        print("-" * 40)

def update_hero_images():
    import os
    import requests

    # Cargar datos de héroes desde el archivo JSON.
    # Se asume que 'load_json' es una función definida en tu proyecto para cargar archivos JSON.
    heroes = load_json("heroes_attributes.json")
    if not heroes:
        print("No se pudieron cargar los datos de héroes.")
        return

    # URL base para construir la URL completa de la imagen.
    base_image_url = "https://cdn.cloudflare.steamstatic.com"

    # Crear el directorio para guardar las imágenes de los héroes (si no existe)
    # Usamos una ruta relativa para que la carpeta se cree en el directorio actual.
    output_dir = "hero_images"
    os.makedirs(output_dir, exist_ok=True)

    print("Lista de héroes y descarga de imágenes:")
    for hero_name, hero_details in heroes.items():
        print(f"Procesando héroe: {hero_name}")
        # Obtener la ruta de la imagen; en OpenDota, 'img' suele ser una ruta relativa.
        img_path = hero_details.get("img")
        if img_path:
            # Construir la URL completa de la imagen
            full_img_url = base_image_url + img_path
            try:
                img_response = requests.get(full_img_url, stream=True)
                img_response.raise_for_status()
                # Definir la ruta para guardar la imagen. Se utiliza el nombre del héroe.
                image_file = os.path.join(output_dir, f"{hero_name}.png")
                with open(image_file, "wb") as f:
                    for chunk in img_response.iter_content(1024):
                        f.write(chunk)
                print(f"Imagen descargada y guardada en: {image_file}")
            except requests.exceptions.RequestException as e:
                print(f"Error al descargar la imagen para {hero_name}: {e}")
        else:
            print(f"No se encontró imagen para el héroe: {hero_name}")
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

        save_json(heroes_dict, "../Data/heroes.json")# Guardar la variable 'items' en un archivo JSON

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


import requests


def get_hero_counters(hero_id: int, max_retries: int = 5, initial_delay: float = 1.0):
    """
    Obtiene los datos de matchups para un héroe desde la API de OpenDota,
    implementando reintentos en caso de recibir un error 429 (Too Many Requests).

    Parámetros:
      - hero_id: ID del héroe.
      - max_retries: Número máximo de reintentos (por defecto 5).
      - initial_delay: Tiempo inicial de espera en segundos (por defecto 1.0).

    Retorna:
      - strong_against: Lista de IDs de héroes contra los que el héroe es fuerte (winrate < 0.5).
      - weak_against: Lista de IDs de héroes contra los que el héroe es débil (winrate >= 0.5).
    """
    import time

    url = f"https://api.opendota.com/api/heroes/{hero_id}/matchups"
    retries = 0
    delay = initial_delay

    while retries < max_retries:
        response = requests.get(url)
        if response.status_code == 429:
            print(
                f"Error 429 para héroe {hero_id}. Reintentando en {delay} segundos... (Intento {retries + 1}/{max_retries})")
            time.sleep(delay)
            retries += 1
            delay *= 2  # Aumenta el delay de forma exponencial.
        else:
            response.raise_for_status()
            data = response.json()
            strong_against = []
            weak_against = []
            for matchup in data:
                games = matchup.get("games_played", 0)
                wins = matchup.get("wins", 0)
                if games > 30:
                    winrate = wins / games
                    if winrate < 0.5:
                        strong_against.append(matchup["hero_id"])
                    else:
                        weak_against.append(matchup["hero_id"])
            return strong_against, weak_against

    raise Exception(f"Se excedió el número máximo de reintentos para obtener datos de matchups del héroe {hero_id}.")


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


def get_player_information(player_id: int):
    """
    Obtiene información de un jugador específico utilizando la API de OpenDota.

    Retorna:
      - Diccionario con la información del jugador, o None si ocurre algún error.
    """
    url = f"https://api.opendota.com/api/players/{player_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        player_data = response.json()
        print("Información del jugador:")
        print(f"Nombre: {player_data.get('profile', {}).get('personaname', 'N/A')}")
        print(f"Account_id: {player_data.get('profile', {}).get('account_id', 'N/A')}")
        print(f"Steam Id: {player_data.get('profile', {}).get('steamid', 'N/A')}")
        print(f"Rank tier: {player_data.get('rank_tier', 'N/A')}")
        print(f"Avatar Medium: {player_data.get('profile', {}).get('avatarmedium', 'N/A')}")
        return player_data
    except requests.RequestException as e:
        print(f"Error al llamar a la API: {e}")
        return None

def get_player_win_lose_information(
        player_id: int,
        limit=None,
        offset=None,
        win=None, patch=None,
        game_mode=None,
        lobby_type=None,
        region=None,
        date=None,
        lane_role=None,
        hero_id=None,
        is_radiant=None,
        included_account_id=None,
        excluded_account_id=None,
        with_hero_id=None,
        against_hero_id=None,
        significant=None,
        having=None,
        sort=None):

    url = f"https://api.opendota.com/api/players/{player_id}/wl"

    params = {
        "limit": limit,
        "offset": offset,
        "win": win,
        "patch": patch,
        "game_mode": game_mode,
        "lobby_type": lobby_type,
        "region": region,
        "date": date,
        "lane_role": lane_role,
        "hero_id": hero_id,
        "is_radiant": is_radiant,
        "included_account_id": included_account_id,
        "excluded_account_id": excluded_account_id,
        "with_hero_id": with_hero_id,
        "against_hero_id": against_hero_id,
        "significant": significant,
        "having": having,
        "sort": sort
    }

    # Eliminar parámetros con valor None
    params = {k: v for k, v in params.items() if v is not None}



    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        player_data = response.json()
        print("Información del jugador:")
        print(f"Victorias: {player_data.get('win', 'N/A')}")
        print(f"Derrotas: {player_data.get('lose', 'N/A')}")
        print(f"Total: {player_data.get('win', 'N/A') + player_data.get('lose', 'N/A')}")
        return player_data
    except requests.RequestException as e:
        print(f"Error al llamar a la API: {e}")
        return None

def get_player_recent_matches(player_id: int):
    """
    Obtiene las últimas partidas de un jugador específico utilizando la API de OpenDota.

    Parámetros:
      - player_id: ID del jugador.
      - limit: Número máximo de partidas a obtener (por defecto 10).

    Retorna:
      - Lista de diccionarios con información de las partidas, o None si ocurre algún error.
    """
    url = f"https://api.opendota.com/api/players/{player_id}/recentMatches"

    try:
        response = requests.get(url)
        response.raise_for_status()
        matches_data = response.json()
        print("Últimas partidas del jugador:")
        for i, match in enumerate(matches_data):
            hero_name = get_hero_from_id(match.get('hero_id', 'N/A'))[0]
            print(f"Match {i} Id: {match.get('match_id', 'N/A')}")
            print(f"  Duración: {match.get('duration', 'N/A')}")
            print(f"  Héroe: {hero_name}")
            print(f"  kills: {match.get('kills', 'N/A')}")
            print(f"  deaths: {match.get('deaths', 'N/A')}")
            print(f"  assists: {match.get('assists', 'N/A')}")
            print(f"  Averange player rank: {match.get('average_rank', 'N/A')}")
            print(f"  GPM: {match.get('gold_per_min', 'N/A')}")
            print(f"  XPM: {match.get('xp_per_min', 'N/A')}")
            print(f"  last hits: {match.get('last_hits', 'N/A')}")
            print(f"  lane: {match.get('lane', 'N/A')}")
            print(f"  lane_role: {match.get('lane_role', 'N/A')}")

        return matches_data
    except requests.RequestException as e:
        print(f"Error al llamar a la API: {e}")
        return None

def get_player_heroes(
        player_id: int,
        limit=None,
        offset=None,
        win=None, patch=None,
        game_mode=None,
        lobby_type=None,
        region=None,
        date=None,
        lane_role=None,
        hero_id=None,
        is_radiant=None,
        included_account_id=None,
        excluded_account_id=None,
        with_hero_id=None,
        against_hero_id=None,
        significant=None,
        having=None,
        sort=None):

    """
        hero_id: El identificador del héroe.
    last_played: La marca de tiempo (timestamp) de la última partida en la que se jugó ese héroe.
    games: El número total de partidas jugadas con ese héroe.
    win: El número de partidas ganadas con ese héroe.

    Adicionalmente, dependiendo de la implementación y versión de la API, puede incluir otras estadísticas como:

    with_games, against_games: Partidas jugadas con o contra el héroe (para análisis más detallados).
    with_win, against_win: Número de victorias en esas categorías.


    :param player_id:
    :param limit:
    :param offset:
    :param win:
    :param patch:
    :param game_mode:
    :param lobby_type:
    :param region:
    :param date:
    :param lane_role:
    :param hero_id:
    :param is_radiant:
    :param included_account_id:
    :param excluded_account_id:
    :param with_hero_id:
    :param against_hero_id:
    :param significant:
    :param having:
    :param sort:
    :return:
    """

    url = f"https://api.opendota.com/api/players/{player_id}/heroes"

    params = {
        "limit": limit,
        "offset": offset,
        "win": win,
        "patch": patch,
        "game_mode": game_mode,
        "lobby_type": lobby_type,
        "region": region,
        "date": date,
        "lane_role": lane_role,
        "hero_id": hero_id,
        "is_radiant": is_radiant,
        "included_account_id": included_account_id,
        "excluded_account_id": excluded_account_id,
        "with_hero_id": with_hero_id,
        "against_hero_id": against_hero_id,
        "significant": significant,
        "having": having,
        "sort": sort
    }

    # Eliminar parámetros con valor None
    params = {k: v for k, v in params.items() if v is not None}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        player_data = response.json()
        print(f"Información del jugador: {player_id}")
        for hero_dict in player_data:
            if hero_dict.get('games', 'N/A'):
                hero_name = get_hero_from_id(hero_dict.get("hero_id", "N/A"))[0]
                print(f"Heroe: {hero_name}")
                print(f"    games: {hero_dict.get('games', 'N/A')}")
                print(f"    win: {hero_dict.get('win', 'N/A')}")
                print(f"    {hero_dict.get('with_win', '0')} partidas ganadas con {hero_name} de companero del total jugadas {hero_dict.get('with_games', '0')}")
                print(
                    f"    {hero_dict.get('against_win', '0')} partidas ganadas con {hero_name} de enemigo del total jugadas {hero_dict.get('against_games', '0')}")
        return player_data
    except requests.RequestException as e:
        print(f"Error al llamar a la API: {e}")
        return None

def get_player_hero_strengths(player_id: int):
    player_data = get_player_heroes(player_id)

    strong_against = []
    weak_against = []
    strong_with = []
    weak_with = []
    weak = []
    strong = []

    for hero_dict in player_data:
        hero_id = hero_dict.get("hero_id", 0)
        games = hero_dict.get("games", 0)
        wins = hero_dict.get("win", 0)
        with_win = hero_dict.get("with_win", 0)
        with_games = hero_dict.get("with_games", 0)
        against_win = hero_dict.get("against_win", 0)
        against_games = hero_dict.get("against_games", 0)

        if games > 30:
            winrate = wins / games
            if winrate < 0.5:
                weak.append(hero_id)
            else:
                strong.append(hero_id)

        if with_games > 30:
            winrate = with_win / with_games
            if winrate < 0.5:
                weak_with.append(hero_id)
            else:
                strong_with.append(hero_id)

        if against_games > 30:
            winrate = against_win / against_games
            if winrate < 0.5:
                weak_against.append(hero_id)
            else:
                strong_against.append(hero_id)

    return  weak, strong, strong_against, weak_against, strong_with, weak_with



# LA IDEA ES HACER UN DICCIONARIO PARA SACAR LOS MISMOS STRONG_AGOINS WEAK_AGAINST PERO AHORA POR JUGADOR
# CREO QUE TAMBIEN PUEDE DESPUES CONSIDERARSE UN CRITERIO DE SINERGIA, OSEA TOMANDO LOS DATOS DE EL PORCENTAJE DE VICTORIA CUANDO JUEGA CON
# LOS OTROS HEORES DEL EQUIPO Y TAMBIEN EL EFECTO CUANDO JUEGA CONTRA LOS HEROES DEL OTRO EQUIPO














