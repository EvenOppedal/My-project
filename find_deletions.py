#!/usr/bin/env python3
"""
Script to find commits in a Git repository with many deletions.
"""

import subprocess
import sys
import argparse
from typing import List, Dict, Tuple


def get_commit_stats(repo_path: str = ".") -> List[Dict[str, any]]:
    """
    Get commit statistics including number of deletions for each commit.
    
    Args:
        repo_path: Path to the git repository (default: current directory)
    
    Returns:
        List of dictionaries containing commit information
    """
    try:
        # Get commit information with stats
        cmd = [
            "git", "-C", repo_path, "log", "--all", "--numstat",
            "--pretty=format:COMMIT_START%n%H%n%h%n%an%n%ae%n%ad%n%s"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        commits = []
        current_commit = None
        
        for line in output.split('\n'):
            if line == "COMMIT_START":
                if current_commit:
                    commits.append(current_commit)
                current_commit = {
                    'hash': '',
                    'short_hash': '',
                    'author': '',
                    'email': '',
                    'date': '',
                    'subject': '',
                    'insertions': 0,
                    'deletions': 0,
                    'files_changed': 0
                }
                state = 'hash'
            elif current_commit:
                if state == 'hash':
                    current_commit['hash'] = line
                    state = 'short_hash'
                elif state == 'short_hash':
                    current_commit['short_hash'] = line
                    state = 'author'
                elif state == 'author':
                    current_commit['author'] = line
                    state = 'email'
                elif state == 'email':
                    current_commit['email'] = line
                    state = 'date'
                elif state == 'date':
                    current_commit['date'] = line
                    state = 'subject'
                elif state == 'subject':
                    current_commit['subject'] = line
                    state = 'stats'
                elif state == 'stats':
                    # Parse numstat output: insertions, deletions, filename
                    parts = line.split('\t')
                    if len(parts) == 3:
                        insertions, deletions, filename = parts
                        # Handle binary files (marked as -)
                        if insertions != '-':
                            current_commit['insertions'] += int(insertions)
                        if deletions != '-':
                            current_commit['deletions'] += int(deletions)
                        current_commit['files_changed'] += 1
        
        # Add the last commit
        if current_commit:
            commits.append(current_commit)
        
        return commits
    
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def find_commits_with_many_deletions(
    commits: List[Dict[str, any]], 
    threshold: int = 100,
    sort_by_deletions: bool = True
) -> List[Dict[str, any]]:
    """
    Filter commits that have many deletions.
    
    Args:
        commits: List of commit dictionaries
        threshold: Minimum number of deletions to consider (default: 100)
        sort_by_deletions: Whether to sort by deletions descending (default: True)
    
    Returns:
        List of commits with many deletions
    """
    filtered = [c for c in commits if c['deletions'] >= threshold]
    
    if sort_by_deletions:
        filtered.sort(key=lambda x: x['deletions'], reverse=True)
    
    return filtered


def display_commits(commits: List[Dict[str, any]], show_all: bool = False):
    """
    Display commit information in a readable format.
    
    Args:
        commits: List of commit dictionaries
        show_all: Whether to show all commits or just summary
    """
    if not commits:
        print("No commits found with the specified criteria.")
        return
    
    print(f"\nFound {len(commits)} commit(s) with many deletions:\n")
    print("=" * 100)
    
    for i, commit in enumerate(commits, 1):
        print(f"\n{i}. Commit: {commit['short_hash']}")
        print(f"   Author: {commit['author']} <{commit['email']}>")
        print(f"   Date: {commit['date']}")
        print(f"   Subject: {commit['subject']}")
        print(f"   Files changed: {commit['files_changed']}")
        print(f"   Insertions: +{commit['insertions']}")
        print(f"   Deletions: -{commit['deletions']}")
        print(f"   Net change: {commit['insertions'] - commit['deletions']}")
        
        if show_all:
            print(f"   Full hash: {commit['hash']}")
    
    print("\n" + "=" * 100)
    
    # Summary statistics
    total_deletions = sum(c['deletions'] for c in commits)
    avg_deletions = total_deletions / len(commits) if commits else 0
    
    print(f"\nSummary:")
    print(f"  Total commits analyzed: {len(commits)}")
    print(f"  Total deletions: {total_deletions}")
    print(f"  Average deletions per commit: {avg_deletions:.2f}")
    if commits:
        print(f"  Max deletions in a single commit: {max(c['deletions'] for c in commits)}")
        print(f"  Min deletions in filtered commits: {min(c['deletions'] for c in commits)}")


def main():
    parser = argparse.ArgumentParser(
        description="Find commits in a Git repository with many deletions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Find commits with at least 100 deletions (default)
  python find_deletions.py
  
  # Find commits with at least 50 deletions
  python find_deletions.py --threshold 50
  
  # Find commits with at least 10 deletions and show full details
  python find_deletions.py --threshold 10 --all
  
  # Analyze a different repository
  python find_deletions.py --repo /path/to/repo --threshold 100
"""
    )
    
    parser.add_argument(
        '--threshold', '-t',
        type=int,
        default=100,
        help='Minimum number of deletions to consider (default: 100)'
    )
    
    parser.add_argument(
        '--repo', '-r',
        type=str,
        default='.',
        help='Path to git repository (default: current directory)'
    )
    
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Show all commit details including full hash'
    )
    
    parser.add_argument(
        '--top', '-n',
        type=int,
        help='Show only top N commits with most deletions'
    )
    
    args = parser.parse_args()
    
    print(f"Analyzing repository: {args.repo}")
    print(f"Looking for commits with at least {args.threshold} deletions...")
    
    # Get all commits with stats
    all_commits = get_commit_stats(args.repo)
    
    if not all_commits:
        print("No commits found in the repository.")
        return
    
    print(f"Total commits in repository: {len(all_commits)}")
    
    # Filter commits with many deletions
    filtered_commits = find_commits_with_many_deletions(all_commits, args.threshold)
    
    # Limit to top N if specified
    if args.top and args.top > 0:
        filtered_commits = filtered_commits[:args.top]
    
    # Display results
    display_commits(filtered_commits, args.all)


if __name__ == "__main__":
    main()
