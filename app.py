from __future__ import annotations

from io import BytesIO
import re
import unicodedata
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ════════════════════════════════════════════════════════════════
# CONFIG & THEME
# ════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Dashboard Comercial 2025 × 2026",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

PRIMARY = "#4F46E5"      # Indigo
SECONDARY = "#06B6D4"    # Cyan
COLOR_2025 = "#6366F1"   # Indigo claro
COLOR_2026 = "#F59E0B"   # Âmbar
SUCCESS = "#10B981"
DANGER = "#EF4444"
BG_SOFT = "#F8FAFC"
TEXT_DARK = "#1E293B"
TEXT_MUTED = "#64748B"

COLOR_MAP = {2025: COLOR_2025, 2026: COLOR_2026}

PALETTE_QUALITATIVE = [
    "#4F46E5", "#06B6D4", "#F59E0B", "#10B981", "#EF4444",
    "#8B5CF6", "#EC4899", "#14B8A6", "#F97316", "#84CC16",
]

# ──────────────────────────── CSS ────────────────────────────

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

/* Fundo geral */
.main {{
    background: {BG_SOFT};
}}

/* Esconde o padding default excessivo */
.block-container {{
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}}

/* ───── Header hero ───── */
.hero-header {{
    background: linear-gradient(120deg, {PRIMARY} 0%, #7C3AED 50%, {SECONDARY} 100%);
    border-radius: 20px;
    padding: 32px 40px;
    margin-bottom: 28px;
    box-shadow: 0 10px 30px rgba(79, 70, 229, 0.25);
    position: relative;
    overflow: hidden;
}}
.hero-header::before {{
    content: "";
    position: absolute;
    top: -50%; right: -10%;
    width: 300px; height: 300px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
}}
.hero-title {{
    color: white;
    font-size: 2rem;
    font-weight: 800;
    margin: 0;
    position: relative;
    z-index: 1;
}}
.hero-subtitle {{
    color: rgba(255,255,255,0.85);
    font-size: 0.95rem;
    margin-top: 6px;
    position: relative;
    z-index: 1;
}}

/* ───── KPI Cards ───── */
.kpi-card {{
    background: white;
    border-radius: 16px;
    padding: 20px 22px;
    box-shadow: 0 2px 12px rgba(30, 41, 59, 0.06);
    border: 1px solid #EEF2F7;
    height: 100%;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    position: relative;
    overflow: hidden;
}}
.kpi-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(30, 41, 59, 0.12);
}}
.kpi-icon {{
    font-size: 1.5rem;
    margin-bottom: 6px;
    display: inline-block;
}}
.kpi-label {{
    font-size: 0.78rem;
    color: {TEXT_MUTED};
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 4px;
}}
.kpi-value {{
    font-size: 1.55rem;
    font-weight: 800;
    color: {TEXT_DARK};
    line-height: 1.2;
}}
.kpi-delta {{
    font-size: 0.82rem;
    font-weight: 600;
    margin-top: 6px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 2px 8px;
    border-radius: 20px;
}}
.kpi-delta.positive {{ color: {SUCCESS}; background: #ECFDF5; }}
.kpi-delta.negative {{ color: {DANGER}; background: #FEF2F2; }}
.kpi-delta.neutral {{ color: {TEXT_MUTED}; background: #F1F5F9; }}
.kpi-bar {{
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
}}

/* ───── Section titles ───── */
.section-title {{
    font-size: 1.15rem;
    font-weight: 700;
    color: #FFFFFF;
    margin: 8px 0 14px 0;
    padding-left: 12px;
    border-left: 4px solid {PRIMARY};
    display: flex;
    align-items: center;
    gap: 8px;
}}

/* ───── Sidebar ───── */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #1E1B4B 0%, #312E81 100%);
}}
section[data-testid="stSidebar"] * {{
    color: #E2E8F0 !important;
}}
section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] {{
    background: rgba(255,255,255,0.08);
    border-radius: 8px;
}}
section[data-testid="stSidebar"] hr {{
    border-color: rgba(255,255,255,0.15);
}}

/* ───── Tabs ───── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 6px;
    background: white;
    padding: 6px;
    border-radius: 14px;
    box-shadow: 0 2px 8px rgba(30,41,59,0.05);
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: 600;
    color: {TEXT_MUTED};
}}
.stTabs [aria-selected="true"] {{
    background: linear-gradient(120deg, {PRIMARY}, #7C3AED) !important;
    color: white !important;
}}

/* ───── DataFrame ───── */
div[data-testid="stDataFrame"] {{
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(30,41,59,0.05);
}}

/* Cards container (chart wrapper) */
.chart-card {{
    background: white;
    border-radius: 16px;
    padding: 18px 20px 6px 20px;
    box-shadow: 0 2px 12px rgba(30, 41, 59, 0.06);
    border: 1px solid #EEF2F7;
    margin-bottom: 18px;
}}

.insight-box {{
    background: linear-gradient(135deg, #EEF2FF 0%, #F0FDFA 100%);
    border-radius: 14px;
    padding: 16px 20px;
    border-left: 4px solid {PRIMARY};
    margin-bottom: 10px;
}}
.insight-box b {{ color: {PRIMARY}; }}
</style>
""", unsafe_allow_html=True)

PLOTLY_TEMPLATE = go.layout.Template(
    layout=dict(
        font=dict(family="Inter, sans-serif", color=TEXT_DARK, size=12.5),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        colorway=PALETTE_QUALITATIVE,
        xaxis=dict(gridcolor="#F1F5F9", zerolinecolor="#E2E8F0"),
        yaxis=dict(gridcolor="#F1F5F9", zerolinecolor="#E2E8F0"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=50, b=40, l=20, r=20),
    )
)

MONTHS = {
    "JANEIRO": 1, "FEVEREIRO": 2, "MARÇO": 3, "MARCO": 3, "ABRIL": 4,
    "MAIO": 5, "JUNHO": 6, "JULHO": 7, "AGOSTO": 8, "SETEMBRO": 9,
    "OUTUBRO": 10, "NOVEMBRO": 11, "DEZEMBRO": 12,
}
MONTH_NAMES = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
]


# ════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════

def norm_text(value) -> str:
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def parse_brl(value):
    """Converte strings monetárias brasileiras / números para float."""
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip().replace("R$", "").replace("\xa0", "").replace(" ", "")
    if not s or s in {"-", "—", "–"}:
        return None
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def parse_month(value):
    """Converte texto do mês (ou número) para número 1-12."""
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)) and not pd.isna(value):
        n = int(value)
        return n if 1 <= n <= 12 else None
    s = strip_accents(norm_text(value)).upper()
    if s.isdigit():
        n = int(s)
        return n if 1 <= n <= 12 else None
    return MONTHS.get(s) or MONTHS.get(s.replace("CO", "ÇO"))


def brl(value: float) -> str:
    if pd.isna(value) or value is None:
        return "R$ 0,00"
    return ("R$ " + f"{value:,.2f}").replace(",", "X").replace(".", ",").replace("X", ".")


def brl_compact(value: float) -> str:
    if pd.isna(value) or value is None:
        return "R$ 0"
    abs_v = abs(value)
    sign = "-" if value < 0 else ""
    if abs_v >= 1_000_000:
        return f"{sign}R$ {abs_v / 1_000_000:,.2f}M".replace(",", "X").replace(".", ",").replace("X", ".")
    if abs_v >= 1_000:
        return f"{sign}R$ {abs_v / 1_000:,.1f}K".replace(",", "X").replace(".", ",").replace("X", ".")
    return brl(value)


def kpi_card(col, icon, label, value, delta_text=None, delta_type="neutral", bar_color=PRIMARY):
    delta_html = ""
    if delta_text:
        arrow = "▲" if delta_type == "positive" else ("▼" if delta_type == "negative" else "•")
        delta_html = f'<div class="kpi-delta {delta_type}">{arrow} {delta_text}</div>'
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-bar" style="background:{bar_color};"></div>
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def section_title(text, icon=""):
    st.markdown(f'<div class="section-title">{icon} {text}</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# PARSER DE DADOS (estrutura tabular simples: Ano | Fabricante | Produto | Mês | Valor)
# ════════════════════════════════════════════════════════════════

COLUMN_ALIASES = {
    "Ano": ["ano", "year"],
    "Fabricante": ["fabricante", "marca", "fornecedor"],
    "Produto": ["produto", "linha", "categoria", "item", "sku", "descricao", "descrição"],
    "Mês": ["mes", "mês", "month", "periodo", "período"],
    "Faturamento": ["faturamento", "valor", "vendas", "total", "receita", "r$"],
}


def match_column(columns: list[str], aliases: list[str]) -> str | None:
    norm_cols = {strip_accents(str(c)).strip().lower(): c for c in columns}
    for alias in aliases:
        for norm_c, original in norm_cols.items():
            if alias in norm_c:
                return original
    return None


@st.cache_data(show_spinner="📥 Lendo planilha…")
def load_excel(file_bytes: bytes, file_name: str) -> pd.DataFrame:
    xls = pd.ExcelFile(BytesIO(file_bytes))

    # ── Localizar a aba "TABELA" (case/acento-insensitive) ──
    target_sheet = None
    for sheet in xls.sheet_names:
        if strip_accents(sheet).strip().upper() == "TABELA":
            target_sheet = sheet
            break

    # Se não achou "TABELA" exata, tenta achar algo que contenha "TABELA"
    if target_sheet is None:
        for sheet in xls.sheet_names:
            if "TABELA" in strip_accents(sheet).strip().upper():
                target_sheet = sheet
                break

    # Define quais abas serão processadas
    sheets_to_read = [target_sheet] if target_sheet else xls.sheet_names

    frames = []
    sheets_used = []
    coverage_values = []

    for sheet in sheets_to_read:
        df_raw = pd.read_excel(xls, sheet_name=sheet)
        if df_raw.empty:
            continue
        df_raw.columns = [norm_text(c) for c in df_raw.columns]
        cols = list(df_raw.columns)
        col_cobertura = match_column(cols, ["cobertura"])

        if col_cobertura is not None:
            valores_cobertura = (
                df_raw[col_cobertura]
                .map(parse_brl)
                .dropna()
            )
            
            coverage_values.extend(valores_cobertura.tolist())

        col_map = {}
        for target, aliases in COLUMN_ALIASES.items():
            found = match_column(cols, aliases)
            if found:
                col_map[target] = found

        # Fallback por posição (A=Ano, B=Fabricante, C=Produto, D=Mês, E=Faturamento)
        if len(col_map) < 4 and len(cols) >= 5:
            fallback_order = ["Ano", "Fabricante", "Produto", "Mês", "Faturamento"]
            for i, t in enumerate(fallback_order):
                if t not in col_map:
                    col_map[t] = cols[i]

        required = {"Ano", "Fabricante", "Mês", "Faturamento"}
        if not required.issubset(col_map.keys()):
            continue

        tmp = pd.DataFrame()
        tmp["Ano"] = pd.to_numeric(df_raw[col_map["Ano"]], errors="coerce")
        tmp["Fabricante"] = df_raw[col_map["Fabricante"]].map(norm_text)
        tmp["Produto"] = (
            df_raw[col_map["Produto"]].map(norm_text) if "Produto" in col_map else sheet
        )
        tmp["Mês_num"] = df_raw[col_map["Mês"]].map(parse_month)
        tmp["Faturamento"] = df_raw[col_map["Faturamento"]].map(parse_brl)

        # Preserva a cobertura na mesma linha dos dados comerciais
        if col_cobertura is not None:
            tmp["COBERTURA"] = (
                df_raw[col_cobertura]
                .map(parse_brl)
                .pipe(pd.to_numeric, errors="coerce")
                .round()
                .astype("Int64")
            )
        else:
            tmp["COBERTURA"] = pd.Series(
                pd.NA, index=tmp.index, dtype="Int64"
            )

        tmp["Origem"] = sheet

        frames.append(tmp)

        sheets_used.append(sheet)

    if not frames:
        raise ValueError(
            "Não encontrei colunas reconhecíveis (Ano, Fabricante, Produto, Mês, Faturamento) "
            f"na(s) aba(s): {', '.join(sheets_to_read)}. Verifique os cabeçalhos."
        )

    df = pd.concat(frames, ignore_index=True)
    df = df.dropna(subset=["Ano", "Mês_num", "Faturamento"])
    df = df[df["Faturamento"] >= 0]
    df["Ano"] = df["Ano"].astype(int)
    df["Mês_num"] = df["Mês_num"].astype(int)
    df["Mês"] = df["Mês_num"].map(lambda n: MONTH_NAMES[n - 1])
    df["Fabricante"] = df["Fabricante"].replace("", "Não informado")
    df["Produto"] = df["Produto"].replace("", "Não informado")

    # Guarda metadado de quais abas foram usadas (para exibir na sidebar)
    df.attrs["sheets_used"] = sheets_used
    df.attrs["coverage_data"] = coverage_values
    return df.reset_index(drop=True)


# ════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 📊 Dashboard Comercial")
    st.caption("Análise estratégica 2025 × 2026")
    # st.divider()

    st.markdown("### 📂 Carregar dados")
    uploaded = st.file_uploader(
        "Arquivo Excel (.xlsx)",
        type=["xlsx", "xlsm", "xls"],
        help="Planilha com colunas: Ano, Fabricante, Produto, Mês, Faturamento.",
    )

    if uploaded is None:
        st.info("👆 Faça upload de um arquivo para começar.")
        st.stop()

    try:
        df = load_excel(uploaded.getvalue(), uploaded.name)
    except Exception as e:
        st.error(f"❌ Erro ao ler o arquivo: {e}")
        st.stop()

    st.success(f"✅ {len(df):,} registros carregados")
    sheets_used = df.attrs.get("sheets_used", [])
    if sheets_used:
        st.caption(f"📑 Aba(s) lida(s): **{', '.join(sheets_used)}**")

    #st.divider()

    st.markdown("### 🔍 Filtros")

    anos_disp = sorted(df["Ano"].unique().tolist())
    anos_sel = st.multiselect("Anos", anos_disp, default=anos_disp, format_func=lambda x: str(int(x)))

    fab_disp = sorted(df["Fabricante"].unique().tolist())
    with st.expander(f"🏭 Fabricantes ({len(fab_disp)})", expanded=False):
        fab_sel = st.multiselect("Selecionar", fab_disp, default=fab_disp, label_visibility="collapsed")

    prod_disp = sorted(df["Produto"].unique().tolist())
    with st.expander(f"📦 Produtos ({len(prod_disp)})", expanded=False):
        prod_sel = st.multiselect("Selecionar", prod_disp, default=prod_disp, label_visibility="collapsed")

    meses_sel = st.multiselect("📅 Meses", MONTH_NAMES, default=MONTH_NAMES)

    #st.divider()
    st.caption(f"🕒 Atualizado em {datetime.now():%d/%m/%Y %H:%M}")


# ════════════════════════════════════════════════════════════════
# FILTRAR DADOS
# ════════════════════════════════════════════════════════════════

mask = (
    df["Ano"].isin(anos_sel)
    & df["Fabricante"].isin(fab_sel)
    & df["Produto"].isin(prod_sel)
    & df["Mês"].isin(meses_sel)
)
fdf = df[mask].copy()

if fdf.empty:
    st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados. Ajuste a barra lateral.")
    st.stop()


# ════════════════════════════════════════════════════════════════
# HEADER
# ════════════════════════════════════════════════════════════════

st.markdown(f"""
<div class="hero-header">
    <div class="hero-title">📊 Dashboard Comercial 2025 × 2026</div>
    <div class="hero-subtitle">
        {len(fdf):,} registros · {fdf['Fabricante'].nunique()} fabricantes ·
        {fdf['Produto'].nunique()} produtos · Atualizado em {datetime.now():%d/%m/%Y}
    </div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# KPIs
# ════════════════════════════════════════════════════════════════

total_geral = fdf["Faturamento"].sum()
totais_ano = fdf.groupby("Ano")["Faturamento"].sum()
total_2025 = totais_ano.get(2025, 0.0)
total_2026 = totais_ano.get(2026, 0.0)

yoy_pct, yoy_delta = None, None
if total_2025 > 0 and total_2026 > 0:
    yoy_delta = total_2026 - total_2025
    yoy_pct = yoy_delta / total_2025 * 100

mensal_geral = fdf.groupby(["Ano", "Mês_num", "Mês"])["Faturamento"].sum().reset_index()
best_row = mensal_geral.loc[mensal_geral["Faturamento"].idxmax()] if not mensal_geral.empty else None

ticket_medio = total_geral / fdf["Fabricante"].nunique() if fdf["Fabricante"].nunique() else 0

c1, c2, c3, c4, c5 = st.columns(5)

kpi_card(c1, "💰", "Faturamento Total", brl_compact(total_geral), bar_color=PRIMARY)
kpi_card(c2, "📅", "Total 2025", brl_compact(total_2025), bar_color=COLOR_2025)
kpi_card(c3, "📅", "Total 2026", brl_compact(total_2026), bar_color=COLOR_2026)

if yoy_pct is not None:
    dtype = "positive" if yoy_pct >= 0 else "negative"
    kpi_card(c4, "📈", "Variação YoY", f"{yoy_pct:+.1f}%",
              delta_text=brl_compact(yoy_delta), delta_type=dtype,
              bar_color=SUCCESS if yoy_pct >= 0 else DANGER)
else:
    kpi_card(c4, "📈", "Variação YoY", "N/D", bar_color=TEXT_MUTED)

if best_row is not None:
    kpi_card(c5, "🏆", "Melhor Mês", f"{best_row['Mês']}/{int(best_row['Ano'])}",
              delta_text=brl_compact(best_row['Faturamento']), delta_type="neutral",
              bar_color=SECONDARY)


# ════════════════════════════════════════════════════════════════
# TABS
# ════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Visão Geral",
    "🏭 Fabricantes",
    "📦 Produtos",
    "⚖️ Comparativo",
    "📋 Dados",
    "🛡️ Cobertura"
])

# ──────────────────────── TAB 1: VISÃO GERAL ────────────────────────
with tab1:
    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        section_title("Evolução Mensal do Faturamento", "📈")
        mensal = (
            fdf.groupby(["Ano", "Mês_num", "Mês"])["Faturamento"].sum()
            .reset_index().sort_values(["Ano", "Mês_num"])
        )
        fig_trend = px.area(
            mensal, x="Mês", y="Faturamento", color="Ano",
            color_discrete_map=COLOR_MAP,
            category_orders={"Mês": MONTH_NAMES},
            markers=True,
            labels={"Faturamento": "Faturamento (R$)", "Mês": ""},
            template=PLOTLY_TEMPLATE,
        )
        fig_trend.update_traces(line=dict(width=3), opacity=0.15,
            hovertemplate="%{y:,.2f}<extra>%{fullData.name}</extra>")
        fig_trend.update_layout(hovermode="x unified", yaxis_tickformat=",.0f",
            legend=dict(orientation="h", y=1.1, x=1, xanchor="right"), height=400)
        st.plotly_chart(fig_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        section_title("Participação por Ano", "🥧")
        fig_pie_ano = px.pie(
            totais_ano.reset_index(), names="Ano", values="Faturamento", hole=0.55,
            color="Ano", color_discrete_map=COLOR_MAP, template=PLOTLY_TEMPLATE,
        )
        fig_pie_ano.update_traces(textinfo="percent+label", textfont_size=13)
        fig_pie_ano.update_layout(height=250, showlegend=False, margin=dict(t=10, b=10))
        st.plotly_chart(fig_pie_ano, use_container_width=True)

        st.markdown("<hr style='margin:6px 0;'>", unsafe_allow_html=True)
        section_title("Top Fabricante", "🏅")
        top5 = fdf.groupby("Fabricante")["Faturamento"].sum().nlargest(5).reset_index()
        fig_top5 = px.bar(
            top5.sort_values("Faturamento"), x="Faturamento", y="Fabricante", orientation="h",
            text_auto=".2s", template=PLOTLY_TEMPLATE,
            color_discrete_sequence=[PRIMARY],
        )
        fig_top5.update_layout(height=220, margin=dict(t=10, b=10, l=10),
                                 xaxis_tickformat=",.0f", yaxis_title="", xaxis_title="")
        fig_top5.update_traces(hovertemplate="%{x:,.2f}<extra></extra>")
        st.plotly_chart(fig_top5, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Heatmap
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    section_title("Mapa de Calor — Faturamento por Mês e Ano", "🗓️")
    heat = fdf.groupby(["Ano", "Mês_num", "Mês"])["Faturamento"].sum().reset_index()
    fig_heat = px.density_heatmap(
        heat, x="Mês", y="Ano", z="Faturamento",
        category_orders={"Mês": MONTH_NAMES},
        color_continuous_scale=["#EEF2FF", PRIMARY, "#1E1B4B"],
        text_auto=".2s", template=PLOTLY_TEMPLATE,
    )
    fig_heat.update_layout(height=220, yaxis=dict(tickformat="d", dtick=1), margin=dict(t=10, b=10))
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────── TAB 2: FABRICANTES ────────────────────────
with tab2:
    fab_agg = fdf.groupby(["Fabricante", "Ano"])["Faturamento"].sum().reset_index()
    TOP_N = st.slider("Número de fabricantes exibidos (ranking)", 5, min(30, fdf["Fabricante"].nunique()), 15)
    top_fabs = fab_agg.groupby("Fabricante")["Faturamento"].sum().nlargest(TOP_N).index.tolist()
    fab_plot = fab_agg[fab_agg["Fabricante"].isin(top_fabs)]

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    section_title(f"Ranking de Fabricantes", "🏭")
    fig_fab = px.bar(
        fab_plot, x="Faturamento", y="Fabricante", color="Ano", barmode="group",
        orientation="h", color_discrete_map=COLOR_MAP,
        category_orders={"Fabricante": top_fabs[::-1]},
        labels={"Faturamento": "Faturamento (R$)", "Fabricante": ""},
        template=PLOTLY_TEMPLATE,
    )
    fig_fab.update_layout(height=max(400, TOP_N * 32), xaxis_tickformat=",.0f",
                            legend=dict(orientation="h", y=1.05, x=1, xanchor="right"))
    fig_fab.update_traces(hovertemplate="%{x:,.2f}<extra>%{fullData.name}</extra>")
    st.plotly_chart(fig_fab, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────── TAB 3: PRODUTOS ────────────────────────
with tab3:
    col_t, col_d = st.columns(2)

    prod_total = fdf.groupby("Produto")["Faturamento"].sum().reset_index().sort_values("Faturamento", ascending=False)

    with col_t:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        section_title("Treemap Geral de Produtos", "🌳")
        fig_tree = px.treemap(
            prod_total, path=["Produto"], values="Faturamento",
            color="Faturamento", color_continuous_scale=["#E0E7FF", PRIMARY, "#1E1B4B"],
            template=PLOTLY_TEMPLATE,
        )
        fig_tree.update_traces(hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<extra></extra>")
        fig_tree.update_layout(height=420, margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_tree, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_d:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        section_title("Participação por Ano", "🥯")
        ano_sel_donut = st.selectbox(
            "Ano de referência", sorted(fdf["Ano"].unique().tolist()),
            format_func=lambda x: str(int(x)),
        )
        prod_agg = fdf.groupby(["Produto", "Ano"])["Faturamento"].sum().reset_index()
        donut_data = prod_agg[prod_agg["Ano"] == ano_sel_donut]
        # Agrupa cauda longa em "Outros"
        donut_sorted = donut_data.sort_values("Faturamento", ascending=False)
        if len(donut_sorted) > 10:
            top10 = donut_sorted.head(10)
            outros_val = donut_sorted.iloc[10:]["Faturamento"].sum()
            donut_final = pd.concat([top10, pd.DataFrame([{"Produto": "Outros", "Faturamento": outros_val}])])
        else:
            donut_final = donut_sorted
        fig_donut = px.pie(
            donut_final, names="Produto", values="Faturamento", hole=0.5,
            color_discrete_sequence=PALETTE_QUALITATIVE, template=PLOTLY_TEMPLATE,
        )
        fig_donut.update_traces(textposition="inside", textinfo="percent",
                                  hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f} (%{percent})<extra></extra>")
        fig_donut.update_layout(height=420, legend=dict(orientation="v", font=dict(size=10)))
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    section_title("Top 15 Produtos por Faturamento", "📦")
    top_prods = prod_total.head(15)
    fig_prod_bar = px.bar(
        top_prods.sort_values("Faturamento"), x="Faturamento", y="Produto", orientation="h",
        color="Faturamento", color_continuous_scale=["#E0E7FF", PRIMARY],
        template=PLOTLY_TEMPLATE,
    )
    fig_prod_bar.update_layout(height=450, xaxis_tickformat=",.0f", coloraxis_showscale=False)
    st.plotly_chart(fig_prod_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────── TAB 4: COMPARATIVO YOY ────────────────────────
with tab4:
    if 2025 in anos_sel and 2026 in anos_sel:
        pivot_yoy = (
            fdf[fdf["Ano"].isin([2025, 2026])]
            .groupby(["Mês_num", "Mês", "Ano"])["Faturamento"].sum()
            .reset_index()
            .pivot_table(index=["Mês_num", "Mês"], columns="Ano", values="Faturamento", fill_value=0)
            .reset_index().sort_values("Mês_num")
        )
        if 2025 in pivot_yoy.columns and 2026 in pivot_yoy.columns:
            pivot_yoy["Delta"] = pivot_yoy[2026] - pivot_yoy[2025]
            pivot_yoy["Delta_%"] = np.where(
                pivot_yoy[2025] > 0, pivot_yoy["Delta"] / pivot_yoy[2025] * 100, np.nan
            )
            pivot_yoy["Cor"] = np.where(pivot_yoy["Delta"] >= 0, SUCCESS, DANGER)

            # Insight automático
            meses_cresceram = (pivot_yoy["Delta"] > 0).sum()
            meses_total = len(pivot_yoy)
            melhor_mes_delta = pivot_yoy.loc[pivot_yoy["Delta"].idxmax()]
            pior_mes_delta = pivot_yoy.loc[pivot_yoy["Delta"].idxmin()]

            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            section_title("Lado a Lado: 2025 vs 2026", "⚖️")
            fig_side = go.Figure()
            fig_side.add_bar(x=pivot_yoy["Mês"], y=pivot_yoy[2025], name="2025", marker_color=COLOR_2025)
            fig_side.add_bar(x=pivot_yoy["Mês"], y=pivot_yoy[2026], name="2026", marker_color=COLOR_2026)
            fig_side.update_layout(template=PLOTLY_TEMPLATE, barmode="group", height=380,
                                     yaxis_tickformat=",.0f",
                                     legend=dict(orientation="h", y=1.08, x=1, xanchor="right"))
            st.plotly_chart(fig_side, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("ℹ️ Selecione os anos **2025 e 2026** simultaneamente na barra lateral para ver o comparativo.")

# ──────────────────────── TAB 5: DADOS ────────────────────────
with tab5:
    section_title("Dados Brutos Filtrados", "🔎")
    st.caption(f"{len(fdf):,} linhas")

    meses = {
        "Janeiro": 1,
        "Fevereiro": 2,
        "Março": 3,
        "Abril": 4,
        "Maio": 5,
        "Junho": 6,
        "Julho": 7,
        "Agosto": 8,
        "Setembro": 9,
        "Outubro": 10,
        "Novembro": 11,
        "Dezembro": 12,
    }

    fdf["Mês_num"] = fdf["Mês"].map(meses)

    display_cols = ["Ano", "Produto", "Fabricante", "Mês", "Faturamento", "Origem"]

    display_df = (
        fdf.sort_values(["Ano", "Mês_num", "Produto"])[display_cols]
        .copy()
    )

    display_df["Faturamento"] = display_df["Faturamento"].map(brl)

    st.dataframe(display_df, use_container_width=True, height=400, hide_index=True)

    colx, coly = st.columns(2)
    csv_bytes = fdf[display_cols].to_csv(index=False).encode("utf-8-sig")
    colx.download_button(
        "⬇️ Baixar CSV filtrado", data=csv_bytes,
        file_name=f"comercial_filtrado_{datetime.now():%Y%m%d_%H%M}.csv",
        mime="text/csv", use_container_width=True,
    )

    xlsx_buf = BytesIO()
    with pd.ExcelWriter(xlsx_buf, engine="openpyxl") as writer:
        fdf[display_cols].to_excel(writer, index=False, sheet_name="Dados")
    coly.download_button(
        "⬇️ Baixar Excel filtrado", data=xlsx_buf.getvalue(),
        file_name=f"comercial_filtrado_{datetime.now():%Y%m%d_%H%M}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)



# ──────────────────────── TAB 6: COBERTURA ────────────────────────
with tab6:
    st.subheader("🛡️ Comparativo de Cobertura — 2025 × 2026")

    cobertura_df = fdf.dropna(subset=["COBERTURA"]).copy()

    if cobertura_df.empty:
        st.warning("Não há dados de cobertura para os filtros selecionados.")

    elif not {2025, 2026}.issubset(set(cobertura_df["Ano"].unique())):
        st.info(
            "Selecione 2025 e 2026 simultaneamente na barra lateral "
            "para comparar a cobertura entre os anos."
        )

    else:
        # Calcula a cobertura média por mês e ano
        cobertura_mensal = (
            cobertura_df[
                cobertura_df["Ano"].isin([2025, 2026])
            ]
            .groupby(["Mês_num", "Mês", "Ano"], as_index=False)
            ["COBERTURA"]
            .max()
        )

        # Organiza os meses e mantém uma coluna para cada ano
        cobertura_pivot = (
            cobertura_mensal
            .pivot_table(
                index=["Mês_num", "Mês"],
                columns="Ano",
                values="COBERTURA",
                aggfunc="mean",
            )
            .reset_index()
            .sort_values("Mês_num")
        )
        # Garante que os valores de cobertura sejam inteiros
        for ano in [2025, 2026]:
            if ano in cobertura_pivot.columns:
                cobertura_pivot[ano] = (
                    pd.to_numeric(cobertura_pivot[ano], errors="coerce")
                    .round()
                    .astype("Int64")
                )

        # KPIs
        c1, c2, c3 = st.columns(3)

        media_2025 = cobertura_df.loc[
            cobertura_df["Ano"] == 2025, "COBERTURA"
        ].mean()

        media_2026 = cobertura_df.loc[
            cobertura_df["Ano"] == 2026, "COBERTURA"
        ].mean()

        diferenca = media_2026 - media_2025

        c1.metric("Cobertura média — 2025", f"{media_2025:,.1f}")
        c2.metric("Cobertura média — 2026", f"{media_2026:,.1f}")
        c3.metric(
            "Variação média",
            f"{diferenca:+,.1f}",
            delta=f"{diferenca / media_2025 * 100:+.1f}%"
            if media_2025 else None,
        )

        # Gráfico de barras agrupadas, semelhante à aba Comparativo
        fig_cobertura = go.Figure()

        if 2025 in cobertura_pivot.columns:
            fig_cobertura.add_bar(
                x=cobertura_pivot["Mês"],
                y=cobertura_pivot[2025],
                name="2025",
                marker_color=COLOR_2025,
                text=cobertura_pivot[2025],
                texttemplate="%{y:.0f}",
                textposition="outside",
            )

        if 2026 in cobertura_pivot.columns:
            fig_cobertura.add_bar(
                x=cobertura_pivot["Mês"],
                y=cobertura_pivot[2026],
                name="2026",
                marker_color=COLOR_2026,
                text=cobertura_pivot[2026],
                texttemplate="%{y:.0f}",
                textposition="outside",
            )


            fig_cobertura.update_layout(
                template=PLOTLY_TEMPLATE,
                barmode="group",
                title="Cobertura mensal — 2025 × 2026",
                xaxis_title="Mês",
                yaxis_title="Cobertura",
                xaxis=dict(
                    categoryorder="array",
                    categoryarray=MONTH_NAMES,
                ),
                legend=dict(
                    orientation="h",
                    y=1.12,
                    x=1,
                    xanchor="right",
                ),
                height=430,
            )


        st.plotly_chart(fig_cobertura, use_container_width=True)

        # Tabela comparativa
        st.subheader("Tabela comparativa por mês")

        colunas_tabela = ["Mês_num", "Mês"]

        if 2025 in cobertura_pivot.columns:
            colunas_tabela.append(2025)

        if 2026 in cobertura_pivot.columns:
            colunas_tabela.append(2026)

        tabela_cobertura = cobertura_pivot[colunas_tabela].copy()

        tabela_cobertura = tabela_cobertura.rename(
            columns={
                "Mês": "Mês",
                2025: "Cobertura 2025",
                2026: "Cobertura 2026",
            }
        )

        tabela_cobertura = tabela_cobertura.drop(columns=["Mês_num"])

        for coluna in ["Cobertura 2025", "Cobertura 2026"]:
            if coluna in tabela_cobertura.columns:
                tabela_cobertura[coluna] = (
                    pd.to_numeric(tabela_cobertura[coluna], errors="coerce")
                    .round()
                    .astype("Int64")
                )

        st.dataframe(
            tabela_cobertura,
            use_container_width=True,
            hide_index=True,
        )


# ════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════

st.markdown(f"""
<div style="text-align:center; color:{TEXT_MUTED}; padding: 20px 0; font-size:0.85rem;">
    Dashboard Comercial 2025 × 2026 · Gerado em {datetime.now():%d/%m/%Y às %H:%M:%S}<br>
    Desenvolvido com Streamlit + Plotly
</div>
""", unsafe_allow_html=True)