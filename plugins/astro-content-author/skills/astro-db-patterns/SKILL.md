# Astro DB Patterns Skill

Common patterns and examples for using Astro DB, including schema design, queries, and data seeding.

## When to Use This Skill

- Setting up Astro DB in a project
- Designing database schemas
- Writing queries with Drizzle ORM
- Seeding development data
- Building API endpoints with database access

## Database Setup

### Install Astro DB

```bash
npx astro add db
```

### Configuration File

Create `db/config.ts`:

```typescript
import { defineDb, defineTable, column } from 'astro:db';

const MyTable = defineTable({
  columns: {
    id: column.number({ primaryKey: true }),
    // ... other columns
  }
});

export default defineDb({
  tables: { MyTable }
});
```

## Column Types

### Text Columns

```typescript
// Basic text
name: column.text()

// Unique text
email: column.text({ unique: true })

// Optional text
bio: column.text({ optional: true })

// Text with default
status: column.text({ default: 'active' })
```

### Number Columns

```typescript
// Basic number
age: column.number()

// Primary key
id: column.number({ primaryKey: true })

// Optional number
rating: column.number({ optional: true })

// Number with default
views: column.number({ default: 0 })

// Unique number
userId: column.number({ unique: true })
```

### Boolean Columns

```typescript
// Basic boolean
published: column.boolean()

// Boolean with default
active: column.boolean({ default: true })
featured: column.boolean({ default: false })

// Optional boolean
verified: column.boolean({ optional: true })
```

### Date Columns

```typescript
// Basic date
createdAt: column.date()

// Optional date
publishedAt: column.date({ optional: true })

// Date with default (requires runtime value)
updatedAt: column.date({ default: new Date() })
```

### JSON Columns

```typescript
// JSON data
metadata: column.json()

// JSON with default
settings: column.json({ default: {} })
options: column.json({ default: [] })

// Optional JSON
extra: column.json({ optional: true })
```

## Common Schema Patterns

### Blog Database

```typescript
import { defineDb, defineTable, column } from 'astro:db';

const Author = defineTable({
  columns: {
    id: column.number({ primaryKey: true }),
    name: column.text(),
    email: column.text({ unique: true }),
    bio: column.text({ optional: true }),
    avatar: column.text({ optional: true }),
    website: column.text({ optional: true }),
    createdAt: column.date()
  }
});

const Post = defineTable({
  columns: {
    id: column.number({ primaryKey: true }),
    title: column.text(),
    slug: column.text({ unique: true }),
    content: column.text(),
    excerpt: column.text({ optional: true }),
    published: column.boolean({ default: false }),
    publishedAt: column.date({ optional: true }),
    updatedAt: column.date({ optional: true }),
    authorId: column.number(),
    views: column.number({ default: 0 }),
    featured: column.boolean({ default: false })
  }
});

const Tag = defineTable({
  columns: {
    id: column.number({ primaryKey: true }),
    name: column.text({ unique: true }),
    slug: column.text({ unique: true })
  }
});

const PostTag = defineTable({
  columns: {
    postId: column.number(),
    tagId: column.number()
  }
});

const Comment = defineTable({
  columns: {
    id: column.number({ primaryKey: true }),
    postId: column.number(),
    author: column.text(),
    email: column.text(),
    content: column.text(),
    approved: column.boolean({ default: false }),
    createdAt: column.date()
  }
});

export default defineDb({
  tables: { Author, Post, Tag, PostTag, Comment }
});
```

### E-commerce Database

```typescript
const Product = defineTable({
  columns: {
    id: column.number({ primaryKey: true }),
    name: column.text(),
    slug: column.text({ unique: true }),
    description: column.text(),
    price: column.number(),
    salePrice: column.number({ optional: true }),
    sku: column.text({ unique: true }),
    inStock: column.boolean({ default: true }),
    quantity: column.number({ default: 0 }),
    categoryId: column.number(),
    images: column.json({ default: [] }),
    createdAt: column.date()
  }
});

const Category = defineTable({
  columns: {
    id: column.number({ primaryKey: true }),
    name: column.text(),
    slug: column.text({ unique: true }),
    description: column.text({ optional: true }),
    parentId: column.number({ optional: true })
  }
});

const Order = defineTable({
  columns: {
    id: column.number({ primaryKey: true }),
    orderNumber: column.text({ unique: true }),
    customerId: column.number(),
    total: column.number(),
    status: column.text({ default: 'pending' }),
    createdAt: column.date(),
    completedAt: column.date({ optional: true })
  }
});

const OrderItem = defineTable({
  columns: {
    id: column.number({ primaryKey: true }),
    orderId: column.number(),
    productId: column.number(),
    quantity: column.number(),
    price: column.number()
  }
});

export default defineDb({
  tables: { Product, Category, Order, OrderItem }
});
```

### User Management Database

```typescript
const User = defineTable({
  columns: {
    id: column.number({ primaryKey: true }),
    username: column.text({ unique: true }),
    email: column.text({ unique: true }),
    passwordHash: column.text(),
    firstName: column.text(),
    lastName: column.text(),
    role: column.text({ default: 'user' }),
    active: column.boolean({ default: true }),
    emailVerified: column.boolean({ default: false }),
    lastLogin: column.date({ optional: true }),
    createdAt: column.date()
  }
});

const Session = defineTable({
  columns: {
    id: column.text({ primaryKey: true }),
    userId: column.number(),
    expiresAt: column.date(),
    createdAt: column.date()
  }
});

const UserProfile = defineTable({
  columns: {
    userId: column.number({ unique: true }),
    bio: column.text({ optional: true }),
    avatar: column.text({ optional: true }),
    location: column.text({ optional: true }),
    website: column.text({ optional: true }),
    social: column.json({ default: {} })
  }
});

export default defineDb({
  tables: { User, Session, UserProfile }
});
```

## Data Seeding

### Basic Seed File

Create `db/seed.ts`:

```typescript
import { db, Author, Post, Tag } from 'astro:db';

export default async function seed() {
  // Insert authors
  await db.insert(Author).values([
    {
      id: 1,
      name: 'John Doe',
      email: 'john@example.com',
      bio: 'Tech enthusiast and blogger',
      createdAt: new Date('2024-01-01')
    },
    {
      id: 2,
      name: 'Jane Smith',
      email: 'jane@example.com',
      bio: 'Software developer',
      createdAt: new Date('2024-01-01')
    }
  ]);

  // Insert tags
  await db.insert(Tag).values([
    { id: 1, name: 'Astro', slug: 'astro' },
    { id: 2, name: 'JavaScript', slug: 'javascript' },
    { id: 3, name: 'Tutorial', slug: 'tutorial' }
  ]);

  // Insert posts
  await db.insert(Post).values([
    {
      id: 1,
      title: 'Getting Started with Astro',
      slug: 'getting-started-astro',
      content: 'Full post content here...',
      excerpt: 'Learn the basics of Astro',
      published: true,
      publishedAt: new Date('2024-01-15'),
      authorId: 1,
      views: 150,
      featured: true
    },
    {
      id: 2,
      title: 'Advanced Astro Patterns',
      slug: 'advanced-astro',
      content: 'Advanced content...',
      published: false,
      authorId: 2,
      views: 0
    }
  ]);
}
```

### Seed with Relationships

```typescript
import { db, Post, Tag, PostTag, Comment } from 'astro:db';

export default async function seed() {
  // ... insert posts and tags ...

  // Link posts to tags (many-to-many)
  await db.insert(PostTag).values([
    { postId: 1, tagId: 1 },  // Post 1 -> Astro
    { postId: 1, tagId: 3 },  // Post 1 -> Tutorial
    { postId: 2, tagId: 1 },  // Post 2 -> Astro
    { postId: 2, tagId: 2 }   // Post 2 -> JavaScript
  ]);

  // Add comments
  await db.insert(Comment).values([
    {
      id: 1,
      postId: 1,
      author: 'Reader',
      email: 'reader@example.com',
      content: 'Great post!',
      approved: true,
      createdAt: new Date()
    }
  ]);
}
```

## Query Patterns

### Select All

```typescript
import { db, Post } from 'astro:db';

const allPosts = await db.select().from(Post);
```

### Select with Filter

```typescript
import { db, Post, eq } from 'astro:db';

// Published posts
const publishedPosts = await db
  .select()
  .from(Post)
  .where(eq(Post.published, true));

// Post by slug
const post = await db
  .select()
  .from(Post)
  .where(eq(Post.slug, 'my-post'))
  .get();  // Returns single result or undefined
```

### Multiple Conditions

```typescript
import { db, Post, eq, gt, and, or } from 'astro:db';

// AND condition
const featuredPublished = await db
  .select()
  .from(Post)
  .where(and(
    eq(Post.published, true),
    eq(Post.featured, true)
  ));

// OR condition
const popularOrFeatured = await db
  .select()
  .from(Post)
  .where(or(
    gt(Post.views, 1000),
    eq(Post.featured, true)
  ));
```

### Comparison Operators

```typescript
import { db, Post, gt, gte, lt, lte, ne, like } from 'astro:db';

// Greater than
const popularPosts = await db
  .select()
  .from(Post)
  .where(gt(Post.views, 100));

// Greater than or equal
const recentPosts = await db
  .select()
  .from(Post)
  .where(gte(Post.publishedAt, new Date('2024-01-01')));

// Less than
const drafts = await db
  .select()
  .from(Post)
  .where(lt(Post.views, 10));

// Not equal
const notDrafts = await db
  .select()
  .from(Post)
  .where(ne(Post.published, false));

// LIKE pattern matching
const astroPosts = await db
  .select()
  .from(Post)
  .where(like(Post.title, '%Astro%'));
```

### Ordering Results

```typescript
import { db, Post, desc, asc } from 'astro:db';

// Descending order
const latestPosts = await db
  .select()
  .from(Post)
  .orderBy(desc(Post.publishedAt));

// Ascending order
const oldestFirst = await db
  .select()
  .from(Post)
  .orderBy(asc(Post.createdAt));

// Multiple order columns
const sorted = await db
  .select()
  .from(Post)
  .orderBy(desc(Post.featured), desc(Post.publishedAt));
```

### Limit and Offset

```typescript
import { db, Post, desc } from 'astro:db';

// Latest 10 posts
const latest = await db
  .select()
  .from(Post)
  .orderBy(desc(Post.publishedAt))
  .limit(10);

// Pagination
const page = 2;
const perPage = 10;
const paginated = await db
  .select()
  .from(Post)
  .limit(perPage)
  .offset((page - 1) * perPage);
```

### Joins

```typescript
import { db, Post, Author, eq } from 'astro:db';

// Inner join
const postsWithAuthors = await db
  .select()
  .from(Post)
  .innerJoin(Author, eq(Post.authorId, Author.id));

// Access joined data
postsWithAuthors.forEach(row => {
  console.log(row.Post.title);
  console.log(row.Author.name);
});
```

### Complex Join Query

```typescript
import { db, Post, Author, Tag, PostTag, eq } from 'astro:db';

// Posts with authors and tags
const postsWithDetails = await db
  .select({
    post: Post,
    author: Author,
    tag: Tag
  })
  .from(Post)
  .innerJoin(Author, eq(Post.authorId, Author.id))
  .innerJoin(PostTag, eq(Post.id, PostTag.postId))
  .innerJoin(Tag, eq(PostTag.tagId, Tag.id));
```

## Insert, Update, Delete

### Insert Single Record

```typescript
import { db, Post } from 'astro:db';

await db.insert(Post).values({
  title: 'New Post',
  slug: 'new-post',
  content: 'Content here',
  authorId: 1,
  published: false
});
```

### Insert Multiple Records

```typescript
await db.insert(Tag).values([
  { name: 'Tag 1', slug: 'tag-1' },
  { name: 'Tag 2', slug: 'tag-2' },
  { name: 'Tag 3', slug: 'tag-3' }
]);
```

### Update Records

```typescript
import { db, Post, eq } from 'astro:db';

// Update single field
await db
  .update(Post)
  .set({ views: 100 })
  .where(eq(Post.id, 1));

// Update multiple fields
await db
  .update(Post)
  .set({
    published: true,
    publishedAt: new Date(),
    updatedAt: new Date()
  })
  .where(eq(Post.slug, 'my-post'));
```

### Delete Records

```typescript
import { db, Post, Comment, eq, lt } from 'astro:db';

// Delete by ID
await db
  .delete(Post)
  .where(eq(Post.id, 1));

// Delete with condition
await db
  .delete(Comment)
  .where(lt(Comment.createdAt, new Date('2024-01-01')));
```

## API Endpoint Patterns

### GET All Items

```typescript
// src/pages/api/posts.json.ts
import type { APIRoute } from 'astro';
import { db, Post, desc } from 'astro:db';

export const GET: APIRoute = async () => {
  const posts = await db
    .select()
    .from(Post)
    .orderBy(desc(Post.publishedAt));

  return new Response(JSON.stringify(posts), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  });
};
```

### GET Single Item

```typescript
// src/pages/api/posts/[slug].json.ts
import type { APIRoute } from 'astro';
import { db, Post, eq } from 'astro:db';

export const GET: APIRoute = async ({ params }) => {
  const post = await db
    .select()
    .from(Post)
    .where(eq(Post.slug, params.slug))
    .get();

  if (!post) {
    return new Response(JSON.stringify({ error: 'Not found' }), {
      status: 404,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  return new Response(JSON.stringify(post), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  });
};
```

### POST Create Item

```typescript
// src/pages/api/posts.json.ts
import type { APIRoute } from 'astro';
import { db, Post } from 'astro:db';

export const POST: APIRoute = async ({ request }) => {
  try {
    const data = await request.json();

    await db.insert(Post).values({
      title: data.title,
      slug: data.slug,
      content: data.content,
      authorId: data.authorId,
      published: false,
      createdAt: new Date()
    });

    return new Response(JSON.stringify({ success: true }), {
      status: 201,
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
};
```

### PUT/PATCH Update Item

```typescript
// src/pages/api/posts/[id].json.ts
import type { APIRoute } from 'astro';
import { db, Post, eq } from 'astro:db';

export const PUT: APIRoute = async ({ params, request }) => {
  const data = await request.json();
  const id = parseInt(params.id);

  await db
    .update(Post)
    .set({
      ...data,
      updatedAt: new Date()
    })
    .where(eq(Post.id, id));

  return new Response(JSON.stringify({ success: true }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' }
  });
};
```

### DELETE Item

```typescript
export const DELETE: APIRoute = async ({ params }) => {
  const id = parseInt(params.id);

  await db.delete(Post).where(eq(Post.id, id));

  return new Response(null, { status: 204 });
};
```

## Production Deployment

### Environment Variables

```env
# .env
ASTRO_DB_REMOTE_URL=libsql://your-db.turso.io
ASTRO_DB_APP_TOKEN=your-auth-token
```

### Push Schema to Production

```bash
astro db push --remote
```

### Verify Remote Connection

```bash
astro db verify --remote
```

## Best Practices

1. **Use Primary Keys**: Always define a primary key for each table
2. **Unique Constraints**: Use `unique: true` for fields like email, slug
3. **Default Values**: Provide sensible defaults for boolean/number fields
4. **Optional Fields**: Mark truly optional fields with `optional: true`
5. **Indexing**: Use unique constraints for fields you'll query often
6. **Relationships**: Use foreign keys (number columns) to link tables
7. **Dates**: Always use `column.date()` for timestamp fields
8. **JSON**: Use JSON columns for flexible/nested data
9. **Naming**: Use consistent naming (camelCase for columns, PascalCase for tables)
10. **Seeding**: Keep seed data representative and minimal

## Tips

- Dev server auto-restarts on schema changes
- Check `.astro/content.db` for local database
- Use `.get()` for single results, omit for arrays
- Drizzle ORM provides type-safe queries
- Test queries in seed file first
- Use transactions for related inserts
- Consider indexes for frequently queried fields
- Migrate carefully in production
