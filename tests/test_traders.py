from app.traders import TraderArena

def test_arena_has_three_independent_profiles():
    a=TraderArena()
    assert len(a.profiles)==3
    assert len({p.strategy for p in a.profiles})==3

def test_tick_is_paper_only():
    a=TraderArena()
    out=a.tick("TEST",100)
    assert out["mode"]=="PAPER"
    assert out["live_orders_enabled"] is False
    assert len(out["traders"])==3

def test_profiles_have_independent_history():
    a=TraderArena()
    a.tick("TEST",100)
    assert all(len(p.history)==1 for p in a.profiles)
