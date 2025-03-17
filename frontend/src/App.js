import React, { useState, useEffect } from "react";
import {fetchHeroes, fetchPlayers, getRecommendations} from "./api";
import "./App.css";

const positions = [
  { id: 1, name: "Carry", image: "/position_images/1.png" },
  { id: 2, name: "Mid", image: "/position_images/2.png" },
  { id: 3, name: "Offlane", image: "/position_images/3.png" },
  { id: 4, name: "Soft Support", image: "/position_images/4.png" },
  { id: 5, name: "Hard Support", image: "/position_images/5.png" },
];

function App() {
  const [heroes, setHeroes] = useState([]);
  const [players, setPlayers] = useState([]);
  const [allies, setAllies] = useState([]);
  const [enemies, setEnemies] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [selectedPosition, setSelectedPosition] = useState(null);
    const [selectedPlayer, setSelectedPlayer] = useState(null);

  useEffect(() => {
    const getHeroes = async () => {
      const data = await fetchHeroes();
      setHeroes(data);
    };

    getHeroes();
  }, []);

  useEffect(() => {
    const getPlayers = async () => {
      const data = await fetchPlayers();
      setPlayers(data);
    };

    getPlayers();
  }, []);

  const handleLeftClick = (hero) => {
    if (!allies.find((h) => h.id === hero.id)) {
      setAllies([...allies, hero]);
    }
  };

  const handleRightClick = (event, hero) => {
    event.preventDefault();
    if (!enemies.find((h) => h.id === hero.id)) {
      setEnemies([...enemies, hero]);
    }
  };

 const fetchRecommendations = async () => {
  if (!selectedPosition) {
    alert("Por favor, selecciona una posición antes de pedir recomendaciones.");
    return;
  }

  const payload = {
      allies: allies.map((h) => h.id),
      enemies: enemies.map((h) => h.id),
      position: selectedPosition, // Usa la posición seleccionada
      num_recom: 3,
  };

  console.log("Datos enviados a la API:", payload);

  try {
    const response = await getRecommendations(payload.allies, payload.enemies, payload.position, payload.num_recom);
    setRecommendations(response.recommendations);
  } catch (error) {
    console.error("Error al obtener recomendaciones:", error);
  }
};

 const fetchRecommendationsForPlayer = async () => {
  if (!selectedPlayer) {
    alert("Por favor, selecciona un jugador antes de pedir recomendaciones.");
    return;
  }

  const payloadforplayer = {
      allies: allies.map((h) => h.id),
      enemies: enemies.map((h) => h.id),
      position: selectedPosition, // Usa la posición seleccionada
      playerId: selectedPlayer,
      num_recom: 3,
  };

  console.log("Datos enviados a la API:", payloadforplayer);

  try {
    const response = await getRecommendationsForPlayer(payloadforplayer.allies, payloadforplayer.enemies, payloadforplayer.position, payloadforplayer.playerId, payloadforplayer.num_recom);
    setRecommendations(response.recommendations);
  } catch (error) {
    console.error("Error al obtener recomendaciones:", error);
  }
};

  return (
    <div className="App">
      <h1>Dota Hero Selector</h1>
      <div className="grid">
        {heroes.map((hero) => (
          <img
            key={hero.id}
            src={`/hero_images/${hero.id}.png`} // Asume que las imágenes están nombradas por ID
            alt={hero.name}
            onClick={() => handleLeftClick(hero)}
            onContextMenu={(e) => handleRightClick(e, hero)}
            className="hero-image"
          />
        ))}
      </div>
      <div className="selected-teams">
        <div>
          <h2>Equipo Aliado:</h2>
          <ul>
            {allies.map((hero) => (
              <li key={hero.id}>{hero.name}</li>
            ))}
          </ul>
        </div>

        <div>
          <h2>Equipo Enemigo:</h2>
          <ul>
            {enemies.map((hero) => (
              <li key={hero.id}>{hero.name}</li>
            ))}
          </ul>
        </div>
      </div>

      <button onClick={fetchRecommendations}>Obtener Recomendaciones</button>

      <div className="selected">
        <h2>Recomendaciones:</h2>
        <ul>
          {recommendations.map((heroId) => (
            <li key={heroId}>ID de héroe recomendado: {heroId}</li>
          ))}
        </ul>
      </div>

      <div className="positions">
        <h2>Selecciona tu posición:</h2>
        <div className="positions-grid">
          {positions.map((pos) => (
            <img
              key={pos.id}
              src={pos.image}
              alt={pos.name}
              className={`position-image ${selectedPosition === pos.id ? "selected" : ""}`}
              onClick={() => setSelectedPosition(pos.id)}
            />
          ))}
        </div>
      </div>

      <div className="positions">
          <h2>Selecciona el Jugador:</h2>
        {players.map((player) => (
          <img
            key={player.id}
            src={`/player_images/${player.id}.jpg`} // Asume que las imágenes están nombradas por ID
            alt={player.name}
            className={`position-image ${selectedPlayer === player.id ? "selected" : ""}`}
              onClick={() => setSelectedPlayer(player.name)}
          />
        ))}
      </div>

        <button onClick={fetchRecommendationsForPlayer}>Obtener Heroes para Jugador</button>

    </div>
  );
}

export default App;