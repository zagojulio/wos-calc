# 🧯 Emergency: Recover `dev` from Remote (Discard Local Changes)

If something goes wrong in the `dev` branch and you need to restore it to match the remote:

1. Switch to the `dev` branch:
   ```bash
   git checkout dev
   ```

2. Fetch the latest state from the remote:
   ```bash
   git fetch origin
   ```

3. Reset your local `dev` to match the remote exactly:
   ```bash
   git reset --hard origin/dev
   ```

4. (Optional) Clean untracked files:
   ```bash
   git clean -fd
   ```

⚠️ Warning: This will delete all local changes and commits that are not in `origin/dev`.

# 🧭 Feature Development Git Workflow (Whiteout Survival Project)

## ✅ Before You Begin

1. Sync the `main` and `dev` branches locally:
   ```bash
   git checkout main
   git pull origin main

   git checkout dev
   git pull origin dev
   ```

2. Create a new feature branch from `dev`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

---

## 🛠 While Developing

3. Work inside `feature/your-feature-name`
   - Save often and commit small logical units

4. Stage and commit your changes regularly:
   ```bash
   git add .
   git commit -m "[TYPE]: Short description of your work"
   ```
   Example commit types:
   - `[FEAT]: Add new training calculator component`
   - `[FIX]: Correct bonus percentage logic`
   - `[REFACTOR]: Clean up input handling`
   - `[TEST]: Add unit tests for formatters`
   - `[DOC]: Update README and changelog`

5. Push your branch to remote (only the first time):
   ```bash
   git push -u origin feature/your-feature-name
   ```

---

## 🧪 After Development

6. Test everything locally:
   - Run the app:
     ```bash
     streamlit run app.py
     ```
   - Run tests:
     ```bash
     pytest
     ```

7. Sync your feature branch with latest `dev` before merging:
   ```bash
   git checkout feature/your-feature-name
   git pull origin dev --rebase
   ```

---

## 🔀 Merge Back to `dev`

8. Merge your feature branch into `dev`:
   ```bash
   git checkout dev
   git pull origin dev
   git merge feature/your-feature-name -m "Merge: Finalize your-feature-name"
   git push origin dev
   ```

9. (Optional) Delete the feature branch:
   ```bash
   git branch -d feature/your-feature-name
   git push origin --delete feature/your-feature-name
   ```

---

## 🚀 Release to `main`

10. Merge `dev` into `main`:
    ```bash
    git checkout main
    git pull origin main
    git merge dev -m "Release: v0.X.X - Description of features"
    git push origin main
    ```

11. Tag the release:
    ```bash
    git tag v0.X.X -m "Release v0.X.X: Key improvements and features"
    git push origin v0.X.X
    ```

12. Update project documentation:
    - `CHANGELOG.md`
    - `TASKS.md`
    - `README.md` (if needed)

---

✅ Done! Your feature is released and history is clean. Ready for the next one.