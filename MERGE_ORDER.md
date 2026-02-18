# Quick Reference: PR Merge Order

## ✅ ALL 5 PRs SHOULD BE MERGED

Execute in this exact order:

```
┌─────────────────────────────────────────────────┐
│ 1️⃣  PR #2: Weekly RFP Aggregator              │
│    Branch: copilot/add-weekly-rfp-aggregator   │
│    Priority: CRITICAL - Base pipeline          │
│    Conflicts: Yes (resolve first)              │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ 2️⃣  PR #3: Budget Extraction Function         │
│    Branch: copilot/add-budget-extract-function │
│    Priority: HIGH - Core feature               │
│    Conflicts: Yes (should be minimal)          │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ 3️⃣  PR #4: Source Weighting Function          │
│    Branch: copilot/add-source-weighting-func.  │
│    Priority: MEDIUM - Scoring enhancement      │
│    Conflicts: Yes (package structure)          │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ 4️⃣  PR #5: Score Item Function                │
│    Branch: copilot/compute-final-score         │
│    Priority: MEDIUM - Modular scoring          │
│    Conflicts: Yes (package structure)          │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ 5️⃣  PR #6: GitHub Actions Workflow            │
│    Branch: copilot/create-weekly-rfps-workflow │
│    Priority: LOW - Automation layer            │
│    Conflicts: Yes (most complex)               │
│    ⚠️  Review firewall warnings                │
└─────────────────────────────────────────────────┘
```

## After Each Merge

1. Update the next PR branch: `git rebase main`
2. Resolve conflicts
3. Run tests: `python -m pytest tests/`
4. Verify functionality

## Important Notes

- **All PRs have merge conflicts** - this is expected
- **PR #2 is the foundation** - merge it first
- **PR #6 has firewall warnings** - may need allowlist config
- **Test after each merge** - don't wait until the end

## Quick Commands

```bash
# For each PR in order:
git fetch origin
git checkout <branch-name>
git rebase main
# ... resolve conflicts ...
git push --force-with-lease
# ... then merge via GitHub UI ...
```

See `PR_REVIEW_ANALYSIS.md` for detailed analysis.
