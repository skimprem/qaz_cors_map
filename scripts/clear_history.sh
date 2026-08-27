#!/usr/bin/env bash
set -euo pipefail

echo "This script helps remove specified paths from the repository history using git-filter-repo."
echo "IT MUST BE RUN LOCALLY. It will perform a mirror clone, rewrite history, and force-push."
echo

REPO_URL=$(git config --get remote.origin.url || true)
if [ -z "$REPO_URL" ]; then
  echo "Could not determine remote origin URL. Run this inside a git clone with origin set." >&2
  exit 1
fi

if ! command -v git-filter-repo >/dev/null 2>&1; then
  echo "git-filter-repo not found. Install it first: https://github.com/newren/git-filter-repo#install"
  echo "On Debian/Ubuntu: pip install --user git-filter-repo" >&2
  exit 1
fi

echo "Repository remote: $REPO_URL"
echo
echo "Paths to remove from history (examples):"
echo "  data/report/"
echo "  instructions/"
echo "  data/chat.md"
echo
read -rp "Enter paths to remove, separated by spaces: " -a TO_REMOVE
if [ ${#TO_REMOVE[@]} -eq 0 ]; then
  echo "No paths provided — aborting." >&2
  exit 1
fi

echo
echo "You are about to permanently remove these paths from the repository history:"
for p in "${TO_REMOVE[@]}"; do echo " - $p"; done
echo
read -rp "Type the repository name to confirm (or Ctrl-C to abort): " CONFIRM
REPO_NAME=$(basename -s .git "${REPO_URL}")
if [ "$CONFIRM" != "$REPO_NAME" ]; then
  echo "Confirmation mismatch (expected: $REPO_NAME). Aborting." >&2
  exit 1
fi

TMPDIR=$(mktemp -d)
echo "Creating mirror clone in $TMPDIR/repo.git ..."
git clone --mirror "$REPO_URL" "$TMPDIR/repo.git"

cd "$TMPDIR/repo.git"

FILTER_CMD=(git-filter-repo --force --invert-paths)
for p in "${TO_REMOVE[@]}"; do
  FILTER_CMD+=(--path "$p")
done

echo "Running: ${FILTER_CMD[*]}"
"${FILTER_CMD[@]}"

echo "Pushing rewritten history back to remote (force)..."
git push --force --all
git push --force --tags

echo "Cleanup local mirror: $TMPDIR"
echo "DONE. Inform collaborators: they'll need to reclone or reset their local clones." 

cat <<'EOF'
Post-clean steps for collaborators:
  - Everyone must reclone the repository, or run:
      git fetch --all
      git reset --hard origin/main
  - Remove any local branches pointing to old history.

Warning: This operation rewrites public history. Coordinate with your team before proceeding.
EOF
