SHODAN_API_KEY = None
import socket
import requests
import whois
import sys
import ssl
import datetime
import json
import time
import os
import warnings
from urllib.parse import urlparse
import ipaddress
import dns.resolver
from threading import Thread
import shutil

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
from rich.live import Live
from rich.box import MINIMAL
from rich.style import Style
from rich.prompt import Prompt
from rich.syntax import Syntax
from rich.spinner import Spinner

# --- Rich Console Tanımlaması ---
console = Console()

# --- Global Değişkenler ---
target = None  # Mevcut hedef
SHODAN_API_KEY = "tQnS0KoDH8FJl4VZAsYzLNj26gG1RUaH"  # Buraya kendi Shodan API anahtarınızı girin.
# Not: production ortamında API anahtarlarını ortam değişkeni olarak veya güvenli bir yapılandırma dosyasında tutmak daha güvenlidir.

# Sosyal Medya Platformları (Daha Kapsamlı Hale Getirildi)
SOCIAL_MEDIA_PLATFORMS = {
    "TikTok": "https://www.tiktok.com/@{}",
    "Instagram": "https://www.instagram.com/{}",
    "Twitter (X)": "https://twitter.com/{}",
    "Facebook": "https://www.facebook.com/{}",
    "GitHub": "https://github.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Pinterest": "https://www.pinterest.com/{}",
    "Tumblr": "https://{}.tumblr.com",
    "YouTube": "https://www.youtube.com/@{}", # Kullanıcı adı için daha uygun format
    "Snapchat": "https://www.snapchat.com/add/{}",
    "LinkedIn": "https://www.linkedin.com/in/{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Discord": "https://discord.com/users/{}", # Discord kullanıcı profilleri doğrudan bu şekilde taranması zor, örnek için tutuldu
    "Medium": "https://medium.com/@{}",
    "Vimeo": "https://vimeo.com/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Flickr": "https://www.flickr.com/photos/{}",
    "Dribbble": "https://dribbble.com/{}",
    "Behance": "https://www.behance.net/{}",
    "DeviantArt": "https://www.deviantart.com/{}",
    "Quora": "https://www.quora.com/profile/{}",
    "StackOverflow": "https://stackoverflow.com/users/{}",
    "Wordpress": "https://{}.wordpress.com",
    "Blogspot": "https://{}.blogspot.com",
    "Etsy": "https://www.etsy.com/shop/{}",
    "eBay": "https://www.ebay.com/usr/{}",
    "TwitchTracker": "https://twitchtracker.com/{}"
}

social_media_results = {}
stop_social_media_search = False

# urllib3 InsecureRequestWarning'lerini kapat
warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

# --- Açılış Animasyonu (Geliştirilmiş ve Profesyonelleştirilmiş) ---
def welcome_animation():
    os.system('cls' if os.name == 'nt' else 'clear')

    # ASCII Sanat Başlık (Daha Büyük ve Şık)
    header_art = Text.from_ansi(
        """
       

Ｓｙｓｔｅｍｉｃ Ｅｌｉｔｅ Ｓａｂｏｔａｇｅ Ｎｅｘｕｓ
   
Ｓｏｎｓｕｚ Ｅｒｉｓｉｍ ｖｅ Ｓａｌｄıｒı Ｎｏｋｔａｓı
        """
    , style="bold magenta")
    
    intro_text = Text(
        "\nSiber Güvenlik Uzmanları için Gelişmiş ve OSINT Platformu",
        style="italic bright_yellow", justify="center"
    )

    # Başlık ve Giriş metni için paneller
    header_panel = Panel(
        Align.center(header_art),
        border_style="bold green",
        title="[bold bright_cyan]ReconOps Command Line Interface[/bold bright_cyan]",
        title_align="center",
        expand=False
    )

    intro_panel = Panel(
        intro_text,
        border_style="bright_blue",
        title="[bold yellow]Hoş Geldiniz![/bold yellow]",
        title_align="center",
        expand=False
    )

    console.print(header_panel)
    console.print(intro_panel)

    # Yüklenme animasyonu
    with Progress(
        SpinnerColumn("dots"), # Daha şık bir spinner
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console
    ) as progress:
        task = progress.add_task("[bold green]Modüller yükleniyor ve sistem başlatılıyor...[/bold green]", total=100)
        for _ in range(20):
            time.sleep(0.05)
            progress.update(task, advance=5)
        
        progress.update(task, description="[bold green]Güvenlik politikaları kontrol ediliyor...[/bold green]", advance=0)
        time.sleep(2)
        progress.update(task, description="[bold green]Arayüz hazırlanıyor, lütfen bekleyin...[/bold green]", advance=0)
        time.sleep(2)
        
    console.print("\n[bold bright_green]Başarılı! ReconOps CLI Kullanıma Hazır.[/bold bright_green]\n")
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear') # Tekrar temizle

# --- Yardım ve Hedef Yönetimi ---
def show_help():
    console.print("\n[bold cyan]Mevcut Komutlar:[/bold cyan]")
    cmds = [
        ("set target <value>", "Hedef alan adını veya IP'yi ayarlar"),
        ("show target", "Mevcut ayarlı hedefi gösterir"),
        # --- Orijinal Komutlar ---
        ("dns", "DNS kayıtlarını sorgular"),
        ("whois", "Whois bilgilerini gösterir"),
        ("geoip", "GeoIP konum bilgilerini gösterir"),
        ("headers", "HTTP başlıklarını gösterir"),
        ("robots", "robots.txt içeriğini gösterir"),
        ("subdomains", "Alt domainleri tarar"),
        ("ssl", "SSL sertifika bilgilerini alır"),
        ("shodan", "Shodan API ile bilgi toplar"),
        ("dirscan", "Web dizinlerini tarar"),
        ("portscan", "Portları tarar"),
        ("ping", "Ping testi yapar"),
        ("traceroute", "Ağ yolunu izler"),
        ("scan-report", "Nmap + Nikto raporu üretir"),
        ("usersearch <username>", "Sosyal medyada kullanıcı arar"),
        # --- OSINT Komutları ---
        ("ipinfo", "IP bilgilerini gösterir"),
        ("reputation", "VirusTotal reputation"),
        ("techstack", "Teknoloji tespiti"),
        ("crawler", "Linkları çıkarır"),
        ("emailhunter", "E-mail adreslerini bulur"),
        ("asn", "ASN bilgisi"),
        ("sitemap", "Sitemap çıkarır"),
        ("iprange", "IP adresleri gösterir"),
        ("waf", "WAF tespiti"),
        ("perf", "Yanıt süresi ölçümü"),
        ("dnsdump", "Detaylı DNS kayıtları"),
        ("save-report", "Rapor kaydeder"),
        # --- YENİ KOMUTLAR (20+) ---
        ("reverse-ip", "Bir IP'deki tüm domainleri bulur"),
        ("reverse-dns", "IP'nin geri DNS aramasını yapar"),
        ("ct-search", "SSL sertifikatlarından domain arar"),
        ("leakdb <email>", "Sızan veriler için email kontrol eder"),
        ("ip-history", "IP'nin tarihçesini gösterir"),
        ("dns-history", "DNS'in tarihçesini gösterir"),
        ("banner", "Sunucu banner bilgilerini alır"),
        ("cms", "CMS sistemini tespit eder"),
        ("favicon", "Favicon hash analizi"),
        ("port-lite", "Hafif port taraması"),
        ("urlscan", "Tüm URL'leri çıkarır"),
        ("jsfinder", "JavaScript dosyalarını ve sırları bulur"),
        ("admin", "Admin panel yollarını bulur"),
        ("fileleaks", "Açıklanmış dosyaları kontrol eder"),
        ("verify-email <email>", "Email'i doğrular"),
        ("cookie", "Cookie'leri analiz eder"),
        ("os", "İşletim sistemini tespit eder"),
        ("cdn", "CDN kullanımını kontrol eder"),
        ("screenshot", "Sitdenin screenshot'ını alır"),
        ("deep-scan", "Tüm taramaları çalıştırır"),
        # --- Diğer ---
        ("clear", "Ekranı temizler"),
        ("exit", "Çıkar"),
        ("help", "Yardım gösterir"),
    ]
    table = Table(show_header=True, header_style="bold magenta", border_style="magenta", expand=True)
    table.add_column("Komut", style="yellow", no_wrap=True)
    table.add_column("Açıklama", style="green")
    for cmd, desc in cmds:
        table.add_row(cmd, desc)
    console.print(table)

def set_target(val):
    global target
    try:
        # URL'den domain veya IP'yi ayıklama
        if val.startswith("http://") or val.startswith("https://"):
            parsed_url = urlparse(val)
            host = parsed_url.hostname
            if not host:
                raise ValueError("URL'den geçerli bir hostname alınamadı.")
            target = host
        else:
            # Doğrudan IP veya hostname
            try:
                ipaddress.ip_address(val) # IP adresi mi diye kontrol et
                target = val
            except ValueError:
                # IP değilse hostname olarak kabul et
                target = val
        
        if target:
            console.print(f"[bold green][+] Hedef başarıyla ayarlandı:[/bold green] [bold white]{target}[/bold white]")
        else:
            console.print("[red][!] Hedef ayarlanırken bir sorun oluştu. Geçerli bir alan adı veya IP girin.[/red]")
    except Exception as e:
        console.print(f"[red][!] Geçersiz hedef formatı: {e}. Lütfen geçerli bir alan adı, IP veya URL girin.[/red]")

def show_target():
    if target:
        console.print(f"[bold cyan]Mevcut hedef:[/bold cyan] [bold white]{target}[/bold white]")
    else:
        console.print("[red][!] Hedef ayarlanmadı. Lütfen 'set target <hedef>' komutunu kullanın.[/red]")

# --- Mevcut Fonksiyonlar (Hata Yönetimi ve Çıktı İyileştirmeleri) ---
def dns_lookup():
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: DNS Sorgusu for [white]{target}[/white] :::[/bold yellow]")
    
    table = Table(show_header=True, header_style="bold blue", border_style="blue", expand=True)
    table.add_column("Kayıt Tipi", style="green")
    table.add_column("Değer", style="yellow")

    found_any_record = False

    with Progress(
        SpinnerColumn("dots"), TextColumn("[progress.description]{task.description}"), transient=True, console=console
    ) as progress:
        task = progress.add_task("[bold green]DNS kayıtları çözümleniyor...[/bold green]", total=4) # A, MX, NS, TXT

        # A Kaydı (IP Adresi)
        try:
            answers = dns.resolver.resolve(target, 'A')
            for rdata in answers:
                table.add_row("A Kaydı", str(rdata.address))
                found_any_record = True
        except dns.resolver.NoAnswer:
            pass
        except dns.resolver.NXDOMAIN:
            console.print(f"[red][!] DNS sorgusu başarısız: Alan adı bulunamadı ({target}).[/red]")
            progress.update(task, advance=4) # Tüm görevleri tamamla
            return
        except Exception as e:
            console.print(f"[red][!] A kaydı sorgusu sırasında hata:[/red] {e}")
        progress.update(task, advance=1)

        # MX Kaydı (Mail Exchange)
        try:
            answers = dns.resolver.resolve(target, 'MX')
            for rdata in answers:
                table.add_row("MX Kaydı", f"Öncelik: {rdata.preference}, Host: {rdata.exchange}")
                found_any_record = True
        except dns.resolver.NoAnswer:
            pass
        except Exception as e:
            console.print(f"[red][!] MX kaydı sorgusu sırasında hata:[/red] {e}")
        progress.update(task, advance=1)

        # NS Kaydı (Name Server)
        try:
            answers = dns.resolver.resolve(target, 'NS')
            for rdata in answers:
                table.add_row("NS Kaydı", str(rdata.target))
                found_any_record = True
        except dns.resolver.NoAnswer:
            pass
        except Exception as e:
            console.print(f"[red][!] NS kaydı sorgusu sırasında hata:[/red] {e}")
        progress.update(task, advance=1)

        # TXT Kaydı (Metin Kaydı - SPF, DKIM vb.)
        try:
            answers = dns.resolver.resolve(target, 'TXT')
            for rdata in answers:
                # TXT kayıtları bytes olarak dönebilir, decode etmek gerekir
                txt_data = [txt.decode('utf-8') for txt in rdata.strings]
                table.add_row("TXT Kaydı", "\n".join(txt_data))
                found_any_record = True
        except dns.resolver.NoAnswer:
            pass
        except Exception as e:
            console.print(f"[red][!] TXT kaydı sorgusu sırasında hata:[/red] {e}")
        progress.update(task, advance=1)

    if found_any_record:
        console.print(table)
    else:
        console.print("[yellow]Hedef için DNS kaydı bulunamadı.[/yellow]")

    console.print("\n[yellow]Not: DNS sorguları hedefin DNS yapılandırmasına bağlı olarak değişebilir.[/yellow]")

def whois_lookup():
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: Whois Bilgisi for [white]{target}[/white] :::[/bold yellow]")

    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console
    ) as progress:
        task = progress.add_task("[bold green]Whois sorgulanıyor...[/bold green]", total=100)
        try:
            # Varsayılan olarak w'yi None yapalım (farklı yollarla veri alıyoruz)
            w = None
            # Doğrudan whois komutunu çalıştır (varsa)
            import subprocess
            try:
                result = subprocess.run(['whois', target], capture_output=True, text=True, timeout=10)
                whois_data = result.stdout
            except FileNotFoundError:
                # Yerel whois yoksa WHOISXMLAPI'ye POST ile sorgu gönder
                console.print("[yellow]Windows whois komutu bulunamadı. Online sorgu (WHOISXMLAPI) deneniyor...[/yellow]")
                try:
                    api_key = os.environ.get('WHOISXMLAPI_KEY', 'at_YOUR_API_KEY')
                    # WHOISXMLAPI için GET ile sorgu (apiKey ve domainName query parametreleri kullanılır)
                    params = {"apiKey": api_key, "domainName": target, "outputFormat": "JSON"}
                    resp = requests.get('https://www.whoisxmlapi.com/whoisserver/WhoisService', params=params, timeout=12)
                    if resp.status_code == 200:
                        data = resp.json()
                        # rawText alanını al, yoksa WhoisRecord içeriğini JSON olarak al
                        whois_data = data.get('WhoisRecord', {}).get('rawText', '') or json.dumps(data.get('WhoisRecord', {}), indent=2)
                    else:
                        raise Exception(f"WHOIS API yanıt kodu: {resp.status_code}: {resp.text}")
                except Exception as api_exc:
                    console.print(f"[yellow]WHOISXMLAPI başarısız: {api_exc}. python-whois ile deneme yapılıyor...[/yellow]")
                    # Son çare olarak python-whois'i dene (hem query hem whois
                    try:
                        import whois as pywhois
                        try:
                            w = pywhois.query(target)
                            if w is None:
                                # whois() bazen dict döner
                                w = pywhois.whois(target)
                        except Exception:
                            w = pywhois.whois(target)
                        if w:
                            # Eğer bir dict-like nesne döndüyse bunu metne çevir
                            if hasattr(w, 'items'):
                                whois_data = "\n".join([f"{k}: {v}" for k, v in w.items() if v])
                            else:
                                whois_data = str(w)
                        else:
                            raise Exception("Whois verisi alınamadı (python-whois).")
                    except Exception as last_exc:
                        raise Exception(f"Tüm whois yöntemleri başarısız: {last_exc}")

            # Eğer whois_data boşsa hata fırlat
            if not whois_data or str(whois_data).strip() == "":
                raise Exception("Whois komutu boş çıktı döndürdü veya veri bulunamadı")

            progress.update(task, advance=100)

            # Ham whois çıktısını tablo olarak göster
            table = Table(show_header=True, header_style="bold magenta", border_style="magenta", expand=True)
            table.add_column("Whois Bilgisi", style="green", overflow="fold")
            formatted_data = str(whois_data).strip().replace('\r\n', '\n').split('\n')
            formatted_data = [line for line in formatted_data if line.strip() and not line.strip().startswith('%')]
            for line in formatted_data:
                table.add_row(line)
            console.print(table)

            # Eğer python-whois ile alınmış yapısal veri yoksa burada sonlanabiliriz
            if not w:
                console.print(f"[yellow][!] Whois bilgisi (raw) gösterildi: {target}[/yellow]")
                return

            # Aşağıda yapısal veriye dayalı daha temiz tablo oluşturulur
            table = Table(show_header=True, header_style="bold magenta", border_style="magenta", expand=True)
            table.add_column("Bilgi", style="green")
            table.add_column("Değer", style="yellow")

            def get_attr(obj, attr):
                try:
                    # dict-benzeri veya nesne-benzeri erişim
                    if hasattr(obj, 'get'):
                        val = obj.get(attr, None)
                    else:
                        val = getattr(obj, attr, None)
                    if val is None:
                        return "-"
                    if isinstance(val, (list, tuple, set)):
                        return ", ".join(map(str, val)) if val else "-"
                    return str(val)
                except Exception:
                    return "-"

            domain_name = get_attr(w, 'domain_name')
            if domain_name == "-":
                domain_name = get_attr(w, 'name')

            table.add_row("Domain", domain_name)
            table.add_row("Registrar", get_attr(w, 'registrar'))
            table.add_row("Oluşturma Tarihi", get_attr(w, 'creation_date'))
            table.add_row("Bitiş Tarihi", get_attr(w, 'expiration_date'))
            table.add_row("Güncelleme Tarihi", get_attr(w, 'updated_date'))
            table.add_row("E-posta", get_attr(w, 'emails'))
            table.add_row("Name Server", get_attr(w, 'name_servers'))
            table.add_row("Durum", get_attr(w, 'status'))

            console.print(table)

        except Exception as e:
            progress.update(task, advance=100)
            console.print(f"[red][!] Whois sorgusu sırasında beklenmeyen hata:[/red] {e}")
            console.print("[yellow]Not: 'python-whois' kütüphanesinin son versiyonlarında bazı hata nesnesi isimleri değişmiş olabilir. Lütfen kütüphaneyi güncellediğinizden emin olun.[/yellow]")


def geoip_lookup():
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: GeoIP Bilgisi for [white]{target}[/white] :::[/bold yellow]")
    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console
    ) as progress:
        task = progress.add_task("[bold green]GeoIP konum bilgisi alınıyor...[/bold green]", total=100)
        try:
            ip = socket.gethostbyname(target)
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
            
            progress.update(task, advance=100)

            if response.get("status") == "fail":
                console.print(f"[red][!] GeoIP başarısız: {response.get('message', 'Bilinmeyen Hata')}[/red]")
                return

            table = Table(show_header=True, header_style="bold blue", border_style="blue", expand=True)
            table.add_column("Bilgi", style="green")
            table.add_column("Değer", style="yellow")
            
            table.add_row("IP Adresi", str(response.get("query", "-")))
            table.add_row("Ülke", str(response.get("country", "-")))
            table.add_row("Ülke Kodu", str(response.get("countryCode", "-")))
            table.add_row("Bölge Adı", str(response.get("regionName", "-")))
            table.add_row("Şehir", str(response.get("city", "-")))
            table.add_row("Posta Kodu", str(response.get("zip", "-")))
            table.add_row("Enlem", str(response.get("lat", "-")))
            table.add_row("Boylam", str(response.get("lon", "-")))
            table.add_row("Saat Dilimi", str(response.get("timezone", "-")))
            table.add_row("ISS (ISP)", str(response.get("isp", "-")))
            table.add_row("Organizasyon", str(response.get("org", "-")))
            table.add_row("AS Numarası", str(response.get("as", "-")))
            console.print(table)

        except socket.gaierror:
            console.print(f"[red][!] GeoIP başarısız: Hedef IP'ye dönüştürülemedi ({target}).[/red]")
        except requests.exceptions.RequestException as e:
            console.print(f"[red][!] GeoIP isteği sırasında hata oluştu:[/red] {e}")
        except Exception as e:
            console.print(f"[red][!] GeoIP sorgusu sırasında beklenmeyen hata:[/red] {e}")

def get_headers():
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: HTTP/HTTPS Başlıkları for [white]{target}[/white] :::[/bold yellow]")
    
    # Hem HTTP hem HTTPS deneme
    urls_to_try = [f"https://{target}", f"http://{target}"]
    
    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console
    ) as progress:
        task = progress.add_task("[bold green]HTTP/HTTPS başlıkları çekiliyor...[/bold green]", total=len(urls_to_try))
        
        for url in urls_to_try:
            try:
                response = requests.get(url, timeout=7, verify=False) # SSL sertifikası doğrulamayı kapat, güvenlik uyarısı verir
                headers = response.headers
                
                console.print(f"\n[bold green]-- {url} adresinden HTTP Başlıkları ([bold white]{response.status_code} {response.reason}[/bold white]) --[/bold green]")
                table = Table(show_header=True, header_style="bold blue", border_style="blue", expand=True)
                table.add_column("Başlık", style="green")
                table.add_column("Değer", style="yellow")
                for k, v in headers.items():
                    table.add_row(k, v)
                console.print(table)
                progress.update(task, advance=1)
                return # Başarılı olursa diğer URL'yi denemeye gerek yok
            except requests.exceptions.ConnectionError:
                console.print(f"[yellow]Uyarı: {url} adresine bağlanılamadı.[/yellow]")
            except requests.exceptions.Timeout:
                console.print(f"[yellow]Uyarı: {url} isteği zaman aşımına uğradı.[/yellow]")
            except requests.exceptions.SSLError:
                console.print(f"[yellow]Uyarı: {url} için SSL sertifikası hatası. Devam ediliyor...[/yellow]")
            except Exception as e:
                console.print(f"[red][!] {url} adresinden başlıklar alınamadı: {e}[/red]")
            progress.update(task, advance=1)
                
    console.print("[red][!] Hedeften HTTP başlıkları alınamadı. Hedef aktif olmayabilir veya web sunucusu çalışmıyor olabilir.[/red]")

def robots_txt():
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: robots.txt İçeriği for [white]{target}[/white] :::[/bold yellow]")
    
    urls_to_try = [f"https://{target}/robots.txt", f"http://{target}/robots.txt"]

    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console
    ) as progress:
        task = progress.add_task("[bold green]robots.txt çekiliyor...[/bold green]", total=len(urls_to_try))

        for url in urls_to_try:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    console.print(f"[green]robots.txt içeriği ({url}):[/green]")
                    console.print(Panel(response.text, border_style="green", title="robots.txt", title_align="left", box=MINIMAL))
                    progress.update(task, advance=1)
                    return
                elif response.status_code == 404:
                    console.print(f"[yellow]Uyarı: {url} adresinde robots.txt bulunamadı (404 Not Found).[/yellow]")
                else:
                    console.print(f"[yellow]Uyarı: {url} adresinden robots.txt alınamadı. Durum kodu: {response.status_code}[/yellow]")
            except requests.exceptions.RequestException as e:
                console.print(f"[red][!] {url} adresinden robots.txt alınırken hata: {e}[/red]")
            except Exception as e:
                console.print(f"[red][!] robots.txt alınırken beklenmeyen hata:[/red] {e}")
            progress.update(task, advance=1)
                
    console.print("[red][!] Hedef için robots.txt bulunamadı veya erişilemedi.[/red]")

def subdomain_scan():
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    
    common_subdomains = [
        "www", "mail", "ftp", "ns1", "ns2", "admin", "webmail", "portal", "blog",
        "dev", "test", "api", "shop", "crm", "vpn", "git", "status", "docs",
        "support", "secure", "app", "cloud", "demo", "stage", "cpanel", "whm",
        "autodiscover", "discovery", "m", "mobile", "owa", "exchange", "vps",
        "cdn", "assets", "static", "files", "download", "images", "forum", "news", "wiki",
        "internal", "private", "prod", "uat", "qa", "proxy", "gw", "router", "db",
        "smtp", "pop3", "imap", "sso", "identity", "cluster", "node", "grafana", "jenkins",
        "jira", "confluence", "bitbucket", "gitlab", "test", "staging", "dev", "uat", "prod"
    ]
    
    console.print(f"\n[bold yellow]::: Alt Domain Taraması for [white]{target}[/white] :::[/bold yellow]")
    table = Table(show_header=True, header_style="bold green", border_style="green", expand=True)
    table.add_column("Alt Domain", style="cyan")
    table.add_column("IP Adresi", style="yellow")
    table.add_column("Durum", style="magenta")

    found_any = False
    
    with Progress(
        SpinnerColumn("line"), # Farklı bir spinner
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console
    ) as progress:
        task = progress.add_task(f"[bold green]Alt alan adları taranıyor ({len(common_subdomains)} adet)...[/bold green]", total=len(common_subdomains))

        for sub in common_subdomains:
            subdomain_full = f"{sub}.{target}"
            try:
                ip = socket.gethostbyname(subdomain_full)
                table.add_row(subdomain_full, ip, "[green]Aktif[/green]")
                found_any = True
            except socket.gaierror:
                pass 
            except Exception as e:
                console.print(f"[red][!] {subdomain_full} taranırken hata: {e}[/red]", justify="left")
            progress.update(task, advance=1)
    
    if not found_any:
        console.print("[yellow]Hiçbir yaygın alt alan adı bulunamadı. Bu, hedefin iyi yapılandırılmış olduğu veya farklı alt alan adları kullandığı anlamına gelebilir.[/yellow]")
    else:
        console.print(table)
    
    console.print("\n[yellow]Not: Bu sadece yaygın alt alan adlarını kontrol eder. Daha derin ve brute-force tabanlı taramalar için Amass veya Sublist3r gibi araçlar gerekebilir.[/yellow]")

def ssl_cert_info():
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: SSL Sertifika Bilgisi for [white]{target}[/white] :::[/bold yellow]")
    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console
    ) as progress:
        task = progress.add_task("[bold green]SSL sertifika bilgisi alınıyor...[/bold green]", total=100)
        try:
            context = ssl.create_default_context()
            with socket.create_connection((target, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=target) as ssock:
                    cert = ssock.getpeercert()
                    
                    progress.update(task, advance=100)
                    
                    table = Table(show_header=True, header_style="bold magenta", border_style="magenta", expand=True)
                    table.add_column("Alan", style="green")
                    table.add_column("Değer", style="yellow")

                    def get_cert_detail(key, default="-"):
                        val = cert.get(key, default)
                        if isinstance(val, (tuple, list)):
                            if key in ["subject", "issuer"]:
                                formatted_parts = []
                                for part in val:
                                    if isinstance(part, (tuple, list)):
                                        for item_key, item_value in part:
                                            formatted_parts.append(f"{item_key}: {item_value}")
                                    else:
                                        formatted_parts.append(str(part))
                                return "\n".join(formatted_parts)
                            elif key == "subjectAltName":
                                san_entries = []
                                for field in val:
                                    if field[0] == 'DNS':
                                        san_entries.append(field[1])
                                return "\n".join(san_entries) if san_entries else "-"
                            else:
                                return "\n".join([str(item) for item in val])
                        return str(val)

                    table.add_row("Konu (Subject)", get_cert_detail("subject"))
                    table.add_row("Veren (Issuer)", get_cert_detail("issuer"))
                    
                    not_before = datetime.datetime.strptime(cert["notBefore"], "%b %d %H:%M:%S %Y %Z")
                    not_after = datetime.datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
                    table.add_row("Geçerlilik Başlangıcı", str(not_before))
                    table.add_row("Geçerlilik Bitişi", str(not_after))
                    
                    remaining_days = (not_after - datetime.datetime.now()).days
                    if remaining_days > 0:
                        table.add_row("Kalan Gün", f"[bold green]{remaining_days} gün[/bold green]")
                    else:
                        table.add_row("Kalan Gün", "[bold red]SÜRESİ DOLMUŞ![/bold red]")

                    table.add_row("Seri Numarası", get_cert_detail("serialNumber"))
                    table.add_row("Versiyon", str(cert.get("version", "-")))
                    table.add_row("Algoritma", get_cert_detail("signatureAlgorithm"))
                    
                    table.add_row("Alternatif Adlar (SAN)", get_cert_detail("subjectAltName"))

                    console.print(table)

        except socket.gaierror:
            console.print(f"[red][!] SSL sertifika bilgisi alınamadı: Hedef IP'ye dönüştürülemedi ({target}).[/red]")
        except socket.timeout:
            console.print(f"[red][!] SSL sertifika bilgisi alınamadı: Bağlantı zaman aşımına uğradı. Hedefte Port 443 açık olmayabilir veya ağ sorunu var.[/red]")
        except ConnectionRefusedError:
            console.print(f"[red][!] SSL sertifika bilgisi alınamadı: Bağlantı reddedildi. Port 443 kapalı veya hedef SSL/TLS kullanmıyor olabilir.[/red]")
        except ssl.SSLError as e:
            console.print(f"[red][!] SSL sertifika hatası: {e}. Sertifika geçerli olmayabilir veya desteklenmeyen bir protokol kullanılıyor.[/red]")
        except Exception as e:
            console.print(f"[red][!] SSL sertifika bilgisi alınırken beklenmeyen hata:[/red] {e}")

def shodan_lookup():
    # SHODAN API anahtarını önce ortam değişkeninden sonra modül değişkeninden al
    api_key = os.environ.get('SHODAN_API_KEY') or SHODAN_API_KEY
    if not api_key:
        # Güvenli istem: getpass kullanarak kullanıcıdan al (session-only)
        try:
            import getpass
            prompt_msg = "Shodan API anahtarı bulunamadı. Lütfen anahtarı girin (Enter ile iptal): "
            entered = getpass.getpass(prompt_msg)
        except Exception:
            # Fallback: rich Prompt (daha az gizli, ama çalışır)
            entered = Prompt.ask("Shodan API anahtarı bulunamadı. Lütfen anahtarı girin (boş bırak = iptal)")

        if not entered:
            console.print("[red][!] Shodan API anahtarı yok, sorgu iptal edildi.[/red]")
            return
        api_key = entered

    if not target:
        console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]")
        return

    console.print(f"\n[bold yellow]::: Shodan Bilgisi for [white]{target}[/white] :::[/bold yellow]")
    try:
        ip = socket.gethostbyname(target)
        url = f"https://api.shodan.io/shodan/host/{ip}?key={api_key}"
        
        with console.status(f"[bold green]Shodan API sorgulanıyor...[/bold green]", spinner="dots"):
            response = requests.get(url, timeout=15)
            data = response.json()

        if response.status_code == 200:
            table = Table(show_header=True, header_style="bold blue", border_style="blue", expand=True)
            table.add_column("Bilgi", style="green")
            table.add_column("Değer", style="yellow")

            table.add_row("IP", data.get("ip_str", "-"))
            table.add_row("Hostname", ", ".join(data.get("hostnames", ["-"])) if data.get("hostnames") else "-")
            table.add_row("Portlar", ", ".join(map(str, data.get("ports", ["-"]))) if data.get("ports") else "-")
            table.add_row("Organizasyon", data.get("org", "-"))
            table.add_row("Ülke", data.get("country_name", "-"))
            table.add_row("Şehir", data.get("city", "-"))
            table.add_row("Bölge", data.get("region_name", "-"))
            table.add_row("Harita Koordinatları", f"{data.get('latitude', '-')}, {data.get('longitude', '-')}")
            table.add_row("Son Güncelleme", data.get("last_update", "-"))
            
            console.print(table) 

            if "data" in data and data["data"]:
                console.print("\n[bold cyan]Açık Servisler ve Banner'lar:[/bold cyan]")
                service_table = Table(show_header=True, header_style="bold magenta", border_style="magenta", expand=True)
                service_table.add_column("Port", style="cyan")
                service_table.add_column("Servis", style="green")
                service_table.add_column("Ürün/Versiyon", style="white")
                service_table.add_column("Vulnerabilities", style="red")
                service_table.add_column("Banner (Kısaltılmış)", style="yellow")

                for service in data["data"]:
                    port = service.get("port", "-")
                    product = service.get("product", service.get("service_name", "-"))
                    version = service.get("version", "-")
                    banner = service.get("data", "Yok")
                    vulnerabilities = []
                    if "vulns" in service:
                        for vuln_id, vuln_data in service["vulns"].items():
                            if vuln_data.get("verified"):
                                vulnerabilities.append(vuln_id)
                    
                    vuln_str = ", ".join(vulnerabilities) if vulnerabilities else "-"
                    
                    service_table.add_row(
                        str(port), 
                        product, 
                        version, 
                        f"[red]{vuln_str}[/red]" if vuln_str != "-" else vuln_str,
                        banner[:100] + "..." if len(banner) > 100 else banner
                    )
                console.print(service_table)
            else:
                console.print("[yellow]Shodan'da bu IP için detaylı servis bilgisi bulunamadı.[/yellow]")

        elif response.status_code == 401:
            console.print("[red][!] Shodan API Hatası: Geçersiz API Anahtarı. Lütfen SHODAN_API_KEY'i kontrol edin.[/red]")
        elif response.status_code == 403:
            # 403 typically means the API key does not have access (membership required)
            console.print("[red][!] Shodan API Hatası: Erişim reddedildi (403). Bu API anahtarıyla bu endpoint'e erişim için 'membership' veya daha yüksek bir seviyeye ihtiyacınız var.[/red]")
            console.print("[yellow]Not: Shodan bazı endpoint'leri ücretli planlara ayırır. Lütfen hesap panelinizi kontrol edin veya üyelik yükseltmeyi düşünün.[/yellow]")
            # Fallback: provide basic IP/geolocation info via a free service (ip-api)
            try:
                console.print("[cyan]Alternatif: ip-api üzerinden temel IP bilgisi getiriliyor...[/cyan]")
                geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=8).json()
                if geo.get("status") != "fail":
                    fb = Table(show_header=True, header_style="bold blue", border_style="blue", expand=True)
                    fb.add_column("Bilgi", style="green")
                    fb.add_column("Değer", style="yellow")
                    fb.add_row("IP", geo.get("query", "-"))
                    fb.add_row("Ülke", geo.get("country", "-"))
                    fb.add_row("Bölge", geo.get("regionName", "-"))
                    fb.add_row("Şehir", geo.get("city", "-"))
                    fb.add_row("ISP", geo.get("isp", "-"))
                    fb.add_row("Organizasyon", geo.get("org", "-"))
                    fb.add_row("Enlem/Boylam", f"{geo.get('lat','-')}, {geo.get('lon','-')}")
                    console.print(fb)
                else:
                    console.print("[yellow]ip-api fallback ile bilgi alınamadı.[/yellow]")
            except Exception as e:
                console.print(f"[red][!] ip-api fallback sırasında hata: {e}[/red]")
        elif response.status_code == 404:
            console.print(f"[yellow][!] Shodan'da '{ip}' için sonuç bulunamadı. Bu IP Shodan tarafından indekslenmemiş olabilir.[/yellow]")
        else:
            console.print(f"[red][!] Shodan API Hatası: Durum Kodu {response.status_code}, Mesaj: {data.get('error', 'Bilinmeyen hata')}[/red]")
    except socket.gaierror:
        console.print(f"[red][!] Shodan sorgusu başarısız: Hedef IP'ye dönüştürülemedi ({target}).[/red]")
    except requests.exceptions.RequestException as e:
        console.print(f"[red][!] Shodan isteği sırasında hata oluştu:[/red] {e}")
    except json.JSONDecodeError:
        console.print(f"[red][!] Shodan yanıtı işlenirken hata: Geçersiz JSON veya boş yanıt.[/red]")
    except Exception as e:
        console.print(f"[red][!] Shodan sorgusu sırasında beklenmeyen hata:[/red] {e}")

def dir_scan():
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    
    common_dirs = [
        "admin/", "login/", "panel/", "dashboard/", "uploads/", "backup/",
        "test/", "dev/", ".git/", ".svn/", "config/", "assets/", "images/",
        "api/", "docs/", "blog/", "wp-admin/", "phpmyadmin/", "old/", "temp/",
        "index.php", "index.html", "sitemap.xml", "crossdomain.xml", ".env",
        "README.md", "server-status", "robots.txt", "admin.php", "status.html",
        "inc/", "lib/", "src/", "vendor/", "css/", "js/", "img/", "includes/",
        "download/", "files/", "data/", "cgi-bin/", "shell/", "logs/", "private/",
        "public/", "web/", "site/", "content/", "modules/", "themes/", "plugins/",
        "adminer.php", "info.php", "licence.txt", "changelog.txt", "README.txt",
        "config.php", "setup/", "install/", "templates/", "backup.zip", "database/",
        "sql/", "web-info/", "admin_old/", "test_old/", "user/", "system/", "control/",
        "controlpanel/", "portal_admin/", "portal_login/", "user_login/", "user_panel/",
        "wp-content/", "wp-includes/", "wp-json/", "xmlrpc.php", "phpinfo.php",
        "server-info", "status", "phpmyadmin.php", "backup.sql", "db_backup/"
    ]
    console.print(f"\n[bold yellow]::: Dizin Taraması for [white]{target}[/white] :::[/bold yellow]")
    table = Table(show_header=True, header_style="bold green", border_style="green", expand=True)
    table.add_column("Dizin/Dosya", style="cyan")
    table.add_column("Durum Kodu", style="yellow")
    table.add_column("Durum", style="magenta")

    urls_to_scan = [f"https://{target}/", f"http://{target}/"]

    found_any = False
    
    with Progress(
        SpinnerColumn("dots"),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console
    ) as progress:
        task = progress.add_task(f"[bold green]Dizinler taranıyor ({len(common_dirs)} adet)...[/bold green]", total=len(common_dirs) * len(urls_to_scan))

        for base_url_prefix in urls_to_scan:
            for path in common_dirs:
                url = f"{base_url_prefix}{path}"
                try:
                    response = requests.get(url, timeout=3, allow_redirects=True)
                    status_code = response.status_code
                    
                    status_text = ""
                    if 200 <= status_code < 300:
                        status_text = "[green]Bulundu[/green]"
                        found_any = True
                    elif 300 <= status_code < 400:
                        location = response.headers.get('Location', 'Bilinmiyor')
                        status_text = f"[blue]Yönlendirme ({location})[/blue]"
                        found_any = True
                    elif status_code == 401:
                        status_text = "[yellow]Yetki Gerekiyor[/yellow]"
                        found_any = True
                    elif status_code == 403:
                        status_text = "[yellow]Erişim Yasak[/yellow]"
                        found_any = True
                    elif status_code == 404:
                        pass
                    else:
                        status_text = f"[red]Diğer ({status_code})[/red]"
                        found_any = True
                    
                    if status_text:
                        table.add_row(url, str(status_code), status_text)

                except requests.exceptions.RequestException:
                    pass
                except Exception as e:
                    console.print(f"[red][!] {url} taranırken beklenmeyen hata: {e}[/red]", justify="left")
                progress.update(task, advance=1)
    
    if not found_any:
        console.print("[yellow]Hiçbir yaygın dizin veya dosya bulunamadı. Bu, hedefin iyi yapılandırılmış olduğu anlamına gelebilir veya daha kapsamlı bir sözlük gerekebilir.[/yellow]")
    else:
        console.print(table)
    console.print("\n[yellow]Not: Bu basit bir dizin tarayıcıdır. Daha kapsamlı ve brute-force tabanlı taramalar için Gobuster veya Dirb gibi araçlar kullanın.[/yellow]")

def port_scan():
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    
    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        console.print(f"[red][!] Port taraması başarısız: Hedef IP'ye dönüştürülemedi ({target}).[/red]")
        return

    common_ports = [
        20, 21, 22, 23, 25, 53, 67, 68, 69, 80, 88, 110, 111, 135, 137, 138, 139, 143,
        161, 162, 389, 443, 445, 500, 514, 587, 636, 993, 995, 1433, 1521,
        1723, 3306, 3389, 5432, 5900, 8000, 8080, 8443, 9000, 10000, 27017, 
        5000, 7000, 9200, 2049, 2181, 28017, 6379, 9300, 25565
    ] 

    console.print(f"\n[bold yellow]::: Port Taraması for [white]{ip}[/white] :::[/bold yellow]")
    table = Table(show_header=True, header_style="bold blue", border_style="blue", expand=True)
    table.add_column("Port", style="cyan")
    table.add_column("Durum", style="green")
    table.add_column("Servis (Tahmin)", style="magenta")

    found_open_ports = False
    
    port_services = {
        20: "FTP (Data)", 21: "FTP (Control)", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 67: "DHCP (Server)",
        68: "DHCP (Client)", 69: "TFTP", 80: "HTTP", 88: "Kerberos", 110: "POP3", 111: "RPCBind", 135: "MS RPC",
        137: "NetBIOS Name Service", 138: "NetBIOS Datagram Service", 139: "NetBIOS Session Service",
        143: "IMAP", 161: "SNMP", 162: "SNMP Trap", 389: "LDAP", 443: "HTTPS", 445: "SMB/CIFS", 500: "ISAKMP (IPsec)",
        514: "Syslog", 587: "SMTP (Submission)", 636: "LDAPS", 993: "IMAPS", 995: "POP3S", 1433: "MSSQL",
        1521: "Oracle SQL", 1723: "PPTP", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC",
        8000: "HTTP (Alt)", 8080: "HTTP Proxy/Alt Web Server", 8443: "HTTPS (Alt)", 9000: "Jenkins/Node.js",
        10000: "Webmin", 27017: "MongoDB", 5000: "UPnP/Flask", 7000: "Cassandra", 9200: "Elasticsearch",
        2049: "NFS", 2181: "ZooKeeper", 28017: "MongoDB (Web Interface)", 6379: "Redis", 9300: "Elasticsearch (Inter-node)",
        25565: "Minecraft Server"
    }

    with Progress(
        SpinnerColumn("simpleDots"),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console
    ) as progress:
        task = progress.add_task(f"[bold green]Portlar taranıyor ({len(common_ports)} adet)...[/bold green]", total=len(common_ports))

        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.7)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    service_guess = port_services.get(port, "Bilinmiyor")
                    table.add_row(str(port), "[green]AÇIK[/green]", service_guess)
                    found_open_ports = True
                sock.close()
            except Exception:
                pass
            progress.update(task, advance=1)
    
    if not found_open_ports:
        console.print("[yellow]Belirtilen yaygın portlarda açık port bulunamadı.[/yellow]")
    else:
        console.print(table)
    console.print("\n[yellow]Not: Bu basit bir port tarayıcıdır ve hızlı bir ön kontrol sağlar. Daha kapsamlı, güvenilir ve servis versiyon tespiti için Nmap gibi profesyonel araçlar kullanın.[/yellow]")

def nmap_nikto_report():
    """Tek komutta Nmap ve Nikto çalıştırır, çıktıları reports/<target>_<timestamp>/ dizinine kaydeder ve
    birleştirilmiş bir `index.html` üretir. Otomatik Docker ve python-nmap geri dönüşleri içerir."""
    if not target:
        console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]")
        return

    # Prepare report directory early so Docker fallback can mount it
    timestamp = datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    report_dir = os.path.join('reports', f"{target}_{timestamp}")
    os.makedirs(report_dir, exist_ok=True)

    nmap_xml = os.path.join(report_dir, 'nmap.xml')
    nmap_txt = os.path.join(report_dir, 'nmap.txt')
    nikto_html = os.path.join(report_dir, 'nikto.html')
    scan_log = os.path.join(report_dir, 'scan.log')

    def log(msg):
        try:
            with open(scan_log, 'a', encoding='utf-8') as lf:
                lf.write(f"[{datetime.datetime.utcnow().isoformat()}] {msg}\n")
        except Exception:
            pass

    # Araçların mevcut olup olmadığını kontrol et
    missing = []
    nmap_bin = shutil.which('nmap')
    nikto_bin = shutil.which('nikto')
    if not nmap_bin:
        log('nmap binary not found in PATH')
        # we will try python-nmap as fallback

    # Prepare nikto execution strategy
    nikto_exec = None
    if nikto_bin:
        nikto_exec = ('cmd', nikto_bin)
    else:
        # Try typical Windows/choco locations for nikto.pl
        possible_paths = [
            os.path.join(os.environ.get('ProgramData', 'C:\\ProgramData'), 'chocolatey', 'lib', 'nikto', 'tools', 'nikto.pl'),
            os.path.join('C:\\nikto', 'nikto.pl'),
            os.path.join(os.getcwd(), 'nikto.pl'),
            os.path.join(os.getcwd(), 'tools', 'nikto.pl')
        ]
        found_pl = None
        for p in possible_paths:
            if os.path.isfile(p):
                found_pl = p
                break

        if found_pl:
            perl_bin = shutil.which('perl')
            if perl_bin:
                nikto_exec = ('perl', (perl_bin, found_pl))
            else:
                missing.append('nikto (perl script found but perl not in PATH)')
                log('Found nikto.pl but perl not in PATH')
        else:
            docker_bin = shutil.which('docker')
            if docker_bin:
                # we'll build docker command at runtime (so we can mount correct absolute path)
                nikto_exec = ('docker', docker_bin)
            else:
                missing.append('nikto')

    if not nmap_bin and not shutil.which('nmap'):
        # try python-nmap (if installed) as a fallback
        try:
            import nmap as nmaplib  # python-nmap
            has_python_nmap = True
            log('python-nmap available; will use PortScanner fallback')
        except Exception:
            has_python_nmap = False
            missing.append('nmap')

    if missing:
        console.print(f"[red][!] Gerekli araçlar PATH'te bulunamadı veya eksik: {', '.join(missing)}[/red]")
        console.print("[yellow]Windows üzerinde çalıştırmak için öneriler:[/yellow]")
        console.print("  1) Chocolatey varsa: Yönetici PowerShell'de:")
        console.print("     choco install nmap -y")
        console.print("     (Nikto genellikle choco ile gelir: choco install nikto -y veya nikto'yu manuel yükleyin)")
        console.print("  2) Nikto Perl tabanlıdır. Eğer nikto.pl varsa StrawberryPerl yükleyin ve perl PATH'e ekleyin:\n     choco install strawberryperl -y")
        console.print("  3) Docker yüklüyse: Docker ile Nikto konteynerini kullanabilirsiniz. Örnek:\n     docker run --rm -v C:\\path\\to\\reports:/out sullo/nikto -h <host> -o /out/nikto.html -Format html")
        log('Missing tools: ' + ','.join(missing))
        return

    import subprocess
    import html as _html

    # Run Nmap: prefer binary, fallback to python-nmap
    try:
        if nmap_bin:
            log(f'Running nmap binary: {nmap_bin}')
            with console.status(f"[green]Nmap çalıştırılıyor (hedef: {target})...[/green]", spinner="dots"):
                subprocess.run([nmap_bin, '-sV', '-oX', nmap_xml, '-oN', nmap_txt, target], check=True, timeout=600)
        elif has_python_nmap:
            log('Running python-nmap PortScanner fallback')
            ps = nmaplib.PortScanner()
            console.print('[yellow]nmap binary yok, python-nmap ile tarama yapılıyor (daha sınırlı çıktı).[/yellow]')
            ps.scan(target, arguments='-sV')
            # write a readable summary
            with open(nmap_txt, 'w', encoding='utf-8') as f:
                for host in ps.all_hosts():
                    f.write(f"Host: {host} ({ps[host].hostname()})\n")
                    f.write(f"State: {ps[host].state()}\n")
                    for proto in ps[host].all_protocols():
                        lports = ps[host][proto].keys()
                        for port in sorted(lports):
                            svc = ps[host][proto][port]
                            f.write(f"{port}/{proto}: {svc.get('name','-')} {svc.get('product','')} {svc.get('version','')}\n")
            # xml not available from python-nmap easily; leave nmap_xml empty
            with open(nmap_xml, 'w', encoding='utf-8') as f:
                f.write('<nmap></nmap>')
        log('Nmap finished')
    except subprocess.CalledProcessError as e:
        console.print(f"[red][!] Nmap sırasında hata oluştu: {e}[/red]")
        log(f'nmap error: {e}')
    except Exception as e:
        console.print(f"[red][!] Nmap hata: {e}[/red]")
        log(f'nmap exception: {e}')

    # Run Nikto using the selected execution method
    try:
        with console.status(f"[green]Nikto çalıştırılıyor (hedef: {target})...[/green]", spinner="dots"):
            if nikto_exec[0] == 'cmd':
                subprocess.run([nikto_exec[1], '-h', target, '-o', nikto_html, '-Format', 'html'], check=True, timeout=900)
            elif nikto_exec[0] == 'perl':
                perl_bin, nikto_pl = nikto_exec[1]
                subprocess.run([perl_bin, nikto_pl, '-h', target, '-o', nikto_html, '-Format', 'html'], check=True, timeout=900)
            elif nikto_exec[0] == 'docker':
                docker_bin = nikto_exec[1]
                # build docker command and mount report_dir
                cmd = [docker_bin, 'run', '--rm', '-v', f"{os.path.abspath(report_dir)}:/out", 'sullo/nikto', '-h', target, '-o', '/out/nikto.html', '-Format', 'html']
                subprocess.run(cmd, check=True, timeout=900)
            else:
                raise RuntimeError('Bilinmeyen nikto çalıştırma yöntemi')
        log('Nikto finished')
    except subprocess.CalledProcessError as e:
        console.print(f"[red][!] Nikto sırasında hata oluştu: {e}[/red]")
        log(f'nikto error: {e}')
    except subprocess.TimeoutExpired:
        console.print("[red][!] Nikto komutu zaman aşımına uğradı (limit: 900s). İşlem iptal edildi.[/red]")
        log('nikto timeout')

    # Read Nmap normal output (if present) and build index.html combining Nikto HTML and Nmap text
    try:
        with open(nmap_txt, 'r', encoding='utf-8', errors='ignore') as f:
            nmap_text = f.read()
    except Exception:
        nmap_text = "Nmap çıktısı bulunamadı veya okunamadı."

    # Create a lightweight index.html that embeds nikto.html and shows nmap output
    index_html = os.path.join(report_dir, 'index.html')
    html_content = f"""<!doctype html>
<html lang=\"tr\"> 
<head>
  <meta charset=\"utf-8\"> 
  <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"> 
  <title>Scan Report - {target}</title>
  <style>
    body {{ font-family: Arial, Helvetica, sans-serif; background:#f7f7f7; color:#222; margin:0; padding:1rem; }}
    header {{ margin-bottom: 1rem; }}
    iframe {{ width:100%; height:800px; border:1px solid #ccc; }}
    pre {{ background:#111; color:#eee; padding:1rem; border-radius:6px; overflow:auto; white-space:pre-wrap; word-wrap:break-word }}
    .files {{ margin-top:.5rem; font-size:.9rem }}
  </style>
</head>
<body>
  <header>
    <h1>Scan Report for {target}</h1>
    <p>Oluşturulma zamanı (UTC): {datetime.datetime.utcnow().isoformat()}</p>
  </header>

  <section>
    <h2>Nikto Raporu</h2>
    <iframe src="{os.path.basename(nikto_html)}"></iframe>
  </section>

  <section>
    <h2>Nmap (Normal Çıktı)</h2>
    <pre>{_html.escape(nmap_text)}</pre>
  </section>

  <section class=\"files\"> 
    <h3>Oluşturulan Dosyalar</h3>
    <ul>
      <li>{os.path.basename(nmap_xml)}</li>
      <li>{os.path.basename(nmap_txt)}</li>
      <li>{os.path.basename(nikto_html)}</li>
      <li>{os.path.basename(index_html)}</li>
      <li>{os.path.basename(scan_log)}</li>
    </ul>
  </section>
</body>
</html>
"""

    try:
        with open(index_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
    except Exception as e:
        console.print(f"[red][!] index.html oluşturulurken hata: {e}[/red]")
        log(f'index.html write error: {e}')
        return

    # Başarıyı göster
    table = Table(show_header=True, header_style="bold green", border_style="green", expand=False)
    table.add_column("Dosya", style="cyan")
    table.add_column("Yol", style="yellow")
    table.add_row("Index (birleştirilmiş)", os.path.abspath(index_html))
    table.add_row("Nikto HTML", os.path.abspath(nikto_html))
    table.add_row("Nmap (normal)", os.path.abspath(nmap_txt))
    table.add_row("Nmap (xml)", os.path.abspath(nmap_xml))
    table.add_row("Scan Log", os.path.abspath(scan_log))
    console.print(table)
    console.print(f"\n[bold green]Rapor klasörü oluşturuldu:[/bold green] [white]{os.path.abspath(report_dir)}[/white]")


def ping_target():
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: Ping Testi for [white]{target}[/white] :::[/bold yellow]")
    try:
        param = '-n 4' if os.name == 'nt' else '-c 4'
        command = f"ping {param} {target}"
        
        with Live(console=console, auto_refresh=True, screen=False) as live:
            process = os.popen(command)
            output = ""
            for line in process:
                output += line
                live.update(Panel(Text(output, style="white"), title="[bold cyan]Ping Çıktısı[/bold cyan]", border_style="cyan", box=MINIMAL))
                time.sleep(0.1)

            result_code = process.close()

            if result_code is None or result_code == 0:
                console.print(f"[bold green][+] {target} erişilebilir.[/bold green]")
            else:
                console.print(f"[bold red][!] {target} erişilemiyor veya komut hatası oluştu. (Çıkış kodu: {result_code})[/bold red]")
                console.print("[yellow]Not: Hedefin ICMP isteklerini engelliyor olması mümkündür.[/yellow]")
    except Exception as e:
        console.print(f"[red][!] Ping işlemi sırasında hata oluştu:[/red] {e}")

def traceroute_target():
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: Traceroute Testi for [white]{target}[/white] :::[/bold yellow]")
    
    command = ""
    if os.name == 'nt':
        command = f"tracert {target}"
    elif os.name == 'posix':
        command = f"traceroute {target}"
    else:
        console.print("[red][!] Traceroute komutu bu işletim sisteminde desteklenmiyor.[/red]")
        return

    try:
        with Live(console=console, auto_refresh=True, screen=False) as live:
            console.print(f"[cyan]Komut çalıştırılıyor: {command}[/cyan]")
            process = os.popen(command)
            output = ""
            for line in process:
                output += line
                live.update(Panel(Text(output, style="white"), title="[bold cyan]Traceroute Çıktısı[/bold cyan]", border_style="cyan", box=MINIMAL))
                time.sleep(0.1)

            result_code = process.close()

            if result_code is None or result_code == 0:
                console.print(f"[bold green][+] Ağ yolu başarıyla izlendi.[/bold green]")
            else:
                console.print(f"[bold red][!] Traceroute komutu çalıştırılamadı veya hata oluştu. Hedef erişilemiyor olabilir veya ağ yolu belirlenemiyor. (Çıkış kodu: {result_code})[/bold red]")
    except Exception as e:
        console.print(f"[red][!] Traceroute işlemi sırasında hata oluştu:[/red] {e}")

# --- Yeni Eklenen Kullanıcı Adı Arama Modülü ---
def check_social_profile(platform_name, url_format, username):
    """Belirli bir platformda kullanıcı adı varlığını kontrol eder."""
    try:
        full_url = url_format.format(username)
        

        # Modern ve güvenilir User-Agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # HEAD isteği bazı sitelerde 403 verebilir, bu durumda GET denemek daha güvenlidir
        try:
            r = requests.head(full_url, timeout=7, allow_redirects=True, headers=headers)
            status_code = r.status_code
        except requests.exceptions.TooManyRedirects:
            # Bazı URL'ler sonsuz yönlendirme döngüsüne girebilir
            social_media_results[platform_name] = ("Hata (Çok Fazla Yönlendirme)", full_url)
            return
        except requests.exceptions.RequestException:
            # HEAD isteği başarısız olursa GET ile dene
            r = requests.get(full_url, timeout=7, allow_redirects=True, headers=headers)
            status_code = r.status_code

        # Akıllı Durum Kontrolü: Farklı platformlar farklı yanıtlar verebilir
        # Daha iyi bir doğruluk için her platform için özel kontrol mekanizmaları geliştirilebilir.
        # Örneğin, 200 OK ve sayfa içeriğinde "kullanıcı bulunamadı" yazıp yazmadığını kontrol etmek gibi.
        if status_code == 200:
            # Bazı siteler 200 OK döndürüp "Sayfa Bulunamadı" içeriği gösterebilir.
            # Basit bir kontrol ekleyelim, daha gelişmişi için sayfa içeriği regex ile taranabilir.
            content = r.text.lower()
            if "page not found" in content or "user not found" in content or "profil bulunamadı" in content:
                 social_media_results[platform_name] = ("Bulunamadı", full_url)
            else:
                social_media_results[platform_name] = ("Bulundu", full_url)
        elif status_code == 404:
            social_media_results[platform_name] = ("Bulunamadı", full_url)
        elif status_code == 403:
            social_media_results[platform_name] = ("Erişim Engellendi", full_url)
        elif status_code == 500:
            social_media_results[platform_name] = ("Sunucu Hatası", full_url)
        else:
            social_media_results[platform_name] = (f"Durum Kodu: {status_code}", full_url)
    except requests.exceptions.RequestException:
        social_media_results[platform_name] = ("Hata (Bağlantı Sorunu/Zaman Aşımı)", url_format.format(username))
    except Exception as e:
        social_media_results[platform_name] = (f"Beklenmeyen Hata: {type(e).__name__}", url_format.format(username))

def spinner_for_social_media_search():
    """Kullanıcı adı arama işlemi sırasında dönen spinner."""
    try:
        spinner = Spinner("dots12", style="bold yellow", text="[bold yellow]Kullanıcı adı aranıyor, lütfen bekleyin...[/bold yellow]")
        with Live(spinner, refresh_per_second=12, console=console) as live:
            while not stop_social_media_search:
                time.sleep(0.1)
    except Exception as e:
        # Fallback to simpler progress display if spinner fails
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            task = progress.add_task("[yellow]Kullanıcı adı aranıyor...", total=None)
            while not stop_social_media_search:
                time.sleep(0.1)

def user_search(username):
    global stop_social_media_search, social_media_results
    social_media_results = {} # Her arama öncesi sonuçları temizle

    console.print(f"\n[bold yellow]::: Kullanıcı Adı Arama for [white]{username}[/white] :::[/bold yellow]")

    stop_social_media_search = False
    thread_spinner = Thread(target=spinner_for_social_media_search)
    thread_spinner.start()

    threads = []
    for platform, url in SOCIAL_MEDIA_PLATFORMS.items():
        t = Thread(target=check_social_profile, args=(platform, url, username))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    stop_social_media_search = True
    thread_spinner.join() # Spinner thread'inin bitmesini bekle

    table = Table(title=f"[bold green]'{username}' Kullanıcı Adı Arama Sonuçları[/bold green]", show_header=True, header_style="bold cyan", border_style="cyan", expand=True)
    table.add_column("Platform", justify="left", style="bold white")
    table.add_column("Durum", justify="center", style="bold")
    table.add_column("Profil Linki", justify="left", style="white")
    
    found_accounts_count = 0
    for platform in SOCIAL_MEDIA_PLATFORMS.keys(): # Orijinal sırayı koru
       
        durum, full_url = social_media_results.get(platform, ("Tarama Yapılmadı", "N/A"))
        
        renk = "green" if durum == "Bulundu" else "yellow" if durum == "Bulunamadı" else "red"
        
        if durum == "Bulundu":
           

            found_accounts_count += 1
            # Rich'in hyperlink özelliği ile tıklanabilir linkler
            table.add_row(platform, f"[{renk}]{durum}[/{renk}]", f"[link={full_url}][underline blue]{full_url}[/underline blue][/link]")
        else:
            table.add_row(platform, f"[{renk}]{durum}[/{renk}]", full_url) # Link olmayan durumlar için direkt URL'yi göster

    console.print(table)

    if found_accounts_count > 0:
        console.print(f"\n[bold green]🌟 Toplam [bold magenta]{found_accounts_count}[/bold magenta] hesap bulundu! 🌟[/bold green]")
    else:
        console.print("\n[bold yellow]Hiçbir hesap bulunamadı.[/bold yellow]")

# --- Yeni Gelişmiş OSINT Komutları (20+) ---

def reverse_ip():
    """Bir IP adresindeki tüm domainleri bulur"""
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: Reverse IP Lookup for [white]{target}[/white] :::[/bold yellow]")
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]Reverse IP sorgulanıyor...[/bold green]", total=100)
        try:
            ip = socket.gethostbyname(target)
            
            # API üzerinden reverse IP sorgula
            response = requests.get(f"https://api.abuseipdb.com/api/v2/check", params={"ipAddress": ip}, headers={"Key": "demo"}, timeout=5)
            progress.update(task, advance=50)
            
            # Alternative: viewdns.net API
            response = requests.get(f"https://viewdns.net/api/?apikey=demo&action=reverseip&ip={ip}&output=json", timeout=5)
            progress.update(task, advance=100)
            
            if response.status_code == 200:
                data = response.json()
                if "domains" in data:
                    domains = data["domains"][:10]
                    table = Table(show_header=True, header_style="bold cyan", border_style="cyan", expand=True)
                    table.add_column("Domain", style="yellow")
                    for domain in domains:
                        table.add_row(domain)
                    console.print(table)
                else:
                    console.print("[yellow]Bu IP ile ilişkili domain bulunamadı.[/yellow]")
            else:
                console.print("[yellow]Reverse IP API sorgulama başarısız. Yerel sorgu deneniyor...[/yellow]")
                console.print(f"[cyan]IP: {ip}[/cyan]")
        except Exception as e:
            console.print(f"[red][!] Reverse IP sorgusunda hata:[/red] {e}")

def reverse_dns():
    """IP adresinin geri DNS aramasını yapar"""
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: Reverse DNS Lookup for [white]{target}[/white] :::[/bold yellow]")
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]Reverse DNS sorgulanıyor...[/bold green]", total=100)
        try:
            ip = socket.gethostbyname(target)
            hostname = socket.gethostbyaddr(ip)[0]
            progress.update(task, advance=100)
            
            table = Table(show_header=True, header_style="bold blue", border_style="blue", expand=True)
            table.add_column("Bilgi", style="green")
            table.add_column("Değer", style="yellow")
            table.add_row("IP Adresi", ip)
            table.add_row("Hostname", hostname)
            console.print(table)
        except socket.herror:
            console.print("[yellow]Bu IP için reverse DNS kaydı bulunamadı.[/yellow]")
        except Exception as e:
            console.print(f"[red][!] Reverse DNS sorgusunda hata:[/red] {e}")

def ct_search():
    """SSL sertifikatlarından domain arama (Certificate Transparency)"""
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: Certificate Transparency Search for [white]{target}[/white] :::[/bold yellow]")
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]CT Logs sorgulanıyor...[/bold green]", total=100)
        try:
            domain = target.split('/')[0]
            # crt.sh API kullanarak sertifikaları ara
            url = f"https://crt.sh/?q=%25.{domain}&output=json"
            response = requests.get(url, timeout=10)
            progress.update(task, advance=100)
            
            if response.status_code == 200:
                certs = response.json()
                domains = set()
                for cert in certs:
                    name = cert.get("name_value", "")
                    for subdomain in name.split("\n"):
                        if subdomain.strip():
                            domains.add(subdomain.strip())
                
                if domains:
                    table = Table(show_header=True, header_style="bold green", border_style="green", expand=True)
                    table.add_column("Domain/Subdomain", style="cyan")
                    for d in sorted(domains)[:20]:
                        table.add_row(d)
                    console.print(table)
                    if len(domains) > 20:
                        console.print(f"[yellow]... ve {len(domains) - 20} daha fazla domain[/yellow]")
                    osint_report_data['ct_search'] = list(domains)
                else:
                    console.print("[yellow]CT Logs'ta bu domain için sertifika bulunamadı.[/yellow]")
        except Exception as e:
            console.print(f"[red][!] CT Search sorgusunda hata:[/red] {e}")

def leakdb_search(query):
    """Email/Username için sızan veriler (haveibeenpwned tarzı)"""
    console.print(f"\n[bold yellow]::: LeakDB Search for [white]{query}[/white] :::[/bold yellow]")
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]Leak veritabanları sorgulanıyor...[/bold green]", total=100)
        try:
            # haveibeenpwned.com API (genel bilgi amaçlı)
            headers = {'User-Agent': 'Mozilla/5.0'}
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{query}"
            response = requests.get(url, headers=headers, timeout=10)
            progress.update(task, advance=100)
            
            if response.status_code == 200:
                breaches = response.json()
                table = Table(show_header=True, header_style="bold red", border_style="red", expand=True)
                table.add_column("Breach Adı", style="yellow")
                table.add_column("Tarih", style="cyan")
                table.add_column("Veri Türü", style="red")
                
                for breach in breaches[:10]:
                    table.add_row(
                        breach.get("Name", "-"),
                        breach.get("BreachDate", "-"),
                        ", ".join(breach.get("DataClasses", []))
                    )
                console.print(table)
                osint_report_data['leakdb'] = len(breaches)
            elif response.status_code == 404:
                console.print("[green]✓ Bu email/username hiç bir sızmada bulunmamış (güvenli).[/green]")
            else:
                console.print(f"[yellow]API durum kodu: {response.status_code}[/yellow]")
        except Exception as e:
            console.print(f"[red][!] LeakDB sorgusunda hata:[/red] {e}")

def ip_history():
    """Hedef IP'nin tarihçesini gösterir"""
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: IP History for [white]{target}[/white] :::[/bold yellow]")
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]IP tarihçesi sorgulanıyor...[/bold green]", total=100)
        try:
            ip = socket.gethostbyname(target)
            # API: viewdns.net
            url = f"https://viewdns.net/api/?apikey=demo&action=iphistory&domain={target}&output=json"
            response = requests.get(url, timeout=10)
            progress.update(task, advance=100)
            
            if response.status_code == 200:
                data = response.json()
                if "response" in data and data["response"]:
                    table = Table(show_header=True, header_style="bold blue", border_style="blue", expand=True)
                    table.add_column("IP Adresi", style="cyan")
                    table.add_column("Tarih", style="yellow")
                    table.add_column("ISP", style="green")
                    
                    for entry in data["response"][:15]:
                        table.add_row(
                            entry.get("ip", "-"),
                            entry.get("date", "-"),
                            entry.get("isp", "-")
                        )
                    console.print(table)
                else:
                    console.print("[yellow]IP tarihçesi bulunamadı.[/yellow]")
        except Exception as e:
            console.print(f"[red][!] IP History sorgusunda hata:[/red] {e}")

def dns_history():
    """Domenin DNS tarihçesini gösterir"""
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: DNS History for [white]{target}[/white] :::[/bold yellow]")
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]DNS tarihçesi sorgulanıyor...[/bold green]", total=100)
        try:
            domain = target.split('/')[0]
            # API: viewdns.net
            url = f"https://viewdns.net/api/?apikey=demo&action=dnshistory&domain={domain}&output=json"
            response = requests.get(url, timeout=10)
            progress.update(task, advance=100)
            
            if response.status_code == 200:
                data = response.json()
                if "response" in data:
                    table = Table(show_header=True, header_style="bold magenta", border_style="magenta", expand=True)
                    table.add_column("IP Adresi", style="cyan")
                    table.add_column("Tarih", style="yellow")
                    
                    for entry in data["response"][:15]:
                        table.add_row(entry.get("ip", "-"), entry.get("date", "-"))
                    console.print(table)
                else:
                    console.print("[yellow]DNS tarihçesi bulunamadı.[/yellow]")
        except Exception as e:
            console.print(f"[red][!] DNS History sorgusunda hata:[/red] {e}")

def banner_grab():
    """Sunucu banner bilgilerini alır"""
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: Banner Grab for [white]{target}[/white] :::[/bold yellow]")
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]Banner bilgisi alınıyor...[/bold green]", total=100)
        try:
            url = f"https://{target}" if not target.startswith("http") else target
            response = requests.get(url, timeout=10, verify=False)
            headers = response.headers
            progress.update(task, advance=100)
            
            table = Table(show_header=True, header_style="bold cyan", border_style="cyan", expand=True)
            table.add_column("Header", style="green")
            table.add_column("Değer", style="yellow")
            
            critical_headers = ["Server", "X-Powered-By", "X-AspNet-Version", "X-Generator", "Content-Management-System"]
            for header in critical_headers:
                if header in headers:
                    table.add_row(header, headers[header])
            
            console.print(table)
            osint_report_data['banner'] = dict(response.headers)
        except Exception as e:
            console.print(f"[red][!] Banner Grab sorgusunda hata:[/red] {e}")

def cms_detect():
    """Sitenin CMS sistemini tespit eder"""
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: CMS Detection for [white]{target}[/white] :::[/bold yellow]")
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]CMS tespit ediliyor...[/bold green]", total=100)
        try:
            url = f"https://{target}" if not target.startswith("http") else target
            response = requests.get(url, timeout=10, verify=False)
            content = response.text.lower()
            headers = response.headers
            progress.update(task, advance=100)
            
            detected_cms = []
            
            # CMS İmzaları
            cms_signatures = {
                "WordPress": ["/wp-content/", "wp-includes", "wordpress", "wp-admin"],
                "Joomla": ["/components/", "/modules/", "joomla"],
                "Drupal": ["/sites/", "/modules/", "/themes/", "drupal"],
                "Magento": ["/media/", "/skin/", "/var/", "magento"],
                "Shopify": ["Shopify.app"],
                "Wix": ["wix.com", "wixstatic"],
                "Squarespace": ["squarespace"],
                "Ghost": ["ghost"],
                "Webflow": ["webflow"],
            }
            
            for cms, signatures in cms_signatures.items():
                if any(sig in content for sig in signatures):
                    detected_cms.append(cms)
            
            if detected_cms:
                table = Table(show_header=True, header_style="bold green", border_style="green", expand=True)
                table.add_column("CMS Sistemi", style="cyan")
                for cms in detected_cms:
                    table.add_row(f"[bold green]✓ {cms}[/bold green]")
                console.print(table)
                osint_report_data['cms'] = detected_cms
            else:
                console.print("[yellow]Bilinen CMS sistemi tespit edilemedi.[/yellow]")
        except Exception as e:
            console.print(f"[red][!] CMS Detection sorgusunda hata:[/red] {e}")

def favicon_hash():
    """Favicon hash'i ile aynı saçları bulur"""
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: Favicon Hash Analysis for [white]{target}[/white] :::[/bold yellow]")
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]Favicon hash hesaplanıyor...[/bold green]", total=100)
        try:
            import base64
            import hashlib
            
            url = f"https://{target}" if not target.startswith("http") else target
            response = requests.get(url, timeout=10, verify=False)
            
            # Favicon bulma
            favicon_url = None
            if '<link rel="icon"' in response.text or '<link rel="shortcut icon"' in response.text:
                import re
                match = re.search(r'<link[^>]*href=["\']([^"\']*favicon[^"\']*)["\']', response.text, re.I)
                if match:
                    favicon_url = match.group(1)
            
            if not favicon_url:
                favicon_url = f"{'/'.join(url.split('/')[:3])}/favicon.ico"
            
            favicon_response = requests.get(favicon_url, timeout=5, verify=False)
            progress.update(task, advance=100)
            
            if favicon_response.status_code == 200:
                favicon_hash = hashlib.md5(favicon_response.content).hexdigest()
                
                table = Table(show_header=True, header_style="bold yellow", border_style="yellow", expand=True)
                table.add_column("Bilgi", style="green")
                table.add_column("Değer", style="yellow")
                table.add_row("Favicon URL", favicon_url)
                table.add_row("MD5 Hash", favicon_hash)
                console.print(table)
                osint_report_data['favicon_hash'] = favicon_hash
            else:
                console.print("[yellow]Favicon bulunamadı.[/yellow]")
        except Exception as e:
            console.print(f"[red][!] Favicon Hash sorgusunda hata:[/red] {e}")

def port_lite_scan():
    """Hafif port taraması (nmap olmadan)"""
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    
    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        console.print(f"[red][!] Port taraması başarısız: Hedef IP'ye dönüştürülemedi.[/red]")
        return
    
    console.print(f"\n[bold yellow]::: Lightweight Port Scan for [white]{ip}[/white] :::[/bold yellow]")
    
    common_ports = [22, 80, 443, 8080, 3306, 5432, 27017, 6379, 5900]
    table = Table(show_header=True, header_style="bold green", border_style="green", expand=True)
    table.add_column("Port", style="cyan")
    table.add_column("Durum", style="green")
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]Portlar taranıyor...[/bold green]", total=len(common_ports))
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((ip, port))
                sock.close()
                
                if result == 0:
                    table.add_row(str(port), "[green]AÇIK[/green]")
                else:
                    table.add_row(str(port), "[red]KAPALI[/red]")
            except:
                pass
            progress.update(task, advance=1)
    
    console.print(table)

def url_scan():
    """Sitede tüm URL'leri çıkarır (JS, CSS, IMG dahil)"""
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: URL Scan for [white]{target}[/white] :::[/bold yellow]")
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]URL'ler taranıyor...[/bold green]", total=100)
        try:
            from bs4 import BeautifulSoup
            import re
            
            url = f"https://{target}" if not target.startswith("http") else target
            response = requests.get(url, timeout=10, verify=False)
            soup = BeautifulSoup(response.content, "html.parser")
            progress.update(task, advance=100)
            
            urls = {
                "links": [],
                "scripts": [],
                "stylesheets": [],
                "images": []
            }
            
            for link in soup.find_all('a', href=True):
                urls["links"].append(link['href'])
            
            for script in soup.find_all('script', src=True):
                urls["scripts"].append(script['src'])
            
            for style in soup.find_all('link', rel='stylesheet'):
                urls["stylesheets"].append(style['href'])
            
            for img in soup.find_all('img', src=True):
                urls["images"].append(img['src'])
            
            table = Table(show_header=True, header_style="bold cyan", border_style="cyan", expand=True)
            table.add_column("Tür", style="green")
            table.add_column("Sayı", style="yellow")
            table.add_row("Links", f"[bold blue]{len(urls['links'])}[/bold blue]")
            table.add_row("Scripts", f"[bold red]{len(urls['scripts'])}[/bold red]")
            table.add_row("Stylesheets", f"[bold green]{len(urls['stylesheets'])}[/bold green]")
            table.add_row("Images", f"[bold yellow]{len(urls['images'])}[/bold yellow]")
            console.print(table)
            
            osint_report_data['urlscan'] = urls
        except ImportError:
            console.print("[red][!] BeautifulSoup4 kütphanesi eksik.[/red]")
        except Exception as e:
            console.print(f"[red][!] URL Scan sorgusunda hata:[/red] {e}")

def js_finder():
    """JavaScript dosyalarını bulur ve API anahtarları arar"""
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: JavaScript Finder for [white]{target}[/white] :::[/bold yellow]")
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]JavaScript dosyaları taranıyor...[/bold green]", total=100)
        try:
            from bs4 import BeautifulSoup
            import re
            
            url = f"https://{target}" if not target.startswith("http") else target
            response = requests.get(url, timeout=10, verify=False)
            soup = BeautifulSoup(response.content, "html.parser")
            progress.update(task, advance=50)
            
            js_files = []
            for script in soup.find_all('script', src=True):
                js_files.append(script['src'])
            
            # Gizli anahtarları ara
            secrets_patterns = {
                "API Keys": r'["\']?(api[_-]?key|apikey)["\']?\s*:\s*["\']([^"\']+)["\']',
                "AWS": r'AKIA[0-9A-Z]{16}',
                "GitHub": r'ghp_[0-9a-zA-Z]{36}',
                "Slack": r'xox[baprs]-[0-9]{10,13}-[a-zA-Z0-9]{24,32}',
            }
            
            found_secrets = []
            for js_file in js_files[:5]:
                try:
                    if js_file.startswith('/'):
                        js_url = f"{'/'.join(url.split('/')[:3])}{js_file}"
                    else:
                        js_url = f"{url.rstrip('/')}/{js_file}"
                    
                    js_response = requests.get(js_url, timeout=5, verify=False)
                    if js_response.status_code == 200:
                        for secret_name, pattern in secrets_patterns.items():
                            matches = re.findall(pattern, js_response.text)
                            if matches:
                                found_secrets.append((secret_name, js_file))
                except:
                    pass
            progress.update(task, advance=100)
            
            table = Table(show_header=True, header_style="bold yellow", border_style="yellow", expand=True)
            table.add_column("JS Dosyası", style="cyan")
            for js_file in js_files[:10]:
                table.add_row(js_file)
            console.print(table)
            
            if found_secrets:
                console.print("[red][!] Olası sırlar bulundu:[/red]")
                for secret_name, js_file in found_secrets:
                    console.print(f"  [yellow]{secret_name}[/yellow] in {js_file}")
            
            osint_report_data['jsfinder'] = js_files
        except Exception as e:
            console.print(f"[red][!] JS Finder sorgusunda hata:[/red] {e}")

def admin_finder():
    """Admin panel yollarını bulur"""
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: Admin Panel Finder for [white]{target}[/white] :::[/bold yellow]")
    
    admin_paths = [
        "/admin", "/administrator", "/admin.php", "/panel", "/controlpanel",
        "/wp-admin", "/admin/index.html", "/administrator/index.php",
        "/backend", "/dashboard", "/login", "/user", "/staff"
    ]
    
    table = Table(show_header=True, header_style="bold red", border_style="red", expand=True)
    table.add_column("Path", style="cyan")
    table.add_column("Durum", style="green")
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]Admin panel yolları taranıyor...[/bold green]", total=len(admin_paths))
        
        for path in admin_paths:
            try:
                url = f"https://{target}{path}"
                response = requests.get(url, timeout=3, verify=False)
                if response.status_code == 200:
                    table.add_row(path, "[green]BULUNDU (200)[/green]")
                elif response.status_code in [301, 302]:
                    table.add_row(path, "[yellow]YÖNLENDIRME[/yellow]")
                elif response.status_code == 401:
                    table.add_row(path, "[red]KORUNAN (401)[/red]")
            except:
                pass
            progress.update(task, advance=1)
    
    console.print(table)

def file_leaks():
    """Açıklanmış dosyaları kontrol eder"""
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: File Leaks Check for [white]{target}[/white] :::[/bold yellow]")
    
    sensitive_files = [
        ".env", "config.php", ".git", "backup.zip", ".env.backup",
        ".env.old", ".env.example", "config.json", "web.config",
        ".htaccess", "robots.txt", "sitemap.xml", ".DS_Store",
        "composer.lock", "package.lock.json", "Dockerfile", ".docker"
    ]
    
    table = Table(show_header=True, header_style="bold red", border_style="red", expand=True)
    table.add_column("Dosya", style="cyan")
    table.add_column("Durum", style="green")
    
    found_any = False
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]Hassas dosyalar taranıyor...[/bold green]", total=len(sensitive_files))
        
        for filename in sensitive_files:
            try:
                url = f"https://{target}/{filename}"
                response = requests.get(url, timeout=3, verify=False)
                if 200 <= response.status_code < 400:
                    table.add_row(filename, f"[bold red]AÇIK ({response.status_code})[/bold red]")
                    found_any = True
            except:
                pass
            progress.update(task, advance=1)
    
    console.print(table)
    if found_any:
        console.print("[red][!] RİSK: Açıklanmış dosya bulundu![/red]")

def verify_email(email):
    """Email adresinin geçerli olup olmadığını kontrol eder"""
    console.print(f"\n[bold yellow]::: Email Verification for [white]{email}[/white] :::[/bold yellow]")
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]Email doğrulanıyor...[/bold green]", total=100)
        try:
            import re
            
            # Format kontrolü
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                console.print("[red]Geçersiz email formatı.[/red]")
                return
            
            domain = email.split('@')[1]
            
            # MX kaydı kontrolü
            mx_records = dns.resolver.resolve(domain, 'MX')
            progress.update(task, advance=50)
            
            if mx_records:
                mx_host = str(mx_records[0].exchange)
                console.print(f"[green]✓ Geçerli email adresi[/green]")
                console.print(f"[cyan]MX Host: {mx_host}[/cyan]")
                osint_report_data['verify_email'] = {"email": email, "status": "valid", "mx_host": mx_host}
            progress.update(task, advance=100)
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
            console.print("[red]✗ MX kaydı bulunamadı - geçersiz domain[/red]")
        except Exception as e:
            console.print(f"[red][!] Email doğrulama sorgusunda hata:[/red] {e}")

def cookie_analyze():
    """Sitenin cookie'lerini analiz eder"""
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: Cookie Analysis for [white]{target}[/white] :::[/bold yellow]")
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]Cookie'ler analiz ediliyor...[/bold green]", total=100)
        try:
            url = f"https://{target}" if not target.startswith("http") else target
            response = requests.get(url, timeout=10, verify=False)
            progress.update(task, advance=100)
            
            cookies = response.cookies
            table = Table(show_header=True, header_style="bold cyan", border_style="cyan", expand=True)
            table.add_column("Cookie Adı", style="green")
            table.add_column("Değer", style="yellow")
            table.add_column("Özellikler", style="magenta")
            
            for cookie in cookies:
                properties = []
                if hasattr(cookie, 'secure') and cookie.secure:
                    properties.append("[green]Secure[/green]")
                if hasattr(cookie, 'has_nonstandard_attr'):
                    if 'httponly' in cookie._rest:
                        properties.append("[blue]HttpOnly[/blue]")
                    if 'samesite' in cookie._rest:
                        properties.append("[yellow]SameSite[/yellow]")
                
                table.add_row(cookie.name, cookie.value[:30] + "..." if len(str(cookie.value)) > 30 else cookie.value, ", ".join(properties) if properties else "Standart")
            
            console.print(table)
            osint_report_data['cookies'] = {c.name: str(c.value) for c in cookies}
        except Exception as e:
            console.print(f"[red][!] Cookie analizi sorgusunda hata:[/red] {e}")

def os_detect():
    """Sunucunun işletim sistemini tespit eder"""
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: OS Detection for [white]{target}[/white] :::[/bold yellow]")
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]İşletim sistemi tespit ediliyor...[/bold green]", total=100)
        try:
            url = f"https://{target}" if not target.startswith("http") else target
            response = requests.get(url, timeout=10, verify=False)
            headers = response.headers
            progress.update(task, advance=100)
            
            os_detected = "Bilinmiyor"
            
            if "Server" in headers:
                server = headers["Server"].lower()
                if "windows" in server or "iis" in server:
                    os_detected = "Windows"
                elif "linux" in server or "ubuntu" in server or "debian" in server:
                    os_detected = "Linux"
                elif "apache" in server or "nginx" in server:
                    os_detected = "Linux (Muhtemelen)"
                elif "darwin" in server or "macos" in server:
                    os_detected = "macOS"
            
            table = Table(show_header=True, header_style="bold green", border_style="green", expand=True)
            table.add_column("Bilgi", style="cyan")
            table.add_column("Değer", style="yellow")
            table.add_row("Tespit Edilen OS", os_detected)
            table.add_row("Server Header", headers.get("Server", "-"))
            console.print(table)
            osint_report_data['os'] = os_detected
        except Exception as e:
            console.print(f"[red][!] OS Detection sorgusunda hata:[/red] {e}")

def cdn_check():
    """Sitenin CDN kullanıp kullanmadığını kontrol eder"""
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: CDN Check for [white]{target}[/white] :::[/bold yellow]")
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]CDN kontrol ediliyor...[/bold green]", total=100)
        try:
            ip = socket.gethostbyname(target)
            url = f"https://{target}" if not target.startswith("http") else target
            response = requests.get(url, timeout=10, verify=False)
            headers = response.headers
            progress.update(task, advance=100)
            
            cdn_signatures = {
                "Cloudflare": ["cf-ray", "cf-request-id", "cf-cache-status"],
                "Akamai": ["x-akamai-transformed", "x-akamai-cache-status"],
                "Fastly": ["x-fastly-request-id", "x-cache"],
                "Cloudflare / Akamai": ["x-cdn"],
                "AWS CloudFront": ["x-amz-cf-id"],
                "Incapsula": ["x-cdn", "x-iinfo"],
                "CDN77": ["x-cdn"],
                "Sucuri": ["x-sucuri-id"],
            }
            
            detected_cdns = []
            for cdn_name, signatures in cdn_signatures.items():
                if any(sig in headers for sig in signatures):
                    detected_cdns.append(cdn_name)
            
            table = Table(show_header=True, header_style="bold yellow", border_style="yellow", expand=True)
            table.add_column("Bilgi", style="green")
            table.add_column("Değer", style="yellow")
            table.add_row("CDN Kullanıyor", "[green]Evet[/green]" if detected_cdns else "[red]Hayır[/red]")
            if detected_cdns: table.add_row("Türü", ", ".join(detected_cdns))
            console.print(table)
            osint_report_data['cdn'] = detected_cdns
        except Exception as e:
            console.print(f"[red][!] CDN Check sorgusunda hata:[/red] {e}")

def screenshot():
    """Sitenin screenshot'ını alır"""
    if not target: console.print("[red][!] Hedef ayarlı değil. 'set target <hedef>' kullanın.[/red]"); return
    console.print(f"\n[bold yellow]::: Screenshot for [white]{target}[/white] :::[/bold yellow]")
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]Screenshot alınıyor...[/bold green]", total=100)
        try:
            domain = target.split('/')[0]
            url = f"https://screenshots.codetabs.com/o:800,h:600/{domain}"
            response = requests.get(url, timeout=15)
            progress.update(task, advance=100)
            
            if response.status_code == 200:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshots/screenshot_{domain}_{timestamp}.png"
                os.makedirs('screenshots', exist_ok=True)
                
                with open(filename, 'wb') as f:
                    f.write(response.content)
                
                console.print(f"[green]✓ Screenshot kaydedildi:[/green] [white]{os.path.abspath(filename)}[/white]")
                osint_report_data['screenshot'] = filename
            else:
                console.print("[yellow]Screenshot API hatası.[/yellow]")
        except Exception as e:
            console.print(f"[red][!] Screenshot sorgusunda hata:[/red] {e}")

# --- Global OSINT Report Data ---
osint_report_data = {}

# --- Eksik OSINT Fonksiyonları ---

def ipinfo_lookup():
    """IP bilgisi"""
    if not target: console.print("[red][!] Target not set.[/red]"); return
    console.print(f"\n[bold yellow]::: IP Info for [white]{target}[/white] :::[/bold yellow]")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]Fetching...[/bold green]", total=100)
        try:
            ip = socket.gethostbyname(target)
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
            progress.update(task, advance=100)
            
            if response.get("status") == "fail": console.print(f"[red]Error: {response.get('message')}[/red]"); return
            
            table = Table(show_header=True, header_style="bold blue", border_style="blue", expand=True)
            table.add_column("Info", style="green")
            table.add_column("Value", style="yellow")
            
            table.add_row("IP", response.get("query", "-"))
            table.add_row("ISP", response.get("isp", "-"))
            table.add_row("Org", response.get("org", "-"))
            table.add_row("Country", response.get("country", "-"))
            table.add_row("City", response.get("city", "-"))
            table.add_row("AS", response.get("as", "-"))
            console.print(table)
            osint_report_data['ipinfo'] = response
        except Exception as e: console.print(f"[red]Error: {e}[/red]")

def reputation_check():
    """Reputation kontrolü"""
    api_key = os.environ.get('VIRUSTOTAL_API_KEY')
    if not api_key: console.print("[red][!] VIRUSTOTAL_API_KEY yok.[/red]"); return
    if not target: console.print("[red][!] Target not set.[/red]"); return
    console.print(f"\n[bold yellow]::: Reputation for [white]{target}[/white] :::[/bold yellow]")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]Checking...[/bold green]", total=100)
        try:
            domain = target.split('/')[0]
            url = f"https://www.virustotal.com/api/v3/domains/{domain}"
            headers = {"x-apikey": api_key}
            response = requests.get(url, headers=headers, timeout=10)
            progress.update(task, advance=100)
            
            if response.status_code == 200:
                data = response.json()["data"]["attributes"]["last_analysis_stats"]
                table = Table(show_header=True, header_style="bold magenta", border_style="magenta", expand=True)
                table.add_column("Status", style="green")
                table.add_column("Count", style="yellow")
                table.add_row("Malicious", f"[red]{data.get('malicious', 0)}[/red]")
                table.add_row("Suspicious", f"[yellow]{data.get('suspicious', 0)}[/yellow]")
                table.add_row("Harmless", f"[green]{data.get('harmless', 0)}[/green]")
                console.print(table)
                osint_report_data['reputation'] = data
            else: console.print(f"[red]API Error: {response.status_code}[/red]")
        except Exception as e: console.print(f"[red]Error: {e}[/red]")

def techstack_detection():
    """Teknoloji tespiti"""
    if not target: console.print("[red][!] Target not set.[/red]"); return
    console.print(f"\n[bold yellow]::: TechStack for [white]{target}[/white] :::[/bold yellow]")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]Detecting...[/bold green]", total=100)
        try:
            url = f"https://{target}" if not target.startswith("http") else target
            response = requests.head(url, timeout=10, allow_redirects=True, verify=False)
            headers = response.headers
            progress.update(task, advance=100)
            
            techs = {}
            if "Server" in headers: techs["Server"] = headers["Server"]
            if "X-Powered-By" in headers: techs["Framework"] = headers["X-Powered-By"]
            if "cf-ray" in headers: techs["CDN"] = "Cloudflare"
            
            table = Table(show_header=True, header_style="bold green", border_style="green", expand=True)
            table.add_column("Tech", style="cyan")
            table.add_column("Value", style="yellow")
            for k, v in techs.items(): table.add_row(k, v)
            console.print(table if techs else "[yellow]No tech found.[/yellow]")
            osint_report_data['techstack'] = techs
        except Exception as e: console.print(f"[red]Error: {e}[/red]")

def crawler_links():
    """Link çıkarma"""
    if not target: console.print("[red][!] Target not set.[/red]"); return
    console.print(f"\n[bold yellow]::: Crawler for [white]{target}[/white] :::[/bold yellow]")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]Crawling...[/bold green]", total=100)
        try:
            from bs4 import BeautifulSoup
            from urllib.parse import urljoin, urlparse
            
            url = f"https://{target}" if not target.startswith("http") else target
            response = requests.get(url, timeout=10, verify=False)
            soup = BeautifulSoup(response.content, "html.parser")
            progress.update(task, advance=100)
            
            internal, external = set(), set()
            target_domain = urlparse(url).netloc
            
            for link in soup.find_all("a", href=True):
                href = urljoin(url, link["href"])
                link_domain = urlparse(href).netloc
                if link_domain == target_domain: internal.add(href)
                else: external.add(href)
            
            table = Table(show_header=True, header_style="bold cyan", border_style="cyan", expand=True)
            table.add_column("Type", style="green")
            table.add_column("Count", style="yellow")
            table.add_row("Internal", str(len(internal)))
            table.add_row("External", str(len(external)))
            console.print(table)
            osint_report_data['crawler'] = {"internal": list(internal)[:10], "external": list(external)[:10]}
        except Exception as e: console.print(f"[red]Error: {e}[/red]")

def emailhunter_scan():
    """Email bulma"""
    if not target: console.print("[red][!] Target not set.[/red]"); return
    console.print(f"\n[bold yellow]::: Email Hunter for [white]{target}[/white] :::[/bold yellow]")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]Scanning...[/bold green]", total=100)
        try:
            import re
            url = f"https://{target}" if not target.startswith("http") else target
            response = requests.get(url, timeout=10, verify=False)
            progress.update(task, advance=100)
            
            emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", response.text))
            
            if emails:
                table = Table(show_header=True, header_style="bold yellow", border_style="yellow", expand=True)
                table.add_column("Email", style="cyan")
                for email in list(emails)[:20]: table.add_row(email)
                console.print(table)
            else: console.print("[yellow]No emails found.[/yellow]")
            osint_report_data['emailhunter'] = list(emails)
        except Exception as e: console.print(f"[red]Error: {e}[/red]")

def perf_test():
    """Performance testi"""
    if not target: console.print("[red][!] Target not set.[/red]"); return
    console.print(f"\n[bold yellow]::: Performance Test for [white]{target}[/white] :::[/bold yellow]")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]Testing...[/bold green]", total=100)
        try:
            import time as time_module
            url = f"https://{target}" if not target.startswith("http") else target
            start = time_module.time()
            response = requests.get(url, timeout=10, verify=False)
            elapsed = (time_module.time() - start) * 1000
            progress.update(task, advance=100)
            
            table = Table(show_header=True, header_style="bold green", border_style="green", expand=True)
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="yellow")
            table.add_row("Response Time (ms)", f"{elapsed:.2f}")
            table.add_row("Status", str(response.status_code))
            table.add_row("Size (bytes)", str(len(response.content)))
            console.print(table)
            osint_report_data['perf'] = {"response_time_ms": elapsed, "status_code": response.status_code}
        except Exception as e: console.print(f"[red]Error: {e}[/red]")

def asn_lookup():
    """ASN bilgisi"""
    if not target: console.print("[red][!] Target not set.[/red]"); return
    console.print(f"\n[bold yellow]::: ASN for [white]{target}[/white] :::[/bold yellow]")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]Fetching...[/bold green]", total=100)
        try:
            ip = socket.gethostbyname(target)
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
            progress.update(task, advance=100)
            
            table = Table(show_header=True, header_style="bold magenta", border_style="magenta", expand=True)
            table.add_column("Field", style="green")
            table.add_column("Value", style="yellow")
            table.add_row("AS", response.get("as", "-"))
            table.add_row("ISP", response.get("isp", "-"))
            table.add_row("Org", response.get("org", "-"))
            table.add_row("Country", response.get("country", "-"))
            console.print(table)
            osint_report_data['asn'] = response
        except Exception as e: console.print(f"[red]Error: {e}[/red]")

def sitemap_extractor():
    """Sitemap çıkarma"""
    if not target: console.print("[red][!] Target not set.[/red]"); return
    console.print(f"\n[bold yellow]::: Sitemap for [white]{target}[/white] :::[/bold yellow]")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]Fetching...[/bold green]", total=100)
        try:
            import xml.etree.ElementTree as ET
            base_url = f"https://{target}" if not target.startswith("http") else target
            sitemap_url = base_url.rstrip("/") + "/sitemap.xml"
            response = requests.get(sitemap_url, timeout=10)
            progress.update(task, advance=100)
            
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                urls = [url.text for url in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
                
                table = Table(show_header=True, header_style="bold cyan", border_style="cyan", expand=True)
                table.add_column("URL", style="yellow")
                for url in urls[:20]: table.add_row(url)
                console.print(table)
                if len(urls) > 20: console.print(f"[yellow]... +{len(urls) - 20}[/yellow]")
                osint_report_data['sitemap'] = urls
            else: console.print("[yellow]Sitemap not found (404).[/yellow]")
        except Exception as e: console.print(f"[red]Error: {e}[/red]")

def iprange_finder():
    """IP adresleri"""
    if not target: console.print("[red][!] Target not set.[/red]"); return
    console.print(f"\n[bold yellow]::: IP Range for [white]{target}[/white] :::[/bold yellow]")
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]Resolving...[/bold green]", total=100)
        try:
            ips = set()
            try: ips.add(socket.gethostbyname(target))
            except: pass
            try:
                results = socket.getaddrinfo(target, None)
                for result in results: ips.add(result[4][0])
            except: pass
            
            progress.update(task, advance=100)
            
            if ips:
                table = Table(show_header=True, header_style="bold blue", border_style="blue", expand=True)
                table.add_column("IP", style="cyan")
                for ip in ips: table.add_row(ip)
                console.print(table)
            else: console.print("[yellow]No IPs found.[/yellow]")
            osint_report_data['iprange'] = list(ips)
        except Exception as e: console.print(f"[red]Error: {e}[/red]")

def waf_detector():
    """WAF tespiti"""
    if not target: console.print("[red][!] Target not set.[/red]"); return
    console.print(f"\n[bold yellow]::: WAF Detection for [white]{target}[/white] :::[/bold yellow]")
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]Checking...[/bold green]", total=100)
        try:
            url = f"https://{target}" if not target.startswith("http") else target
            response = requests.get(url, timeout=10, verify=False)
            headers = response.headers
            progress.update(task, advance=100)
            
            waf_sigs = {
                "Cloudflare": ["cf-ray", "cf-request-id"],
                "AWS": ["x-amzn-waf-action"],
                "Akamai": ["x-akamai-transformed"],
            }
            
            detected_waf = [name for name, sigs in waf_sigs.items() if any(sig in headers for sig in sigs)]
            
            table = Table(show_header=True, header_style="bold yellow", border_style="yellow", expand=True)
            table.add_column("Status", style="green")
            table.add_column("Value", style="yellow")
            table.add_row("WAF Detected", "[green]Yes[/green]" if detected_waf else "[red]No[/red]")
            if detected_waf: table.add_row("Type", ", ".join(detected_waf))
            console.print(table)
            osint_report_data['waf'] = detected_waf
        except Exception as e: console.print(f"[red]Error: {e}[/red]")

def dnsdump_records():
    """DNS dump"""
    if not target: console.print("[red][!] Target not set.[/red]"); return
    console.print(f"\n[bold yellow]::: DNS Dump for [white]{target}[/white] :::[/bold yellow]")
    
    record_types = ["A", "AAAA", "MX", "TXT", "NS"]
    records = {}
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console) as progress:
        task = progress.add_task("[bold green]Querying...[/bold green]", total=len(record_types))
        
        for rtype in record_types:
            try:
                answers = dns.resolver.resolve(target, rtype)
                records[rtype] = [str(rdata) for rdata in answers]
            except: pass
            progress.update(task, advance=1)
    
    if records:
        table = Table(show_header=True, header_style="bold magenta", border_style="magenta", expand=True)
        table.add_column("Type", style="cyan")
        table.add_column("Values", style="yellow")
        for rtype, values in records.items():
            table.add_row(rtype, "\n".join(values) if values else "-")
        console.print(table)
    else: console.print("[yellow]No DNS records found.[/yellow]")
    osint_report_data['dnsdump'] = records

def save_osint_report(format_type="json"):
    """Rapor kaydeder"""
    if not osint_report_data: console.print("[red][!] No report data.[/red]"); return
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = os.path.join('reports', target if target else 'unknown')
    os.makedirs(report_dir, exist_ok=True)
    
    filename = os.path.join(report_dir, f"osint_report_{timestamp}.{format_type}")
    
    try:
        if format_type == "json":
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(osint_report_data, f, indent=2, ensure_ascii=False)
        else:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"OSINT Report - {target}\nDate: {datetime.datetime.now()}\n\n")
                for key, value in osint_report_data.items():
                    f.write(f"[{key.upper()}]\n{json.dumps(value, indent=2, ensure_ascii=False)}\n\n")
        
        console.print(f"[bold green][+] Report:[/bold green] [white]{os.path.abspath(filename)}[/white]")
    except Exception as e: console.print(f"[red]Error: {e}[/red]")

def sqlmap_scan():
    """SQLMap taraması"""
    if not target: console.print("[red][!] Target not set.[/red]"); return
    console.print(f"\n[bold yellow]::: SQLMap for [white]{target}[/white] :::[/bold yellow]")
    console.print("[green]✓ SQLMap module ready[/green]")
    osint_report_data['sqlmap'] = {"status": "ready"}

def full_scan():
    """FULL SCAN - Tüm taramaları çalıştır"""
    if not target:
        console.print("[red][!] Target not set.[/red]")
        return
    
    console.print(Panel(
        Text(f"🔥 FULL SCAN STARTED 🔥\nTarget: {target}\nRunning all scans...", 
             justify="center", style="bold red"),
        border_style="bold red", expand=True
    ))
    
    all_scans = [
        ("DNS", dns_lookup),
        ("Whois", whois_lookup),
        ("GeoIP", geoip_lookup),
        ("Headers", get_headers),
        ("Robots", robots_txt),
        ("Subdomains", subdomain_scan),
        ("SSL", ssl_cert_info),
        ("TechStack", techstack_detection),
        ("Crawler", crawler_links),
        ("EmailHunter", emailhunter_scan),
        ("ASN", asn_lookup),
        ("Sitemap", sitemap_extractor),
        ("IPRange", iprange_finder),
        ("WAF", waf_detector),
        ("DNSDump", dnsdump_records),
        ("ReverseIP", reverse_ip),
        ("ReverseDNS", reverse_dns),
        ("CTSearch", ct_search),
        ("IPHistory", ip_history),
        ("DNSHistory", dns_history),
        ("Banner", banner_grab),
        ("CMS", cms_detect),
        ("Favicon", favicon_hash),
        ("PortLite", port_lite_scan),
        ("URLScan", url_scan),
        ("JSFinder", js_finder),
        ("Admin", admin_finder),
        ("FileLeaks", file_leaks),
        ("Cookie", cookie_analyze),
        ("OS", os_detect),
        ("CDN", cdn_check),
        ("Perf", perf_test),
        ("PortScan", port_scan),
        ("DirScan", dir_scan),
        ("Shodan", shodan_lookup),
        ("IPInfo", ipinfo_lookup),
        ("Reputation", reputation_check),
    ]
    
    completed, failed = 0, 0
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    scan_log = os.path.join('reports', f"fullscan_{target}_{timestamp}.log")
    os.makedirs('reports', exist_ok=True)
    
    with open(scan_log, 'w', encoding='utf-8') as log_file:
        log_file.write(f"=== FULL SCAN START ===\nTarget: {target}\nDate: {datetime.datetime.now()}\nTotal: {len(all_scans)}\n\n")
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), TextColumn("[progress.percentage]{task.percentage:>3.1f}%"), transient=False, console=console) as progress:
        task = progress.add_task("[bold green]FULL SCAN running...[/bold green]", total=len(all_scans))
        
        for scan_name, scan_func in all_scans:
            try:
                console.print(f"\n[bold cyan]>>> {scan_name}[/bold cyan]")
                progress.update(task, description=f"[bold green]{scan_name}...[/bold green]")
                scan_func()
                completed += 1
                console.print(f"[green]✓ {scan_name}[/green]")
                with open(scan_log, 'a', encoding='utf-8') as log_file:
                    log_file.write(f"[{datetime.datetime.now()}] {scan_name} - OK\n")
            except Exception as e:
                failed += 1
                console.print(f"[red]✗ {scan_name}[/red]")
                with open(scan_log, 'a', encoding='utf-8') as log_file:
                    log_file.write(f"[{datetime.datetime.now()}] {scan_name} - FAILED\n")
            finally:
                progress.update(task, advance=1)
                time.sleep(0.2)
    
    console.print(Panel(
        Text(f"""
╔════════════════════════════════╗
║     FULL SCAN COMPLETE        ║
╚════════════════════════════════╝

📊 RESULTS:
  ✓ Successful: {completed}/{len(all_scans)}
  ✗ Failed: {failed}/{len(all_scans)}
  📁 Log: {scan_log}
  🎯 Target: {target}
  ⏰ Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """, justify="center", style="bold green"),
        border_style="bold green", title="[bold cyan]SUMMARY[/bold cyan]"
    ))
    
    console.print("\n[cyan]Saving report...[/cyan]")
    save_osint_report("json")

def deep_scan():
    """Tüm taramaları çalıştırır"""
    full_scan()

# --- Ana Döngü ---
# --- Ana Döngü ---
def process_command(cmd):
    """Komutu işler"""
    cmd = cmd.strip().lower()

    if cmd == "exit": 
        console.print("\n[bold red]Exiting![/bold red]")
        return "exit"
    elif cmd == "help": show_help()
    elif cmd == "full-scan": full_scan()
    elif cmd == "deep-scan": deep_scan()
    elif cmd == "sqlmap": sqlmap_scan()
    elif cmd.startswith("set target"):
        parts = cmd.split(maxsplit=2)
        if len(parts) == 3: set_target(parts[2].strip())
    elif cmd == "show target": show_target()
    elif cmd == "dns": dns_lookup()
    elif cmd == "whois": whois_lookup()
    elif cmd == "geoip": geoip_lookup()
    elif cmd == "headers": get_headers()
    elif cmd == "robots": robots_txt()
    elif cmd == "subdomains": subdomain_scan()
    elif cmd == "ssl": ssl_cert_info()
    elif cmd == "shodan": shodan_lookup()
    elif cmd == "dirscan": dir_scan()
    elif cmd == "portscan": port_scan()
    elif cmd == "scan-report": nmap_nikto_report()
    elif cmd == "ping": ping_target()
    elif cmd == "traceroute": traceroute_target()
    elif cmd.startswith("usersearch"):
        parts = cmd.split(maxsplit=1)
        if len(parts) == 2: user_search(parts[1].strip())
    elif cmd == "ipinfo": ipinfo_lookup()
    elif cmd == "reputation": reputation_check()
    elif cmd == "techstack": techstack_detection()
    elif cmd == "crawler": crawler_links()
    elif cmd == "emailhunter": emailhunter_scan()
    elif cmd == "asn": asn_lookup()
    elif cmd == "sitemap": sitemap_extractor()
    elif cmd == "iprange": iprange_finder()
    elif cmd == "waf": waf_detector()
    elif cmd == "perf": perf_test()
    elif cmd == "dnsdump": dnsdump_records()
    elif cmd == "save-report":
        # Non-interactive fallback: default to json
        format_choice = "json"
        console.print("[yellow]Auto-selecting output format: JSON[/yellow]")
        save_osint_report(format_choice)
    elif cmd == "reverse-ip": reverse_ip()
    elif cmd == "reverse-dns": reverse_dns()
    elif cmd == "ct-search": ct_search()
    elif cmd.startswith("leakdb"):
        parts = cmd.split(maxsplit=1)
        if len(parts) == 2: leakdb_search(parts[1].strip())
    elif cmd == "ip-history": ip_history()
    elif cmd == "dns-history": dns_history()
    elif cmd == "banner": banner_grab()
    elif cmd == "cms": cms_detect()
    elif cmd == "favicon": favicon_hash()
    elif cmd == "port-lite": port_lite_scan()
    elif cmd == "urlscan": url_scan()
    elif cmd == "jsfinder": js_finder()
    elif cmd == "admin": admin_finder()
    elif cmd == "fileleaks": file_leaks()
    elif cmd.startswith("verify-email"):
        parts = cmd.split(maxsplit=1)
        if len(parts) == 2: verify_email(parts[1].strip())
    elif cmd == "cookie": cookie_analyze()
    elif cmd == "os": os_detect()
    elif cmd == "cdn": cdn_check()
    elif cmd == "screenshot": screenshot()
    elif cmd == "clear": 
        console.print("[bold yellow]Clearing screen...[/bold yellow]") 
    elif cmd == "": pass
    else: console.print("[red][!] Unknown command[/red]")

def main():
    welcome_animation()
    
    console.print(Panel(Text("[bold bright_green]ReconOps CLI - OSINT Reconnaissance Platform[/bold bright_green]", justify="center"), 
                        border_style="green", expand=False, box=MINIMAL))
    
    console.print("[cyan]Help: 'help' | Full Scan: 'full-scan'[/cyan]\n")

    while True:
        try:
            cmd = Prompt.ask("[bold blue]ReconOps > [/bold blue]", console=console).strip().lower()
            if process_command(cmd) == "exit":
                break
        except KeyboardInterrupt: console.print("\n[bold red]Interrupted![/bold red]"); break
        except Exception as e: console.print(f"[red]Error: {e}[/red]")

# --- Teybr OS Integration ---

class GeconSession:
    def __init__(self, shell):
        self.shell = shell
        # Initial greeting and setup
        self.buffer = []
        try:
            with console.capture() as capture:
                # Re-run welcome part or just print a header
                console.print(Panel(Text("[bold bright_green]ReconOps CLI[/bold bright_green]", justify="center"), border_style="green", expand=False))
                console.print("[cyan]Interactive Mode Activated. Type 'exit' to return.[/cyan]")
            self.initial_output = capture.get()
        except Exception:
            self.initial_output = "Welcome to Gecon."

    def handle_input(self, command_str):
        cmd = command_str.strip()
        
        if cmd.lower() == "exit":
            self.shell.active_session = None
            return [{"text": "Exiting Gecon...", "color": "yellow"}]

        try:
            with console.capture() as capture:
                result = process_command(cmd)
            
            output_str = capture.get()
            
            lines = output_str.splitlines()
            response = []
            
            import re
            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
            
            for line in lines:
                clean_line = ansi_escape.sub('', line)
                
                # Simple color heuristic
                color = "white"
                line_lower = clean_line.lower()
                if "error" in line_lower or "[!]" in line:
                    color = "red"
                elif "[+]" in line or "success" in line_lower or "✓" in clean_line:
                    color = "green"
                elif ":::" in line or "warning" in line_lower:
                    color = "yellow"
                elif ">>>" in line:
                    color = "cyan"
                
                if clean_line.strip():
                     response.append({"text": clean_line, "color": color})
            
            # If no output captured (e.g. empty command), just return prompt or nothing?
            if not response and cmd:
               # Ensure user sees something if they typed valid command but it was silent
               pass

            if str(result) == "exit":
                self.shell.active_session = None
                response.append({"text": "Gecon session ended.", "color": "yellow"})
                
            return response

        except Exception as e:
            return [{"text": f"Gecon Error: {e}", "color": "red"}]

def register(shell):
    def start_gecon(args):
        try:
            session = GeconSession(shell)
            shell.active_session = session
            
            import re
            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
            
            output = []
            for line in session.initial_output.splitlines():
                clean = ansi_escape.sub('', line)
                if clean.strip():
                    output.append({"text": clean, "color": "cyan"})
            
            return output
        except Exception as e:
            return [{"text": f"Failed to start Gecon: {e}", "color": "red"}]

    shell.register_command("gecon", start_gecon)
    shell.register_command("reconops", start_gecon)

if __name__ == "__main__":
    main()