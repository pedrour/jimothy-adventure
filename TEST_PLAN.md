# Jimothy Eats Seattle — Test Plan

This plan must pass on every implementation round before shipping.

---

## 1. Core Gameplay

| # | Test | Expected |
|---|------|----------|
| 1.1 | Page loads | Canvas appears, Jimothy visible on ground, background music starts on first tap/keypress |
| 1.2 | Arrow keys move Jimothy | Left/right movement, Jimothy faces correct direction |
| 1.3 | Space / ArrowUp jumps | Jimothy leaves ground, physics returns him to ground |
| 1.4 | Land on fence | Jimothy stops at fence top, does not fall through |
| 1.5 | Jump fence → branch | Double-height jump reaches branch platforms |
| 1.6 | Collect food item | Score increases, popup appears, particle burst fires, collect sound plays |
| 1.7 | Coffee collection | Score increases, orange ZOOM! HUD badge appears, Jimothy moves faster for ~3.5s |
| 1.8 | S / ArrowDown near trash | Rummage animation plays (~1.3s), points awarded, can shows open lid |
| 1.9 | S far from trash | No rummage animation (proximity check) |
| 1.10 | Progress bar | Fills as snacks/cans collected, raccoon emoji icon tracks along bar |
| 1.11 | Snack counter HUD | Shows `🦝 N/20 snacks` correctly |
| 1.12 | Camera follows Jimothy | camX tracks smoothly, world scrolls, Jimothy stays ~35% from left |
| 1.13 | World boundary | Jimothy can't go past left or right world edge |
| 1.14 | Fall off world | Jimothy respawns on ground (no death — just reset Y) |
| 1.15 | Collect all 14 food + 6 cans | Win screen triggers, victory music plays, bg music stops |

---

## 2. Cheat Codes

| # | Test | Expected |
|---|------|----------|
| 2.1 | Down×10 within 900ms | Win screen fires immediately with full score |
| 2.2 | Down×10 spread >900ms | Streak resets, no cheat win |
| 2.3 | Down cheat on win screen | No effect (won check guards it) |
| 2.4 | Up×10 within 900ms | Orca breach starts immediately, toast shows "🐋 orca spotted!" |
| 2.5 | Up×10 spread >900ms | Streak resets, no orca |
| 2.6 | Up×10 on mobile (JUMP button) | Same as 2.4 — noteUpPress fires on touchstart |
| 2.7 | Up×10 on win screen | No effect (won check guards it) |
| 2.8 | Up×10 after orca already shown | No second orca (orcaShown guard) |

---

## 3. Orca Sighting

| # | Test | Expected |
|---|------|----------|
| 3.1 | ~20% runs show orca | After camX > ~1110 (15% of WORLD_W), orca breach appears. Expected in roughly 1/5 fresh playthroughs. |
| 3.2 | Orca position | Orca appears at screen right (~x=391), in the Puget Sound water band, behind the ferry |
| 3.3 | Breach arc | Orca rises ~82px above water surface and dips back over 300 frames (~5s) |
| 3.4 | Orca toast | "🐋 orca spotted!" notification appears, fades after ~3s, auto-removes from DOM |
| 3.5 | Win-scene orcas | Two permanent orcas always leap on win screen (unaffected by gameplay orca logic) |
| 3.6 | `orca_sighted` GA event | Fires with `{forced:true}` on cheat, no param on organic |
| 3.7 | No double orca | Once `orcaShown=true`, natural trigger cannot fire again in same run |
| 3.8 | Orca in explore mode | Works same as daily mode |
| 3.9 | Orca during win screen | Not drawn (drawBg not called when `won=true`) |

---

## 4. Daily Mode

| # | Test | Expected |
|---|------|----------|
| 4.1 | "📅 DAILY" button visible | Top-left corner, dark translucent background |
| 4.2 | Click DAILY button | Game restarts in daily mode; button turns purple with `.active` class |
| 4.3 | Click again to toggle off | Returns to explore mode, button loses purple |
| 4.4 | Daily mode HUD timer | "⏱ M:SS" counter appears (top-right, below coffee boost area) after first movement |
| 4.5 | Timer accuracy | Timer tracks real wall-clock time (not frame-count) |
| 4.6 | Daily win screen title | Shows "🦝 DAILY #N DONE! 🦝" instead of "JIMOTHY IS FULL" |
| 4.7 | Daily win score line | Shows `all 20 snacks · N bites · ⏱ M:SS · 🔥×S` |
| 4.8 | Streak logic | First completion: streak=1. Next day completion: streak=2. Two days skipped: resets to 1 |
| 4.9 | Streak persistence | `jimothy_streak` in localStorage persists across page reloads |
| 4.10 | Only first completion counts | Re-playing and winning in same day does NOT overwrite first result |
| 4.11 | Daily key format | `jimothy_daily_<days-since-epoch>` unique per UTC day |
| 4.12 | Daily share text | Format: `🦝 Jimothy Daily #N · ⏱ M:SS\n🔥×S 🍖 P bites\nplayjimothy.com` |
| 4.13 | Explore share text | Format: `🦝 I fed Jimothy N bites exploring Seattle!...` (unchanged) |
| 4.14 | `mode_changed` GA event | Fires when daily mode toggled |
| 4.15 | `game_start` GA event includes mode | `{mode:'daily'}` or `{mode:'explore'}` |
| 4.16 | `game_complete` GA event includes mode | `{score, mode:'daily', time_ms:N}` or `{score, mode:'explore'}` |
| 4.17 | Button shows "📅 DONE" | After winning in daily mode, button updates to "📅 DONE" |
| 4.18 | Timer doesn't show in explore mode | No timer pill visible in explore mode |
| 4.19 | Timer resets on restart | Switching mode or pressing Space to restart clears timer to 0 |

---

## 5. Audio

| # | Test | Expected |
|---|------|----------|
| 5.1 | No autoplay on load | Music is silent until first user gesture |
| 5.2 | First gesture starts music | Any tap/click/keydown anywhere on page triggers music |
| 5.3 | Mute button | 🔊 → 🔇, music stops, audio context suspends |
| 5.4 | Unmute button | 🔇 → 🔊, music resumes |
| 5.5 | Tab background / foreground | Music pauses when tab hidden, resumes when shown |
| 5.6 | Jump sound | Plays on jump (not held jump — only first press) |
| 5.7 | Collect sound | Plays on food collection |
| 5.8 | Rummage sound | Ascending chord on S-press near can |
| 5.9 | Victory music | Fires on win, loops until win screen exits |
| 5.10 | No music during win scene | Background loop stops before victory plays |
| 5.11 | Daily button unlocks audio | Clicking DAILY button counts as user gesture for audio |

---

## 6. Win Screen

| # | Test | Expected |
|---|------|----------|
| 6.1 | Win delay | Win screen renders 160 frames (~2.7s) before showing HTML buttons |
| 6.2 | HTML buttons position | Share/X/Facebook buttons anchored to canvas via `layoutWinActions()` |
| 6.3 | Win screen at 360px | All text visible, no overflow, contact email legible |
| 6.4 | Win screen at 430px | Same as above |
| 6.5 | Win screen at 1280px | Canvas centered, buttons correctly positioned |
| 6.6 | Landscape orientation | Buttons re-anchor after orientationchange (250ms delay) |
| 6.7 | Win Jimothy visible | Dancing raccoon visible against night sky (lightened gradient + halo) |
| 6.8 | Space Needle visible | Full Space Needle with rainbow rim animation |
| 6.9 | Win orcas | Two orcas leaping on each side, rainbow splash rings |
| 6.10 | Fireworks | Fireworks launch and fade over the city |
| 6.11 | "tap / SPACE to go again" | Appears after 160 frames |
| 6.12 | Space/SPACE restarts | Pressing Space on win screen calls init() |
| 6.13 | Contact email readable | `get in touch — contact@nebulaailabs.com` at 14px, two-tone |
| 6.14 | URL in canvas | `playjimothy.com` at 78% opacity |

---

## 7. Share

| # | Test | Expected |
|---|------|----------|
| 7.1 | "SHARE SCORE" button | Visible and clickable on win screen |
| 7.2 | Mobile image share | `navigator.canShare({files})` path: canvas PNG + share text offered |
| 7.3 | Mobile URL share fallback | If file share unavailable, `navigator.share({url})` used |
| 7.4 | Desktop clipboard fallback | `clipboard.writeText(shareText)`, button briefly shows "✓ Copied!" |
| 7.5 | X share button | Opens `x.com/intent/tweet` with noopener,noreferrer |
| 7.6 | Facebook share button | Opens FB sharer with noopener,noreferrer |
| 7.7 | Share GA events | `share_tapped` → `share_completed` with correct method |
| 7.8 | Daily share text | Shows day #, time, streak, score |
| 7.9 | Explore share text | Shows score and challenge message |

---

## 8. Analytics

| # | Test | Expected |
|---|------|----------|
| 8.1 | `game_start` | Fires on first movement, includes `{mode}` |
| 8.2 | `game_progress` | Fires at 25%, 50%, 75% world traversal |
| 8.3 | `session_duration_bucket` | Fires at 30s, 60s, 2min, 5min on page |
| 8.4 | `coffee_collected` | Fires each time coffee food item is collected |
| 8.5 | `trash_rummaged` | Fires each time S pressed near can (start of rummage) |
| 8.6 | `game_complete` | Fires with `{score, mode, time_ms}` on win |
| 8.7 | `mute_toggled` | Fires with `{muted:true/false}` on each toggle |
| 8.8 | `share_tapped` | Fires with `{score}` or `{score, platform}` |
| 8.9 | `share_completed` | Fires with `{method, score}` |
| 8.10 | `orca_sighted` | Fires with optional `{forced:true}` |
| 8.11 | `mode_changed` | Fires with `{mode}` when daily toggled |
| 8.12 | No console errors from gtag | `track()` is always wrapped in try/catch |

---

## 9. Security

| # | Test | Expected |
|---|------|----------|
| 9.1 | window.open calls | All have `noopener,noreferrer` (X, Facebook share) |
| 9.2 | No innerHTML | All dynamic text uses `textContent` or Canvas API, no innerHTML |
| 9.3 | Share button text reset | Uses `textContent`, not innerHTML |
| 9.4 | localStorage values | Only game state stored (score, streak, time); no user PII |

---

## 10. Performance / Stability

| # | Test | Expected |
|---|------|----------|
| 10.1 | No JS errors on load | Browser console clean |
| 10.2 | 60fps game loop | `requestAnimationFrame` loop runs; no dropped frames on modern mobile |
| 10.3 | No AudioContext leaks | Single audio context per page load; oscillators `stop()` after use |
| 10.4 | Memory: orca toast DOM | Toast `<div>` removed from DOM after 3.7s |
| 10.5 | Memory: particles array | Filtered each frame; never unboundedly grows |
| 10.6 | Memory: fireworks array | Capped at 16, filtered when t>56 |
| 10.7 | File size | `index.html` under 200KB (current ~107KB JS + HTML) |
| 10.8 | OG image served | `og-image.png` loads (1200×630) |
| 10.9 | robots.txt serves | `/robots.txt` returns text/plain, references sitemap |
| 10.10 | sitemap.xml serves | Valid XML with `https://playjimothy.com/` URL |

---

## 11. Cross-Feature Regression

| # | Test | Expected |
|---|------|----------|
| 11.1 | Daily mode + orca | Orca appears and toast shows correctly when in daily mode |
| 11.2 | Cheat win in daily mode | Saves daily result with timer elapsed so far |
| 11.3 | Orca during coffee boost | No visual conflict; both coffee glow and orca coexist |
| 11.4 | Switch mode mid-game | Daily button toggles mode and restarts fresh (timer resets) |
| 11.5 | Multiple restarts | State fully resets each `init()` call; no stale orca/daily state |
| 11.6 | Mute + win | Win screen stays silent after muting before win |
| 11.7 | Win screen orca vs gameplay orca | Win scene always has two orcas; gameplay orca is separate and only shows during play |

---

## Quick Smoke Test (run before every push)

1. Load `https://playjimothy.com` fresh  
2. Press ArrowRight → music starts, Jimothy moves  
3. Check `🦝 0/20 snacks` HUD  
4. Collect one food item → popup + sound  
5. Press S near trash → rummage animation  
6. Press ArrowDown×10 fast → win screen fires  
7. Win screen: all text visible, buttons positioned, Jimothy dancing  
8. Press Space → restarts  
9. Click 📅 DAILY button → purple, timer shows after movement  
10. CheatWin → "DAILY #N DONE!" on win screen with time  
11. Press ArrowUp×10 fast → "🐋 orca spotted!" toast appears  
