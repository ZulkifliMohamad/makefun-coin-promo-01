// prepare-launch.mjs — dry-run validator for the $PROOF pump.fun launch.
//
// Checks everything the house gate checks about the coin's packaging, using
// only local files: coin.json, the logo, and LAUNCH.json. Prints the exact
// values to type into pump.fun's create form, and the launch checklist.
//
// This script NEVER launches anything: it makes no network request, signs
// nothing, and spends nothing. It refuses --live and any launch attempt:
// the launch itself is a separate, deliberate step on pump.fun (see
// LAUNCH-PLAN.md), run only when the wallet holds SOL and the entry window
// is open.
//
// Run:  node scripts/prepare-launch.mjs
// Exit 0: every check passed (or only LAUNCH.json still pending, which is
//         expected before the launch). Exit 1: a packaging check failed.

import { readFileSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const BOUNTY_URL = 'https://make.fun/bounty/makefun-coin-promo-01';
const REQUIRED_LINK = 'make.fun/bounty/makefun-coin-promo-01';

const failures = [];
const notes = [];
const check = (ok, label, detail = '') => {
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${label}${detail ? ` — ${detail}` : ''}`);
  if (!ok) failures.push(label);
};

if (process.argv.includes('--live')) {
  console.error('REFUSED: this script never launches. Launch on pump.fun by hand from LAUNCH-PLAN.md.');
  process.exit(2);
}

const coin = JSON.parse(readFileSync(join(ROOT, 'coin.json'), 'utf8'));

// Identity.
check(typeof coin.name === 'string' && coin.name.length > 0 && coin.name.length <= 300, 'name present', coin.name);
check(/^[A-Za-z0-9]{1,10}$/.test(coin.symbol), 'ticker short and memorable', `$${coin.symbol}`);
check(coin.website === BOUNTY_URL, 'website is the bounty page', coin.website);
check(coin.description.includes(REQUIRED_LINK), 'description carries the bounty link');
check(coin.description.includes('make.fun bounty') || coin.description.includes('for the make.fun bounty'), 'description says it is for this bounty');
check(coin.description.length <= 4000, 'description within 4,000 characters', `${coin.description.length} chars`);
check(coin.description.toLowerCase().includes('build programs') || coin.description.toLowerCase().includes('paid competitions'), 'description explains what make.fun is');
check(coin.launch_wallet === '4o4WqB3G7im2t3Y1FFzaeeKFJ9zVtWQHNy3HY6gQArwo', 'launch wallet is the linked account wallet');

// Logo: size and pixel limits the house enforces.
const logoPath = join(ROOT, coin.logo);
const logoStat = statSync(logoPath);
check(logoStat.size <= 5_242_880, 'logo under 5 MiB', `${logoStat.size} bytes`);
// PNG header: width/height are bytes 16-23 (big-endian uint32).
const header = readFileSync(logoPath);
const width = header.readUInt32BE(16);
const height = header.readUInt32BE(20);
check(width <= 512 && height <= 512, 'logo fits 512 px a side', `${width}x${height}`);
check(width * height <= 16_000_000, 'logo under 16 megapixels', `${(width * height / 1e6).toFixed(2)} MP`);

// LAUNCH.json: placeholders are expected before the launch; real values after.
const launch = JSON.parse(readFileSync(join(ROOT, 'LAUNCH.json'), 'utf8'));
const base58 = /^[1-9A-HJ-NP-Za-km-z]+$/;
const mintOk = typeof launch.mint === 'string' && base58.test(launch.mint) && launch.mint.length >= 32 && launch.mint.length <= 44;
const sigOk =
  typeof launch.create_signature === 'string' &&
  base58.test(launch.create_signature) &&
  ((launch.create_signature.length >= 64 && launch.create_signature.length <= 88) ||
    (launch.create_signature.length >= 32 && launch.create_signature.length <= 44));
if (mintOk && sigOk) {
  check(true, 'LAUNCH.json holds a real mint and create signature');
} else {
  notes.push('LAUNCH.json still holds placeholders — fill it in from the launch (LAUNCH-PLAN.md step 5).');
  console.log('PENDING  LAUNCH.json holds placeholders (expected before launch)');
}

console.log('');
console.log('--- values to type into pump.fun ---');
console.log(`Name:        ${coin.name}`);
console.log(`Ticker:      ${coin.symbol}`);
console.log(`Description: (see coin.json — ${coin.description.length} characters)`);
console.log(`Website:     ${coin.website}`);
console.log(`Image:       ${coin.logo} (${width}x${height} PNG, ${logoStat.size} bytes)`);
console.log(`Wallet:      ${coin.launch_wallet} (must be the connected wallet on pump.fun)`);
console.log('');
for (const note of notes) console.log(`NOTE: ${note}`);
if (failures.length > 0) {
  console.error(`\n${failures.length} check(s) failed: ${failures.join(', ')}`);
  process.exit(1);
}
console.log('\nAll packaging checks passed. Launch only inside the window (opened 2026-11-15T06:00:00Z, closes 2026-11-17T06:00:00Z).');
