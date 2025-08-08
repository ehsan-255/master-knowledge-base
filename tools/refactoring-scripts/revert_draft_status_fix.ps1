# This PowerShell script performs a surgical git operation to revert the status
# of 47 standard documents from 'active' back to 'draft'. It does this by
# checking out the last known good version of each file from the parent commit
# of the problematic "housekeeping" commit.

# The "good" commit hash, where all 47 files were still drafts.
$goodCommit = "8bd0a40d1a8235a77716b964e62bf6f6384d520b"

# The list of 47 files to be reverted. This list is derived from the
# `draft-standards-tracking-sheet.md` which was part of the L2-SL3 task.
$filesToRevert = @(
    "standards/src/AS-KB-DIRECTORY-STRUCTURE.md",
    "standards/src/AS-SCHEMA-CONCEPT-DEFINITION.md",
    "standards/src/AS-SCHEMA-METHODOLOGY-DESCRIPTION.md",
    "standards/src/AS-SCHEMA-REFERENCE.md",
    "standards/src/AS-SCHEMA-RELTABLE-DEFINITION.md",
    "standards/src/AS-SCHEMA-TASK.md",
    "standards/src/AS-STRUCTURE-ASSET-ORGANIZATION.md",
    "standards/src/AS-STRUCTURE-DOC-CHAPTER.md",
    "standards/src/AS-STRUCTURE-KB-PART.md",
    "standards/src/AS-STRUCTURE-KB-ROOT.md",
    "standards/src/AS-STRUCTURE-MASTER-KB-INDEX.md",
    "standards/src/AS-STRUCTURE-TEMPLATES-DIRECTORY.md",
    "standards/src/CS-ADMONITIONS-POLICY.md",
    "standards/src/CS-CONTENT-PROFILING-POLICY.md",
    "standards/src/CS-LINKING-INTERNAL-POLICY.md",
    "standards/src/CS-MODULARITY-TRANSCLUSION-POLICY.md",
    "standards/src/CS-POLICY-DIGITAL-ABSTRACTION.md",
    "standards/src/CS-POLICY-KB-IDENTIFICATION.md",
    "standards/src/CS-POLICY-KB-PART-CONTENT.md",
    "standards/src/CS-POLICY-LAYERED-INFORMATION.md",
    "standards/src/CS-POLICY-PART-OVERVIEW.md",
    "standards/src/CS-POLICY-SCOPE-EXCLUSION.md",
    "standards/src/CS-POLICY-SCOPE-INCLUSION.md",
    "standards/src/CS-POLICY-TONE-LANGUAGE.md",
    "standards/src/CS-TOC-POLICY.md",
    "standards/src/GM-GLOSSARY-STANDARDS-TERMS.md",
    "standards/src/GM-GUIDE-KB-USAGE.md",
    "standards/src/GM-MANDATE-KB-USAGE-GUIDE.md",
    "standards/src/GM-MANDATE-STANDARDS-GLOSSARY.md",
    "standards/src/GM-REGISTRY-GOVERNANCE.md",
    "standards/src/MT-KEYREF-MANAGEMENT.md",
    "standards/src/MT-REGISTRY-TAG-GLOSSARY.md",
    "standards/src/MT-STRATEGY-PRIMARY-TOPIC-KEYWORD.md",
    "standards/src/MT-TAGGING-STRATEGY-POLICY.md",
    "standards/src/MT-TAGS-IMPLEMENTATION.md",
    "standards/src/OM-AUTOMATION-LLM-PROMPT-LIBRARY.md",
    "standards/src/OM-OVERVIEW-PUBLISHING-PIPELINE.md",
    "standards/src/OM-POLICY-STANDARDS-DEPRECATION.md",
    "standards/src/OM-VERSIONING-CHANGELOGS.md",
    "standards/src/QM-VALIDATION-METADATA.md",
    "standards/src/SF-ACCESSIBILITY-IMAGE-ALT-TEXT.md",
    "standards/src/SF-CALLOUTS-SYNTAX.md",
    "standards/src/SF-FORMATTING-CITATIONS.md",
    "standards/src/SF-SYNTAX-DIAGRAMS-MERMAID.md",
    "standards/src/SF-SYNTAX-MATH-EQUATIONS.md",
    "standards/src/SF-SYNTAX-YAML-FRONTMATTER.md",
    "standards/src/SF-TOC-SYNTAX.md",
    "standards/src/SF-TRANSCLUSION-SYNTAX.md",
    "standards/src/UA-SCHEMA-LLM-IO.md"
)

Write-Host "Starting surgical fix to revert 47 standards to 'draft' status."
Write-Host "Restoring files from commit: $goodCommit"

foreach ($file in $filesToRevert) {
    Write-Host "Restoring: $file"
    git checkout $goodCommit -- $file
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to restore $file. Aborting."
        exit 1
    }
}

Write-Host "All 47 files have been restored to the staging area."
Write-Host "Committing the surgical fix..."

# The commit message, explaining the action clearly.
$commitMessage = @"
fix: Revert status of 47 standards to 'draft'

This commit performs a surgical fix to revert the status of 47 standard documents from 'active' back to 'draft'.

This change was necessitated by the undocumented mass-promotion in commit fb67f67, which occurred outside of established project protocols. This revert restores the repository to the state required by the 'audit-remediation-initiative' without affecting other changes made in the aforementioned commit.
"@

git commit -m $commitMessage

if ($LASTEXITCODE -eq 0) {
    Write-Host "Surgical fix successfully committed."
    Write-Host "The repository is now in the correct state to proceed with the audit-remediation-initiative."
} else {
    Write-Error "Git commit failed. Please review the status manually."
} 