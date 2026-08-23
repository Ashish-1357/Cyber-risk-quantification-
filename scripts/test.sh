#!/bin/bash
# Run all tests

cd server
source venv/bin/activate 2>/dev/null || true
pytest -v
