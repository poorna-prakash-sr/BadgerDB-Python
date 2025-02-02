package main

/*
#cgo CFLAGS: -I.
#include <stdlib.h>
*/
import "C"

import (
	"log"

	"github.com/dgraph-io/badger/v4"
)

var db *badger.DB

//export OpenDB
func OpenDB(path *C.char) C.int {
	opts := badger.DefaultOptions(C.GoString(path)).WithLoggingLevel(badger.ERROR)
	var err error
	db, err = badger.Open(opts)
	if err != nil {
		log.Println("Error opening DB:", err)
		return -1
	}
	return 0
}

//export CloseDB
func CloseDB() {
	if db != nil {
		db.Close()
	}
}

//export Put
func Put(key *C.char, value *C.char) C.int {
	err := db.Update(func(txn *badger.Txn) error {
		return txn.Set([]byte(C.GoString(key)), []byte(C.GoString(value)))
	})
	if err != nil {
		log.Println("Error updating DB:", err)
		return -1
	}
	return 0
}

//export Get
func Get(key *C.char) *C.char {
	var val []byte
	err := db.View(func(txn *badger.Txn) error {
		item, err := txn.Get([]byte(C.GoString(key)))
		if err != nil {
			return err
		}
		val, err = item.ValueCopy(nil)
		return err
	})
	if err != nil {
		log.Println("Error getting DB:", err)
		return nil
	}
	return C.CString(string(val))
}

//export Delete
func Delete(key *C.char) C.int {
	err := db.Update(func(txn *badger.Txn) error {
		return txn.Delete([]byte(C.GoString(key)))
	})
	if err != nil {
		log.Println("Error deleting DB:", err)
		return -1
	}
	return 0
}

//export Iterate
func Iterate() *C.char {
	var result string
	err := db.View(func(txn *badger.Txn) error {
		it := txn.NewIterator(badger.DefaultIteratorOptions)
		defer it.Close()

		for it.Rewind(); it.Valid(); it.Next() {
			item := it.Item()
			k := item.Key()
			result += string(k) + "\n"
		}
		return nil
	})
	if err != nil {
		log.Println("Iterate error:", err)
		return nil
	}
	return C.CString(result)
}

func main() {} // Required for `-buildmode=c-shared`
