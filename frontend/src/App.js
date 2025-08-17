import React, { useState, useEffect } from "react";
import { fetchHeroes, fetchPlayers, getRecommendations, getRecommendationsForPlayer } from "./api";
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
  const [selectedPlayerName, setSelectedPlayerName] = useState(null);

  useEffect(() => {
    fetchHeroes().then(setHeroes).catch(console.error);
    fetchPlayers().then(setPlayers).catch(console.error);
  }, []);

  const toggleSelection = (hero, list, setList) => {
    setList(list.some((h) => h.id === hero.id) ? list.filter((h) => h.id !== hero.id) : [...list, hero]);
  };

  const fetchRecommendations = async () => {
    if (!selectedPosition) return alert("Por favor, selecciona una posición antes de pedir recomendaciones.");
    try {
      const response = await getRecommendations(
        allies.map((h) => h.id),
        enemies.map((h) => h.id),
        selectedPosition,
        3
      );
      setRecommendations(response.recommendations || []);
    } catch (error) {
      console.error("Error al obtener recomendaciones:", error);
    }
  };

  const fetchRecommendationsForPlayer = async () => {
    if (!selectedPlayerName) return alert("Por favor, selecciona un jugador antes de pedir recomendaciones.");
    if (!selectedPosition) return alert("Por favor, selecciona una posición antes de pedir recomendaciones.");
    try {
      const response = await getRecommendationsForPlayer(
        allies.map((h) => h.id),
        enemies.map((h) => h.id),
        selectedPosition,
        selectedPlayerName,
        5
      );
      setRecommendations(response.recommendations || []);
    } catch (error) {
      console.error("Error al obtener recomendaciones para jugador:", error);
    }
  };

  return (
    <div className="App">
      <h1>Dota Hero Selector</h1>
      <div className="grid">
        {heroes.map((hero) => (
          <img
            key={hero.id}
            src={`/hero_images/${hero.id}.png`}
            alt={hero.name}
            onClick={() => toggleSelection(hero, allies, setAllies)}
            onContextMenu={(e) => { e.preventDefault(); toggleSelection(hero, enemies, setEnemies); }}
            className="hero-image"
          />
        ))}
      </div>

      {/* Contenedor para los equipos aliados y enemigos */}
      <div className="teams-container">
        <div className="team">
          <h2>Equipo Aliado:</h2>
          <ul>{allies.map((hero) => (<li key={hero.id}>{hero.name}</li>))}</ul>
        </div>
        <div className="team">
          <h2>Equipo Enemigo:</h2>
          <ul>{enemies.map((hero) => (<li key={hero.id}>{hero.name}</li>))}</ul>
        </div>
      </div>

      <button onClick={fetchRecommendations}>Obtener Recomendaciones</button>




        <div className="selection-container">
          <div className="player-selection">
            <h2>Selecciona el Jugador:</h2>
            {players.map((player) => (
              <img
                key={player.name}
                src={`/player_images/${player.id}.jpg`}
                alt={player.name}
                className={`position-image ${selectedPlayerName === player.name ? "selected" : ""}`}
                onClick={() => setSelectedPlayerName(player.name)}
              />
            ))}
          </div>
          <div className="position-selection">
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
        </div>

      <button onClick={fetchRecommendationsForPlayer}>Obtener Héroes para Jugador</button>

      <div className="selected">
        <h2>Recomendaciones:</h2>
        <ul>{recommendations.map((heroId) => (<li key={heroId}>ID de héroe recomendado: {heroId}</li>))}</ul>
      </div>
    </div>
  );
}

export default App;


// HACER QUE EL PROGRAMA RESALTE LOS HEROES RECOMENDADOS EN LA LISTA
