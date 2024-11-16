#!/bin/sh

PROTO_DIR="shared"

echo "Starting proto file generation..."

if [ -d "$PROTO_DIR" ]; then
    for proto_file in "$PROTO_DIR"/*.proto; do
        if [ -f "$proto_file" ]; then
            echo "Generating files for: $proto_file"
            python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. "$proto_file"
        else
            echo "No .proto files found in $PROTO_DIR"
        fi
    done
else
    echo "Directory $PROTO_DIR does not exist!"
    exit 1
fi

echo "Proto file generation completed. Starting application..."
exec "$@"
