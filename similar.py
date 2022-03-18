# Imports
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

books = pd.read_csv('Dataset/books.csv')
ratings = pd.read_csv('Dataset/ratings.csv')
tags = pd.read_csv('Dataset/tags.csv')
book_tags = pd.read_csv('Dataset/book_tags.csv')

# Delete NaN values of original_publication_year
for x in ["original_publication_year"]:
    books = books[books[x].notnull()]

# Delete negative values
books = books[(books['original_publication_year'] >= 0)]

# Grouping by the book_id to know how many ratings have each book
rating_book = ratings.groupby('book_id').book_id.apply(lambda x: len(x)).sort_values()

rating_user = ratings.groupby('user_id').user_id.apply(lambda x: len(x)).sort_values()

# Merge the two datasets grouping by the tag_id.
data = pd.merge(book_tags, tags, left_on='tag_id', right_on='tag_id', how='inner')

titles = books[['book_id', 'title', 'goodreads_book_id', 'authors']]

# Merge the book dataset with the new one to know the title and the author
data = pd.merge(titles, data, left_on='goodreads_book_id', right_on='goodreads_book_id')



# For each book, join all their tags
list_tags = data.groupby(by='goodreads_book_id')['tag_name'].apply(set).apply(list)

# Append this list of tags on the books dataset
books['tags'] = books['goodreads_book_id'].apply(lambda x: ' '.join(list_tags[x]))

pd.reset_option('max_colwidth')


# Function to get the index of the book given its title.
def get_book_id(book_title):
    index = books.index[books['original_title'] == book_title].to_list()
    if index:
        return index[0]
    else:
        return None


def get_book_id_isbn(isbn):
    index = books.index[books['isbn'] == isbn].to_list()
    if index:
        return index[0]
    else:
        return None


# Function to get the title of a book given its id.
def get_book_title(book_id):
    title = books.iloc[book_id]['original_title']
    if (title == "NaN"):
        title = books.iloc[book_id]['title']
    return title


def get_book_image(book_id):
    image = books.iloc[book_id]['image_url']
    return image


def get_book_isbn(book_id):
    isbn = books.iloc[book_id]['isbn']
    return isbn


def get_book_authors(book_id):
    authors = books.iloc[book_id]['authors']
    return authors


# Function that takes the book title and returns the most similar books.
def get_similar_books(title, n=5):
    # Get the book id
    book_id = get_book_id(title)

    if book_id is None:
        print("Book not found.")
    else:

        # Get the pariwsie similarity scores of all books with that book
        book_similarities = list(enumerate(similarities[book_id]))

        # Sort the books based on the similarity scores
        book_similarities = sorted(book_similarities, key=lambda x: x[1], reverse=True)

        # Get the scores of the 5 most similar book
        most_similar_books = book_similarities[1:1 + n]
        most_similar_books = list(map(lambda x: (get_book_title(x[0]), round(x[1], 2)), most_similar_books))

        most_similar_books_df = pd.DataFrame(most_similar_books, columns=['Title', 'Similarity'])
        print("For this book we will recommand you:\n")

        return most_similar_books_df


tfidf = TfidfVectorizer(stop_words='english')

tfidf_matrix = tfidf.fit_transform(books['tags'])

similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)


def similarBooks(book_title):


    result = get_similar_books(book_title)
    df = pd.DataFrame(columns=['Title', 'authors', 'image', 'Similarity'])
    for b in result.index:
        df1 = {'Title':get_book_title(get_book_id((result['Title'][b]))),
               'authors': get_book_authors(get_book_id((result['Title'][b]))),
               'image': get_book_image(get_book_id((result['Title'][b]))), 'Similarity': result['Similarity'][b]}
        if("nophoto" in df1['image']):
            df1['image']="data:image/png;base64,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"

        df = df.append(df1, ignore_index=True)
    return df




