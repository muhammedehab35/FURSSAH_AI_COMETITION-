import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()

# ⚠️ SÉCURITÉ: Ne jamais exposer votre clé API dans le code
# Utilisez uniquement les variables d'environnement
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_traffic(flow_features: str) -> dict:
    prompt = f"""
You are a cybersecurity expert analyzing network traffic flows.

Given the following raw flow features, return a detailed JSON response with:
- origin (e.g., botnet, legitimate_client, unknown)
- traffic_type (malicious, benign, suspicious)
- generation_type (bot, human, unknown)
- anomalies (detailed list of anomalies found)
- threats (e.g., DDoS, port scan, brute force, data exfiltration, none)
- severity (low, medium, high, critical)
- confidence (float between 0 and 1)
- explanation (a paragraph explaining why it is classified this way)
- protocol (TCP/UDP/ICMP if detectable)
- flow_direction (unidirectional, bidirectional, unknown)
- risk_score (from 0 to 100 based on threat and severity)
- recommended_action (e.g., block IP, investigate further, allow)

Input: {flow_features}

Return only the JSON object, no commentary or explanation.
"""

    try:
        # Utilisation de la nouvelle API OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        
        content = response.choices[0].message.content
        
        # Tentative de parsing JSON
        return json.loads(content)
        
    except json.JSONDecodeError as e:
        print(f"⚠️ Erreur JSON: {e}")
        print("Réponse brute reçue:")
        print(content)
        return {}
    except Exception as e:
        print(f"⚠️ Erreur lors de l'appel API: {e}")
        return {}

# 🧪 Exemple d'usage avec des features réseau simulées
if __name__ == "__main__":
    features = """
    Destination Port: 55153, Flow Duration: 4, Total Fwd Packets: 2, 
    Total Backward Packets: 0, Total Length of Fwd Packets: 37, 
    Total Length of Bwd Packets: 0, Fwd Packet Length Max: 31, 
    Fwd Packet Length Min: 6, Fwd Packet Length Mean: 18.5, 
    Flow Bytes/s: 9250000, Flow Packets/s: 500000, SYN Flag Count: 1, 
    ACK Flag Count: 1, URG Flag Count: 0, PSH Flag Count: 0, 
    Bwd Packet Length Mean: 0, Down/Up Ratio: 0, Average Packet Size: 34
    """
    
    result = analyze_traffic(features)
    if result:
        print("🔍 Analyse du trafic réseau:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("❌ Échec de l'analyse")