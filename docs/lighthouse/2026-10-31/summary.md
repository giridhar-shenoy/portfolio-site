# Lighthouse, 31 Oct 2026

Lighthouse 12.6.0, mobile form factor (default simulated throttling), headless Chrome
(`Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/156.0.0.0 Safari/537.36`), against `python3 -m http.server -d public 8765` on this laptop. Run with
`npx --yes lighthouse@12.6.0 <url> --chrome-flags=--headless=new --output=json --output=html`.
The HTML reports are kept; the JSON copies were deleted after this table was made from them.

Targets: Performance ≥ 95, Accessibility 100, Best Practices ≥ 95, SEO ≥ 95.

| Page | Performance | Accessibility | Best Practices | SEO |
|---|---|---|---|---|
| 404 | 100 | 95 | 96 | 100 |
| index | 100 | 100 | 100 | 100 |
| repos | 100 | 100 | 100 | 100 |
| work/bot-and-brew | 100 | 100 | 100 | 100 |
| work/orangewood-controls | 100 | 100 | 100 | 100 |

404 locally is below target on Accessibility and Best Practices only because its URLs are
absolute to `/portfolio-site/` (GitHub Pages serves it for missing paths at any depth): served
from `public/` they 404, so the stylesheet is missing (unstyled tap targets) and the console shows
the failed requests. On the deployed site those URLs resolve.

repos.report.html was re-run at 09:01, after the table fix in 287be21: 100 / 100 / 100 / 100.
