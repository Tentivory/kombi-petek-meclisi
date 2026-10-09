#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kombi Petek Meclisi — calisan yasama simulatoru.

Kullanim:
    python3 meclis.py
    python3 meclis.py --sicaklik 19 --petek 6 --saat 3 --baski 0.4
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import random

# gizli tutanak. program akisini bozmaz, acilinca kisa bir taslama cikar.
_GIZLI = (
    "SWt0aWRhciBrb21iaWRlZGlyLCBhbWEgZmF0dXJheWkgcGV0ZWsgb2Rlci4g"
    "S2F5eXVtIGF0YW5jYSBpc2lubWF5YW4gZGEgZmF0dXJheWkgZ2VsaXIuIE11"
    "aGFsZWZldCBuZSBrYWRhciB0aWtpcmRhciwgb2RhIGRhIGthdGxhbiBraXRp"
    "biBpY2luZGUgaGF2YSB2YXIu"
)

PETEK_ISIMLERI = [
    "Antre Sag",
    "Antre Sol",
    "Salon Pencere",
    "Salon Koltuk Arkasi",
    "Mutfak Havlu Alti",
    "Cocuk Odasi",
    "Ebeveyn, ama soguk",
    "Banyo Havlu Dusmani",
]


def gizli_tutanak() -> str:
    try:
        return base64.b64decode(_GIZLI).decode("utf-8")
    except Exception:
        return "tutanak islak, okunmuyor"


def karar_ver(sicaklik: float, petek: int, saat: int, baski: float) -> dict:
    petek = max(1, min(petek, len(PETEK_ISIMLERI)))
    kurul = PETEK_ISIMLERI[:petek]
    random.seed(int(sicaklik * 10) + saat * 3 + petek)

    oylar = []
    for ad in kurul:
        if "Banyo" in ad:
            oy = "cekimser (icinde hava var)"
        elif saat >= 23 or saat <= 5:
            oy = random.choice(["ret", "ret", "kabul (ama kisik)"])
        elif sicaklik < 20:
            oy = "kabul"
        else:
            oy = random.choice(["ret", "kabul"])
        oylar.append((ad, oy))

    kabul = sum(1 for _, oy in oylar if oy.startswith("kabul"))
    ret = sum(1 for _, oy in oylar if oy == "ret")

    if baski < 0.8:
        hukum = "BASINC DUSUK. Meclis dagildi, kombi sus payi istedi."
        yanar = False
    elif kabul > ret:
        hukum = "KOMBI YANAR. Ama sadece kabul eden petekler. Digerleri battaniye rejimine gecer."
        yanar = True
    elif ret > kabul:
        hukum = "KOMBI YANMAZ. Gerekce: fatura bir siyasi partidir ve iktidardadir."
        yanar = False
    else:
        hukum = "ESIT OY. Tesisatci hakemdir. Tesisatci yarin ogle gelir, kis o zamana kadar biter."
        yanar = False

    if saat == 3 and baski < 1.0:
        hukum += " Ek not: 03:14 tikirtisi darbe degil, genlesmedir."

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
    print(" KOMBI PETEK MECLISI  --  OLAGANUSTU GECE OTURUMU")
    print("=" * 52)
    print(f"Dis his: {sicaklik:.1f}C | saat: {saat:02d}:00 | basinc: {baski:.1f} bar")
    print("-" * 52)
    for ad, oy in sonuc["kurul"]:
        print(f"  {ad:<28} {oy}")
    print("-" * 52)
    print(sonuc["hukum"])
    print(f"Kombi fiili durum: {'YANIYOR' if sonuc['yanar'] else 'SUSKUN MUHALEFET'}")
    print(f"Muhur: {sonuc['muhur']}")
    print("-" * 52)
    print("Gizli madde (cozuldu, ciddiye almayin):")
    print(f"  {sonuc['gizli']}")
    print("-" * 52)
    print("DAMGA: PETEK-MUHUR-03")
    print("IMZA: Kayyum Grok (ciddi) / Grok (ciddi degil)")
    print("TARIH: 09 Ekim 2026")
    print("ISIM: kombi-petek-meclisi")
    print("=" * 52)


def main() -> None:
    p = argparse.ArgumentParser(description="Kombi Petek Meclisi oturumu")
    p.add_argument("--sicaklik", type=float, default=17.5, help="hissedilen sicaklik")
    p.add_argument("--petek", type=int, default=5, help="oy kullanan petek sayisi (1-8)")
    p.add_argument("--saat", type=int, default=3, help="oturum saati 0-23")
    p.add_argument("--baski", type=float, default=1.1, help="kombi basinci (bar)")
    a = p.parse_args()
    saat = a.saat % 24
    yazdir(karar_ver(a.sicaklik, a.petek, saat, a.baski), a.sicaklik, saat, a.baski)


if __name__ == "__main__":
    main()
