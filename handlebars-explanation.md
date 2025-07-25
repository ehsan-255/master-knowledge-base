# Handlebars Templating Engine - Simple Explanation

## What is Handlebars?

**Handlebars** is like a **smart text processor** that takes a template (a blueprint) and fills in the blanks with real data. Think of it like a **mail merge** system, but much more powerful.

### Simple Analogy
Imagine you're writing a letter to multiple people:

**Template (Blueprint):**
```
Dear {{name}},

Thank you for your order of {{item}} on {{date}}.
Your total was ${{amount}}.

Best regards,
{{company_name}}
```

**Data:**
```json
{
  "name": "John Smith",
  "item": "laptop",
  "date": "July 25, 2025",
  "amount": "1,299.99",
  "company_name": "TechStore"
}
```

**Result:**
```
Dear John Smith,

Thank you for your order of laptop on July 25, 2025.
Your total was $1,299.99.

Best regards,
TechStore
```

## How Handlebars Works

### 1. **Template Creation**
You write a template with **placeholders** (variables) in double curly braces `{{variable_name}}`

### 2. **Data Preparation**
You prepare your data (usually in JSON format)

### 3. **Processing**
Handlebars takes your template and data, then **replaces** all placeholders with actual values

### 4. **Output**
You get the final document with all placeholders filled in

## Basic Handlebars Syntax

### **Simple Variables**
```handlebars
Hello {{name}}! You are {{age}} years old.
```

### **Object Properties**
```handlebars
{{user.name}} lives in {{user.city}}
```

### **Conditional Logic (if/else)**
```handlebars
{{#if user.isLoggedIn}}
  Welcome back, {{user.name}}!
{{else}}
  Please log in.
{{/if}}
```

### **Loops (each)**
```handlebars
{{#each products}}
  - {{name}}: ${{price}}
{{/each}}
```

### **Comments**
```handlebars
{{!-- This is a comment that won't appear in output --}}
```

## Handlebars in Code2Prompt

In code2prompt, Handlebars is used to create **dynamic prompts** for AI models:

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

Please analyze this codebase and provide documentation.
```

**What happens:**
1. `{{ absolute_code_path }}` gets replaced with the actual project path
2. `{{ source_tree }}` gets replaced with the directory structure
3. `{{#each files}}` loops through each file
4. `{{path}}` and `{{code}}` get replaced with actual file paths and content

## Other Use Cases for Handlebars

### 1. **Web Development**

#### **Email Templates**
```handlebars
Subject: Order Confirmation for {{orderNumber}}

Dear {{customerName}},

Your order has been confirmed:
{{#each items}}
- {{name}}: ${{price}}
{{/each}}

Total: ${{total}}
```

#### **HTML Generation**
```handlebars
<!DOCTYPE html>
<html>
<head>
    <title>{{pageTitle}}</title>
</head>
<body>
    <h1>{{pageTitle}}</h1>
    {{#each posts}}
    <article>
        <h2>{{title}}</h2>
        <p>{{content}}</p>
        <small>By {{author}} on {{date}}</small>
    </article>
    {{/each}}
</body>
</html>
```

### 2. **Documentation Generation**

#### **API Documentation**
```handlebars
# {{apiName}} API Documentation

## Endpoints

{{#each endpoints}}
### {{method}} {{path}}

**Description:** {{description}}

**Parameters:**
{{#each parameters}}
- `{{name}}` ({{type}}): {{description}}
{{/each}}

**Response:**
```json
{{responseExample}}
```
{{/each}}
```

### 3. **Report Generation**

#### **Sales Reports**
```handlebars
# Sales Report - {{month}} {{year}}

## Summary
- Total Sales: ${{totalSales}}
- Number of Orders: {{orderCount}}
- Average Order Value: ${{averageOrder}}

## Top Products
{{#each topProducts}}
{{rank}}. {{name}} - {{quantity}} units - ${{revenue}}
{{/each}}
```

### 4. **Configuration Files**

#### **Docker Compose**
```handlebars
version: '3.8'
services:
  {{serviceName}}:
    image: {{imageName}}:{{tag}}
    ports:
      - "{{port}}:{{containerPort}}"
    environment:
      - DB_HOST={{dbHost}}
      - DB_NAME={{dbName}}
      - API_KEY={{apiKey}}
```

### 5. **Code Generation**

#### **React Component**
```handlebars
import React from 'react';

const {{componentName}} = ({ {{#each props}}{{name}}{{#unless @last}}, {{/unless}}{{/each}}) => {
  return (
    <div className="{{className}}">
      {{#each children}}
      <{{elementType}}>{{content}}</{{elementType}}>
      {{/each}}
    </div>
  );
};

export default {{componentName}};
```

## Popular Tools That Use Handlebars

### 1. **Static Site Generators**
- **Jekyll** (Ruby) - Blog and documentation sites
- **Hugo** (Go) - Fast static site generation
- **Gatsby** (React) - Modern web development

### 2. **Email Services**
- **SendGrid** - Transactional emails
- **Mailchimp** - Marketing emails
- **Nodemailer** - Node.js email sending

### 3. **Documentation Tools**
- **Swagger** - API documentation
- **JSDoc** - JavaScript documentation
- **Sphinx** - Python documentation

### 4. **Build Tools**
- **Webpack** - Asset bundling
- **Gulp** - Task automation
- **Yeoman** - Project scaffolding

## Handlebars vs Other Templating Engines

| Feature | Handlebars | EJS | Pug | Mustache |
|---------|------------|-----|-----|----------|
| **Syntax** | `{{variable}}` | `<%= variable %>` | `#{variable}` | `{{variable}}` |
| **Logic** | Limited | Full JavaScript | Limited | Minimal |
| **Learning Curve** | Easy | Medium | Medium | Very Easy |
| **Performance** | Fast | Fast | Fast | Very Fast |
| **Popularity** | Very High | High | Medium | High |

## Why Handlebars is Popular

### **1. Simple Syntax**
- Easy to learn and read
- Minimal learning curve
- Clear separation of logic and presentation

### **2. Logic-Less Philosophy**
- Keeps templates simple
- Prevents complex logic in templates
- Encourages clean separation of concerns

### **3. Extensible**
- Custom helpers for complex logic
- Partials for reusable components
- Built-in helpers for common operations

### **4. Cross-Platform**
- Works in browsers and Node.js
- Available in multiple programming languages
- Consistent syntax across platforms

## Getting Started with Handlebars

### **1. Install (Node.js)**
```bash
npm install handlebars
```

### **2. Basic Usage**
```javascript
const Handlebars = require('handlebars');

// Template
const template = Handlebars.compile('Hello {{name}}!');

// Data
const data = { name: 'World' };

// Result
const result = template(data);
console.log(result); // "Hello World!"
```

### **3. With Loops**
```javascript
const template = Handlebars.compile(`
{{#each items}}
- {{name}}: ${{price}}
{{/each}}
`);

const data = {
  items: [
    { name: 'Apple', price: 1.00 },
    { name: 'Banana', price: 0.50 }
  ]
};

console.log(template(data));
// Output:
// - Apple: $1.00
// - Banana: $0.50
```

## Best Practices

### **1. Keep Templates Simple**
```handlebars
<!-- Good -->
{{#each users}}
  <div>{{name}}</div>
{{/each}}

<!-- Avoid complex logic in templates -->
{{#if (and user.isAdmin (eq user.role 'super'))}}
```

### **2. Use Helpers for Complex Logic**
```javascript
Handlebars.registerHelper('formatCurrency', function(amount) {
  return '$' + amount.toFixed(2);
});
```

### **3. Organize with Partials**
```handlebars
{{> header}}
{{> content}}
{{> footer}}
```

### **4. Validate Your Data**
```javascript
// Always validate data before templating
if (!data || !data.users) {
  throw new Error('Invalid data structure');
}
```

## Common Use Cases Summary

1. **Web Development** - HTML generation, dynamic content
2. **Email Marketing** - Personalized email campaigns
3. **Documentation** - API docs, user guides, reports
4. **Code Generation** - Scaffolding, boilerplate code
5. **Configuration** - Environment-specific configs
6. **Reports** - Business reports, analytics
7. **Content Management** - Dynamic website content
8. **Notifications** - System alerts, user messages

---

**In essence, Handlebars is a powerful tool for creating dynamic content by combining templates with data. It's simple to learn, widely supported, and perfect for scenarios where you need to generate consistent, personalized content from structured data.**
