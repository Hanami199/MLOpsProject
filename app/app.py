from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Sostituisci 'movies.csv' con il percorso reale del tuo file CSV
df = pd.read_csv('./movies.csv')  # Il CSV deve avere una colonna 'title'

@app.route('/movies')
def get_movies():
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify([])
    # Filtra i titoli che contengono la query
    results = df[df['title'].str.lower().str.contains(query)]
    # Restituisci solo i primi 10 risultati
    return jsonify(results['title'].head(10).tolist())

if __name__ == '__main__':
    app.run(debug=True)