# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/fauzinfau4/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/fauzinfau4/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Sum up 19 November's world news in one image: the program writes one image of the day's news (Thursday 19 November 2026) — the first-ever Trump–Xi–Putin trilateral in Shenzhen, GTA VI launches worldwide to near-perfect reviews, Democrats nominate Hakeem Jeffries to be the first Black Speaker, Iran strikes US bases in Kuwait and Bahrain, the EU offers Ukraine a €45bn loan to be repaid from Russian reparations, and Pew projects Islam becoming the world's largest religion by 2035. An AI judge compares the images two at a time, and the 50 best win rates share $250.

## The poster

A newspaper-style front page drawn entirely with Pillow primitives — no downloaded assets, no network, fully deterministic. A masthead names the day, a full-width hero covers the Shenzhen summit, four cards cover gaming, US politics, the Gulf war and Ukraine, and a numbers strip visualises Pew's 2035 projections (2.57bn Muslims vs 2.52bn Christians).

## Run it

```sh
python3 draw.py            # re-render entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=7tgjyx9m&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
