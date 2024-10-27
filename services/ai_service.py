import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def get_ai_response(prompt, context="educational"):
    """Get AI response for educational queries"""
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful educational assistant. Provide clear, concise answers suitable for students."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Sorry, I couldn't process your request at the moment. Please try again later."

def generate_study_material(topic, type="summary"):
    """Generate educational content for teachers"""
    try:
        prompt = f"Create a detailed {type} about {topic} suitable for students."
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert teacher creating educational content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Sorry, I couldn't generate the content at the moment. Please try again later."
