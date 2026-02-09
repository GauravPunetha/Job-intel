# GitHub Push Instructions

## Step 1: Install Git (if not already installed)

**Windows:** Download from https://git-scm.com/download/win

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., `job-intelligence`)
3. Choose Public or Private
4. DO NOT initialize with README (we have one)
5. Click "Create repository"

## Step 3: Push Code to GitHub

In PowerShell, navigate to the project directory:

```powershell
cd C:\Users\10735751\Downloads\job-intel-starter\job-intel

# Initialize git
git init

# Configure user (one-time)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Job Intelligence Platform"

# Add remote (replace USERNAME and REPO_NAME)
git remote add origin https://github.com/USERNAME/REPO_NAME.git

# Push to GitHub (first time)
git branch -M main
git push -u origin main
```

## Step 4: Verify on GitHub

Visit `https://github.com/USERNAME/REPO_NAME` to see your code uploaded!

## Future Pushes

After making changes:

```powershell
git add .
git commit -m "Your commit message"
git push
```

## Optional: Add GitHub SSH Key

For passwordless pushes:

```powershell
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Copy public key and add to GitHub Settings → SSH Keys
```

Then use SSH URL instead:
```
git remote add origin git@github.com:USERNAME/REPO_NAME.git
```

---

**Project Ready for GitHub!** ✅
- Clean codebase with no unnecessary files
- Clear README with setup instructions
- Contributing guidelines included
- MIT License included
- .gitignore properly configured
