import openai
import os
import json
import logging
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration du logging
logger = logging.getLogger(__name__)

# Configuration OpenAI
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_traffic(flow_features: str, mode: str = "detailed") -> dict:
    """
    Analyse le trafic réseau en utilisant OpenAI GPT
    
    Args:
        flow_features (str): Features du flux réseau
        mode (str): Mode d'analyse (detailed, quick, threat-focused)
    
    Returns:
        dict: Résultats de l'analyse
    """
    
    # Adapter le prompt selon le mode
    prompt = create_prompt(flow_features, mode)
    
    try:
        logger.info(f"Envoi de la requête à OpenAI - Mode: {mode}")
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=1500
        )
        
        content = response.choices[0].message.content
        logger.info("Réponse reçue d'OpenAI")
        
        # Parser la réponse JSON
        result = json.loads(content)
        
        # Validation et nettoyage des données
        result = validate_and_clean_result(result)
        
        return result
        
    except json.JSONDecodeError as e:
        logger.error(f"Erreur de parsing JSON: {e}")
        logger.error(f"Contenu reçu: {content}")
        return create_fallback_result(flow_features)
        
    except Exception as e:
        logger.error(f"Erreur lors de l'appel OpenAI: {e}")
        return create_fallback_result(flow_features)

def create_prompt(flow_features: str, mode: str) -> str:
    """Crée le prompt adapté au mode d'analyse"""
    
    base_fields = """
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
"""
    
    if mode == "quick":
        prompt = f"""
You are a cybersecurity expert. Analyze this network flow quickly and return a JSON with these essential fields:
- traffic_type, severity, risk_score, threats, recommended_action, confidence

Input: {flow_features}

Return only the JSON object.
"""
    elif mode == "threat-focused":
        prompt = f"""
You are a cybersecurity expert focusing on threat detection. Analyze this network flow for malicious activity and return a detailed JSON with:
{base_fields}

Focus particularly on identifying potential threats, attack patterns, and security risks.

Input: {flow_features}

Return only the JSON object.
"""
    else:  # detailed mode
        prompt = f"""
You are a cybersecurity expert analyzing network traffic flows.

Given the following raw flow features, return a detailed JSON response with:
{base_fields}

Input: {flow_features}

Return only the JSON object, no commentary or explanation.
"""
    
    return prompt

def validate_and_clean_result(result: dict) -> dict:
    """Valide et nettoie les résultats de l'analyse"""
    
    # Champs obligatoires avec valeurs par défaut
    defaults = {
        'origin': 'unknown',
        'traffic_type': 'unknown',
        'generation_type': 'unknown',
        'anomalies': [],
        'threats': [],
        'severity': 'low',
        'confidence': 0.5,
        'explanation': 'Analyse automatique du trafic réseau.',
        'protocol': 'unknown',
        'flow_direction': 'unknown',
        'risk_score': 0,
        'recommended_action': 'monitor'
    }
    
    # Appliquer les valeurs par défaut
    for key, default_value in defaults.items():
        if key not in result:
            result[key] = default_value
    
    # Validation des types
    if not isinstance(result['anomalies'], list):
        result['anomalies'] = [str(result['anomalies'])] if result['anomalies'] else []
    
    if not isinstance(result['threats'], list):
        result['threats'] = [str(result['threats'])] if result['threats'] else []
    
    # Validation des valeurs numériques
    try:
        result['confidence'] = max(0, min(1, float(result['confidence'])))
        result['risk_score'] = max(0, min(100, int(result['risk_score'])))
    except (ValueError, TypeError):
        result['confidence'] = 0.5
        result['risk_score'] = 50
    
    # Validation du niveau de sévérité
    valid_severities = ['low', 'medium', 'high', 'critical']
    if result['severity'] not in valid_severities:
        result['severity'] = 'low'
    
    return result

def create_fallback_result(flow_features: str) -> dict:
    """Crée un résultat de secours en cas d'échec de l'API"""
    
    logger.warning("Utilisation du résultat de secours")
    
    # Analyse basique basée sur des heuristiques simples
    risk_score = analyze_basic_features(flow_features)
    
    if risk_score > 70:
        severity = 'high'
        traffic_type = 'suspicious'
        recommended_action = 'investigate further'
    elif risk_score > 40:
        severity = 'medium'
        traffic_type = 'suspicious'
        recommended_action = 'monitor closely'
    else:
        severity = 'low'
        traffic_type = 'benign'
        recommended_action = 'allow'
    
    return {
        'origin': 'laptop MAC',
        'traffic_type': traffic_type,
        'generation_type': '11',
        'anomalies': ['Analyse de secours - données limitées'],
        'threats': ['unknown'],
        'severity': severity,
        'confidence': 0.3,
        'explanation': 'Analyse de secours effectuée suite à un problème avec le service principal.',
        'protocol': 'unknown',
        'flow_direction': 'unknown',
        'risk_score': risk_score,
        'recommended_action': recommended_action
    }

def analyze_basic_features(flow_features: str) -> int:
    """Analyse basique pour calculer un score de risque"""
    
    risk_score = 0
    features_lower = flow_features.lower()
    
    # Heuristiques simples
    if 'packets/s: 5000' in features_lower or 'flow packets/s: 5000' in features_lower:
        risk_score += 30
    
    if 'syn flag count: 1' in features_lower and 'ack flag count: 0' in features_lower:
        risk_score += 25
    
    if 'total backward packets: 0' in features_lower:
        risk_score += 20
    
    if any(port in features_lower for port in ['port: 22', 'port: 23', 'port: 445']):
        risk_score += 15
    
    return min(100, risk_score)

def get_sample_analysis() -> dict:
    """Retourne un exemple d'analyse pour les tests"""
    
    return {
        'origin': 'unknown',
        'traffic_type': 'suspicious',
        'generation_type': 'bot',
        'anomalies': [
            'Taux de paquets anormalement élevé (500K pps)',
            'Flux unidirectionnel inhabituel',
            'Port de destination non standard'
        ],
        'threats': ['port scan', 'potential DDoS'],
        'severity': 'high',
        'confidence': 0.85,
        'explanation': 'Ce flux présente des caractéristiques suspectes avec un taux de paquets extrêmement élevé et une communication unidirectionnelle, suggérant une activité de reconnaissance ou une tentative d\'attaque DDoS.',
        'protocol': 'TCP',
        'flow_direction': 'unidirectional',
        'risk_score': 75,
        'recommended_action': 'investigate further'
    }