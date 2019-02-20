# Developer -- hasmeed
# Git https://github.com/hasmeed
# Mail: hasmeedcoder@gmail.com

import pandas as pd


def recommendmovie():
    movie_title = str(input("Enter the movie title:"))

    column_names = ["user_id", "item_id", "rating", "timestamp"]
    path = "file.tsv"
    df = pd.read_csv(path, sep="\t", names=column_names)

    movie_titles = pd.read_csv("Movie_Id_Titles.csv")

    data = pd.merge(left=df, right=movie_titles, on="item_id")

    if movie_title not in list(data["title"]):
        print(f"sorry no movie found with title {movie_title}. try again")
        return None

    ratings = pd.DataFrame(data.groupby("title")["rating"].mean())

    ratings["num of ratings"] = pd.DataFrame(data.groupby("title")["rating"].count())

    moviemat = data.pivot_table(index="user_id", columns="title", values="rating")

    movie_user_rating = moviemat[movie_title]

    cors_movie = moviemat.corrwith(movie_user_rating)

    similar_movies = pd.DataFrame(cors_movie, columns=["Correlation"])

    similar_movies.dropna(inplace=True)

    similar_movies = similar_movies.join(ratings["num of ratings"])

    return (
        similar_movies[similar_movies["num of ratings"] > 100]
        .sort_values("Correlation", ascending=False)
        .head(10)
    )


print(recommendmovie())
