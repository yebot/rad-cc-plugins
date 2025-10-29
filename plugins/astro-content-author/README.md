# Astro Content Author Plugin

Comprehensive toolkit for creating and managing content in Astro projects, including markdown files, content collections, images, data fetching, and Astro DB integration.

## Overview

This plugin provides specialized agents, commands, and skills to help you work efficiently with Astro's content system. Whether you're building a blog, documentation site, e-commerce platform, or portfolio, these tools will streamline your content workflow.

## Components

### Agents

#### content-creator
Expert at creating markdown and MDX content with proper frontmatter, layouts, and structure.

**Use when:**
- Creating blog posts
- Writing documentation pages
- Adding any markdown-based content
- Working with MDX components

**Example:**
```
Create a new blog post about Astro's content collections with frontmatter for title, description, date, author, and tags
```

#### collection-architect
Expert at designing and implementing content collections with schemas, loaders, and TypeScript integration.

**Use when:**
- Setting up new content types
- Defining collection schemas
- Organizing content structure
- Implementing type-safe content

**Example:**
```
Create a new product collection with fields for name, price, description, images, and category
```

#### image-optimizer
Expert at integrating and optimizing images using Astro's Image and Picture components.

**Use when:**
- Adding images to content
- Optimizing image performance
- Setting up responsive images
- Configuring image workflows

**Example:**
```
Add an optimized hero image to my blog post with AVIF and WebP formats
```

#### data-fetcher
Expert at implementing data fetching patterns including API calls, GraphQL, headless CMS integration, and Astro DB.

**Use when:**
- Integrating external data sources
- Setting up API endpoints
- Working with databases
- Connecting to headless CMS

**Example:**
```
Set up Astro DB with tables for blog posts, authors, and comments
```

### Commands

#### /astro-content:new-post
Quick workflow for creating a new blog post with proper frontmatter and structure.

**Usage:**
```
/astro-content:new-post
```

The command will:
1. Ask for post details (title, description, author, tags)
2. Check the collection schema
3. Generate a URL-friendly slug
4. Create the file with complete frontmatter
5. Add starter content structure

#### /astro-content:new-collection
Guided workflow for setting up a new content collection with schema definition.

**Usage:**
```
/astro-content:new-collection
```

The command will:
1. Gather collection requirements
2. Design appropriate schema fields
3. Create/update config file
4. Set up directory structure
5. Generate sample content
6. Provide query examples

### Skills

#### frontmatter-schemas
Common Zod schema patterns and frontmatter examples for content collections.

**Includes:**
- Blog post schemas
- Documentation schemas
- Product schemas
- Team member schemas
- Project/portfolio schemas
- Zod validation patterns
- Frontmatter examples

**Usage:**
```
Use the frontmatter-schemas skill to help design a schema for my docs collection
```

#### astro-db-patterns
Common patterns for using Astro DB including schema design, queries, and seeding.

**Includes:**
- Column type examples
- Schema patterns (blog, e-commerce, user management)
- Data seeding patterns
- Query examples (select, filter, join, order, limit)
- Insert/update/delete patterns
- API endpoint patterns
- Production deployment

**Usage:**
```
Use the astro-db-patterns skill to help set up a database for my blog
```

## Installation

### From Marketplace

```bash
/plugin install astro-content-author@rad-cc-plugins
```

### From Source

```bash
/plugin add ./plugins/astro-content-author
```

## Common Workflows

### Creating a Blog Post

1. Use the command:
   ```
   /astro-content:new-post
   ```

2. Or ask directly:
   ```
   Create a blog post about TypeScript best practices
   ```

The content-creator agent will handle it automatically.

### Setting Up a New Collection

1. Use the command:
   ```
   /astro-content:new-collection
   ```

2. Or ask directly:
   ```
   Create a products collection with name, price, description, and images
   ```

The collection-architect agent will handle it automatically.

### Adding Optimized Images

```
Add a hero image to my blog post with responsive sizes and modern formats
```

The image-optimizer agent will configure the Image/Picture component properly.

### Setting Up Astro DB

```
Set up Astro DB with tables for posts, authors, tags, and comments
```

The data-fetcher agent will create the schema, seed file, and provide query examples.

## Best Practices

### Content Organization

- Use content collections for queryable content (blog, docs, products)
- Use pages directory for standalone pages
- Keep images in `src/` for optimization
- Use `public/` only for static assets

### Schema Design

- Always use `z.coerce.date()` for date strings
- Provide defaults for booleans and arrays
- Use enums for fixed value sets
- Validate URLs and emails with built-in validators
- Keep schemas focused and specific

### Images

- Use Picture component for hero images (multiple formats)
- Use Image component for thumbnails
- Always provide descriptive alt text
- Use AVIF + WebP for modern browsers
- Provide JPG fallback for older browsers

### Data Fetching

- Use Astro DB for relational data needs
- Cache external API responses when possible
- Use API endpoints for client-side data needs
- Implement proper error handling
- Test with rate limits in mind

## Examples

### Blog Post Example

```markdown
---
title: 'Getting Started with Astro'
description: 'Learn the fundamentals of building fast websites with Astro'
pubDate: 2024-01-15
author: 'John Doe'
tags: ['astro', 'tutorial', 'web-dev']
draft: false
featured: true
image:
  url: './images/hero.jpg'
  alt: 'Astro logo with stars'
---

# Introduction

Welcome to this comprehensive guide...
```

### Collection Schema Example

```typescript
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/blog" }),
  schema: z.object({
    title: z.string().max(80),
    description: z.string().max(160),
    pubDate: z.coerce.date(),
    author: z.string(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
    featured: z.boolean().default(false)
  })
});

export const collections = { blog };
```

### Astro DB Schema Example

```typescript
import { defineDb, defineTable, column } from 'astro:db';

const Post = defineTable({
  columns: {
    id: column.number({ primaryKey: true }),
    title: column.text(),
    slug: column.text({ unique: true }),
    content: column.text(),
    published: column.boolean({ default: false }),
    publishedAt: column.date({ optional: true }),
    authorId: column.number(),
    views: column.number({ default: 0 })
  }
});

export default defineDb({ tables: { Post } });
```

## Tips

- The agents work proactively - just describe what you need
- Use commands for guided workflows
- Use skills for reference and patterns
- Check existing content for consistency
- Run `npm run dev` to catch validation errors early
- Test schema changes with sample content first

## Documentation

For detailed documentation on Astro's content features:

- [Markdown Content](https://docs.astro.build/en/guides/markdown-content/)
- [Content Collections](https://docs.astro.build/en/guides/content-collections/)
- [Images](https://docs.astro.build/en/guides/images/)
- [Data Fetching](https://docs.astro.build/en/guides/data-fetching/)
- [Astro DB](https://docs.astro.build/en/guides/astro-db/)

## Support

For issues or questions about this plugin:
- Check agent descriptions for guidance
- Review skill documentation for patterns
- Open an issue in the marketplace repository

## Version

1.0.0

## Author

Tobey Forsman (tobeyforsman@gmail.com)
