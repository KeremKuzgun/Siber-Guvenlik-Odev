import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Ortak değişkenler
key = os.urandom(32) # 256-bit rastgele anahtar
msg = b"Tutar: 100 TL"

print(f"Orijinal Mesaj: {msg.decode()}")
print("-" * 50)

# ==========================================
# 1. BÖLÜM: CTR Modunda Anahtarsız Değişim
# ==========================================
nonce_ctr = os.urandom(16)
cipher_ctr = Cipher(algorithms.AES(key), modes.CTR(nonce_ctr))
encryptor = cipher_ctr.encryptor()

# Şifreleme (Bytearray yapıyoruz ki içindeki baytları kurcalayabilelim)
ct_ctr = bytearray(encryptor.update(msg) + encryptor.finalize())
print("1) CTR Modu: Mesaj başarıyla şifrelendi.")

# SALDIRI: '1' karakterini (index 7) '9' yapmak için XOR işlemi uyguluyoruz
# Saldırgan anahtarı bilmiyor, sadece '1'in 7. sırada olduğunu biliyor!
ct_ctr[7] ^= (ord('1') ^ ord('9'))
print("2) CTR Modu: Şifreli metin anahtarsız olarak manipüle edildi!")

# Şifre Çözme (Kurban manipüle edilmiş veriyi kendi anahtarıyla açıyor)
decryptor = cipher_ctr.decryptor()
pt_ctr = decryptor.update(ct_ctr) + decryptor.finalize()
print(f"🚨 CTR Çözülen Mesaj: {pt_ctr.decode()} (BÜYÜK ZAFİYET!)")
print("-" * 50)

# ==========================================
# 2. BÖLÜM: AES-GCM İle Aynı Saldırıyı Deneme
# ==========================================
aesgcm = AESGCM(key)
nonce_gcm = os.urandom(12)

# Şifreleme
ct_gcm = bytearray(aesgcm.encrypt(nonce_gcm, msg, None))
print("3) AES-GCM Modu: Mesaj başarıyla şifrelendi.")

# AYNI SALDIRI: Şifreli metni tekrar kurcalıyoruz
ct_gcm[7] ^= (ord('1') ^ ord('9'))
print("4) AES-GCM Modu: Şifreli metin kurcalandı, çözülmeye çalışılıyor...")

# Şifre Çözme
try:
    pt_gcm = aesgcm.decrypt(nonce_gcm, ct_gcm, None)
    print(pt_gcm.decode())
except Exception as e:
    print(f"🛡️ AES-GCM Hatası Yakaladı: {type(e).__name__}")
    print("Sonuç: GCM değişikliği fark etti ve işlemi reddetti!")