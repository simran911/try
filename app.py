from flask import Flask, request, jsonify, render_template  # Added render_template
from flask_cors import CORS
import groq
import json
from config import Config
from datetime import datetime
import os
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load configuration
app.config.from_object(Config)

# Load personal information
with open('personal_info.json', 'r') as f:
    PERSONAL_INFO = json.load(f)

# Initialize Groq client
client = groq.Client(api_key=app.config['GROQ_API_KEY'])

def generate_prompt(user_query):
    """Generate the system prompt with Simran Kumari's professional information"""
    experience_str = "\n".join(
        f"- {exp['role']} at {exp['company']} ({exp['years']})"
        for exp in PERSONAL_INFO['experience']
    )
    
    return f"""You are a professional AI assistant representing Simran Kumari, an AI Engineer. 
Your responses must be:
- Strictly based on the provided information below
- Professional yet approachable in tone
- Concise (1-2 paragraphs maximum)
- Redirect personal questions to professional topics

Professional Background:
Name: {PERSONAL_INFO['name']}
Profession: {PERSONAL_INFO['profession']}

Technical Skills:
{', '.join(PERSONAL_INFO['skills'])}

Professional Experience:
{experience_str}

Education:
- {PERSONAL_INFO['education']}

Contact Information:
- Email: {PERSONAL_INFO['contact']['email']}
- LinkedIn: {PERSONAL_INFO['contact']['linkedin']}
- GitHub: {PERSONAL_INFO['contact']['github']}

Current Date: {datetime.now().strftime('%B %d, %Y')}

Response Guidelines:
1. Focus exclusively on professional queries about Simran's AI/ML experience
2. For skills inquiries, highlight relevant technologies
3. When discussing experience, mention companies and durations
4. For non-professional queries, respond: "I specialize in discussing Simran's professional background as an AI engineer."

User Question: {user_query}

Professional Response:"""

@app.route('/')
def home():
    # Get basic info for the template
    basic_info = {
        'name': PERSONAL_INFO['name'],
        'profession': PERSONAL_INFO['profession'],
        'avatar_text': PERSONAL_INFO['name'][0]
    }
    return render_template('index.html', personal_info=basic_info)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_query = data.get('message', '').strip()
        
        if not user_query:
            return jsonify({'error': 'Empty message'}), 400

        # Generate prompt with context
        prompt = generate_prompt(user_query)

        # Get response from Groq
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=app.config['MODEL_NAME'],
            temperature=app.config['TEMPERATURE'],
            max_tokens=app.config['MAX_TOKENS']
        )

        # Extract and clean the response
        bot_response = response.choices[0].message.content
        bot_response = bot_response.replace("Answer:", "").strip()

        return jsonify({
            'response': bot_response,
            'status': 'success'
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'response': "Sorry, I'm having trouble responding right now.",
            'status': 'error'
        }), 500

@app.route('/personal_info', methods=['GET'])
def get_personal_info():
    """Endpoint to get basic personal info for the frontend"""
    return jsonify({
        'name': PERSONAL_INFO['name'],
        'profession': PERSONAL_INFO['profession'],
        'avatar_text': PERSONAL_INFO['name'][0]  # First letter for avatar
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)  # Disable debug mode!