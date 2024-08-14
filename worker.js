// Listen for messages from the main thread
self.addEventListener('message', function(event) {
    const routes = event.data;
    const featureCollection = {
        "type": "FeatureCollection",
        "features": []
    };

    // Process each route
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

    // Send the processed data back to the main thread
    self.postMessage(featureCollection);
});
