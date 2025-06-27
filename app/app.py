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
    ratings = rec.get_rating() if hasattr(rec, 'get_rating') else ["-"] * len(titles)
    release_years = rec.get_year() if hasattr(rec, 'get_year') else ["-"] * len(titles)
    durations = rec.get_duration() if hasattr(rec, 'get_duration') else ["-"] * len(titles)
    listed_ins = rec.get_listed_in() if hasattr(rec, 'get_listed_in') else ["-"] * len(titles)

    # Ottieni il type dal DataFrame, come per la barra di ricerca
    types = []
    for t in titles:
        row = df[df['title'] == t]
        if not row.empty and pd.notna(row.iloc[0]['type']):
            types.append(row.iloc[0]['type'])
        else:
            types.append("-")

    details = []
    for i in range(len(titles)):
        details.append({
            "type": types[i] if pd.notna(types[i]) else "-",
            "rating": ratings[i] if pd.notna(ratings[i]) else "-",
            "release_year": str(release_years[i]) if pd.notna(release_years[i]) else "-",
            "duration": durations[i] if pd.notna(durations[i]) else "-",
            "listed_in": listed_ins[i] if pd.notna(listed_ins[i]) else "-"
        })
    return jsonify({'titles': titles, 'details': details})

if __name__ == '__main__':
    app.run(debug=True)
