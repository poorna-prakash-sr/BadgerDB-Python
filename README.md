
# BadgerDB Python Wrapper

This is a Python wrapper for [BadgerDB](https://github.com/dgraph-io/badger), a fast and efficient key-value store written in Go. This wrapper allows Python applications to interact with BadgerDB via a shared library (`libbadger.so`), providing a straightforward interface for managing key-value pairs.

## Features

- **Insert key-value pairs**: Store key-value pairs in the BadgerDB database.
- **Retrieve values by key**: Get values stored in the database using their corresponding keys.
- **Delete key-value pairs**: Remove key-value pairs from the database.
- **Iterate over all keys**: Retrieve a list of all keys currently stored in the database.
- **Export to JSON**: Dump all key-value pairs in the database into a JSON file.
- **Import from JSON**: Load key-value pairs from a JSON file into the database.

## Installation

### Using pip

You can install this package directly from PyPI using `pip`:

```bash
pip install badgerdb-python
```

This will install the Python wrapper along with the necessary dependencies, including the required `libbadger.so` shared library that contains the Go-based functions needed to interact with the BadgerDB.

### Requirements

- Python 3.x

## Usage

### Basic Operations

You can use the BadgerDB wrapper to perform basic database operations like inserting, retrieving, and deleting key-value pairs.

#### Example: Insert, Retrieve, and Delete Key-Value Pairs

```python
from badgerdb import BadgerDB

# Initialize the database (replace with your DB path)
db = BadgerDB("/path/to/db")

# Insert a key-value pair
db.put("Hey", "I am Badger!")

# Retrieve the value for the key 'Hey'
print(db.get("Hey"))  # Output: I am Badger!

# Delete the key-value pair for 'Hey'
db.delete("Hey")

# Close the database when done
db.close()
```

### Iterating Over Keys

You can retrieve a list of all the keys in the database.

```python
from badgerdb import BadgerDB

# Initialize the database
db = BadgerDB("/path/to/db")

# Insert some key-value pairs
db.put("name", "Alice")
db.put("age", "30")
db.put("city", "New York")

# Iterate over all keys
keys = db.iterate()
print(keys)  # Output: ['name', 'age', 'city']

# Close the database when done
db.close()
```

### Exporting and Importing Data as JSON

You can export the entire database to a JSON file and later import it back into the database.

#### Export to JSON

```python
from badgerdb import BadgerDB

# Initialize the database
db = BadgerDB("/path/to/db")

# Insert some data
db.put("key1", "value1")
db.put("key2", "value2")

# Export the data to a JSON file
db.dump_to_json("/path/to/output.json")

# Close the database
db.close()
```

#### Import from JSON

```python
from badgerdb import BadgerDB

# Initialize the database
db = BadgerDB("/path/to/db")

# Import data from a JSON file
db.load_from_json("/path/to/output.json")

# Verify that the data is imported
print(db.get("key1"))  # Output: value1
print(db.get("key2"))  # Output: value2

# Close the database
db.close()
```

## Features

- **Error Handling**: The wrapper will raise exceptions if there are any issues interacting with the database (e.g., attempting to access a non-existent key or failing to load data from a file).
- **Data Integrity**: Supports basic CRUD (Create, Read, Update, Delete) operations ensuring consistency during data manipulations.

## Contributing

We welcome contributions from the community! If you'd like to contribute, follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-name`).
6. Create a pull request.

For larger changes or bug fixes, feel free to open an issue to discuss the proposed changes before implementing them.

## Acknowledgements

This Python wrapper relies on the **`libbadger.so`** shared library for interacting with the BadgerDB database. Special thanks to the developers who created the `gobadger` library and its C-compatible shared library (`libbadger.so`) that enables this Python integration.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.