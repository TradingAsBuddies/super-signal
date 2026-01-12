import io, sys
from super_signal.models import StockInfo, RiskAnalysis
import super_signal.fetchers.yahoo_finance as yf_fetch
import super_signal.formatters.display as disp

# Patch fetch_vix_value
orig = getattr(yf_fetch, 'fetch_vix_value', None)
setattr(yf_fetch, 'fetch_vix_value', lambda: 99.55)

si = StockInfo(ticker='FAKE', long_name='Fake Corp', regular_market_price=10.0)
si.directors = []
ra = RiskAnalysis(ticker='FAKE')

buf = io.StringIO()
sys_stdout = sys.stdout
sys.stdout = buf
try:
    disp.print_stock_summary(si, ra, float_threshold=3_000_000)
finally:
    sys.stdout = sys_stdout
    if orig is not None:
        setattr(yf_fetch, 'fetch_vix_value', orig)

out = buf.getvalue()
print('---OUTPUT START---')
print(out)
print('---OUTPUT END---')
print('Contains VIX?', 'VIX' in out)
print('Contains 99.55?', '99.55' in out)
