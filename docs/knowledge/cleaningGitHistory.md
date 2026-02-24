# Git Repository Cleanup: Removing Large Files from History

*A step-by-step guide to diagnosing and fixing Git bloat caused by accidentally committed large files, using BFG Repo-Cleaner.*

---

## ⚡ Cheat Sheet – Quick Commands

| Step | Command |
|------|---------|
| **Find largest files in history** | `git rev-list --objects --all \| git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \| Where-Object {$_ -match "blob"} \| Sort-Object {[int]($_.Split()[1])} -Descending \| Select-Object -First 10` |
| **Install BFG** (if not already) | Download `bfg-1.14.0.jar` from [https://rtyley.github.io/bfg-repo-cleaner/](https://rtyley.github.io/bfg-repo-cleaner/) |
| **Run BFG to delete folders/files** | `java -jar bfg-1.14.0.jar --delete-folders "data" --delete-files "*.pth,*.tar.gz" .` |
| **Clean up Git after BFG** | `git reflog expire --expire=now --all` <br> `git gc --prune=now --aggressive` |
| **Verify packfile size** | `git count-objects -v` (look for `size-pack` in KB) |
| **Force‑push cleaned branch** | `git push origin <branch> --force` |
| **Override main with another branch** | `git push origin task2:main --force` |

---

## 1. The Problem

You noticed that a `git push` was **404 MB** and failed with an `HTTP 408` timeout, even though `git ls-files` showed only normal‑sized files. This indicates that **large files are present in the Git history**, even if they are no longer tracked.

Typical culprits in ML projects:
- Dataset files (e.g., CIFAR-10 batches, tar.gz archives)
- Model checkpoint files (`.pth`, `.h5`)
- Large notebooks with embedded outputs

---

## 2. Diagnosis – Finding the Large Files in History

Use this PowerShell command to list the largest blobs (file versions) ever committed:

```powershell
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | Where-Object {$_ -match "blob"} | ForEach-Object {$_ -replace "blob ", ""} | Sort-Object {[int]($_.Split()[1])} -Descending | Select-Object -First 10
```

**Sample output:**

```
90c5365492dea3b3c855b2375f1de8588ac1bda4 170498071 projects/02-deep-learning-cifar/data/cifar-10-python.tar.gz
66a0d630a7eb736563b1861ce716bdc489f2113b 31035999 projects/02-deep-learning-cifar/data/cifar-10-batches-py/data_batch_3
...
c73f3e880d47fc8b3065fd331e8e84727c8b7437 25476453 projects/02-deep-learning-cifar/models/checkpoint_epoch15.pth
```

This confirms that large files exist in the commit history and are causing the bloat.

---

## 3. Solution – Using BFG Repo‑Cleaner

[BFG Repo‑Cleaner](https://rtyley.github.io/bfg-repo-cleaner/) is a fast, simple tool to remove unwanted files from Git history.

### 3.1. Download BFG
- Go to [https://rtyley.github.io/bfg-repo-cleaner/](https://rtyley.github.io/bfg-repo-cleaner/)
- Download the `bfg-1.14.0.jar` file (or the latest version).

### 3.2. Run BFG from your repository root
```powershell
java -jar C:\path\to\bfg-1.14.0.jar --delete-folders "data" --delete-files "*.pth,*.tar.gz" .
```
- `--delete-folders "data"` removes any folder named `data` and its contents.
- `--delete-files "*.pth,*.tar.gz"` removes all files matching these patterns.
- Adjust patterns as needed (e.g., `checkpoint_*.pth` if you want to keep `final_model.pth`).

BFG will update your repository’s commits, stripping out the specified files.

### 3.3. Clean up Git’s internal data
After BFG finishes, run:

```powershell
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

This removes leftover references and compresses the repository.

### 3.4. Verify the cleanup
Check the packfile size:

```powershell
git count-objects -v
```

Look for `size-pack` (in KB). A clean repo should be much smaller – e.g., 80‑100 MB instead of 400+ MB.

Also re‑run the large‑file search; the huge blobs should be gone.

---

## 4. Pushing the Cleaned History

Because you rewrote history, you must force‑push your branch to the remote.

```powershell
git push origin task2 --force
```

If you want to replace the **main** branch entirely with your cleaned `task2` branch:

```powershell
git push origin task2:main --force
```

**⚠️ Warning:** This rewrites history on the remote. All collaborators must re‑clone or carefully rebase their work. Open pull requests may close automatically.

---

## 5. Handling Conflicts After Force Push

If you see a message like *"This branch has conflicts that must be resolved"* after force‑pushing, it means your local branch and the remote base branch have diverged. To resolve:

1. **Abort any ongoing merge:**
   ```powershell
   git merge --abort
   ```

2. **If you want your branch to become the new main, force‑push directly to main (see section 4).**

3. **If you need to merge changes from main (e.g., to update a PR), fetch and merge:**
   ```powershell
   git fetch origin main
   git checkout task2
   git merge origin/main
   ```
   Resolve conflicts manually, then:
   ```powershell
   git add <resolved-files>
   git commit -m "Merge main into task2"
   git push origin task2
   ```

---

## 6. Final Verification

- Run `git count-objects -v` again – the `size-pack` should be stable.
- Push a small change to confirm speed.
- Ask collaborators to re‑clone if necessary.

---

## 7. Important Notes

- **BFG changes commit hashes** – treat this as a one‑time cleanup.
- Always **backup** your repository before starting.
- Use `.gitignore` to prevent future accidents, and consider **Git LFS** for large binary files.
- After force‑pushing to main, protect the branch again if you temporarily disabled branch protection.

---