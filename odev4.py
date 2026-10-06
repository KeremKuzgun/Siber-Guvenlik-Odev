import time
import hashlib
from argon2 import PasswordHasher

password = b"kriptografi_lab_2026"
tekrar = 100000 # SHA-256'nın hızını belirgin şekilde görmek için 100 bin döngü

print("Ölçümler başlatılıyor, bilgisayarının işlemci hızına göre 1-2 saniye sürebilir...\n")

# --- SHA-256 Hız Ölçümü ---
start_sha = time.time()
for _ in range(tekrar):
    hashlib.sha256(password).hexdigest()
sha_total = time.time() - start_sha
sha_tekli_sure = sha_total / tekrar

print(f"SHA-256 ile {tekrar} adet hash oluşturma süresi: {sha_total:.4f} saniye")
print(f"SHA-256 TEKLİ Hash Süresi: {sha_tekli_sure:.8f} saniye\n")

# --- Argon2id Hız Ölçümü ---
# Argon2id zaten donanımı yorduğu için tek bir döngü yeterlidir
ph = PasswordHasher()
start_argon = time.time()
ph.hash(password.decode())
argon_sure = time.time() - start_argon

print(f"Argon2id TEKLİ Hash Süresi: {argon_sure:.4f} saniye\n")

# --- Karşılaştırma ---
fark = int(argon_sure / sha_tekli_sure)
print(f"🚨 SONUÇ: Argon2id, SHA-256'dan yaklaşık {fark:,} kat daha yavaş çalışıyor!")