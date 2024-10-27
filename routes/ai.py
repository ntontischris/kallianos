from flask import Blueprint, jsonify, request
from services.ai_service import get_ai_response, generate_study_material

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/ai/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')
    if not message:
        return jsonify({'error': 'No message provided'}), 400
        
    response = get_ai_response(message)
    return jsonify({'response': response})

@ai_bp.route('/ai/generate-content', methods=['POST'])
def generate_content():
    data = request.json
    topic = data.get('topic')
    content_type = data.get('type', 'summary')
    
    if not topic:
        return jsonify({'error': 'No topic provided'}), 400
        
    content = generate_study_material(topic, content_type)
    return jsonify({'content': content})
