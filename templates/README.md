# Code2Prompt Templates Directory

This directory contains official Handlebars templates for the [Code2Prompt](https://github.com/mufeedvh/code2prompt) CLI tool. These templates help generate structured prompts for various code analysis and documentation tasks.

## 📁 Available Templates

### 1. **document-the-code.hbs**
Generates prompts for comprehensive code documentation with language-specific comment styles.

### 2. **find-security-vulnerabilities.hbs**
Performs comprehensive security analysis to identify potential vulnerabilities.

### 3. **clean-up-code.hbs**
Improves code quality through refactoring and cleanup without changing behavior.

### 4. **fix-bugs.hbs**
Identifies and fixes potential bugs through systematic code analysis.

### 5. **write-github-pull-request.hbs**
Creates professional GitHub pull request descriptions from git changes.

### 6. **write-github-readme.hbs**
Generates comprehensive README files suitable for GitHub projects.

### 7. **write-git-commit.hbs**
Generates conventional git commit messages from code changes.

### 8. **improve-performance.hbs**
Optimizes code performance while maintaining correctness and readability.

### 9. **binary-exploitation-ctf-solver.hbs**
Solves CTF binary exploitation challenges with systematic analysis and exploit development.

### 10. **cryptography-ctf-solver.hbs**
Solves CTF cryptography challenges by analyzing encryption methods and finding weaknesses.

### 11. **reverse-engineering-ctf-solver.hbs**
Solves CTF reverse engineering challenges through binary analysis and debugging.

### 12. **claude-xml.hbs**
Generates XML-formatted output optimized for Claude AI models.

### 13. **refactor.hbs**
Refactors codebase to improve design, maintainability, and performance following SOLID principles.

### 14. **web-ctf-solver.hbs**
Solves CTF web exploitation challenges by testing for common web vulnerabilities and crafting exploits.

### 15. **hma-v2.2-compliance-analyzer.hbs**
Analyzes codebases for compliance with Hexagonal Microkernel Architecture (HMA) v2.2 principles and standards.

## 🚀 Usage

```bash
# Basic usage with a template
code2prompt /path/to/codebase --template templates/document-the-code.hbs

# With output file
code2prompt . --template templates/find-security-vulnerabilities.hbs --output-file security-analysis.md

# With git integration
code2prompt . --template templates/write-github-pull-request.hbs --diff --output-file pr-description.md
```

## 📝 Creating Custom Templates

### Template Structure Overview

Code2Prompt templates use the [Handlebars](https://handlebarsjs.com/) templating engine. Each template should follow this basic structure:

```handlebars
Project Path: {{ absolute_code_path }}

Source Tree:
```
{{ source_tree }}
```

{{#each files}}
{{#if code}}
`{{path}}`:

{{code}}

{{/if}}
{{/each}}

[Your custom prompt content here]
```

### Available Variables

#### Core Variables
- `{{ absolute_code_path }}` - Absolute path to the codebase
- `{{ source_tree }}` - Directory tree structure
- `{{ files }}` - Array of file objects

#### File Object Properties
- `{{ path }}` - File path relative to codebase root
- `{{ code }}` - File content (only available if file is readable)
- `{{ size }}` - File size in bytes
- `{{ modified }}` - Last modified timestamp

#### Git Integration Variables
- `{{ git_diff }}` - Git diff content (when using `--diff`)
- `{{ git_diff_branch }}` - Git diff between branches (when using `--git-diff-branch`)
- `{{ git_log_branch }}` - Git log between branches (when using `--git-log-branch`)

### Template Best Practices

#### 1. **Clear Purpose Definition**
Start your template with a clear statement of what you want to achieve:

```handlebars
Project Path: {{ absolute_code_path }}

I want you to [specific task description]. Please analyze the following codebase:

Source Tree:
```
{{ source_tree }}
```

{{#each files}}
{{#if code}}
`{{path}}`:

{{code}}

{{/if}}
{{/each}}

[Detailed instructions for the LLM]
```

#### 2. **Structured Instructions**
Break down complex tasks into clear, numbered steps:

```handlebars
Please perform the following analysis:

1. **Step One**: [Specific instruction]
2. **Step Two**: [Specific instruction]
3. **Step Three**: [Specific instruction]

For each finding, provide:
- File path and line number
- Description of the issue
- Suggested solution
- Impact assessment
```

#### 3. **Conditional Logic**
Use Handlebars conditionals to handle different scenarios:

```handlebars
{{#if git_diff}}
Git Changes:
```
{{git_diff}}
```
{{else}}
No git changes detected.
{{/if}}

{{#each files}}
{{#if code}}
File: {{path}}
Content: {{code}}
{{else}}
File: {{path}} (binary or unreadable)
{{/if}}
{{/each}}
```

#### 4. **Output Formatting**
Specify the desired output format clearly:

```handlebars
Please provide your analysis in the following format:

## Summary
[Brief overview]

## Detailed Findings
### Finding 1
- **File**: [file path]
- **Issue**: [description]
- **Solution**: [recommendation]

## Recommendations
[Prioritized list of actions]
```

### Template Categories

#### **Analysis Templates**
For code analysis, review, and assessment:

```handlebars
Project Path: {{ absolute_code_path }}

I need you to analyze this codebase for [specific analysis type].

Source Tree:
```
{{ source_tree }}
```

{{#each files}}
{{#if code}}
`{{path}}`:

{{code}}

{{/if}}
{{/each}}

Please provide:
1. Comprehensive analysis of [specific aspect]
2. Identification of [specific issues/patterns]
3. Recommendations for [improvements/fixes]
4. Priority ranking of findings
```

#### **Generation Templates**
For creating new content based on existing code:

```handlebars
Project Path: {{ absolute_code_path }}

I want you to generate [specific output type] based on this codebase.

Source Tree:
```
{{ source_tree }}
```

{{#each files}}
{{#if code}}
`{{path}}`:

{{code}}

{{/if}}
{{/each}}

Please create:
1. [Specific output requirement 1]
2. [Specific output requirement 2]
3. [Specific output requirement 3]

Format the output as [markdown/JSON/XML/etc.]
```

#### **Transformation Templates**
For code refactoring and modification:

```handlebars
Project Path: {{ absolute_code_path }}

I need you to transform this codebase by [specific transformation].

Source Tree:
```
{{ source_tree }}
```

{{#each files}}
{{#if code}}
`{{path}}`:

{{code}}

{{/if}}
{{/each}}

Please:
1. Identify opportunities for [transformation type]
2. Provide specific code changes
3. Maintain existing functionality
4. Follow [language] best practices
5. Add explanatory comments for changes
```

### Advanced Template Techniques

#### **User-Defined Variables**
Create templates that prompt for additional input:

```handlebars
Project Path: {{ absolute_code_path }}

Analysis for: {{ project_name }}
Focus Area: {{ focus_area }}
Priority Level: {{ priority_level }}

Source Tree:
```
{{ source_tree }}
```

{{#each files}}
{{#if code}}
`{{path}}`:

{{code}}

{{/if}}
{{/each}}

Please analyze this codebase with focus on {{ focus_area }}.
Priority should be given to {{ priority_level }} issues.
```

When using this template, code2prompt will prompt you to enter values for `project_name`, `focus_area`, and `priority_level`.

#### **Conditional Content**
Use conditionals to provide different instructions based on context:

```handlebars
{{#if git_diff}}
This analysis includes recent changes:
```
{{git_diff}}
```
{{/if}}

{{#each files}}
{{#if code}}
`{{path}}`:
{{code}}
{{else}}
`{{path}}` (binary file - skipping analysis)
{{/if}}
{{/each}}
```

#### **Iterative Processing**
Process files with specific criteria:

```handlebars
{{#each files}}
{{#if code}}
{{#if (contains path ".js")}}
JavaScript file: {{path}}
{{code}}
{{/if}}
{{/if}}
{{/each}}
```

### Template Testing

#### **1. Dry Run Testing**
Test your template with a small codebase first:

```bash
# Test with a small directory
code2prompt ./test-project --template my-new-template.hbs --output-file test-output.md
```

#### **2. Template Validation**
Ensure your Handlebars syntax is correct:

```bash
# Check for syntax errors
handlebars my-template.hbs --validate
```

#### **3. Token Count Monitoring**
Monitor token usage to stay within LLM limits:

```bash
code2prompt . --template my-template.hbs --tokens format
```

### Template Examples

#### **Code Review Template**
```handlebars
Project Path: {{ absolute_code_path }}

I need a comprehensive code review of this project.

Source Tree:
```
{{ source_tree }}
```

{{#each files}}
{{#if code}}
`{{path}}`:

{{code}}

{{/if}}
{{/each}}

Please provide a detailed code review covering:

1. **Code Quality**
   - Readability and maintainability
   - Adherence to best practices
   - Code organization and structure

2. **Potential Issues**
   - Bugs and edge cases
   - Performance concerns
   - Security vulnerabilities

3. **Improvements**
   - Refactoring opportunities
   - Optimization suggestions
   - Documentation needs

4. **Overall Assessment**
   - Strengths of the codebase
   - Areas for improvement
   - Priority recommendations
```

#### **API Documentation Template**
```handlebars
Project Path: {{ absolute_code_path }}

I need you to generate comprehensive API documentation for this project.

Source Tree:
```
{{ source_tree }}
```

{{#each files}}
{{#if code}}
`{{path}}`:

{{code}}

{{/if}}
{{/each}}

Please create API documentation including:

1. **Endpoint Overview**
   - List all API endpoints
   - HTTP methods supported
   - Base URL information

2. **Detailed Endpoint Documentation**
   - Request parameters
   - Response formats
   - Status codes
   - Example requests/responses

3. **Authentication**
   - Authentication methods
   - Required headers
   - Token management

4. **Error Handling**
   - Common error codes
   - Error response formats
   - Troubleshooting guide

Format the output in Markdown with proper code examples.
```

### Template Maintenance

#### **Version Control**
- Keep templates in version control
- Use semantic versioning for template updates
- Document changes in template comments

#### **Documentation**
- Include usage examples in template comments
- Document any special requirements or dependencies
- Provide clear descriptions of expected outputs

#### **Regular Updates**
- Review and update templates periodically
- Test with different codebases and languages
- Gather feedback from users

## 🔧 Troubleshooting

### Common Issues

#### **Template Not Found**
```bash
# Ensure correct path
code2prompt . --template ./templates/my-template.hbs

# Check file exists
ls templates/my-template.hbs
```

#### **Handlebars Syntax Errors**
- Validate syntax with online Handlebars validators
- Check for missing closing tags
- Ensure proper variable names

#### **Large Output Issues**
- Use `--tokens format` to monitor token count
- Consider splitting large codebases
- Use more specific include/exclude patterns

### Getting Help

- [Code2Prompt Documentation](https://code2prompt.dev)
- [Handlebars Documentation](https://handlebarsjs.com/)
- [GitHub Repository](https://github.com/mufeedvh/code2prompt)
- [Discord Community](https://discord.gg/code2prompt)

## 📄 License

These templates are part of the Code2Prompt project and are licensed under the MIT License.

---

*This README provides comprehensive guidance for using and creating Code2Prompt templates. For advanced usage and specific use cases, refer to the official documentation.*
