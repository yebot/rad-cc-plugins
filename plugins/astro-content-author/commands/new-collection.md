# Create New Astro Content Collection

This command guides you through creating a new content collection in an Astro project with proper schema definition, directory structure, and TypeScript integration.

## Instructions

Follow these steps to create a new content collection:

### 1. Gather Requirements

Ask the user for:
- Collection name (e.g., 'blog', 'docs', 'products', 'team')
- Collection purpose (what type of content?)
- Required fields and their types
- Optional fields
- File format preference (markdown, JSON, YAML, etc.)

### 2. Design Schema Fields

Based on the collection purpose, determine appropriate fields:

**For blog/articles:**
- title (string, required)
- description (string, required)
- pubDate (date, required)
- author (string, required)
- tags (array of strings)
- draft (boolean, default false)
- image (object with url and alt)

**For documentation:**
- title (string, required)
- description (string, required)
- sidebar (object with order, label)
- lastUpdated (date, optional)
- contributors (array of strings)

**For products:**
- name (string, required)
- description (string, required)
- price (number, required)
- category (enum)
- features (array of strings)
- inStock (boolean)
- images (array of objects)

**For team members:**
- name (string, required)
- role (string, required)
- bio (string, required)
- avatar (string, required)
- social (object with URLs)
- startDate (date, required)

### 3. Locate or Create Config File

1. Check if config exists:
   - Look for `src/content/config.ts`
   - Or `src/content.config.ts`

2. If it doesn't exist, create `src/content/config.ts`

3. Ensure imports are present:
```typescript
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';
```

### 4. Define Collection Schema

Create the collection definition with appropriate Zod schema:

```typescript
const [collectionName] = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/[collectionName]" }),
  schema: z.object({
    // Define fields based on requirements
  })
});
```

Use appropriate Zod types:
- `z.string()` - Text fields
- `z.number()` - Numeric fields
- `z.boolean()` - True/false fields
- `z.coerce.date()` - Date fields (with auto-conversion)
- `z.array(z.string())` - Arrays
- `z.object({...})` - Nested objects
- `z.enum(['value1', 'value2'])` - Fixed options
- Add `.optional()` for optional fields
- Add `.default(value)` for default values

### 5. Add to Collections Export

Update the export statement:

```typescript
export const collections = {
  // existing collections...
  [collectionName]: [collectionName]
};
```

### 6. Create Collection Directory

Create the directory structure:
```bash
mkdir -p src/content/[collectionName]
```

### 7. Create Sample Content File

Create a sample file to test the schema:

**For markdown:**
`src/content/[collectionName]/sample.md`

**For JSON:**
`src/content/[collectionName]/sample.json`

**For YAML:**
`src/content/[collectionName]/sample.yml`

Include frontmatter/data that matches the schema.

### 8. Validate Schema

1. Start the dev server: `npm run dev`
2. Check for TypeScript errors
3. Verify the sample file validates correctly
4. Check `.astro/types.d.ts` for generated types

### 9. Document Usage

Create a comment block in the config explaining the collection:

```typescript
/**
 * [Collection Name] Collection
 *
 * Purpose: [Description]
 *
 * Required fields:
 * - field1: description
 * - field2: description
 *
 * Optional fields:
 * - field3: description
 */
const [collectionName] = defineCollection({...});
```

### 10. Provide Query Examples

Show the user how to query the new collection:

```typescript
import { getCollection, getEntry } from 'astro:content';

// Get all items
const items = await getCollection('[collectionName]');

// Get published items (if applicable)
const published = await getCollection('[collectionName]', ({ data }) => {
  return !data.draft;
});

// Get single item
const item = await getEntry('[collectionName]', 'slug');
```

## Complete Example

**Collection Config** (`src/content/config.ts`):

```typescript
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/**
 * Blog Posts Collection
 *
 * Stores blog articles and tutorials
 */
const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/blog" }),
  schema: z.object({
    title: z.string().max(80),
    description: z.string().max(160),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    author: z.string(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
    featured: z.boolean().default(false),
    image: z.object({
      url: z.string(),
      alt: z.string()
    }).optional()
  })
});

/**
 * Documentation Collection
 *
 * Technical documentation and guides
 */
const docs = defineCollection({
  loader: glob({ pattern: "**/*.mdx", base: "./src/content/docs" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    sidebar: z.object({
      order: z.number(),
      label: z.string().optional(),
      hidden: z.boolean().default(false)
    }).optional(),
    lastUpdated: z.coerce.date().optional(),
    contributors: z.array(z.string()).default([])
  })
});

export const collections = { blog, docs };
```

**Sample Blog Post** (`src/content/blog/first-post.md`):

```markdown
---
title: 'My First Post'
description: 'This is my first blog post'
pubDate: 2024-01-15
author: 'John Doe'
tags: ['intro', 'blogging']
draft: false
featured: true
---

# Hello World

This is my first post!
```

## Definition of Done

- [ ] Collection requirements gathered from user
- [ ] Schema fields identified and typed
- [ ] Config file located or created
- [ ] Collection definition added with proper schema
- [ ] Loader configured for correct file pattern
- [ ] Zod types match requirements
- [ ] Collection exported in collections object
- [ ] Collection directory created
- [ ] Sample content file created
- [ ] Sample file validates against schema
- [ ] Dev server starts without errors
- [ ] TypeScript types generated correctly
- [ ] Documentation comments added
- [ ] Query examples provided to user

## Schema Best Practices

### String Validation
```typescript
title: z.string().min(1).max(100)
email: z.string().email()
url: z.string().url()
slug: z.string().regex(/^[a-z0-9-]+$/)
```

### Number Validation
```typescript
price: z.number().positive()
age: z.number().int().min(0).max(120)
rating: z.number().min(1).max(5)
```

### Dates
```typescript
pubDate: z.coerce.date()  // Converts strings to Date
deadline: z.date()         // Requires Date object
```

### Arrays
```typescript
tags: z.array(z.string()).min(1)      // At least one
images: z.array(z.string()).max(10)   // Maximum 10
authors: z.array(z.string()).default([])
```

### Enums
```typescript
status: z.enum(['draft', 'published', 'archived'])
priority: z.enum(['low', 'medium', 'high'])
```

### Optional Fields
```typescript
subtitle: z.string().optional()
updatedDate: z.coerce.date().optional()
```

### Default Values
```typescript
draft: z.boolean().default(false)
views: z.number().default(0)
tags: z.array(z.string()).default([])
```

### Nested Objects
```typescript
author: z.object({
  name: z.string(),
  email: z.string().email(),
  url: z.string().url().optional()
})
```

### Records (Dynamic Keys)
```typescript
metadata: z.record(z.string())  // Any string keys
settings: z.record(z.boolean()) // Boolean values
```

## Loader Patterns

### Markdown Files
```typescript
loader: glob({ pattern: "**/*.md", base: "./src/content/blog" })
```

### MDX Files
```typescript
loader: glob({ pattern: "**/*.mdx", base: "./src/content/docs" })
```

### Multiple Formats
```typescript
loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/mixed" })
```

### JSON Files
```typescript
loader: glob({ pattern: "**/*.json", base: "./src/content/data" })
```

### YAML Files
```typescript
loader: glob({ pattern: "**/*.{yml,yaml}", base: "./src/content/config" })
```

### Single File
```typescript
loader: file("src/data/settings.json")
```

## Common Collection Types

### Blog
```typescript
const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/blog" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    author: z.string(),
    tags: z.array(z.string()),
    draft: z.boolean().default(false)
  })
});
```

### Portfolio Projects
```typescript
const projects = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/projects" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    technologies: z.array(z.string()),
    liveUrl: z.string().url().optional(),
    githubUrl: z.string().url().optional(),
    thumbnail: z.string(),
    date: z.coerce.date()
  })
});
```

### Product Catalog
```typescript
const products = defineCollection({
  loader: glob({ pattern: "**/*.json", base: "./src/content/products" }),
  schema: z.object({
    name: z.string(),
    description: z.string(),
    price: z.number().positive(),
    category: z.enum(['software', 'hardware', 'service']),
    features: z.array(z.string()),
    inStock: z.boolean()
  })
});
```

## Error Prevention

- Always use `z.coerce.date()` for date strings
- Provide defaults for booleans and arrays
- Use enums for fixed value sets
- Validate URLs and emails with built-in validators
- Test schema with sample content first
- Restart dev server after schema changes
- Export all collections in the collections object
- Use consistent naming (kebab-case for directories)

## Tips

- Start with required fields, add optional later
- Use TypeScript comments for documentation
- Create sample content immediately
- Test validation with invalid data
- Consider future needs when designing schema
- Use subdirectories for organization
- Keep schemas focused and specific
- Reuse common patterns across collections
