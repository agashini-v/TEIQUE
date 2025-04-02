app.py

from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if you're using AI)
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# API Key for AI services (e.g., Gemini 2.0 or any other API service)
API_KEY = os.getenv("GEMINI_API_KEY")  # Optional for AI analysis

# Route to render the questionnaire page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the submission of the questionnaire
@app.route('/submit', methods=['POST'])
def submit():
    # Get the responses from the form (30 questions)
    responses = [int(request.form[f'q{i}']) for i in range(1, 31)]

    # Calculate emotional intelligence score
    score, feedback = calculate_emotional_intelligence(responses)

    # Return the score and feedback as JSON (for display)
    return jsonify({
        'score': score,
        'feedback': feedback
    })

# Function to calculate the emotional intelligence score
def calculate_emotional_intelligence(responses):
    reverse_scoring_questions = [
        1, 2, 4, 5, 7, 8, 10, 12, 13, 14, 16, 18, 22, 25, 26, 28
    ]
    total_score = 0

    for idx, response in enumerate(responses):
        if idx in reverse_scoring_questions:
            total_score += (8 - response)  # Reverse scoring
        else:
            total_score += response

    feedback = generate_feedback(total_score)
    return total_score, feedback

# Function to generate feedback based on score
def generate_feedback(score):
    if score < 100:
        return "Your emotional intelligence could benefit from focusing on emotional regulation and self-awareness."
    elif score < 150:
        return "You have a moderate level of emotional intelligence. Focus on enhancing your social skills and emotional resilience."
    else:
        return "You exhibit a high level of emotional intelligence. Keep nurturing your skills and further develop your emotional resilience!"

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
