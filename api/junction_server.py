import numpy as np
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

movies = pd.read_pickle('movies.pkl')


def movie_score(movie_params, user_happiness, user_bullets, user_brightness, user_sexuality):
    return 1. / 2 * 1. / movie_params['id'] + \
           user_happiness * movie_params['norm_emotions h/(h+s)'] + \
           user_brightness * movie_params['norm_brightness'] + \
           user_sexuality * movie_params['norm_nsfw'] + \
           1.2 * user_bullets * movie_params['norm_gunshots']


def get_top10(user_happiness, user_bullets, user_brightness, user_sexuality):
    scores = [movie_score(row, user_happiness, user_bullets, user_brightness, user_sexuality) for idx, row in
              movies.iterrows()]
    return np.argsort(scores)[::-1][:10]


@app.route('/api/get', methods=['GET'])
def get():
    param_names = ['happiness', 'bullets', 'brightness', 'sexuality']
    user_happiness, user_bullets, user_brightness, user_sexuality = [float(request.args.get(x)) / 50 - 1 for x in
                                                                     param_names]

    top10_idx = get_top10(user_happiness, user_bullets, user_brightness, user_sexuality)
    top10 = movies.iloc[top10_idx]

    result = [{
        'title': row['title'],
        'description': row['description'],
        'genre': row['genre'],
        'cover': row['img_url'],
        'year': row['year']
    } for idx, row in top10.iterrows()]
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8886')
