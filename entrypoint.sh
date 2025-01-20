#!/bin/bash

echo "Entrypoint script running"

# Run the portfolio_manager command with all arguments passed
portfolio_manager "$@"

# Exit with the same status code as portfolio_manager
exit $?