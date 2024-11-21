#!/bin/bash

echo "Starting cleanup process..."

clean_python_cache() {
    echo "Cleaning Python cache files..."
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    find . -type f -name "*.pyo" -delete
    find . -type f -name "*.pyd" -delete
}

clean_uploads() {
    echo "Cleaning upload directories..."
    rm -rf ui-service/static/uploads/*
    rm -rf ai-service/uploads/*
    
    mkdir -p ui-service/static/uploads
    mkdir -p ai-service/uploads
    chmod 777 ui-service/static/uploads
    chmod 777 ai-service/uploads
    echo "Upload directories cleaned and recreated"
}

clean_logs() {
    echo "Cleaning log files..."
    find . -type f -name "*.log" -delete
    find . -type f -name "*.log.*" -delete
}

clean_docker() {
    echo "Cleaning Docker artifacts..."
    if command -v docker &> /dev/null; then
        docker-compose down -v 2>/dev/null
        docker system prune -f 2>/dev/null
    fi
}

clean_venv() {
    echo "Cleaning virtual environments..."
    rm -rf ui-service/venv
    rm -rf ai-service/venv
}

clean_temp() {
    echo "Cleaning temporary files..."
    find . -type f -name ".DS_Store" -delete
    find . -type f -name "*.swp" -delete
    find . -type f -name "*.swo" -delete
    find . -type f -name "*~" -delete
}

echo "=== Starting Deep Cleanup ==="

clean_python_cache
clean_uploads
clean_logs
clean_docker
clean_venv
clean_temp

echo "=== Cleanup Complete ==="
echo "The following items were cleaned:"
echo "✓ Python cache files"
echo "✓ Upload directories"
echo "✓ Log files"
echo "✓ Docker artifacts"
echo "✓ Virtual environments"
echo "✓ Temporary files"
echo ""
echo "System is clean and ready for development!" 