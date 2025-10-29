# Create New Astro Blog Post

This command guides you through creating a new blog post for an Astro site with proper frontmatter, content structure, and collection compliance.

## Instructions

Follow these steps to create a new blog post:

### 1. Gather Information

Ask the user for the following details (if not already provided):
- Post title
- Post description (for SEO)
- Author name
- Tags (comma-separated or array)
- Whether to create a draft or published post
- Target collection (default: 'blog')

### 2. Check Collection Schema

Before creating the post:

1. Look for the content collection configuration:
   - Check `src/content/config.ts`
   - Or check `src/content.config.ts`

2. Review the schema for the target collection (usually 'blog')

3. Note all required and optional fields

4. Identify the data types for each field

### 3. Generate Slug

Create a URL-friendly slug from the title:
- Convert to lowercase
- Replace spaces with hyphens
- Remove special characters
- Example: "My First Post!" → "my-first-post"

### 4. Determine File Location

Based on the project structure:
- Collection-based: `src/content/blog/[slug].md`
- Page-based: `src/pages/blog/[slug].md`

Check existing posts to determine the correct location.

### 5. Create Frontmatter

Build frontmatter matching the schema. Common fields:

```yaml
---
title: 'Post Title Here'
description: 'SEO-friendly description'
pubDate: 2024-01-15
author: 'Author Name'
tags: ['astro', 'blogging', 'tutorial']
draft: false
image:
  url: './images/cover.jpg'
  alt: 'Image description'
---
```

Adapt based on the actual schema found in step 2.

### 6. Create Starter Content

Add initial markdown content:

```markdown
# Introduction

Start writing your post here...

## Main Section

Content goes here.

## Conclusion

Wrap up your thoughts.
```

### 7. Handle Images (Optional)

If the user wants to include images:

1. Create an `images/` directory next to the post (if it doesn't exist)
2. Note the image paths in frontmatter
3. Provide guidance on image placement

### 8. Write the File

Create the file with:
- Complete frontmatter
- Starter content structure
- Proper formatting

### 9. Validate

After creating the file:

1. Check that all required schema fields are present
2. Verify the file path is correct
3. Ensure frontmatter is valid YAML
4. Confirm dates are in correct format

### 10. Next Steps

Inform the user:
- File location
- How to add images (if applicable)
- How to preview: `npm run dev`
- How to build: `npm run build`

## Example Output

**For a collection-based blog:**

File: `src/content/blog/getting-started-with-astro.md`

```markdown
---
title: 'Getting Started with Astro'
description: 'Learn the basics of building fast websites with Astro'
pubDate: 2024-01-15
author: 'John Doe'
tags: ['astro', 'tutorial', 'getting-started']
draft: false
---

# Introduction

Welcome to this comprehensive guide on getting started with Astro!

## What is Astro?

Astro is a modern web framework...

## Setting Up Your First Project

Let's walk through the setup process...

## Conclusion

You've learned the basics of Astro. Happy building!
```

## Definition of Done

- [ ] User requirements gathered (title, description, etc.)
- [ ] Collection schema reviewed and understood
- [ ] Slug generated from title
- [ ] Correct file location determined
- [ ] Frontmatter created matching schema
- [ ] All required fields included
- [ ] Dates in ISO format (YYYY-MM-DD)
- [ ] Starter content added
- [ ] File created successfully
- [ ] Validation passed (schema compliance)
- [ ] User informed of next steps

## Important Notes

- Always check the existing collection schema before creating frontmatter
- Use ISO date format: `2024-01-15` or `2024-01-15T10:00:00Z`
- Ensure tags are arrays: `['tag1', 'tag2']` not `'tag1, tag2'`
- Use proper YAML syntax (quoted strings, correct indentation)
- Don't include `layout` field for content collection posts
- Do include `layout` field for page-based posts

## Error Prevention

- Verify collection name exists in config
- Check all required fields are present
- Validate date format
- Ensure proper YAML syntax
- Don't mix collection and page patterns
- Test with `npm run dev` after creation
