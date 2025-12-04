#!/bin/bash
# Install Stockfish chess engine

echo "Installing Stockfish chess engine..."

# Update package list
sudo apt-get update

# Install Stockfish
sudo apt-get install -y stockfish

# Verify installation
if command -v stockfish &> /dev/null; then
    echo "✓ Stockfish installed successfully"
    stockfish --version
else
    echo "✗ Stockfish installation failed"
    exit 1
fi
