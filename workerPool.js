// workerPool.js

const numberOfWorkers = navigator.hardwareConcurrency || 4;
const workers = [];

for (let i = 0; i < numberOfWorkers; i++) {
  workers.push(new Worker('worker.js'));
}

export function processRoutes(routes, callback) {
  let completedWorkers = 0;
  let featureCollections = [];
  const chunkSize = Math.ceil(routes.length / numberOfWorkers);

  workers.forEach((worker, index) => {
    const start = index * chunkSize;
    const end = Math.min(start + chunkSize, routes.length);
    const chunk = routes.slice(start, end);

    worker.onmessage = function(event) {
      featureCollections.push(event.data);
      completedWorkers++;

      if (completedWorkers === numberOfWorkers) {
        const mergedFeatureCollection = {
          "type": "FeatureCollection",
          "features": featureCollections.flatMap(fc => fc.features)
        };
        callback(mergedFeatureCollection);
      }
    };

    worker.postMessage({ routes: chunk });
  });
}
