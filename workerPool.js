// workerPool.js
console.log("x")
export async function processRoutes(routes, callback) {
  // Create a pool of workers
  const numWorkers = navigator.hardwareConcurrency || 4; // Use the number of available cores or 4
  const workers = [];
  const tasks = [];
  
  // Create a pool of workers
  for (let i = 0; i < numWorkers; i++) {
    const worker = new Worker('worker.js');
    workers.push(worker);
  }

  // Distribute tasks
  const chunkSize = Math.ceil(routes.length / numWorkers);
  for (let i = 0; i < numWorkers; i++) {
    const chunk = routes.slice(i * chunkSize, (i + 1) * chunkSize);
    tasks.push(new Promise((resolve, reject) => {
      const worker = workers[i];
      worker.postMessage({ type: 'process', chunk });
      worker.onmessage = (event) => {
        resolve(event.data);
      };
      worker.onerror = (error) => {
        reject(error);
      };
    }));
  }

  try {
    const results = await Promise.all(tasks);
    const featureCollection = {
      type: 'FeatureCollection',
      features: results.flat()
    };
    callback(featureCollection);
  } catch (error) {
    console.error('Error processing routes:', error);
  } finally {
    workers.forEach(worker => worker.terminate());
  }
}
