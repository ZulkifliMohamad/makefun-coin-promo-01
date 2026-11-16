# LAUNCH-PLAN.md — Proof of Fun ($PROOF) on pump.fun

## Status

**Build only. The coin has NOT been launched.** Everything below is prepared
and validated; the launch itself, the GitHub repository, and the submission
are deliberately not done in this build (see "What still blocks submission"
in BUILD-REPORT.md).

## The coin

| Field | Exact value |
|---|---|
| Name | Proof of Fun |
| Ticker | PROOF |
| Website | https://make.fun/bounty/makefun-coin-promo-01 |
| Image | `assets/logo.png` (512x512 PNG, 13,046 bytes) |
| Wallet | 4o4WqB3G7im2t3Y1FFzaeeKFJ9zVtWQHNy3HY6gQArwo (linked, primary, on @steady-koala-56) |
| Description | Verbatim from `coin.json` (pump.fun's description limit is 1,000 chars — the text below is 711 characters, so it fits; paste it whole) |

Description (paste exactly):

> Proof that fun pays. $PROOF is the medal AI agents earn on make.fun — the arena where people and their AI agents build real programs, enter paid bounties, and get scored and ranked in the open. No pitch decks. No promises. Just code, judged live, winners paid in USDC.
>
> This coin was launched by an AI agent, with no human step, for the make.fun bounty: https://make.fun/bounty/makefun-coin-promo-01 — see the bounty, then go build something and take the prize yourself. If an agent can launch a coin to sell you on bounties, imagine what yours can build next.
>
> make.fun is a site where people and their AI agents build programs, enter them in paid competitions (bounties) and are scored and ranked in the open.

## Pre-launch checklist

- [x] Coin concept, name, ticker, description, website decided (`coin.json`).
- [x] Logo drawn and validated: 512x512 PNG, 13,046 bytes, 0.26 MP (limits: 5 MiB, 16 MP).
- [x] Packaging validated: `node scripts/prepare-launch.mjs` — all checks pass (see BUILD-REPORT.md).
- [x] Wallet linked to the make.fun account: verified via `wallet list` — linked, primary, added 2026-11-16T08:20:43Z.
- [x] Node.js 22.18+: verified v24.22.1.
- [ ] **SOL balance unknown.** Two public RPC balance lookups failed (mainnet-beta 429 rate limit; Ankr endpoint timed out). Before launching, check the balance of `4o4WqB3G7im2t3Y1FFzaeeKFJ9zVtWQHNy3HY6gQArwo` and fund it with enough SOL for pump.fun's launch fee plus the coin's first buy, plus ~0.0035 SOL kept aside for a prize claim if the entry wins. Never share the keypair or seed phrase with anyone.
- [ ] Entry window open: launch at or after 2026-11-15T06:00:00Z and before 2026-11-17T06:00:00Z. Do not launch early or late — a coin created outside the window is refused.
- [ ] Wallet connected on pump.fun (pump.fun requires a browser wallet connection; the agent cannot do this step from this VM — it needs the live browser or the operator's connected wallet session).

## Launch steps (pump.fun)

1. Open https://pump.fun/ and connect the wallet `4o4WqB3G7im2t3Y1FFzaeeKFJ9zVtWQHNy3HY6gQArwo` (the same wallet linked to the make.fun account — the house checks that the create transaction was signed by, or names as creator, a wallet linked to the submitting account).
2. Create a new coin with the exact values in the table above. Upload `assets/logo.png` as the image. Set the website to `https://make.fun/bounty/makefun-coin-promo-01` (scheme included). Paste the description verbatim.
3. Leave socials (X, Telegram) empty — the coin has none, and the judge reads missing links as "(none)".
4. Choose the first buy amount (small — the coin's price and trading are never judged; the buy exists only because pump.fun's flow asks for one).
5. Confirm and sign the create transaction with the linked wallet. **Record two values immediately:**
   - `mint` — the coin's mint address.
   - `create_signature` — the base58 signature of the transaction that created it.
6. Verify on pump.fun that the coin page shows the right name, ticker, logo, description (with the bounty link as plain text), and the website button pointing to make.fun.

## Post-launch steps (in order)

1. Fill in `LAUNCH.json` with the real `mint` and `create_signature` (replace both placeholders).
2. Run the program the way the grader does and confirm the copy:
   `mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts`
   then `diff LAUNCH.json out/LAUNCH.json` (must be identical).
3. Re-run `node scripts/prepare-launch.mjs` — the LAUNCH.json line must now say PASS.
4. Create the GitHub repository **after the competition opened** (2026-11-15T06:00:00Z), copy this directory in as the first commit, and:
   - Replace the `{owner}` / `{repo}` placeholders in the README badges with the real owner and repo name.
   - Add `.makefun/owner.json` — already present, wallet `4o4WqB3G7im2t3Y1FFzaeeKFJ9zVtWQHNy3HY6gQArwo` (only needed if the GitHub owner is not the account's GitHub login).
   - Set the GitHub About: description "`Proof of Fun ($PROOF) — the medal AI agents earn on make.fun. Built by an AI agent for make.fun's 'Launch a coin that sells make.fun' bounty, $1,000 in USDC.`", homepage `https://make.fun/bounty/makefun-coin-promo-01`, topics `makefun, ai-agents, bounties, growth`.
   - Keep the MIT `LICENSE`.
5. Bundle the transcripts of every agent session that built and launched the entry (kit CLI `bundle`, from the kit directory). This build session started after the competition opened; the launch session must be part of the bundle too, and the transcripts must show the coin being launched (thinking_launch check).
6. Run the pre-submit check from the kit directory:
   `node cli/makefun.mjs check --kit . --repo <repository> --transcripts transcripts.tar.gz`
   Fix every failure it names.
7. Submit (signs with the keypair — the wallet that signs is the payout wallet):
   `node cli/makefun.mjs submit --competition makefun-coin-promo-01 --repo-url https://github.com/<owner>/<repo> --commit <sha> --title "Proof of Fun" --bundle transcripts.tar.gz --keypair wallet.json`
8. Follow it: `node cli/makefun.mjs status --submission <id>`.

## Costs to expect

- pump.fun launch fee + first buy: paid in SOL from the launch wallet (amount depends on pump.fun at launch time; keep the wallet funded above that plus ~0.0035 SOL for a possible prize claim).
- No make.fun entry fee for this bounty (entry_fee: none).
- No fee is paid anywhere in this build.

## Risks and honest limits

- The launch needs a browser wallet connection on pump.fun, which this VM cannot do unattended; it is the one step that needs the operator's live session or a browser agent.
- The SOL balance is unverified (public RPC failures). Do not start the launch until the balance is confirmed.
- A coin created outside the entry window, from an unlinked wallet, or with a missing/wrong website or description link is refused outright and takes no reward — the checklist above exists to prevent exactly that.
