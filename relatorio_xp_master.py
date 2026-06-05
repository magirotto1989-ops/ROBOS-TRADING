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
VERDE_ESCURO = colors.HexColor("#145A32")
CINZA_CLARO  = colors.HexColor("#F2F3F4")
CINZA_MEDIO  = colors.HexColor("#BDC3C7")
BRANCO       = colors.white
PRETO        = colors.black

styles = getSampleStyleSheet()

def style(name, **kw):
    return ParagraphStyle(name, **kw)

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

bullet_verde = style("BulletVerde",
    fontSize=10, leading=15, textColor=VERDE_ESCURO,
    fontName="Helvetica-Bold", alignment=TA_LEFT,
    leftIndent=14, firstLineIndent=-10,
    spaceBefore=3, spaceAfter=3)

bold_body = style("BoldBody",
    fontSize=10, leading=15, textColor=AZUL_ESCURO,
    fontName="Helvetica-Bold", alignment=TA_LEFT,
    spaceBefore=4, spaceAfter=2)

nota_style = style("Nota",
    fontSize=8.5, leading=13, textColor=colors.HexColor("#555555"),
    fontName="Helvetica-Oblique", alignment=TA_JUSTIFY,
    leftIndent=10, rightIndent=10, spaceBefore=4, spaceAfter=4)

destaque_verde = style("DestaqueVerde",
    fontSize=11, leading=16, textColor=VERDE_ESCURO,
    fontName="Helvetica-Bold", alignment=TA_JUSTIFY,
    spaceBefore=4, spaceAfter=4,
    leftIndent=8, rightIndent=8)

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

def bullet(texto, icon="▸", st=None):
    return Paragraph(f"{icon} {texto}", st or bullet_style)

def caixa_destaque(paragrafos, cor_borda=VERDE, cor_fundo=colors.HexColor("#EAFAF1")):
    inner = Table([[p] for p in paragrafos], colWidths=[doc.width - 1.2*cm])
    inner.setStyle(TableStyle([
        ("LEFTPADDING",   (0,0), (-1,-1), 0),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
        ("TOPPADDING",    (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
    ]))
    outer = Table([[inner]], colWidths=[doc.width])
    outer.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), cor_fundo),
        ("ROUNDEDCORNERS",[6]),
        ("BOX",           (0,0), (-1,-1), 2, cor_borda),
        ("TOPPADDING",    (0,0), (-1,-1), 12),
        ("BOTTOMPADDING", (0,0), (-1,-1), 12),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("RIGHTPADDING",  (0,0), (-1,-1), 14),
    ]))
    return outer

def divider(cor=AZUL_CLARO):
    return HRFlowable(width="100%", thickness=1, color=cor, spaceAfter=6, spaceBefore=6)

# ── Conteúdo ─────────────────────────────────────────────────────────────
story = []

# ── Capa ─────────────────────────────────────────────────────────────────
capa = Table(
    [[Paragraph("RELATÓRIO DE ANÁLISE DE RISCO", titulo_doc)],
     [Paragraph("XP Investimentos × Banco Master", subtitulo_doc)],
     [Spacer(1, 0.3*cm)],
     [Paragraph("Segurança do Patrimônio &amp; Valor da Consultoria Fee-Based", subtitulo_doc)],
     [Spacer(1, 0.5*cm)],
     [Paragraph(f"Data: {date.today().strftime('%d/%m/%Y')}  |  Uso Exclusivo do Cliente", data_style)]],
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
        "apurados, esclarece o que está — e o que <b>não está</b> — em risco para o investidor, e evidencia "
        "como a consultoria independente fee-based protege o patrimônio em cenários como este.", body),
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
    ["Risco Reputacional",    "ALTO",       "Ação judicial pública; ampla cobertura midiática negativa"],
    ["Risco Regulatório",     "ALTO",       "Investigação em andamento pelo MP e possível ação do BC/CVM"],
    ["Risco Legal",           "MÉDIO-ALTO", "Exposição a indenizações; desfecho incerto"],
    ["Risco Operacional",     "BAIXO",      "Plataforma estável; sem risco de insolvência imediata"],
    ["Risco de Solvência",    "BAIXO",      "XP Inc. é empresa listada (NASDAQ) com capital sólido"],
    ["Risco de Conflito",     "ALTO",       "Modelo de negócio com incentivos desalinhados ao cliente"],
    ["Risco para o Capital",  "BAIXO",      "Ativos custodiados na B3 — protegidos mesmo em falência da XP"],
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
    [[Paragraph(c, style(f"mh{i}{j}",
        fontSize=9,
        fontName="Helvetica-Bold" if i==0 else "Helvetica",
        textColor=BRANCO if i==0 else PRETO,
        leading=13)) for j, c in enumerate(row)]
     for i, row in enumerate(matriz_data)],
    colWidths=[5.5*cm, 2.8*cm, doc.width - 8.3*cm]
)
matriz_tbl.setStyle(TableStyle(m_style))
story += [matriz_tbl, Spacer(1, 0.4*cm)]

# ── 4. O Capital Está em Risco? ──────────────────────────────────────
story += [
    header_block("4. O SEU CAPITAL ESTÁ EM RISCO? ENTENDA A DIFERENÇA", VERDE),
    Spacer(1, 0.3*cm),
    Paragraph(
        "Esta é a pergunta mais importante — e a resposta exige clareza técnica. "
        "O escândalo do Banco Master é grave do ponto de vista ético e regulatório, "
        "mas <b>não significa que o dinheiro investido em outros produtos vai desaparecer</b>. "
        "Entenda por quê:", body),
    Spacer(1, 0.25*cm),
]

# Caixa: Custódia B3
story += [
    caixa_destaque([
        Paragraph("CUSTÓDIA INDEPENDENTE: A PROTEÇÃO ESTRUTURAL DO INVESTIDOR", style("CxTit",
            fontSize=11, fontName="Helvetica-Bold", textColor=VERDE_ESCURO,
            leading=15, alignment=TA_LEFT)),
        Spacer(1, 0.15*cm),
        Paragraph(
            "No Brasil, os ativos financeiros dos investidores são <b>segregados do patrimônio da corretora</b> "
            "por determinação legal. Isso significa que mesmo que a XP Investimentos fosse à falência amanhã, "
            "seus ativos <b>não seriam usados para pagar credores da empresa</b>.", body),
        Spacer(1, 0.1*cm),
        bullet("Ações, ETFs e BDRs → custodiados na <b>B3 (Bolsa de Valores)</b>", "✔", bullet_verde),
        bullet("Fundos de investimento → patrimônio separado, gerido pela gestora, não pela XP", "✔", bullet_verde),
        bullet("Tesouro Direto → custodiado diretamente no <b>Tesouro Nacional</b>", "✔", bullet_verde),
        bullet("CDBs, LCIs e LCAs de outros bancos → vinculados ao emissor, não à XP", "✔", bullet_verde),
        Spacer(1, 0.1*cm),
        Paragraph(
            "<b>Conclusão:</b> a XP é apenas a plataforma de acesso. O patrimônio pertence ao investidor "
            "e está protegido por lei. Uma eventual crise na corretora <b>não faz o dinheiro desaparecer</b>.",
            destaque_verde),
    ], cor_borda=VERDE, cor_fundo=colors.HexColor("#EAFAF1")),
    Spacer(1, 0.3*cm),
]

story += [
    Paragraph("<b>O que de fato pode estar em risco</b>", bold_body),
    bullet("CDBs do <b>Banco Master</b> acima de R$ 250 mil/CPF — pois o FGC não cobre o excedente", "⚠"),
    bullet("Novas aquisições de CDBs de bancos pequenos via plataformas com conflito de interesse", "⚠"),
    bullet("Ações da <b>XP Inc. (XPFS3)</b> para quem as detém — risco reputacional afeta cotação", "⚠"),
    Spacer(1, 0.3*cm),
]

# ── 5. Por que a Consultoria Fee-Based Protege o Patrimônio ───────────
story += [
    header_block("5. POR QUE A CONSULTORIA FEE-BASED PROTEGE SEU PATRIMÔNIO", VERDE_ESCURO),
    Spacer(1, 0.3*cm),
    Paragraph(
        "O caso XP × Banco Master é um exemplo perfeito de como o <b>modelo de remuneração do consultor "
        "define — ou destrói — a qualidade do conselho financeiro</b>. Veja o contraste:", body),
    Spacer(1, 0.25*cm),
]

# Tabela comparativa
comp_data = [
    ["Critério", "Modelo Comissionado (XP)", "Consultor Fee-Based"],
    ["Fonte de receita",    "Comissão paga pelo produto",        "Honorário pago pelo cliente"],
    ["Incentivo principal", "Vender o produto que paga mais",    "Resultado e satisfação do cliente"],
    ["Conflito de interesse","Estrutural e permanente",          "Inexistente — interesses alinhados"],
    ["Seleção de produtos", "Limitada ao catálogo da plataforma","Universo aberto, sem restrições"],
    ["Transparência",       "Comissão frequentemente oculta",    "Remuneração 100% transparente"],
    ["Fidelidade ao cliente","Secundária ao volume de vendas",   "Única obrigação e compromisso"],
    ["Risco ao patrimônio", "Alto (caso Banco Master)",          "Minimizado pela ausência de viés"],
]

comp_style = [
    ("BACKGROUND",    (0,0), (-1,0), AZUL_ESCURO),
    ("TEXTCOLOR",     (0,0), (-1,0), BRANCO),
    ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
    ("BACKGROUND",    (2,1), (2,-1), colors.HexColor("#EAFAF1")),
    ("FONTSIZE",      (0,0), (-1,-1), 8.5),
    ("ALIGN",         (0,0), (-1,-1), "LEFT"),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("ROWBACKGROUNDS",(0,1), (1,-1), [CINZA_CLARO, BRANCO]),
    ("GRID",          (0,0), (-1,-1), 0.4, CINZA_MEDIO),
    ("TOPPADDING",    (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("LEFTPADDING",   (0,0), (-1,-1), 7),
    ("RIGHTPADDING",  (0,0), (-1,-1), 7),
    ("TEXTCOLOR",     (2,1), (2,-1), VERDE_ESCURO),
    ("FONTNAME",      (2,1), (2,-1), "Helvetica-Bold"),
    ("TEXTCOLOR",     (1,1), (1,-1), VERMELHO),
]

comp_tbl = Table(
    [[Paragraph(c, style(f"ct{i}{j}",
        fontSize=8.5,
        fontName="Helvetica-Bold" if i==0 else "Helvetica",
        textColor=BRANCO if i==0 else PRETO,
        leading=12)) for j, c in enumerate(row)]
     for i, row in enumerate(comp_data)],
    colWidths=[4.2*cm, 5.8*cm, doc.width - 10*cm]
)
comp_tbl.setStyle(TableStyle(comp_style))
story += [comp_tbl, Spacer(1, 0.35*cm)]

# Caixa de vantagens fee-based
story += [
    caixa_destaque([
        Paragraph("AS 6 VANTAGENS CONCRETAS DO SEU CONSULTOR FEE-BASED", style("CxTit2",
            fontSize=11, fontName="Helvetica-Bold", textColor=VERDE_ESCURO,
            leading=15, alignment=TA_LEFT)),
        Spacer(1, 0.15*cm),
        bullet("<b>Recomendação isenta:</b> nenhum produto é indicado porque paga mais comissão — "
               "a seleção é feita exclusivamente pelo mérito e adequação ao seu perfil.", "1.", bullet_verde),
        bullet("<b>Acesso ao melhor do mercado:</b> sem estar preso ao catálogo de uma única plataforma, "
               "o consultor fee-based varre todo o mercado e encontra as melhores oportunidades para você.", "2.", bullet_verde),
        bullet("<b>Alinhamento total de interesses:</b> o consultor só prospera se você prosperar — "
               "sua carteira bem sucedida é o único produto que ele precisa vender.", "3.", bullet_verde),
        bullet("<b>Monitoramento ativo e alerta precoce:</b> sem incentivo para manter produtos ruins na carteira, "
               "o consultor age imediatamente ao identificar riscos como o do Banco Master.", "4.", bullet_verde),
        bullet("<b>Transparência total de custos:</b> você sabe exatamente quanto paga e por quê — "
               "não há taxas ocultas embutidas em produtos.", "5.", bullet_verde),
        bullet("<b>Proteção patrimonial de longo prazo:</b> a visão fee-based é construtiva e contínua — "
               "o foco está em preservar e crescer seu patrimônio, não em bater metas de distribuição.", "6.", bullet_verde),
    ], cor_borda=VERDE, cor_fundo=colors.HexColor("#EAFAF1")),
    Spacer(1, 0.35*cm),
]

# ── 6. Veredicto ───────────────────────────────────────────────────────
story += [
    header_block("6. VEREDICTO FINAL", AZUL_ESCURO),
    Spacer(1, 0.3*cm),
]

veredictos = [
    ("CAPITAL\nCUSTODIADO", "PROTEGIDO",
     "Ações, fundos, Tesouro Direto e demais ativos custodiados na B3 "
     "ou nos emissores <b>não desaparecem</b> em eventual problema com a XP. "
     "A segregação patrimonial é garantida por lei.",
     VERDE),
    ("CURTO PRAZO\n(0–6 meses)", "ATENÇÃO PONTUAL",
     "Verifique se há CDBs do Banco Master acima de R$ 250 mil/CPF. "
     "Evite novos CDBs de bancos pequenos sem análise independente. "
     "Monitore o andamento da ação judicial.",
     AZUL_CLARO),
    ("MÉDIO PRAZO\n(6–18 meses)", "ACOMPANHAMENTO",
     "O desfecho regulatório definirá se o modelo da XP será reformado. "
     "Avalie diversificação de custódia se necessário. "
     "Seu consultor fee-based manterá você informado sem viés.",
     LARANJA),
    ("LONGO PRAZO\n(+18 meses)", "SEGURO COM CONSULTORIA",
     "Com um consultor fee-based ao seu lado, você está estruturalmente "
     "protegido contra conflitos de interesse como o exposto neste caso. "
     "A decisão de plataforma pode ser revista a qualquer momento.",
     AZUL_MEDIO),
]

for prazo, nivel, descricao, cor in veredictos:
    prazo_p = Paragraph(prazo.replace("\n", "<br/>"),
        style(f"Prazo{prazo[:3]}", fontSize=9, fontName="Helvetica-Bold",
              textColor=BRANCO, alignment=TA_CENTER, leading=13))
    nivel_p = Paragraph(nivel,
        style(f"Nivel{prazo[:3]}", fontSize=10, fontName="Helvetica-Bold",
              textColor=BRANCO, alignment=TA_CENTER))
    desc_p  = Paragraph(descricao, body)

    v_tbl = Table(
        [[prazo_p, nivel_p, desc_p]],
        colWidths=[3*cm, 4.5*cm, doc.width - 7.5*cm]
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

# ── 7. Recomendações ───────────────────────────────────────────────────
story += [
    Spacer(1, 0.1*cm),
    header_block("7. RECOMENDAÇÕES PRÁTICAS", AZUL_MEDIO),
    Spacer(1, 0.2*cm),
    bullet("<b>Não entre em pânico:</b> seus ativos custodiados estão protegidos por lei — "
           "o dinheiro não some com problemas na corretora.", "1."),
    bullet("<b>Verifique agora</b> se possui CDBs do Banco Master acima de R$ 250 mil/CPF "
           "e acione o FGC se necessário.", "2."),
    bullet("<b>Não adquira novos</b> CDBs de bancos de médio/pequeno porte sem análise "
           "independente do seu consultor.", "3."),
    bullet("<b>Acompanhe a Ação Civil Pública</b> no TJRJ — o desfecho pode gerar ressarcimentos "
           "adicionais para quem foi prejudicado.", "4."),
    bullet("<b>Mantenha sua consultoria fee-based:</b> este caso prova, na prática, por que o modelo "
           "isento é o mais seguro para o seu patrimônio.", "5."),
    bullet("<b>Revise sua carteira</b> junto ao seu consultor para confirmar que não há exposição "
           "indesejada a produtos com conflito de interesse.", "6."),
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
        f"Gerado em {date.today().strftime('%d/%m/%Y')} · Robos Trading · Uso Exclusivo do Cliente",
        style("Footer", fontSize=8, textColor=CINZA_MEDIO,
              fontName="Helvetica", alignment=TA_CENTER)),
]

doc.build(story)
print(f"PDF gerado: {OUTPUT}")
