# Prisma ORM Skill

Expert knowledge for working with Prisma ORM - the next-generation Node.js and TypeScript ORM.

## When to Use This Skill

Invoke this skill when working with:
- Database schema design with Prisma
- Prisma Client queries (CRUD operations)
- Database migrations
- Relations and data modeling
- Performance optimization
- Type-safe database access

## Documentation Files

This skill includes comprehensive Prisma documentation:

- [Schema Reference](./docs/schema-reference.md) - Data types, attributes, and schema syntax
- [CRUD Operations](./docs/crud-operations.md) - Create, Read, Update, Delete operations
- [Relations](./docs/relations.md) - One-to-one, one-to-many, many-to-many relationships
- [Filtering & Sorting](./docs/filtering-sorting.md) - Query filters and ordering
- [Transactions](./docs/transactions.md) - ACID transactions and batch operations
- [Migrations](./docs/migrations.md) - Database migration workflows

## Quick Reference

### Project Setup

```bash
# Install Prisma CLI
npm install prisma --save-dev

# Initialize Prisma in project
npx prisma init

# Install Prisma Client
npm install @prisma/client

# Generate client after schema changes
npx prisma generate

# Create and apply migrations
npx prisma migrate dev --name init

# Open Prisma Studio (GUI)
npx prisma studio
```

### Schema Structure

```prisma
// prisma/schema.prisma

generator client {
  provider = "prisma-client-js"
  output   = "./generated/client"
}

datasource db {
  provider = "postgresql"  // or mysql, sqlite, mongodb, cockroachdb
  url      = env("DATABASE_URL")
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String?
  role      Role     @default(USER)
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int

  @@index([authorId])
}

model Profile {
  id     Int    @id @default(autoincrement())
  bio    String?
  user   User   @relation(fields: [userId], references: [id])
  userId Int    @unique
}

enum Role {
  USER
  ADMIN
}
```

### Essential Prisma Client Patterns

```typescript
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

// CREATE
const user = await prisma.user.create({
  data: {
    email: 'alice@example.com',
    name: 'Alice',
    posts: {
      create: { title: 'Hello World' }
    }
  },
  include: { posts: true }
})

// READ
const users = await prisma.user.findMany({
  where: {
    email: { contains: '@example.com' }
  },
  include: { posts: true },
  orderBy: { createdAt: 'desc' },
  take: 10
})

// UPDATE
const updated = await prisma.user.update({
  where: { id: 1 },
  data: { name: 'Alice Updated' }
})

// DELETE
const deleted = await prisma.user.delete({
  where: { id: 1 }
})

// UPSERT
const upserted = await prisma.user.upsert({
  where: { email: 'bob@example.com' },
  update: { name: 'Bob Updated' },
  create: { email: 'bob@example.com', name: 'Bob' }
})

// TRANSACTION
const [posts, users] = await prisma.$transaction([
  prisma.post.findMany(),
  prisma.user.count()
])

// INTERACTIVE TRANSACTION
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data: { email: 'new@example.com' } })
  await tx.post.create({ data: { title: 'Post', authorId: user.id } })
})
```

## Best Practices

### Schema Design

1. **Always define explicit output** for generator:
   ```prisma
   generator client {
     provider = "prisma-client-js"
     output   = "./generated/client"
   }
   ```

2. **Use indexes for foreign keys and frequently queried fields**:
   ```prisma
   model Post {
     authorId Int
     @@index([authorId])
   }
   ```

3. **Use enums for fixed value sets**:
   ```prisma
   enum Status {
     DRAFT
     PUBLISHED
     ARCHIVED
   }
   ```

### Query Optimization

1. **Select only needed fields**:
   ```typescript
   const users = await prisma.user.findMany({
     select: { id: true, email: true }
   })
   ```

2. **Use pagination for large datasets**:
   ```typescript
   const users = await prisma.user.findMany({
     skip: 20,
     take: 10
   })
   ```

3. **Batch operations for bulk updates**:
   ```typescript
   await prisma.post.updateMany({
     where: { published: false },
     data: { published: true }
   })
   ```

### Migrations

1. **Always name migrations descriptively**:
   ```bash
   npx prisma migrate dev --name add_user_profile
   ```

2. **Review generated SQL before applying**:
   ```bash
   npx prisma migrate dev --create-only
   ```

3. **Use baseline for existing databases**:
   ```bash
   npx prisma migrate resolve --applied 0_init
   ```

## Common Patterns

### Soft Delete

```prisma
model Post {
  id        Int       @id @default(autoincrement())
  deletedAt DateTime?

  @@index([deletedAt])
}
```

```typescript
// Soft delete
await prisma.post.update({
  where: { id: 1 },
  data: { deletedAt: new Date() }
})

// Query non-deleted
const posts = await prisma.post.findMany({
  where: { deletedAt: null }
})
```

### Optimistic Locking

```prisma
model Resource {
  id      Int @id @default(autoincrement())
  data    String
  version Int @default(0)
}
```

```typescript
const resource = await prisma.resource.findUnique({ where: { id: 1 } })

const updated = await prisma.resource.updateMany({
  where: { id: 1, version: resource.version },
  data: { data: 'new data', version: { increment: 1 } }
})

if (updated.count === 0) {
  throw new Error('Concurrent modification detected')
}
```

### Connection Pooling

```typescript
// For serverless environments
const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL + '?connection_limit=1'
    }
  }
})
```