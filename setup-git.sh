# Remove old .git directory if it exists
rm -rf .git

# Initialize new repository
git init

# Add new remote origin
git remote add origin https://github.com/Xycho23/Materio.git

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit"

# Rename branch to main and push
git branch -M main
git push -u origin main
