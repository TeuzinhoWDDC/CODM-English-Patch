from __future__ import annotations

import gzip
import hashlib
import json
import os
import shutil
import struct
import sys
from datetime import datetime
from pathlib import Path

import compression.zstd as zstd


PACKAGE = Path(__file__).resolve().parent
MAIN_RELATIVE = Path("CODM_Data/StreamingAssets/0db.bytes")
LOCALE_RELATIVE = Path(
    "PersistentData/ExtractQts/57/LanguageBytes/"
    "cPVHOPHMaPLBpJJZRZNM_IG_lv.bytes"
)
ARCHIVE_CATALOG = "LanguageBytes/cPVHOPHMaPLB_IG_lv.bytes"
CURRENT_PATCH_SHA256 = "8384f6f298cf01ae9d97a3599c6ee392be6d0515505b81471e0213e71272b697"
PREVIOUS_PATCH_SHA256 = "0064682c2b576167424ca9f61706dd204bb5a353da4a9ce60f453067e3cab9c5"
PREVIOUS_V01_PACKAGE_SHA256 = "626d73a33c935dafc139635cb995a8ea717b4054359789f0a0da909af072f127"
PREVIOUS_DIRECT_V01_SHA256 = "459c24040070c13c4abfcc973507df2cdc39140a5f644b26dfb8b29c99741772"
PREVIOUS_V03_DRAFT_SHA256 = "ad4f9017e9d05706cb3be6f9ce5987301d0e5e7573272c1c825ba7dec6adf04f"
PREVIOUS_V03_LOBBY_QA4_SHA256 = "5e83b1db7d9eb509b1fdbd0b51d77e8895d00b62cb29a830da0dbbbed298f533"
PREVIOUS_V03_SETTINGS_QA1_SHA256 = "bec0e0b0e11f501de5618b3203745e9189b1655c2de2d7b5748d4fe057cd5f50"
PREVIOUS_V03_SETTINGS_QA2_SHA256 = "1739999dee308569d3a5f618fac25cf3a33ca23460578e64f5d5d7469dd9f621"
PREVIOUS_V03_SETTINGS_QA3_SHA256 = "f884e2bff9b1b67a937885dc2890ab80c54846862b65b6e6b65716c35b3aedbf"
SOURCE_ARCHIVE_SHA256 = "25db47665c230d93245e3a80ed613e02b9814d32b2d1ffe0f38a0a71b1589bfc"
OLD_LOCALE_SHA256 = "77176686955a8d3b1dc7d7e7b78aaab98eb1853ad8939ed58f5b9b097aff02e3"
ENGLISH_LOCALE_SOURCE_SHA256 = "3e7f570ff4d96ed0f3d6c885a9f5494df9022c983a9ceec67cfa9ad1c0439ed9"
PREVIOUS_ENGLISH_LOCALE_SHA256 = "7aac3cce704dd1cc89af94955470803aeaee197d140dde5c4e45c898c1e58e0f"
PREVIOUS_ENGLISH_LOCALE_QA3_SHA256 = "4f9eaaab4ec3aa44b823d8d271bf7f59d7874b21f10466e6bc6debbb3ced204f"
ENGLISH_LOCALE_SHA256 = "92ef69b2381e02b804a9dcefa11bc6060b4897c3c359092dfadcd9a8b7e6f42c"
SECONDARY_LOCALE_RELATIVE = Path("PersistentData/ExtractQts/57/LanguageBytes/cPVHOPHMaPLBpJJZRZNM_IG_eu.bytes")
SECONDARY_LOCALE_SOURCE_SHA256 = "7d38c6e0ff7542c96ff37d158ecf2f2a748a662ebfbfab9f0eb2404f6b043107"
SECONDARY_LOCALE_PREVIOUS_SHA256 = "a8736afb6a301d167c69892779d19d4259dbeb40b3a9727ada10cbc303986924"
PREVIOUS_SECONDARY_LOCALE_QA3_SHA256 = "e99badfefaf7a8f82d4d0d1984c5a9f4190b42715f6279b20556acbccb5de4f0"
SECONDARY_LOCALE_PATCHED_SHA256 = "a54454b1bd34691d98b62415721a084cced255578c46076388506160500d7f02"
MAPPING_FILE = PACKAGE / "translations.json.gz"
PAYLOAD_MAIN = PACKAGE / "Payload" / MAIN_RELATIVE
PAYLOAD_LOCALE = PACKAGE / "Payload" / LOCALE_RELATIVE
PAYLOAD_SECONDARY_LOCALE = PACKAGE / "Payload" / SECONDARY_LOCALE_RELATIVE
REPORT_FILE = PACKAGE / "Last-Run-Report.txt"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def contains_cjk(text: str | None) -> bool:
    return text is not None and any(
        "\u3400" <= char <= "\u9fff" or "\uf900" <= char <= "\ufaff"
        for char in text
    )


def parse_archive(data: bytes):
    if len(data) < 12:
        raise ValueError("O arquivo principal é curto demais para ser válido.")
    count = struct.unpack_from("<I", data, 8)[0]
    if count == 0 or count > 100000:
        raise ValueError(f"Número inesperado de arquivos internos: {count}.")
    pos = 12
    entries = []
    paths = set()
    for _ in range(count):
        if pos + 2 > len(data):
            raise ValueError("Índice interno incompleto.")
        path_len = struct.unpack_from("<H", data, pos)[0]
        pos += 2
        if path_len == 0 or pos + path_len + 8 > len(data):
            raise ValueError("Caminho ou índice interno inválido.")
        path = data[pos : pos + path_len].decode("utf-8")
        pos += path_len
        offset, size = struct.unpack_from("<II", data, pos)
        pos += 8
        if path in paths:
            raise ValueError(f"Caminho interno duplicado: {path}")
        paths.add(path)
        entries.append({"path": path, "offset": offset, "size": size})
    table_end = pos
    data_size = len(data) - table_end
    for entry in entries:
        if entry["offset"] > data_size or entry["size"] > data_size - entry["offset"]:
            raise ValueError(f"Índice fora do arquivo: {entry['path']}")
    return data[:12], entries, table_end


def archive_member(data: bytes, table_end: int, entry: dict, extra: int = 0) -> bytes:
    start = table_end + entry["offset"]
    end = start + entry["size"] + extra
    if end > len(data):
        raise ValueError(f"Conteúdo interno incompleto: {entry['path']}")
    return data[start:end]


def decode_catalog(blob: bytes):
    if len(blob) < 3 or blob[:2] != b"\x23\xea":
        raise ValueError("O catálogo de idioma tem um marcador não reconhecido.")
    decoded = zstd.decompress(blob[2:])
    if len(decoded) < 4:
        raise ValueError("O catálogo de idioma está incompleto.")
    count = struct.unpack_from("<I", decoded)[0]
    if count == 0 or count > 2000000:
        raise ValueError(f"Quantidade inesperada de textos: {count}.")
    pos = 4
    records = []
    for _ in range(count):
        if pos + 6 > len(decoded):
            raise ValueError("Registro incompleto no catálogo de idioma.")
        tag, length = struct.unpack_from("<IH", decoded, pos)
        pos += 6
        if pos + length > len(decoded):
            raise ValueError("Texto incompleto no catálogo de idioma.")
        raw = decoded[pos : pos + length]
        pos += length
        try:
            text = raw.decode("utf-16le")
        except UnicodeDecodeError:
            text = None
        records.append((tag, raw, text))
    return records, decoded[pos:]


def encode_catalog(records, footer: bytes) -> bytes:
    out = bytearray(struct.pack("<I", len(records)))
    for tag, raw, _text in records:
        if len(raw) > 0xFFFF:
            raise ValueError(f"Um texto excede o limite do formato (tag {tag:08x}).")
        out += struct.pack("<IH", tag, len(raw)) + raw
    out += footer
    return bytes(out)


def rebuild_archive(data: bytes, header: bytes, entries: list[dict], table_end: int,
                    target_entry: dict, new_member: bytes) -> bytes:
    old_data = data[table_end:]
    cursor = 0
    rebuilt_data = bytearray()
    for entry in sorted(entries, key=lambda item: item["offset"]):
        offset, size = entry["offset"], entry["size"]
        if offset < cursor:
            raise ValueError("Os arquivos internos se sobrepõem; nenhuma alteração foi salva.")
        rebuilt_data += old_data[cursor:offset]
        entry["new_offset"] = len(rebuilt_data)
        if entry["path"] == target_entry["path"]:
            rebuilt_data += new_member
            entry["new_size"] = len(new_member) - 2
        else:
            rebuilt_data += old_data[offset : offset + size]
            entry["new_size"] = size
        cursor = offset + size
    rebuilt_data += old_data[cursor:]

    index = bytearray(header)
    for entry in entries:
        path = entry["path"].encode("utf-8")
        if len(path) > 0xFFFF:
            raise ValueError("Um caminho interno excede o limite do formato.")
        index += struct.pack("<H", len(path)) + path
        index += struct.pack("<II", entry["new_offset"], entry["new_size"])
    return bytes(index + rebuilt_data)


def load_translations() -> dict[str, str]:
    with gzip.open(MAPPING_FILE, "rt", encoding="utf-8") as stream:
        translations = json.load(stream)
    if not isinstance(translations, dict) or len(translations) < 1000:
        raise ValueError("O arquivo de traduções está ausente ou incompleto.")
    return translations


def find_game_root() -> Path:
    beside_game = PACKAGE.parent
    if (beside_game / MAIN_RELATIVE).is_file():
        return beside_game
    path_file = PACKAGE / "GamePath.txt"
    configured = path_file.read_text(encoding="utf-8-sig").strip() if path_file.is_file() else ""
    if configured:
        game_root = Path(configured.strip('"'))
        if (game_root / MAIN_RELATIVE).is_file():
            return game_root
        raise FileNotFoundError(
            f"Não encontrei CODM_Data\\StreamingAssets\\0db.bytes em:\n{game_root}\n\n"
            "Ajuste o caminho em GamePath.txt."
        )
    print("Cole o caminho da pasta CODM (a que contém CODM_Data) e pressione Enter:")
    configured = input("> ").strip().strip('"')
    if not configured:
        raise FileNotFoundError("Nenhum caminho foi informado.")
    game_root = Path(configured).expanduser()
    if not (game_root / MAIN_RELATIVE).is_file():
        raise FileNotFoundError(
            f"Não encontrei CODM_Data\\StreamingAssets\\0db.bytes em:\n{game_root}"
        )
    path_file.write_text(str(game_root.resolve()) + "\n", encoding="utf-8")
    return game_root


def create_backup(game_root: Path, targets: list[Path]) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup_dir = PACKAGE / "Backups" / stamp
    for target in targets:
        if target.exists():
            relative = target.relative_to(game_root)
            destination = backup_dir / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, destination)
    return backup_dir


def atomic_replace(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(path.name + ".codm-english.tmp")
    try:
        with temp_path.open("wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        temp_path.replace(path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def apply_patch() -> int:
    game_root = find_game_root()
    main_path = game_root / MAIN_RELATIVE
    locale_path = game_root / LOCALE_RELATIVE
    if not PAYLOAD_LOCALE.is_file():
        raise FileNotFoundError("O pacote de idioma inglês está faltando em Payload.")
    current_main = main_path.read_bytes()
    current_hash = sha256(current_main)
    current_locale_hash = sha256(locale_path.read_bytes()) if locale_path.is_file() else None

    # Upgrade only exact known catalogs that match this analyzed client build.
    upgrade_from_previous = False
    if current_hash == CURRENT_PATCH_SHA256:
        updated_main = current_main
        translated_occurrences = 0
        remaining_cjk = None
        already_current = True
    elif current_hash in {PREVIOUS_PATCH_SHA256, PREVIOUS_V01_PACKAGE_SHA256, PREVIOUS_DIRECT_V01_SHA256, PREVIOUS_V03_DRAFT_SHA256, PREVIOUS_V03_LOBBY_QA4_SHA256, PREVIOUS_V03_SETTINGS_QA1_SHA256, PREVIOUS_V03_SETTINGS_QA2_SHA256, PREVIOUS_V03_SETTINGS_QA3_SHA256}:
        updated_main = PAYLOAD_MAIN.read_bytes()
        if sha256(updated_main) != CURRENT_PATCH_SHA256:
            raise ValueError("O payload do candidato de loja não corresponde ao hash declarado; o jogo não foi alterado.")
        translated_occurrences = 0
        remaining_cjk = 0
        already_current = False
        upgrade_from_previous = True
    else:
        already_current = False
        translations = load_translations()
        header, entries, table_end = parse_archive(current_main)
        by_path = {entry["path"]: entry for entry in entries}
        target_entry = by_path.get(ARCHIVE_CATALOG)
        if target_entry is None:
            raise ValueError(
                "A atualização mudou a estrutura do catálogo principal. "
                "O jogo não foi alterado."
            )
        records, footer = decode_catalog(archive_member(current_main, table_end, target_entry, 2))
        untouched_hashes = {
            entry["path"]: sha256(archive_member(current_main, table_end, entry))
            for entry in entries
            if entry["path"] != ARCHIVE_CATALOG
        }
        updated = []
        translated_occurrences = 0
        for tag, raw, text in records:
            english = translations.get(text) if text is not None else None
            if english is not None and english != text and contains_cjk(text):
                raw = english.encode("utf-16le")
                text = english
                translated_occurrences += 1
            updated.append((tag, raw, text))

        if translated_occurrences == 0:
            raise ValueError(
                "Nenhum texto conhecido foi encontrado na versão instalada. "
                "Pode ser uma atualização com catálogo novo; o jogo não foi alterado."
            )
        remaining_cjk = sum(contains_cjk(text) for _tag, _raw, text in updated)
        new_plain = encode_catalog(updated, footer)
        new_member = b"\x23\xea" + zstd.compress(new_plain, level=19)
        updated_main = rebuild_archive(
            current_main, header, entries, table_end, target_entry, new_member
        )

        # Reopen the generated archive before touching the installed copy.
        check_header, check_entries, check_table_end = parse_archive(updated_main)
        check_entry = {entry["path"]: entry for entry in check_entries}[ARCHIVE_CATALOG]
        check_records, check_footer = decode_catalog(
            archive_member(updated_main, check_table_end, check_entry, 2)
        )
        if check_header != header or check_footer != footer or len(check_records) != len(records):
            raise ValueError("A conferência do catálogo falhou; o jogo não foi alterado.")
        for expected, actual in zip(updated, check_records):
            if expected[0] != actual[0] or expected[1] != actual[1]:
                raise ValueError(
                    "A conferência dos registros falhou; o jogo não foi alterado."
                )
        check_by_path = {entry["path"]: entry for entry in check_entries}
        for path, old_hash in untouched_hashes.items():
            new_hash = sha256(
                archive_member(updated_main, check_table_end, check_by_path[path])
            )
            if new_hash != old_hash:
                raise ValueError(
                    f"Outro arquivo interno mudou ({path}); o jogo não foi alterado."
                )

    locale_bytes = PAYLOAD_LOCALE.read_bytes()
    if sha256(locale_bytes) != ENGLISH_LOCALE_SHA256:
        raise ValueError("O payload da tabela inglesa não corresponde ao hash declarado.")
    locale_action = "tabela inglesa de lobby e loja já atualizada" if current_locale_hash == ENGLISH_LOCALE_SHA256 else ""
    install_locale = False
    if current_locale_hash == ENGLISH_LOCALE_SHA256:
        pass
    elif current_locale_hash in {None, OLD_LOCALE_SHA256, ENGLISH_LOCALE_SOURCE_SHA256, PREVIOUS_ENGLISH_LOCALE_SHA256, PREVIOUS_ENGLISH_LOCALE_QA3_SHA256}:
        install_locale = True
        locale_action = "tabela inglesa atualizada com lobby e itens da loja"
    else:
        locale_action = "arquivo de idioma atualizado desconhecido; preservado por segurança"

    secondary_locale_path = game_root / SECONDARY_LOCALE_RELATIVE
    current_secondary_hash = (
        sha256(secondary_locale_path.read_bytes())
        if secondary_locale_path.is_file() else None
    )
    install_secondary_locale = False
    secondary_locale_action = "arquivo não encontrado; preservado"
    if current_secondary_hash == SECONDARY_LOCALE_PATCHED_SHA256:
        secondary_locale_action = "tabela de loja atualizada; conteúdo China-only preservado"
    elif current_secondary_hash in {SECONDARY_LOCALE_SOURCE_SHA256, SECONDARY_LOCALE_PREVIOUS_SHA256, PREVIOUS_SECONDARY_LOCALE_QA3_SHA256}:
        secondary_locale_bytes = PAYLOAD_SECONDARY_LOCALE.read_bytes()
        if sha256(secondary_locale_bytes) != SECONDARY_LOCALE_PATCHED_SHA256:
            raise ValueError("O payload da tabela secundária não corresponde ao hash declarado.")
        install_secondary_locale = True
        secondary_locale_action = "itens da loja Global localizados; ofertas China-only preservadas"
    elif current_secondary_hash is not None:
        secondary_locale_action = "arquivo de idioma atualizado desconhecido; preservado por segurança"

    changed_paths = []
    if updated_main != current_main:
        changed_paths.append(main_path)
    if install_locale:
        changed_paths.append(locale_path)
    if install_secondary_locale:
        changed_paths.append(secondary_locale_path)
    if not changed_paths:
        summary = (
            "A tradução deste pacote já está aplicada.\n"
            f"Jogo: {game_root}\n"
            f"Arquivo de idioma: {locale_action}\n"
            f"Loja e itens: {secondary_locale_action}\n"
        )
        REPORT_FILE.write_text(summary, encoding="utf-8")
        print(summary)
        return 0

    backup_dir = create_backup(game_root, changed_paths)
    try:
        if updated_main != current_main:
            atomic_replace(main_path, updated_main)
        if install_locale:
            atomic_replace(locale_path, locale_bytes)
        if install_secondary_locale:
            atomic_replace(secondary_locale_path, secondary_locale_bytes)
    except Exception:
        for target_path in reversed(changed_paths):
            original = backup_dir / target_path.relative_to(game_root)
            if original.is_file():
                atomic_replace(target_path, original.read_bytes())
        raise

    final_hash = sha256(updated_main)
    if already_current:
        translation_summary = "O catálogo principal v0.3-draft-lobby-qa1 já estava aplicado."
    elif upgrade_from_previous:
        translation_summary = "O catálogo principal foi atualizado; nenhum registro chinês permanece no catálogo principal."
    else:
        translation_summary = (
            f"Novos textos conhecidos traduzidos: {translated_occurrences:,}\n"
            f"Registros com caracteres chineses ainda presentes: {remaining_cjk:,}"
        )
    report = (
        "Tradução aplicada.\n"
        f"Jogo: {game_root}\n"
        f"Hash do catálogo antes: {current_hash}\n"
        f"Hash do catálogo agora: {final_hash}\n"
        f"{translation_summary}\n"
        f"Idioma adicional: {locale_action}\n"
        f"Loja e itens: {secondary_locale_action}\n"
        f"Cópia de segurança: {backup_dir}\n"
    )
    REPORT_FILE.write_text(report, encoding="utf-8")
    print(report)
    return 0


def main() -> int:
    try:
        return apply_patch()
    except Exception as error:
        message = f"Não foi possível aplicar a tradução.\n\nMotivo: {error}\n"
        print(message, file=sys.stderr)
        try:
            REPORT_FILE.write_text(message, encoding="utf-8")
        except OSError:
            pass
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
