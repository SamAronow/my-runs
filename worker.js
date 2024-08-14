// worker.js

onmessage = function(event) {
    if (event.data.type === 'process') {
      const chunk = event.data.chunk;
      const features = chunk.map(route => ({
        type: 'Feature',
        properties: {
          name: route.features[0].start
        },
        geometry: {
          type: 'LineString',
          coordinates: route.features[0].geometry.coordinates[0]
        }
      }));
      postMessage(features);
    }
  };
  