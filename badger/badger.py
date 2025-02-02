import ctypes
import os
import json

# Load the shared library
lib_path = os.path.join(os.path.dirname(__file__), "libbadger.so")
lib = ctypes.CDLL(lib_path)

# Define function signatures
lib.OpenDB.argtypes = [ctypes.c_char_p]
lib.OpenDB.restype = ctypes.c_int

lib.CloseDB.argtypes = []
lib.CloseDB.restype = None

lib.Put.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.Put.restype = ctypes.c_int

lib.Get.argtypes = [ctypes.c_char_p]
lib.Get.restype = ctypes.c_char_p

lib.Delete.argtypes = [ctypes.c_char_p]
lib.Delete.restype = ctypes.c_int

lib.Iterate.argtypes = []
lib.Iterate.restype = ctypes.c_char_p

class BadgerDB:
    def __init__(self, path: str):
        if lib.OpenDB(path.encode("utf-8")) != 0:
            raise Exception("Failed to open BadgerDB")

    def put(self, key: str, value: str):
        """Insert a key-value pair"""
        if lib.Put(key.encode("utf-8"), value.encode("utf-8")) != 0:
            raise Exception("Failed to insert key-value pair")

    def get(self, key: str) -> str:
        """Retrieve a value for a key"""
        result = lib.Get(key.encode("utf-8"))
        return result.decode("utf-8") if result else None

    def delete(self, key: str):
        """Delete a key-value pair"""
        if lib.Delete(key.encode("utf-8")) != 0:
            raise Exception("Failed to delete key")

    def iterate(self):
        """
        Returns a list of keys stored in the database.
        (This method relies on the Go wrapper returning all keys as a newline‐separated string.)
        """
        result = lib.Iterate()
        return result.decode("utf-8").strip().split("\n") if result else []
    
    def export_to_json(self, filename: str):
        """
        Export all key-value pairs from the DB to a JSON file.
        This method iterates over all keys (using self.iterate()) and retrieves
        the corresponding value for each key using self.get().
        """
        data = {}
        keys = self.iterate()
        for key in keys:
            # Retrieve the value for each key
            value = self.get(key)
            if value is not None:
                data[key] = value
        # Write the dictionary to a JSON file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Dumped {len(data)} key-value pairs to {filename}")

    def load_from_json(self, filename: str):
        """
        Load key-value pairs from a JSON file and store them in the DB.
        The JSON file should contain a dictionary of key-value pairs.
        """
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for key, value in data.items():
            self.put(key, value)
        print(f"Loaded {len(data)} key-value pairs from {filename}")


    def close(self):
        lib.CloseDB()


