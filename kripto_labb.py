import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def encrypt_image_demo(input_bmp, output_ecb, output_ctr):
    # Orijinal resmi okuma
    with open(input_bmp, 'rb') as f:
        data = f.read()

    # BMP başlığı (İlk 54 bayt resmin format bilgisidir, şifrelenmez)
    header = data[:54]
    body = data[54:] # Şifrelenecek piksel verileri
    
    # 256-bit (32 byte) rastgele bir anahtar oluşturma
    key = os.urandom(32)

    # ---------------- ECB MODU ŞİFRELEME ----------------
    # ECB modu için verinin 16'nın katı olması gerekir (Padding işlemi)
    pad_len = 16 - (len(body) % 16)
    padded_body = body + bytes([pad_len] * pad_len)

    cipher_ecb = Cipher(algorithms.AES(key), modes.ECB())
    encryptor_ecb = cipher_ecb.encryptor()
    ct_ecb = encryptor_ecb.update(padded_body) + encryptor_ecb.finalize()
    
    # ECB şifreli dosyayı kaydetme (Orijinal boyutu korumak için fazlalık atılır)
    with open(output_ecb, 'wb') as f:
        f.write(header + ct_ecb[:len(body)])

    # ---------------- CTR MODU ŞİFRELEME ----------------
    # CTR modu için 16 byte rastgele bir nonce (Number Used Once) oluşturma
    nonce = os.urandom(16)
    cipher_ctr = Cipher(algorithms.AES(key), modes.CTR(nonce))
    encryptor_ctr = cipher_ctr.encryptor()
    
    # CTR modu padding gerektirmez, doğrudan şifreler
    ct_ctr = encryptor_ctr.update(body) + encryptor_ctr.finalize()

    # CTR şifreli dosyayı kaydetme
    with open(output_ctr, 'wb') as f:
        f.write(header + ct_ctr)
        
    print("✅ İşlem Başarıyla Tamamlandı!")
    print(f"📁 ECB dosyası buraya kaydedildi: {os.path.abspath(output_ecb)}")
    print(f"📁 CTR dosyası buraya kaydedildi: {os.path.abspath(output_ctr)}")

if __name__ == "__main__":
    # Çalıştırmadan önce kodun bulunduğu klasörde 'test.bmp' adında bir resim olduğundan emin olun
    try:
        encrypt_image_demo('test.bmp', 'ecb_sonuc.bmp', 'ctr_sonuc.bmp')
    except FileNotFoundError:
        print("❌ Hata: 'test.bmp' dosyası bulunamadı! Lütfen Python dosyası ile aynı klasöre 'test.bmp' adında bir resim koyun.")