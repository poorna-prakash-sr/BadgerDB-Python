#!/bin/bash

set -e

echo "Building BadgerDB shared library..."
cd go-wrapper
go build -o libbadger.so -buildmode=c-shared badger_wrapper.go
mv libbadger.so ../badger/
mv libbadger.h ../badger/
cd ..
echo "Build complete!"
