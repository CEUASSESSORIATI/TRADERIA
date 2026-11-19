-- Migration complementar de desempenho/consistência (paper trading).
-- Executar depois do schema inicial no SQL Editor do Lovable Cloud.
-- Não concede permissões a anon/authenticated.

create index if not exists cti_quotes_observed_at_idx
  on public.cti_market_quotes (observed_at desc);

create index if not exists cti_trades_strategy_created_idx
  on public.cti_paper_trades (strategy, created_at desc);

create index if not exists cti_snapshots_strategy_captured_idx
  on public.cti_strategy_snapshots (strategy, captured_at desc);

create index if not exists cti_decisions_strategy_created_idx
  on public.cti_strategy_decisions (strategy, created_at desc);

alter table public.cti_market_quotes
  add constraint cti_quotes_positive_price check (price_brl > 0);

alter table public.cti_paper_trades
  add constraint cti_trades_positive_values check
    (quantity > 0 and price_brl > 0 and gross_brl >= 0 and fee_brl >= 0 and slippage_brl >= 0);

alter table public.cti_strategy_decisions
  add constraint cti_decisions_confidence_range check (confidence between 0 and 1);

alter table public.cti_strategy_decisions
  add constraint cti_decisions_valid_signal check (signal in ('buy','sell','hold'));

alter table public.cti_strategy_decisions
  add constraint cti_decisions_valid_strategy check
    (strategy in ('conservative','moderate','aggressive'));

-- Reforça a ausência de acesso via roles públicas da API.
revoke all on public.cti_market_quotes from anon, authenticated;
revoke all on public.cti_paper_trades from anon, authenticated;
revoke all on public.cti_strategy_snapshots from anon, authenticated;
revoke all on public.cti_strategy_decisions from anon, authenticated;
