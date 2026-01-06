#!/bin/bash

# Test script to verify the website files are valid

echo "🔍 Chess Opening Explorer - File Validation"
echo "==========================================="
echo ""

# Check if required files exist
echo "✓ Checking required files..."
files=("index.html" "app.js" "styles.css")
missing=0

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file exists ($(wc -c < "$file") bytes)"
    else
        echo "  ✗ $file is missing!"
        missing=$((missing + 1))
    fi
done

echo ""

if [ $missing -eq 0 ]; then
    echo "✅ All required files present!"
else
    echo "❌ $missing file(s) missing"
    exit 1
fi

echo ""
echo "🌐 To test locally, run:"
echo "   python -m http.server 8000"
echo "   Then open: http://localhost:8000"
echo ""
echo "🚀 To deploy to GitHub Pages:"
echo "   git add ."
echo "   git commit -m 'Add Chess Opening Explorer website'"
echo "   git push origin main"
echo ""
echo "📝 See GITHUB_PAGES_SETUP.md for detailed setup instructions"
