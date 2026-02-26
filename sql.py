import sqlite3

# Create connection
connection = sqlite3.connect("data.db")

cursor = connection.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    course TEXT,
    marks INTEGER
)
""")

# Insert sample data
cursor.execute("INSERT INTO students (name, age, course, marks) VALUES ('Gayatri', 21, 'CSE', 85)")
cursor.execute("INSERT INTO students (name, age, course, marks) VALUES ('Ravi', 22, 'ECE', 78)")
cursor.execute("INSERT INTO students (name, age, course, marks) VALUES ('Anjali', 20, 'CSE', 92)")
cursor.execute("INSERT INTO students (name, age, course, marks) VALUES ('Kiran', 23, 'EEE', 70)")

connection.commit()
connection.close()

print("Database and table created successfully!")
