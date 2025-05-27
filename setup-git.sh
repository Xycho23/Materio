# Initialize a new Git repository
git init

# Add all files to staging
git add .

# Create initial commit
git commit -m "Initial commit"

# Add remote origin
git remote add origin https://github.com/Xycho23/Materio.git

# Push to main branch
# If your default branch is 'main':
git push -u origin main
# Or if your default branch is 'master':
git push -u origin master
