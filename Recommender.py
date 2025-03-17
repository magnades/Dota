import requests
from collections import defaultdict
import logging

# Configurar logging (opcional)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class DotaHeroRecommender:
    def __init__(self):
        self.hero_data = self._fetch_hero_data()
        self.counters = self._get_counters_data()
        self.players = self._get_players_data()
        self.player_strengths = self._get_players_strengths()
        # Mapeo de roles numéricos a nombres de posiciones deseadas
        self.positions = {
            1: "Carry",
            2: "Mid",
            3: "Offlane",
            4: "Soft Support",
            5: "Hard Support"
        }

    def _get_players_strengths(self):
        return self.load_json("players_heroes_strengths.json")

    def _get_players_data(self):
        return self.load_json("players_information.json")
    def _get_player_id(self, player_name):
        return self.players.get(player_name, None)


    def _fetch_hero_data(self) -> dict:
        """
        Obtiene información de héroes desde la API de OpenDota y la organiza en un diccionario
        donde la clave es el ID del héroe.
        """
        heroes =  self.load_json("backend/Data/heroes.json")
        logging.info("Se obtuvieron datos de %d héroes", len(heroes))
        result = {}

        for hero, values in heroes.items():
            result[values['id']] = values

        return result


    def _get_counters_data(self) -> dict:
        """
        Retorna datos de contra-picks (counters) de forma simplificada para algunos héroes.
        Los datos indican a qué héroes es fuerte (strong_against) y contra quién es débil (weak_against).
        Estos datos son ficticios y deben ampliarse con información real.
        """
        return self.load_json("backend/Data/matchups.json")

    @staticmethod
    def load_json(filename: str):
        import json

        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"El archivo '{filename}' no existe.")
            data = None

        return data

    def recommend_heroes(self, allies: list, enemies: list, position: int, num_recom: int) -> list:
        """
        Recomienda héroes basándose en:
          - Contra-picks de los enemigos (si un enemigo es débil ante cierto héroe, se suma mayor puntuación).
          - Sinergia con los aliados (si un aliado tiene buena sinergia con cierto héroe, se suma una bonificación).
          - Coincidencia con el rol deseado, evaluado según la lista de roles del héroe obtenido de la API.

        Parámetros:
          - allies: Lista de IDs de héroes ya seleccionados como aliados.
          - enemies: Lista de IDs de héroes enemigos.
          - position: Código numérico del rol deseado (1: Carry, 2: Mid, 3: Offlane, 4: Soft Support, 5: Hard Support).

        Retorna:
          - Lista con los IDs de los 3 héroes recomendados.
        """
        all_heroes = set(self.hero_data.keys())
        banned = set(allies + enemies)
        candidates = all_heroes - banned

        scores = defaultdict(int)

        # Factor 1: Contra-picks enemigos (aumenta 3 puntos si el candidato es débil contra el enemigo)
        for enemy in enemies:
            if str(enemy) in self.counters:
                for counter in self.counters[str(enemy)].get('weak_against', []):
                    if counter in candidates:
                        scores[counter] += 3

        # Factor 2: Sinergia con aliados (aumenta 2 puntos si el candidato es fuerte contra el aliado)
        for ally in allies:
            if str(ally) in self.counters:
                for synergy in self.counters[str(ally)].get('strong_against', []):
                    if synergy in candidates:
                        scores[synergy] += 2

        # Factor 3: Bonus por rol deseado
        desired_role = self.positions.get(position, "")
        if desired_role:
            for candidate in candidates:
                hero = self.hero_data.get(candidate, {})
                hero_roles = hero.get("roles", [])
                if desired_role in hero_roles:
                    scores[candidate] += 1  # Bonus de 1 punto por coincidir con el rol deseado

        # Ordenar candidatos por puntuación (de mayor a menor)
        sorted_candidates = sorted(candidates, key=lambda x: scores[x], reverse=True)
        logging.info("Puntuaciones de candidatos: %s", {k: scores[k] for k in sorted_candidates})

        recommendations = sorted_candidates[:num_recom]

        print(f"Recomendaciones para {self.positions[position]}:")
        for hero_id in recommendations:
            hero_name = self.get_hero_from_id(hero_id)[0]
            print(f"- {hero_name}")

        return sorted_candidates[:3]

    def get_player_strength(self, player_id):
        return self.player_strengths.get(str(player_id), {})

    def recommend_heroes_for_player(self, allies: list, enemies: list, position: int, player_name: str, num_recom: int) -> list:
        """
        Recomienda héroes basándose en:
          - Contra-picks de los enemigos (si un enemigo es débil ante cierto héroe, se suma mayor puntuación).
          - Sinergia con los aliados (si un aliado tiene buena sinergia con cierto héroe, se suma una bonificación).
          - Coincidencia con el rol deseado, evaluado según la lista de roles del héroe obtenido de la API.

        Parámetros:
          - allies: Lista de IDs de héroes ya seleccionados como aliados.
          - enemies: Lista de IDs de héroes enemigos.
          - position: Código numérico del rol deseado (1: Carry, 2: Mid, 3: Offlane, 4: Soft Support, 5
        """
        player_id = self._get_player_id(player_name)
        player_heroes_strengths = self.get_player_strength(player_id)

        player_heroes = set(player_heroes_strengths.get("strong", []))

        banned = set(allies + enemies)
        candidates = player_heroes - banned

        scores = defaultdict(int)

        # Factor 1: Contra-picks enemigos (aumenta 3 puntos si el candidato es débil contra el enemigo)
        for enemy in enemies:
            if str(enemy) in self.counters:
                for counter in self.counters[str(enemy)].get('weak_against', []):
                    if counter in candidates:
                        scores[counter] += 3

        # Factor 2: Sinergia con aliados (aumenta 2 puntos si el candidato es fuerte contra el aliado)
        for ally in allies:
            if str(ally) in self.counters:
                for synergy in self.counters[str(ally)].get('strong_against', []):
                    if synergy in candidates:
                        scores[synergy] += 2

        # Factor 3: Bonus por rol deseado
        desired_role = self.positions.get(position, "")
        if desired_role:
            for candidate in candidates:
                hero = self.hero_data.get(candidate, {})
                hero_roles = hero.get("roles", [])
                if desired_role in hero_roles:
                    scores[candidate] += 1  # Bonus de 1 punto por coincidir con el rol deseado

        # Factor 4: Bonus por fortaleza contra enemigos (aumenta 3 puntos si el jugador es fuerte contra los enemigos)

        for enemy in enemies:
            if enemy in player_heroes_strengths.get("strong_against", []):
                for counter in candidates:
                    scores[counter] += 3

        # Factor 5: Bonus por Sinergia con aliados (aumenta 2 puntos si el jugador es fuerte jugando con los alidados)
        for ally in allies:
            if ally in player_heroes_strengths.get("strong_with", []):
                for counter in candidates:
                    scores[counter] += 3

        # Ordenar candidatos por puntuación (de mayor a menor)
        sorted_candidates = sorted(candidates, key=lambda x: scores[x], reverse=True)
        logging.info("Puntuaciones de candidatos: %s", {k: scores[k] for k in sorted_candidates})

        recommendations = sorted_candidates[:num_recom]

        print(f"Recomendaciones para {self.positions[position]}:")
        for hero_id in recommendations:
            hero_name = self.get_hero_from_id(hero_id)[0]
            print(f"- {hero_name}")

        return sorted_candidates[:num_recom]


    def get_hero_from_id(self, hero_id: int):
        heroes = self.load_json("backend/Data/heroes.json")
        for hero_name, hero_details in heroes.items():
            if hero_details.get("id") == hero_id:
                # print(f'Heroe encontrado: {hero_name}')
                return hero_name, hero_details

        return None, None



