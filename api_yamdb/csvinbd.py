import csv
import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()


with open('static/data/category.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        id = row['id']
        name = row['name']
        slug = row['slug']
        c.execute(
            "INSERT INTO reviews_category "
            "(id, name, slug) "
            "VALUES(?,?,?)",
            (id, name, slug)
        )
        conn.commit()


with open('static/data/titles.csv', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        id = row['id']
        name = row['name']
        year = row['year']
        category = row['category']
        c.execute(
            "INSERT INTO reviews_title"
            "(id, name, year, category_id)"
            "VALUES(?,?,?,?)",
            (id, name, year, category)
        )
        conn.commit()


with open('static/data/review.csv', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        id = row['id']
        title_id = row['title_id']
        text = row['text']
        author = row['author']
        score = row['score']
        pub_date = row['pub_date']
        c.execute(
            "INSERT INTO reviews_review"
            "(id, title_id, text, author_id, score, pub_date)"
            "VALUES(?,?,?,?,?,?)",
            (id, title_id, text, author, score, pub_date)
        )
        conn.commit()


with open('static/data/genre.csv', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        id = row['id']
        name = row['name']
        slug = row['slug']
        c.execute(
            "INSERT INTO reviews_genre"
            "(id, name, slug)"
            "VALUES(?,?,?)",
            (id, name, slug)
        )
        conn.commit()


with open(
        'static/data/genre_title.csv', encoding='utf-8'
) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        id = row['id']
        title_id = row['title_id']
        genre_id = row['genre_id']
        c.execute(
            "INSERT INTO reviews_title_genre"
            "(id, title_id, genre_id)"
            "VALUES(?,?,?)",
            (id, title_id, genre_id)
        )
        conn.commit()


with open('static/data/comments.csv', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        id = row['id']
        review_id = row['review_id']
        text = row['text']
        author = row['author']
        pub_date = row['pub_date']
        c.execute(
            "INSERT INTO reviews_comment"
            "(id, review_id, text, author_id, pub_date)"
            "VALUES(?,?,?,?,?)",
            (id, review_id, text, author, pub_date)
        )
        conn.commit()


with open('static/data/users.csv', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        id = row['id']
        username = row['username']
        email = row['email']
        role = row['role']
        bio = row['bio']
        first_name = row['first_name']
        last_name = row['last_name']
        password = 'qwerty'
        is_superuser = False
        is_staff = False
        is_active = True
        date_joined = '2022-05-18 18:27:27.322617+00:00'
        c.execute(
            "INSERT INTO reviews_user"
            "(id, username, email, role, bio, first_name, last_name,"
            " password, is_superuser, is_staff, is_active, date_joined)"
            "VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            (id, username, email, role, bio, first_name, last_name,
             password, is_superuser, is_staff, is_active, date_joined)
        )
        conn.commit()


conn.close()
