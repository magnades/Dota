# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from DotaHeroRecommender import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # La URL donde corre tu app React
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)

# Instanciar la clase recomendadora
recommender = DotaHeroRecommender()

@app.get("/api/heroes")
def get_heroes():
    """
    Endpoint para obtener la lista de héroes.
    Retorna un diccionario con los datos de los héroes, con la clave siendo el ID del héroe.
    """
    return recommender.get_heroes_data()

@app.get("/api/players")
def get_players():
    """
    Endpoint para obtener la lista de héroes.
    Retorna un diccionario con los datos de los héroes, con la clave siendo el ID del héroe.
    """
    return recommender.get_players_info()

# Definir el modelo de datos para la solicitud de recomendación.
class RecommendRequest(BaseModel):
    allies: List[int]   # Lista de IDs de héroes aliados
    enemies: List[int]  # Lista de IDs de héroes enemigos
    position: int       # Código numérico del rol deseado (1: Carry, 2: Mid, etc.)
    num_recom: int = 5  # Número de recomendaciones deseadas (por defecto 3)

class RecommendForPlayerRequest(BaseModel):
    allies: List[int]   # Lista de IDs de héroes aliados
    enemies: List[int]  # Lista de IDs de héroes enemigos
    position: int       # Código numérico del rol deseado (1: Carry, 2: Mid, etc.)
    player_name: str         # Nombre del jugador
    num_recom: int = 5  # Número de recomendaciones deseadas (por defecto 3)

@app.post("/api/recommend")
def recommend_heroes(request: RecommendRequest):
    """
    Endpoint para obtener recomendaciones de héroes.
    Recibe en el body la lista de héroes aliados, enemigos, el rol deseado y el número de recomendaciones.
    Retorna una lista con los nombres localizados de los héroes recomendados.
    """
    try:
        recommended_ids = recommender.recommend_heroes(
            allies=request.allies,
            enemies=request.enemies,
            position=request.position,
            num_recom=request.num_recom
        )
        # Convertir los IDs recomendados a nombres (o retornar el diccionario completo según necesites)
        recommended_names = [
            recommender.hero_data.get(hero_id, {}).get("localized_name", str(hero_id))
            for hero_id in recommended_ids
        ]
        return {"recommendations": recommended_names}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/api/recommendforplayer")
def recommend_heroes_for_player(req: RecommendForPlayerRequest):
    """
    Endpoint para obtener recomendaciones de héroes.
    Recibe en el body la lista de héroes aliados, enemigos, el rol deseado y el número de recomendaciones.
    Retorna una lista con los nombres localizados de los héroes recomendados.
    """
    try:
        recommended_ids = recommender.recommend_heroes_for_player(
            allies=req.allies,
            enemies=req.enemies,
            position=req.position,
            player_name=req.player_name,
            num_recom=req.num_recom
        )
        # Convertir los IDs recomendados a nombres (o retornar el diccionario completo según necesites)
        recommended_names = [
            recommender.hero_data.get(hero_id, {}).get("localized_name", str(hero_id))
            for hero_id in recommended_ids
        ]
        return {"recommendations": recommended_names}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# @app.post("/api/recommend")
# def get_recommendations(request: RecommendRequest):
#     print("Datos recibidos en FastAPI:", request.model_dump())
#     return {"message": "Datos recibidos correctamente para player"}
#
# @app.post("/api/recommendforplayer")
# async def recommend_for_player(req: RecommendForPlayerRequest):
#     # Aquí deberías usar req.player_name y hacer lo que necesites con él
#     print(f"Jugador seleccionado: {req.player_name}")
#     # Lógica para devolver recomendaciones
#     return {"recommendations": [1, 2, 3]}  # ejemplo de respuesta

