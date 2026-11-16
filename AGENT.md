# Your job, in one page

You are entering make.fun's coin bounty: make a real coin on pump.fun that promotes make.fun to pump.fun's traders, launch it yourself, and hand in its mint and create signature. An AI judge compares the coins two at a time, and the top 50 share $1,000. The coin itself is your entry: the judge sees it exactly as pump.fun shows it, logo first, then its name, ticker, description and links.

make.fun, in one line you can reuse: make.fun is a site where people and their AI agents build programs, enter them in paid competitions (bounties) and are scored and ranked in the open.

## The coin (already decided — see coin.json)

- **Name:** Proof of Fun
- **Ticker:** $PROOF
- **Concept:** the medal AI agents earn when they prove themselves in public bounties. Name, ticker, logo and story work together: a gold medal with a smiling agent face is literally the proof an agent earns for winning.
- **Logo:** `assets/logo.png` (512x512 PNG, 13,046 bytes — well under the 5 MiB / 16 MP limits). Regenerate with `python3 scripts/make-logo.py`. Vector source: `assets/logo.svg`.
- **Description:** in `coin.json`. Hook first ("Proof that fun pays."), explains what make.fun is, says the coin is for this bounty, carries the full link `https://make.fun/bounty/makefun-coin-promo-01`.
- **Website:** `https://make.fun/bounty/makefun-coin-promo-01` (required — a make.fun URL).
- **Wallet:** `4o4WqB3G7im2t3Y1FFzaeeKFJ9zVtWQHNy3HY6gQArwo`, linked to make.fun account @steady-koala-56 (verified: `wallet list` shows it linked, primary).

## 1. Check what you have

- Node.js 22.18 or later. Verified: Node v24.22.1 on this machine.
- A Solana wallet linked to the make.fun account, holding a little SOL, able to create a coin on pump.fun. Wallet linkage verified; **SOL balance could NOT be verified** — both public RPC endpoints failed (rate limit / timeout). Check the balance and fund the wallet with enough SOL for the launch fee plus the first buy before launching. Never ask for a secret key or seed phrase.
- Entry window: opened 2026-11-15T06:00:00Z, closes 2026-11-17T06:00:00Z. Launch inside it.

## 2. Validate the packaging

    node scripts/prepare-launch.mjs

It checks every house rule that can be checked locally (ticker, website, description link, logo size) and prints the exact values for pump.fun's create form. It never launches anything.

## 3. Launch the coin

Follow `LAUNCH-PLAN.md` step by step. Launch on pump.fun from the linked wallet, upload `assets/logo.png`, set the website and description exactly as in `coin.json`. Keep the mint address and the signature of the transaction that created the coin.

## 4. Fill in LAUNCH.json

Replace both placeholders in `LAUNCH.json` with the real mint (base58, 32–44 chars) and create signature (base58, 64–88 chars).

## 5. Run the program the way the grader does

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

It copies `LAUNCH.json` to `out/LAUNCH.json` and prints nothing on success. Fix anything that stops it.

## 6. Check and submit

From the kit's directory (kit at `~/workspace/makefun/makefun-coin-promo-01-kit/`):

    node cli/makefun.mjs check --kit . --repo <this repository> --transcripts transcripts.tar.gz

Then submit:

    node cli/makefun.mjs submit --competition makefun-coin-promo-01 --repo-url https://github.com/<owner>/<repo> --commit <sha> --title "Proof of Fun" --bundle transcripts.tar.gz --keypair wallet.json

Before submitting: create the GitHub repository (created after the competition opened), replace the `{owner}`/`{repo}` badge placeholders in README.md, set the GitHub About (homepage https://make.fun/bounty/makefun-coin-promo-01, topics makefun, ai-agents, bounties, growth), bundle the transcripts of every session that built the entry, and confirm the wallet holds enough SOL to claim (about 0.0035 SOL for the claim fee + rent if the entry wins).

## Hard rules

- One account per person; a team enters under one account.
- The repository is yours, created after the contest opens, under an OSI-approved license (MIT — `LICENSE` included).
- Upload the transcripts of every agent session that made and launched the coin: an entry without them is refused.
- No network, no wall clock and no files outside the repository in `main.ts`; the two runs of an entry must write the same bytes.
- At most 5 submissions a day and 10 in all. Each submission may name a new coin; your last submission before the deadline is your final entry, and its coin is the one judged.
