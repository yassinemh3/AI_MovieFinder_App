from flask import Flask, render_template, request
import rdflib
from flask import jsonify
from recommendations_model import recommend,load_data,before_serevr

# from recommendations_model import load_data,recommend
app = Flask(__name__)

# Initialize RDF graph and parse RDF data file
g = rdflib.Graph()
g.parse("IAI_Team4_MovieFinder/TMDB.ttl", format='turtle')
nn_model,movies=before_serevr()
# Initialize variables to store search type and query
search_type = "title"
search_query = ""

def search_overview_content(words) -> list:
    global g
    query = """
    PREFIX : <https://www.themoviedb.org/kaggle-export/> 
    SELECT ?movie_title
    WHERE {
        ?movie a :Movie;
            :overview ?overview;
            :title ?movie_title.
        FILTER(STRLEN(?overview) > 0 && CONTAINS(UCASE(?overview), UCASE("%s")))
    }""" % words.upper()

    query_result = g.query(query)

    result = [str(row[0]) for row in query_result]

    return result


def search_overview(title) -> list:
    global g
    query = """
    PREFIX : <https://www.themoviedb.org/kaggle-export/> 
    SELECT ?overview
    WHERE {
        ?movie a :Movie;
            :overview ?overview;
            :title ?movie_title.
        FILTER(CONTAINS(UCASE(?movie_title), UCASE("%s")))
    }""" % title.upper()

    query_result = g.query(query)

    result = [row[0] for row in query_result]

    return result


def search_title(title) -> list:
    global g
    query = """
    PREFIX : <https://www.themoviedb.org/kaggle-export/> 
    SELECT ?movie_title
    WHERE {
        ?movie a :Movie;
            :title ?movie_title.
        FILTER(CONTAINS(UCASE(?movie_title), UCASE("%s")))
    }""" % title.upper()

    query_result = g.query(query)

    result = [row[0] for row in query_result]

    return result


def actor_search(title) -> list:
    global g
    query = f"""
    PREFIX : <https://www.themoviedb.org/kaggle-export/> 
    SELECT ?actor
    WHERE {{
        ?movie a :Movie;
            :title "{title}";
            :cast/:name ?actor.
    }}"""

    query_result = g.query(query)
    result = [row[0] for row in query_result]
    return result


def recommended_titles(title) -> list:
    return recommend(title, nn_model,movies)

@app.route("/getOverview")
def getOverview():
    title = request.args.get("title")
    overview = search_overview(title)
    return jsonify(overview)


# Define routes
@app.route("/")
def index():
    return render_template("index.html", title="Find The Movie with AI", search_type=search_type, search_query=search_query)
@app.route("/search", methods=["POST"])
def search():
    global search_type
    global search_query
    search_result = []
    # Get the search type and query from the form
    search_type = request.form["search_type"]
    search_query = request.form["search_query"]
    print(search_type)
    print(search_query)

    if search_type == "title":
        try:
            print("searching title")
            title_result = recommended_titles(search_query)
            # title_result_strings = [title for title in title_result]
            search_result = title_result
            print(title_result)
        except ValueError:
            print("No results found")

    elif search_type == "actor":
        try:
            print("searching actor")
            actor_result = actor_search(search_query)
            actor_result_strings = [title.toPython() for title in actor_result]
            search_result = actor_result_strings
            print(actor_result_strings)
        except ValueError:
            print("No results found")

    elif search_type == "overview":
        try:
            print("searching overview")
            overview_result = search_overview(search_query)
            overview_result_strings = [overview.toPython() for overview in overview_result]
            search_result = overview_result_strings
            print(overview_result_strings)
        except ValueError:
            print("No results found")

    elif search_type == "overview_content":
        try:
            print("searching overview_content")
            overview_content_result = search_overview_content(search_query)
            print(overview_content_result)
            search_result = overview_content_result
            print(overview_content_result)
        except ValueError:
            print("No results found")
    else:
        search_result = []  # Handle other search types here if needed

    return render_template("index.html", title="Find The Movie with AI", search_type=search_type, search_query=search_query, search_result=search_result)


# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
