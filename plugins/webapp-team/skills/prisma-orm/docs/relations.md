# Prisma Relations

Complete guide to defining and querying relationships between models.

## Relation Types Overview

| Type | Example | Foreign Key Location |
|------|---------|---------------------|
| One-to-One | User ↔ Profile | Either side (with @unique) |
| One-to-Many | User → Posts | "Many" side |
| Many-to-Many | Posts ↔ Tags | Join table |

## One-to-One Relations

A user has one profile, a profile belongs to one user.

```prisma
model User {
  id      Int      @id @default(autoincrement())
  email   String   @unique
  profile Profile?
}

model Profile {
  id     Int    @id @default(autoincrement())
  bio    String?
  user   User   @relation(fields: [userId], references: [id])
  userId Int    @unique  // @unique makes it one-to-one
}
```

### Querying One-to-One

```typescript
// Create user with profile
const user = await prisma.user.create({
  data: {
    email: 'alice@example.com',
    profile: {
      create: {
        bio: 'Software developer',
      },
    },
  },
  include: { profile: true },
})

// Get user with profile
const user = await prisma.user.findUnique({
  where: { id: 1 },
  include: { profile: true },
})

// Update profile through user
const user = await prisma.user.update({
  where: { id: 1 },
  data: {
    profile: {
      update: {
        bio: 'Updated bio',
      },
    },
  },
})

// Create or connect profile
const user = await prisma.user.update({
  where: { id: 1 },
  data: {
    profile: {
      upsert: {
        create: { bio: 'New bio' },
        update: { bio: 'Updated bio' },
      },
    },
  },
})
```

## One-to-Many Relations

A user has many posts, each post belongs to one user.

```prisma
model User {
  id    Int    @id @default(autoincrement())
  email String @unique
  posts Post[]
}

model Post {
  id       Int    @id @default(autoincrement())
  title    String
  author   User   @relation(fields: [authorId], references: [id])
  authorId Int

  @@index([authorId])
}
```

### Querying One-to-Many

```typescript
// Create user with posts
const user = await prisma.user.create({
  data: {
    email: 'bob@example.com',
    posts: {
      create: [
        { title: 'Post 1' },
        { title: 'Post 2' },
      ],
    },
  },
  include: { posts: true },
})

// Get user with filtered posts
const user = await prisma.user.findUnique({
  where: { id: 1 },
  include: {
    posts: {
      where: { published: true },
      orderBy: { createdAt: 'desc' },
      take: 10,
    },
  },
})

// Add posts to existing user
const user = await prisma.user.update({
  where: { id: 1 },
  data: {
    posts: {
      create: { title: 'New Post' },
    },
  },
})

// Connect existing post to user
const user = await prisma.user.update({
  where: { id: 1 },
  data: {
    posts: {
      connect: { id: 5 },
    },
  },
})

// Disconnect post from user
const user = await prisma.user.update({
  where: { id: 1 },
  data: {
    posts: {
      disconnect: { id: 5 },
    },
  },
})

// Set specific posts (replaces all)
const user = await prisma.user.update({
  where: { id: 1 },
  data: {
    posts: {
      set: [{ id: 1 }, { id: 2 }],
    },
  },
})
```

## Many-to-Many Relations

### Implicit Many-to-Many

Prisma automatically creates the join table.

```prisma
model Post {
  id    Int    @id @default(autoincrement())
  title String
  tags  Tag[]
}

model Tag {
  id    Int    @id @default(autoincrement())
  name  String @unique
  posts Post[]
}
```

### Querying Implicit Many-to-Many

```typescript
// Create post with tags
const post = await prisma.post.create({
  data: {
    title: 'Prisma Guide',
    tags: {
      create: [
        { name: 'prisma' },
        { name: 'database' },
      ],
    },
  },
  include: { tags: true },
})

// Connect existing tags
const post = await prisma.post.create({
  data: {
    title: 'Another Post',
    tags: {
      connect: [
        { name: 'prisma' },
        { name: 'database' },
      ],
    },
  },
})

// Connect or create
const post = await prisma.post.create({
  data: {
    title: 'Tagged Post',
    tags: {
      connectOrCreate: [
        {
          where: { name: 'typescript' },
          create: { name: 'typescript' },
        },
        {
          where: { name: 'nodejs' },
          create: { name: 'nodejs' },
        },
      ],
    },
  },
})

// Get posts by tag
const posts = await prisma.post.findMany({
  where: {
    tags: {
      some: {
        name: 'prisma',
      },
    },
  },
})
```

### Explicit Many-to-Many

When you need extra fields on the relation.

```prisma
model Post {
  id       Int            @id @default(autoincrement())
  title    String
  tags     PostTag[]
}

model Tag {
  id    Int       @id @default(autoincrement())
  name  String    @unique
  posts PostTag[]
}

model PostTag {
  post      Post     @relation(fields: [postId], references: [id])
  postId    Int
  tag       Tag      @relation(fields: [tagId], references: [id])
  tagId     Int
  assignedAt DateTime @default(now())
  assignedBy String?

  @@id([postId, tagId])
}
```

### Querying Explicit Many-to-Many

```typescript
// Create post with tags and metadata
const post = await prisma.post.create({
  data: {
    title: 'New Post',
    tags: {
      create: [
        {
          assignedBy: 'admin',
          tag: {
            connectOrCreate: {
              where: { name: 'prisma' },
              create: { name: 'prisma' },
            },
          },
        },
      ],
    },
  },
  include: {
    tags: {
      include: { tag: true },
    },
  },
})

// Query through join table
const postTags = await prisma.postTag.findMany({
  where: {
    post: { id: 1 },
  },
  include: {
    tag: true,
  },
})
```

## Self-Relations

A model relating to itself.

### One-to-Many Self-Relation (Tree Structure)

```prisma
model Category {
  id       Int        @id @default(autoincrement())
  name     String
  parent   Category?  @relation("CategoryToCategory", fields: [parentId], references: [id])
  parentId Int?
  children Category[] @relation("CategoryToCategory")
}
```

```typescript
// Create nested categories
const category = await prisma.category.create({
  data: {
    name: 'Electronics',
    children: {
      create: [
        {
          name: 'Phones',
          children: {
            create: [
              { name: 'Smartphones' },
              { name: 'Feature Phones' },
            ],
          },
        },
        { name: 'Computers' },
      ],
    },
  },
  include: {
    children: {
      include: { children: true },
    },
  },
})
```

### Many-to-Many Self-Relation (Followers)

```prisma
model User {
  id         Int    @id @default(autoincrement())
  name       String
  followers  User[] @relation("UserFollows")
  following  User[] @relation("UserFollows")
}
```

```typescript
// Follow a user
const user = await prisma.user.update({
  where: { id: 1 },
  data: {
    following: {
      connect: { id: 2 },
    },
  },
})

// Get followers
const user = await prisma.user.findUnique({
  where: { id: 1 },
  include: {
    followers: true,
    following: true,
  },
})
```

## Referential Actions

Control what happens when related records are deleted or updated.

```prisma
model Post {
  id       Int  @id @default(autoincrement())
  author   User @relation(fields: [authorId], references: [id], onDelete: Cascade, onUpdate: Cascade)
  authorId Int
}
```

### Available Actions

| Action | On Delete | On Update |
|--------|-----------|-----------|
| `Cascade` | Delete related records | Update foreign key |
| `Restrict` | Prevent deletion if related records exist | Prevent update |
| `NoAction` | Similar to Restrict (database-dependent) | Similar to Restrict |
| `SetNull` | Set foreign key to null | Set foreign key to null |
| `SetDefault` | Set foreign key to default value | Set foreign key to default |

### Common Patterns

```prisma
// Cascade delete - delete posts when user is deleted
model Post {
  author   User @relation(fields: [authorId], references: [id], onDelete: Cascade)
  authorId Int
}

// Set null - keep posts but remove author reference
model Post {
  author   User? @relation(fields: [authorId], references: [id], onDelete: SetNull)
  authorId Int?
}

// Restrict - prevent user deletion if they have posts
model Post {
  author   User @relation(fields: [authorId], references: [id], onDelete: Restrict)
  authorId Int
}
```

## Multiple Relations Between Same Models

Use relation names to disambiguate.

```prisma
model User {
  id           Int     @id @default(autoincrement())
  writtenPosts Post[]  @relation("WrittenPosts")
  likedPosts   Post[]  @relation("LikedPosts")
}

model Post {
  id       Int    @id @default(autoincrement())
  title    String
  author   User   @relation("WrittenPosts", fields: [authorId], references: [id])
  authorId Int
  likedBy  User[] @relation("LikedPosts")
}
```

```typescript
// Create post with author
const post = await prisma.post.create({
  data: {
    title: 'My Post',
    author: { connect: { id: 1 } },
  },
})

// Add likes
const post = await prisma.post.update({
  where: { id: 1 },
  data: {
    likedBy: {
      connect: [{ id: 2 }, { id: 3 }],
    },
  },
})

// Get user with both relations
const user = await prisma.user.findUnique({
  where: { id: 1 },
  include: {
    writtenPosts: true,
    likedPosts: true,
  },
})
```

## Filtering by Relations

```typescript
// Posts with at least one comment
const posts = await prisma.post.findMany({
  where: {
    comments: {
      some: {},
    },
  },
})

// Posts with no comments
const posts = await prisma.post.findMany({
  where: {
    comments: {
      none: {},
    },
  },
})

// Posts where all comments are approved
const posts = await prisma.post.findMany({
  where: {
    comments: {
      every: {
        approved: true,
      },
    },
  },
})

// Users with published posts containing "prisma"
const users = await prisma.user.findMany({
  where: {
    posts: {
      some: {
        published: true,
        title: {
          contains: 'prisma',
        },
      },
    },
  },
})
```