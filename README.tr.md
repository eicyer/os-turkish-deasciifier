# Mac için Türkçe Otomatik Düzeltme

*🇬🇧 For the English version, see [README.md](README.md).*

İngilizce klavyede Türkçe yazın — bu küçük menü çubuğu uygulaması harfleri
sizin yerinize, siz yazarken otomatik olarak düzeltir.

Örneğin şunu yazdığınızda:

> bugun cok guzel bir gun

anında şuna dönüşür:

> bugün çok güzel bir gün

Mac'inizin her yerinde çalışır — tarayıcıda, Mail'de, WhatsApp'ta, tüm
uygulamalarda. Menü çubuğundan (ekranın sağ üst köşesindeki küçük simgeler
sırası) tek tıkla açıp kapatabilirsiniz; burada küçük bir **ğ** olarak
görünür — bu uygulamanın sizin için eklediği harfin ta kendisi.

- Soluk, silik bir **ğ** uygulamanın şu an hiçbir şey yapmadığı anlamına
  gelir.
- Koyu, dolu bir **ğ** siz yazarken aktif olarak düzeltme yaptığı anlamına
  gelir.

Kapalıyken yazdıklarınıza kesinlikle dokunulmaz.

---

## İndirme (herkes için — Terminal gerekmez)

1. [En son sürüm](https://github.com/eicyer/os-turkish-deasciifier/releases/latest)
   sayfasına gidip `TurkishAutocorrect.dmg` dosyasını indirin.
2. İndirdiğiniz `.dmg` dosyasını açın, ardından **TurkishAutocorrect**
   simgesini yanındaki **Applications** klasör kısayoluna sürükleyin.
3. **Applications** klasörünü açıp **TurkishAutocorrect**'e çift tıklayın.
   - Bu uygulama App Store'da satılmadığı ve Apple tarafından ücretli olarak
     imzalanmadığı için, macOS ilk seferinde muhtemelen
     *"Apple TurkishAutocorrect'in zararlı yazılım içermediğini
     doğrulayamadı"* benzeri bir mesajla engelleyecektir. Bu beklenen bir
     durumdur — izin vermek için: **Sistem Ayarları → Gizlilik ve
     Güvenlik**'i açın, en alta doğru kaydırıp güvenlik uyarısını bulun,
     **Yine de Aç**'a tıklayın, ardından açılan pencerede **Aç**'ı
     onaylayın. Bunu yalnızca bir kez yapmanız yeterli.
4. Menü çubuğunda soluk bir **ğ** görmelisiniz. Tıklayıp **Enabled**
   seçeneğini işaretleyerek düzeltmeyi açın — simge koyulaşır. 🎉
5. Uygulama tuş vuruşlarınızı dinlemeye çalıştığında macOS iki izin
   isteyecektir — her istekte **Sistem Ayarları'nı Aç**'a tıklayın (veya
   oraya elle gidin) ve **TurkishAutocorrect**'i şu bölümlerde açın:
   - **Gizlilik ve Güvenlik → Erişilebilirlik**
   - **Gizlilik ve Güvenlik → Giriş İzleme**

   Bir istek görmüyorsanız ve düzeltme hiçbir şey yapmıyorsa, bu iki listeyi
   doğrudan kontrol edin — anahtar muhtemelen hâlâ kapalıdır.
6. Her oturum açtığınızda otomatik çalışsın mı? Menü çubuğu simgesine
   tıklayıp **Start at Login**'i işaretleyin.

Hepsi bu kadar — Python, `git clone`, Terminal gerekmez. Bu noktadan sonraki
bölümler, uygulamayı kaynak koddan geliştirenler içindir.

## Kullanım

1. Menü çubuğunda **ğ** simgesine tıklayın.
2. **Enabled**'ı işaretleyin — simge koyulaşır.
3. Herhangi bir yerde yazın — boşluk, Enter veya noktalama işaretine
   bastığınız anda kelimeler düzeltilir.
4. Ara vermek için **Enabled**'ın işaretini kaldırın (simge tekrar
   soluklaşır).
5. **Quit** düzeltmeyi kapatır ama simge menü çubuğunda kalır — böylece onu
   tekrar açacak bir menü olmadan asla kalmazsınız; uygulamadan tamamen
   çıkmaz. **Start at Login**'i açtıysanız arka plan süreci de çalışmaya
   devam eder, böylece tekrar etkinleştirdiğinizde hazırdır.

### Deneyin

**TextEdit** uygulamasını açın, yeni bir belge başlatın ve
`bugun cok guzel bir gun ` yazın (sonunda bir boşluk olsun). Yazı
`bugün çok güzel bir gün ` haline gelmelidir.

## Nasıl çalışır

- Menü çubuğu simgesi ve menü
  [`rumps`](https://github.com/jaredks/rumps) ile oluşturulur.
- Tuş vuruşları sistem genelinde (engellenmeden)
  [`pynput`](https://github.com/moses-palmer/pynput) ile izlenir.
- Açıkken uygulama, o an yazmakta olduğunuz kelimenin harflerini biriktirir.
  Her kelime sınırında (boşluk, noktalama, Enter, Tab) kelimeyi
  [`turkish-deasciifier`](https://github.com/emres/turkish-deasciifier)
  kütüphanesinden geçirir — bu, Deniz Yüret'in bağlam tabanlı Türkçe
  deasciification algoritmasının Python uyarlamasıdır (böylece çevredeki
  harflere göre `güzel` ile `gzel` arasındaki farkı doğru seçer). Sonuç
  farklıysa, ASCII kelimeyi silmek için backspace gönderir ve yerine
  düzeltilmiş Türkçe kelimeyi yazar.
- Bu kütüphane PyPI'da yayımlanmadığı için `requirements.txt` onu doğrudan
  `git+https://github.com/emres/turkish-deasciifier.git` üzerinden kurar.
- İndirilebilir `.app`, kendi Python yorumlayıcısını da içine gömen
  [`py2app`](https://py2app.readthedocs.io/) ile derlenir (bkz. `setup.py`)
  — böylece kullanıcıların Python kurulu olmasına gerek kalmaz.

## Bilinmesi iyi olur (mevcut sınırlamalar)

- Kelimenin ortasında imleci hareket ettirirseniz (ok tuşları, başka bir
  yere tıklama), yanlış düzeltme riskine girmemek için o kelimeye
  dokunulmaz.
- İçinde rakam olan kelimeler (örneğin `gun2`) düzeltilmez.
- Düzeltme bağlama duyarlıdır ama kusursuz değildir — nadiren bir kelime
  istemediğiniz şekilde düzeltilebilir. Silip, düzeltmeyi kapatarak yeniden
  yazmanız yeterli.
- Enjekte edilen backspace/yeniden yazma ile bir sonraki tuş vuruşunuzun
  teorik olarak iç içe geçebileceği küçük bir an vardır; pratikte
  gözlemlenmedi ama bozuk bir çıktı görürseniz bilmekte fayda var.

## İleride yapılabilecekler

- Finder/Dock için özel bir `.icns` uygulama simgesi (şu an py2app'in genel
  varsayılanı kullanılıyor) — menü çubuğu simgesinden ayrı, onun kendi
  tasarımı zaten var (yukarı bakın).
- Gatekeeper'ın "Yine de Aç" adımını tamamen ortadan kaldırmak için ücretli
  bir Apple Developer hesabıyla sürümü notarize etmek.

---

## Kaynaktan çalıştırma (geliştiriciler / katkıda bulunanlar)

Bu noktadan sonrası uygulamayı derlemek veya değiştirmek isteyenler
içindir. Sadece kullanmak istiyorsanız yukarıdaki
[İndirme](#i̇ndirme-herkes-için--terminal-gerekmez) bölümüne bakın.

### Gerekenler

- Bir Mac (macOS).
- Python 3. Çoğu Mac'te zaten kuruludur; yoksa
  [python.org](https://www.python.org/downloads/) adresinden
  indirebilirsiniz.

### Tek seferlik kurulum

**1. Depoyu klonlayın:**

```bash
git clone https://github.com/eicyer/os-turkish-deasciifier.git
cd os-turkish-deasciifier
```

**2. Gerekli bileşenleri kurun:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Bu, uygulamanın ihtiyaç duyduğu her şeyi içeren `venv` adlı özel bir klasör
oluşturur; Mac'inizde başka hiçbir şeyi değiştirmez.

### Başlatma

```bash
source venv/bin/activate
python app.py
```

Menü çubuğunda soluk bir **ğ** görmelisiniz. Tıklayıp **Enabled**'ı
işaretleyerek düzeltmeyi açın.

#### Arka planda otomatik çalıştırma (önerilir)

`app.py`'yi her seferinde elle başlatmak yerine, macOS'un oturum
açtığınızda otomatik başlatması ve çökerse yeniden başlatması
(`KeepAlive`) için kullanıcıya özel bir **LaunchAgent** olarak kaydedin:

```bash
./install-launchagent.sh
```

Bu, `~/Library/LaunchAgents/com.github.eicyer.tr-autocorrect.plist`
dosyasını yazar ve uygulamayı hemen başlatır — birkaç saniye içinde menü
çubuğunda soluk bir **ğ** görünmelidir, bundan sonra Terminal penceresine
gerek kalmaz.

Arka plan sürecini tamamen durdurmak için (örneğin kaldırmadan veya kodu
güncellemeden önce):

```bash
./uninstall-launchagent.sh
```

Bu, süreci durdurur ve plist dosyasını siler, böylece bir sonraki oturum
açılışında geri gelmez. Geri getirmek için `./install-launchagent.sh`'i
tekrar çalıştırın (veya `TurkishAutocorrect.command` dosyasına çift
tıklayın).

Bu şekilde çalıştırmanın bilinmesi gereken artı/eksileri:
- Erişilebilirlik/Giriş İzleme izinleri, sadece uygulamayı açıkken değil,
  sürekli olarak verilmiş sayılır.
- **Enabled** kapalıyken bile, siz kaldırana kadar az miktarda CPU/bellek
  kullanılmaya devam eder.
- Uygulama başlangıçta başarısız olursa, `launchd` anında değil ~10
  saniyede bir (`ThrottleInterval`) yeniden dener.
- Ekli bir Terminal penceresi olmadığından, hatalar stdout yerine bu
  klasördeki `tr-autocorrect.log` dosyasına yazılır — bir şey çalışmıyorsa
  oraya bakın.

Arka plan süreci olarak çalıştırmak istemiyorsanız, `python app.py`'yi her
seferinde elle çalıştırın — durdurmak için çalıştığı Terminal penceresinde
`Ctrl+C` kullanmanız gerekir.

### macOS izinlerini verme (kaynaktan çalıştırırken)

Bu bölüm, iznin ham yorumlayıcı binary'sine verilmesi gereken yukarıdaki
`python app.py` / venv iş akışı içindir. İndirilen `.app`'i kurduysanız,
yukarıdaki [İndirme](#i̇ndirme-herkes-için--terminal-gerekmez) bölümündeki
daha basit adımları kullanın — oradaki izin isteği doğrudan
**TurkishAutocorrect** olarak etiketlenir.

İki ayrı gizlilik izni söz konusudur:

1. **Erişilebilirlik** — backspace/yeniden yazma tuş vuruşlarını simüle
   etmek için gerekir.
2. **Giriş İzleme** — sistem genelinde tuş dinleme yapan her uygulama için
   macOS Catalina'dan beri gereklidir.

Adımlar:

1. **Sistem Ayarları → Gizlilik ve Güvenlik → Erişilebilirlik** bölümünü
   açın.
2. **+** düğmesine tıklayın (önce Mac parolanızı girmeniz gerekebilir).
3. Açılan dosya seçicide `Cmd + Shift + G` tuşlarına basın, venv'inizin
   Python yolunu yapıştırıp Enter'a basın. Bu yolu bulmak için uygulamanın
   klasöründeyken Terminal'de şunu çalıştırın:
   ```bash
   venv/bin/python3 -c "import sys; print(sys.executable)"
   ```
   Yazdırdığı satırı kopyalayın — eklenecek yol budur.
4. Yeni eklenen öğenin yanındaki anahtarın **açık** olduğundan emin olun.
5. Aynı işlemi **Sistem Ayarları → Gizlilik ve Güvenlik → Giriş İzleme**
   bölümünde de tekrarlayın.
6. Bu listelerden herhangi birinde **Terminal** de görünüyorsa (veya
   `python app.py`'yi başlattığınız başka bir uygulama) onu da açın — bazı
   macOS sürümleri izni Terminal'e atayabiliyor.
7. Uygulamayı kapatıp yeniden başlatın (`Ctrl+C`, ardından tekrar
   `python app.py`) — izin değişiklikleri genellikle sürecin yeniden
   başlamasını gerektirir.

> **Yazarken hiçbir şey olmuyor mu?** Neredeyse her zaman bu iki izinden
> biri eksiktir. İki listeyi de tekrar kontrol edin.

### İndirilebilir `.app`'i derleme

```bash
source venv/bin/activate
pip install py2app
python3 setup.py py2app
```

`dist/TurkishAutocorrect.app` dosyasını üretir. Bunun nasıl derlendiği,
ad-hoc imzalandığı, bir DMG'ye paketlendiği ve bir `v*.*.*` etiketi
gönderildiğinde GitHub Releases'e otomatik olarak yayınlandığı için
`.github/workflows/release.yml` dosyasına bakın.
