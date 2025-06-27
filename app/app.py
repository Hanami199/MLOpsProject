from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.backend import ModelRecommendation

app = Flask(__name__)
CORS(app)

csv_path = 'data/netflix_titles.csv'
df = pd.read_csv(csv_path)

@app.route('/movies')
def get_movies():
    query = request.args.get('query', '').strip().lower()
    if not query:
        return jsonify([])

    # Titoli esatti (case-insensitive)
    exact_matches = df[df['title'].str.lower() == query][['title', 'type']].to_dict(orient='records')
    # Titoli che contengono la query ma non sono esatti
    contains_matches = df[
        (df['title'].str.lower().str.contains(query, na=False)) &
        (df['title'].str.lower() != query)
    ][['title', 'type']].to_dict(orient='records')

    # Unisci, esatti prima, poi i parziali, e limita a 10 risultati
    results = (exact_matches + contains_matches)[:10]
    return jsonify(results)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    algorithm = data.get('algorithm', 'MLOVIE')
    movies = data.get('movies', [])
    rec = ModelRecommendation(model_type=algorithm, film_list_titles=movies)
    titles = rec.get_title()
    # Recupera dettagli per ogni titolo
    details = []
    for t in titles:
        row = df[df['title'] == t]
        if not row.empty:
            r = row.iloc[0]
            details.append({
                "type": r['type'].strip().lower() if pd.notna(r['type']) else "-",
                "rating": r['rating'] if pd.notna(r['rating']) else "-",
                "release_year": str(r['release_year']) if pd.notna(r['release_year']) else "-",
                "duration": r['duration'] if pd.notna(r['duration']) else "-",
                "listed_in": r['listed_in'] if pd.notna(r['listed_in']) else "-"
            })
        else:
            details.append({
                "type": "-",
                "rating": "-",
                "release_year": "-",
                "duration": "-",
                "listed_in": "-"
            })
    return jsonify({'titles': titles, 'details': details})

if __name__ == '__main__':
    app.run(debug=True)
