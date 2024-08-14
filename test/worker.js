// worker.js

self.onmessage = function(event) {
    const { routes } = event.data;
    const featureCollection = {
      "type": "FeatureCollection",
      "features": []
    };
  
    // Process routes and build GeoJSON features
    for (let i = 0; i < routes.length; i++) {
      let route = routes[i];
      featureCollection.features.push({
        "type": "Feature",
        "properties": {
          "name": route.features[0].start
        },
        "geometry": {
          "type": "LineString",
          "coordinates": route.features[0].geometry.coordinates[0]
        }
      });
    }
  
    // Post the featureCollection back to the main thread
    self.postMessage(featureCollection);
  };
  