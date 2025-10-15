// async function fetchAndPlot(method) {
//     const response = await fetch("http://127.0.0.1:8000/reduce/pca", { method: "POST" , headers: {"Content-Type" : "application/json"}});
//     const data = await response.json();
//     console.log(data);
//     const trace = {
//         x: data.x,
//         y: data.y,
//         z: data.z,
//         mode: "markers",
//         marker: { size: 5, color: data.label, colorscale: "Viridis" },
//         type: "scatter3d"
//     };

//     Plotly.newPlot("plot", [trace], { title: "PCA en 3D" });
// }

// document.getElementById("btn-pca").onclick = () => fetchAndPlot("pca");
// document.getElementById("btn-tsne").onclick = () => fetchAndPlot("tsne");
// document.getElementById("btn-umap").onclick = () => fetchAndPlot("umap");

// ------------------------------------------

const API_URL = "http://127.0.0.1:5500/reduce"; // Backend FastAPI

async function fetchAndPlot(method) {
  try {
    const response = await fetch(`${API_URL}/${method}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dataset: "iris" }), // exemple dataset
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP : ${response.status}`);
    }

    const data = await response.json();
    console.log("Réponse API :", data);

    // Récupération des coordonnées et labels envoyés par l’API
    const x = data.x;
    const y = data.y;
    const z = data.z ?? null; // si 3D
    const labels = data.labels ?? [];

    // Création du graphe Plotly
    let trace;
    if (z) {
      trace = {
        x,
        y,
        z,
        mode: "markers",
        type: "scatter3d",
        marker: { size: 5, color: labels, colorscale: "Viridis" },
      };
    } else {
      trace = {
        x,
        y,
        mode: "markers",
        type: "scatter",
        marker: { size: 8, color: labels, colorscale: "Viridis" },
      };
    }

    Plotly.newPlot("plot", [trace], {
      title: `Résultat ${method.toUpperCase()}`,
      margin: { t: 40 },
      scene: z ? { aspectmode: "cube" } : undefined,
    });
  } catch (error) {
    console.error("Erreur lors du fetch :", error);
  }
}
