from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def handle_query():
    # Ottieni il campo 'query' dal corpo della richiesta
    data = request.json
    query = data.get('query')

    # Verifica se il campo 'query' è presente
    if not query:
        return jsonify({"error": "Il campo 'query' è obbligatorio"}), 400

    # Risposta con un lorem ipsum
    lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " \
                  "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."

    return jsonify({"response": lorem_ipsum})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

