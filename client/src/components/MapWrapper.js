
import React, { useState, useEffect, useRef } from "react";

import Map from "ol/Map";
import View from "ol/View";
import TileLayer from "ol/layer/Tile";
import Heatmap from "ol/layer/Heatmap";
import VectorSource from "ol/source/Vector";
import OSM from "ol/source/OSM";


function MapWrapper(props) {
  // set intial state
  const [map, setMap] = useState();
  const [heatmapLayer, setHeatmapLayer] = useState();

  // pull refs
  const mapElement = useRef();
  const mapRef = useRef();

  useEffect(() => {
    var heatMapSource = new VectorSource();
    var initheatmapLayer = new Heatmap({
      name: "Heatmap",
      source: heatMapSource,
      blur: 50,
      radius: 50,
      weight: function (feature) {
        return 1;
      },
    });

    var newMap = new Map({
      target: mapElement.current,
      layers: [
        new TileLayer({
          source: new OSM(),
        }),

        initheatmapLayer,
      ],
      view: new View({
        projection: "EPSG:3857",
        center: [0, 0],
        zoom: 2,
      }),
      controls: [],
    });
    mapRef.current = newMap;
    setMap(newMap);
    setHeatmapLayer(initheatmapLayer);
  }, []);

  useEffect(() => {
    if (props.features.length) {
      map.removeLayer(heatmapLayer);

      var heatMapSource = new VectorSource({ features: props.features });

      var newheatmapLayer = new Heatmap({
        source: heatMapSource,
        blur: 30,
        radius: 20,
        weight: function (feature) {
          return 1;
        },
      });
      map.addLayer(newheatmapLayer);
      setHeatmapLayer(newheatmapLayer);

      map.getView().fit(heatMapSource.getExtent(), {
        padding: [100, 100, 100, 100],
      });
    }
  }, [props.features]);

  return (
    <div>
      <div ref={mapElement} className="map-container"></div>
    </div>
  );
}

export default MapWrapper;
