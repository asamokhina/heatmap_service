import "./App.css";

import React, { useState, useEffect } from "react";
import Button from "@mui/material/Button";

import GeoJSON from "ol/format/GeoJSON";

import MapWrapper from "./components/MapWrapper";
import Dropdown from "./components/Dropdown";

function App() {
  const [features, setFeatures] = useState([]);
  const [generateMap, setGenerateMap] = useState(false);
  const [selectedId, setSelectedId] = useState(null);
  // const [isAuthenticated, setIsAuthenticated] = useState(false);

  // FIXME move to proper function
  const backendURL = "http://localhost:80/api";

  const handleIdSelection = (id) => {
    setSelectedId(id);
  };

  const handleClick = () => {
    setGenerateMap(true);
  };

  // initialization - retrieve GeoJSON features
  useEffect(() => {
    if (selectedId && generateMap) {
      fetch(`${backendURL}/data/${selectedId}`)
        .then((response) => response.json())
        .then((fetchedFeatures) => {
          const wktOptions = {
            // FIXME these are assumtions
            dataProjection: "EPSG:4326",
            featureProjection: "EPSG:3857",
          };
          const parsedFeatures = new GeoJSON().readFeatures(
            fetchedFeatures,
            wktOptions
          );

          setFeatures(parsedFeatures);
          // map is generated, the cycle is finished
          setGenerateMap(false);
        });
    }
  }, [generateMap]);

  return (
    <div className="App">
      <div className="controls">
        <Dropdown onSelect={handleIdSelection} />
        <Button
          variant="contained"
          onClick={handleClick}
          disabled={!selectedId}
        >
          Generate heatmap
        </Button>
      </div>
      <div className="map-container">
        <MapWrapper features={features} />
      </div>
    </div>

    // <div>
    // {isAuthenticated ? (
    //   <div className="App">
    //     <div className="controls">
    //       <Dropdown onSelect={handleIdSelection} />
    //       <Button
    //         variant="contained"
    //         onClick={handleClick}
    //         disabled={!selectedId}
    //       >
    //         Generate heatmap
    //       </Button>
    //     </div>
    //     <div className="map-container">
    //       <MapWrapper features={features} />
    //     </div>
    //   </div>
    // ) : (
    //   <LoginForm onLogin={handleLogin} />
    // )}
    // </div>
  );
}

export default App;
