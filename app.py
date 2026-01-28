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
    # STAMPA TUTTO QUELLO CHE ARRIVA (DEBUG)
    print("Dati ricevuti grezzi:", request.data)
    try:
        data = request.json
        print("JSON parsato:", data)
    except:
        print("Errore nel parsing JSON")
        data = {}

    # Se non troviamo l'url, usiamo un link di fallback per TESTARE DISCORD
    original_url = data.get('url', 'https://instagram.com/p/LINK-DI-EMERGENZA-TEST')
    
    print(f"URL elaborato: {original_url}")

    # LA CORREZIONE
    fixed_url = original_url.replace("instagram.com", "eeinstagram.com").replace("instagr.am", "eeinstagram.com")
    
    payload = {
        "content": f"Nuovo post (DEBUG)! 📸\n{fixed_url}"
    }
    
    # Inviamo a Discord
    print(f"Tentativo invio a Discord a: {DISCORD_WEBHOOK_URL}")
    try:
        r = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        print(f"Risposta Discord: {r.status_code} - {r.text}")
        r.raise_for_status()
    except Exception as e:
        print(f"Errore invio Discord: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
    return jsonify({"status": "success", "fixed_url": fixed_url}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
