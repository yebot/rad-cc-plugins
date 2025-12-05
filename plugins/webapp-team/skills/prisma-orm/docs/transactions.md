# Prisma Transactions

Complete guide to database transactions with Prisma.

## Transaction Types Overview

| Type | Use Case | Method |
|------|----------|--------|
| Nested Writes | Related records in single query | Automatic |
| Sequential Operations | Independent queries together | `$transaction([])` |
| Interactive | Complex logic with conditionals | `$transaction(async (tx) => {})` |
| Batch Operations | Bulk create/update/delete | `createMany`, `updateMany`, `deleteMany` |

## Nested Writes (Automatic Transactions)

Creating or updating related records atomically.

```typescript
// Create user with profile and posts - all or nothing
const user = await prisma.user.create({
  data: {
    email: 'alice@example.com',
    name: 'Alice',
    profile: {
      create: {
        bio: 'Software Developer',
      },
    },
    posts: {
      create: [
        { title: 'Post 1', content: 'Content 1' },
        { title: 'Post 2', content: 'Content 2' },
      ],
    },
  },
  include: {
    profile: true,
    posts: true,
  },
})

// Update with nested operations
const user = await prisma.user.update({
  where: { id: 1 },
  data: {
    profile: {
      update: { bio: 'Updated bio' },
    },
    posts: {
      updateMany: {
        where: { published: false },
        data: { published: true },
      },
    },
  },
})
```

## Sequential Operations ($transaction array)

Execute multiple independent queries in a single transaction.

```typescript
// Basic transaction
const [posts, users] = await prisma.$transaction([
  prisma.post.findMany({ where: { published: true } }),
  prisma.user.count(),
])

// Delete in correct order (foreign key constraints)
const deleteComments = prisma.comment.deleteMany({
  where: { postId: 1 },
})
const deletePost = prisma.post.delete({
  where: { id: 1 },
})

await prisma.$transaction([deleteComments, deletePost])

// Transfer between accounts
const from = prisma.account.update({
  where: { id: 1 },
  data: { balance: { decrement: 100 } },
})
const to = prisma.account.update({
  where: { id: 2 },
  data: { balance: { increment: 100 } },
})

await prisma.$transaction([from, to])
```

### With Isolation Level

```typescript
await prisma.$transaction(
  [
    prisma.account.update({
      where: { id: 1 },
      data: { balance: { decrement: 100 } },
    }),
    prisma.account.update({
      where: { id: 2 },
      data: { balance: { increment: 100 } },
    }),
  ],
  {
    isolationLevel: Prisma.TransactionIsolationLevel.Serializable,
  }
)
```

## Interactive Transactions

For complex logic that requires reading data before writing.

```typescript
// Money transfer with balance check
async function transfer(from: string, to: string, amount: number) {
  return prisma.$transaction(async (tx) => {
    // 1. Check sender's balance
    const sender = await tx.account.findUnique({
      where: { email: from },
    })

    if (!sender || sender.balance < amount) {
      throw new Error('Insufficient funds')
    }

    // 2. Deduct from sender
    await tx.account.update({
      where: { email: from },
      data: { balance: { decrement: amount } },
    })

    // 3. Add to recipient
    const recipient = await tx.account.update({
      where: { email: to },
      data: { balance: { increment: amount } },
    })

    return recipient
  })
}

// Usage
try {
  await transfer('alice@example.com', 'bob@example.com', 100)
} catch (error) {
  console.error('Transfer failed:', error.message)
}
```

### With Configuration

```typescript
await prisma.$transaction(
  async (tx) => {
    // Transaction logic
  },
  {
    maxWait: 5000,   // Max time to wait to acquire a connection (default: 2000ms)
    timeout: 10000,  // Max time for transaction to complete (default: 5000ms)
    isolationLevel: Prisma.TransactionIsolationLevel.ReadCommitted,
  }
)
```

### Default Configuration at Client Level

```typescript
const prisma = new PrismaClient({
  transactionOptions: {
    isolationLevel: Prisma.TransactionIsolationLevel.Serializable,
    maxWait: 5000,
    timeout: 10000,
  },
})
```

## Isolation Levels

| Level | Dirty Read | Non-Repeatable Read | Phantom Read |
|-------|------------|---------------------|--------------|
| ReadUncommitted | Possible | Possible | Possible |
| ReadCommitted | No | Possible | Possible |
| RepeatableRead | No | No | Possible |
| Serializable | No | No | No |

### Database Support

| Database | Default | Supported Levels |
|----------|---------|------------------|
| PostgreSQL | ReadCommitted | All except Snapshot |
| MySQL | RepeatableRead | All except Snapshot |
| SQL Server | ReadCommitted | All |
| SQLite | Serializable | Serializable only |
| CockroachDB | Serializable | Serializable only |

```typescript
import { Prisma } from '@prisma/client'

// PostgreSQL example
await prisma.$transaction(
  async (tx) => {
    // ...
  },
  {
    isolationLevel: Prisma.TransactionIsolationLevel.Serializable,
  }
)
```

## Batch Operations

All batch operations are automatically transactional.

### createMany

```typescript
const result = await prisma.user.createMany({
  data: [
    { email: 'user1@example.com', name: 'User 1' },
    { email: 'user2@example.com', name: 'User 2' },
    { email: 'user3@example.com', name: 'User 3' },
  ],
  skipDuplicates: true,  // Skip records that violate unique constraints
})
// Returns: { count: 3 }
```

### updateMany

```typescript
const result = await prisma.post.updateMany({
  where: {
    authorId: 1,
    published: false,
  },
  data: {
    published: true,
    publishedAt: new Date(),
  },
})
// Returns: { count: 5 }
```

### deleteMany

```typescript
const result = await prisma.comment.deleteMany({
  where: {
    postId: 1,
  },
})
// Returns: { count: 10 }
```

## Error Handling

### Transaction Rollback

```typescript
try {
  await prisma.$transaction(async (tx) => {
    await tx.user.create({ data: { email: 'test@example.com' } })

    // This will fail and rollback the user creation
    throw new Error('Something went wrong')
  })
} catch (error) {
  console.error('Transaction rolled back:', error.message)
}
```

### Retry Logic for Serialization Errors

```typescript
const MAX_RETRIES = 3

async function executeWithRetry<T>(
  fn: () => Promise<T>,
  retries = MAX_RETRIES
): Promise<T> {
  try {
    return await fn()
  } catch (error) {
    if (error.code === 'P2034' && retries > 0) {
      // P2034: Transaction failed due to conflict
      console.log(`Retrying transaction... (${retries} attempts left)`)
      return executeWithRetry(fn, retries - 1)
    }
    throw error
  }
}

// Usage
const result = await executeWithRetry(async () => {
  return prisma.$transaction(
    async (tx) => {
      // Your transaction logic
    },
    {
      isolationLevel: Prisma.TransactionIsolationLevel.Serializable,
    }
  )
})
```

## Optimistic Concurrency Control

Prevent lost updates with version checking.

```prisma
model Product {
  id      Int    @id @default(autoincrement())
  name    String
  stock   Int
  version Int    @default(0)
}
```

```typescript
async function decrementStock(productId: number, quantity: number) {
  // 1. Read current state
  const product = await prisma.product.findUnique({
    where: { id: productId },
  })

  if (!product || product.stock < quantity) {
    throw new Error('Insufficient stock')
  }

  // 2. Update with version check
  const result = await prisma.product.updateMany({
    where: {
      id: productId,
      version: product.version,  // Only succeed if version matches
    },
    data: {
      stock: { decrement: quantity },
      version: { increment: 1 },
    },
  })

  // 3. Check if update succeeded
  if (result.count === 0) {
    throw new Error('Concurrent modification detected. Please retry.')
  }

  return result
}
```

## Common Patterns

### Idempotent Operations

Design operations that can be safely retried.

```typescript
async function createOrderIdempotent(orderId: string, items: Item[]) {
  // Check if order already exists
  const existing = await prisma.order.findUnique({
    where: { id: orderId },
  })

  if (existing) {
    return existing  // Return existing order instead of creating duplicate
  }

  return prisma.order.create({
    data: {
      id: orderId,
      items: {
        create: items,
      },
    },
  })
}
```

### Atomic Counter

```typescript
// Safe increment without read-then-write race condition
const post = await prisma.post.update({
  where: { id: 1 },
  data: {
    views: { increment: 1 },
  },
})
```

### Reservation Pattern

```typescript
async function reserveSeat(seatId: number, userId: number) {
  return prisma.$transaction(async (tx) => {
    // Lock and check seat
    const seat = await tx.seat.findFirst({
      where: {
        id: seatId,
        reservedBy: null,
      },
    })

    if (!seat) {
      throw new Error('Seat not available')
    }

    // Reserve seat
    return tx.seat.update({
      where: { id: seatId },
      data: {
        reservedBy: userId,
        reservedAt: new Date(),
      },
    })
  })
}
```

## Best Practices

1. **Keep transactions short** - Long-running transactions can cause deadlocks and reduce concurrency.

2. **Avoid external calls in transactions** - Don't make HTTP requests or other I/O within interactive transactions.

3. **Use appropriate isolation level** - Higher isolation = more consistency but lower performance.

4. **Handle failures gracefully** - Implement retry logic for transient failures.

5. **Use optimistic locking for high-concurrency scenarios** - Reduces lock contention.

```typescript
// BAD: Long transaction with external call
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data: {...} })
  await sendWelcomeEmail(user.email)  // DON'T DO THIS
  await tx.emailLog.create({ data: {...} })
})

// GOOD: External call after transaction
const user = await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data: {...} })
  await tx.emailLog.create({ data: { status: 'pending', ... } })
  return user
})
await sendWelcomeEmail(user.email)
await prisma.emailLog.update({
  where: { userId: user.id },
  data: { status: 'sent' },
})
```
