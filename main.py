from flask import Flask, request, jsonify
import config

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    intent_name = req.get('queryResult', {}).get('intent', {}).get('displayName', '')
    
    response_text = "I am your AI Healthcare Assistant. How can I help you today?"
    
    if intent_name == "Symptom_Triage_Intent":
        parameters = req.get('queryResult', {}).get('parameters', {})
        symptom = parameters.get('symptom', '')
        
        if 'fever' in str(symptom).lower() or 'cold' in str(symptom).lower():
            response_text = f"Based on your symptoms, you should consult a {config.DEFAULT_DEPARTMENT}."
        elif 'chest' in str(symptom).lower():
            response_text = "⚠️ Chest pain can be serious. Please visit the Emergency department immediately!"
        else:
            response_text = f"Noted your symptoms regarding {symptom}."
            
    elif intent_name == "Book_Appointment_Intent":
        parameters = req.get('queryResult', {}).get('parameters', {})
        date = parameters.get('date', 'tomorrow')
        response_text = f"Your appointment has been successfully booked for {date}."

    return jsonify({
        "fulfillmentText": response_text
    })

if __name__ == '__main__':
    app.run(port=5000, debug=config.DEBUG_MODE)
