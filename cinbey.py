# -*- coding: utf-8 -*-
"""
CinBey Cam Leak API - Matrix Style
Developer: CinBey
Telegram: @Cinweb
Sürüm: 3.0
"""

from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import requests
import re
import random
import logging
from datetime import datetime
import time

# --- KONFIGÜRASYON ---
app = Flask(__name__)
CORS(app)

# --- USER-AGENT LISTESI ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

# --- TÜM ÜLKE KODLARI (ISO 3166-1) ---
ALL_COUNTRIES = {
    # Avrupa
    'AD': 'Andorra', 'AL': 'Arnavutluk', 'AM': 'Ermenistan', 'AT': 'Avusturya',
    'AZ': 'Azerbaycan', 'BA': 'Bosna Hersek', 'BE': 'Belçika', 'BG': 'Bulgaristan',
    'BY': 'Belarus', 'CH': 'İsviçre', 'CY': 'Kıbrıs', 'CZ': 'Çekya',
    'DE': 'Almanya', 'DK': 'Danimarka', 'EE': 'Estonya', 'ES': 'İspanya',
    'FI': 'Finlandiya', 'FR': 'Fransa', 'GB': 'İngiltere', 'GE': 'Gürcistan',
    'GR': 'Yunanistan', 'HR': 'Hırvatistan', 'HU': 'Macaristan', 'IE': 'İrlanda',
    'IL': 'İsrail', 'IS': 'İzlanda', 'IT': 'İtalya', 'LT': 'Litvanya',
    'LU': 'Lüksemburg', 'LV': 'Letonya', 'MD': 'Moldova', 'ME': 'Karadağ',
    'MK': 'Kuzey Makedonya', 'MT': 'Malta', 'NL': 'Hollanda', 'NO': 'Norveç',
    'PL': 'Polonya', 'PT': 'Portekiz', 'RO': 'Romanya', 'RS': 'Sırbistan',
    'RU': 'Rusya', 'SE': 'İsveç', 'SI': 'Slovenya', 'SK': 'Slovakya',
    'SM': 'San Marino', 'TR': 'Türkiye', 'UA': 'Ukrayna', 'VA': 'Vatikan',
    
    # Asya
    'AE': 'Birleşik Arap Emirlikleri', 'AF': 'Afganistan', 'BD': 'Bangladeş',
    'BH': 'Bahreyn', 'BN': 'Brunei', 'BT': 'Butan', 'CN': 'Çin',
    'HK': 'Hong Kong', 'ID': 'Endonezya', 'IN': 'Hindistan', 'IQ': 'Irak',
    'IR': 'İran', 'JO': 'Ürdün', 'JP': 'Japonya', 'KG': 'Kırgızistan',
    'KH': 'Kamboçya', 'KP': 'Kuzey Kore', 'KR': 'Güney Kore', 'KW': 'Kuveyt',
    'KZ': 'Kazakistan', 'LA': 'Laos', 'LB': 'Lübnan', 'LK': 'Sri Lanka',
    'MM': 'Myanmar', 'MN': 'Moğolistan', 'MO': 'Makao', 'MV': 'Maldivler',
    'MY': 'Malezya', 'NP': 'Nepal', 'OM': 'Umman', 'PH': 'Filipinler',
    'PK': 'Pakistan', 'PS': 'Filistin', 'QA': 'Katar', 'SA': 'Suudi Arabistan',
    'SG': 'Singapur', 'SY': 'Suriye', 'TH': 'Tayland', 'TJ': 'Tacikistan',
    'TM': 'Türkmenistan', 'TW': 'Tayvan', 'UZ': 'Özbekistan', 'VN': 'Vietnam',
    'YE': 'Yemen',
    
    # Afrika
    'AO': 'Angola', 'BF': 'Burkina Faso', 'BI': 'Burundi', 'BJ': 'Benin',
    'BW': 'Botsvana', 'CD': 'Kongo DC', 'CF': 'Orta Afrika Cumhuriyeti',
    'CG': 'Kongo', 'CI': 'Fildişi Sahili', 'CM': 'Kamerun', 'CV': 'Cape Verde',
    'DJ': 'Cibuti', 'DZ': 'Cezayir', 'EG': 'Mısır', 'EH': 'Batı Sahra',
    'ER': 'Eritre', 'ET': 'Etiyopya', 'GA': 'Gabon', 'GH': 'Gana',
    'GM': 'Gambiya', 'GN': 'Gine', 'GQ': 'Ekvator Ginesi', 'GW': 'Gine-Bissau',
    'KE': 'Kenya', 'KM': 'Komorlar', 'LR': 'Liberya', 'LS': 'Lesotho',
    'LY': 'Libya', 'MA': 'Fas', 'MG': 'Madagaskar', 'ML': 'Mali',
    'MR': 'Moritanya', 'MU': 'Mauritius', 'MW': 'Malavi', 'MZ': 'Mozambik',
    'NA': 'Namibya', 'NE': 'Nijer', 'NG': 'Nijerya', 'RE': 'Réunion',
    'RW': 'Ruanda', 'SC': 'Seyşeller', 'SD': 'Sudan', 'SL': 'Sierra Leone',
    'SN': 'Senegal', 'SO': 'Somali', 'SS': 'Güney Sudan', 'ST': 'São Tomé ve Príncipe',
    'SZ': 'Esvatini', 'TD': 'Çad', 'TG': 'Togo', 'TN': 'Tunus',
    'TZ': 'Tanzanya', 'UG': 'Uganda', 'ZA': 'Güney Afrika', 'ZM': 'Zambiya',
    'ZW': 'Zimbabve',
    
    # Kuzey Amerika
    'AG': 'Antigua ve Barbuda', 'BB': 'Barbados', 'BS': 'Bahamalar',
    'CA': 'Kanada', 'CR': 'Kosta Rika', 'CU': 'Küba', 'DM': 'Dominik',
    'DO': 'Dominik Cumhuriyeti', 'GD': 'Grenada', 'GT': 'Guatemala',
    'HN': 'Honduras', 'HT': 'Haiti', 'JM': 'Jamaika', 'MX': 'Meksika',
    'NI': 'Nikaragua', 'PA': 'Panama', 'SV': 'El Salvador', 'TT': 'Trinidad ve Tobago',
    'US': 'Amerika Birleşik Devletleri',
    
    # Güney Amerika
    'AR': 'Arjantin', 'BO': 'Bolivya', 'BR': 'Brezilya', 'CL': 'Şili',
    'CO': 'Kolombiya', 'EC': 'Ekvador', 'GY': 'Guyana', 'PE': 'Peru',
    'PY': 'Paraguay', 'SR': 'Surinam', 'UY': 'Uruguay', 'VE': 'Venezuela',
    
    # Okyanusya
    'AU': 'Avustralya', 'FJ': 'Fiji', 'FM': 'Mikronezya', 'KI': 'Kiribati',
    'MH': 'Marshall Adaları', 'NZ': 'Yeni Zelanda', 'PG': 'Papua Yeni Gine',
    'SB': 'Solomon Adaları', 'TO': 'Tonga', 'TV': 'Tuvalu', 'VU': 'Vanuatu',
    'WS': 'Samoa'
}

# --- TXT DOSYALARINI YÜKLE ---
WEBCAM_DB = []
WEBCAM_USA = []

try:
    with open('WebCamersDB.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and line.startswith('http'):
                WEBCAM_DB.append(line)
    print(f"✅ WebCamersDB.txt yüklendi: {len(WEBCAM_DB)} IP")
except:
    print("⚠️ WebCamersDB.txt bulunamadı, varsayılan veri kullanılıyor...")
    WEBCAM_DB = [
        "http://217.76.38.238:80", "http://217.76.38.237:80", "http://212.26.235.210:80",
        "http://91.199.196.151:80", "http://5.42.20.69:80", "http://85.202.233.150:81",
        "http://78.110.157.166:1024", "http://78.110.157.166:91", "http://78.110.157.166:5000",
        "http://91.108.45.201:80", "http://188.226.87.82:80", "http://46.146.208.178:81",
        "http://91.247.124.105:8081", "http://109.197.197.128:8083", "http://91.203.177.39:85",
        "http://176.62.89.111:81", "http://109.202.162.108:81", "http://188.226.22.77:80",
        "http://217.13.216.146:80", "http://176.119.241.11:8001", "http://62.133.173.82:8080"
    ]

try:
    with open('WebCamersUSA.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and line.startswith('http'):
                WEBCAM_USA.append(line)
    print(f"✅ WebCamersUSA.txt yüklendi: {len(WEBCAM_USA)} IP")
except:
    print("⚠️ WebCamersUSA.txt bulunamadı, varsayılan veri kullanılıyor...")
    WEBCAM_USA = [
        "http://8.2.73.51:80", "http://166.130.18.45:1024", "http://166.155.161.45:81",
        "http://24.113.115.44:80", "http://64.19.81.38:82", "http://64.19.81.38:81",
        "http://137.119.104.31:8080", "http://166.168.57.31:81", "http://173.13.228.92:80"
    ]

# --- FONKSİYONLAR ---

def get_countries_from_insecam():
    """Insecam'dan ülke listesini çeker"""
    try:
        url = "http://www.insecam.org/en/jsoncountries/"
        response = requests.get(url, headers={"User-Agent": random.choice(USER_AGENTS)}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('countries', {})
    except Exception as e:
        print(f"Insecam ülke listesi hatası: {e}")
    return {}

def scan_insecam_by_country(country_code, max_pages=5):
    """Insecam'dan belirli ülkeye ait kameraları tarar - TÜM SAYFALAR"""
    found_ips = []
    try:
        for page in range(max_pages):
            url = f"http://www.insecam.org/en/bycountry/{country_code}/?page={page}"
            headers = {"User-Agent": random.choice(USER_AGENTS)}
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                ip_pattern = r"http://\d+\.\d+\.\d+\.\d+:\d+"
                found = re.findall(ip_pattern, response.text)
                found_ips.extend(found)
                print(f"  Sayfa {page+1}: {len(found)} IP bulundu")
                time.sleep(0.3)
            else:
                break
    except Exception as e:
        print(f"Insecam tarama hatası ({country_code}): {e}")
    
    return list(set(found_ips))

def get_webcams_by_country(country_code):
    """Ülke koduna göre web kameralarını getirir - TÜM VERİLER"""
    country_code = country_code.upper()
    
    # Yerel veritabanı (tüm veriler)
    if country_code == 'TR':
        return WEBCAM_DB
    elif country_code == 'US':
        return WEBCAM_USA
    
    # Insecam'dan tüm sayfaları tara
    return scan_insecam_by_country(country_code, max_pages=10)

# --- HTML ŞABLONU - MATRIX STYLE ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CinBey Cam Leak • Matrix</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Share Tech Mono', monospace;
            background: #000;
            color: #00ff41;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            position: relative;
            overflow-x: hidden;
        }
        
        /* Matrix arka plan */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                linear-gradient(180deg, rgba(0,255,65,0.02) 0%, transparent 100%),
                repeating-linear-gradient(0deg, rgba(0,255,65,0.01) 0px, rgba(0,255,65,0.01) 2px, transparent 2px, transparent 4px);
            pointer-events: none;
            z-index: 0;
            animation: matrixRain 20s linear infinite;
        }
        
        @keyframes matrixRain {
            0% { background-position: 0 0; }
            100% { background-position: 0 100px; }
        }
        
        .container {
            max-width: 820px;
            width: 100%;
            background: rgba(0, 10, 0, 0.92);
            border-radius: 12px;
            padding: 28px 24px 32px;
            border: 1px solid #00ff41;
            box-shadow: 0 0 40px rgba(0, 255, 65, 0.1), inset 0 0 40px rgba(0, 255, 65, 0.05);
            position: relative;
            z-index: 1;
        }
        
        /* Glitch efekti */
        .container::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, transparent 40%, rgba(0,255,65,0.1) 50%, transparent 60%);
            background-size: 300% 300%;
            animation: glitchBorder 3s ease-in-out infinite;
            border-radius: 14px;
            z-index: -1;
        }
        
        @keyframes glitchBorder {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 6px;
            border-bottom: 1px solid rgba(0, 255, 65, 0.2);
            padding-bottom: 12px;
        }
        
        .header h1 {
            font-size: 22px;
            font-weight: 400;
            color: #00ff41;
            text-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
            letter-spacing: 2px;
        }
        
        .header h1 .cursor {
            animation: blink 1s step-end infinite;
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }
        
        .badge {
            background: rgba(0, 255, 65, 0.1);
            padding: 4px 14px;
            border-radius: 4px;
            font-size: 12px;
            color: #00ff41;
            border: 1px solid rgba(0, 255, 65, 0.3);
            letter-spacing: 1px;
        }
        
        .subtitle {
            color: #00cc33;
            font-size: 13px;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(0, 255, 65, 0.1);
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
        }
        
        .subtitle .dev {
            color: #00ff41;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            background: rgba(0, 20, 0, 0.6);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 24px;
            border: 1px solid rgba(0, 255, 65, 0.15);
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-item .number {
            font-size: 24px;
            font-weight: 400;
            color: #00ff41;
            text-shadow: 0 0 15px rgba(0, 255, 65, 0.2);
        }
        
        .stat-item .label {
            font-size: 10px;
            color: #00aa33;
            margin-top: 2px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stat-item .number.orange { color: #ffaa33; }
        .stat-item .number.blue { color: #33aaff; }
        .stat-item .number.green { color: #33ff66; }
        .stat-item .number.pink { color: #ff66aa; }
        
        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 14px;
            flex-wrap: wrap;
        }
        
        .input-group input {
            flex: 1;
            padding: 12px 16px;
            border-radius: 6px;
            border: 1px solid rgba(0, 255, 65, 0.3);
            background: rgba(0, 20, 0, 0.8);
            color: #00ff41;
            font-family: 'Share Tech Mono', monospace;
            font-size: 15px;
            min-width: 140px;
            outline: none;
            transition: 0.3s;
        }
        
        .input-group input:focus {
            border-color: #00ff41;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.1);
        }
        
        .input-group input::placeholder {
            color: #006622;
        }
        
        .btn {
            padding: 12px 24px;
            border-radius: 6px;
            border: 1px solid rgba(0, 255, 65, 0.3);
            font-family: 'Share Tech Mono', monospace;
            font-weight: 400;
            font-size: 14px;
            cursor: pointer;
            transition: 0.3s;
            background: rgba(0, 20, 0, 0.8);
            color: #00ff41;
            letter-spacing: 1px;
        }
        
        .btn:hover {
            background: rgba(0, 255, 65, 0.1);
            border-color: #00ff41;
            box-shadow: 0 0 25px rgba(0, 255, 65, 0.15);
            transform: scale(1.02);
        }
        
        .btn-primary {
            background: rgba(0, 255, 65, 0.15);
            border-color: #00ff41;
        }
        
        .btn-primary:hover {
            background: rgba(0, 255, 65, 0.25);
        }
        
        .btn-group {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 6px;
        }
        
        .btn-group .btn {
            flex: 1;
            min-width: 90px;
            text-align: center;
        }
        
        .result-box {
            margin-top: 20px;
            background: rgba(0, 10, 0, 0.9);
            border-radius: 6px;
            padding: 14px 16px;
            border: 1px solid rgba(0, 255, 65, 0.15);
            max-height: 420px;
            overflow-y: auto;
            font-family: 'Share Tech Mono', monospace;
        }
        
        .result-box::-webkit-scrollbar {
            width: 6px;
        }
        
        .result-box::-webkit-scrollbar-track {
            background: rgba(0, 20, 0, 0.5);
        }
        
        .result-box::-webkit-scrollbar-thumb {
            background: #00ff41;
            border-radius: 3px;
        }
        
        .result-box .empty {
            color: #006622;
            text-align: center;
            padding: 30px 0;
            font-size: 13px;
            letter-spacing: 2px;
        }
        
        .result-box .ip-item {
            padding: 6px 10px;
            border-bottom: 1px solid rgba(0, 255, 65, 0.05);
            font-size: 13px;
            color: #00dd44;
            word-break: break-all;
            transition: 0.2s;
        }
        
        .result-box .ip-item:hover {
            background: rgba(0, 255, 65, 0.05);
        }
        
        .result-box .ip-item:last-child {
            border-bottom: none;
        }
        
        .result-box .ip-item .idx {
            color: #006622;
            margin-right: 10px;
            font-size: 11px;
        }
        
        .result-box .ip-item .status {
            color: #00aa33;
            font-size: 10px;
            margin-left: 10px;
        }
        
        .result-box .count-badge {
            color: #00ff41;
            font-size: 12px;
            padding: 4px 12px;
            background: rgba(0, 255, 65, 0.05);
            border: 1px solid rgba(0, 255, 65, 0.1);
            border-radius: 4px;
            display: inline-block;
            margin-bottom: 12px;
            letter-spacing: 1px;
        }
        
        .footer {
            margin-top: 20px;
            text-align: center;
            font-size: 12px;
            color: #006622;
            border-top: 1px solid rgba(0, 255, 65, 0.1);
            padding-top: 16px;
            letter-spacing: 1px;
        }
        
        .footer a {
            color: #00ff41;
            text-decoration: none;
        }
        
        .footer a:hover {
            text-decoration: underline;
        }
        
        .telegram-link {
            display: inline-block;
            margin-top: 4px;
            padding: 4px 16px;
            background: rgba(0, 255, 65, 0.05);
            border: 1px solid rgba(0, 255, 65, 0.2);
            border-radius: 4px;
            color: #00ff41 !important;
            font-size: 13px;
        }
        
        .telegram-link:hover {
            background: rgba(0, 255, 65, 0.1);
            text-decoration: none !important;
        }
        
        .scanning-text {
            color: #ffaa33;
            animation: pulse 1s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
        
        @media (max-width: 600px) {
            .stats { grid-template-columns: repeat(2, 1fr); }
            .header h1 { font-size: 18px; }
            .input-group input { min-width: 100px; font-size: 13px; }
            .btn-group .btn { min-width: 60px; font-size: 12px; padding: 10px 12px; }
            .container { padding: 16px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <div class="header">
            <h1>❯ CinBey Cam Leak <span class="cursor">█</span></h1>
            <div class="badge">MATRIX v3.0</div>
        </div>
        <div class="subtitle">
            <span>$ ./scan --target=global</span>
            <span class="dev">Developer: <strong>CinBey</strong></span>
        </div>

        <!-- İSTATİSTİKLER -->
        <div class="stats">
            <div class="stat-item">
                <div class="number orange">{{ stats.total }}</div>
                <div class="label">Total Cameras</div>
            </div>
            <div class="stat-item">
                <div class="number blue">{{ stats.countries }}</div>
                <div class="label">Countries</div>
            </div>
            <div class="stat-item">
                <div class="number green">{{ stats.usa }}</div>
                <div class="label">USA</div>
            </div>
            <div class="stat-item">
                <div class="number pink">{{ stats.russia }}</div>
                <div class="label">Russia</div>
            </div>
        </div>

        <!-- ARAMA -->
        <div class="input-group">
            <input type="text" id="countryInput" placeholder="> Enter country code (TR, US, ...)" value="TR">
            <button class="btn btn-primary" onclick="getByCountry()">▶ SCAN</button>
        </div>

        <!-- BUTONLAR -->
        <div class="btn-group">
            <button class="btn" onclick="listCountries()">🌐 COUNTRIES</button>
            <button class="btn" onclick="getAll()">📡 ALL CAMS</button>
            <button class="btn" onclick="getRandom()">🎲 RANDOM</button>
        </div>

        <!-- SONUÇ ALANI -->
        <div class="result-box" id="resultBox">
            <div class="empty">$ ./cinbey --help<br>Choose a command to start scanning...</div>
        </div>

        <!-- FOOTER -->
        <div class="footer">
            <div>$ API: kenevizcamleakapi.up.railway.app</div>
            <div style="margin-top:4px;">
                Developer: <strong style="color:#00ff41;">CinBey</strong>
                &nbsp;•&nbsp;
                <a href="https://t.me/Cinweb" target="_blank" class="telegram-link">📱 @Cinweb</a>
            </div>
        </div>
    </div>

    <script>
        const API_BASE = window.location.origin;

        function showResult(data) {
            const box = document.getElementById('resultBox');
            
            if (!data || data.status === 'error') {
                box.innerHTML = `<div class="empty">❌ ${data?.message || 'No results found.'}</div>`;
                return;
            }

            // Ülke listesi
            if (data.countries && typeof data.countries === 'object') {
                let html = `<div class="count-badge">🌐 ${data.total} countries</div>`;
                const entries = Object.entries(data.countries);
                for (const [code, info] of entries.slice(0, 150)) {
                    const name = typeof info === 'string' ? info : info.country;
                    const count = typeof info === 'object' ? info.count : 0;
                    html += `<div class="ip-item"><span class="idx">${code}</span> ${name} <span style="color:#006622;">[${count}]</span></div>`;
                }
                if (entries.length > 150) {
                    html += `<div class="ip-item" style="color:#006622;text-align:center;">+ ${entries.length - 150} more...</div>`;
                }
                box.innerHTML = html;
                return;
            }

            // Kamera listesi (TÜM VERİLER)
            if (data.webcams && data.webcams.length > 0) {
                let html = `<div class="count-badge">📡 ${data.total || data.webcams.length} cameras • ${data.country_name || ''}</div>`;
                data.webcams.forEach((ip, i) => {
                    html += `<div class="ip-item"><span class="idx">${String(i+1).padStart(3, '0')}.</span> ${ip} <span class="status">[ONLINE]</span></div>`;
                });
                box.innerHTML = html;
                return;
            }

            // Rastgele
            if (data.webcam) {
                box.innerHTML = `<div class="ip-item" style="font-size:18px;text-align:center;padding:20px;">🎲 ${data.webcam} <span class="status">[ACTIVE]</span></div>`;
                return;
            }

            box.innerHTML = `<div class="empty">${data.message || 'No data.'}</div>`;
        }

        function getByCountry() {
            const code = document.getElementById('countryInput').value.trim().toUpperCase();
            if (!code) {
                document.getElementById('resultBox').innerHTML = `<div class="empty">⚠️ Enter a country code.</div>`;
                return;
            }
            
            const box = document.getElementById('resultBox');
            box.innerHTML = `<div class="empty" style="color:#ffaa33;">⏳ Scanning ${code}... <span class="scanning-text">█</span></div>`;
            
            fetch(`${API_BASE}/${code}`)
                .then(r => r.json())
                .then(data => showResult(data))
                .catch(() => showResult({ status: 'error', message: 'Connection error!' }));
        }

        function listCountries() {
            const box = document.getElementById('resultBox');
            box.innerHTML = `<div class="empty" style="color:#ffaa33;">⏳ Loading countries... <span class="scanning-text">█</span></div>`;
            
            fetch(`${API_BASE}/countries`)
                .then(r => r.json())
                .then(data => showResult(data))
                .catch(() => showResult({ status: 'error', message: 'Connection error!' }));
        }

        function getAll() {
            const box = document.getElementById('resultBox');
            box.innerHTML = `<div class="empty" style="color:#ffaa33;">⏳ Fetching all cameras... <span class="scanning-text">█</span></div>`;
            
            fetch(`${API_BASE}/all`)
                .then(r => r.json())
                .then(data => showResult(data))
                .catch(() => showResult({ status: 'error', message: 'Connection error!' }));
        }

        function getRandom() {
            fetch(`${API_BASE}/random`)
                .then(r => r.json())
                .then(data => showResult(data))
                .catch(() => showResult({ status: 'error', message: 'Connection error!' }));
        }

        // Enter tuşu ile arama
        document.getElementById('countryInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') getByCountry();
        });

        // Sayfa açılışında TR getir (TÜM VERİLER)
        window.onload = function() {
            setTimeout(getByCountry, 500);
        };
    </script>
</body>
</html>
'''

# --- API ENDPOINT'LERİ ---

@app.route('/', methods=['GET'])
def home():
    """Ana sayfa - Matrix arayüz"""
    all_cams = list(set(WEBCAM_DB + WEBCAM_USA))
    insecam = get_countries_from_insecam()
    
    stats = {
        'total': len(all_cams),
        'countries': len(ALL_COUNTRIES),
        'usa': len(WEBCAM_USA),
        'russia': insecam.get('RU', {}).get('count', 0)
    }
    
    return render_template_string(HTML_TEMPLATE, stats=stats)

@app.route('/countries', methods=['GET'])
def get_countries():
    """Tüm ülkeleri listeler"""
    insecam_countries = get_countries_from_insecam()
    
    all_countries = {}
    for code, name in ALL_COUNTRIES.items():
        count = 0
        if code in insecam_countries:
            count = insecam_countries[code].get('count', 0)
        if code == 'TR':
            count = len(WEBCAM_DB)
        elif code == 'US':
            count = len(WEBCAM_USA)
        all_countries[code] = {
            'country': name,
            'count': count
        }
    
    return jsonify({
        'status': 'success',
        'total': len(all_countries),
        'countries': all_countries,
        'developer': 'CinBey'
    })

@app.route('/<country_code>', methods=['GET'])
def get_country_webcams(country_code):
    """Belirtilen ülkenin web kameralarını döndürür - TÜM VERİLER"""
    country_code = country_code.upper()
    country_name = ALL_COUNTRIES.get(country_code, country_code)
    
    # Tüm verileri çek
    ips = get_webcams_by_country(country_code)
    
    if ips:
        return jsonify({
            'status': 'success',
            'country_code': country_code,
            'country_name': country_name,
            'total': len(ips),
            'webcams': ips,  # TÜM VERİLER
            'developer': 'CinBey'
        })
    else:
        return jsonify({
            'status': 'error',
            'country_code': country_code,
            'country_name': country_name,
            'total': 0,
            'message': f'{country_name} için hiç kamera bulunamadı!',
            'developer': 'CinBey'
        })

@app.route('/all', methods=['GET'])
def get_all_webcams():
    """Tüm web kameralarını listeler"""
    all_cams = list(set(WEBCAM_DB + WEBCAM_USA))
    
    # Popüler ülkelerden tüm verileri çek
    popular = ['DE', 'FR', 'RU', 'JP', 'IT', 'ES', 'NL', 'GB', 'CA', 'AU', 'BR', 'IN', 'CN']
    for code in popular:
        if code not in ['US', 'TR']:
            extra = scan_insecam_by_country(code, max_pages=5)
            all_cams.extend(extra)
    
    all_cams = list(set(all_cams))
    
    return jsonify({
        'status': 'success',
        'total': len(all_cams),
        'webcams': all_cams,
        'developer': 'CinBey'
    })

@app.route('/random', methods=['GET'])
def get_random_webcam():
    """Rastgele bir web kamerası döndürür"""
    all_cams = list(set(WEBCAM_DB + WEBCAM_USA))
    
    if all_cams:
        return jsonify({
            'status': 'success',
            'webcam': random.choice(all_cams),
            'developer': 'CinBey'
        })
    
    return jsonify({
        'status': 'error',
        'message': 'Hiç kamera bulunamadı!',
        'developer': 'CinBey'
    })

@app.route('/search', methods=['GET'])
def search_webcams():
    """IP adresine göre arama yapar"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({
            'status': 'error',
            'message': 'Arama sorgusu gerekli! (q parametresi)',
            'example': '/search?q=217.76',
            'developer': 'CinBey'
        })
    
    all_cams = list(set(WEBCAM_DB + WEBCAM_USA))
    results = [cam for cam in all_cams if query.lower() in cam.lower()]
    
    return jsonify({
        'status': 'success',
        'query': query,
        'total': len(results),
        'results': results,
        'developer': 'CinBey'
    })

@app.route('/stats', methods=['GET'])
def get_stats():
    """İstatistikleri gösterir"""
    all_cams = list(set(WEBCAM_DB + WEBCAM_USA))
    insecam = get_countries_from_insecam()
    
    return jsonify({
        'status': 'success',
        'stats': {
            'webcam_db': len(WEBCAM_DB),
            'webcam_usa': len(WEBCAM_USA),
            'total_webcams': len(all_cams),
            'countries': len(ALL_COUNTRIES),
            'russia': insecam.get('RU', {}).get('count', 0)
        },
        'developer': 'CinBey'
    })

@app.route('/export', methods=['GET'])
def export_webcams():
    """Tüm kameraları TXT dosyası olarak indir"""
    all_cams = list(set(WEBCAM_DB + WEBCAM_USA))
    filename = f"cinbey_webcams_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# CinBey Cam Leak - Tüm Web Kameraları\n")
        f.write(f"# Developer: CinBey\n")
        f.write(f"# Telegram: @Cinweb\n")
        f.write(f"# Toplam: {len(all_cams)}\n")
        f.write(f"# Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for cam in all_cams:
            f.write(f"{cam}\n")
    
    return send_file(filename, as_attachment=True)

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint bulunamadı!',
        'available_endpoints': [
            '/',
            '/countries',
            '/<country_code>',
            '/all',
            '/random',
            '/search?q=ip',
            '/stats',
            '/export'
        ],
        'developer': 'CinBey'
    }), 404

# --- ANA UYGULAMA ---
if __name__ == '__main__':
    all_cams = list(set(WEBCAM_DB + WEBCAM_USA))
    insecam = get_countries_from_insecam()
    
    print("=" * 70)
    print("🔥 CINBEY CAM LEAK - MATRIX STYLE 🔥")
    print("=" * 70)
    print(f"📁 WebCamersDB: {len(WEBCAM_DB)} IP")
    print(f"📁 WebCamersUSA: {len(WEBCAM_USA)} IP")
    print(f"📊 Toplam Kamera: {len(all_cams)} IP")
    print(f"🌍 Toplam Ülke: {len(ALL_COUNTRIES)} ülke")
    print(f"🇺🇸 ABD: {len(WEBCAM_USA)} IP")
    print(f"🇷🇺 Rusya: {insecam.get('RU', {}).get('count', 0)} IP")
    print("=" * 70)
    print("📡 API ÇALIŞIYOR: http://localhost:5000")
    print("=" * 70)
    print("👨‍💻 Developer: CinBey")
    print("📱 Telegram: @Cinweb")
    print("=" * 70)
    print("🎯 MATRIX MODE AKTİF - TÜM VERİLER GELİYOR!")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=5000, debug=True)