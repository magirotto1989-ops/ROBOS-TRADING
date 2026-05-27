from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import date

OUTPUT = "/home/user/ROBOS-TRADING/Relatorio_XP_Banco_Master.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm
)

W, H = A4

# ── Paleta ──────────────────────────────────────────────────────────────
AZUL_ESCURO  = colors.HexColor("#0D2137")
AZUL_MEDIO   = colors.HexColor("#1A4B8C")
AZUL_CLARO   = colors.HexColor("#2E86C1")
VERMELHO     = colors.HexColor("#C0392B")
LARANJA      = colors.HexColor("#E67E22")
AMARELO      = colors.HexColor("#F1C40F")
VERDE        = colors.HexColor("#1E8449")
CINZA_CLARO  = colors.HexColor("#F2F3F4")
CINZA_MEDIO  = colors.HexColor("#BDC3C7")
BRANCO       = colors.white
PRETO        = colors.black

styles = getSampleStyleSheet()

def style(name, **kw):
    s = ParagraphStyle(name, **kw)
    return s

titulo_doc = style("TituloDoc",
    fontSize=22, leading=28, textColor=BRANCO,
    fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4)

subtitulo_doc = style("SubtituloDoc",
    fontSize=13, leading=18, textColor=AZUL_CLARO,
    fontName="Helvetica", alignment=TA_CENTER, spaceAfter=2)

data_style = style("DataStyle",
    fontSize=9, leading=12, textColor=CINZA_MEDIO,
    fontName="Helvetica", alignment=TA_CENTER)

sec_header = style("SecHeader",
    fontSize=13, leading=17, textColor=BRANCO,
    fontName="Helvetica-Bold", alignment=TA_LEFT,
    spaceBefore=14, spaceAfter=6,
    leftIndent=8, rightIndent=8,
    borderPadding=(5, 8, 5, 8))

body = style("Body",
    fontSize=10, leading=15, textColor=PRETO,
    fontName="Helvetica", alignment=TA_JUSTIFY,
    spaceBefore=3, spaceAfter=3)

bullet_style = style("Bullet",
    fontSize=10, leading=15, textColor=PRETO,
    fontName="Helvetica", alignment=TA_LEFT,
    leftIndent=14, firstLineIndent=-10,
    spaceBefore=2, spaceAfter=2)

bold_body = style("BoldBody",
    fontSize=10, leading=15, textColor=AZUL_ESCURO,
    fontName="Helvetica-Bold", alignment=TA_LEFT,
    spaceBefore=4, spaceAfter=2)

nota_style = style("Nota",
    fontSize=8.5, leading=13, textColor=colors.HexColor("#555555"),
    fontName="Helvetica-Oblique", alignment=TA_JUSTIFY,
    leftIndent=10, rightIndent=10, spaceBefore=4, spaceAfter=4)

verdict_style = style("Verdict",
    fontSize=12, leading=17, textColor=BRANCO,
    fontName="Helvetica-Bold", alignment=TA_CENTER,
    spaceBefore=6, spaceAfter=6)

def header_block(texto, cor=AZUL_MEDIO):
    tbl = Table([[Paragraph(texto, sec_header)]], colWidths=[doc.width])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), cor),
        ("ROUNDEDCORNERS", [4]),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ]))
    return tbl

def bullet(texto, icon="▸"):
    return Paragraph(f"{icon} {texto}", bullet_style)

def divider(cor=AZUL_CLARO):
    return HRFlowable(width="100%", thickness=1, color=cor, spaceAfter=6, spaceBefore=6)

# ── Conteúdo ─────────────────────────────────────────────────────────────
story = []

# ── Capa ─────────────────────────────────────────────────────────────────
capa = Table(
    [[Paragraph("RELATÓRIO DE ANÁLISE DE RISCO", titulo_doc)],
     [Paragraph("XP Investimentos × Banco Master", subtitulo_doc)],
     [Spacer(1, 0.3*cm)],
     [Paragraph("Tópicos Críticos &amp; Avaliação de Segurança para Investidores", subtitulo_doc)],
     [Spacer(1, 0.5*cm)],
     [Paragraph(f"Data: {date.today().strftime('%d/%m/%Y')}  |  Uso Exclusivo Interno", data_style)]],
    colWidths=[doc.width]
)
capa.setStyle(TableStyle([
    ("BACKGROUND",     (0,0), (-1,-1), AZUL_ESCURO),
    ("ROUNDEDCORNERS", [8]),
    ("TOPPADDING",     (0,0), (-1,-1), 22),
    ("BOTTOMPADDING",  (0,0), (-1,-1), 22),
    ("LEFTPADDING",    (0,0), (-1,-1), 16),
    ("RIGHTPADDING",   (0,0), (-1,-1), 16),
]))
story += [capa, Spacer(1, 0.7*cm)]

# ── 1. Contexto ────────────────────────────────────────────────────────
story += [
    header_block("1. CONTEXTO — O QUE ACONTECEU?"),
    Spacer(1, 0.2*cm),
    Paragraph(
        "O vídeo <b>\"As Íntimas Relações da XP Investimentos com o Banco Master\"</b> expõe uma série de "
        "vínculos entre a maior corretora do Brasil e o Banco Master, que entrou em liquidação extrajudicial "
        "decretada pelo Banco Central em <b>novembro de 2025</b>. A análise a seguir sintetiza os fatos "
        "apurados e avalia os riscos para investidores que ainda mantêm ativos na plataforma XP.", body),
    Spacer(1, 0.3*cm),
]

# ── 2. Tópicos Críticos ──────────────────────────────────────────────
story += [
    header_block("2. TÓPICOS CRÍTICOS IDENTIFICADOS", VERMELHO),
    Spacer(1, 0.2*cm),
]

topicos = [
    ("TC-01", "Conflito de Interesse Societário",
     "A XP foi sócia do Will Bank, banco digital do mesmo grupo controlado por Daniel Vorcaro (grupo Master). "
     "Ao sair da sociedade, recebeu como pagamento <b>CDBs emitidos pelo próprio Banco Master</b> — ativos que "
     "depois distribuiu em larga escala para seus clientes. Esse duplo papel (ex-sócia e distribuidora) configura "
     "um grave conflito de interesse não divulgado ao investidor de varejo.", VERMELHO),
    ("TC-02", "Volume Bilionário de CDBs Distribuídos",
     "A XP liderou a distribuição de CDBs do Banco Master com <b>R$ 26 bilhões</b> — 64% do total de "
     "R$ 40,6 bilhões distribuídos no mercado. Esse volume impulsionou artificialmente a carteira de "
     "empréstimos do Master em <b>86% ao ano</b>, crescimento insustentável que sinalizava risco elevado.", LARANJA),
    ("TC-03", "Uso Enganoso do FGC como Argumento de Venda",
     "A principal tese comercial usada pela XP para vender os CDBs era a <b>cobertura do FGC (Fundo "
     "Garantidor de Créditos)</b>. Porém, o FGC cobre apenas R$ 250 mil por CPF por instituição, e muitos "
     "investidores possuíam valores acima desse limite. A ação judicial aponta que o risco real do emissor "
     "foi sistematicamente omitido.", LARANJA),
    ("TC-04", "Manutenção da Oferta até Véspera do Colapso",
     "Apesar de sinais crescentes de fragilidade financeira do Banco Master, a XP manteve a oferta ativa "
     "de CDBs até <b>pouco antes da liquidação</b> em novembro de 2025. Isso sugere que ou a plataforma "
     "desconsiderou os alertas, ou priorizou receita de distribuição em detrimento dos clientes.", VERMELHO),
    ("TC-05", "Ação Civil Pública em Andamento",
     "A <b>6ª Vara Empresarial do Rio de Janeiro</b> encaminhou ao Ministério Público uma Ação Civil "
     "Pública contra XP, BTG Pactual e Nubank por omissão de riscos e uso do FGC como garantia enganosa. "
     "O trio responde por R$ 35,6 bilhões dos R$ 40,6 bilhões distribuídos.", VERMELHO),
    ("TC-06", "Vínculos Extracurriculares (F1)",
     "XP e Banco Master co-investiram aproximadamente <b>R$ 26 milhões</b> na carreira do piloto Felipe "
     "Drugovich na Fórmula 1, revelando um relacionamento institucional próximo além do mercado financeiro, "
     "o que reforça a tese de parceria estrutural e não apenas comercial.", AMARELO),
]

for cod, titulo, descricao, cor in topicos:
    badge = Table([[Paragraph(f"<b>{cod}</b>", style("Badge",
        fontSize=9, fontName="Helvetica-Bold", textColor=BRANCO, alignment=TA_CENTER))]],
        colWidths=[1.4*cm])
    badge.setStyle(TableStyle([
        ("BACKGROUND",     (0,0), (-1,-1), cor),
        ("ROUNDEDCORNERS", [4]),
        ("TOPPADDING",     (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",  (0,0), (-1,-1), 4),
    ]))
    titulo_p = Paragraph(f"<b>{titulo}</b>", bold_body)
    desc_p   = Paragraph(descricao, body)
    inner = Table([[badge, Table([[titulo_p],[desc_p]], colWidths=[doc.width - 1.8*cm])]],
                  colWidths=[1.6*cm, doc.width - 1.6*cm])
    inner.setStyle(TableStyle([
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
    ]))
    outer = Table([[inner]], colWidths=[doc.width])
    outer.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), CINZA_CLARO),
        ("ROUNDEDCORNERS",[5]),
        ("BOX",           (0,0), (-1,-1), 1, cor),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
    ]))
    story += [KeepTogether([outer, Spacer(1, 0.25*cm)])]

# ── 3. Matriz de Risco ─────────────────────────────────────────────────
story += [
    Spacer(1, 0.2*cm),
    header_block("3. MATRIZ DE RISCO — XP INVESTIMENTOS", AZUL_ESCURO),
    Spacer(1, 0.3*cm),
]

matriz_data = [
    ["Dimensão de Risco", "Nível", "Justificativa"],
    ["Risco Reputacional",    "ALTO",   "Ação judicial pública; ampla cobertura midiática negativa"],
    ["Risco Regulatório",     "ALTO",   "Investigação em andamento pelo MP e possível ação do BC/CVM"],
    ["Risco Legal",           "MÉDIO-ALTO", "Exposição a indenizações; desfecho incerto"],
    ["Risco Operacional",     "BAIXO",  "Plataforma estável; sem risco de insolvência imediata"],
    ["Risco de Solvência",    "BAIXO",  "XP Inc. é empresa listada (NASDAQ) com capital sólido"],
    ["Risco de Conflito",     "ALTO",   "Modelo de negócio com incentivos desalinhados ao cliente"],
    ["Risco para Investidor", "MÉDIO",  "Ativos custodiados são separados do patrimônio da corretora"],
]

cor_nivel = {
    "ALTO":       VERMELHO,
    "MÉDIO-ALTO": LARANJA,
    "MÉDIO":      AMARELO,
    "BAIXO":      VERDE,
}

m_style = [
    ("BACKGROUND",    (0,0), (-1,0), AZUL_ESCURO),
    ("TEXTCOLOR",     (0,0), (-1,0), BRANCO),
    ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",      (0,0), (-1,-1), 9),
    ("ALIGN",         (0,0), (-1,-1), "LEFT"),
    ("ALIGN",         (1,0), (1,-1), "CENTER"),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("ROWBACKGROUNDS",(0,1), (-1,-1), [CINZA_CLARO, BRANCO]),
    ("GRID",          (0,0), (-1,-1), 0.4, CINZA_MEDIO),
    ("TOPPADDING",    (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
]

for i, row in enumerate(matriz_data[1:], 1):
    nivel = row[1]
    cor   = cor_nivel.get(nivel, CINZA_MEDIO)
    m_style += [
        ("BACKGROUND", (1, i), (1, i), cor),
        ("TEXTCOLOR",  (1, i), (1, i), BRANCO),
        ("FONTNAME",   (1, i), (1, i), "Helvetica-Bold"),
    ]

matriz_tbl = Table(
    [[Paragraph(c, style(f"mh{j}",
        fontSize=9,
        fontName="Helvetica-Bold" if i==0 else "Helvetica",
        textColor=BRANCO if i==0 else PRETO,
        leading=13)) for j, c in enumerate(row)]
     for i, row in enumerate(matriz_data)],
    colWidths=[5.5*cm, 2.8*cm, doc.width - 8.3*cm]
)
matriz_tbl.setStyle(TableStyle(m_style))
story += [matriz_tbl, Spacer(1, 0.4*cm)]

# ── 4. Análise: É Seguro Manter Investimentos na XP? ──────────────────
story += [
    header_block("4. ANÁLISE: É SEGURO MANTER INVESTIMENTOS NA XP?", AZUL_MEDIO),
    Spacer(1, 0.3*cm),
]

story += [
    Paragraph("<b>4.1 O que está efetivamente em risco</b>", bold_body),
    bullet("Seus <b>ativos (ações, fundos, títulos)</b> são custodiados pela B3 ou pelo emissor, "
           "<b>não pelo patrimônio da XP</b>. Uma eventual falência da corretora não implica perda desses ativos.", "✔"),
    bullet("CDBs do Banco Master já comprados acima de R$ 250 mil por CPF <b>podem sofrer perda "
           "parcial</b>, pois excedem o limite do FGC.", "⚠"),
    bullet("Investimentos em outros produtos (Tesouro Direto, ações, fundos de terceiros) "
           "estão <b>protegidos por custódia independente</b>.", "✔"),
    Spacer(1, 0.2*cm),

    Paragraph("<b>4.2 Riscos Indiretos ao Permanecer na XP</b>", bold_body),
    bullet("Possível <b>deterioração do modelo de assessoria</b> se a plataforma for obrigada a mudar "
           "sua forma de remuneração (comissões).", "⚠"),
    bullet("Risco de <b>novos produtos problemáticos</b>: o modelo de incentivos por distribuição "
           "ainda não foi reformado estruturalmente.", "⚠"),
    bullet("Impacto reputacional pode afetar o <b>valor das ações XP Inc. (XPFS3)</b> para quem as detém.", "⚠"),
    Spacer(1, 0.2*cm),

    Paragraph("<b>4.3 Fatores que Atenuam o Risco</b>", bold_body),
    bullet("A XP é uma empresa <b>listada na NASDAQ</b>, auditada e com balanços públicos.", "✔"),
    bullet("O <b>Banco Central e a CVM</b> têm regulação ativa sobre a corretora.", "✔"),
    bullet("A plataforma tem <b>mais de 4 milhões de clientes</b> e seria systemicamente relevante "
           "para qualquer intervenção regulatória.", "✔"),
    bullet("Os investidores do Banco Master <b>estão sendo ressarcidos via FGC</b> (até o limite), "
           "reduzindo o dano concreto imediato.", "✔"),
    Spacer(1, 0.3*cm),
]

# ── 5. Veredicto ───────────────────────────────────────────────────────
story += [
    header_block("5. VEREDICTO FINAL", AZUL_ESCURO),
    Spacer(1, 0.3*cm),
]

veredictos = [
    ("CURTO PRAZO\n(0–6 meses)", "MODERADAMENTE SEGURO",
     "Seus ativos custodiados não estão em risco direto. "
     "Evite novos CDBs de bancos pequenos distribuídos pela XP. "
     "Monitore o andamento da ação judicial.",
     AZUL_CLARO),
    ("MÉDIO PRAZO\n(6–18 meses)", "ATENÇÃO REDOBRADA",
     "O desfecho regulatório e judicial definirá se o modelo da XP "
     "será reformado. Avalie diversificação para outra custódia "
     "(BTG, Rico, Clear, Banco Inter).",
     LARANJA),
    ("LONGO PRAZO\n(+18 meses)", "DECISÃO ESTRATÉGICA",
     "Se a XP não demonstrar reforma estrutural no modelo de incentivos, "
     "considere migração completa da carteira. "
     "A lealdade à plataforma não deve superar a proteção do patrimônio.",
     AZUL_MEDIO),
]

for prazo, nivel, descricao, cor in veredictos:
    prazo_p = Paragraph(prazo.replace("\n", "<br/>"),
        style("Prazo", fontSize=9, fontName="Helvetica-Bold",
              textColor=BRANCO, alignment=TA_CENTER, leading=13))
    nivel_p = Paragraph(nivel,
        style("Nivel2", fontSize=10, fontName="Helvetica-Bold",
              textColor=BRANCO, alignment=TA_CENTER))
    desc_p  = Paragraph(descricao, body)

    v_tbl = Table(
        [[prazo_p, nivel_p, desc_p]],
        colWidths=[3*cm, 5*cm, doc.width - 8*cm]
    )
    v_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (0,-1), AZUL_ESCURO),
        ("BACKGROUND",    (1,0), (1,-1), cor),
        ("BACKGROUND",    (2,0), (2,-1), CINZA_CLARO),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN",         (0,0), (1,-1), "CENTER"),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("GRID",          (0,0), (-1,-1), 0.5, CINZA_MEDIO),
    ]))
    story += [v_tbl, Spacer(1, 0.2*cm)]

# ── 6. Recomendações ───────────────────────────────────────────────────
story += [
    Spacer(1, 0.1*cm),
    header_block("6. RECOMENDAÇÕES PRÁTICAS", VERDE),
    Spacer(1, 0.2*cm),
    bullet("<b>Verifique imediatamente</b> se possui CDBs do Banco Master acima de R$ 250 mil/CPF.", "1."),
    bullet("<b>Não adquira novos</b> CDBs de bancos de médio/pequeno porte via qualquer plataforma "
           "sem análise de risco independente.", "2."),
    bullet("<b>Diversifique a custódia:</b> mantenha ativos críticos em mais de uma instituição.", "3."),
    bullet("<b>Acompanhe o andamento</b> da Ação Civil Pública no TJRJ contra XP, BTG e Nubank.", "4."),
    bullet("<b>Consulte um advisor independente</b> (fee-only) sem vínculo com distribuidoras.", "5."),
    bullet("<b>Leia os prospectos</b> de todos os produtos antes de investir; exija disclosure "
           "completo de riscos e comissões.", "6."),
    Spacer(1, 0.3*cm),
]

# ── Rodapé / Disclaimer ────────────────────────────────────────────────
story += [
    divider(CINZA_MEDIO),
    Paragraph(
        "<b>Disclaimer:</b> Este relatório tem caráter <b>exclusivamente informativo e educacional</b>. "
        "Não constitui recomendação de investimento, consultoria financeira ou jurídica. "
        "As informações foram compiladas a partir de fontes públicas disponíveis até maio de 2026. "
        "Consulte sempre um profissional habilitado antes de tomar decisões financeiras.",
        nota_style),
    Paragraph(
        f"Gerado em {date.today().strftime('%d/%m/%Y')} · Robos Trading · Uso Interno",
        style("Footer", fontSize=8, textColor=CINZA_MEDIO,
              fontName="Helvetica", alignment=TA_CENTER)),
]

doc.build(story)
print(f"PDF gerado: {OUTPUT}")
