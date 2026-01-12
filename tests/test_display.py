from super_signal.models import StockInfo, RiskAnalysis
from super_signal.formatters.display import print_stock_summary
from super_signal.config import DISPLAY_CONFIG


def test_print_stock_summary_includes_vix(monkeypatch, capsys):
    # Create a minimal StockInfo
    si = StockInfo(ticker="FAKE", long_name="Fake Corp", regular_market_price=10.0)
    # Ensure directors list exists
    si.directors = []

    ra = RiskAnalysis(ticker="FAKE")

    # Patch fetch_vix_value to return a known value
    import super_signal.fetchers.yahoo_finance as yf_fetch

    monkeypatch.setattr(yf_fetch, "fetch_vix_value", lambda: 99.55)

    # Call the formatter
    print_stock_summary(si, ra, float_threshold=3_000_000)

    captured = capsys.readouterr()
    out = captured.out

    assert "VIX" in out
    assert "99.55" in out
