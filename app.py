
import streamlit as st
import sqlite3
import google.generativeai as genai


# ==============================
# 🔑 GOOGLE API KEY
# ==============================
GOOGLE_API_KEY = "AIzaSyCxFGRTTXA--uICjJi0HmoMBoOaZZ0iswo"
genai.configure(api_key=GOOGLE_API_KEY)


# ==============================
# DATABASE INITIALIZATION
# ==============================
def initialize_database():
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        course TEXT,
        marks INTEGER
    )
    """)

    # Insert sample data ONLY if table is empty
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]

    if count == 0:
        sample_data = [
            (1, "John", 20, "Math", 85),
            (2, "Alice", 22, "Science", 90),
            (3, "Bob", 19, "Math", 78),
            (4, "Emma", 21, "Computer", 92),
            (5, "David", 23, "Science", 88)
        ]

        cursor.executemany(
            "INSERT INTO students VALUES (?, ?, ?, ?, ?)",
            sample_data
        )

    connection.commit()
    connection.close()


# ==============================
# GEMINI QUERY GENERATION
# ==============================
def get_response(question):

    prompt = f"""
Convert the following natural language question into a valid SQLite SQL query.

Table:
students(id INTEGER PRIMARY KEY, name TEXT, age INTEGER, course TEXT, marks INTEGER)

Rules:
- Return only SQL query.
- No explanation.
- No markdown.
- No backticks.
- Must work in SQLite.

Question: {question}
"""

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        sql_query = response.text.strip()

        # 🔥 Clean markdown formatting if Gemini adds it
        sql_query = sql_query.replace("```sql", "")
        sql_query = sql_query.replace("```", "")
        sql_query = sql_query.strip()

        return sql_query

    except Exception as e:
        return f"ERROR: {str(e)}"


# ==============================
# SQL EXECUTION
# ==============================
def read_query(query):
    try:
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        cursor.execute(query)
        rows = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description] if cursor.description else []

        connection.close()

        return columns, rows

    except Exception as e:
        return None, str(e)


# ==============================
# HOME PAGE
# ==============================
def page_home():

    st.markdown("""
        <style>
        .title {color: #00FF7F; text-align: center;}
        .subtitle {color: #00FF7F; text-align: center;}
        .offerings {color: white; font-size: 18px;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='title'>Welcome to IntelliSQL!</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='subtitle'>Revolutionizing Database Querying with Advanced LLM Capabilities</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/4149/4149676.png", width=250)

    with col2:
        st.markdown("""
        <div class='offerings'>
        <ul>
        <li>Intelligent Query Assistance</li>
        <li>Data Exploration</li>
        <li>Efficient Data Retrieval</li>
        <li>Performance Optimization</li>
        <li>Syntax Suggestions</li>
        <li>Trend Analysis</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)


# ==============================
# ABOUT PAGE
# ==============================
def page_about():

    st.markdown("<h1 style='color:#00FF7F;'>About IntelliSQL</h1>", unsafe_allow_html=True)

    st.write("""
    IntelliSQL revolutionizes database querying using advanced Large Language Models (LLMs).
    It allows intelligent, intuitive interaction with SQL databases using natural language.
    """)

    st.image("https://upload.wikimedia.org/wikipedia/en/6/68/Oracle_SQL_Developer_logo.png", width=300)


# ==============================
# INTELLIGENT QUERY PAGE
# ==============================
def page_intelligent_query_assistance():

    st.markdown("<h1 style='color:#00FF7F;'>Intelligent Query Assistance</h1>", unsafe_allow_html=True)

    st.write("""
    Enter your question in natural language.
    IntelliSQL will generate SQL and execute it on the database.
    """)

    col1, col2 = st.columns(2)

    with col1:
        user_query = st.text_input("Enter your query:")

        if st.button("Generate & Execute") and user_query:

            sql_query = get_response(user_query)

            if sql_query.startswith("ERROR"):
                st.error(sql_query)
            else:
                st.subheader("Generated SQL Query:")
                st.code(sql_query, language="sql")

                columns, result = read_query(sql_query)

                st.subheader("Query Result:")

                if columns is None:
                    st.error(result)
                else:
                    if result:
                        table_data = []
                        for row in result:
                            row_dict = {}
                            for i in range(len(columns)):
                                row_dict[columns[i]] = row[i]
                            table_data.append(row_dict)

                        st.table(table_data)
                    else:
                        st.info("No records found.")

    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/2910/2910791.png", width=300)


# ==============================
# MAIN FUNCTION
# ==============================
def main():

    st.set_page_config(
        page_title="IntelliSQL",
        page_icon="⭐",
        layout="wide"
    )

    initialize_database()

    st.sidebar.title("Navigation")

    pages = {
        "Home": page_home,
        "About": page_about,
        "Intelligent Query Assistance": page_intelligent_query_assistance
    }

    selection = st.sidebar.radio("Go to", list(pages.keys()))

    page = pages[selection]
    page()


# ==============================
# ENTRY POINT
# ==============================
if __name__ == "__main__":
    main()
