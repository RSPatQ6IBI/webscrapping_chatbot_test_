
def create_table_in_postgre_():
    import psycopg2
    try:
        import tomllib  # Python 3.11+
    except ImportError:
        import tomli as tomllib  # Backport for older versions

    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)

    # Access specific fields
    db_name_ = data["database_details"]["db_name"]
    db_user_ = data["database_details"]["db_user"]
    db_password_ = data["database_details"]["db_pswd"]


    try:
        conn = psycopg2.connect(
            host="localhost",
            database=db_name_,
            user=db_user_,
            password=db_password_
        )
        cur = conn.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS ww2articles_(
            page_title VARCHAR(255) NOT NULL,
            heading VARCHAR(100) PRIMARY KEY,
            paragraph TEXT,
            paragraph_article_ TEXT,
            link VARCHAR(255)
        );
        '''
        cur.execute(create_table_query)
        conn.commit()
        print("Table created successfully!")

    except Exception as error:
        print(f"Error: {error}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def insert_data_into_postgre_(data_dict_):
    import psycopg2
    try:
        import tomllib  # Python 3.11+
    except ImportError:
        import tomli as tomllib  # Backport for older versions

    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)

    # Access specific fields
    db_name_ = data["database_details"]["db_name"]
    db_user_ = data["database_details"]["db_user"]
    db_password_ = data["database_details"]["db_pswd"]

    try:
        conn = psycopg2.connect(
            host="localhost",
            database=db_name_,
            user=db_user_,
            password=db_password_
        )
        cur = conn.cursor()
        insert_query = '''
        INSERT INTO ww2articles_ (page_title, heading, paragraph, paragraph_article_, link)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (heading) DO NOTHING;
        '''
        for element in data_dict_:
            cur.execute(insert_query, (
                element['page_title'],
                element['heading'],
                element['paragraph'],
                element['paragraph_article_'] if element['paragraph_article_'] else None,
                element['link']
            ))
        conn.commit()
        print("Data inserted successfully!", element['heading'][0])

    except Exception as error:
        print(f"Error: {error}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def fetch_data_from_postgre_():
    import psycopg2
    try:
        import tomllib  # Python 3.11+
    except ImportError:
        import tomli as tomllib  # Backport for older versions

    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)

    # Access specific fields
    db_name_ = data["database_details"]["db_name"]
    db_user_ = data["database_details"]["db_user"]
    db_password_ = data["database_details"]["db_pswd"]

    try:
        conn = psycopg2.connect(
            host="localhost",
            database=db_name_,
            user=db_user_,
            password=db_password_
        )
        cur = conn.cursor()
        select_query = 'SELECT * FROM ww2articles_;'
        # select_query = 'SELECT page_title, heading, paragraph, paragraph_article_ FROM ww2articles_;'
        print("Fetching data from PostgreSQL...",'\n',10*'-.-,')
        cur.execute(select_query)
        rows = cur.fetchall()
        # for row in rows:
        #     print(row)
        return rows

    except Exception as error:
        print(f"Error: {error}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close() 