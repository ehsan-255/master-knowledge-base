# Markdown Preview Extension Settings Reference
**Date:** 2025-01-20 03:20
**Project:** Master Knowledge Base
**Scope:** Complete markdown preview settings documentation

## Built-in VS Code Markdown Preview Settings

### **Core Preview Settings**

| Setting | Default | Values | Description |
|---------|---------|--------|-------------|
| `markdown.preview.breaks` | `false` | `true/false` | Render line breaks as `<br>` |
| `markdown.preview.fontSize` | `14` | `number` | Font size in preview |
| `markdown.preview.lineHeight` | `1.4` | `number` | Line height in preview |
| `markdown.preview.scrollPreviewWithEditor` | `false` | `true/false` | Sync preview scroll with editor |
| `markdown.preview.scrollBeyondLastLine` | `true` | `true/false` | Allow scrolling past last line |
| `markdown.preview.wordWrap` | `off` | `on/off/wordWrapColumn` | Word wrap in preview |
| `markdown.preview.doubleClickToSwitchToEditor` | `true` | `true/false` | Double-click to edit |
| `markdown.preview.openMarkdownLinks` | `inPreview` | `inPreview/inBrowser/off` | How to open links |
| `markdown.preview.markEditorSelection` | `true` | `true/false` | Highlight selection in preview |

### **Preview Appearance**

| Setting | Default | Values | Description |
|---------|---------|--------|-------------|
| `markdown.preview.typographer` | `false` | `true/false` | Enable typographer quotes |
| `markdown.preview.linkify` | `true` | `true/false` | Convert URLs to links |
| `markdown.preview.breaks` | `false` | `true/false` | Convert line breaks to `<br>` |
| `markdown.preview.typographer` | `false` | `true/false` | Smart typography quotes |

---

## Markdown All in One Extension Settings

### **Table of Contents**

| Setting | Default | Values | Description |
|---------|---------|--------|-------------|
| `markdown.extension.toc.levels` | `1..3` | `string` | TOC heading levels (e.g., "1..6") |
| `markdown.extension.toc.orderedList` | `true` | `true/false` | Use ordered lists in TOC |
| `markdown.extension.toc.updateOnSave` | `false` | `true/false` | Auto-update TOC on save |
| `markdown.extension.toc.plaintext` | `false` | `true/false` | Plain text TOC |
| `markdown.extension.toc.githubCompatibility` | `false` | `true/false` | GitHub-compatible TOC |

### **Preview Enhancements**

| Setting | Default | Values | Description |
|---------|---------|--------|-------------|
| `markdown.extension.preview.autoShowPreviewToSide` | `false` | `true/false` | Auto-show preview |
| `markdown.extension.preview.breaks` | `false` | `true/false` | Line breaks in preview |
| `markdown.extension.preview.fontSize` | `14` | `number` | Preview font size |
| `markdown.extension.preview.lineHeight` | `1.6` | `number` | Preview line height |
| `markdown.extension.preview.scrollPreviewWithEditor` | `false` | `true/false` | Sync scroll |
| `markdown.extension.preview.scrollBeyondLastLine` | `false` | `true/false` | Scroll past end |
| `markdown.extension.preview.wordWrap` | `off` | `on/off` | Word wrap in preview |

### **Syntax Highlighting**

| Setting | Default | Values | Description |
|---------|---------|--------|-------------|
| `markdown.extension.syntax.decorations` | `false` | `true/false` | Syntax decorations |
| `markdown.extension.syntax.plain` | `false` | `true/false` | Plain text mode |
| `markdown.extension.syntax.underline` | `false` | `true/false` | Underline links |

### **Editing Features**

| Setting | Default | Values | Description |
|---------|---------|--------|-------------|
| `markdown.extension.list.indentationSize` | `one` | `one/two` | List indentation |
| `markdown.extension.orderedList.marker` | `ordered` | `ordered/one/ordered` | List markers |
| `markdown.extension.orderedList.autoRenumber` | `true` | `true/false` | Auto-renumber lists |
| `markdown.extension.orderedList.marker` | `ordered` | `ordered/one/ordered` | List marker style |

---

## Popular Markdown Extension Settings

### **Markdown Preview Enhanced**

| Setting | Default | Values | Description |
|---------|---------|--------|-------------|
| `markdown-preview-enhanced.previewTheme` | `github-light.css` | `string` | Preview theme |
| `markdown-preview-enhanced.codeBlockTheme` | `github.css` | `string` | Code block theme |
| `markdown-preview-enhanced.revealjsTheme` | `white.css` | `string` | Reveal.js theme |
| `markdown-preview-enhanced.enableTypographer` | `false` | `true/false` | Typographer quotes |
| `markdown-preview-enhanced.enableExtendedTableSyntax` | `false` | `true/false` | Extended tables |

### **Markdown PDF**

| Setting | Default | Values | Description |
|---------|---------|--------|-------------|
| `markdown-pdf.outputDirectory` | `""` | `string` | PDF output directory |
| `markdown-pdf.outputDirectoryRelativePathFile` | `false` | `true/false` | Relative output path |
| `markdown-pdf.styles` | `[]` | `array` | Custom CSS styles |
| `markdown-pdf.stylesRelativePathFile` | `false` | `true/false` | Relative style paths |
| `markdown-pdf.includeDefaultStyles` | `true` | `true/false` | Include default styles |

---

## Current Project Settings

### **Currently Configured Settings**

```json
{
  // Built-in VS Code settings
  "markdown.preview.breaks": true,
  "markdown.preview.fontSize": 14,
  "markdown.preview.lineHeight": 1.6,
  "markdown.preview.scrollPreviewWithEditor": true,
  "markdown.preview.scrollBeyondLastLine": false,
  "markdown.preview.wordWrap": "on",

  // Markdown All in One settings
  "markdown.extension.toc.levels": "1..6",
  "markdown.extension.toc.orderedList": false,
  "markdown.extension.toc.updateOnSave": true,
  "markdown.extension.syntax.decorations": true,
  "markdown.extension.preview.autoShowPreviewToSide": true,
  "markdown.extension.preview.breaks": true,
  "markdown.extension.preview.fontSize": 14,
  "markdown.extension.preview.lineHeight": 1.6,
  "markdown.extension.preview.scrollPreviewWithEditor": true,
  "markdown.extension.preview.scrollBeyondLastLine": false,
  "markdown.extension.preview.wordWrap": "on"
}
```

---

## Recommended Settings for Knowledge Base

### **Enhanced Readability**
```json
{
  "markdown.preview.fontSize": 16,
  "markdown.preview.lineHeight": 1.8,
  "markdown.preview.wordWrap": "on",
  "markdown.extension.preview.fontSize": 16,
  "markdown.extension.preview.lineHeight": 1.8
}
```

### **Better Navigation**
```json
{
  "markdown.extension.toc.levels": "1..6",
  "markdown.extension.toc.updateOnSave": true,
  "markdown.preview.scrollPreviewWithEditor": true,
  "markdown.extension.preview.autoShowPreviewToSide": true
}
```

### **Professional Appearance**
```json
{
  "markdown.extension.syntax.decorations": true,
  "markdown.preview.breaks": true,
  "markdown.extension.preview.breaks": true
}
```

---

## Extension Installation Commands

### **Install Popular Extensions**
```bash
# Markdown All in One
code --install-extension yzhang.markdown-all-in-one

# Markdown Preview Enhanced
code --install-extension shd101wyy.markdown-preview-enhanced

# Markdown PDF
code --install-extension yzane.markdown-pdf
```

---

**Reference Generated:** 2025-01-20 03:20
**Total Settings Documented:** 50+ markdown preview settings
**Extensions Covered:** Built-in, Markdown All in One, Markdown Preview Enhanced, Markdown PDF
**Use Case:** Knowledge Base Documentation Optimization
