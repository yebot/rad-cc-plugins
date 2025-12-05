# Prisma CRUD Operations

Complete reference for Create, Read, Update, and Delete operations with Prisma Client.

## Setup

```typescript
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

// Always disconnect when done (in scripts)
async function main() {
  // Your queries here
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect())
```

## CREATE Operations

### create() - Single Record

```typescript
// Basic create
const user = await prisma.user.create({
  data: {
    email: 'alice@example.com',
    name: 'Alice',
  },
})

// Create with relation
const userWithPost = await prisma.user.create({
  data: {
    email: 'bob@example.com',
    name: 'Bob',
    posts: {
      create: {
        title: 'My First Post',
        content: 'Hello World!',
      },
    },
  },
  include: {
    posts: true,
  },
})

// Create with multiple nested records
const userWithPosts = await prisma.user.create({
  data: {
    email: 'carol@example.com',
    name: 'Carol',
    posts: {
      create: [
        { title: 'Post 1', content: 'Content 1' },
        { title: 'Post 2', content: 'Content 2' },
      ],
    },
  },
  include: {
    posts: true,
  },
})

// Create and connect to existing record
const post = await prisma.post.create({
  data: {
    title: 'New Post',
    author: {
      connect: { id: 1 },
    },
  },
})

// connectOrCreate - connect if exists, create if not
const post = await prisma.post.create({
  data: {
    title: 'Tagged Post',
    author: { connect: { id: 1 } },
    tags: {
      connectOrCreate: [
        {
          where: { name: 'typescript' },
          create: { name: 'typescript' },
        },
        {
          where: { name: 'prisma' },
          create: { name: 'prisma' },
        },
      ],
    },
  },
})
```

### createMany() - Multiple Records

```typescript
// Bulk insert
const result = await prisma.user.createMany({
  data: [
    { email: 'user1@example.com', name: 'User 1' },
    { email: 'user2@example.com', name: 'User 2' },
    { email: 'user3@example.com', name: 'User 3' },
  ],
})
// Returns: { count: 3 }

// Skip duplicates (PostgreSQL, MySQL, SQLite)
const result = await prisma.user.createMany({
  data: [
    { email: 'existing@example.com', name: 'Existing' },
    { email: 'new@example.com', name: 'New' },
  ],
  skipDuplicates: true,
})
```

### createManyAndReturn() - Bulk Insert with Return

```typescript
// PostgreSQL, CockroachDB, SQLite (Prisma 5.14.0+)
const users = await prisma.user.createManyAndReturn({
  data: [
    { email: 'user1@example.com', name: 'User 1' },
    { email: 'user2@example.com', name: 'User 2' },
  ],
  select: {
    id: true,
    email: true,
  },
})
```

## READ Operations

### findUnique() - Single Record by Unique Field

```typescript
// By primary key
const user = await prisma.user.findUnique({
  where: { id: 1 },
})

// By unique field
const user = await prisma.user.findUnique({
  where: { email: 'alice@example.com' },
})

// By compound unique constraint
const orderItem = await prisma.orderItem.findUnique({
  where: {
    orderId_productId: {
      orderId: 1,
      productId: 2,
    },
  },
})

// With relations
const user = await prisma.user.findUnique({
  where: { id: 1 },
  include: {
    posts: true,
    profile: true,
  },
})
```

### findUniqueOrThrow() - Throws if Not Found

```typescript
try {
  const user = await prisma.user.findUniqueOrThrow({
    where: { id: 999 },
  })
} catch (error) {
  // PrismaClientKnownRequestError with code P2025
  console.error('User not found')
}
```

### findFirst() - First Matching Record

```typescript
// Find first matching
const post = await prisma.post.findFirst({
  where: {
    published: true,
  },
})

// With ordering
const latestPost = await prisma.post.findFirst({
  where: { authorId: 1 },
  orderBy: { createdAt: 'desc' },
})

// Filter by relation
const userWithPosts = await prisma.user.findFirst({
  where: {
    posts: {
      some: {
        published: true,
      },
    },
  },
})
```

### findMany() - Multiple Records

```typescript
// All records
const users = await prisma.user.findMany()

// With filtering
const activeUsers = await prisma.user.findMany({
  where: {
    active: true,
    role: 'ADMIN',
  },
})

// With pagination
const users = await prisma.user.findMany({
  skip: 20,
  take: 10,
})

// Cursor-based pagination
const users = await prisma.user.findMany({
  take: 10,
  cursor: { id: 100 },
  skip: 1, // Skip the cursor
})

// With ordering
const users = await prisma.user.findMany({
  orderBy: [
    { role: 'asc' },
    { name: 'asc' },
  ],
})

// With field selection
const users = await prisma.user.findMany({
  select: {
    id: true,
    email: true,
    name: true,
  },
})

// With relations
const users = await prisma.user.findMany({
  include: {
    posts: {
      where: { published: true },
      orderBy: { createdAt: 'desc' },
      take: 5,
    },
    _count: {
      select: { posts: true },
    },
  },
})
```

### count() - Count Records

```typescript
// Count all
const userCount = await prisma.user.count()

// Count with filter
const adminCount = await prisma.user.count({
  where: { role: 'ADMIN' },
})
```

### aggregate() - Aggregations

```typescript
const stats = await prisma.post.aggregate({
  _count: { id: true },
  _avg: { views: true },
  _sum: { views: true },
  _min: { views: true },
  _max: { views: true },
  where: {
    published: true,
  },
})
```

### groupBy() - Group Results

```typescript
const postsByStatus = await prisma.post.groupBy({
  by: ['status'],
  _count: { id: true },
  _avg: { views: true },
})

// With filtering
const postsByAuthor = await prisma.post.groupBy({
  by: ['authorId'],
  _count: { id: true },
  having: {
    id: {
      _count: {
        gt: 5,
      },
    },
  },
})
```

## UPDATE Operations

### update() - Single Record

```typescript
// Basic update
const user = await prisma.user.update({
  where: { id: 1 },
  data: { name: 'Updated Name' },
})

// Update with relations
const user = await prisma.user.update({
  where: { id: 1 },
  data: {
    posts: {
      create: { title: 'New Post' },
    },
  },
  include: { posts: true },
})

// Disconnect relation
const user = await prisma.user.update({
  where: { id: 1 },
  data: {
    profile: {
      disconnect: true,
    },
  },
})

// Connect to different record
const post = await prisma.post.update({
  where: { id: 1 },
  data: {
    author: {
      connect: { id: 2 },
    },
  },
})
```

### Atomic Number Operations

```typescript
// Increment/Decrement
const post = await prisma.post.update({
  where: { id: 1 },
  data: {
    views: { increment: 1 },
    likes: { decrement: 1 },
  },
})

// Multiply/Divide
const product = await prisma.product.update({
  where: { id: 1 },
  data: {
    price: { multiply: 1.1 },  // 10% increase
    stock: { divide: 2 },
  },
})
```

### updateMany() - Multiple Records

```typescript
// Update many
const result = await prisma.post.updateMany({
  where: {
    authorId: 1,
    published: false,
  },
  data: {
    published: true,
  },
})
// Returns: { count: 5 }
```

### upsert() - Update or Create

```typescript
const user = await prisma.user.upsert({
  where: { email: 'alice@example.com' },
  update: {
    name: 'Alice Updated',
    lastLogin: new Date(),
  },
  create: {
    email: 'alice@example.com',
    name: 'Alice',
  },
})
```

## DELETE Operations

### delete() - Single Record

```typescript
const user = await prisma.user.delete({
  where: { id: 1 },
})
```

### deleteMany() - Multiple Records

```typescript
// Delete matching records
const result = await prisma.post.deleteMany({
  where: {
    authorId: 1,
    published: false,
  },
})
// Returns: { count: 3 }

// Delete all records
const result = await prisma.post.deleteMany({})
```

### Cascading Deletes with Transaction

```typescript
// Delete related records first
const deleteComments = prisma.comment.deleteMany({
  where: { postId: 1 },
})

const deletePost = prisma.post.delete({
  where: { id: 1 },
})

// Execute in order
await prisma.$transaction([deleteComments, deletePost])
```

## Select vs Include

### select - Return Specific Fields Only

```typescript
const user = await prisma.user.findUnique({
  where: { id: 1 },
  select: {
    id: true,
    email: true,
    posts: {
      select: {
        id: true,
        title: true,
      },
    },
  },
})
// Returns: { id: 1, email: '...', posts: [{ id: 1, title: '...' }] }
```

### include - Return All Fields Plus Relations

```typescript
const user = await prisma.user.findUnique({
  where: { id: 1 },
  include: {
    posts: true,
    profile: true,
  },
})
// Returns: { id, email, name, ..., posts: [...], profile: {...} }
```

### Nested Selection

```typescript
const user = await prisma.user.findUnique({
  where: { id: 1 },
  include: {
    posts: {
      select: {
        id: true,
        title: true,
        comments: {
          select: {
            id: true,
            content: true,
          },
          take: 3,
        },
      },
      where: { published: true },
      orderBy: { createdAt: 'desc' },
      take: 5,
    },
  },
})
```

## Relation Count

```typescript
const user = await prisma.user.findUnique({
  where: { id: 1 },
  include: {
    _count: {
      select: {
        posts: true,
        comments: true,
      },
    },
  },
})
// Returns: { ..., _count: { posts: 10, comments: 25 } }
```

## Distinct

```typescript
// Get distinct values
const categories = await prisma.post.findMany({
  distinct: ['category'],
  select: { category: true },
})
```

## Raw Queries

```typescript
// Raw SELECT
const users = await prisma.$queryRaw`
  SELECT * FROM users WHERE email LIKE ${`%@example.com`}
`

// Raw INSERT/UPDATE/DELETE
const result = await prisma.$executeRaw`
  UPDATE users SET active = true WHERE last_login > ${lastMonth}
`

// Unsafe (use with caution - SQL injection risk)
const users = await prisma.$queryRawUnsafe(
  `SELECT * FROM users WHERE role = '${role}'`
)
```