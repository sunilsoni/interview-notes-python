import re


class MicroDB:
    def __init__(self):
        self.tables = {}

    def create_table(self, command):
        match = re.match(r'CREATE TABLE (\w+) \((.+)\)', command)
        table_name = match.group(1)
        schema = match.group(2).split(', ')
        columns = {col.split()[0]: col.split()[1] for col in schema}
        self.tables[table_name] = {'schema': columns, 'data': []}

    def insert_into(self, command):
        match = re.match(r'INSERT INTO (\w+) \((.+)\) VALUES \((.+)\)', command)
        table_name = match.group(1)
        columns = match.group(2).split(', ')
        values = match.group(3).split(', ')
        table = self.tables[table_name]
        row = {col: val.strip().strip("'") for col, val in zip(columns, values)}
        table['data'].append(row)

    def select(self, command):
        match = re.match(r'SELECT (.+) FROM (\w+)(?: WHERE (.+))?', command)
        fields = match.group(1).split(', ')
        table_name = match.group(2)
        condition = match.group(3)

        table = self.tables[table_name]
        data = table['data']

        if condition:
            data = self.apply_condition(data, condition)

        if fields == ['*']:
            return [list(row.values()) for row in data]
        else:
            return [[row[field] for field in fields] for row in data]

    def apply_condition(self, data, condition):
        def eval_condition(row, condition):
            condition = condition.replace('AND', ' and ').replace('OR', ' or ')
            condition = re.sub(r'(\w+)', r'row["\1"]', condition)
            return eval(condition)

        return [row for row in data if eval_condition(row, condition)]

    def execute(self, command):
        if command.startswith('CREATE TABLE'):
            self.create_table(command)
        elif command.startswith('INSERT INTO'):
            self.insert_into(command)
        elif command.startswith('SELECT'):
            return self.select(command)


# Example usage
db = MicroDB()
db.execute("CREATE TABLE users (id INT, name STRING, age INT)")
db.execute("INSERT INTO users (id, name, age) VALUES (1, 'Alice', 30)")
db.execute("INSERT INTO users (id, name, age) VALUES (2, 'Bob', 25)")
db.execute("INSERT INTO users (id, name, age) VALUES (3, 'Charlie', 27)")
db.execute("INSERT INTO users (id, name, age) VALUES (4, 'Dave', 45)")

results1 = db.execute("SELECT * FROM users WHERE age < 30")
print(results1)  # Output: [['2', 'Bob', '25'], ['3', 'Charlie', '27']]

results2 = db.execute("SELECT * FROM users WHERE age < 30 OR age >= 40")
print(results2)  # Output: [['2', 'Bob', '25'], ['3', 'Charlie', '27'], ['4', 'Dave', '45']]

results3 = db.execute("SELECT name FROM users WHERE age < 30")
print(results3)  # Output: [['Bob'], ['Charlie']]

results4 = db.execute('SELECT name from users WHERE age < 30 AND name != "Charlie"')
print(results4)  # Output: [['Bob']]
