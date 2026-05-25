import sqlparse
import re
import joblib

# Load ML model
model = joblib.load('model/query_model.pkl')


def extract_features(query):

    query_upper = query.upper()

    joins = query_upper.count('JOIN')

    has_where = 1 if 'WHERE' in query_upper else 0

    has_orderby = 1 if 'ORDER BY' in query_upper else 0

    select_all = 1 if 'SELECT *' in query_upper else 0

    like_wildcard = 1 if re.search(
        r"LIKE\\s+'%.*%'",
        query_upper
    ) else 0

    query_length = len(query)

    return [[
        joins,
        has_where,
        has_orderby,
        select_all,
        like_wildcard,
        query_length
    ]]


def calculate_score(query):

    score = 100

    query_upper = query.upper()

    if 'SELECT *' in query_upper:
        score -= 15

    if 'JOIN' in query_upper:
        score -= 10

    if 'ORDER BY' in query_upper:
        score -= 10

    if re.search(r"LIKE\\s+'%.*%'", query_upper):
        score -= 25

    if 'WHERE' not in query_upper:
        score -= 20

    return max(score, 0)


def analyze_query(query):

    suggestions = []

    optimized_query = query

    features = extract_features(query)

    prediction = model.predict(features)[0]

    if 'SELECT *' in query.upper():

        suggestions.append(
            'Avoid SELECT *. Fetch only needed columns.'
        )

        optimized_query = optimized_query.replace('*', 'id')

    if 'WHERE' not in query.upper():

        suggestions.append(
            'Missing WHERE clause may scan full table.'
        )

    if re.search(r"LIKE\\s+'%.*%'", query.upper()):

        suggestions.append(
            'Leading wildcard prevents indexing.'
        )

    if 'ORDER BY' in query.upper():

        suggestions.append(
            'Create index on ORDER BY column.'
        )

    if 'JOIN' in query.upper():

        suggestions.append(
            'Index JOIN columns.'
        )

    score = calculate_score(query)

    return {
        'original_query': query,
        'optimized_query': optimized_query,
        'prediction': prediction,
        'score': score,
        'suggestions': suggestions
    }