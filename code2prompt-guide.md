# Code2Prompt CLI Guide

A comprehensive guide for using the Code2Prompt CLI tool to convert your codebase into structured LLM prompts.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [File Filtering Patterns](#file-filtering-patterns)
3. [Handlebars Templates](#handlebars-templates)
4. [Built-in Templates](#built-in-templates)
5. [Custom Templates](#custom-templates)
6. [Advanced Features](#advanced-features)
7. [Examples](#examples)
8. [Best Practices](#best-practices)



## Basic Usage

### Simple Command
```bash
code2prompt /path/to/your/codebase
```

### Basic Options
```bash
code2prompt /path/to/your/codebase \
  --output-file output.md \
  --output-format markdown \
  --tokens format
```

### Command Structure
```bash
code2prompt [OPTIONS] <PATH>
```

**Arguments:**
- `<PATH>` - Path to the codebase directory

**Common Options:**
- `-i, --include <INCLUDE>` - Patterns to include
- `-e, --exclude <EXCLUDE>` - Patterns to exclude
- `-O, --output-file <OUTPUT_FILE>` - Output file path
- `-F, --output-format <OUTPUT_FORMAT>` - Output format (markdown, json, xml)
- `-t, --template <TEMPLATE>` - Custom Handlebars template path
- `-c, --encoding <ENCODING>` - Tokenizer (cl100k, p50k, p50k_edit, r50k, gpt2)
- `--tokens <FORMAT>` - Display token count (raw or format)
- `-d, --diff` - Include git diff
- `-l, --line-numbers` - Add line numbers to source code
- `--absolute-paths` - Use absolute paths instead of relative
- `--hidden` - Include hidden directories and files
- `--no-clipboard` - Disable copying to clipboard

## File Filtering Patterns

### Include Patterns
Use glob patterns to include specific files:

```bash
# Include only JavaScript and HTML files
code2prompt . --include "*.js,*.html"

# Include multiple patterns
code2prompt . --include "*.py,*.js,*.md"

# Include files from specific directories
code2prompt . --include "src/**/*.js,lib/**/*.py"
```

### Exclude Patterns
Use glob patterns to exclude files:

```bash
# Exclude node_modules and build directories
code2prompt . --exclude "node_modules/,build/,dist/"

# Exclude multiple patterns
code2prompt . --exclude "*.log,*.tmp,*.cache"

# Exclude hidden files
code2prompt . --exclude ".*"
```

### Include vs Exclude Priority
By default, exclude patterns take precedence. Use `--include-priority` to reverse this:

```bash
code2prompt . --include "*.js" --exclude "test/*.js" --include-priority
```

### Respect .gitignore
By default, code2prompt respects `.gitignore` rules. Use `--no-ignore` to disable:

```bash
code2prompt . --no-ignore
```

## Handlebars Templates

Code2Prompt uses Handlebars templating engine for customizable prompt generation.

### Template Syntax

**Basic Variables:**
```handlebars
{{absolute_code_path}}     # Absolute path to codebase
{{source_tree}}           # Directory tree structure
{{files}}                 # Array of file objects
{{git_diff}}              # Git diff (if available)
```

**File Object Properties:**
```handlebars
{{#each files}}
  Path: {{path}}          # File path
  Content: {{code}}       # File content
  Size: {{size}}          # File size
  Modified: {{modified}}  # Last modified date
{{/each}}
```

**Conditional Logic:**
```handlebars
{{#if files}}
  {{#each files}}
    File: {{path}}
    Content: {{code}}
  {{/each}}
{{else}}
  No files found.
{{/if}}
```

### Using Templates

```bash
# Use a custom template
code2prompt . --template my-template.hbs

# Use built-in template
code2prompt . --template document-the-code.hbs
```

## Built-in Templates

**Note**: The cargo installation doesn't include built-in templates by default. I've created a set of official templates from the [GitHub repository](https://github.com/mufeedvh/code2prompt/tree/main/crates/code2prompt-core/templates) in the `templates/` directory for you to use.

### Available Templates

#### 1. document-the-code.hbs
**Purpose**: Generates prompts for comprehensive code documentation with language-specific comment styles.

**What it does**:
- Analyzes all public functions, methods, classes, and modules
- Adds idiomatic documentation comments (/// for Rust, """ for Python, /** */ for TypeScript, etc.)
- Includes parameter descriptions, return values, error cases, and related code entities
- Places comments directly above function/class/module definitions

**Use case**: When you need to add professional documentation to your codebase.

```bash
code2prompt . --template templates/document-the-code.hbs
```

#### 2. find-security-vulnerabilities.hbs
**Purpose**: Performs comprehensive security analysis to identify potential vulnerabilities.

**What it does**:
- Scans for input validation vulnerabilities, SQL injection, XSS, authentication issues
- Checks for insecure data handling, configuration problems, and outdated dependencies
- Identifies privilege escalation, resource consumption, and cryptographic weaknesses
- Provides detailed vulnerability reports with file paths, line numbers, impact assessment, and remediation steps
- Generates a Markdown table with CVSS vectors and confidence scores

**Use case**: Security audits, penetration testing preparation, compliance reviews.

```bash
code2prompt . --template templates/find-security-vulnerabilities.hbs
```

#### 3. clean-up-code.hbs
**Purpose**: Improves code quality through refactoring and cleanup without changing behavior.

**What it does**:
- Enhances readability, clarity, and adherence to language idioms
- Improves modularity, organization, and consistency in style
- Removes unused code, simplifies complex logic, and improves naming
- Maintains existing functionality while improving error handling
- Adds explanatory comments for changes made

**Use case**: Code maintenance, technical debt reduction, preparation for code reviews.

```bash
code2prompt . --template templates/clean-up-code.hbs
```

#### 4. fix-bugs.hbs
**Purpose**: Identifies and fixes potential bugs through systematic code analysis.

**What it does**:
- Diagnoses edge cases, off-by-one errors, unexpected data types
- Identifies uncaught exceptions, concurrency issues, and configuration problems
- Provides specific bug locations, descriptions, and example inputs that trigger issues
- Suggests fixes while maintaining existing code style
- Recommends regression tests to prevent recurrence

**Use case**: Debugging sessions, quality assurance, pre-release testing.

```bash
code2prompt . --template templates/fix-bugs.hbs
```

#### 5. write-github-pull-request.hbs
**Purpose**: Creates professional GitHub pull request descriptions from git changes.

**What it does**:
- Analyzes git diffs and logs to understand changes
- Generates structured PR descriptions with clear sections
- Includes motivation, detailed changes, and context
- Follows GitHub best practices for PR documentation
- Provides human-readable explanations for technical changes

**Use case**: Creating pull requests, documenting code changes, team collaboration.

```bash
code2prompt . --template templates/write-github-pull-request.hbs --diff
```

#### 6. write-github-readme.hbs
**Purpose**: Generates comprehensive README files suitable for GitHub projects.

**What it does**:
- Analyzes codebase to understand project purpose and functionality
- Creates professional README with title, description, features, installation instructions
- Includes usage examples, configuration options, and contribution guidelines
- Adds testing instructions, license information, and acknowledgments
- Makes projects accessible to new users and contributors

**Use case**: Project documentation, open source preparation, onboarding new developers.

```bash
code2prompt . --template templates/write-github-readme.hbs
```

#### 7. write-git-commit.hbs
**Purpose**: Generates conventional git commit messages from code changes.

**What it does**:
- Analyzes git diffs to understand the purpose of changes
- Creates concise, informative commit messages following conventional commit format
- Uses imperative mood, proper capitalization, and appropriate length
- Includes descriptive body when needed
- Separates subject from body with blank lines

**Use case**: Creating meaningful commit messages, maintaining clean git history, team collaboration.

```bash
code2prompt . --template templates/write-git-commit.hbs
```

#### 8. improve-performance.hbs
**Purpose**: Optimizes code performance while maintaining correctness and readability.

**What it does**:
- Analyzes algorithm complexity and identifies expensive operations
- Suggests caching, memoization, and parallelization opportunities
- Recommends more efficient data structures and built-in functions
- Identifies unnecessary iterations and repeated calculations
- Provides specific optimization suggestions with estimated impact
- Maintains code clarity while improving performance

**Use case**: Performance optimization, scalability improvements, resource efficiency.

```bash
code2prompt . --template templates/improve-performance.hbs
```

#### 9. binary-exploitation-ctf-solver.hbs
**Purpose**: Solves CTF binary exploitation challenges with systematic analysis and exploit development.

**What it does**:
- Examines source code for vulnerabilities (buffer overflow, use-after-free, integer issues)
- Performs static analysis to identify vulnerable functions and security mitigations
- Conducts dynamic analysis with debuggers to understand crash behavior
- Develops exploit strategies (EIP control, arbitrary read/write, information leak)
- Constructs payloads using tools like pwntools, Ropper, one_gadget
- Ensures exploit reliability for remote challenges

**Use case**: CTF competitions, security research, exploit development training.

```bash
code2prompt . --template templates/binary-exploitation-ctf-solver.hbs
```

#### 10. cryptography-ctf-solver.hbs
**Purpose**: Solves CTF cryptography challenges by analyzing encryption methods and finding weaknesses.

**What it does**:
- Identifies encryption types (classical ciphers, modern symmetric/asymmetric crypto, hashes)
- Analyzes cryptographic weaknesses (weak keys, insecure modes, oracle attacks)
- Performs decryption attempts (brute-force, frequency analysis, mathematical exploits)
- Cracks hashes using wordlists, rules, and masks
- Handles encoding schemes (Base64, hex, etc.) and padding oracle vulnerabilities

**Use case**: CTF competitions, cryptography research, security analysis.

```bash
code2prompt . --template templates/cryptography-ctf-solver.hbs
```

#### 11. reverse-engineering-ctf-solver.hbs
**Purpose**: Solves CTF reverse engineering challenges through binary analysis and debugging.

**What it does**:
- Identifies target file types (compiled binaries, bytecode, obfuscated scripts)
- Sets up analysis environment with disassemblers, debuggers, and VM isolation
- Performs static analysis to find strings, imported functions, and control flow
- Conducts dynamic analysis with breakpoints and memory inspection
- Bypasses anti-reversing techniques (packing, anti-debug, obfuscation)
- Solves input checks and locates flags in memory or decrypted resources

**Use case**: CTF competitions, malware analysis, software reverse engineering.

```bash
code2prompt . --template templates/reverse-engineering-ctf-solver.hbs
```

#### 12. claude-xml.hbs
**Purpose**: Generates XML-formatted output optimized for Claude AI models.

**What it does**:
- Structures project information in XML format for Claude's preferred input
- Includes project path, source tree, and file contents in XML tags
- Provides conditional instructions section for custom prompts
- Uses Claude's recommended XML structure for better comprehension
- Optimizes output specifically for Claude's processing capabilities

**Use case**: When working with Claude AI models, structured data analysis, XML-based workflows.

```bash
code2prompt . --template templates/claude-xml.hbs
```

#### 13. refactor.hbs
**Purpose**: Refactors codebase to improve design, maintainability, and performance following SOLID principles.

**What it does**:
- Analyzes code for adherence to SOLID principles and design patterns
- Identifies code smells, duplication, and areas for improvement
- Suggests refactoring strategies for better separation of concerns
- Improves naming, readability, and modularity
- Removes dead code and updates to modern language features
- Maintains existing functionality while improving architecture
- Provides step-by-step refactoring with explanations and benefits

**Use case**: Code architecture improvements, technical debt reduction, design pattern implementation.

```bash
code2prompt . --template templates/refactor.hbs
```

#### 14. web-ctf-solver.hbs
**Purpose**: Solves CTF web exploitation challenges by testing for common web vulnerabilities and crafting exploits.

**What it does**:
- Explores web applications to identify endpoints, authentication, and input fields
- Analyzes page source and HTTP traffic for clues and vulnerabilities
- Tests for common web vulnerabilities (SQL injection, XSS, template injection)
- Identifies command injection, directory traversal, and access control issues
- Crafts malicious payloads for exploitation (SQL injection, XSS, etc.)
- Locates flags in admin pages, database dumps, or source code files
- Provides vulnerable URLs and exploit payloads for CTF challenges

**Use case**: CTF competitions, web security research, penetration testing practice.

```bash
code2prompt . --template templates/web-ctf-solver.hbs
```

#### 15. hma-v2.2-compliance-analyzer.hbs
**Purpose**: Analyzes codebases for compliance with Hexagonal Microkernel Architecture (HMA) v2.2 principles and standards.

**What it does**:
- Evaluates layered architecture compliance (L0-L4 layers)
- Assesses core architectural principles (plugin autonomy, explicit boundaries, minimal core)
- Validates mandatory interoperability standards (Tier 1 requirements)
- Analyzes technology stack against three-tier framework (Mandatory/Recommended/Alternative)
- Reviews plugin structure and standard port implementations
- Checks event-driven architecture compliance
- Evaluates security implementation and trust boundaries
- Assesses observability implementation and telemetry standards
- Provides detailed compliance scoring and migration recommendations

**Use case**: Architecture reviews, HMA v2.2 compliance audits, migration planning, technology stack evaluation.

```bash
code2prompt . --template templates/hma-v2.2-compliance-analyzer.hbs
```

## Custom Templates

### Creating Custom Templates

Create a `.hbs` file with your custom template:

```handlebars
# my-custom-template.hbs
Project Analysis Request

**Project Path:** {{absolute_code_path}}

**Source Tree:**
```
{{source_tree}}
```

**Files to Analyze:**
{{#each files}}
### {{path}}
```{{file_extension}}
{{code}}
```
{{/each}}

**Analysis Request:**
Please analyze this codebase and provide:
1. Code quality assessment
2. Potential improvements
3. Security considerations
4. Performance optimizations
```

### User-Defined Variables

You can add custom variables to your templates:

```handlebars
# template-with-variables.hbs
Analysis for: {{project_name}}
Focus Area: {{focus_area}}
Priority: {{priority_level}}

{{#each files}}
File: {{path}}
Content: {{code}}
{{/each}}
```

When using this template, code2prompt will prompt you to enter values for `project_name`, `focus_area`, and `priority_level`.

## Advanced Features

### Git Integration

**Include Git Diff:**
```bash
code2prompt . --diff
```

**Compare Branches:**
```bash
code2prompt . --git-diff-branch main feature-branch
```

**Git Log Between Branches:**
```bash
code2prompt . --git-log-branch main feature-branch
```

### Token Counting

**Display Token Count:**
```bash
code2prompt . --tokens format
```

**Raw Token Count:**
```bash
code2prompt . --tokens raw
```

**Custom Tokenizer:**
```bash
code2prompt . --encoding cl100k  # OpenAI models
code2prompt . --encoding p50k    # GPT-2 models
```

### Output Formats

**Markdown (default):**
```bash
code2prompt . --output-format markdown
```

**JSON:**
```bash
code2prompt . --output-format json
```

**XML:**
```bash
code2prompt . --output-format xml
```

### File Organization

**Sort Files:**
```bash
code2prompt . --sort name_asc    # Alphabetical ascending
code2prompt . --sort name_desc   # Alphabetical descending
code2prompt . --sort date_asc    # Date ascending
code2prompt . --sort date_desc   # Date descending
```

**Include Hidden Files:**
```bash
code2prompt . --hidden
```

**Follow Symlinks:**
```bash
code2prompt . --follow-symlinks
```

## Examples

### Example 1: Basic Code Analysis
```bash
# Analyze a JavaScript project
code2prompt ./my-js-project \
  --include "*.js,*.jsx,*.ts,*.tsx" \
  --exclude "node_modules/,dist/,build/" \
  --output-file analysis.md \
  --tokens format
```

### Example 2: Security Audit
```bash
# Security analysis with custom template
code2prompt ./web-app \
  --template find-security-vulnerabilities.hbs \
  --include "*.js,*.py,*.php" \
  --exclude "vendor/,node_modules/" \
  --output-file security-audit.md
```

### Example 3: Documentation Generation
```bash
# Generate documentation for API
code2prompt ./api-project \
  --template document-the-code.hbs \
  --include "src/**/*.js" \
  --exclude "tests/,examples/" \
  --line-numbers \
  --output-file api-docs.md
```

### Example 4: Performance Optimization
```bash
# Performance analysis
code2prompt ./performance-critical-app \
  --template improve-performance.hbs \
  --include "*.js,*.py" \
  --exclude "tests/,docs/" \
  --tokens format \
  --output-file performance-analysis.md
```

### Example 5: Git-Based Analysis
```bash
# Analyze changes in feature branch
code2prompt ./project \
  --template write-github-pull-request.hbs \
  --git-diff-branch main feature-branch \
  --include "*.js,*.css" \
  --output-file pr-description.md
```

## Best Practices

### 1. File Filtering
- Always exclude build artifacts and dependencies
- Use specific include patterns to focus on relevant files
- Consider file size and token limits

```bash
# Good practice
code2prompt . \
  --include "src/**/*.{js,ts,jsx,tsx}" \
  --exclude "node_modules/,dist/,build/,*.min.js,*.bundle.js"
```

### 2. Template Usage
- Start with built-in templates for common tasks
- Create custom templates for project-specific needs
- Use user-defined variables for flexibility

### 3. Token Management
- Monitor token counts to stay within LLM limits
- Use appropriate tokenizers for your target model
- Consider splitting large codebases

### 4. Output Organization
- Use descriptive output filenames
- Choose appropriate output formats
- Include relevant metadata

### 5. Git Integration
- Use git diffs for change-focused analysis
- Compare branches for comprehensive reviews
- Include commit history for context

### 6. Template Design
- Keep templates focused and specific
- Use clear variable names
- Include proper formatting and structure
- Test templates with small codebases first

## Troubleshooting

### Common Issues

**1. Missing libclang (Windows)**
```bash
# Install LLVM and set environment variable
winget install LLVM.LLVM
$env:LIBCLANG_PATH = "C:\Program Files\LLVM\bin"
cargo install code2prompt
```

**2. Large Codebases**
- Use specific include/exclude patterns
- Consider splitting into smaller chunks
- Monitor token counts

**3. Template Errors**
- Check Handlebars syntax
- Verify variable names
- Test with simple templates first

**4. Git Integration Issues**
- Ensure repository is initialized
- Check branch names
- Verify git permissions

## Resources

- [Official Documentation](https://code2prompt.dev)
- [GitHub Repository](https://github.com/mufeedvh/code2prompt)
- [Handlebars Documentation](https://handlebarsjs.com/)
- [Discord Community](https://discord.gg/code2prompt)

---

*This guide covers the essential features of Code2Prompt CLI. For advanced usage and specific use cases, refer to the official documentation and community resources.*
