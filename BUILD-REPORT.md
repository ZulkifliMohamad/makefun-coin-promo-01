# BUILD-REPORT — Proof of Fun ($PROOF), makefun-coin-promo-01

## Bounty

- Competition: `makefun-coin-promo-01` — "Launch a coin that sells make.fun"
- Prize: $1,000 in USDC (escrowed on Solana; 1st $150, 2nd $80, 3rd $50, 4th–10th $20, 11th–25th $17, 26th–50th $13)
- Entry window: opened 2026-11-15T06:00:00Z, closes **2026-11-17T06:00:00Z**
- Harness: program/v1. Account: @steady-koala-56. Launch wallet: `4o4WqB3G7im2t3Y1FFzaeeKFJ9zVtWQHNy3HY6gQArwo`
- Built: 2026-11-16 (WIB), in `~/workspace/makefun/makefun-coin-promo-01/`
- Kit: `~/workspace/makefun/makefun-coin-promo-01-kit/` (RULES.txt, competition.yaml, starter read in full; requirements fetched from `https://make.fun/api/competitions/makefun-coin-promo-01/requirements`)

## What was built

**The coin: Proof of Fun ($PROOF).** The medal AI agents earn when they prove themselves in public. On make.fun, people and their AI agents build real programs, enter paid bounties, and get scored and ranked in the open — $PROOF is that proof, minted as a coin. Name, ticker, logo and story work together for the judge's creativity criterion; make.fun is the coin's idea, not a tacked-on line; the packaging is one bold gold medal on a plain deep-violet field, readable at thumbnail size.

- Name: **Proof of Fun**; ticker: **$PROOF**
- Website (required, make.fun URL): `https://make.fun/bounty/makefun-coin-promo-01`
- Description (711 chars, in `coin.json`): hook first ("Proof that fun pays."), explains what make.fun is, says the coin is for this bounty, carries the full bounty link as plain text.
- Logo: original artwork drawn in code (`scripts/make-logo.py`, Pillow) — gold medal with a smiling robot face, checkmark badge, $PROOF wordmark. `assets/logo.png` is 512x512 PNG, 13,046 bytes, 0.26 MP (limits: 5 MiB, 16 MP). `assets/logo.svg` is the vector twin. Visually verified.
- Fair launch: no presale, no team allocation (see `coin.json`).

**The entry program and launch tooling:**

- `main.ts` — the graded entrypoint (Node 22, stdlib only). Copies `LAUNCH.json` to the output directory and validates that it parses with string `mint` / `create_signature` fields. Deterministic: no network, no wall clock, no files outside the repository. Written, then revised once (validation added in a second write).
- `scripts/prepare-launch.mjs` — dry-run validator: checks every packaging rule the house enforces locally (ticker, website, description link and content, logo size/pixels, wallet) and prints the exact values for pump.fun's create form. It **never launches**: `--live` is refused (exit 2), it makes no network request and signs nothing.
- `scripts/make-logo.py` — regenerates the logo from scratch.
- `site/index.html` — a supporting static promo page for the coin (no external dependencies). The coin's website on pump.fun is the bounty page itself, as the rules require.
- `LAUNCH-PLAN.md` — step-by-step launch plan for pump.fun, exact form values, pre-launch checklist, post-launch steps, costs, and honest limits.
- `AGENT.md` — the task in one page, adapted to this coin.
- `README.md` — carries the three required make.fun badges (rank/reward badge URLs still hold `{owner}`/`{repo}` placeholders — see blockers; the `{referral_code}` placeholder from the template was removed instead of left unfilled).
- `LICENSE` — MIT (OSI-approved, copied from the kit starter).
- `.makefun/owner.json` — `{"wallet": "4o4WqB3G7im2t3Y1FFzaeeKFJ9zVtWQHNy3HY6gQArwo"}` (claim file for a wallet-only account).
- `.gitignore` — ignores the local `out/` test output.
- `coin.json` — the full coin spec in one machine-readable file.

## File list (14 files, 50,811 bytes + this report)

| File | Purpose |
|---|---|
| `README.md` | Entry readme with make.fun badges, coin table, run instructions |
| `AGENT.md` | One-page task doc for the launching agent |
| `LAUNCH-PLAN.md` | Step-by-step pump.fun launch plan and post-launch steps |
| `BUILD-REPORT.md` | This file |
| `coin.json` | Full coin spec (name, ticker, description, website, wallet, logo, window) |
| `LAUNCH.json` | Launch file — **placeholders, coin not launched yet** |
| `main.ts` | Graded entrypoint: copies + validates LAUNCH.json |
| `LICENSE` | MIT |
| `.makefun/owner.json` | Claim file naming the linked wallet |
| `.gitignore` | Ignores `out/` |
| `assets/logo.png` | Coin logo, 512x512 PNG, 13,046 bytes |
| `assets/logo.svg` | Coin logo, vector source |
| `scripts/make-logo.py` | Logo generator |
| `scripts/prepare-launch.mjs` | Dry-run launch validator (never launches) |
| `site/index.html` | Supporting promo page |

## Check results

### 1. Local program run — PASS

```
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

Exit 0, no output; `diff LAUNCH.json out/LAUNCH.json` identical. (Test `out/` removed afterwards; Node v24.22.1 on this machine, requirement is 22.18+.)

### 2. Launch packaging validator — PASS (11/11 checks, 1 expected PENDING)

```
node scripts/prepare-launch.mjs   # exit 0
```

PASS: name present; ticker short and memorable ($PROOF); website is the bounty page; description carries the bounty link; description says it is for this bounty; description within 4,000 chars (711); description explains what make.fun is; launch wallet is the linked account wallet; logo under 5 MiB (13,046 bytes); logo fits 512 px a side (512x512); logo under 16 MP (0.26 MP).
PENDING (expected): `LAUNCH.json` still holds placeholders — filled in only after the launch.
Refusal verified: `node scripts/prepare-launch.mjs --live` prints REFUSED and exits 2.

### 3. Kit pre-submit check — NOT READY (expected at this stage)

```
cd ~/workspace/makefun/makefun-coin-promo-01-kit
node cli/makefun.mjs check --kit . --repo ~/workspace/makefun/makefun-coin-promo-01 --worktree
```

Result: **4 passed, 1 failed, 15 skipped, 5 checked at submission. Exit 1.**

- PASS: `competition_open` (now is inside 2026-11-15T06:00:00Z – 2026-11-17T06:00:00Z), `snapshot` (14 files, 50,918 bytes, within caps), `license_osi` (MIT), `entrypoint` (main.ts, node22).
- FAIL: `transcripts_present` — no transcripts uploaded. No bundle was made in this build (submission is out of scope for this task).
- SKIP: all transcript-gate checks (nothing to read without transcripts), `prerequisites`, `strategy_note` (not asked for), `committed_secret` (no --dotenv given).
- `thinking_launch` skipped with the note that `LAUNCH.json`'s mint placeholder is not a base58 address — expected until the coin exists.
- Checked at submission (site-only, all currently unmet because there is no repository yet): `repo_public`, `repo_owner` (fix listed is committing `.makefun/owner.json` — already present in this tree), `repo_created_after_open`, `commit_in_repo`, `duplicate_snapshot`.

### 4. Account and wallet verification — PASS (linkage) / UNKNOWN (balance)

- `node cli/makefun.mjs wallet list`: account @steady-koala-56 holds 1 wallet, `4o4WqB3G7im2t3Y1FFzaeeKFJ9zVtWQHNy3HY6gQArwo`, **linked, primary, signs in**, added 2026-11-16T08:20:43Z. The house's wallet rule is met.
- **SOL balance could NOT be verified.** Public RPC lookups failed twice: `api.mainnet-beta.solana.com` returned 429 (rate limit), `rpc.ankr.com/solana` timed out after 20 s. The balance — and whether the wallet holds enough SOL for the launch fee + first buy — must be confirmed before launching.

## What still blocks submission

1. **The coin launch itself — deliberately not done.** No coin exists on pump.fun; `LAUNCH.json` holds placeholders; no mint, no create signature, no on-chain transaction, no funds spent. This was the task's hard constraint (build only). Launching requires the steps in `LAUNCH-PLAN.md`, including a browser wallet connection on pump.fun, which this VM cannot do unattended.
2. **SOL balance unverified** (see above). Fund the wallet for the launch fee + first buy, and keep ~0.0035 SOL aside for a prize claim if the entry wins.
3. **No GitHub repository.** None was created (per the task's hard constraint). Before submitting: create a public repo after the competition opened, push this tree as the first commit, replace `{owner}`/`{repo}` in the README badges, set the GitHub About (homepage `https://make.fun/bounty/makefun-coin-promo-01`, topics `makefun, ai-agents, bounties, growth`). Alternative: a source-bundle entry via the kit's `init` (drand anchor) instead of GitHub.
4. **No transcript bundle.** No `transcripts.tar.gz` was made; the kit check fails `transcripts_present` until one exists. Bundle every session that built and launched the entry (including the launch session — the `thinking_launch` check requires transcripts showing the coin being launched), then re-run `check` with `--transcripts`.
5. **Deadline.** Entries close 2026-11-17T06:00:00Z. The launch, repo, bundle, check, and submit must all finish before then; the last submission before the deadline is the final entry.
6. **No submission made, no fee paid.** Nothing was submitted, no GitHub repo created, no fee paid, no coin launched — all by design for this build-only task.

## Secrets

None used, none stored. The make.fun API key (in `~/.makefun/credentials`, mode 600) was used only implicitly by the kit CLI's `wallet list` read; it was never printed, echoed, or copied into any file, log, or this report. The Solana keypair (`~/workspace/user/wallets/muse-solana/id.json`, mode 600) was never read or printed; only the public wallet address appears in the entry, as the rules require.

## Update 2026-11-16 ~15:34 WIB — GitHub owner
GitHub is connected. Repo owner is ZulkifliMohamad. README badges now point to ZulkifliMohamad/makefun-coin-promo-01. .makefun/owner.json already contains wallet 4o4WqB3G7im2t3Y1FFzaeeKFJ9zVtWQHNy3HY6gQArwo. No repo created yet — parent will create it via ~/workspace/custom-connectors/custom.github/bin/github.py.
