# CAG actual spending (2024-25)

The Reserve Bank publishes state spending by area about two years late. For 2024-25 the app uses the CAG's audited
Finance Accounts (Volume II) for Andhra Pradesh and Telangana instead.

How the numbers are made:
1. `pdftotext -layout` on Finance Accounts Volume II (Statements 15, 16 and 18).
2. `read_finance_accounts.py <txt> <heads.json>` reads every major-head total: revenue (2xxx/3xxx), capital outlay
   (4xxx/5xxx) and loans disbursed (6xxx/7xxx; 6003/6004 are the state's own borrowing and are left out).
3. `rbi_heads.py <heads.json> ap|ts` adds them up by the same major heads the Reserve Bank uses for each area, and prints
   the 2023-24 check: the same method on the 2023-24 column reproduces the Reserve Bank's 2023-24 figures exactly for
   most areas (small gaps are loans, which that column does not include).
4. Totals come from the CAG's Accounts at a Glance 2024-25: revenue + capital + loans disbursed
   (AP 2,27,961 + 16,141 + 5,032; Telangana 1,77,224 + 36,072 + 4,855, in ₹ crore).

Result: `web/data/cag-2024-25.json` (₹ crore), also built into the app as `CAG`. The app shows it only where the Reserve
Bank has not published that year yet.
