
from flask import Flask, request, jsonify
from meilisearch import Client

app = Flask(__name__)
meili_client = Client('http://127.0.0.1:7700')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    created_before = request.form.get('created_before', None)
    filters = request.form.getlist('filters', type=str)

    search_params = {'query': query}
    if created_before:
        search_params['filter'] = f'created_at < {created_before}'
    if filters:
        search_params['filter'] = ' AND '.join([f'{key}:{value}' for key, value in zip(filters[::2], filters[1::2])]

    results = meili_client.index('movies').search(search_params)

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
