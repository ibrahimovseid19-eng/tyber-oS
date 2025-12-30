# Teybr oS APK Yapım Kılavuzu

Teybr oS uygulamanızı bir Android APK dosyasına dönüştürmek için aşağıdaki adımları takip etmelisiniz. Bu işlem bilgisayarınızda **Flutter** ve **Android Geliştirme Araçlarının** kurulu olmasını gerektirir.

## Gereksinimler

1.  **Flutter SDK**: Google'ın UI geliştirme kiti.
2.  **Android SDK & Araçları**: Android Studio üzerinden kurulur.
3.  **Python & Flet**: Zaten projenizde mevcut.

## Adım 1: Flutter Kurulumu (Eğer kurulu değilse)

1.  [Flutter Windows Kurulum](https://docs.flutter.dev/get-started/install/windows) sayfasına gidin.
2.  Flutter SDK zip dosyasını indirin ve örneğin `C:\src\flutter` gibi bir yere çıkartın.
3.  Bilgisayarınızın "Ortam Değişkenleri" (Environment Variables) ayarlarına gidin ve `Path` değişkenine `C:\src\flutter\bin` yolunu ekleyin.
4.  Terminali kapatıp açın ve şu komutu çalıştırın:
    ```bash
    flutter doctor
    ```
    Bu komut eksik olan diğer araçları (Android Studio vb.) size söyleyecektir.

## Adım 2: Android Studio Kurulumu

1.  `flutter doctor` çıktısında Android Studio eksik görünüyorsa, [Android Studio İndir](https://developer.android.com/studio) sayfasından indirip kurun.
2.  Kurulum sırasında "Android SDK", "Android SDK Command-line Tools" ve "Android SDK Build-Tools" seçeneklerinin işaretli olduğundan emin olun.
3.  Kurulum bittikten sonra tekrar `flutter doctor` çalıştırın ve tüm onay işaretlerinin yeşil olduğundan emin olun.

## Adım 3: APK Oluşturma

Tüm kurulumlar tamamsa, Teybr oS klasöründe terminali açın ve şu komutu girin:

```bash
flet build apk
```

Bu komut:
- Projenizi analiz eder.
- Gerekli tüm Python ve kütüphane dosyalarını paketler.
- Sonunda bir `.apk` dosyası üretir.

Oluşan dosya genellikle `build/app/outputs/flutter-apk/app-release.apk` yolunda bulunur.

## Alternatif: GitHub Actions (Kurulum yapmadan)

Eğer bilgisayarınıza bu kadar büyük programlar kurmak istemiyorsanız:

1.  Projenizi GitHub'a yükleyin.
2.  GitHub reponuzda `.github/workflows/build_apk.yml` adında bir dosya oluşturun.
3.  İçerisine Flet'in hazır build şablonunu yapıştırın (Flet dökümanlarında bulunur).
4.  Git'e "push" yaptığınızda GitHub sunucuları sizin için APK'yı üretip "Releases" kısmına koyacaktır.
