import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import warnings
import time
import yfinance as yf

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Ultra Pro Dip DNA Analiz", page_icon="🧬", layout="wide")

st.title("🧬 Ultra Pro Dip DNA Analiz Sistemi")
st.markdown("80-80 Pivot + 40+ MA + 100 Bar Öncesi Yol Analizi + İstatistiksel Sentez")

# ============================================================================
# BÖLÜM 1: TÜM BIST HİSSELERİ (İŞ YATIRIM LİSTESİNDEN)
# ============================================================================
@st.cache_data(ttl=86400)
def get_bist_tickers():
    return [
        "A1CAP.IS", "A1YEN.IS", "AAGYO.IS", "ACSEL.IS", "ADEL.IS", "ADESE.IS", "ADGYO.IS", "AEFES.IS", "AFYON.IS", "AGESA.IS",
        "AGHOL.IS", "AGROT.IS", "AGYO.IS", "AHGAZ.IS", "AHSGY.IS", "AKBNK.IS", "AKCNS.IS", "AKENR.IS", "AKFGY.IS", "AKFIS.IS",
        "AKFYE.IS", "AKGRT.IS", "AKHAN.IS", "AKMGY.IS", "AKSA.IS", "AKSEN.IS", "AKSGY.IS", "AKSUE.IS", "AKYHO.IS", "ALARK.IS",
        "ALBRK.IS", "ALBTNH.IS", "ALCAR.IS", "ALCTL.IS", "ALFAS.IS", "ALGYO.IS", "ALKA.IS", "ALKIM.IS", "ALKLC.IS", "ALTINS1.IS",
        "ALTNY.IS", "ALVES.IS", "ANELE.IS", "ANGEN.IS", "ANHYT.IS", "ANSGR.IS", "ARASE.IS", "ARCLK.IS", "ARDYZ.IS", "ARENA.IS",
        "ARFYE.IS", "ARMGD.IS", "ARSAN.IS", "ARTMS.IS", "ARZUM.IS", "ASELS.IS", "ASGYO.IS", "ASTOR.IS", "ASUZU.IS", "ATAGY.IS",
        "ATAKP.IS", "ATATP.IS", "ATATR.IS", "ATEKS.IS", "ATLAS.IS", "ATSYH.IS", "AVGYO.IS", "AVHOL.IS", "AVOD.IS", "AVPGY.IS",
        "AVTUR.IS", "AYCES.IS", "AYDEM.IS", "AYEN.IS", "AYES.IS", "AYGAZ.IS", "AZTEK.IS", "BAGFS.IS", "BAHKM.IS", "BAKAB.IS",
        "BALAT.IS", "BALSU.IS", "BANVT.IS", "BARMA.IS", "BASCM.IS", "BASGZ.IS", "BAYRK.IS", "BEGYO.IS", "BERA.IS", "BESLR.IS",
        "BESTE.IS", "BETAE.IS", "BEYAZ.IS", "BFREN.IS", "BIENY.IS", "BIGCH.IS", "BIGIN.IS", "BIGTK.IS", "BIMAS.IS", "BINBN.IS",
        "BINHO.IS", "BIOEN.IS", "BIZIM.IS", "BJKAS.IS", "BLCYT.IS", "BLUME.IS", "BMSCH.IS", "BMSTL.IS", "BNTAS.IS", "BOBET.IS",
        "BORLS.IS", "BORSK.IS", "BOSSA.IS", "BRISA.IS", "BRKO.IS", "BRKSN.IS", "BRKVY.IS", "BRLSM.IS", "BRMEN.IS", "BRSAN.IS",
        "BRYAT.IS", "BSOKE.IS", "BTCIM.IS", "BUCIM.IS", "BULGS.IS", "BURCE.IS", "BURVA.IS", "BVSAN.IS", "BYDNR.IS", "CANTE.IS",
        "CASA.IS", "CATES.IS", "CCOLA.IS", "CELHA.IS", "CEMAS.IS", "CEMTS.IS", "CEMZY.IS", "CEOEM.IS", "CGCAM.IS", "CIMSA.IS",
        "CLEBI.IS", "CMBTN.IS", "CMENT.IS", "CONSE.IS", "COSMO.IS", "CRDFA.IS", "CRFSA.IS", "CUSAN.IS", "CVKMD.IS", "CWENE.IS",
        "DAGI.IS", "DAPGM.IS", "DARDL.IS", "DCTTR.IS", "DENGE.IS", "DERHL.IS", "DERIM.IS", "DESA.IS", "DESPC.IS", "DEVA.IS",
        "DGATE.IS", "DGGYO.IS", "DGNMO.IS", "DIRIT.IS", "DITAS.IS", "DMLKTG.IS", "DMRGD.IS", "DMSAS.IS", "DNISI.IS", "DOAS.IS",
        "DOCO.IS", "DOFER.IS", "DOFRB.IS", "DOGUB.IS", "DOHOL.IS", "DOKTA.IS", "DSTKF.IS", "DUNYH.IS", "DURDO.IS", "DURKN.IS",
        "DYOBY.IS", "DZGYO.IS", "EBEBK.IS", "ECILC.IS", "ECOGR.IS", "ECZYT.IS", "EDATA.IS", "EDIP.IS", "EFOR.IS", "EGEEN.IS",
        "EGEGY.IS", "EGEPO.IS", "EGGUB.IS", "EGPRO.IS", "EGSER.IS", "EKDMR.IS", "EKGYO.IS", "EKIM.IS", "EKIZ.IS", "EKOS.IS",
        "EKSUN.IS", "ELITE.IS", "EMKEL.IS", "EMNIS.IS", "EMPAE.IS", "ENDAE.IS", "ENERY.IS", "ENJSA.IS", "ENKAI.IS", "ENPRA.IS",
        "ENSRI.IS", "ENTRA.IS", "EPLAS.IS", "ERBOS.IS", "ERCB.IS", "EREGL.IS", "ERSU.IS", "ESCAR.IS", "ESCOM.IS", "ESEN.IS",
        "ETILR.IS", "ETYAT.IS", "EUHOL.IS", "EUKYO.IS", "EUPWR.IS", "EUREN.IS", "EUYO.IS", "EYGYO.IS", "FADE.IS", "FENER.IS",
        "FLAP.IS", "FMIZP.IS", "FONET.IS", "FORMT.IS", "FORTE.IS", "FRIGO.IS", "FRMPL.IS", "FROTO.IS", "FZLGY.IS", "GARAN.IS",
        "GARFA.IS", "GATEG.IS", "GEDIK.IS", "GEDZA.IS", "GENIL.IS", "GENKM.IS", "GENTS.IS", "GEREL.IS", "GESAN.IS", "GIPTA.IS",
        "GLBMD.IS", "GLCVY.IS", "GLRMK.IS", "GLRYH.IS", "GLYHO.IS", "GMTAS.IS", "GOKNR.IS", "GOLDA.IS", "GOLTS.IS", "GOODY.IS",
        "GOZDE.IS", "GRNYO.IS", "GRSEL.IS", "GRTHO.IS", "GSDDE.IS", "GSDHO.IS", "GSRAY.IS", "GUBRF.IS", "GUNDG.IS", "GWIND.IS",
        "GZNMI.IS", "HALKB.IS", "HATEK.IS", "HATSN.IS", "HDFGS.IS", "HEDEF.IS", "HEKTS.IS", "HKTM.IS", "HLGYO.IS", "HOROZ.IS",
        "HRKET.IS", "HTTBT.IS", "HUBVC.IS", "HUNER.IS", "HURGZ.IS", "ICBCT.IS", "ICUGS.IS", "IDGYO.IS", "IEYHO.IS", "IHAAS.IS",
        "IHEVA.IS", "IHGZT.IS", "IHLAS.IS", "IHLGM.IS", "IHYAY.IS", "IMASM.IS", "INDES.IS", "INFO.IS", "INGRM.IS", "INTEK.IS",
        "INTEM.IS", "INVEO.IS", "INVES.IS", "ISATR.IS", "ISBIR.IS", "ISBTR.IS", "ISCTR.IS", "ISDMR.IS", "ISFIN.IS", "ISGSY.IS",
        "ISGYO.IS", "ISKPL.IS", "ISKUR.IS", "ISMEN.IS", "ISSEN.IS", "ISVEA.IS", "ISYAT.IS", "IZENR.IS", "IZFAS.IS", "IZINV.IS",
        "IZMDC.IS", "JANTS.IS", "KAPLM.IS", "KAREL.IS", "KARSN.IS", "KARTN.IS", "KATMR.IS", "KAYSE.IS", "KBORU.IS", "KCAER.IS",
        "KCHOL.IS", "KENT.IS", "KERVN.IS", "KFEIN.IS", "KGYO.IS", "KIMMR.IS", "KLGYO.IS", "KLKIM.IS", "KLMSN.IS", "KLNMA.IS",
        "KLRHO.IS", "KLSER.IS", "KLSYN.IS", "KLYPV.IS", "KMPUR.IS", "KNFRT.IS", "KOCMT.IS", "KONKA.IS", "KONTR.IS", "KONYA.IS",
        "KOPOL.IS", "KORDS.IS", "KOTON.IS", "KRDMA.IS", "KRDMB.IS", "KRDMD.IS", "KRGYO.IS", "KRONT.IS", "KRPLS.IS", "KRSTL.IS",
        "KRTEK.IS", "KRVGD.IS", "KSTUR.IS", "KTLEV.IS", "KTSKR.IS", "KUTPO.IS", "KUVVA.IS", "KUYAS.IS", "KZBGY.IS", "KZGYO.IS",
        "LIDER.IS", "LIDFA.IS", "LILAK.IS", "LINK.IS", "LKMNH.IS", "LMKDC.IS", "LOGO.IS", "LRSHO.IS", "LUKSK.IS", "LXGYO.IS",
        "LYDHO.IS", "LYDYE.IS", "MAALT.IS", "MACKO.IS", "MAGEN.IS", "MAKIM.IS", "MAKTK.IS", "MANAS.IS", "MARBL.IS", "MARKA.IS",
        "MARMR.IS", "MARTI.IS", "MAVI.IS", "MCARD.IS", "MEDTR.IS", "MEGAP.IS", "MEGMT.IS", "MEKAG.IS", "MEPET.IS", "MERCN.IS",
        "MERIT.IS", "MERKO.IS", "METRO.IS", "MEYSU.IS", "MGROS.IS", "MHRGY.IS", "MIATK.IS", "MMCAS.IS", "MNDRS.IS", "MNDTR.IS",
        "MOBTL.IS", "MOGAN.IS", "MOPAS.IS", "MPARK.IS", "MRGYO.IS", "MRSHL.IS", "MSGYO.IS", "MTRKS.IS", "MTRYO.IS", "MZHLD.IS",
        "NATEN.IS", "NETAS.IS", "NETCD.IS", "NIBAS.IS", "NTGAZ.IS", "NTHOL.IS", "NUGYO.IS", "NUHCM.IS", "OBAMS.IS", "OBASE.IS",
        "ODAS.IS", "ODINE.IS", "OFSYM.IS", "ONCSM.IS", "ONRYT.IS", "ORCAY.IS", "ORGE.IS", "ORMA.IS", "ORZAX.IS", "OSMEN.IS",
        "OSTIM.IS", "OTKAR.IS", "OTTO.IS", "OYAKC.IS", "OYAYO.IS", "OYLUM.IS", "OYYAT.IS", "OZATD.IS", "OZGYO.IS", "OZKGY.IS",
        "OZRDN.IS", "OZSUB.IS", "OZYSR.IS", "PAGYO.IS", "PAHOL.IS", "PAMEL.IS", "PAPIL.IS", "PARSN.IS", "PASEU.IS", "PATEK.IS",
        "PCILT.IS", "PEKGY.IS", "PENGD.IS", "PENTA.IS", "PETKM.IS", "PETUN.IS", "PGSUS.IS", "PINSU.IS", "PKART.IS", "PKENT.IS",
        "PLTUR.IS", "PNLSN.IS", "PNSUT.IS", "POLHO.IS", "POLTK.IS", "PRDGS.IS", "PRKAB.IS", "PRKME.IS", "PRZMA.IS", "PSDTC.IS",
        "PSGYO.IS", "QNBFK.IS", "QNBTR.IS", "QUAGR.IS", "RALYH.IS", "RAYSG.IS", "REEDR.IS", "RGYAS.IS", "RNPOL.IS", "RODRG.IS",
        "RTALB.IS", "RUBNS.IS", "RUZYE.IS", "RYGYO.IS", "RYSAS.IS", "SAFKR.IS", "SAHOL.IS", "SAMAT.IS", "SANEL.IS", "SANFM.IS",
        "SANKO.IS", "SARAE.IS", "SARKY.IS", "SASA.IS", "SAYAS.IS", "SDTTR.IS", "SEGMN.IS", "SEGYO.IS", "SEKFK.IS", "SEKUR.IS",
        "SELEC.IS", "SELVA.IS", "SERNT.IS", "SEYKM.IS", "SILVR.IS", "SISE.IS", "SKBNK.IS", "SKTAS.IS", "SKYLP.IS", "SKYMD.IS",
        "SMART.IS", "SMRTG.IS", "SMRVA.IS", "SNGYO.IS", "SNICA.IS", "SNPAM.IS", "SODSN.IS", "SOHOE.IS", "SOKE.IS", "SOKM.IS",
        "SONME.IS", "SRVGY.IS", "SSAAT.IS", "SUMAS.IS", "SUNTK.IS", "SURGY.IS", "SUWEN.IS", "SVGYO.IS", "TABGD.IS", "TARKM.IS",
        "TATEN.IS", "TATGD.IS", "TAVHL.IS", "TBORG.IS", "TCELL.IS", "TCKRC.IS", "TDGYO.IS", "TEHOL.IS", "TEKTU.IS", "TERA.IS",
        "TEZOL.IS", "TGSAS.IS", "THYAO.IS", "TKFEN.IS", "TKNSA.IS", "TLMAN.IS", "TMPOL.IS", "TMSN.IS", "TNZTP.IS", "TOASO.IS",
        "TRALT.IS", "TRCAS.IS", "TRENJ.IS", "TRGYO.IS", "TRHOL.IS", "TRILC.IS", "TRMET.IS", "TSGYO.IS", "TSKB.IS", "TSPOR.IS",
        "TTKOM.IS", "TTRAK.IS", "TUCLK.IS", "TUKAS.IS", "TUPRS.IS", "TUREX.IS", "TURGG.IS", "TURSG.IS", "UCAYM.IS", "UFUK.IS",
        "ULAS.IS", "ULKER.IS", "ULUFA.IS", "ULUSE.IS", "ULUUN.IS", "UMPAS.IS", "UNLU.IS", "USAK.IS", "VAKBN.IS", "VAKFA.IS",
        "VAKFN.IS", "VAKKO.IS", "VANGD.IS", "VBTYZ.IS", "VERTU.IS", "VERUS.IS", "VESBE.IS", "VESTL.IS", "VKFYO.IS", "VKGYO.IS",
        "VKING.IS", "VRGYO.IS", "VSNMD.IS", "YAPRK.IS", "YATAS.IS", "YAYLA.IS", "YBTAS.IS", "YEOTK.IS", "YESIL.IS", "YGGYO.IS",
        "YIGIT.IS", "YKBNK.IS", "YKSLN.IS", "YONGA.IS", "YUNSA.IS", "YYAPI.IS", "YYLGD.IS", "ZEDUR.IS", "ZERGY.IS", "ZGYO.IS",
        "ZOREN.IS", "ZRGYO.IS"
    ]

# ============================================================================
# BÖLÜM 2: MANUEL İNDİKATÖR HESAPLAMA
# ============================================================================
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

# ============================================================================
# BÖLÜM 3: 80-80 PIVOT VE 100 BAR ÖNCESİ YOL ANALİZİ
# ============================================================================
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

# ============================================================================
# BÖLÜM 4: DİP DNA SENTEZİ
# ============================================================================
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
        'path_vol_ratio_med': float(dips_df['vol_ratio'].median()),
        'path_vol_spike_avg': float(dips_df['path_vol_spike_days'].mean()),
        'path_bearish_days_avg': float(dips_df['path_bearish_align_days'].mean())
    }
    return dna

def generate_dna_insights(dna):
    if not dna:
        return []
    insights = []
    insights.append(f" **Toplam Analiz Edilen Dip:** {dna['total_dips']}")
    insights.append(f"📉 **Tipik Dip RSI:** {dna['dip_rsi_med']:.1f} ({dna['dip_rsi_25']:.1f} - {dna['dip_rsi_75']:.1f})")
    insights.append(f"🌀 **MA Sıkışması:** %{dna['dip_ema_tangle_med']:.2f}")
    insights.append(f"🚦 **Bearish Hizalanma:** %{dna['dip_bearish_align_pct']:.1f}")
    insights.append(f"🛣️ **RSI<30 Gün:** {dna['path_rsi_below_30_avg']:.1f} gün")
    insights.append(f"💥 **Hacim Patlaması:** {dna['path_vol_spike_avg']:.1f} gün")
    return insights

# ============================================================================
# BÖLÜM 5: CANLI TARAMA - SON 10 BAR
# ============================================================================
def scan_last_10_bars_for_signals(ticker, dna):
    try:
        df = yf.download(ticker, period="3mo", progress=False, timeout=10)
        if df.empty or len(df) < 20:
            return None
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        if isinstance(df['Volume'], pd.DataFrame):
            df['Volume'] = df['Volume'].iloc[:, 0]
        for col in ['Open', 'High', 'Low', 'Close']:
            if isinstance(df[col], pd.DataFrame):
                df[col] = df[col].iloc[:, 0]
                
        df = df.ffill().dropna()
        if len(df) < 20:
            return None
            
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

# ============================================================================
# BÖLÜM 4: DİP DNA SENTEZİ
# ============================================================================
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
        'path_vol_ratio_med': float(dips_df['vol_ratio'].median()),
        'path_vol_spike_avg': float(dips_df['path_vol_spike_days'].mean()),
        'path_bearish_days_avg': float(dips_df['path_bearish_align_days'].mean())
    }
    return dna

def generate_dna_insights(dna):
    if not dna:
        return []
    insights = []
    insights.append(f" **Toplam Analiz Edilen Dip:** {dna['total_dips']}")
    insights.append(f"📉 **Tipik Dip RSI:** {dna['dip_rsi_med']:.1f} ({dna['dip_rsi_25']:.1f} - {dna['dip_rsi_75']:.1f})")
    insights.append(f"🌀 **MA Sıkışması:** %{dna['dip_ema_tangle_med']:.2f}")
    insights.append(f"🚦 **Bearish Hizalanma:** %{dna['dip_bearish_align_pct']:.1f}")
    insights.append(f"🛣️ **RSI<30 Gün:** {dna['path_rsi_below_30_avg']:.1f} gün")
    insights.append(f"💥 **Hacim Patlaması:** {dna['path_vol_spike_avg']:.1f} gün")
    return insights
    # ============================================================================
# BÖLÜM 5: CANLI TARAMA - SON 10 BAR
# ============================================================================
def scan_last_10_bars_for_signals(ticker, dna):
    try:
        df = yf.download(ticker, period="3mo", progress=False, timeout=10)
        if df.empty or len(df) < 20:
            return None
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        if isinstance(df['Volume'], pd.DataFrame):
            df['Volume'] = df['Volume'].iloc[:, 0]
        for col in ['Open', 'High', 'Low', 'Close']:
            if isinstance(df[col], pd.DataFrame):
                df[col] = df[col].iloc[:, 0]
                
        df = df.ffill().dropna()
        if len(df) < 20:
            return None
            
        df = calculate_massive_indicators(df)
        
        current_price = float(df.iloc[-1]['Close'])
        last_10_signals = []
        
        for i in range(max(0, len(df)-10), len(df)):
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
                last_10_signals.append({
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
        
        if last_10_signals:
            return {
                'ticker': ticker,
                'signals': last_10_signals,
                'latest_signal': last_10_signals[-1]
            }
        return None
    except Exception:
        return None

# ============================================================================
# BÖLÜM 6: STREAMLIT ARAYÜZÜ
# ============================================================================
with st.sidebar:
    st.header("⚙️ Kontrol Paneli")
    mode = st.radio("Analiz Modu", ["Tek Hisse Derin Analiz", "Çoklu Hisse Tarama", "Tüm BIST DNA Sentezi", "🎯 CANLI SİNYALLER (Son 10 Bar)"], index=0)
    st.markdown("---")
    if mode == "Tek Hisse Derin Analiz":
        ticker_input = st.text_input("Hisse Kodu", "THYAO.IS").upper().strip()
        if not ticker_input.endswith('.IS'):
            ticker_input += '.IS'
    elif mode == "Çoklu Hisse Tarama":
        tickers_text = st.text_area("Hisseler (her satıra bir tane)", "THYAO.IS\nASELS.IS\nGARAN.IS\nEREGL.IS\nSISE.IS", height=150)
    
    st.markdown("---")
    st.info("🧬 **Sistem Özellikleri:**\n- 20 SMA + 20 EMA (SMA 800, EMA 600 dahil)\n- 80-80 Pivot Tespiti\n- 100 Bar Öncesi Yol Analizi\n- Python 3.14 Uyumlu")

# MOD 1: TEK HİSSE DERİN ANALİZ
if mode == "Tek Hisse Derin Analiz":
    st.header(f"🔬 {ticker_input} Derin Dip Analizi")
    if st.button("Analizi Başlat", type="primary"):
        with st.spinner(f"{ticker_input} verisi çekiliyor ve 40+ indikatör hesaplanıyor..."):
            df, dips_df = process_stock(ticker_input, period="10y")
        
        if dips_df is not None and not dips_df.empty:
            st.success(f"✅ {len(dips_df)} adet 80-80 pivot dibi bulundu!")
            
            dna = synthesize_dip_dna(dips_df)
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Toplam Dip", dna['total_dips'])
            col2.metric("Tipik Dip RSI", f"{dna['dip_rsi_med']:.1f}")
            col3.metric("Ort. EMA Tangle", f"%{dna['dip_ema_tangle_med']:.2f}")
            col4.metric("Bearish Hizalanma", f"%{dna['dip_bearish_align_pct']:.1f}")
            
            st.markdown("---")
            tab1, tab2, tab3 = st.tabs([" Dip DNA Sentezi", "🛣️ 100 Barlık Yol Analizi", "📈 Grafik"])
            
            with tab1:
                st.subheader("Bu Hisse İçin Çıkarılan Dip DNA'sı")
                insights = generate_dna_insights(dna)
                for insight in insights:
                    st.markdown(f"- {insight}")
            
            with tab2:
                st.subheader("Dibe Giden 100 Barlık Yolun İstatistikleri")
                path_df = pd.DataFrame({
                    'Metrik': ['Ortalama RSI', 'En Düşük RSI', 'RSI<30 Gün', 'Ort. Hacim', 'Hacim Patlaması', 'Bearish Gün'],
                    'Değer': [
                        f"{dna['path_rsi_mean']:.1f}",
                        f"{dna['path_rsi_min']:.1f}",
                        f"{dna['path_rsi_below_30_avg']:.1f} gün",
                        f"{dna['path_vol_ratio_med']:.2f}x",
                        f"{dna['path_vol_spike_avg']:.1f} gün",
                        f"{dna['path_bearish_days_avg']:.1f} gün"
                    ]
                })
                st.dataframe(path_df, use_container_width=True)
            
            with tab3:
                st.subheader(f"{ticker_input} Fiyat ve Pivot Dipler")
                fig = go.Figure()
                fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Fiyat'))
                
                pivot_dates = [d['date'] for d in dips_df.to_dict('records')]
                pivot_prices = [d['price'] for d in dips_df.to_dict('records')]
                fig.add_trace(go.Scatter(x=pivot_dates, y=pivot_prices, mode='markers', marker=dict(symbol='triangle-down', size=12, color='red'), name='80-80 Pivot Dipler'))
                
                for p in [50, 200, 600, 800]:
                    col_ema = f'EMA_{p}' if p in [50, 200, 600] else None
                    col_sma = f'SMA_{p}' if p == 800 else None
                    
                    if col_ema and col_ema in df.columns:
                        fig.add_trace(go.Scatter(x=df.index, y=df[col_ema], mode='lines', name=f'EMA {p}', line=dict(width=1)))
                    if col_sma and col_sma in df.columns:
                        fig.add_trace(go.Scatter(x=df.index, y=df[col_sma], mode='lines', name=f'SMA {p}', line=dict(width=1, dash='dash')))
                
                fig.update_layout(title=f"{ticker_input} Detaylı Grafik", height=600, xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"⚠️ {ticker_input} için yeterli veri veya pivot dibi bulunamadı.")

# MOD 2: ÇOKLU HİSSE TARAMA
elif mode == "Çoklu Hisse Tarama":
    st.header("🔍 Çoklu Hisse Tarama")
    tickers_list = [t.strip().upper() for t in tickers_text.split('\n') if t.strip()]
    tickers_list = [t if t.endswith('.IS') else t + '.IS' for t in tickers_list]
    
    if st.button("Taramayı Başlat", type="primary"):
        progress_bar = st.progress(0)
        all_dips = []
        
        for i, t in enumerate(tickers_list):
            try:
                df, dips_df = process_stock(t, period="5y")
                if dips_df is not None and not dips_df.empty:
                    all_dips.append(dips_df)
            except Exception:
                pass
            
            if i % 10 == 0:
                progress_bar.progress((i + 1) / len(tickers_list))
        
        progress_bar.progress(1.0)
        
        if all_dips:
            master_df = pd.concat(all_dips, ignore_index=True)
            st.success(f"✅ Tarama tamamlandı! Toplam {len(master_df)} dip analiz edildi.")
            
            master_dna = synthesize_dip_dna(master_df)
            st.subheader("🧬 Tüm Hisseler İçin Ortak Dip DNA Sentezi")
            insights = generate_dna_insights(master_dna)
            for insight in insights:
                st.markdown(f"- {insight}")
            
            st.subheader("🏆 En Çok Dip Oluşturan Hisseler")
            summary = master_df.groupby('ticker').agg(
                Dip_Sayisi=('ticker', 'count'),
                Ort_Dip_RSI=('rsi', 'mean'),
                Ort_EMA_Tangle=('ema_tangle', 'mean'),
                Ort_Yol_Hacim_Patlamasi=('path_vol_spike_days', 'mean')
            ).sort_values('Dip_Sayisi', ascending=False).reset_index()
            
            st.dataframe(summary.head(50), use_container_width=True)
        else:
            st.warning("⚠️ Hiçbir hisse için dip bulunamadı.")

# MOD 3: TÜM BIST DNA SENTEZİ
elif mode == "Tüm BIST DNA Sentezi":
    st.header(" Tüm BIST DNA Sentezi")
    st.warning("⚠️ Bu işlem 600+ hisse için çalışır ve 10-15 dakika sürebilir.")
    
    if st.button("Tüm BIST'i Tara", type="primary"):
        all_tickers = get_bist_tickers()
        st.write(f"Toplam {len(all_tickers)} hisse taranacak...")
        
        progress_bar = st.progress(0)
        all_dips = []
        start_time = time.time()
        
        for i, t in enumerate(all_tickers):
            try:
                df, dips_df = process_stock(t, period="5y")
                if dips_df is not None and not dips_df.empty:
                    all_dips.append(dips_df)
            except Exception:
                pass
            
            if i % 20 == 0:
                progress_bar.progress((i + 1) / len(all_tickers))
        
        progress_bar.progress(1.0)
        elapsed = time.time() - start_time
        
        st.success(f"✅ Tarama tamamlandı! Süre: {elapsed:.0f} saniye. {len(all_dips)} hisse için dip bulundu.")
        
        if all_dips:
            master_df = pd.concat(all_dips, ignore_index=True)
            
            master_dna = synthesize_dip_dna(master_df)
            st.subheader("🧬 Tüm BIST İçin Ortak Dip DNA Sentezi")
            insights = generate_dna_insights(master_dna)
            for insight in insights:
                st.markdown(f"- {insight}")
            
            st.subheader("🏆 En Çok Dip Oluşturan Hisseler")
            summary = master_df.groupby('ticker').agg(
                Dip_Sayisi=('ticker', 'count'),
                Ort_Dip_RSI=('rsi', 'mean'),
                Ort_EMA_Tangle=('ema_tangle', 'mean'),
                Ort_Yol_Hacim_Patlamasi=('path_vol_spike_days', 'mean')
            ).sort_values('Dip_Sayisi', ascending=False).reset_index()
            
            st.dataframe(summary.head(50), use_container_width=True)
            
            csv = master_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8')
            st.download_button("📥 Tüm Analiz Verisini İndir (CSV)", data=csv, file_name=f"bist_dip_dna_analiz_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")
        else:
            st.warning("⚠️ Hiçbir hisse için dip bulunamadı.")

# MOD 4: CANLI SİNYALLER (SON 10 BAR)
elif mode == "🎯 CANLI SİNYALLER (Son 10 Bar)":
    st.header("🎯 CANLI SİNYALLER - Son 10 Barda Sinyal Veren Hisseler")
    st.markdown("Bu modül, son 10 işlem günü içinde dip DNA'sına uyan hisseleri tespit eder.")
    
    if st.button("🔍 Canlı Sinyalleri Tara", type="primary", use_container_width=True):
        all_tickers = get_bist_tickers()
        st.write(f" {len(all_tickers)} hisse taranıyor...")
        
        progress_bar = st.progress(0)
        live_signals = []
        start_time = time.time()
        
        # Önce tüm BIST için master DNA oluştur
        st.info(" İlk olarak tüm BIST için master DNA oluşturuluyor...")
        all_dips_for_dna = []
        for i, t in enumerate(all_tickers[:100]):  # İlk 100 hisse ile DNA oluştur
            try:
                df, dips_df = process_stock(t, period="5y")
                if dips_df is not None and not dips_df.empty:
                    all_dips_for_dna.append(dips_df)
            except Exception:
                pass
        
        if all_dips_for_dna:
            master_df_dna = pd.concat(all_dips_for_dna, ignore_index=True)
            master_dna = synthesize_dip_dna(master_df_dna)
            st.success(f"✅ Master DNA oluşturuldu! {len(master_df_dna)} dip analiz edildi.")
            
            st.info("🔍 Şimdi son 10 barda sinyal veren hisseler aranıyor...")
            
            for i, t in enumerate(all_tickers):
                try:
                    result = scan_last_10_bars_for_signals(t, master_dna)
                    if result:
                        live_signals.append(result)
                except Exception:
                    pass
                
                if i % 50 == 0:
                    progress_bar.progress((i + 1) / len(all_tickers))
            
            progress_bar.progress(1.0)
            elapsed = time.time() - start_time
            
            if live_signals:
                st.success(f"✅ Tarama tamamlandı! Süre: {elapsed:.0f} saniye. **{len(live_signals)} hisse** son 10 barda sinyal verdi!")
                
                # Sonuçları göster
                st.subheader(f"🎯 Son 10 Barda Sinyal Veren {len(live_signals)} Hisse")
                
                # Her hisse için detaylı bilgi
                for signal_data in live_signals:
                    with st.expander(f"📈 {signal_data['ticker']} - {signal_data['latest_signal']['date']} - Skor: {signal_data['latest_signal']['match_score']}"):
                        latest = signal_data['latest_signal']
                        
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("Fiyat", f"{latest['price']} TL")
                        col2.metric("Mevcut Fiyat", f"{latest['current_price']} TL")
                        col3.metric("Değişim", f"%{latest['increase_pct']}")
                        col4.metric("Eşleşme Skoru", f"%{latest['match_score']}")
                        
                        st.markdown("### İndikatör Değerleri")
                        ind_df = pd.DataFrame({
                            'İndikatör': ['RSI', 'MFI', 'StochRSI', 'EMA Tangle', 'Hacim Çarpanı', 'Fiyat Pozisyonu'],
                            'Değer': [latest['rsi'], latest['mfi'], latest['stoch'], f"%{latest['ema_tangle']:.2f}", f"{latest['vol_ratio']:.2f}x", f"%{latest['price_pos']:.1f}"]
                        })
                        st.dataframe(ind_df, use_container_width=True)
                        
                        if len(signal_data['signals']) > 1:
                            st.markdown("### Son 10 Bardaki Tüm Sinyaller")
                            sig_df = pd.DataFrame(signal_data['signals'])
                            st.dataframe(sig_df, use_container_width=True)
            else:
                st.warning("️ Son 10 barda DNA'ya uyan sinyal bulunamadı.")
        else:
            st.error(" Master DNA oluşturulamadı. Lütfen tekrar deneyin.")

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'><p>Ultra Pro Dip DNA Analiz Sistemi v5.0 | Tüm BIST Hisseleri + Canlı Sinyal Tarama</p></div>", unsafe_allow_html=True)
