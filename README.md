[![make.fun](https://make.fun/badge.svg)](https://make.fun)

# The World Today — 19 November 2026

A one-page newspaper front page for Thursday 19 November 2026, drawn
entirely in code with Pillow shapes and text. No photos, no downloaded
assets, no network calls — every pixel comes from the scripts in this repo.

## What's on the page

- **Lead story — the Shenzhen summit.** Trump, Xi and Putin hold the
  first-ever trilateral meeting of the three nuclear powers, on the APEC
  sidelines in Shenzhen. Nuclear arsenals and the Iran war top the agenda;
  nobody expects a deal.
- **GTA VI launches worldwide** after 13 years, to near-perfect reviews:
  99 on Metacritic, with analysts projecting $3.2bn in sales by year-end.
- **Hakeem Jeffries wins the Democratic nomination** for Speaker of the
  US House, 251–11 in a secret ballot. If the full House confirms him on
  3 January, he becomes the first Black Speaker.
- **Strikes escalate in the Gulf.** Iranian drones hit US facilities at
  Ali Al-Salem base in Kuwait, after US jets struck an IRGC missile site
  on Qeshm Island; Gulf defences intercepted the attacks.
- **The EU proposes a €45bn loan for Ukraine** for 2027 — €25bn military
  and €20bn budget support — covering two-thirds of Kyiv's €70bn gap, to
  be repaid only once Russia pays reparations.
- **A demographic turning point.** Pew Research projects Islam becoming
  the world's largest religion by 2035: 2.57bn Muslims against 2.52bn
  Christians, driven by higher birth rates.

## Layout

A dark navy masthead with the date, a full-width hero card for the
Shenzhen summit, a 2×2 grid for the GTA VI, Jeffries, Gulf and EU
stories, and a full-width numbers strip for the Pew projection, with
two population bars and a big "2035".

## Run it

Render the poster:

```bash
python3 draw.py
```

That writes `entry.png` (1024×1024). Then ship it the way the grader
does:

```bash
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

`main.py` only copies `entry.png` byte-for-byte into the output
directory; it does no rendering and no network access. Running it twice
produces identical bytes.

## Files

- `draw.py` — draws the whole front page with Pillow primitives.
- `main.py` — copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (or `/output`).
- `entry.png` — the rendered 1024×1024 front page.
- `LICENSE` — MIT.

---

Built with [make.fun](https://make.fun/?ref=7tgjyx9m)
