# NSC Version 2 Migration Guide

This kit is an **overlay for the existing NorthStar Comms repository**. It is not a new repository and it does not replace labor-intensive project documentation.

## Preserve Version 1 first

Before copying any Version 2 files, make sure the current `main` branch is clean and committed.

### GitHub Desktop method

1. Open GitHub Desktop.
2. Select the NorthStar Comms repository.
3. Review the **Changes** tab.
4. Enter the summary `Checkpoint NorthStar Comms Version 1`.
5. Select **Commit to main**.
6. Select **Push origin**.
7. In the top menu, choose **Branch → New branch**.
8. Name the branch `nsc-v2`.
9. Create it from `main`.
10. Select **Publish branch**.

### Command-line method

```bash
git status
git add .
git commit -m "Checkpoint NorthStar Comms Version 1"
git push origin main

git tag -a v1.0.0 -m "NorthStar Comms Version 1 checkpoint"
git push origin v1.0.0

git switch -c nsc-v2
git push -u origin nsc-v2
```

Do not run the commit command when `git status` says there is nothing to commit. The tag should be created on the final Version 1 commit.

## Optional GitHub release for the Version 1 tag

On GitHub, open the repository, select **Releases**, choose **Draft a new release**, select the existing `v1.0.0` tag, and publish it as `NorthStar Comms Version 1`. A release is optional; the tag itself is the historical checkpoint.

## Copy the Version 2 kit

Copy these folders into the repository root:

```text
data/
profiles/
scripts/
tests/
exports/
docs/migrations/
```

### Efficient replacement rule

- **Merge folders; do not delete the repository root.**
- Replace a same-named generated/test file only after reviewing it.
- Keep the existing `README.md`, `CHANGELOG.md`, `LICENSE`, project documentation, issue templates, and GitHub configuration.
- Copy the contents of `snippets/README_V2_SECTION.md` into the existing README at the architecture/build section.
- Copy the newest entry from `snippets/CHANGELOG_V2_ENTRY.md` into the existing CHANGELOG.
- Add the lines in `snippets/GITIGNORE_ADDitions.txt` to the existing `.gitignore`; do not overwrite the whole file.

GitHub Desktop can perform the copy safely:
1. Open **Repository → Show in Explorer/Finder**.
2. Open this migration kit in a second window.
3. Drag the listed folders into the repository.
4. When prompted about same-named folders, choose **merge**.
5. Review all changes in GitHub Desktop before committing.

## Build and validate

From the repository root:

```bash
python scripts/validate_nsc.py
python scripts/build_exports.py --radio all
```

Expected outputs:

```text
exports/gm25/NSC_GM25_CHIRP_v2.csv
exports/uv5r/NSC_UV5R_BAOFENG_STOCK_v2_PROVISIONAL.csv
exports/uv32/NSC_UV32_CPS_v2.csv
```

The UV-5R file remains provisional because the supplied `.dat` file is a radio image rather than a stock-software CSV schema export.

## Commit Version 2 migration

```bash
git status
git add data profiles scripts tests exports docs snippets
git commit -m "Add NSC Version 2 canonical data and radio exporters"
git push origin nsc-v2
```

## Test on radios before merging

1. Import the GM25 export into CHIRP and confirm all 128 rows.
2. Import the UV32 export and confirm the known successful column structure.
3. Test the provisional UV-5R export in the Baofeng software.
4. Record any corrections in the profile—not by manually editing the generated output.
5. Rebuild and retest.

After successful testing, open a pull request from `nsc-v2` into `main`. Review the file changes, merge the pull request, then create a `v2.0.0` tag/release.
