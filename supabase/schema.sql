-- Ragnarok Zero Wiki - Supabase schema
-- Run this file in the Supabase SQL Editor after creating the project.

create extension if not exists pgcrypto;

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  email text,
  role text not null default 'editor' check (role in ('admin','editor')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.wiki_pages (
  id uuid primary key default gen_random_uuid(),
  slug text not null unique,
  title_en text not null,
  title_fr text,
  content_en text not null default '',
  content_fr text not null default '',
  section text not null default 'guide',
  verification_status text not null default 'unverified' check (verification_status in ('verified','partial','unverified')),
  published boolean not null default true,
  created_by uuid references auth.users(id) on delete set null,
  updated_by uuid references auth.users(id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.items (
  id bigint primary key,
  aegis_name text,
  name_en text not null,
  name_fr text,
  item_type text,
  subtype text,
  attack integer,
  defense integer,
  weight numeric,
  slots integer,
  required_level integer,
  description_en text,
  description_fr text,
  image_path text,
  verification_status text not null default 'unverified' check (verification_status in ('verified','partial','unverified')),
  source text not null default 'client',
  published boolean not null default true,
  updated_by uuid references auth.users(id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.monsters (
  id bigint primary key,
  name_en text not null,
  name_fr text,
  level integer,
  hp bigint,
  race text,
  element text,
  size text,
  base_exp bigint,
  job_exp bigint,
  image_path text,
  description_en text,
  description_fr text,
  verification_status text not null default 'unverified' check (verification_status in ('verified','partial','unverified')),
  source text not null default 'client',
  published boolean not null default true,
  updated_by uuid references auth.users(id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.skills (
  id bigint primary key,
  technical_name text,
  name_en text not null,
  name_fr text,
  max_level integer,
  description_en text,
  description_fr text,
  verification_status text not null default 'unverified' check (verification_status in ('verified','partial','unverified')),
  source text not null default 'client',
  published boolean not null default true,
  updated_by uuid references auth.users(id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.revisions (
  id bigint generated always as identity primary key,
  entity_type text not null,
  entity_id text not null,
  data jsonb not null,
  changed_by uuid references auth.users(id) on delete set null,
  created_at timestamptz not null default now()
);

alter table public.profiles enable row level security;
alter table public.wiki_pages enable row level security;
alter table public.items enable row level security;
alter table public.monsters enable row level security;
alter table public.skills enable row level security;
alter table public.revisions enable row level security;

create or replace function public.is_wiki_editor()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1 from public.profiles
    where id = auth.uid() and role in ('admin','editor')
  );
$$;

create policy "Public can read published pages" on public.wiki_pages for select using (published = true or public.is_wiki_editor());
create policy "Editors manage pages" on public.wiki_pages for all using (public.is_wiki_editor()) with check (public.is_wiki_editor());

create policy "Public can read published items" on public.items for select using (published = true or public.is_wiki_editor());
create policy "Editors manage items" on public.items for all using (public.is_wiki_editor()) with check (public.is_wiki_editor());

create policy "Public can read published monsters" on public.monsters for select using (published = true or public.is_wiki_editor());
create policy "Editors manage monsters" on public.monsters for all using (public.is_wiki_editor()) with check (public.is_wiki_editor());

create policy "Public can read published skills" on public.skills for select using (published = true or public.is_wiki_editor());
create policy "Editors manage skills" on public.skills for all using (public.is_wiki_editor()) with check (public.is_wiki_editor());

create policy "Users can read own profile" on public.profiles for select using (id = auth.uid());
create policy "Admins can manage profiles" on public.profiles for all using (
  exists (select 1 from public.profiles p where p.id = auth.uid() and p.role = 'admin')
) with check (
  exists (select 1 from public.profiles p where p.id = auth.uid() and p.role = 'admin')
);

create policy "Editors can read revisions" on public.revisions for select using (public.is_wiki_editor());
create policy "Editors can insert revisions" on public.revisions for insert with check (public.is_wiki_editor());
