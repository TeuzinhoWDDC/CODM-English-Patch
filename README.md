# CODM English Patch — final release v0.3 (discontinued)

> **Warning: discontinued and unofficial.** This patch modifies Call of Duty: Mobile game files. Activision's published COD Mobile security policy describes enforcement for unauthorized software that modifies game data and for reverse engineering game data. A patch that only changes text is **not guaranteed to be safe**; using it may trigger anti-cheat checks or account penalties, including a ban. Use at your own risk. For the lowest account risk, keep and play on an unmodified official installation.

This community project is not affiliated with or endorsed by Activision or Tencent. It is discontinued: v0.3 is the final release, with no future updates, compatibility fixes, or support planned. The Chinese edition may have separate publisher rules; this patch has no publisher authorization.

## What v0.3 contains

- The English UI patch for the analyzed Windows client build, including tested lobby, settings, and store wording updates.
- The correction of the `day/days` to `Jesus` mistranslations found in the tested catalog.
- A portable patcher that backs up target files before writing.
- A Portuguese guide for applying and restoring the patch.

The user reported that the v0.3 clone worked after the latest corrections. This is not a guarantee for other installs or game updates. The patch changes local language resources; that does not make it ban-safe or publisher-approved.

## Download and use

Download `CODM-English-Patch-v0.3.zip` from [GitHub Releases](https://github.com/TeuzinhoWDDC/CODM-English-Patch/releases/latest). Read [TUTORIAL-PT-BR.md](TUTORIAL-PT-BR.md) and the warning above before using it. The package does not include the complete game client. It is tied to the catalog build recorded in `manifest.json`; newer or different builds may not work.

The patcher makes backups under `Backups/<date-time>/`. To restore the original resources, close the game and restore those files to their original paths, or use the official launcher's repair/verification option. A clean official installation is the safest choice for normal online play.

## Coverage and limits

The patch covers the language resources included in this final package. Text delivered by servers, embedded in artwork/video, or stored in opaque resources may remain in Chinese. Global wording parity is not certified for every string. Compatibility with future game updates is not maintained.

**Final status: discontinued.** No further translations, troubleshooting, or compatibility work will be provided.
