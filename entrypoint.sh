#!/bin/bash

echo "Entrypoint script running"

# Run the strategie_meister command with all arguments passed
strategie_meister "$@"

# Exit with the same status code as strategie_meister
exit $?