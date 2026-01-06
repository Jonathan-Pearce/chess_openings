# GitHub Pages Setup Instructions

This document provides step-by-step instructions for deploying the Chess Opening Explorer website to GitHub Pages.

## Prerequisites

- GitHub account with access to this repository
- Repository must be public (for free GitHub Pages) or have GitHub Pro/Team/Enterprise

## Setup Steps

### 1. Commit and Push the Website Files

First, add all the new files to git and push them to GitHub:

```bash
git add .
git commit -m "Add GitHub Pages website for Chess Opening Explorer"
git push origin main
```

### 2. Enable GitHub Pages

1. Go to your repository on GitHub: https://github.com/Jonathan-Pearce/chess_openings
2. Click on **Settings** (top menu)
3. Click on **Pages** (left sidebar under "Code and automation")
4. Under "Build and deployment":
   - Source: Select **GitHub Actions**
5. The GitHub Actions workflow will automatically deploy the site

### 3. Wait for Deployment

1. Go to the **Actions** tab in your repository
2. You should see a "Deploy to GitHub Pages" workflow running
3. Wait for it to complete (usually takes 1-2 minutes)
4. Once complete, your site will be available at:
   - **https://jonathan-pearce.github.io/chess_openings/**

### 4. Verify the Website

Visit your GitHub Pages URL and verify:
- Chess board displays correctly
- You can make moves by dragging pieces
- Lichess statistics load after making moves
- Stockfish analysis button works
- All styling appears correct

## Troubleshooting

### Site Not Loading

If the site doesn't load:
1. Check the Actions tab for any deployment errors
2. Ensure the workflow completed successfully
3. Wait a few minutes for GitHub's CDN to update
4. Try accessing in an incognito/private browser window

### JavaScript Errors

If you see JavaScript errors in the browser console:
1. Check that all CDN resources are loading (chess.js, chessboard.js, stockfish.js)
2. Verify your browser supports ES6 JavaScript
3. Try a different browser (Chrome/Firefox recommended)

### Lichess API Not Working

If Lichess statistics don't load:
1. Check browser console for CORS errors
2. Verify you have internet connectivity
3. Check if Lichess API is operational: https://lichess.org/api
4. The API has rate limits - wait a minute and try again

### Stockfish Not Working

If Stockfish analysis doesn't work:
1. The engine may take 10-30 seconds to initialize
2. Check browser console for loading errors
3. Try a smaller depth value (10-15) first
4. Some browsers may block Web Workers - try Chrome/Firefox

## Updating the Website

To make changes to the website:

1. Edit the files locally:
   - `index.html` - Structure and content
   - `styles.css` - Styling and layout
   - `app.js` - Functionality and logic

2. Test locally:
   ```bash
   python -m http.server 8000
   # Open http://localhost:8000 in browser
   ```

3. Commit and push changes:
   ```bash
   git add .
   git commit -m "Update website: describe your changes"
   git push origin main
   ```

4. GitHub Actions will automatically redeploy (check Actions tab)

## Custom Domain (Optional)

To use a custom domain:

1. Add a `CNAME` file to the repository root with your domain
2. Configure DNS settings with your domain provider
3. In GitHub Settings → Pages, add your custom domain
4. Enable "Enforce HTTPS"

See: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site

## Files Overview

### Website Files
- `index.html` - Main HTML structure
- `app.js` - JavaScript application logic
- `styles.css` - CSS styling
- `.nojekyll` - Tells GitHub Pages not to use Jekyll

### Deployment Files
- `.github/workflows/pages.yml` - GitHub Actions deployment workflow

### Documentation
- `WEBSITE.md` - Website documentation
- `GITHUB_PAGES_SETUP.md` - This file
- `README.md` - Repository overview

## Support

For issues or questions:
- Check GitHub Issues: https://github.com/Jonathan-Pearce/chess_openings/issues
- Review GitHub Pages docs: https://docs.github.com/en/pages
- Check GitHub Actions logs in the Actions tab

## Resources

- **GitHub Pages Documentation**: https://docs.github.com/en/pages
- **Chess.js**: https://github.com/jhlywa/chess.js
- **Chessboard.js**: https://chessboardjs.com/
- **Stockfish.js**: https://github.com/nmrugg/stockfish.js
- **Lichess API**: https://lichess.org/api
