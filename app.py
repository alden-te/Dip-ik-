import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import warnings
import time

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Ultra Pro Dip DNA Analiz", page_icon="🧬", layout="wide")

st.title("🧬 Ultra Pro Dip DNA Analiz Sistemi")
st.markdown("80-80 Pivot + 40+ MA + 100 Bar Öncesi Yol Analizi + İstatistiksel Sentez")

@st.cache_data(ttl=86400)
def get_bist_tickers():
    try:
        from borsapy import Borsapy
        bp = Borsapy()
        stocks = bp.get_all_stocks()
        if stocks and len(stocks) > 50:
            tickers = [s['kod'] + '.IS' for s in stocks if 'kod' in s]
            st.sidebar.success(f"✅ Borsapy'den {len(tickers)} hisse çekildi.")
            return tickers
    except Exception as e:
        st.sidebar.warning(f"⚠️ Borsapy bağlantı hatası, yedek liste kullanılıyor. ({e})")
    
    return [
        "THYAO.IS", "ASELS.IS", "GARAN.IS", "EREGL.IS", "SISE.IS", "AKBNK.IS", "HALKB.IS", 
        "ISCTR.IS", "YKBNK.IS", "SAHOL.IS", "TUPRS.IS", "KCHOL.IS", "SOKM.IS", "BIMAS.IS", 
        "MGROS.IS", "FROTO.IS", "TOASO.IS", "TTRAK.IS", "ALARK.IS", "ENJSA.IS", "PETKM.IS", 
        "TCELL.IS", "TTKOM.IS", "VESBE.IS", "ARCLK.IS", "HEKTS.IS", "MAALT.IS", "OSTIM.IS", 
        "PKENT.IS", "ISGYO.IS", "AKSEN.IS", "AKGRT.IS", "ALBRK.IS", "ALGYO.IS", "ANSGR.IS", 
        "BANVT.IS", "BIZIM.IS", "BOLUC.IS", "BRKSN.IS", "BRYAT.IS", "BSOKE.IS", "CELHA.IS", 
        "CIMSA.IS", "DENGE.IS", "DERIM.IS", "DEVA.IS", "DITAS.IS", "DOHOL.IS", "ECILC.IS", 
        "ECZYT.IS", "EGEEN.IS", "EGEGR.IS", "EMKEL.IS", "ENKAI.IS", "ERBOS.IS", "ERSU.IS", 
        "ESCOM.IS", "FENER.IS", "FLAP.IS", "FORMT.IS", "GEDIK.IS", "GLYHO.IS", "GOODY.IS", 
        "GOLTS.IS", "GRNSY.IS", "GUBRF.IS", "HATEK.IS", "HUBVC.IS", "IHLAS.IS", "IHLGM.IS", 
        "ISDMR.IS", "ISFIN.IS", "ISGSY.IS", "ISYAT.IS", "IZMDC.IS", "JANTS.IS", "KAREL.IS", 
        "KARSN.IS", "KENT.IS", "KLMSN.IS", "KORDS.IS", "KUTPO.IS", "KZBGY.IS", "LOGO.IS", 
        "LUXKM.IS", "MAVI.IS", "MESYO.IS", "MIATK.IS", "MPARK.IS", "MRDIN.IS", "NETAS.IS", 
        "NIBAS.IS", "OBASE.IS", "OHHUD.IS", "ONCSM.IS", "ORGE.IS", "OTKAR.IS", "OYAKC.IS", 
        "OYLUM.IS", "OYYAT.IS", "PAGYO.IS", "PAPIL.IS", "PAREL.IS", "PASEU.IS", "PENTA.IS", 
        "PETUN.IS", "PINSU.IS", "PKART.IS", "PLTUR.IS", "PNSUT.IS", "PRDGS.IS", "PRKAB.IS", 
        "PRKME.IS", "PSDTC.IS", "PSGYO.IS", "RAYSG.IS", "RCYAS.IS", "RYSAS.IS", "SARKY.IS", 
        "SASA.IS", "SAYAS.IS", "SDTTR.IS", "SELEC.IS", "SELGD.IS", "SERNT.IS", "SEYKM.IS", 
        "SKBNK.IS", "SKTAS.IS", "SKYLP.IS", "SMART.IS", "SNGYO.IS", "SONME.IS", "SRVGY.IS", 
        "SUGRT.IS", "SUMAS.IS", "SUNTK.IS", "TATGD.IS", "TATKS.IS", "TAVHA.IS", "TEKTU.IS", 
        "TEKNO.IS", "TLMAN.IS", "TMPOL.IS", "TRGYO.IS", "TRKCM.IS", "TRNCA.IS", "TSGYO.IS", 
        "TSKB.IS", "TUCLK.IS", "TUKAS.IS", "ULUUN.IS", "UNLU.IS", "UTASY.IS", "UZRGM.IS", 
        "VAKBN.IS", "VAKKO.IS", "VANET.IS", "VERUS.IS", "VKING.IS", "VKGYO.IS", "YATAS.IS", 
        "YBOYA.IS", "YESIL.IS", "YGYO.IS", "YKSLN.IS", "YONGA.IS", "YUNSA.IS", "AVOD.IS", 
        "AYCES.IS", "AYDEM.IS"
    ]

def calc_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calc_mfi(high, low, close, volume, period=14):
    tp = (high + low + close) / 3
    mf = tp * volume
    delta_mfi = tp.diff()
    pos_mf = mf.where(delta_mfi > 0, 0).rolling(window=period).sum()
    neg_mf = mf.where(delta_mfi < 0, 0).rolling(window=period).sum()
    return 100 - (100 / (1 + pos_mf / neg_mf))

def calc_stoch_rsi(rsi, period=14, k=3, d=3):
    low_rsi = rsi.rolling(window=period).min()
    high_rsi = rsi.rolling(window=period).max()
    stoch = 100 * ((rsi - low_rsi) / (high_rsi - low_rsi))
    k_line = stoch.rolling(window=k).mean()
    d_line = k_line.rolling(window=d).mean()
    return k_line, d_line

def calc_williams_r(high, low, close, period=14):
    hh = high.rolling(window=period).max()
    ll = low.rolling(window=period).min()
    return -100 * ((hh - close) / (hh - ll))

def calc_macd(close, fast=12, slow=26, signal=9):
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    hist = macd_line - signal_line
    return macd_line, signal_line, hist

def calc_bbands(close, period=20, std_dev=2):
    mid = close.rolling(window=period).mean()
    std = close.rolling(window=period).std()
    upper = mid + (std_dev * std)
    lower = mid - (std_dev * std)
    pct = (close - lower) / (upper - lower)
    width = ((upper - lower) / mid) * 100
    return upper, mid, lower, pct, width

def calc_atr(high, low, close, period=14):
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(window=period).mean()

def calculate_massive_indicators(df):
    if df is None or len(df) < 800:
        return None
    df = df.copy()
    
    sma_periods = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 250, 300, 400, 800]
    for p in sma_periods:
        df[f'SMA_{p}'] = df['Close'].rolling(window=p).mean()
        df[f'Dist_SMA_{p}'] = ((df['Close'] - df[f'SMA_{p}']) / df[f'SMA_{p}']) * 100
        
    ema_periods = [5, 8, 10, 13, 20, 21, 30, 34, 40, 50, 60, 70, 80, 90, 100, 120, 150, 200, 300, 600]
    for p in ema_periods:
        df[f'EMA_{p}'] = df['Close'].ewm(span=p, adjust=False).mean()
        df[f'Dist_EMA_{p}'] = ((df['Close'] - df[f'EMA_{p}']) / df[f'EMA_{p}']) * 100
        
    df['RSI_14'] = calc_rsi(df['Close'], 14)
    df['MFI_14'] = calc_mfi(df['High'], df['Low'], df['Close'], df['Volume'], 14)
    k, d = calc_stoch_rsi(df['RSI_14'], 14, 3, 3)
    df['STOCHRSIk_14'] = k
    df['STOCHRSId_14'] = d
    df['WILLR_14'] = calc_williams_r(df['High'], df['Low'], df['Close'], 14)
    m, s, h = calc_macd(df['Close'], 12, 26, 9)
    df['MACD_12_26_9'] = m
    df['MACDs_12_26_9'] = s
    df['MACDh_12_26_9'] = h
    u, mid, l, p, w = calc_bbands(df['Close'], 20, 2)
    df['BBU_20'] = u
    df['BBM_20'] = mid
    df['BBL_20'] = l
    df['BBP_20'] = p
    df['BBB_20'] = w
    df['ATR_14'] = calc_atr(df['High'], df['Low'], df['Close'], 14)
    df['Vol_SMA_20'] = df['Volume'].rolling(window=20).mean()
    df['Vol_Ratio'] = df['Volume'] / df['Vol_SMA_20']
    
    return df

def find_80_80_pivots(df):
    lows = df['Low'].values
    n = len(lows)
    pivots = []
    for i in range(80, n - 80):
        if np.all(lows[i] < lows[i-80:i]) and np.all(lows[i] < lows[i+1:i+81]):
            pivots.append(i)
    return pivots

def analyze_100bar_path(df, dip_idx):
    start_idx = max(0, dip_idx - 100)
    path_window = df.iloc[start_idx : dip_idx]
    dip_bar = df.iloc[dip_idx]
    
    dip_price = float(dip_bar['Close'])
    
    ema_vals = [float(dip_bar.get(f'EMA_{p}', np.nan)) for p in [8, 13, 21, 50, 200, 600] if pd.notna(dip_bar.get(f'EMA_{p}', np.nan))]
    sma_vals = [float(dip_bar.get(f'SMA_{p}', np.nan)) for p in [20, 50, 100, 200, 800] if pd.notna(dip_bar.get(f'SMA_{p}', np.nan))]
    
    ema_tangle = (np.std(ema_vals) / np.mean(ema_vals)) * 100 if len(ema_vals) > 1 and np.mean(ema_vals) > 0 else 50
    sma_tangle = (np.std(sma_vals) / np.mean(sma_vals)) * 100 if len(sma_vals) > 1 and np.mean(sma_vals) > 0 else 50
    
    is_bearish_align = 1 if (len(ema_vals) >= 6 and all(ema_vals[i] < ema_vals[i+1] for i in range(len(ema_vals)-1))) else 0
    
    low_20 = df['Low'].iloc[max(0, dip_idx-19):dip_idx+1].min()
    high_20 = df['High'].iloc[max(0, dip_idx-19):dip_idx+1].max()
    range_20 = high_20 - low_20
    price_pos = ((dip_price - low_20) / range_20) * 100 if range_20 > 0 else 50
    
    path_stats = {
        'path_rsi_mean': float(path_window['RSI_14'].mean()),
        'path_rsi_min': float(path_window['RSI_14'].min()),
        'path_rsi_below_30_days': int((path_window['RSI_14'] < 30).sum()),
        'path_mfi_mean': float(path_window['MFI_14'].mean()),
        'path_vol_ratio_mean': float(path_window['Vol_Ratio'].mean()),
        'path_vol_spike_days': int((path_window['Vol_Ratio'] > 2.0).sum()),
        'path_bearish_align_days': 0
    }
    
    bearish_days = 0
    for i in range(len(path_window)):
        row = path_window.iloc[i]
        e_vals = [float(row.get(f'EMA_{p}', np.nan)) for p in [8, 13, 21, 50, 200, 600] if pd.notna(row.get(f'EMA_{p}', np.nan))]
        if len(e_vals) >= 6 and all(e_vals[j] < e_vals[j+1] for j in range(len(e_vals)-1)):
            bearish_days += 1
    path_stats['path_bearish_align_days'] = bearish_days
    
    return {
        'date': df.index[dip_idx].strftime('%Y-%m-%d'),
        'price': dip_price,
        'rsi': float(dip_bar.get('RSI_14', 50)),
        'mfi': float(dip_bar.get('MFI_14', 50)),
        'stoch': float(dip_bar.get('STOCHRSIk_14', 50)),
        'willr': float(dip_bar.get('WILLR_14', -50)),
        'ema_tangle': ema_tangle,
        'sma_tangle': sma_tangle,
        'is_bearish_align': is_bearish_align,
        'price_pos': price_pos,
        'vol_ratio': float(dip_bar.get('Vol_Ratio', 1.0)),
        'bbp': float(dip_bar.get('BBP_20', 0.5)),
        **path_stats
    }

def process_stock(ticker, period="5y"):
    import yfinance as yf
    try:
        df = yf.download(ticker, period=period, progress=False, timeout=15)
        if df.empty or len(df) < 800:
            return None, None
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        if isinstance(df['Volume'], pd.DataFrame):
            df['Volume'] = df['Volume'].iloc[:, 0]
        for col in ['Open', 'High', 'Low', 'Close']:
            if isinstance(df[col], pd.DataFrame):
                df[col] = df[col].iloc[:, 0]
                
        df = df.ffill().dropna()
        if len(df) < 800:
            return None, None
            
        df = calculate_massive_indicators(df)
        pivots = find_80_80_pivots(df)
        
        if len(pivots) < 1:
            return df, None
            
        dips = []
        for p_idx in pivots:
            if pd.to_datetime(df.index[p_idx]).weekday() >= 5:
                continue
            analysis = analyze_100bar_path(df, p_idx)
            if analysis:
                analysis['ticker'] = ticker
                dips.append(analysis)
                
        return df, pd.DataFrame(dips) if dips else None
    except Exception:
        return None, None

def synthesize_dip_dna(dips_df):
    if dips_df is None or dips_df.empty:
        return None
    
    dna = {
        'total_dips': len(dips_df),
        'dip_rsi_med': float(dips_df['rsi'].median()),
        'dip_rsi_25': float(dips_df['rsi'].quantile(0.25)),
        'dip_rsi_75': float(dips_df['rsi'].quantile(0.75)),
        'dip_mfi_med': float(dips_df['mfi'].median()),
        'dip_stoch_med': float(dips_df['stoch'].median()),
        'dip_ema_tangle_med': float(dips_df['ema_tangle'].median()),
        'dip_vol_ratio_med': float(dips_df['vol_ratio'].median()),
        'dip_price_pos_med': float(dips_df['price_pos'].median()),
        'dip_bearish_align_pct': float(dips_df['is_bearish_align'].mean()) * 100,
        'path_rsi_mean': float(dips_df['path_rsi_mean'].median()),
        'path_rsi_min': float(dips_df['path_rsi_min'].median()),
        'path_rsi_below_30_avg': float(dips_df['path_rsi_below_30_days'].mean()),
        'path_vol_spike_avg': float(dips_df['path_vol_spike_days'].mean()),
        'path_bearish_days_avg': float(dips_df['path_bearish_align_days'].mean())
    }
    return dna

def generate_dna_insights(dna):
    if not dna:
        return []
    insights = []
    insights.append(f"📊 **Toplam Analiz Edilen Dip:** {dna['total_dips']}")
    insights.append(f"📉 **Tipik Dip RSI:** {dna['dip_rsi_med']:.1f} (Çoğunlukla {dna['dip_rsi_25']:.1f} - {dna['dip_rsi_75']:.1f} aralığında)")
    insights.append(f"🌀 **MA Sıkışması:** Dip anında ortalama EMA tangle %{dna['dip_ema_tangle_med']:.2f}")
    insights.append(f"🚦 **Trend Durumu:** Diplerin %{dna['dip_bearish_align_pct']:.1f}'inde EMA'lar tam bearish hizalıydı (8<13<21<50<200<600)")
    insights.append(f"🛣️ **Dibe Giden Yol:** Son 100 barda ortalama {dna['path_rsi_below_30_avg']:.1f} gun RSI < 30 bolgesinde kaldi.")
    insights.append(f"💥 **Kapitulasyon:** Dibe inerken ortalama {dna['path_vol_spike_avg']:.1f} gun hacim 2 katindan fazla patladi.")
    return insights

def scan_live_for_dna(ticker, dna, lookback=60):
    import yfinance as yf
    try:
        df = yf.download(ticker, period="1y", progress=False, timeout=10)
        if df.empty or len(df) < 100:
            return []
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        if isinstance(df['Volume'], pd.DataFrame):
            df['Volume'] = df['Volume'].iloc[:, 0]
            
        df = df.ffill().dropna()
        df = calculate_massive_indicators(df)
        
        current_price = float(df.iloc[-1]['Close'])
        signals = []
        
        for i in range(len(df)-lookback, len(df)):
            row = df.iloc[i]
            date = df.index[i].strftime('%Y-%m-%d')
            if pd.to_datetime(date).weekday() >= 5:
                continue
                
            close = float(row['Close'])
            price_increase = ((current_price / close) - 1) * 100
            if price_increase >= 10.0:
                continue
                
            rsi = float(row.get('RSI_14', 50))
            mfi = float(row.get('MFI_14', 50))
            stoch = float(row.get('STOCHRSIk_14', 50))
            vol_ratio = float(row.get('Vol_Ratio', 1.0))
            bbp = float(row.get('BBP_20', 0.5))
            
            ema_vals = [float(row.get(f'EMA_{p}', np.nan)) for p in [8, 13, 21, 50, 200, 600] if pd.notna(row.get(f'EMA_{p}', np.nan))]
            ema_tangle = (np.std(ema_vals) / np.mean(ema_vals)) * 100 if len(ema_vals) > 1 and np.mean(ema_vals) > 0 else 50
            
            low_20 = df['Low'].iloc[max(0, i-19):i+1].min()
            high_20 = df['High'].iloc[max(0, i-19):i+1].max()
            range_20 = high_20 - low_20
            price_pos = ((close - low_20) / range_20) * 100 if range_20 > 0 else 50
            
            score = 0
            if dna['dip_rsi_25'] <= rsi <= dna['dip_rsi_75']: score += 25
            elif abs(rsi - dna['dip_rsi_med']) < 10: score += 15
            
            if abs(ema_tangle - dna['dip_ema_tangle_med']) < 5: score += 20
            elif ema_tangle < 10: score += 10
            
            if abs(vol_ratio - dna['dip_vol_ratio_med']) < 1.0: score += 20
            if price_pos < 30: score += 20
            if bbp < 0.2: score += 15
            
            if score >= 60:
                signals.append({
                    'date': date,
                    'price': round(close, 2),
                    'current_price': round(current_price, 2),
                    'increase_pct': round(price_increase, 2),
                    'match_score': score,
                    'rsi': round(rsi, 1),
                    'mfi': round(mfi, 1),
                    'stoch': round(stoch, 1),
                    'ema_tangle': round(ema_tangle, 2),
                    'vol_ratio': round(vol_ratio, 2),
                    'price_pos': round(price_pos, 1)
                })
        return signals
    except Exception:
        return []

with st.sidebar:
    st.header("⚙️ Kontrol Paneli")
    mode = st.radio("Analiz Modu", ["Tek Hisse Derin Analiz", "Çoklu Hisse Tarama", "Tüm BIST DNA Sentezi"], index=0)
    st.markdown("---")
    if mode == "Tek Hisse Derin Analiz":
        ticker_input = st.text_input("Hisse Kodu", "THYAO.IS").upper().strip()
        if not ticker_input.endswith('.IS'):
            ticker_input += '.IS'
    elif mode == "Çoklu Hisse Tarama":
        tickers_text = st.text_area("Hisseler (her satıra bir tane)", "THYAO.IS\nASELS.IS\nGARAN.IS\nEREGL.IS\nSISE.IS", height=150)
    
    st.markdown("---")
    st.info("🧬 **Sistem Özellikleri:**\n- 20 SMA + 20 EMA (SMA 800, EMA 600 dahil)\n- 80-80 Pivot Tespiti\n- 100 Bar Öncesi Yol Analizi\n- Python 3.14 Uyumlu")

if mode == "Tek Hisse Derin Analiz":
    st.header(f"🔬 {ticker_input} Derin Dip Analizi")
    if st.button("Analizi Başlat", type="primary"):
        with st.spinner(f"{ticker_input} verisi çekiliyor ve 40+ indikatör hesaplanıyor..."):
            df, dips_df = process_stock(ticker_input, period="10y")
        
        if dips_df is not None and not dips_df.empty:
            st.success(f"✅ {len(dips_df)} adet 80-80 pivot dibi bulundu ve analiz edildi!")
            
            dna = synthesize_dip_dna(dips_df)
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Toplam Dip", dna['total_dips'])
            col2.metric("Tipik Dip RSI", f"{dna['dip_rsi_med']:.1f}")
            col3.metric("Ort. EMA Tangle", f"%{dna['dip_ema_tangle_med']:.2f}")
            col4.metric("Bearish Hizalanma", f"%{dna['dip_bearish_align_pct']:.1f}")
            
            st.markdown("---")
            tab1, tab2, tab3 = st.tabs(["🧬 Dip DNA Sentezi", "🛣️ 100 Barlık Yol Analizi", "📈 Grafik ve Tüm Dipler"])
            
            with tab1:
                st.subheader("Bu Hisse İçin Çıkarılan Dip DNA'sı")
                insights = generate_dna_insights(dna)
                for insight in insights:
                    st.markdown(f"- {insight}")
                
                st.markdown("### 🎯 Canlı Tarama Sonuçları (Son 60 Gün)")
                with st.spinner("DNA ile canlı piyasa eşleştiriliyor..."):
                    live_signals = scan_live_for_dna(ticker_input, dna, lookback=60)
                if live_signals:
                    st.success(f"✅ {len(live_signals)} adet yüksek eşleşmeli sinyal bulundu!")
                    sig_df = pd.DataFrame(live_signals)
                    sig_df = sig_df.sort_values('match_score', ascending=False)
                    
                    def get_status(row):
                        if row['increase_pct'] < -5: return "⚠️ Zararda"
                        elif row['increase_pct'] < 3: return "🟡 Bekleme"
                        elif row['increase_pct'] < 8: return "🟢 Hareket Başladı"
                        else: return "🔴 Fırsat Kaçmış"
                    sig_df['Durum'] = sig_df.apply(get_status, axis=1)
                    
                    cols_to_show = ['date', 'price', 'current_price', 'increase_pct', 'match_score', 'rsi', 'mfi', 'ema_tangle', 'Durum']
                    st.dataframe(sig_df[cols_to_show], use_container_width=True)
                else:
                    st.warning("⚠️ Son 60 günde bu DNA profiline uyan (%60+ eşleşme) bir sinyal bulunamadı.")
            
            with tab2:
                st.subheader("Dibe Giden 100 Barlık Yolun İstatistikleri")
                st.markdown("Bir dibin gerçek olup olmadığını anlamak için oraya *nasıl* geldiğine bakmak gerekir.")
                path_df = pd.DataFrame({
                    'Metrik': [
                        'Dip Oncesi Ortalama RSI',
                        'Dip Oncesi Ulasilan En Dusuk RSI',
                        'Dip Oncesi RSI < 30 Oldugu Gun Sayisi',
                        'Dip Oncesi Ortalama Hacim Carpani',
                        'Dip Oncesi Hacim Patlamasi (>2x) Gun Sayisi',
                        'Dip Oncesi Tam Bearish MA Hizalanmasi Olan Gun Sayisi'
                    ],
                    'Medyan / Ortalama Deger': [
                        f"{dna['path_rsi_mean']:.1f}",
                        f"{dna['path_rsi_min']:.1f}",
                        f"{dna['path_rsi_below_30_avg']:.1f}
