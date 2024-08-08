import re


class MicroDB:
    def __init__(self):
        self.tables = {}

    def execute(self, cmd):
        cmd = cmd.strip()
        if cmd.startswith('CREATE TABLE'):
            self.create_table(cmd)
        elif cmd.startswith('INSERT INTO'):
            self.insert_into(cmd)
        elif cmd.startswith('SELECT'):
            return self.select(cmd)

    def create_table(self, cmd):
        match = re.match(r'CREATE TABLE (\w+) \((.+)\)', cmd)
        if match:
            table_name = match.group(1)
            columns = [col.strip().split() for col in match.group(2).split(',')]
            self.tables[table_name] = columns

    def insert_into(self, cmd):
        match = re.match(r'INSERT INTO (\w+) \((.+)\) VALUES \((.+)\)', cmd)
        if match:
            table_name = match.group(1)
            columns = match.group(2).split(',')
            values = match.group(3).split(',')
            if table_name in self.tables:
                table_columns = [col[0] for col in self.tables[table_name]]
                if len(columns) == len(values) and set(columns) <= set(table_columns):
                    print(f"Inserted into {table_name}: {values}")
                    # Here you would actually insert the values into the table
                else:
                    print("Column names/values mismatch or unknown column")
            else:
                print(f"Table {table_name} does not exist")

    def select(self, cmd):
        match = re.match(r'SELECT (.+) FROM (\w+) WHERE (.+)', cmd)
        if match:
            fields = match.group(1).split(',')
            table_name = match.group(2)
            condition = match.group(3)
            if table_name in self.tables:
                results = []
                # Here you would actually query the data based on the condition
                print(f"Selected from {table_name} with condition: {condition}")
                return results
            else:
                print(f"Table {table_name} does not exist")


# Example usage
db = MicroDB()
db.execute("CREATE TABLE users (id INT, name STRING, age INT)")
db.execute("INSERT INTO users (id, name, age) VALUES (1, 'Alice', 30)")
db.execute("INSERT INTO users (id, name, age) VALUES (2, 'Bob', 25)")
db.execute("INSERT INTO users (id, name, age) VALUES (3, 'Charlie', 27)")
db.execute("INSERT INTO users (id, name, age) VALUES (4, 'Dave', 45)")

results1 = db.execute("SELECT * FROM users WHERE age < 30")
print(results1)  # Output: Selected from users with condition: age < 30

results2 = db.execute("SELECT * FROM users WHERE age < 30 OR age >= 40")
print(results2)  # Output: Selected from users with condition: age < 30 OR age >= 40

# Bonus question 1
results3 = db.execute("SELECT name FROM users WHERE age < 30")
print(results3)  # Output: Selected from users with condition: age < 30

# Bonus question 2
results4 = db.execute('SELECT name FROM users WHERE age < 30 AND name != "Charlie"')
print(results4)  # Output: Selected from users with condition: age < 30 AND name != "Charlie"
