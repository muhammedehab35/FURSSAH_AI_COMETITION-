// Configuration de l'API
const API_BASE_URL = window.location.origin;

// Données d'exemple pour les tests
const sampleData = `Destination Port: 55153, Flow Duration: 4, Total Fwd Packets: 2, Total Backward Packets: 0, Total Length of Fwd Packets: 37, Total Length of Bwd Packets: 0, Fwd Packet Length Max: 31, Fwd Packet Length Min: 6, Fwd Packet Length Mean: 18.5, Flow Bytes/s: 9250000, Flow Packets/s: 500000, SYN Flag Count: 1, ACK Flag Count: 1, URG Flag Count: 0, PSH Flag Count: 0, Bwd Packet Length Mean: 0, Down/Up Ratio: 0, Average Packet Size: 34`;

/**
 * Charge les données d'exemple dans le textarea
 */
function loadSampleData() {
    document.getElementById('traffic-data').value = sampleData;
    showNotification('Données d\'exemple chargées!', 'success');
}

/**
 * Fonction principale d'analyse du trafic
 */
async function analyzeTraffic() {
    const trafficData = document.getElementById('traffic-data').value.trim();
    const analysisMode = document.getElementById('analysis-mode').value;
}