# CODM English Patch v0.2

## What changed

- Replaces all Chinese-bearing records in the analyzed main `0db.bytes`
  language catalog: 164,256 records across 130,989 unique phrases.
- Includes the login and loading strings found in that catalog.
- Adds the 337 Chinese phrases missing from v0.1, reuses 111 exact English
  matches found in the installed game's paired locale, and adds selected
  terminology and high-visibility corrections.
- Keeps unrelated archive members unchanged and checks formatting tokens
  before saving.
- Adds an upgrade path for the exact v0.1 package hash and the direct v0.1
  install hash recorded for the analyzed build.
- Creates a timestamped backup before writing.

## Install

Download `CODM-English-Patch-v0.2.zip`, extract it, close the game and emulator,
then run `Apply-Translation.cmd`. Enter the game folder that contains
`CODM.exe` and `CODM_Data` when prompted. The [Portuguese tutorial](TUTORIAL-PT-BR.md)
explains installation, updates, and restoration.

## Limits

This release translates the main language catalog only. Opaque data tables,
server-delivered text, and text baked into images or videos are not covered.
The 130,652 phrases inherited from v0.1 have not all been individually
reviewed; long descriptions may still sound unnatural. Exact parity with the
Global client is not certified because a matching English catalog for this
client build is unavailable.

The v0.2 clone was reported working by the user. A complete screen-by-screen
visual review has not been recorded. This patch is unofficial, does not
include the complete game client, and does not change login or servers.

## Download integrity

- File: `CODM-English-Patch-v0.2.zip`
- Size: 75,966,559 bytes
- SHA-256: `7D36DD6D2CFC21D07545D0734DBD8020E2E670FEED9D63838A144154E49ACBCE`
