from flask import Blueprint, jsonify, request
from services.ai_service import get_ai_response, generate_study_material, analyze_sentiment, recommend_learning_path, generate_quiz, translate_content, tutoring_assistance, interactive_simulation, track_progress, analyze_feedback, recommend_content, voice_interaction, ai_assessment, personalized_notifications, adaptive_learning, real_time_collaboration, ai_insights, automated_grading, intelligent_search, ai_recommendations, predictive_analytics, ai_alerts, smart_scheduling, ai_diagnostics, virtual_assistant, ai_personalization

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

@ai_bp.route('/ai/analyze-sentiment', methods=['POST'])
def analyze_sentiment_route():
    data = request.json
    message = data.get('message')
    if not message:
        return jsonify({'error': 'No message provided'}), 400
        
    sentiment = analyze_sentiment(message)
    return jsonify({'sentiment': sentiment})

@ai_bp.route('/ai/recommend-learning-path', methods=['POST'])
def recommend_learning_path_route():
    data = request.json
    user_profile = data.get('user_profile')
    if not user_profile:
        return jsonify({'error': 'No user profile provided'}), 400
        
    learning_path = recommend_learning_path(user_profile)
    return jsonify({'learning_path': learning_path})

@ai_bp.route('/ai/generate-quiz', methods=['POST'])
def generate_quiz_route():
    data = request.json
    user_learning_history = data.get('user_learning_history')
    if not user_learning_history:
        return jsonify({'error': 'No user learning history provided'}), 400
        
    quiz = generate_quiz(user_learning_history)
    return jsonify({'quiz': quiz})

@ai_bp.route('/ai/translate-content', methods=['POST'])
def translate_content_route():
    data = request.json
    content = data.get('content')
    target_language = data.get('target_language')
    if not content or not target_language:
        return jsonify({'error': 'Content and target language must be provided'}), 400
        
    translated_content = translate_content(content, target_language)
    return jsonify({'translated_content': translated_content})

@ai_bp.route('/ai/tutoring-assistance', methods=['POST'])
def tutoring_assistance_route():
    data = request.json
    query = data.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
        
    assistance = tutoring_assistance(query)
    return jsonify({'assistance': assistance})

@ai_bp.route('/ai/interactive-simulation', methods=['POST'])
def interactive_simulation_route():
    data = request.json
    topic = data.get('topic')
    if not topic:
        return jsonify({'error': 'No topic provided'}), 400
        
    simulation = interactive_simulation(topic)
    return jsonify({'simulation': simulation})

@ai_bp.route('/ai/track-progress', methods=['POST'])
def track_progress_route():
    data = request.json
    user_activity = data.get('user_activity')
    if not user_activity:
        return jsonify({'error': 'No user activity provided'}), 400
        
    progress = track_progress(user_activity)
    return jsonify({'progress': progress})

@ai_bp.route('/ai/analyze-feedback', methods=['POST'])
def analyze_feedback_route():
    data = request.json
    feedback = data.get('feedback')
    if not feedback:
        return jsonify({'error': 'No feedback provided'}), 400
        
    insights = analyze_feedback(feedback)
    return jsonify({'insights': insights})

@ai_bp.route('/ai/recommend-content', methods=['POST'])
def recommend_content_route():
    data = request.json
    user_interests = data.get('user_interests')
    if not user_interests:
        return jsonify({'error': 'No user interests provided'}), 400
        
    recommendations = recommend_content(user_interests)
    return jsonify({'recommendations': recommendations})

@ai_bp.route('/ai/voice-interaction', methods=['POST'])
def voice_interaction_route():
    data = request.json
    audio_input = data.get('audio_input')
    if not audio_input:
        return jsonify({'error': 'No audio input provided'}), 400
        
    response = voice_interaction(audio_input)
    return jsonify({'response': response})

@ai_bp.route('/ai/ai-assessment', methods=['POST'])
def ai_assessment_route():
    data = request.json
    user_responses = data.get('user_responses')
    if not user_responses:
        return jsonify({'error': 'No user responses provided'}), 400
        
    assessment = ai_assessment(user_responses)
    return jsonify({'assessment': assessment})

@ai_bp.route('/ai/personalized-notifications', methods=['POST'])
def personalized_notifications_route():
    data = request.json
    user_activity = data.get('user_activity')
    if not user_activity:
        return jsonify({'error': 'No user activity provided'}), 400
        
    notifications = personalized_notifications(user_activity)
    return jsonify({'notifications': notifications})

@ai_bp.route('/ai/adaptive-learning', methods=['POST'])
def adaptive_learning_route():
    data = request.json
    user_performance = data.get('user_performance')
    if not user_performance:
        return jsonify({'error': 'No user performance provided'}), 400
        
    adapted_content = adaptive_learning(user_performance)
    return jsonify({'adapted_content': adapted_content})

@ai_bp.route('/ai/real-time-collaboration', methods=['POST'])
def real_time_collaboration_route():
    data = request.json
    session_data = data.get('session_data')
    if not session_data:
        return jsonify({'error': 'No session data provided'}), 400
        
    collaboration = real_time_collaboration(session_data)
    return jsonify({'collaboration': collaboration})

@ai_bp.route('/ai/ai-insights', methods=['POST'])
def ai_insights_route():
    data = request.json
    data_input = data.get('data')
    if not data_input:
        return jsonify({'error': 'No data provided'}), 400
        
    insights = ai_insights(data_input)
    return jsonify({'insights': insights})

@ai_bp.route('/ai/automated-grading', methods=['POST'])
def automated_grading_route():
    data = request.json
    submissions = data.get('submissions')
    if not submissions:
        return jsonify({'error': 'No submissions provided'}), 400
        
    grading = automated_grading(submissions)
    return jsonify({'grading': grading})

@ai_bp.route('/ai/intelligent-search', methods=['POST'])
def intelligent_search_route():
    data = request.json
    query = data.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
        
    search_results = intelligent_search(query)
    return jsonify({'search_results': search_results})

@ai_bp.route('/ai/ai-recommendations', methods=['POST'])
def ai_recommendations_route():
    data = request.json
    user_data = data.get('user_data')
    if not user_data:
        return jsonify({'error': 'No user data provided'}), 400
        
    recommendations = ai_recommendations(user_data)
    return jsonify({'recommendations': recommendations})

@ai_bp.route('/ai/predictive-analytics', methods=['POST'])
def predictive_analytics_route():
    data = request.json
    data_input = data.get('data')
    if not data_input:
        return jsonify({'error': 'No data provided'}), 400
        
    predictions = predictive_analytics(data_input)
    return jsonify({'predictions': predictions})

@ai_bp.route('/ai/ai-alerts', methods=['POST'])
def ai_alerts_route():
    data = request.json
    data_input = data.get('data')
    if not data_input:
        return jsonify({'error': 'No data provided'}), 400
        
    alerts = ai_alerts(data_input)
    return jsonify({'alerts': alerts})

@ai_bp.route('/ai/smart-scheduling', methods=['POST'])
def smart_scheduling_route():
    data = request.json
    events = data.get('events')
    if not events:
        return jsonify({'error': 'No events provided'}), 400
        
    schedule = smart_scheduling(events)
    return jsonify({'schedule': schedule})

@ai_bp.route('/ai/ai-diagnostics', methods=['POST'])
def ai_diagnostics_route():
    data = request.json
    symptoms = data.get('symptoms')
    if not symptoms:
        return jsonify({'error': 'No symptoms provided'}), 400
        
    diagnostics = ai_diagnostics(symptoms)
    return jsonify({'diagnostics': diagnostics})

@ai_bp.route('/ai/virtual-assistant', methods=['POST'])
def virtual_assistant_route():
    data = request.json
    request_content = data.get('request')
    if not request_content:
        return jsonify({'error': 'No request provided'}), 400
        
    assistance = virtual_assistant(request_content)
    return jsonify({'assistance': assistance})

@ai_bp.route('/ai/ai-personalization', methods=['POST'])
def ai_personalization_route():
    data = request.json
    user_data = data.get('user_data')
    if not user_data:
        return jsonify({'error': 'No user data provided'}), 400
        
    personalization = ai_personalization(user_data)
    return jsonify({'personalization': personalization})
