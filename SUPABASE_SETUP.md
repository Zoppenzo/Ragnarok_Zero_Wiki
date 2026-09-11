# Supabase setup — Ragnarok Zero Wiki

## 1. Create the project
Create a Supabase project for the wiki.

## 2. Create the database
Open Supabase SQL Editor and run the complete file:

`supabase/schema.sql`

## 3. Create the first admin account
In Supabase Authentication, create/sign up the account that will administer the wiki.
Copy its UUID, then run this in SQL Editor (replace the two values):

```sql
insert into public.profiles (id, email, role)
values ('USER_UUID_HERE', 'YOUR_EMAIL_HERE', 'admin')
on conflict (id) do update set role = 'admin', email = excluded.email;
```

## 4. Connect the website
Open:

`assets/supabase-config.js`

Replace:

- `YOUR_SUPABASE_PROJECT_URL`
- `YOUR_SUPABASE_ANON_KEY`

Use only the public project URL and the browser-safe anon/publishable key.
Never commit a `service_role` secret.

## 5. Admin URL
Once configured, open:

`/admin/`

Log in with the admin account created above.

## Current admin features
- secure Supabase authentication
- admin/editor role check
- list/search pages
- list/search items
- list/search monsters
- list/search skills
- create records
- edit records
- publish/unpublish records
- verification status fields

## Next migration step
The existing static data in `index.html` and `assets/client-*` can then be imported progressively into Supabase while keeping the public wiki working during the migration.
