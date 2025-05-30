from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from analyzer import analyze_traffic
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, 
           static_folder='../frontend', 
           template_folder='../frontend')
CORS(app)

@app.route('/')
def index():
    """Page d'accueil - sert l'interface web"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_endpoint():
    """Endpoint pour analyser le trafic réseau"""
    try:
        data = request.get_json()
        
        if not data or 'features' not in data:
            return jsonify({
                'error': 'Données manquantes',
                'message': 'Le champ features est requis'
            }), 400
        
        features = data['features']
        analysis_mode = data.get('mode', 'detailed')
        
        logger.info(f"Analyse en cours - Mode: {analysis_mode}")
        
        # Appel à la fonction d'analyse
        result = analyze_traffic(features, analysis_mode)
        
        if not result:
            return jsonify({
                'error': 'Échec de l\'analyse',
                'message': 'Impossible d\'analyser les données fournies'
            }), 500
        
        logger.info("Analyse terminée avec succès")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {str(e)}")
        return jsonify({
            'error': 'Erreur serveur',
            'message': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérification de l'état du serveur"""
    return jsonify({
        'status': 'healthy',
        'message': 'Serveur opérationnel'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint non trouvé',
        'message': 'L\'URL demandée n\'existe pas'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Erreur serveur interne',
        'message': 'Une erreur inattendue s\'est produite'
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Démarrage du serveur sur le port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)