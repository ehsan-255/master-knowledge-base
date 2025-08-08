$files = @(
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

foreach ($file in $files) {
    $content = Get-Content -Path $file -Raw
    $newContent = $content -replace 'status: active', 'status: draft'
    # Use -NoNewline to prevent adding extra lines at the end of the file
    Set-Content -Path $file -Value $newContent -NoNewline
    Write-Host "Processed $file"
}

Write-Host "Done." 