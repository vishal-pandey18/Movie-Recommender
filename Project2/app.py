from flask import Flask, render_template, request, jsonify
from movie_process import recommend, new 
import pickle

app = Flask(__name__)

movies_df = pickle.load(open('movie_list.pkl','rb')) 
similarity = pickle.load(open('similarity.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/recommend', methods=['POST'])
def recommend_api():
    data = request.json
    query = data.get('query', '').strip()
    top_n = int(data.get('top_n', 5)) 

    recommendations = []

    if query == '':
        return jsonify([]) 
        
    if query in movies_df['title'].values:
        recommendations = recommend(query)
    else:
        genre = query.lower()
        genre_matches = movies_df[movies_df['tags'].str.contains(genre)]
        recommendations = genre_matches['title'].tolist()

    if not recommendations:
        return jsonify([])

    return jsonify(recommendations[:top_n])

if __name__ == "__main__":

    app.run(debug=True, threaded=True)
