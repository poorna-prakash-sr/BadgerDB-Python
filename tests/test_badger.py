import os
import json
import tempfile
import shutil
import unittest
from badgerdb_python.badger import BadgerDB

class TestBadgerDB(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test case."""
        self.temp_db_dir = tempfile.mkdtemp(prefix="badgerdb_test_")
        self.db = BadgerDB(self.temp_db_dir)

    def tearDown(self):
        """Clean up after each test case."""
        self.db.close()
        shutil.rmtree(self.temp_db_dir)

    def test_initialization(self):
        """Test database initialization."""
        self.assertTrue(os.path.exists(self.temp_db_dir), 
                       "Database directory should exist after initialization")
        self.assertIsInstance(self.db, BadgerDB, 
                            "Should create a BadgerDB instance")

    def test_put_and_get(self):
        """Test basic put and get operations."""
        # Test with string value
        self.db.put("key1", "value1")
        self.assertEqual(self.db.get("key1"), "value1", 
                        "Should retrieve the correct string value")

        # Test with numeric value (converted to string)
        self.db.put("key2", "42")
        self.assertEqual(self.db.get("key2"), "42", 
                        "Should retrieve the correct numeric string value")

        # Test with dictionary value (converted to JSON string)
        test_dict = {"nested": "data"}
        self.db.put("key3", json.dumps(test_dict))
        self.assertEqual(self.db.get("key3"), json.dumps(test_dict), 
                        "Should retrieve the correct JSON string value")

    def test_get_nonexistent_key(self):
        """Test getting a key that doesn't exist."""
        self.assertIsNone(self.db.get("nonexistent_key"), 
                         "Should return None for nonexistent key")

    def test_delete(self):
        """Test delete operation."""
        # Insert and verify data exists
        self.db.put("test_key", "test_value")
        self.assertEqual(self.db.get("test_key"), "test_value", 
                        "Value should exist before deletion")

        # Delete and verify data is gone
        self.db.delete("test_key")
        self.assertIsNone(self.db.get("test_key"), 
                         "Value should not exist after deletion")

        # Test deleting non-existent key (should not raise error)
        self.db.delete("nonexistent_key")

    def test_iterate(self):
        """Test key iteration."""
        test_data = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3"
        }

        # Insert test data
        for key, value in test_data.items():
            self.db.put(key, value)

        # Get all keys and verify
        keys = list(self.db.iterate())
        for key in test_data:
            self.assertIn(key, keys, 
                         f"Key '{key}' should be present in iteration")

    def test_export_and_import_json(self):
        """Test JSON export and import functionality."""
        # Initial test data (all strings)
        test_data = {
            "key1": "value1",
            "key2": "42",
            "key3": json.dumps({"nested": "data"})
        }

        # Insert test data
        for key, value in test_data.items():
            self.db.put(key, value)

        # Export to JSON
        json_path = os.path.join(self.temp_db_dir, "export.json")
        self.db.export_to_json(json_path)  

        # Clear database
        for key in self.db.iterate():
            self.db.delete(key)

        # Verify database is empty
        self.assertEqual(list(self.db.iterate()), [], 
                        "Database should be empty after clearing")

        # Import from JSON
        self.db.load_from_json(json_path)

        # Verify imported data
        imported_keys = list(self.db.iterate())
        self.assertEqual(len(imported_keys), len(test_data), 
                        "Should have same number of records after import")

        for key, expected_value in test_data.items():
            actual_value = self.db.get(key)
            self.assertEqual(actual_value, expected_value, 
                           f"Value for key '{key}' should match after import")

    def test_large_data_handling(self):
        """Test handling of large data sets."""
        # Create a large dataset (all strings)
        large_data = {f"key{i}": f"value{i}" for i in range(1000)}

        # Insert all data
        for key, value in large_data.items():
            self.db.put(key, value)

        # Verify all data
        for key, expected_value in large_data.items():
            actual_value = self.db.get(key)
            self.assertEqual(actual_value, expected_value, 
                           f"Value for key '{key}' should match in large dataset")

    def test_update_existing_key(self):
        """Test updating an existing key."""
        # Initial insert
        self.db.put("test_key", "initial_value")
        self.assertEqual(self.db.get("test_key"), "initial_value", 
                        "Should have initial value")

        # Update
        self.db.put("test_key", "updated_value")
        self.assertEqual(self.db.get("test_key"), "updated_value", 
                        "Should have updated value")

if __name__ == '__main__':
    unittest.main()