# Prisma Filtering and Sorting

Complete reference for filtering records and ordering results.

## Basic Filtering

### Equality

```typescript
// Exact match
const users = await prisma.user.findMany({
  where: {
    email: 'alice@example.com',
  },
})

// Same as equals operator
const users = await prisma.user.findMany({
  where: {
    email: { equals: 'alice@example.com' },
  },
})
```

### Not Equal

```typescript
const users = await prisma.user.findMany({
  where: {
    role: { not: 'ADMIN' },
  },
})
```

### In / Not In

```typescript
// In list
const users = await prisma.user.findMany({
  where: {
    id: { in: [1, 2, 3, 4, 5] },
  },
})

// Not in list
const users = await prisma.user.findMany({
  where: {
    role: { notIn: ['ADMIN', 'MODERATOR'] },
  },
})
```

## Comparison Operators

```typescript
const posts = await prisma.post.findMany({
  where: {
    views: { gt: 100 },      // Greater than
    likes: { gte: 10 },      // Greater than or equal
    comments: { lt: 50 },    // Less than
    shares: { lte: 5 },      // Less than or equal
  },
})

// Date comparisons
const recentPosts = await prisma.post.findMany({
  where: {
    createdAt: {
      gte: new Date('2024-01-01'),
      lt: new Date('2024-02-01'),
    },
  },
})
```

## String Filters

```typescript
const users = await prisma.user.findMany({
  where: {
    email: { contains: '@gmail.com' },
  },
})

const users = await prisma.user.findMany({
  where: {
    name: { startsWith: 'A' },
  },
})

const users = await prisma.user.findMany({
  where: {
    email: { endsWith: '.com' },
  },
})
```

### Case-Insensitive Search

```typescript
// PostgreSQL and MongoDB only
const users = await prisma.user.findMany({
  where: {
    email: {
      contains: 'alice',
      mode: 'insensitive',
    },
  },
})

const users = await prisma.user.findMany({
  where: {
    name: {
      startsWith: 'j',
      mode: 'insensitive',
    },
  },
})
```

## Null Checks

```typescript
// Is null
const usersWithoutProfile = await prisma.user.findMany({
  where: {
    profileId: null,
  },
})

// Is not null
const usersWithProfile = await prisma.user.findMany({
  where: {
    profileId: { not: null },
  },
})
```

## Logical Operators

### AND

```typescript
// Implicit AND (all conditions in same object)
const posts = await prisma.post.findMany({
  where: {
    published: true,
    authorId: 1,
  },
})

// Explicit AND
const posts = await prisma.post.findMany({
  where: {
    AND: [
      { published: true },
      { authorId: 1 },
      { views: { gt: 100 } },
    ],
  },
})
```

### OR

```typescript
const users = await prisma.user.findMany({
  where: {
    OR: [
      { email: { endsWith: '@gmail.com' } },
      { email: { endsWith: '@yahoo.com' } },
    ],
  },
})
```

### NOT

```typescript
const users = await prisma.user.findMany({
  where: {
    NOT: {
      role: 'ADMIN',
    },
  },
})

// Multiple NOT conditions
const users = await prisma.user.findMany({
  where: {
    NOT: [
      { role: 'ADMIN' },
      { email: { endsWith: '@test.com' } },
    ],
  },
})
```

### Combined Operators

```typescript
const users = await prisma.user.findMany({
  where: {
    OR: [
      {
        AND: [
          { role: 'ADMIN' },
          { active: true },
        ],
      },
      {
        AND: [
          { role: 'MODERATOR' },
          { verified: true },
        ],
      },
    ],
    NOT: {
      email: { endsWith: '@blocked.com' },
    },
  },
})
```

## Filtering by Relations

### some - At Least One Match

```typescript
// Users who have at least one published post
const users = await prisma.user.findMany({
  where: {
    posts: {
      some: {
        published: true,
      },
    },
  },
})
```

### every - All Must Match

```typescript
// Users where all posts are published
const users = await prisma.user.findMany({
  where: {
    posts: {
      every: {
        published: true,
      },
    },
  },
})
```

### none - No Matches

```typescript
// Users with no unpublished posts
const users = await prisma.user.findMany({
  where: {
    posts: {
      none: {
        published: false,
      },
    },
  },
})

// Users with no posts at all
const usersWithoutPosts = await prisma.user.findMany({
  where: {
    posts: {
      none: {},
    },
  },
})
```

### Nested Relation Filters

```typescript
// Posts by users who are admins
const posts = await prisma.post.findMany({
  where: {
    author: {
      role: 'ADMIN',
    },
  },
})

// Posts with comments from specific user
const posts = await prisma.post.findMany({
  where: {
    comments: {
      some: {
        author: {
          email: 'alice@example.com',
        },
      },
    },
  },
})
```

### is / isNot for Optional Relations

```typescript
// Posts with no author (null)
const orphanPosts = await prisma.post.findMany({
  where: {
    author: null,
  },
})

// Posts with an author
const authoredPosts = await prisma.post.findMany({
  where: {
    author: { isNot: null },
  },
})

// Alternative syntax
const authoredPosts = await prisma.post.findMany({
  where: {
    author: {
      is: {
        role: 'ADMIN',
      },
    },
  },
})
```

## Sorting

### Basic Ordering

```typescript
// Ascending
const users = await prisma.user.findMany({
  orderBy: {
    name: 'asc',
  },
})

// Descending
const users = await prisma.user.findMany({
  orderBy: {
    createdAt: 'desc',
  },
})
```

### Multiple Sort Fields

```typescript
const users = await prisma.user.findMany({
  orderBy: [
    { role: 'asc' },
    { name: 'asc' },
  ],
})
```

### Sort by Relation Field

```typescript
// Posts sorted by author name
const posts = await prisma.post.findMany({
  orderBy: {
    author: {
      name: 'asc',
    },
  },
})
```

### Sort by Relation Count

```typescript
// Users sorted by number of posts
const users = await prisma.user.findMany({
  orderBy: {
    posts: {
      _count: 'desc',
    },
  },
})
```

### Sort Nested Relations

```typescript
const users = await prisma.user.findMany({
  include: {
    posts: {
      orderBy: {
        createdAt: 'desc',
      },
    },
  },
})
```

### Null Positioning

```typescript
// Nulls last
const users = await prisma.user.findMany({
  orderBy: {
    name: { sort: 'asc', nulls: 'last' },
  },
})

// Nulls first
const users = await prisma.user.findMany({
  orderBy: {
    deletedAt: { sort: 'desc', nulls: 'first' },
  },
})
```

## Pagination

### Offset Pagination

```typescript
// Page 1 (items 1-10)
const page1 = await prisma.post.findMany({
  skip: 0,
  take: 10,
})

// Page 2 (items 11-20)
const page2 = await prisma.post.findMany({
  skip: 10,
  take: 10,
})

// Helper function
async function getPaginatedPosts(page: number, pageSize: number = 10) {
  const skip = (page - 1) * pageSize

  const [posts, total] = await prisma.$transaction([
    prisma.post.findMany({
      skip,
      take: pageSize,
      orderBy: { createdAt: 'desc' },
    }),
    prisma.post.count(),
  ])

  return {
    posts,
    total,
    page,
    pageSize,
    totalPages: Math.ceil(total / pageSize),
  }
}
```

### Cursor Pagination

More efficient for large datasets.

```typescript
// First page
const firstPage = await prisma.post.findMany({
  take: 10,
  orderBy: { id: 'asc' },
})

// Next page (using last item's ID as cursor)
const lastId = firstPage[firstPage.length - 1].id

const nextPage = await prisma.post.findMany({
  take: 10,
  skip: 1,  // Skip the cursor
  cursor: { id: lastId },
  orderBy: { id: 'asc' },
})

// Helper function
async function getCursorPaginatedPosts(cursor?: number, pageSize: number = 10) {
  const posts = await prisma.post.findMany({
    take: pageSize + 1,  // Fetch one extra to check if there's more
    ...(cursor && {
      skip: 1,
      cursor: { id: cursor },
    }),
    orderBy: { id: 'asc' },
  })

  const hasMore = posts.length > pageSize
  const items = hasMore ? posts.slice(0, -1) : posts
  const nextCursor = hasMore ? items[items.length - 1].id : undefined

  return {
    items,
    nextCursor,
    hasMore,
  }
}
```

## Full-Text Search

### PostgreSQL

```typescript
// Enable in schema
generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["fullTextSearch"]
}

// Query
const posts = await prisma.post.findMany({
  where: {
    title: {
      search: 'prisma & database',
    },
  },
})

// Sort by relevance
const posts = await prisma.post.findMany({
  where: {
    title: {
      search: 'prisma',
    },
  },
  orderBy: {
    _relevance: {
      fields: ['title', 'content'],
      search: 'prisma',
      sort: 'desc',
    },
  },
})
```

### MySQL

```typescript
// Enable in schema
generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["fullTextSearch", "fullTextIndex"]
}

model Post {
  id      Int    @id
  title   String @db.VarChar(255)
  content String @db.Text

  @@fulltext([title, content])
}

// Query
const posts = await prisma.post.findMany({
  where: {
    title: {
      search: 'prisma database',
    },
  },
})
```

## JSON Filtering

```typescript
// Filter by JSON field value
const users = await prisma.user.findMany({
  where: {
    settings: {
      path: ['notifications', 'email'],
      equals: true,
    },
  },
})

// Array contains
const users = await prisma.user.findMany({
  where: {
    settings: {
      path: ['roles'],
      array_contains: 'admin',
    },
  },
})

// String contains in JSON
const users = await prisma.user.findMany({
  where: {
    settings: {
      path: ['theme'],
      string_contains: 'dark',
    },
  },
})
```

## Array Filtering (PostgreSQL)

```typescript
// Has element
const posts = await prisma.post.findMany({
  where: {
    tags: {
      has: 'prisma',
    },
  },
})

// Has every element
const posts = await prisma.post.findMany({
  where: {
    tags: {
      hasEvery: ['prisma', 'typescript'],
    },
  },
})

// Has some elements
const posts = await prisma.post.findMany({
  where: {
    tags: {
      hasSome: ['prisma', 'orm', 'database'],
    },
  },
})

// Is empty
const posts = await prisma.post.findMany({
  where: {
    tags: {
      isEmpty: true,
    },
  },
})
```
