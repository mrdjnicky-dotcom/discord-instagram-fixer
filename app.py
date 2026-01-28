from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# --- CONFIGURAZIONE ---
# Incolla qui sotto il tuo Webhook Discord tra le virgolette
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1465762210331496592/1_Q5DeYMoHNABKaCoUZJIEkdWR6MMqIgX64cFlngNVk6ZJaKomlUp1xNxnuZoPTeB4I0"
# ----------------------

@app.route('/', methods=['GET'])
def home():
    return "Il bot è attivo! Usa /webhook per inviare dati."

@app.route('/webhook', methods=['POST'])
def handle_instagram():
    # Riceviamo i dati da IFTTT
    data = request.json
    if not data:
        return jsonify({"error": "No JSON received"}), 400
        
    original_url = data.get('url', '')
    
    # Se non c'è URL, ci fermiamo
    if not original_url:
        return jsonify({"error": "No URL found"}), 400

    # LA CORREZIONE: Sostituiamo il dominio
    # Supportiamo sia instagram.com che instagr.am
    fixed_url = original_url.replace("instagram.com", "eeinstagram.com").replace("instagr.am", "eeinstagram.com")
    
    # Creiamo il messaggio per Discord
    payload = {
        "content": f"Nuovo post di Romagnoli Esports! 📸\n{fixed_url}"
    }
    
    # Inviamo a Discord
    try:
        print(f"Tentativo invio a Discord: {payload}")  # Debug 1
        r = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        print(f"Risposta Discord: {r.status_code} - {r.text}")  # Debug 2: FONDAMENTALE
        r.raise_for_status()
    except Exception as e:
        print(f"Errore invio Discord: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
