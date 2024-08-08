# Revised MicroDB class to ensure no errors and complete the testing.

class MicroDB:
    def __init__(self):
        self.tables = {}

    def execute(self, command):
        if command.startswith("CREATE TABLE"):
            self.create_table(command)
        elif command.startswith("INSERT INTO"):
            self.insert_into(command)
        elif command.startswith("SELECT"):
            return self.select(command)
        else:
            return "Unsupported command"

    def create_table(self, command):
        pattern = r"CREATE TABLE (\w+) \((.+)\)"
        match = re.match(pattern, command)
        table_name, columns = match.groups()
        columns = columns.split(", ")
        schema = {}
        for column in columns:
            name, data_type = column.split(" ")
            schema[name] = data_type
        self.tables[table_name] = {'schema': schema, 'rows': []}

    def insert_into(self, command):
        pattern = r"INSERT INTO (\w+) \((.+)\) VALUES \((.+)\)"
        match = re.match(pattern, command)
        table_name, columns, values = match.groups()
        columns = columns.split(", ")
        values = values.split(", ")
        row = {}
        for col, val in zip(columns, values):
            val = val.strip("'")
            if self.tables[table_name]['schema'][col] == "INT":
                val = int(val)
            row[col] = val
        self.tables[table_name]['rows'].append(row)

    def select(self, command):
        pattern = r"SELECT (.+) FROM (\w+) WHERE (.+)"
        match = re.match(pattern, command)
        fields, table_name, condition = match.groups()
        select_all = fields.strip() == '*'
        fields = fields.split(", ")

        rows = self.tables[table_name]['rows']
        filtered_rows = []
        for row in rows:
            if self.evaluate_condition(row, condition):
                if select_all:
                    filtered_rows.append([str(row[col]) for col in self.tables[table_name]['schema']])
                else:
                    filtered_rows.append([str(row[col]) for col in fields])
        return filtered_rows

    def evaluate_condition(self, row, condition):
        or_conditions = condition.split(" OR ")
        for or_cond in or_conditions:
            and_conditions = or_cond.split(" AND ")
            and_results = []
            for and_cond in and_conditions:
                column, op, value = self.parse_condition(and_cond)
                if not self.check_condition(row[column], op, value.strip('"').strip("'")):
                    and_results.append(False)
                else:
                    and_results.append(True)
            if all(and_results):
                return True
        return False

    def parse_condition(self, condition):
        ops = ['>=', '<=', '!=', '=', '>', '<']
        for op in ops:
            if op in condition:
                column, value = condition.split(op)
                return column.strip(), op, value.strip()
        raise ValueError("Invalid condition")

    def check_condition(self, row_value, op, value):
        if isinstance(row_value, int):
            value = int(value)
        elif isinstance(row_value, str):
            value = str(value)
        if op == '>':
            return row_value > value
        elif op == '<':
            return row_value < value
        elif op == '=':
            return row_value == value
        elif op == '!=':
            return row_value != value
        elif op == '>=':
            return row_value >= value
        elif op == '<=':
            return row_value <= value
        return False


# Initialize the database
db = MicroDB()
db.execute("CREATE TABLE users (id INT, name STRING, age INT)")
db.execute("INSERT INTO users (id, name, age) VALUES (1, 'Alice', 30)")
db.execute("INSERT INTO users (id, name, age) VALUES (2, 'Bob', 25)")
db.execute("INSERT INTO users (id, name, age) VALUES (3, 'Charlie', 27)")
db.execute("INSERT INTO users (id, name, age) VALUES (4, 'Dave', 45)")

# Testing select queries
results1 = db.execute("SELECT * FROM users WHERE age < 30")
results2 = db.execute("SELECT * FROM users WHERE age < 30 OR age >= 40")
results3 = db.execute("SELECT name FROM users WHERE age < 30")
results4 = db.execute('SELECT name FROM users WHERE age < 30 AND name != "Charlie"')

(results1, results2, results3, results4)
