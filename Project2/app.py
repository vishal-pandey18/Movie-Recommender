from flask import Flask, render_template, request, jsonify
from movie_process import recommend, new  # import your recommend function and movie DataFrame
import pickle

app = Flask(__name__)

# Load pickled data
movies_df = pickle.load(open('movie_list.pkl','rb'))  # your DataFrame
similarity = pickle.load(open('similarity.pkl','rb')) # cosine similarity matrix

# -------------------------------
# Home page
# -------------------------------
@app.route('/')
def home():
    return render_template('index.html')  # frontend HTML

# -------------------------------
# Recommendation API
# -------------------------------
@app.route('/recommend', methods=['POST'])
def recommend_api():
    data = request.json
    query = data.get('query', '').strip()
    top_n = int(data.get('top_n', 5))  # number of recommendations

    recommendations = []

    if query == '':
        return jsonify([])  # no input

    # Check if input is a movie title
    if query in movies_df['title'].values:
        recommendations = recommend(query)
    else:
        # Treat input as a genre
        genre = query.lower()
        genre_matches = movies_df[movies_df['tags'].str.contains(genre)]
        recommendations = genre_matches['title'].tolist()

    # If nothing found, return empty list
    if not recommendations:
        return jsonify([])

    # Return top N recommendations
    return jsonify(recommendations[:top_n])

# -------------------------------
# Run the app
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True, threaded=True)