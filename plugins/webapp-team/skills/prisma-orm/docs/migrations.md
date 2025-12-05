# Prisma Migrations

Complete guide to database migrations with Prisma Migrate.

## Overview

Prisma Migrate creates and manages database schema changes through version-controlled SQL migration files.

```
prisma/
├── schema.prisma          # Your data model
└── migrations/
    ├── 20240101000000_init/
    │   └── migration.sql
    ├── 20240115000000_add_posts/
    │   └── migration.sql
    └── migration_lock.toml
```

## Development Workflow

### Creating Migrations

```bash
# Create and apply migration
npx prisma migrate dev --name init

# Create migration without applying (review first)
npx prisma migrate dev --name add_user_profile --create-only
```

### What `migrate dev` Does

1. Creates new migration file based on schema changes
2. Applies pending migrations to database
3. Regenerates Prisma Client
4. Triggers generators (if configured)

### Example Workflow

```bash
# 1. Modify schema.prisma
# Add a new model or field

# 2. Create migration
npx prisma migrate dev --name add_user_settings

# 3. Review generated SQL (optional but recommended)
cat prisma/migrations/20240115_add_user_settings/migration.sql

# 4. Continue development...
```

## Production Deployment

### Apply Migrations

```bash
# Apply all pending migrations
npx prisma migrate deploy
```

### Deployment Checklist

```markdown
[ ] Backup database before migration
[ ] Test migration on staging environment
[ ] Review migration SQL for performance impact
[ ] Plan for rollback if needed
[ ] Schedule maintenance window for large migrations
[ ] Monitor migration progress
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Deploy Database Migrations
  run: npx prisma migrate deploy
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

## Migration Commands Reference

| Command | Purpose | Environment |
|---------|---------|-------------|
| `prisma migrate dev` | Create and apply migrations | Development |
| `prisma migrate deploy` | Apply pending migrations | Production |
| `prisma migrate reset` | Reset database and apply all migrations | Development |
| `prisma migrate resolve` | Mark migration as applied/rolled back | Production |
| `prisma migrate status` | Check migration status | Any |
| `prisma migrate diff` | Generate SQL diff between states | Any |

## Adding Prisma to Existing Database

### Baseline Migration

```bash
# 1. Pull existing schema
npx prisma db pull

# 2. Create migrations directory
mkdir -p prisma/migrations/0_init

# 3. Generate baseline SQL
npx prisma migrate diff \
  --from-empty \
  --to-schema-datamodel prisma/schema.prisma \
  --script > prisma/migrations/0_init/migration.sql

# 4. Mark baseline as applied
npx prisma migrate resolve --applied 0_init

# 5. Future migrations will work normally
npx prisma migrate dev --name add_new_feature
```

## Schema Changes & Generated SQL

### Adding a Table

```prisma
// schema.prisma
model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  createdAt DateTime @default(now())
}
```

Generated SQL:
```sql
-- CreateTable
CREATE TABLE "Post" (
    "id" SERIAL NOT NULL,
    "title" TEXT NOT NULL,
    "content" TEXT,
    "published" BOOLEAN NOT NULL DEFAULT false,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Post_pkey" PRIMARY KEY ("id")
);
```

### Adding a Column

```prisma
model User {
  id    Int     @id @default(autoincrement())
  email String  @unique
  name  String?
+ bio   String? // New optional field
}
```

Generated SQL:
```sql
-- AlterTable
ALTER TABLE "User" ADD COLUMN "bio" TEXT;
```

### Adding Required Column (with default)

```prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
+ role      String   @default("USER") // Required with default
}
```

Generated SQL:
```sql
-- AlterTable
ALTER TABLE "User" ADD COLUMN "role" TEXT NOT NULL DEFAULT 'USER';
```

### Adding Index

```prisma
model Post {
  id       Int    @id @default(autoincrement())
  authorId Int
  title    String

+ @@index([authorId])
+ @@index([title])
}
```

Generated SQL:
```sql
-- CreateIndex
CREATE INDEX "Post_authorId_idx" ON "Post"("authorId");
CREATE INDEX "Post_title_idx" ON "Post"("title");
```

### Adding Relation

```prisma
model User {
  id    Int    @id @default(autoincrement())
  email String @unique
+ posts Post[]
}

model Post {
  id       Int    @id @default(autoincrement())
  title    String
+ author   User   @relation(fields: [authorId], references: [id])
+ authorId Int
}
```

Generated SQL:
```sql
-- AlterTable
ALTER TABLE "Post" ADD COLUMN "authorId" INTEGER NOT NULL;

-- AddForeignKey
ALTER TABLE "Post" ADD CONSTRAINT "Post_authorId_fkey"
  FOREIGN KEY ("authorId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
```

## Handling Data Migrations

### Backfilling Data

For complex migrations requiring data transformation:

```bash
# 1. Create migration for schema change
npx prisma migrate dev --name add_full_name --create-only

# 2. Edit migration to include data backfill
```

Edit `migration.sql`:
```sql
-- AlterTable
ALTER TABLE "User" ADD COLUMN "fullName" TEXT;

-- Backfill data
UPDATE "User" SET "fullName" = "firstName" || ' ' || "lastName";

-- Make column required after backfill
ALTER TABLE "User" ALTER COLUMN "fullName" SET NOT NULL;
```

```bash
# 3. Apply migration
npx prisma migrate dev
```

### Custom Migration Script

For complex data transformations:

```typescript
// scripts/migrate-data.ts
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function main() {
  // Get all users needing migration
  const users = await prisma.user.findMany({
    where: { fullName: null },
  })

  // Update in batches
  const batchSize = 100
  for (let i = 0; i < users.length; i += batchSize) {
    const batch = users.slice(i, i + batchSize)

    await prisma.$transaction(
      batch.map(user =>
        prisma.user.update({
          where: { id: user.id },
          data: { fullName: `${user.firstName} ${user.lastName}` },
        })
      )
    )

    console.log(`Migrated ${Math.min(i + batchSize, users.length)}/${users.length}`)
  }
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect())
```

## Troubleshooting

### Migration Drift

When database schema doesn't match migration history:

```bash
# Check status
npx prisma migrate status

# If drift detected, options:
# 1. Reset database (development only)
npx prisma migrate reset

# 2. Mark migration as applied (if manually applied)
npx prisma migrate resolve --applied migration_name

# 3. Mark migration as rolled back
npx prisma migrate resolve --rolled-back migration_name
```

### Failed Migration

```bash
# 1. Check what failed
npx prisma migrate status

# 2. Fix the issue in your database manually if needed

# 3. Mark as resolved
npx prisma migrate resolve --applied failed_migration_name

# Or rollback
npx prisma migrate resolve --rolled-back failed_migration_name
```

### Shadow Database Issues

Prisma uses a shadow database for development migrations:

```bash
# If shadow database issues occur
npx prisma migrate dev --create-only

# Configure shadow database URL if needed
# In schema.prisma:
datasource db {
  provider          = "postgresql"
  url               = env("DATABASE_URL")
  shadowDatabaseUrl = env("SHADOW_DATABASE_URL")
}
```

## Best Practices

### 1. Always Review Generated SQL

```bash
npx prisma migrate dev --name my_change --create-only
cat prisma/migrations/*/migration.sql
# Review, then apply
npx prisma migrate dev
```

### 2. Use Descriptive Migration Names

```bash
# Good
npx prisma migrate dev --name add_user_profile_table
npx prisma migrate dev --name add_email_index_to_users
npx prisma migrate dev --name remove_deprecated_fields

# Bad
npx prisma migrate dev --name update
npx prisma migrate dev --name fix
```

### 3. Test on Copy of Production Data

```bash
# Dump production (sanitized)
pg_dump production_db > dump.sql

# Restore to staging
psql staging_db < dump.sql

# Test migration
DATABASE_URL=staging_url npx prisma migrate deploy
```

### 4. Handle Large Tables Carefully

For tables with millions of rows:

```sql
-- Instead of:
ALTER TABLE "LargeTable" ADD COLUMN "newCol" TEXT NOT NULL DEFAULT 'value';

-- Do:
-- Step 1: Add nullable column
ALTER TABLE "LargeTable" ADD COLUMN "newCol" TEXT;

-- Step 2: Backfill in batches (separate script)

-- Step 3: Add constraint
ALTER TABLE "LargeTable" ALTER COLUMN "newCol" SET NOT NULL;
```

### 5. Use Indexes Wisely

```prisma
model Post {
  id       Int    @id
  authorId Int
  status   String
  title    String

  // Good: Index on foreign key (used in JOINs)
  @@index([authorId])

  // Good: Compound index for common queries
  @@index([status, authorId])

  // Avoid: Index on rarely filtered columns
  // @@index([title]) // Only if you filter by title often
}
```

### 6. Version Control Migrations

```gitignore
# .gitignore
# DO NOT ignore migrations folder
# prisma/migrations/ <- Keep this tracked

# Only ignore development database
*.db
*.sqlite
```

## Squashing Migrations

Combine multiple migrations into one (development only):

```bash
# 1. Reset and recreate
npx prisma migrate reset

# 2. Delete all migrations
rm -rf prisma/migrations/*

# 3. Create fresh migration
npx prisma migrate dev --name init
```

**Warning**: Only do this before deploying to production. Never squash migrations that have been applied to production.
