# Mac için Türkçe Otomatik Düzeltme

*🇬🇧 For the English version, see [README.md](README.md).*

İngilizce klavyede Türkçe yazın — bu küçük uygulama harfleri sizin yerinize,
siz yazarken otomatik olarak düzeltir.

Örneğin şunu yazdığınızda:

> bugun cok guzel bir gun

anında şuna dönüşür:

> bugün çok güzel bir gün

Mac'inizin her yerinde çalışır — tarayıcıda, Mail'de, WhatsApp'ta, tüm
uygulamalarda. Menü çubuğundan (ekranın sağ üst köşesindeki küçük simgeler
sırası) tek tıkla açıp kapatabilirsiniz.

- Menü çubuğunda **TR·off** görünüyorsa uygulama şu an hiçbir şey yapmıyor
  demektir.
- **TR·on** görünüyorsa siz yazarken aktif olarak düzeltme yapıyordur.

Kapalıyken yazdıklarınıza kesinlikle dokunulmaz.

---

## Gerekenler

- Bir Mac (macOS).
- Python 3. Çoğu Mac'te zaten kuruludur; yoksa
  [python.org](https://www.python.org/downloads/) adresinden
  indirebilirsiniz.
- Aşağıdaki tek seferlik kurulum için yaklaşık 5 dakika.

## Tek seferlik kurulum

Birkaç komutu **Terminal** uygulamasına kopyalayıp yapıştırmanız gerekecek
(ekranın sağ üstündeki büyüteç aramasıyla bulabilirsiniz — `Cmd + Boşluk`
tuşlarına basın, "Terminal" yazın, Enter'a basın).

**1. Adım — Uygulamayı indirin.** Terminal'e şunu yapıştırıp Enter'a basın:

```bash
git clone https://github.com/eicyer/os-turkish-deasciifier.git
cd os-turkish-deasciifier
```

**2. Adım — Gerekli bileşenleri kurun.** Şu satırları yapıştırıp Enter'a
basın:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Bu, uygulamanın ihtiyaç duyduğu her şeyi içeren `venv` adlı özel bir klasör
oluşturur. Mac'inizde başka hiçbir şeyi değiştirmez.

**3. Adım — Başlatın:**

```bash
python app.py
```

Ekranın üstündeki menü çubuğunda **TR·off** yazısını görmelisiniz. 🎉

**4. Adım — İzin verin (önemli!).** İlk çalıştırdığınızda, siz izin verene
kadar macOS uygulamanın tuş vuruşlarını görmesini engeller. Bir sonraki
bölüme bakın.

## macOS izinlerini verme

Uygulamanın yazdıklarınızı okuyup düzeltebilmesi için macOS **iki** ayrı
yerde izin vermenizi ister. Bu tek seferlik bir işlemdir.

1. **Sistem Ayarları → Gizlilik ve Güvenlik → Erişilebilirlik** bölümünü
   açın.
2. **+** düğmesine tıklayın (önce Mac parolanızı girmeniz gerekebilir).
3. Açılan dosya seçicide `Cmd + Shift + G` tuşlarına basın, uygulamanın
   Python yolunu yapıştırıp Enter'a basın. Bu yolu bulmak için uygulamanın
   klasöründeyken Terminal'de şunu çalıştırın:
   ```bash
   venv/bin/python3 -c "import sys; print(sys.executable)"
   ```
   Yazdırdığı satırı kopyalayın — eklenecek yol budur.
4. Yeni eklenen öğenin yanındaki anahtarın **açık** olduğundan emin olun.
5. Aynı işlemi **Sistem Ayarları → Gizlilik ve Güvenlik → Giriş İzleme**
   bölümünde de tekrarlayın.
6. Bu listelerden herhangi birinde **Terminal** de görünüyorsa onu da açın —
   bazı macOS sürümleri izni Terminal'e atayabiliyor.
7. Uygulamayı kapatıp yeniden başlatın (izinler ancak yeniden başlatınca
   etkili olur).

> **Yazarken hiçbir şey olmuyor mu?** Neredeyse her zaman bu iki izinden
> biri eksiktir. İki listeyi de tekrar kontrol edin.

## Kullanım

1. Menü çubuğunda **TR·off** yazısına tıklayın.
2. **Enabled** seçeneğine tıklayıp işaretlenmesini sağlayın. Başlık
   **TR·on** olur.
3. Herhangi bir yerde yazın — boşluk, Enter veya noktalama işaretine
   bastığınız anda kelimeler düzeltilir.
4. Ara vermek için **Enabled**'a tekrar tıklayın (**TR·off**'a döner).
5. Tamamen kapatmak için menü çubuğu simgesine tıklayıp **Quit** seçin.

### Deneyin

**TextEdit** uygulamasını açın, yeni bir belge başlatın ve
`bugun cok guzel bir gun ` yazın (sonunda bir boşluk olsun). Yazı
`bugün çok güzel bir gün ` haline gelmelidir.

## Otomatik başlatma (önerilir)

Uygulamayı her seferinde elle başlatmak yerine, Mac'inizin oturum
açtığınızda otomatik başlatmasını sağlayabilirsiniz. Uygulamanın
klasöründeyken Terminal'de şunu çalıştırın:

```bash
./install-launchagent.sh
```

Hepsi bu — artık oturum açtıktan birkaç saniye sonra **TR·off** simgesi
kendiliğinden belirir, Terminal penceresine gerek kalmaz. Uygulama bir gün
çökerse macOS onu sessizce yeniden başlatır.

Bu mod hakkında bilinmesi gereken birkaç şey:

- **Quit gerçekten kapatır.** Menü çubuğundan **Quit** seçmek otomatik
  başlatmayı da devre dışı bırakır; böylece uygulama anında geri gelmez.
- **Quit'ten sonra geri getirmek için** Finder'da uygulamanın klasöründeki
  **`TurkishAutocorrect.command`** dosyasına çift tıklayın veya
  `./install-launchagent.sh` komutunu yeniden çalıştırın.
- **Bir sorun olursa** hata mesajları ekranda gösterilmek yerine uygulama
  klasöründeki `tr-autocorrect.log` dosyasına kaydedilir.
- Kapalıyken bile az miktarda bellek kullanır — diğer küçük menü çubuğu
  araçlarıyla benzer düzeyde.

Otomatik başlatmayı tamamen kaldırmak için:

```bash
./uninstall-launchagent.sh
```

## Bilinmesi iyi olur (mevcut sınırlamalar)

- Kelimenin ortasında imleci hareket ettirirseniz (ok tuşları, başka bir
  yere tıklama), yanlış düzeltme riskine girmemek için o kelimeye
  dokunulmaz.
- İçinde rakam olan kelimeler (örneğin `gun2`) düzeltilmez.
- Düzeltme bağlama duyarlıdır ama kusursuz değildir — nadiren bir kelime
  istemediğiniz şekilde düzeltilebilir. Silip, düzeltmeyi kapatarak yeniden
  yazmanız yeterli.

## Meraklısına: nasıl çalışır

- Menü çubuğu simgesi ve menü
  [`rumps`](https://github.com/jaredks/rumps) ile oluşturulur.
- Tuş vuruşları sistem genelinde (engellenmeden)
  [`pynput`](https://github.com/moses-palmer/pynput) ile izlenir.
- Açıkken uygulama, o an yazmakta olduğunuz kelimenin harflerini biriktirir.
  Her kelime sınırında (boşluk, noktalama, Enter, Tab) kelimeyi
  [`turkish-deasciifier`](https://github.com/emres/turkish-deasciifier)
  kütüphanesinden geçirir — bu, Deniz Yüret'in bağlam tabanlı Türkçe
  deasciification algoritmasının Python uyarlamasıdır. Sonuç farklıysa,
  ASCII kelimeyi silmek için backspace gönderir ve yerine düzeltilmiş
  Türkçe kelimeyi yazar.
- Bu kütüphane PyPI'da yayımlanmadığı için `requirements.txt` onu doğrudan
  GitHub'dan kurar.
- `install-launchagent.sh`, uygulamayı `RunAtLoad` ve `KeepAlive`
  özellikleriyle kullanıcıya özel bir macOS **LaunchAgent** olarak kaydeder
  (`~/Library/LaunchAgents/com.github.eicyer.tr-autocorrect.plist`); oturum
  açılışında başlama ve çökünce yeniden başlama bunun sayesindedir.

## İleride yapılabilecekler

- `py2app` ile bağımsız bir `.app` olarak paketlemek; böylece hiç Terminal
  kurulumu gerekmez.
- `TR·on` / `TR·off` yazısı yerine gerçek bir menü çubuğu simgesi.
