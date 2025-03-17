const API_URL = "http://127.0.0.1:8000";

export const getRecommendations = async (allies, enemies, position, num_recom) => {
  const response = await fetch(`${API_URL}/api/recommend`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ allies, enemies, position, num_recom }),
  });

  if (!response.ok) {
    throw new Error("Error al obtener las recomendaciones");
  }

  return response.json();
};

export const getRecommendationsForPlayer = async (allies, enemies, position, player, num_recom) => {
  const response = await fetch(`${API_URL}/api/recommendforplayer`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ allies, enemies, position, player, num_recom }),
  });

  if (!response.ok) {
    throw new Error("Error al obtener las recomendaciones para jugador");
  }

  return response.json();
};

// api.js
export const fetchHeroes = async () => {
  try {
    const response = await fetch(`${API_URL}/api/heroes`);
    if (!response.ok) {
      throw new Error("Error al obtener héroes");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error al obtener héroes:", error);
    return []; // Devuelve un array vacío en caso de error
  }
};

// api.js
export const fetchPlayers = async () => {
  try {
    const response = await fetch(`${API_URL}/api/players`);
    if (!response.ok) {
      throw new Error("Error al obtener jugadores");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error al obtener jugadores:", error);
    return []; // Devuelve un array vacío en caso de error
  }
};



