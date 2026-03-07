# New Relic

A starter project folder for your **new relic** repository.

## What is included

- `create-github-repo.sh`: a helper script to create and push this project to your GitHub account.

## Create the GitHub repository (recommended)

From inside this folder, run:

```bash
bash create-github-repo.sh <your-github-username>
```

Example:

```bash
bash create-github-repo.sh felixwubootcamp
```

This will:

1. Initialize a local git repository.
2. Create an initial commit.
3. Create a GitHub repo named `new-relic` (private by default).
4. Push `main` to GitHub.

## Manual alternative

If you prefer to create the repo yourself in the GitHub UI, use:

```bash
git init
git add .
git commit -m "Initial commit for New Relic project"
git branch -M main
git remote add origin git@github.com:<your-username>/new-relic.git
git push -u origin main
```
