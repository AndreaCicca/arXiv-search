from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa la libreria CORS

app = Flask(__name__)
CORS(app)  # Abilita CORS per tutte le rotte e tutte le origini

@app.route('/query', methods=['POST', 'OPTIONS'])
def handle_query():
    if request.method == 'OPTIONS':
        # Gestisci la preflight request
        return '', 200

    data = request.json
    query = data.get('query')

    if not query:
        return jsonify({"error": "Il campo 'query' è obbligatorio"}), 400

    lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " \
                  "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."

    return jsonify({"response": lorem_ipsum})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
