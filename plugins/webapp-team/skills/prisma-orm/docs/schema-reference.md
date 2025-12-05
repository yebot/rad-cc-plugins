# Prisma Schema Reference

Complete reference for Prisma schema syntax, data types, and attributes.

## Schema File Structure

The Prisma schema file (`prisma/schema.prisma`) contains three main sections:

```prisma
// 1. Data Source - Database connection
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// 2. Generator - Client generation settings
generator client {
  provider = "prisma-client-js"
  output   = "./generated/client"
}

// 3. Data Model - Your application models
model User {
  id    Int    @id @default(autoincrement())
  email String @unique
  name  String?
}
```

## Data Source Configuration

### Supported Providers

| Provider | Value |
|----------|-------|
| PostgreSQL | `postgresql` |
| MySQL | `mysql` |
| SQLite | `sqlite` |
| SQL Server | `sqlserver` |
| MongoDB | `mongodb` |
| CockroachDB | `cockroachdb` |

### Connection URL Format

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
  // Or direct URL (not recommended for production)
  // url = "postgresql://user:password@localhost:5432/mydb?schema=public"
}
```

**PostgreSQL URL Format:**
```
postgresql://USER:PASSWORD@HOST:PORT/DATABASE?schema=SCHEMA
```

**MySQL URL Format:**
```
mysql://USER:PASSWORD@HOST:PORT/DATABASE
```

**SQLite URL Format:**
```
file:./dev.db
```

## Generator Configuration

```prisma
generator client {
  provider      = "prisma-client-js"
  output        = "./generated/client"    // Custom output location
  binaryTargets = ["native", "linux-musl"] // For deployment
  engineType    = "client"                  // Edge-compatible (no binary)
}
```

## Scalar Data Types

| Prisma Type | PostgreSQL | MySQL | SQLite | MongoDB |
|-------------|------------|-------|--------|---------|
| `String` | text | varchar(191) | TEXT | String |
| `Boolean` | boolean | tinyint(1) | INTEGER | Bool |
| `Int` | integer | int | INTEGER | Int |
| `BigInt` | bigint | bigint | INTEGER | Long |
| `Float` | double precision | double | REAL | Double |
| `Decimal` | decimal(65,30) | decimal(65,30) | DECIMAL | Decimal128 |
| `DateTime` | timestamp(3) | datetime(3) | DATETIME | Timestamp |
| `Json` | jsonb | json | - | Object |
| `Bytes` | bytea | longblob | BLOB | BinData |

## Field Modifiers

```prisma
model Example {
  required  String    // Required field
  optional  String?   // Optional field (can be null)
  list      String[]  // Array/list of values
}
```

## Field Attributes (@)

### @id - Primary Key

```prisma
model User {
  id Int @id @default(autoincrement())  // Auto-increment integer
}

model Post {
  id String @id @default(uuid())  // UUID string
}

model Item {
  id String @id @default(cuid())  // CUID string
}
```

### @unique - Unique Constraint

```prisma
model User {
  id    Int    @id @default(autoincrement())
  email String @unique
}
```

### @default - Default Values

```prisma
model Post {
  id        Int      @id @default(autoincrement())
  uuid      String   @default(uuid())
  cuid      String   @default(cuid())
  createdAt DateTime @default(now())
  published Boolean  @default(false)
  views     Int      @default(0)
  role      Role     @default(USER)
}
```

**Available Default Functions:**
- `autoincrement()` - Auto-incrementing integer
- `uuid()` - UUID v4 string
- `cuid()` - CUID string
- `now()` - Current timestamp
- `dbgenerated()` - Database-generated value

### @updatedAt - Auto-Update Timestamp

```prisma
model Post {
  id        Int      @id @default(autoincrement())
  updatedAt DateTime @updatedAt  // Auto-updates on every change
}
```

### @map - Column Name Mapping

```prisma
model User {
  id        Int    @id @default(autoincrement())
  firstName String @map("first_name")  // Maps to snake_case column
}
```

### @db - Native Database Types

```prisma
model Product {
  id          Int     @id @default(autoincrement())
  name        String  @db.VarChar(255)
  price       Decimal @db.Decimal(10, 2)
  description String  @db.Text
  data        Json    @db.JsonB  // PostgreSQL JSONB
}
```

### @relation - Relationship Definition

```prisma
model Post {
  id       Int  @id @default(autoincrement())
  author   User @relation(fields: [authorId], references: [id])
  authorId Int
}
```

### @ignore - Exclude from Client

```prisma
model User {
  id           Int    @id
  internalData String @ignore  // Not accessible in Prisma Client
}
```

## Model Attributes (@@)

### @@id - Composite Primary Key

```prisma
model OrderItem {
  orderId   Int
  productId Int
  quantity  Int

  @@id([orderId, productId])
}
```

### @@unique - Compound Unique Constraint

```prisma
model User {
  firstName String
  lastName  String
  email     String

  @@unique([firstName, lastName])
  @@unique([email])
}
```

### @@index - Database Index

```prisma
model Post {
  id       Int    @id
  title    String
  authorId Int
  status   String

  @@index([authorId])
  @@index([status, authorId])
  @@index([title], type: Hash)  // Hash index (PostgreSQL)
}
```

### @@map - Table Name Mapping

```prisma
model User {
  id Int @id

  @@map("users")  // Maps to 'users' table
}
```

### @@schema - Multi-Schema Support

```prisma
model User {
  id Int @id

  @@schema("auth")  // PostgreSQL schema
}
```

### @@ignore - Exclude Entire Model

```prisma
model InternalLog {
  id      Int    @id
  message String

  @@ignore  // Model not included in Prisma Client
}
```

## Enums

```prisma
enum Role {
  USER
  ADMIN
  MODERATOR
}

enum Status {
  DRAFT
  PUBLISHED
  ARCHIVED
}

model User {
  id   Int  @id @default(autoincrement())
  role Role @default(USER)
}

model Post {
  id     Int    @id @default(autoincrement())
  status Status @default(DRAFT)
}
```

## Comments

```prisma
// Single-line comment

/// Documentation comment (included in generated client)
model User {
  /// The user's unique identifier
  id Int @id @default(autoincrement())

  /// The user's email address
  email String @unique
}

/*
  Multi-line comment
  Not included in generated client
*/
```

## Environment Variables

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

**.env file:**
```env
DATABASE_URL="postgresql://user:password@localhost:5432/mydb?schema=public"
```

## Complete Example Schema

```prisma
generator client {
  provider = "prisma-client-js"
  output   = "./generated/client"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

enum Role {
  USER
  ADMIN
}

enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}

model User {
  id        Int       @id @default(autoincrement())
  email     String    @unique
  name      String?
  role      Role      @default(USER)
  posts     Post[]
  profile   Profile?
  comments  Comment[]
  createdAt DateTime  @default(now())
  updatedAt DateTime  @updatedAt

  @@index([email])
  @@map("users")
}

model Profile {
  id     Int     @id @default(autoincrement())
  bio    String? @db.Text
  avatar String?
  user   User    @relation(fields: [userId], references: [id], onDelete: Cascade)
  userId Int     @unique

  @@map("profiles")
}

model Post {
  id        Int        @id @default(autoincrement())
  title     String     @db.VarChar(255)
  content   String?    @db.Text
  status    PostStatus @default(DRAFT)
  author    User       @relation(fields: [authorId], references: [id])
  authorId  Int
  comments  Comment[]
  tags      Tag[]
  createdAt DateTime   @default(now())
  updatedAt DateTime   @updatedAt

  @@index([authorId])
  @@index([status])
  @@map("posts")
}

model Comment {
  id        Int      @id @default(autoincrement())
  content   String   @db.Text
  post      Post     @relation(fields: [postId], references: [id], onDelete: Cascade)
  postId    Int
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int
  createdAt DateTime @default(now())

  @@index([postId])
  @@index([authorId])
  @@map("comments")
}

model Tag {
  id    Int    @id @default(autoincrement())
  name  String @unique
  posts Post[]

  @@map("tags")
}
```