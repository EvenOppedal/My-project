# My-project
This is my project for EDX - python for data science 

## Tools

### Find Commits with Many Deletions

A Python script to analyze Git repository history and identify commits with many deletions.

#### Usage

```bash
# Find commits with at least 100 deletions (default threshold)
python3 find_deletions.py

# Find commits with at least 50 deletions
python3 find_deletions.py --threshold 50

# Find commits with at least 10 deletions and show full details
python3 find_deletions.py --threshold 10 --all

# Show only top 5 commits with most deletions
python3 find_deletions.py --threshold 10 --top 5

# Analyze a different repository
python3 find_deletions.py --repo /path/to/repo --threshold 100
```

#### Features

- Analyzes all commits in the repository
- Shows commit hash, author, date, and subject
- Displays insertion/deletion statistics for each commit
- Configurable deletion threshold
- Option to limit results to top N commits
- Summary statistics including total and average deletions

#### Options

- `--threshold, -t`: Minimum number of deletions to consider (default: 100)
- `--repo, -r`: Path to git repository (default: current directory)
- `--all, -a`: Show all commit details including full hash
- `--top, -n`: Show only top N commits with most deletions
- `--help, -h`: Show help message
