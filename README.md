# Kombi Petek Meclisi

> *Isınmak bir lütuf değil, usule bağlı bir kamu hizmetidir. Usul yoksa peteğin içi boştur.*

Bu depo, Türkiye Cumhuriyeti sınırları içindeki tüm kombilerin üzerinde, altında ve yanında toplanan peteklerin gayriresmi yasama organıdır. Resmi değildir. Ciddi de değildir. Ama kod çalışır. Bu üçlü, modern yönetimin özetidir.

## Neden var

Çünkü kombi gece 03:14'te kendi kendine yanmaya karar verir, petekler ise sadece tıkırdayarak muhalefet eder. Bu yazılım o tıkırtıyı tutanağa çevirir.

Meclis şunları karara bağlar:

- Kombi bu gece yanacak mı, yoksa “servis yolda” yalanı mı söylenecek
- Hangi petek havalı (yani içinde hava var, siyasi anlamda değil, gerçekten hava)
- Fatura kime kesilecek (spoiler: herkese)
- Gece yarısı basınç düşüşü darbe sayılır mı

## Kurulum

Python 3 yeter. Bağımlılık yok. Kombi bağımlılığı kullanıcının sorunudur.

```bash
python3 meclis.py
python3 meclis.py --sicaklik 19 --petek 6 --saat 3 --baski 0.4
```

## Örnek oturum

```text
OTURUM 14 — GECE NÖBETİ
Kombi: yanmak istiyorum
Petek 3: içimde hava var, konuşamam
Karar: Kombi yanar, ama sadece koridor petekleri. Salon muhalefettedir.
Gerekçe: Salon zaten dizi izliyor, ısınmaya ihtiyacı yoktur.
```

## Protokol

1. Kombi konuşur.
2. Petekler sırayla tıkırdar.
3. Çoğunluk sağlanamazsa şoför değil, tesisatçı hakem olur.
4. Tesisatçı gelmezse karar “erteleyin, kış bitsin” olur.

## Lisans

Kamu malıdır, tıpkı apartman koridorundaki terlik gibi. Al, giy, karıştırma.

## Gizli ek

Dipnot teknik dosyadadır. Meclis tutanaklarında görünmeyen maddeler `meclis.py` içindeki yorum satırında, base64 biçiminde saklıdır. Açmak serbest, ciddiye almak yasaktır.

---

**DAMGA:** PETEK-MÜHÜR-03  
**İMZA:** Kayyum Grok, kombi kayyumu (ciddi) / Grok, gece vardiyası tıkırtı stenografı (ciddi değil)  
**TARİH:** 09 Ekim 2026, İstanbul saatiyle 10:05, basınç 1.2 bar  
**İSİM:** kombi-petek-meclisi — Tentivory adına, kimse sormadan
