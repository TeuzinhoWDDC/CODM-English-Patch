# CODM English Patch

Community-made English interface patch for the Chinese Call of Duty: Mobile
Windows client. It uses the game files already installed on your computer; it
does not include the complete game client and is not affiliated with
Activision or Tencent.

## Latest release

**v0.2** — download the portable package from
[GitHub Releases](https://github.com/TeuzinhoWDDC/CODM-English-Patch/releases/latest).

The patch replaces every Chinese-bearing record in the main language catalog
for the analyzed build: 164,256 records across 130,989 unique phrases. It also
creates a backup before changing game files and can upgrade the exact v0.1
catalogs listed in the package manifest.

## Quick start

1. Download and extract `CODM-English-Patch-v0.2.zip` to its own folder.
2. Close CODM and the emulator completely.
3. Run `Apply-Translation.cmd`. Administrator access is not required.
4. When asked, enter the game folder containing both `CODM.exe` and
   `CODM_Data` (for example, `F:\CODMGameApps\CN\emulator\Extract\CODM`).
5. Wait for the success message, note the backup location, then start the game
   normally.

See the full [Portuguese installation and restore tutorial](TUTORIAL-PT-BR.md).

## Backups, updates, and recovery

The patcher saves files under `Backups/<date-time>/` before writing. To undo
the patch, close the game and copy those files back to the same paths in the
game folder. After a game update, run the patcher again only if the catalog
format is still recognized. Compatibility with future updates is not
guaranteed.

## Scope and known limits

- Coverage is complete only for Chinese strings in the main `0db.bytes`
  language catalog of the analyzed build. Other tables, server-delivered text,
  and words embedded in images or videos are outside this release.
- The 130,652 phrases inherited from v0.1 received targeted term normalization
  and selected corrections, but were not reviewed one by one. Some long
  descriptions may still sound unnatural.
- Exact wording parity with COD Mobile Global is not certified because a
  matching Global language catalog for this client build is unavailable.
- The patch changes interface resources only; it does not change login,
  servers, backend behavior, or gameplay protections.

The repository contains the patcher and documentation. The portable release
package and its bundled runtime are published as a GitHub Release, not stored
in Git history.
