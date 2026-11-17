-- Execute no SQL Editor do projeto Lovable Cloud/Supabase.
-- Esta migration cria somente tabelas de telemetria do CEU Trader.
-- A service role deve permanecer exclusivamente no backend Windows.
create table if not exists public.cti_market_quotes (
  id bigint generated always as identity primary key,
  symbol text not null,
  price_brl numeric(24,8) not null,
  source text not null,
  observed_at timestamptz not null
);

create table if not exists public.cti_paper_trades (
  id uuid primary key,
  strategy text not null check (strategy in ('conservative','moderate','aggressive')),
  side text not null check (side in ('buy','sell')),
  symbol text not null,
  quantity numeric(28,12) not null,
  price_brl numeric(24,8) not null,
  gross_brl numeric(24,8) not null,
  fee_brl numeric(24,8) not null,
  slippage_brl numeric(24,8) not null,
  realized_pnl_brl numeric(24,8) not null default 0,
  created_at timestamptz not null
);

create table if not exists public.cti_strategy_snapshots (
  id bigint generated always as identity primary key,
  strategy text not null check (strategy in ('conservative','moderate','aggressive')),
  initial_capital_brl numeric(24,8) not null,
  cash_brl numeric(24,8) not null,
  btc_quantity numeric(28,12) not null,
  equity_brl numeric(24,8) not null,
  realized_pnl_brl numeric(24,8) not null,
  daily_realized_pnl_brl numeric(24,8) not null,
  unrealized_pnl_brl numeric(24,8) not null,
  return_pct numeric(12,6) not null,
  peak_equity_brl numeric(24,8) not null,
  drawdown_pct numeric(12,6) not null,
  halted boolean not null default false,
  captured_at timestamptz not null default now()
);

create table if not exists public.cti_strategy_decisions (
  id bigint generated always as identity primary key,
  strategy text not null,
  signal text not null,
  confidence numeric(5,4) not null,
  reason text not null,
  price_brl numeric(24,8) not null,
  risk_allowed boolean not null,
  risk_reason text not null,
  created_at timestamptz not null
);

-- Para instalação inicial, habilite RLS e não conceda acesso público.
alter table public.cti_market_quotes enable row level security;
alter table public.cti_paper_trades enable row level security;
alter table public.cti_strategy_snapshots enable row level security;
alter table public.cti_strategy_decisions enable row level security;
