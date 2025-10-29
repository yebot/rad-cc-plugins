# Astro Frontmatter Schemas Skill

Common Zod schema patterns and frontmatter examples for Astro content collections.

## When to Use This Skill

- Designing content collection schemas
- Creating frontmatter for markdown files
- Validating content structure
- Setting up type-safe content

## Common Schema Patterns

### Blog Post Schema

```typescript
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/blog" }),
  schema: z.object({
    // Core Fields
    title: z.string().max(80),
    description: z.string().max(160),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),

    // Author
    author: z.string(),
    authorUrl: z.string().url().optional(),

    // Categorization
    tags: z.array(z.string()).default([]),
    category: z.enum(['tutorial', 'news', 'guide', 'review']).optional(),

    // Publishing
    draft: z.boolean().default(false),
    featured: z.boolean().default(false),

    // Media
    image: z.object({
      url: z.string(),
      alt: z.string()
    }).optional(),

    // SEO
    canonicalURL: z.string().url().optional(),

    // Metadata
    readingTime: z.number().optional(),
    relatedPosts: z.array(z.string()).default([])
  })
});
```

**Corresponding Frontmatter:**

```yaml
---
title: 'Getting Started with Astro'
description: 'Learn the fundamentals of building fast websites with Astro'
pubDate: 2024-01-15
updatedDate: 2024-01-20
author: 'John Doe'
authorUrl: 'https://example.com/john'
tags: ['astro', 'tutorial', 'web-dev']
category: 'tutorial'
draft: false
featured: true
image:
  url: './images/hero.jpg'
  alt: 'Astro logo with stars'
canonicalURL: 'https://example.com/blog/getting-started'
readingTime: 8
relatedPosts: ['advanced-astro', 'astro-tips']
---
```

### Documentation Schema

```typescript
const docs = defineCollection({
  loader: glob({ pattern: "**/*.mdx", base: "./src/content/docs" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),

    // Sidebar
    sidebar: z.object({
      order: z.number(),
      label: z.string().optional(),
      hidden: z.boolean().default(false),
      badge: z.string().optional()
    }).optional(),

    // Status
    lastUpdated: z.coerce.date().optional(),
    version: z.string().optional(),
    deprecated: z.boolean().default(false),

    // Contributors
    contributors: z.array(z.string()).default([]),

    // Navigation
    prev: z.object({
      text: z.string(),
      link: z.string()
    }).optional(),
    next: z.object({
      text: z.string(),
      link: z.string()
    }).optional(),

    // Table of Contents
    tableOfContents: z.boolean().default(true),
    tocDepth: z.number().min(1).max(6).default(3)
  })
});
```

**Corresponding Frontmatter:**

```yaml
---
title: 'API Reference'
description: 'Complete API documentation for the core library'
sidebar:
  order: 2
  label: 'API Docs'
  hidden: false
  badge: 'New'
lastUpdated: 2024-01-20
version: '2.1.0'
deprecated: false
contributors: ['john-doe', 'jane-smith']
prev:
  text: 'Installation'
  link: '/docs/installation'
next:
  text: 'Configuration'
  link: '/docs/configuration'
tableOfContents: true
tocDepth: 3
---
```

### Product Schema

```typescript
const products = defineCollection({
  loader: glob({ pattern: "**/*.json", base: "./src/content/products" }),
  schema: z.object({
    // Basic Info
    name: z.string(),
    description: z.string(),
    shortDescription: z.string().max(100).optional(),

    // Pricing
    price: z.number().positive(),
    currency: z.string().default('USD'),
    salePrice: z.number().positive().optional(),

    // Categorization
    category: z.enum(['software', 'hardware', 'service', 'digital']),
    tags: z.array(z.string()).default([]),

    // Inventory
    sku: z.string(),
    inStock: z.boolean().default(true),
    quantity: z.number().int().min(0).optional(),

    // Features
    features: z.array(z.string()),
    specifications: z.record(z.string()).optional(),

    // Media
    images: z.array(z.object({
      url: z.string(),
      alt: z.string(),
      primary: z.boolean().default(false)
    })),

    // Rating
    rating: z.number().min(0).max(5).optional(),
    reviewCount: z.number().int().min(0).default(0)
  })
});
```

**Corresponding JSON:**

```json
{
  "name": "Premium Web Hosting",
  "description": "Fast, reliable web hosting with 99.9% uptime",
  "shortDescription": "Premium hosting solution",
  "price": 29.99,
  "currency": "USD",
  "salePrice": 19.99,
  "category": "service",
  "tags": ["hosting", "cloud", "premium"],
  "sku": "HOST-001",
  "inStock": true,
  "quantity": 100,
  "features": [
    "99.9% uptime guarantee",
    "Free SSL certificate",
    "24/7 support"
  ],
  "specifications": {
    "storage": "100GB SSD",
    "bandwidth": "Unlimited",
    "domains": "1"
  },
  "images": [
    {
      "url": "/images/hosting-main.jpg",
      "alt": "Server rack",
      "primary": true
    }
  ],
  "rating": 4.5,
  "reviewCount": 127
}
```

### Team Member Schema

```typescript
const team = defineCollection({
  loader: glob({ pattern: "**/*.yml", base: "./src/content/team" }),
  schema: z.object({
    name: z.string(),
    role: z.string(),
    department: z.enum(['engineering', 'design', 'marketing', 'sales']).optional(),

    bio: z.string(),

    avatar: z.string(),

    social: z.object({
      twitter: z.string().url().optional(),
      github: z.string().url().optional(),
      linkedin: z.string().url().optional(),
      website: z.string().url().optional()
    }).optional(),

    startDate: z.coerce.date(),
    location: z.string().optional(),

    skills: z.array(z.string()).default([]),
    featured: z.boolean().default(false)
  })
});
```

**Corresponding YAML:**

```yaml
name: 'Jane Smith'
role: 'Senior Software Engineer'
department: 'engineering'
bio: 'Full-stack developer with 10 years experience building scalable web applications.'
avatar: '/images/team/jane.jpg'
social:
  twitter: 'https://twitter.com/janesmith'
  github: 'https://github.com/janesmith'
  linkedin: 'https://linkedin.com/in/janesmith'
  website: 'https://janesmith.dev'
startDate: 2020-03-15
location: 'San Francisco, CA'
skills: ['TypeScript', 'React', 'Node.js', 'AWS']
featured: true
```

### Project/Portfolio Schema

```typescript
const projects = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/projects" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),

    technologies: z.array(z.string()),

    liveUrl: z.string().url().optional(),
    githubUrl: z.string().url().optional(),
    demoUrl: z.string().url().optional(),

    thumbnail: z.string(),
    images: z.array(z.string()).default([]),

    date: z.coerce.date(),
    endDate: z.coerce.date().optional(),

    status: z.enum(['active', 'completed', 'archived']).default('active'),
    featured: z.boolean().default(false),

    client: z.string().optional(),
    team: z.array(z.string()).default([]),

    tags: z.array(z.string()).default([])
  })
});
```

**Corresponding Frontmatter:**

```yaml
---
title: 'E-commerce Platform Redesign'
description: 'Complete redesign and modernization of legacy e-commerce platform'
technologies: ['React', 'Next.js', 'TypeScript', 'Tailwind CSS', 'PostgreSQL']
liveUrl: 'https://shop.example.com'
githubUrl: 'https://github.com/example/shop'
thumbnail: './images/shop-thumb.jpg'
images:
  - './images/shop-1.jpg'
  - './images/shop-2.jpg'
  - './images/shop-3.jpg'
date: 2023-06-01
endDate: 2023-12-15
status: 'completed'
featured: true
client: 'Example Corp'
team: ['john-doe', 'jane-smith']
tags: ['web-dev', 'e-commerce', 'react']
---
```

## Zod Validation Patterns

### String Validation

```typescript
// Basic string
title: z.string()

// Length constraints
title: z.string().min(1).max(100)
description: z.string().max(500)

// Email validation
email: z.string().email()

// URL validation
website: z.string().url()

// Regex pattern
slug: z.string().regex(/^[a-z0-9-]+$/)
phone: z.string().regex(/^\+?[1-9]\d{1,14}$/)

// Specific values
status: z.string().refine(val => ['draft', 'published'].includes(val))
```

### Number Validation

```typescript
// Basic number
count: z.number()

// Integer only
age: z.number().int()

// Positive numbers
price: z.number().positive()

// Range
rating: z.number().min(1).max(5)
percentage: z.number().min(0).max(100)

// With coercion (converts strings)
views: z.coerce.number()
```

### Date Validation

```typescript
// With coercion (recommended)
pubDate: z.coerce.date()

// Strict date object
deadline: z.date()

// Date range
startDate: z.coerce.date()
endDate: z.coerce.date().refine(
  (date) => date > startDate,
  "End date must be after start date"
)
```

### Array Validation

```typescript
// Array of strings
tags: z.array(z.string())

// Minimum items
tags: z.array(z.string()).min(1)

// Maximum items
images: z.array(z.string()).max(10)

// Default value
tags: z.array(z.string()).default([])

// Array of objects
authors: z.array(z.object({
  name: z.string(),
  email: z.string().email()
}))
```

### Object Validation

```typescript
// Nested object
author: z.object({
  name: z.string(),
  email: z.string().email(),
  url: z.string().url().optional()
})

// Record (dynamic keys)
metadata: z.record(z.string())
settings: z.record(z.boolean())

// Partial object (all fields optional)
options: z.object({
  theme: z.string(),
  color: z.string()
}).partial()
```

### Enum Validation

```typescript
// Fixed set of values
status: z.enum(['draft', 'published', 'archived'])
priority: z.enum(['low', 'medium', 'high'])
category: z.enum(['news', 'tutorial', 'guide'])
```

### Boolean Validation

```typescript
// Basic boolean
published: z.boolean()

// With default
draft: z.boolean().default(false)
featured: z.boolean().default(false)
```

### Optional and Default Values

```typescript
// Optional field
subtitle: z.string().optional()
updatedDate: z.coerce.date().optional()

// With default value
draft: z.boolean().default(false)
views: z.number().default(0)
tags: z.array(z.string()).default([])
```

### Union Types

```typescript
// Multiple possible types
content: z.union([
  z.string(),
  z.object({ html: z.string() })
])

// Discriminated union
media: z.discriminatedUnion('type', [
  z.object({
    type: z.literal('image'),
    url: z.string(),
    alt: z.string()
  }),
  z.object({
    type: z.literal('video'),
    url: z.string(),
    duration: z.number()
  })
])
```

## Best Practices

1. **Use z.coerce.date()** for date strings in frontmatter
2. **Provide defaults** for booleans and arrays
3. **Use enums** for fixed sets of values
4. **Validate formats** with built-in validators (email, url)
5. **Add constraints** (min, max) for better validation
6. **Use optional()** for truly optional fields
7. **Document schemas** with TypeScript comments
8. **Keep schemas DRY** by extracting common patterns

## Common Frontmatter Patterns

### Minimal Blog Post

```yaml
---
title: 'Post Title'
description: 'Post description'
pubDate: 2024-01-15
author: 'Author Name'
tags: ['tag1', 'tag2']
---
```

### Full-Featured Blog Post

```yaml
---
title: 'Comprehensive Post Title'
description: 'Detailed SEO-optimized description'
pubDate: 2024-01-15
updatedDate: 2024-01-20
author: 'Author Name'
authorUrl: 'https://author.com'
tags: ['web-dev', 'tutorial']
category: 'tutorial'
draft: false
featured: true
image:
  url: './hero.jpg'
  alt: 'Hero image description'
canonicalURL: 'https://example.com/original'
readingTime: 10
relatedPosts: ['post-1', 'post-2']
---
```

### Documentation Page

```yaml
---
title: 'Getting Started'
description: 'Introduction to the framework'
sidebar:
  order: 1
  label: 'Intro'
lastUpdated: 2024-01-15
contributors: ['john', 'jane']
tableOfContents: true
---
```

### Product (JSON)

```json
{
  "name": "Product Name",
  "description": "Product description",
  "price": 99.99,
  "category": "software",
  "sku": "PROD-001",
  "inStock": true,
  "features": ["Feature 1", "Feature 2"],
  "images": [
    { "url": "/img.jpg", "alt": "Product", "primary": true }
  ]
}
```

## Tips

- Always match frontmatter to schema exactly
- Use ISO date format: `2024-01-15`
- Quote strings with special characters
- Use arrays for multiple values: `['tag1', 'tag2']`
- Nest objects with proper indentation
- Test with sample content first
- Check generated types in `.astro/types.d.ts`
