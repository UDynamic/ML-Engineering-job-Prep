# 📁 Mastering Multiple `.gitignore` Files for Large Files in Git

*A practical guide with PowerShell commands*


## Multy layer ignoring from root folder

Final code in **Project/.gitignore** :

``` Git
# Define the path to the .gitignore file
$gitignorePath = "02-deep-learning-cifar/.gitignore"

# Create or append the ignore rules
@"
# Ignore the data folder (all contents)
data/

# Ignore all model checkpoint files, but keep the final model
models/checkpoint_*.pth
!models/final_model.pth
"@ | Add-Content -Path $gitignorePath 
```
---

## Quick review

| Goal | Command / Rule |
|------|----------------|
| **List tracked files** | `git ls-files` |
| **List untracked (not ignored) files** | `git ls-files --others --exclude-standard` |
| **List ignored files** | `git ls-files --others --ignored --exclude-standard` |
| **Check why a file is ignored** | `git check-ignore -v <file>` |
| **Untrack a file/folder (keep on disk)** | `git rm --cached <path>` |
| **Ignore a folder** | Add `folder_name/` to `.gitignore` |
| **Ignore all files of a type except one** | `*.ext`<br>`!important.ext` |
| **Stop tracking & ignore in one commit** | 1. `git rm --cached <path>`<br>2. Add ignore rule to `.gitignore`<br>3. Commit both changes |

---

## 2. 🧠 Understanding Multiple `.gitignore` Files

Git allows you to place `.gitignore` files in **any subdirectory** of your repository. Each one applies to that directory and its subdirectories. Rules are **cumulative** – if multiple `.gitignore` files match a file, the most specific (closest to the file) wins.

### Key Principles:
- **Scope:** A `.gitignore` affects its own folder and all subfolders
- **Precedence:** Rules in subdirectories override parent rules
- **Negation:** Use `!` to re-include specific files that were ignored by broader patterns
- **Combination:** Rules from all `.gitignore` files are combined

### Example Structure:
```
repo/
├── .gitignore                (ignores *.log)
├── models/
│   ├── .gitignore            (ignores *.pth, but !final_model.pth)
│   ├── final_model.pth       (tracked due to negation)
│   └── checkpoint_5.pth      (ignored)
└── data/
    └── .gitignore            (ignores everything in data/)
```

This is especially useful for:
- Ignoring large generated data folders (e.g., `data/`, `outputs/`)
- Selectively tracking only important files inside a folder

---

## 3. 🎯 Our Goal: A Deep Learning Project (CIFAR‑10)

We have a folder `02-deep-learning-cifar/` with this structure (partial):

```
02-deep-learning-cifar/
├── data/                    # Large dataset files (CIFAR-10)
│   └── cifar-10-batches-py/
│       ├── data_batch_1
│       ├── data_batch_2
│       ├── data_batch_3
│       ├── data_batch_4
│       ├── data_batch_5
│       ├── test_batch
│       └── batches.meta
├── models/                   # Trained models
│   ├── checkpoint_epoch5.pth
│   ├── checkpoint_epoch10.pth
│   ├── checkpoint_epoch15.pth
│   ├── checkpoint_epoch20.pth
│   └── final_model.pth       # The only one we want to keep tracked
├── .gitignore                # We'll edit this one
├── README.md
├── requirements.txt
└── src/                      # Source code folder
    ├── __init__.py
    ├── config.py
    ├── dataset.py
    ├── model.py
    ├── train.py
    └── utils.py
```

### Current Status (from your `git ls-files` output):
- ✅ All source code files are tracked (good!)
- ✅ README and requirements are tracked
- ✅ `.gitkeep` placeholder files exist (common for empty folders)
- ❌ **PROBLEM:** Large CIFAR-10 dataset files are tracked (~160MB)
- ❌ **PROBLEM:** All model checkpoint files are tracked (multiple .pth files)

### Requirements:
1. **Untrack** everything inside `data/` (already tracked)
2. **Untrack** all model checkpoints (keep only `final_model.pth`)
3. **Add ignore rules** so these files stay untracked in the future
4. **Keep** all source code, README, and other essential files tracked

---
## history

This is super common with ML projects - someone commits a 200MB model file, then removes it with .gitignore, but Git keeps it forever in history.

Let's find the culprits. Run this exact command:

```Git

git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | Where-Object {$_ -match "blob"} | ForEach-Object {$_ -replace "blob ", ""} | Sort-Object {[int]($_.Split()[1])} -Descending | Select-Object -First 10

```