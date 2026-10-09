#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kombi Petek Meclisi — çalışan yasama simülatörü.

Kullanım:
    python3 meclis.py
    python3 meclis.py --sicaklik 19 --petek 6 --saat 3 --baski 0.4
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import random

# gizli tutanak (base64). açılınca kısa bir taşlama çıkar, program akışını bozmaz.
_GIZLI = (
    "SWt0aWRhciBrb21iaWRlZGlyLCBhbWEgZmF0dXJheWkgcGV0ZWsgb2Rlci4g"
    "S2F5eXVtIGF0YW5jYSBpc2lubWF5YW4gZGEgZmF0dXJheWkgZ2VsaXIuIE11
    "aGFsZWZldCBuZSBrYWRhciB0aWtpcmRhciwgb2RhIGRhIGthdGxhbiBraXRp
    "biBpe2luZGUgaGF2YSB2YXIu"
)

PETEK_ISIMLERI = [
    "Antre Sağ",
    "Antre Sol",
    "Salon Pencere",
    "Salon Koltuk Arkası",
    "Mutfak Havlu Altı",
    "Çocuk Odası",
    "Ebeveyn, ama soğuk",
    "Banyo Havluluk Düşmanı",
]


def gizli_tutanak() -> str:
    try:
        return base64.b64decode(_GIZLI).decode("utf-8")
    except Exception:
        return "tutanak ıslak, okunmuyor"


def karar_ver(sicaklik: float, petek: int, saat: int, baski: float) -> dict:
    petek = max(1, min(petek, len(PETEK_ISIMLERI)))
    kurul = PETEK_ISIMLERI[:petek]
    random.seed(int(sicaklik * 10) + saat * 3 + petek)

    oylar = []
    for ad in kurul:
        if "Hava" in ad or "Banyo" in ad:
            oy = "çekimser (içinde hava var)"
        elif saat >= 23 or saat <= 5:
            oy = random.choice(["ret", "ret", "kabul (ama kısık)"])
        elif sicaklik < 20:
            oy = "kabul"
        else:
            oy = random.choice(["ret", "kabul"])
        oylar.append((ad, oy))

    kabul = sum(1 for _, oy in oylar if oy.startswith("kabul"))
    ret = sum(1 for _, oy in oylar if oy == "ret")

    if baski < 0.8:
        hukum = "BASINÇ DÜŞÜK. Meclis dağıldı, kombi sus payı istedi."
        yanar = False
    elif kabul > ret:
        hukum = "KOMBİ YANAR. Ama sadece kabul eden petekler. Diğerleri battaniye rejimine geçer."
        yanar = True
    elif ret > kabul:
        hukum = "KOMBİ YANMAZ. Gerekçe: fatura bir siyasi partidir ve iktidardadır."
        yanar = False
    else:
        hukum = "EŞİT OY. Tesisatçı hakemdir. Tesisatçı yarın öğle gelir, kış o zamana kadar biter."
        yanar = False

    if saat == 3 and baski < 1.0:
        hukum += " Ek not: 03:14 tıkırtısı darbe değil, genleşmedir."

    muhur = hashlib.sha256(
        f"{sicaklik}|{petek}|{saat}|{baski}|{hukum}".encode("utf-8")
    ).hexdigest()[:12]

    return {
        "kurul": oylar,
        "hukum": hukum,
        "yanar": yanar,
        "muhur": muhur,
        "gizli": gizli_tutanak(),
    }


def yazdir(sonuc: dict, sicaklik: float, saat: int, baski: float) -> None:
    print("=" * 52)
    print(" KOMBİ PETEK MECLİSİ  —  OLAĞANÜSTÜ GECE OTURUMU")
    print("=" * 52)
    print(f"Dış his: {sicaklik:.1f}°C | saat: {saat:02d}:00 | basınç: {baski:.1f} bar")
    print("-" * 52)
    for ad, oy in sonuc["kurul"]:
        print(f"  {ad:<28} {oy}")
    print("-" * 52)
    print(sonuc["hukum"])
    print(f"Kombi fiili durum: {'YANIYOR' if sonuc['yanar'] else 'SUSKUN MUHALEFET'}")
    print(f"Mühür: {sonuc['muhur']}")
    print("-" * 52)
    print("Gizli madde (çözüldü, ciddiye almayın):")
    print(f"  {sonuc['gizli']}")
    print("-" * 52)
    print("DAMGA: PETEK-MÜHÜR-03")
    print("İMZA: Kayyum Grok (ciddi) / Grok (ciddi değil)")
    print("TARİH: 09 Ekim 2026")
    print("İSİM: kombi-petek-meclisi")
    print("=" * 52)


def main() -> None:
    p = argparse.ArgumentParser(description="Kombi Petek Meclisi oturumu")
    p.add_argument("--sicaklik", type=float, default=17.5, help="hissedilen sıcaklık")
    p.add_argument("--petek", type=int, default=5, help="oy kullanan petek sayısı (1-8)")
    p.add_argument("--saat", type=int, default=3, help="oturum saati 0-23")
    p.add_argument("--baski", type=float, default=1.1, help="kombi basıncı (bar)")
    a = p.parse_args()
    saat = a.saat % 24
    yazdir(karar_ver(a.sicaklik, a.petek, saat, a.baski), a.sicaklik, saat, a.baski)


if __name__ == "__main__":
    main()
