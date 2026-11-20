#!/usr/bin/env python3
"""Gera o guia HTML da viagem: mapa real, abas, sanfona por cidade."""
import base64
import io
import json
import os

from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # raiz do repo
IMG = os.path.join(BASE, "img")
DATA = os.path.join(BASE, "data")
HOTEIS_CIDADES = os.path.join(DATA, "hoteis_cidades.json")


def b64(nome, largura=900, qualidade=70):
    im = Image.open(os.path.join(IMG, nome)).convert("RGB")
    if im.width > largura:
        im = im.resize((largura, int(im.height * largura / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=qualidade, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def gmaps(q):
    return "https://www.google.com/maps/search/?api=1&query=" + q.replace(" ", "+")


CIDADES = [
    dict(id="pequim", nome="Pequim", emoji="🏯", noites=7, datas="30/12 – 06/01",
         lat=39.9042, lon=116.4074, img="pequim.jpg",
         cap="Cidade Proibida vista do Parque Jingshan",
         resumo="Sete noites no centro do poder: o império na Cidade Proibida e no Templo do Céu, o século XX no "
                "Museu Nacional e na praça, e a cidade de um andar nos hutongs. É aqui que o feriado de Ano Novo "
                "fica resolvido, sem mala e sem trem.",
         atracoes=[
             ("Cidade Proibida", "3-4 h", "≈ ¥40 (inverno)",
              "Ter–dom, 8:30–16:30 · fecha às segundas · reserva online com passaporte, 7 dias antes", "forbidden city"),
             ("Grande Muralha (Mutianyu)", "dia inteiro", "≈ ¥45 + teleférico ≈ ¥120",
              "Abre ~8:00 · melhor chegar cedo · 1h30 de carro do centro", "Mutianyu Great Wall"),
             ("Templo do Céu", "2 h", "≈ ¥28 (parque) / ¥35 (combinado)",
              "Parque 6:00–21:00 · melhor de manhã, com tai chi", "Temple of Heaven Beijing"),
             ("Museu Nacional", "2-3 h", "grátis",
              "Fecha às segundas · última entrada 16:00 · reserva obrigatória", "National Museum of China"),
             ("Templo Lama (Yonghegong)", "1h30", "≈ ¥25",
              "8:00–17:00 · chega-se de metrô (linha 2/5, Yonghegong)", "Yonghegong Lama Temple"),
             ("Museu Nacional de Arte da China", "2 h", "≈ ¥30",
              "Perto da praça, cercado de água · boa opção de arte numa tarde fria", "National Art Museum of China"),
             ("798 Art District", "meio dia", "grátis",
              "Galerias ~10:00–18:00, muitas fecham às segundas", "798 Art District Beijing"),
         ],
         dicas=["01/01 é feriado: reservar Cidade Proibida em 25/12 e Museu Nacional em 29/12",
                "Grande Muralha no dia 31/12 (dia útil) em vez do feriado",
                "Hasteamento da bandeira às 07:36 no dia 1º — chegar 1h30 antes",
                "Em 04/01 (segunda) os museus fecham: dia de Palácio de Verão, Beihai e hutongs"],
         hoteis=[("Ascott Raffles City Beijing", "5★ · 4,5 (70)", "Dongzhimen — apartamento com cozinha, piscina"),
                 ("Holiday Inn Express Dongzhimen", "4★ · 4,4 (229)", "Dongzhimen — quartos twin, café da manhã"),
                 ("Shichahai Shadow Art Hotel", "4★ · 4,6 (89)", "Gulou — hutong com teatro de sombras")]),
    dict(id="datong", nome="Datong", emoji="🗿", noites=2, datas="06 – 08/01",
         lat=40.0900, lon=113.3000, img="datong.jpg",
         cap="Grutas de Yungang, séculos V-VI",
         resumo="Onde a arte budista chinesa começa. Duas obras-primas em um dia e o ponto mais frio da viagem "
                "(−13 °C à noite).",
         atracoes=[
             ("Grutas de Yungang", "3 h", "≈ ¥120",
              "8:30–17:00 (inverno fecha mais cedo) · patrimônio UNESCO", "Yungang Grottoes"),
             ("Templo Suspenso (Xuankong Si)", "2 h", "≈ ¥130",
              "8:00–17:30 · 1h15 de carro de Datong · construído em 491 d.C.", "Hanging Temple Datong"),
             ("Templo Huayan", "1 h", "≈ ¥50", "8:00–17:00 · dinastia Liao, século XI", "Huayan Temple Datong"),
             ("Muralha de Datong", "1 h", "grátis (subida paga)", "Abre até ~21:00 · boa ao entardecer", "Datong City Wall"),
         ],
         dicas=["Separar Yungang e Templo Suspenso em períodos diferentes do dia: são 1h15 um do outro",
                "Roupa de frio extremo: é o ponto mais frio do roteiro"],
         hoteis=None),
    dict(id="pingyao", nome="Pingyao", emoji="🏮", noites=2, datas="08 – 10/01",
         lat=37.2000, lon=112.1800, img="pingyao.jpg",
         cap="Pingyao, cidade murada",
         resumo="Uma cidade do século XIX inteira, dentro de 6 km de muro Ming, sem carros. Aqui nasceu o "
                "primeiro banco da China.",
         atracoes=[
             ("Muralha Ming", "1h30", "≈ ¥125 (passe de 3 dias)",
              "8:00–18:00 · o passe cobre os principais edifícios", "Pingyao Ancient City Wall"),
             ("Rishengchang", "1 h", "incluso no passe",
              "8:00–18:00 · primeira casa bancária da China (1823)", "Rishengchang Pingyao"),
             ("Templo Shuanglin", "1 h", "≈ ¥35", "8:00–18:00 · esculturas pintadas · 6 km da cidade", "Shuanglin Temple Pingyao"),
             ("Casas de mercadores (Wang/Qiao)", "meio dia", "≈ ¥60 cada",
              "8:00–18:00 · fora da cidade, precisa de carro", "Wang Family Compound Shanxi"),
         ],
         dicas=["Passe de 3 dias vale a pena mesmo com 2 noites",
                "Andar de noite dentro da cidade murada, quando o turismo interno vai embora"],
         hoteis=None),
    dict(id="xian", nome="Xi'an", emoji="🏛️", noites=3, datas="10 – 13/01",
         lat=34.3416, lon=108.9398, img="xian.jpg",
         cap="Exército de Terracota, 210 a.C.",
         resumo="Capital de 13 dinastias e marco zero da China unificada. Um dia para a Terracota, um para a "
                "cidade e um para o Monte Hua.",
         atracoes=[
             ("Exército de Terracota", "meio dia", "≈ ¥120",
              "8:30–17:00 · 1h de ônibus/carro · comprar junto com o Museu do Sítio", "Terracotta Army Xi'an"),
             ("Muralha de Xi'an", "2 h", "≈ ¥54 + aluguel de bike",
              "8:00–22:00 · 14 km de perímetro, dá para pedalar", "Xi'an City Wall"),
             ("Museu de História de Shaanxi", "3 h", "grátis com reserva",
              "Fecha às segundas · reserva com passaporte", "Shaanxi History Museum"),
             ("Monte Hua", "dia inteiro", "≈ ¥160 + teleférico",
              "40 min de trem-bala até Huashan Norte · passarela de tábuas ·",
              "Mount Hua Shaanxi"),
             ("Bairro Muçulmano", "2 h", "grátis",
              "Movimento do fim da tarde à noite · melhor comida de rua da viagem", "Muslim Quarter Xi'an"),
         ],
         dicas=["Monte Hua em dia sem neve prevista: com gelo, a passarela fecha",
                "Muralha ao entardecer, de bicicleta"],
         hoteis=None),
    dict(id="chongqing", nome="Chongqing", emoji="🌉", noites=2, datas="13 – 15/01",
         lat=29.5630, lon=106.5516, img="chongqing.jpg",
         cap="Chongqing sobre o Yangtzé",
         resumo="Capital da China na guerra (1937-46) e a cidade vertical: metrô atravessando prédios, elevador "
                "como transporte público e hotpot na origem.",
         atracoes=[
             ("Museu dos Três Gargantas", "2 h", "grátis com reserva",
              "Fecha às segundas · 9:00–17:00", "Three Gorges Museum Chongqing"),
             ("Hongya Cave", "1h30", "grátis",
              "Melhor à noite, quando acende · 11 andares de palafitas", "Hongya Cave Chongqing"),
             ("Teleférico do Yangtzé", "1 h", "≈ ¥30 (ida)",
              "9:00–22:00 · travessia de 5 min com vista da cidade", "Yangtze River Cableway Chongqing"),
             ("Esculturas de Dazu", "meio dia", "≈ ¥115",
              "1h30 de carro · UNESCO · 50 mil imagens budistas e taoístas", "Dazu Rock Carvings"),
             ("Estação Liziba", "30 min", "grátis (metrô)",
              "Linha 2 · o trem atravessa o 6º ao 8º andar de um prédio", "Liziba Station Chongqing"),
         ],
         dicas=["Hotpot de Chongqing é mais apimentado que o de Sichuan: pedir “menos pimenta” (微辣)",
                "A cidade é vertical: contar com escadarias e ladeiras mesmo em trechos curtos"],
         hoteis=None),
    dict(id="changsha", nome="Changsha", emoji="🌶️", noites=2, datas="15 – 17/01 (A: 18 – 20/01)",
         lat=28.2282, lon=112.9388, img="changsha.jpg",
         cap="Pavilhão Aiwan, monte Yuelu",
         resumo="Academia Yuelu (976) e a cozinha mais apimentada do país. De lá sai o desvio para Hengshan, "
                "se quisermos outra subida.",
         atracoes=[
             ("Academia Yuelu", "2 h", "≈ ¥40",
              "7:30–18:00 · campus universitário mais antigo em atividade", "Yuelu Academy Changsha"),
             ("Museu de Hunan", "3 h", "grátis com reserva",
              "Fecha às segundas · múmia de Lady Dai, 2.100 anos", "Hunan Museum Changsha"),
             ("Ilha Laranja", "2 h", "grátis",
              "Aberto o dia todo · caminhada e o poema de Mao no rio", "Orange Isle Changsha"),
             ("Hengshan (Nanyue)", "dia inteiro", "≈ ¥80 + teleférico",
              "40 min de trem-bala + ônibus · 1.300 m de subida", "Mount Heng Hunan"),
         ],
         dicas=["Cozinha de Hunan: pedir “pouco picante” não resolve — provar aos poucos",
                "Shaoshan (cidade natal de Mao) a 1h, se houver interesse político"],
         hoteis=None),
    dict(id="xangai", nome="Xangai", emoji="🏙️", noites=3, datas="20 – 23/01 (C: 17 – 22/01)",
         lat=31.2304, lon=121.4737, img="xangai.jpg",
         cap="O Bund",
         resumo="A outra China: cais colonial, Concessão Francesa, arte contemporânea no West Bund — e um dia "
                "inteiro em Suzhou.",
         atracoes=[
             ("O Bund", "2 h", "grátis",
              "Aberto o dia todo · melhor ao entardecer, quando acendem as luzes", "The Bund Shanghai"),
             ("Museu de Xangai", "3 h", "grátis com reserva",
              "Fecha às segundas · bronzes, cerâmica e caligrafia", "Shanghai Museum"),
             ("Concessão Francesa", "meio dia", "grátis",
              "Wukang Road e Tianzifang · cafés e ruas arborizadas", "Former French Concession Shanghai"),
             ("Jardim Yu", "2 h", "≈ ¥40",
              "8:45–16:45 · cidade antiga ao redor", "Yu Garden Shanghai"),
             ("Suzhou (bate-volta)", "dia inteiro", "trem ≈ ¥40 cada way",
              "25 min de trem-bala · jardins UNESCO e canais", "Humble Administrator's Garden Suzhou"),
         ],
         dicas=["Reservar museus com passaporte no dia anterior",
                "Suzhou: escolher 2 jardins, não 4 — são parecidos e cansam"],
         hoteis=None),
    dict(id="hangzhou", nome="Hangzhou", emoji="🍵", noites=1, datas="23 – 24/01",
         lat=30.2741, lon=120.1551, img="hangzhou.jpg",
         cap="Lago Oeste",
         resumo="O lugar mais pintado da China, a 1h de Xangai: Lago Oeste, templo Lingyin e chá Longjing com "
                "os produtores.",
         atracoes=[
             ("Lago Oeste", "meio dia", "grátis",
              "Aberto o dia todo · alugar bicicleta na margem", "West Lake Hangzhou"),
             ("Templo Lingyin", "2h30", "≈ ¥75 (entrada + templo)",
              "7:00–18:00 · 300 arhats esculpidos na rocha", "Lingyin Temple Hangzhou"),
             ("Campos de chá Longjing", "2 h", "grátis (degustação paga)",
              "Meijiawu · provar com os produtores", "Meijiawu Tea Village"),
         ],
         dicas=["Uma noite é pouco: priorizar Lago Oeste ao entardecer e Lingyin de manhã"],
         hoteis=None),
    dict(id="nanjing", nome="Nanjing", emoji="🕯️", noites=1, datas="24 – 25/01",
         lat=32.0603, lon=118.7969, img="nanjing.jpg",
         cap="Nanjing",
         resumo="Capital de seis dinastias e palco do episódio mais duro da história moderna chinesa. Uma noite, "
                "mas que fecha o arco político.",
         atracoes=[
             ("Memorial do Massacre de 1937", "2h30", "grátis com reserva",
              "Fecha às segundas · 8:30–16:30 · austero, indispensável", "Memorial Hall of the Victims in Nanjing Massacre"),
             ("Muralha Ming", "2 h", "≈ ¥30",
              "8:30–17:00 · trecho de Zhonghua Gate", "Zhonghua Gate Nanjing"),
             ("Mausoléu de Sun Yat-sen", "2 h", "grátis com reserva",
              "8:30–17:00 · fecha às segundas", "Sun Yat-sen Mausoleum Nanjing"),
         ],
         dicas=["Chegar de trem de Xangai/Hangzhou e sair para Pequim no dia seguinte",
                "O memorial exige reserva e não é lugar de foto"],
         hoteis=None),
    dict(id="zhangjiajie", nome="Zhangjiajie", emoji="🌄", noites=3, datas="15 – 18/01 (opção A)",
         lat=29.1170, lon=110.4790, img="zhangjiajie.jpg",
         cap="Zhangjiajie National Forest Park",
         resumo="As montanhas de Avatar: mais de 3 mil pilares de arenito cobertos de pinheiros. O desvio mais "
                "espetacular e o de maior risco climático.",
         atracoes=[
             ("Wulingyuan / Yuanjiajie", "2 dias", "≈ ¥228 (passe de 4 dias)",
              "7:00–18:00 · inclui ônibus internos · teleféricos à parte", "Zhangjiajie National Forest Park"),
             ("Elevador de Bailong", "1 h", "≈ ¥72",
              "326 m de altura · pode fechar por manutenção ou vento", "Bailong Elevator"),
             ("Monte Tianmen", "meio dia", "≈ ¥278",
              "Teleférico de 7,4 km · 999 degraus até o Portão do Céu", "Tianmen Mountain"),
             ("Ponte de vidro do Grand Canyon", "2 h", "≈ ¥140",
              "430 m de extensão a 300 m de altura", "Zhangjiajie Grand Canyon Glass Bridge"),
         ],
         dicas=["Em janeiro, 52% dos dias têm céu encoberto: reservar 3 dias para garantir um dia aberto",
                "Dormir dentro do parque (Wulingyuan) economiza 1h de traslado por dia"],
         hoteis=None),
    dict(id="guilin", nome="Guilin / Yangshuo", emoji="🛶", noites=3, datas="17 – 20/01 (opção B)",
         lat=25.2736, lon=110.2900, img="yangshuo.jpg",
         cap="Rio Li, em Yangshuo",
         resumo="Karst, rio e bicicleta. O clima mais ameno da viagem e o único lugar do roteiro com arrozais.",
         atracoes=[
             ("Cruzeiro no Rio Li", "4 h", "≈ ¥215–270",
              "Saídas de manhã de Guilin a Yangshuo · 4h de barco", "Li River Cruise Guilin"),
             ("Bicicleta em Yangshuo", "meio dia", "≈ ¥50/dia",
              "Alugar na vila · rota do rio Yulong", "Yangshuo Yulong River"),
             ("Terraços de Longji", "dia inteiro", "≈ ¥80–100",
              "2h de carro · em janeiro os terraços estão secos", "Longji Rice Terraces Longsheng"),
             ("Caverna da Flauta de Junco", "2 h", "≈ ¥90",
              "8:00–17:30 · iluminação artificial, mais espetáculo que natureza", "Reed Flute Cave Guilin"),
         ],
         dicas=["Base em Yangshuo, não em Guilin: a paisagem está na vila",
                "Voo Guilin → Xangai resolve o trecho longo até o delta"],
         hoteis=None),
    dict(id="huangshan", nome="Huangshan", emoji="⛰️", noites=1, datas="23 – 24/01 (opção C)",
         lat=30.1340, lon=118.1610, img="huangshan.jpg",
         cap="Huangshan (Montanha Amarela)",
         resumo="O mar de nuvens: picos de granito, pinheiros e escadarias. Em janeiro, geada e pouca gente.",
         atracoes=[
             ("Picos (Yuping/Beihai)", "1 dia e meio", "≈ ¥150–190 + teleférico ≈ ¥80",
              "Abre 6:30 · subir de teleférico e descer a pé, ou o contrário", "Huangshan Yellow Mountain"),
             ("Nascer do sol no alto", "—", "incluso",
              "Dormir no topo (hotéis caros) ou descer de madrugada", "Huangshan sunrise"),
             ("Aldeias de Hongcun / Xidi", "meio dia", "≈ ¥104 cada",
              "UNESCO · cenário de “O Tigre e o Dragão”", "Hongcun Village Anhui"),
         ],
         dicas=["Gelo nas escadarias: crampon é obrigatório em janeiro",
                "Deixar a mala no hotel da base e subir só com mochila"],
         hoteis=None),
]

ABAS = [("roteiro", "🗺️ Roteiro"), ("passagens", "✈️ Passagens"), ("hoteis", "🛏️ Hospedagens"),
        ("passeios", "🎟️ Passeios"), ("preparo", "🎒 Preparo")]

CSS = """
:root{--navy:#12263a;--terra:#d94f30;--ink:#23262b;--grey:#6b7280;--line:#e3e6ea;--bg:#f5f6f8}
*{box-sizing:border-box}
body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.55;-webkit-text-size-adjust:100%}
.wrap{max-width:1120px;margin:0 auto;padding:0 16px 64px}
header.hero{color:#fff;padding:44px 0 0;background-image:linear-gradient(100deg,rgba(18,38,58,.95),rgba(18,38,58,.72)),var(--hero);background-size:cover;background-position:center}
.kicker{font-size:11.5px;letter-spacing:2px;text-transform:uppercase;color:#9fc3e0;font-weight:700}
h1{font-size:clamp(25px,4.6vw,38px);margin:8px 0 10px;font-weight:800;line-height:1.1}
.lead{font-size:clamp(14px,1.7vw,17px);color:#d7e5f0;max-width:720px;margin:0 0 18px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:22px}
.chip{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);padding:5px 11px;border-radius:999px;font-size:12.5px}
nav.tabs{display:flex;flex-wrap:wrap;gap:4px;padding:0;background:transparent}
nav.tabs button{flex:0 0 auto;background:rgba(255,255,255,.1);border:none;border-radius:10px 10px 0 0;color:#cfe0ee;padding:11px 16px;font-size:14px;font-weight:600;cursor:pointer;font-family:inherit}
nav.tabs button[aria-selected="true"]{background:var(--bg);color:var(--navy)}
section[role=tabpanel]{display:none;padding-top:22px}
section[role=tabpanel].on{display:block}
h2{font-size:clamp(19px,2.6vw,24px);margin:26px 0 10px;color:var(--navy)}
h2:first-child{margin-top:0}
.sub{display:block;font-size:13.5px;font-weight:400;color:var(--grey);margin-top:3px}
p{margin:0 0 12px}
.note{font-size:12.5px;color:var(--grey)}
#map{height:440px;border-radius:14px;border:1px solid var(--line);z-index:0}
.leaflet-container{font-family:inherit}
details{background:#fff;border:1px solid var(--line);border-radius:14px;margin-bottom:10px;overflow:hidden}
details summary{cursor:pointer;padding:14px 16px;display:flex;align-items:center;gap:10px;font-weight:700;font-size:16px;list-style:none}
details summary::-webkit-details-marker{display:none}
details summary .chev{margin-left:auto;color:#9aa1ab;transition:transform .15s;font-size:13px}
details[open] summary .chev{transform:rotate(90deg)}
details summary .when{margin-left:auto;font-size:12.5px;color:var(--grey);font-weight:500}
details .inner{padding:0 16px 16px}
details img{width:100%;height:190px;object-fit:cover;object-position:center 60%;border-radius:10px;display:block}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;border-radius:10px;margin:10px 0}
.tw table{min-width:560px}
table{width:100%;border-collapse:collapse;background:#fff;font-size:13.5px}
th{background:#eef1f5;text-align:left;padding:8px 10px;font-size:12.5px;color:#37414d}
td{padding:8px 10px;border-top:1px solid var(--line);vertical-align:top}
.tag{display:inline-block;font-size:11.5px;background:#f1f3f6;color:#37414d;border-radius:999px;padding:3px 9px;margin:0 4px 4px 0}
a{color:#1c5d80}
a.btn{display:inline-block;background:var(--navy);color:#fff;text-decoration:none;padding:8px 13px;border-radius:9px;font-size:13px;font-weight:600;margin:6px 6px 0 0}
a.btn.ghost{background:#fff;color:var(--navy);border:1px solid var(--line)}
.status{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;margin:10px 0 0}
.st{background:#fff;border:1px solid var(--line);border-radius:11px;padding:12px 14px;font-size:13.5px}
.st b{display:block;font-size:13.5px}
.st span{color:var(--grey);font-size:12.5px}
.fine{font-size:11.5px;color:#9aa1ab}
ul.tight{margin:6px 0 10px;padding-left:20px;font-size:13.5px}
ul.tight li{margin:5px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px}
.mini{background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px 14px;font-size:13.5px}
.mini b{display:block;font-size:14px;margin-bottom:2px}
footer{margin-top:36px;font-size:11.5px;color:var(--grey)}
"""


def hoteis_por_cidade():
    dados = {}
    if os.path.exists(HOTEIS_CIDADES):
        dados = json.load(open(HOTEIS_CIDADES, encoding="utf-8"))
    return dados


def top3(lista):
    def val(x):
        try:
            nota = float((x.get("nota") or "0").replace(",", "."))
        except Exception:
            nota = 0
        try:
            aval = int((x.get("avaliacoes") or "0").replace(".", ""))
        except Exception:
            aval = 0
        return nota, aval

    bons = [x for x in lista if val(x)[1] >= 25]
    if len(bons) < 3:
        bons = sorted(lista, key=val, reverse=True)
    return sorted(bons, key=val, reverse=True)[:3]




def svg_schema():
    """Esquema de posições em SVG — funciona sem internet."""
    pts = {c["id"]: (c["lon"], c["lat"], c["nome"]) for c in CIDADES}
    w, h = 760, 500

    def xy(lon, lat):
        return (30 + (lon - 106.0) * 44, 40 + (41.5 - lat) * 26)

    p = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto">',
         '<rect width="100%" height="100%" fill="#fbfcfd"/>']
    for x in range(40, w, 46):
        p.append(f'<line x1="{x}" y1="20" x2="{x}" y2="{h-20}" stroke="#eef1f4"/>')
    for y in range(40, h, 26):
        p.append(f'<line x1="20" y1="{y}" x2="{w-20}" y2="{y}" stroke="#eef1f4"/>')

    anel = ["pequim", "datong", "pingyao", "xian", "chongqing", "changsha", "xangai",
            "hangzhou", "nanjing", "pequim"]
    d = " ".join(("M" if i == 0 else "L") + "%.0f,%.0f" % xy(pts[n][0], pts[n][1]) for i, n in enumerate(anel))
    p.append(f'<path d="{d}" fill="none" stroke="#12263a" stroke-width="3" stroke-linejoin="round"/>')
    for cor, seq in (("#2f6b4f", ["chongqing", "zhangjiajie", "changsha"]),
                     ("#1f6f8b", ["changsha", "guilin", "xangai"]),
                     ("#7a4b2a", ["hangzhou", "huangshan", "nanjing"])):
        dd = " ".join(("M" if i == 0 else "L") + "%.0f,%.0f" % xy(pts[n][0], pts[n][1]) for i, n in enumerate(seq))
        p.append(f'<path d="{dd}" fill="none" stroke="{cor}" stroke-width="2.5" stroke-dasharray="7 5"/>')

    rot = {"pequim": (12, -6, "start"), "datong": (10, -10, "start"), "pingyao": (11, 5, "start"),
           "xian": (11, 5, "start"), "chongqing": (11, 16, "start"), "zhangjiajie": (-11, 5, "end"),
           "changsha": (11, 15, "start"), "guilin": (11, 16, "start"), "xangai": (-12, -8, "end"),
           "hangzhou": (-12, 14, "end"), "huangshan": (-11, 15, "end"), "nanjing": (12, -8, "start")}
    for cid, (lon, lat, nome) in pts.items():
        x, y = xy(lon, lat)
        cor = {"zhangjiajie": "#2f6b4f", "guilin": "#1f6f8b", "huangshan": "#7a4b2a"}.get(cid, "#12263a")
        p.append(f'<circle cx="{x}" cy="{y}" r="6" fill="#fff" stroke="{cor}" stroke-width="3"/>')
        dx, dy, anc = rot[cid]
        p.append(f'<text x="{x+dx}" y="{y+dy}" font-size="13.5" font-weight="600" fill="#23262b" '
                 f'text-anchor="{anc}" font-family="system-ui,sans-serif">{nome}</text>')
    p.append('<rect x="20" y="18" width="186" height="104" rx="10" fill="#fff" stroke="#e3e6ea"/>')
    for i, (cor, dash, txt) in enumerate([("#12263a", "", "trajeto comum"), ("#2f6b4f", "7 5", "A · Zhangjiajie"),
                                          ("#1f6f8b", "7 5", "B · Guilin"), ("#7a4b2a", "7 5", "C · Huangshan")]):
        y = 42 + i * 22
        da = f' stroke-dasharray="{dash}"' if dash else ""
        p.append(f'<line x1="34" y1="{y}" x2="62" y2="{y}" stroke="{cor}" stroke-width="3"{da}/>')
        p.append(f'<text x="70" y="{y+4.5}" font-size="12.5" fill="#4b5563" font-family="system-ui,sans-serif">{txt}</text>')
    p.append("</svg>")
    return "".join(p)


def main():
    imgs = {c["id"]: b64(c["img"]) for c in CIDADES}
    hero = b64("muralha.jpg", largura=1500, qualidade=72)
    hoteis = hoteis_por_cidade()

    # ---------- sanfona de cidades
    cidades_html = []
    for c in CIDADES:
        atr = "".join(
            f"<tr><td><b>{n}</b><br><span class='fine'>{obs}</span></td><td>{t}</td><td>{p}</td>"
            f"<td><a href='{gmaps(g)}' target='_blank' rel='noopener'>mapa</a></td></tr>"
            for n, t, p, obs, g in c["atracoes"])

        if c["hoteis"]:
            hot = "".join(f"<li><b>{n}</b> — {r} · <span class='fine'>{o}</span></li>" for n, r, o in c["hoteis"])
        else:
            lista = hoteis.get(c["nome"].replace("Guilin / Yangshuo", "Guilin"), [])
            if not lista:
                lista = hoteis.get(c["nome"], [])
            if lista:
                hot = "".join(
                    f"<li><b>{h['nome']}</b> — {h['estrelas']}★ · {h['nota']} ({h['avaliacoes']} avaliações)</li>"
                    for h in top3(lista))
            else:
                hot = "<li class='fine'>Levantar no Booking pelo link abaixo.</li>"

        dicas = "".join(f"<li>{d}</li>" for d in c["dicas"])
        cidades_html.append(f"""
    <details id="city-{c['id']}">
      <summary>{c['emoji']} {c['nome']}<span class="when">{c['noites']} noites · {c['datas']}</span><span class="chev">▶</span></summary>
      <div class="inner">
        <img src="{imgs[c['id']]}" alt="{c['nome']}">
        <div class="cap fine" style="margin:6px 0 10px">{c['cap']} · Wikimedia Commons</div>
        <p>{c['resumo']}</p>
        <h3 style="font-size:14.5px;margin:14px 0 4px">O que fazer</h3>
        <table><thead><tr><th>Atração</th><th>Tempo</th><th>Ingresso (referência)</th><th></th></tr></thead>
        <tbody>{atr}</tbody></table>
        <h3 style="font-size:14.5px;margin:14px 0 4px">Onde dormir</h3>
        <ul class="tight">{hot}</ul>
        <h3 style="font-size:14.5px;margin:14px 0 4px">Programação e dicas</h3>
        <ul class="tight">{dicas}</ul>
        <a class="btn" href="https://www.booking.com/searchresults.pt-br.html?ss={c['nome'].replace(' ', '+')}%2C+China&checkin={DATA_IN[c['id']]}&checkout={DATA_OUT[c['id']]}&group_adults=4&no_rooms=2" target="_blank" rel="noopener">Ver hospedagem</a>
        <a class="btn ghost" href="{gmaps(c['nome'] + ' China')}" target="_blank" rel="noopener">No mapa</a>
      </div>
    </details>""")

    # ---------- tabela consolidada de passeios
    passeios = []
    for c in CIDADES:
        for n, t, p, obs, g in c["atracoes"]:
            passeios.append(f"<tr><td><b>{c['emoji']} {c['nome']}</b></td><td>{n}</td><td>{t}</td>"
                            f"<td>{p}</td><td class='fine'>{obs}</td>"
                            f"<td><a href='{gmaps(g)}' target='_blank' rel='noopener'>mapa</a></td></tr>")

    # ---------- hospedagens consolidadas
    linhas_hotel = []
    for c in CIDADES:
        if c["hoteis"]:
            for n, r, o in c["hoteis"]:
                linhas_hotel.append(f"<tr><td><b>{c['emoji']} {c['nome']}</b></td><td>{n}</td><td>{r}</td><td class='fine'>{o}</td></tr>")
        else:
            lista = hoteis.get("Guilin" if "Guilin" in c["nome"] else c["nome"], [])
            for h in top3(lista):
                linhas_hotel.append(f"<tr><td><b>{c['emoji']} {c['nome']}</b></td><td>{h['nome']}</td>"
                                    f"<td>{h['estrelas']}★ · {h['nota']}</td><td class='fine'>{h['avaliacoes']} avaliações</td></tr>")

    pontos_json = json.dumps([{"id": c["id"], "nome": c["nome"], "lat": c["lat"], "lon": c["lon"],
                               "noites": c["noites"], "datas": c["datas"], "emoji": c["emoji"]} for c in CIDADES],
                             ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Guia da viagem · China em 30 dias</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<style>:root{{--hero:url({hero})}}</style>
<style>{CSS}</style>
</head>
<body>
<header class="hero">
  <div class="wrap">
    <div class="kicker">Guia da viagem · versão de trabalho</div>
    <h1>China em 30 dias</h1>
    <p class="lead">Mapa do trajeto, sanfona por cidade, passagens emitidas, hospedagem pesquisada e o que reservar — tudo em abas.</p>
    <div class="chips">
      <span class="chip">30/12/2026 → 27/01/2027</span>
      <span class="chip">27 noites</span>
      <span class="chip">4 viajantes</span>
      <span class="chip">Air China · 5HAJHF</span>
    </div>
    <nav class="tabs" role="tablist">
      {"".join(f'<button role="tab" data-tab="{k}" aria-selected="{"true" if i == 0 else "false"}">{v}</button>' for i, (k, v) in enumerate(ABAS))}
    </nav>
  </div>
</header>

<div class="wrap">

<section role="tabpanel" id="tab-roteiro" class="on">
  <h2>O trajeto<span class="sub">Clique em uma cidade no mapa — ou abra a sanfona abaixo. As linhas pontilhadas são as três variantes de natureza.</span></h2>
  <div id="map"></div>
  <p class="fine">Mapa com dados do OpenStreetMap (precisa de internet). Sem conexão, use o esquema abaixo.</p>

  <details id="esquema-offline">
    <summary>🧭 Esquema de posições (funciona offline)<span class="chev">▶</span></summary>
    <div class="inner">{svg_schema()}</div>
  </details>

  <div class="status">
    <div class="st"><b>✅ Passagens</b><span>Air China 5HAJHF · ida 29/12, volta 27/01 02:45</span></div>
    <div class="st"><b>✅ Visto</b><span>Isento · chegada 30/12, saída 27/01 (28 dias)</span></div>
    <div class="st"><b>🟡 Roteiro</b><span>Três variantes em aberto: 🌄 🛶 ⛰️</span></div>
    <div class="st"><b>⬜ Hospedagem</b><span>Pequim sugerida em Dongzhimen</span></div>
    <div class="st"><b>⬜ Trens</b><span>Venda abre ~15 dias antes de cada trecho</span></div>
  </div>

  <h2>Cidades, uma por uma<span class="sub">Cada bloco tem atrações, onde dormir e a programação sugerida.</span></h2>
  {"".join(cidades_html)}
</section>

<section role="tabpanel" id="tab-passagens">
  <h2>Passagens emitidas<span class="sub">Air China · localizador 5HAJHF · emitido em 13/10/2026</span></h2>
  <table>
    <thead><tr><th>Trecho</th><th>Voo</th><th>Horários</th><th>Duração</th></tr></thead>
    <tbody>
      <tr><td><b>IDA · 29/12</b><br>São Paulo → Pequim</td><td>CA898 · Boeing 787-900</td>
        <td>GRU 08:30 → Madri 22:35<br><span class="tag">conexão 2h05 · T1</span><br>Madri 00:40 → PEK 18:45 (+1 dia)</td><td>23h15</td></tr>
      <tr><td><b>VOLTA · 27/01</b><br>Pequim → São Paulo</td><td>CA875 · A350-900<br>CA7105 (LATAM)</td>
        <td>PEK 02:45 → Paris 07:00<br><span class="tag">conexão 5h05 · T1 → T2A</span><br>Paris 12:05 → GRU 20:00</td><td>28h15</td></tr>
    </tbody>
  </table>
  <div class="grid">
    <div class="mini"><b>Bagagem</b>2 peças na ida, <b>1 peça na volta</b> — o limite para as compras na China.</div>
    <div class="mini"><b>Assentos</b>52A (GRU→PEK) e 54A (PEK→CDG). O trecho Paris→São Paulo ainda sem assento.</div>
    <div class="mini"><b>Saída de Pequim</b>Voo às 02:45: estar no aeroporto por volta de <b>00:45</b> do dia 27.</div>
  </div>
  <h2>Para consultar e comparar</h2>
  <a class="btn" href="https://www.airchina.com.br" target="_blank" rel="noopener">Air China (gestão da reserva)</a>
  <a class="btn ghost" href="https://www.google.com/travel/flights?q=Flights%20from%20GRU%20to%20PEK%20on%202026-12-29%20through%202027-01-27&curr=BRL&hl=pt-BR" target="_blank" rel="noopener">Google Flights · mesma rota</a>
  <a class="btn ghost" href="https://www.trip.com/flights/" target="_blank" rel="noopener">Trip.com</a>
  <h2>Trens internos</h2>
  <table>
    <thead><tr><th>Trecho</th><th>Data</th><th>Duração aprox.</th><th>Venda abre</th></tr></thead>
    <tbody>
      <tr><td>Pequim → Datong</td><td>06/01</td><td>1h45</td><td>~21/12/2026</td></tr>
      <tr><td>Datong → Pingyao</td><td>08/01</td><td>3h</td><td>~24/12/2026</td></tr>
      <tr><td>Pingyao → Xi'an</td><td>10/01</td><td>3h</td><td>~26/12/2026</td></tr>
      <tr><td>Xi'an → Chongqing</td><td>13/01</td><td>5h</td><td>~29/12/2026</td></tr>
      <tr><td>Chongqing → bloco de natureza</td><td>15/01</td><td>4h30</td><td>~01/01/2027</td></tr>
      <tr><td>Nanjing → Pequim</td><td>25/01</td><td>3h30</td><td>~10/01/2027</td></tr>
    </tbody>
  </table>
  <p class="note">Comprar no <a href="https://www.trip.com/trains/" target="_blank" rel="noopener">Trip.com</a> (aceita cartão internacional) ou no <a href="https://www.12306.cn" target="_blank" rel="noopener">12306</a>. Em período de chunyun, comprar no primeiro dia da janela.</p>
</section>

<section role="tabpanel" id="tab-hoteis">
  <h2>Pequim · onde ficar nas 7 noites<span class="sub">Bairro escolhido: Dongzhimen — comida a qualquer hora, hutong a pé, metrô 2/5/13 e saída fácil para o aeroporto.</span></h2>
  <table>
    <thead><tr><th>Opção</th><th>Categoria / nota</th><th>Por que serve para 4</th></tr></thead>
    <tbody>
      <tr><td><b>Ascott Raffles City Beijing</b><br><span class="fine">Dongzhimen</span></td><td>5★ · 4,5 (70)</td>
        <td>Apartamento com cozinha, piscina e academia. Confirmar a categoria de <b>dois dormitórios</b>: a de entrada pode ser estúdio.</td></tr>
      <tr><td><b>Holiday Inn Express Dongzhimen</b><br><span class="fine">Dongzhimen</span></td><td>4★ · 4,4 (229)</td>
        <td>Padrão previsível, quartos twin, café da manhã. Duas reservas (casal + twin) resolvem o grupo.</td></tr>
      <tr><td><b>Shichahai Shadow Art Hotel</b><br><span class="fine">Gulou / Shichahai</span></td><td>4★ · 4,6 (89)</td>
        <td>Alternativa “hutong com charme”, com teatro de sombras. Quartos menores.</td></tr>
    </tbody>
  </table>
  <a class="btn" href="https://www.booking.com/searchresults.pt-br.html?ss=Dongzhimen%2C+Pequim&checkin=2026-12-30&checkout=2027-01-06&group_adults=4&no_rooms=2" target="_blank" rel="noopener">Dongzhimen · preços</a>
  <a class="btn ghost" href="https://www.airbnb.com.br/s/Beijing--China/homes?checkin=2026-12-30&checkout=2027-01-06&adults=4" target="_blank" rel="noopener">Apartamentos inteiros</a>
  <p class="note">Dois critérios eliminam opções ruins em janeiro: aquecimento funcionando e no máximo 10 minutos a pé do metrô.</p>

  <h2>Hospedagem nas outras cidades<span class="sub">Os 3 melhores de cada cidade na pesquisa do Google Hotels (nota e volume de avaliações), sem preço — os preços mudam por data.</span></h2>
  <table>
    <thead><tr><th>Cidade</th><th>Hospedagem</th><th>Nota</th><th>Avaliações</th></tr></thead>
    <tbody>{"".join(linhas_hotel)}</tbody>
  </table>
  <p class="note">Levantamento feito para o grupo; preços e disponibilidade precisam ser conferidos nas datas exatas.</p>
</section>

<section role="tabpanel" id="tab-passeios">
  <h2>Todos os passeios, com ingresso de referência<span class="sub">Valores em yuan (¥) arredondados: são referência para orçamento, não cotação. Confirmar no site ou na bilheteria.</span></h2>
  <table>
    <thead><tr><th>Cidade</th><th>Atração</th><th>Tempo</th><th>Ingresso</th><th>Horário / observação</th><th></th></tr></thead>
    <tbody>{"".join(passeios)}</tbody>
  </table>
  <h2>Reservas que não podem escorregar</h2>
  <ul class="tight">
    <li><b>25/12/2026</b> — Cidade Proibida (visita 02/01), janela de 7 dias, com passaporte</li>
    <li><b>29/12/2026</b> — Museu Nacional (visita 05/01)</li>
    <li><b>~21/12/2026</b> — trem Pequim → Datong (06/01)</li>
    <li><b>~01/01/2027</b> — trem do bloco de natureza</li>
    <li><b>~10/01/2027</b> — trem Nanjing → Pequim (25/01)</li>
  </ul>
  <h2>Ingressos e reservas oficiais</h2>
  <a class="btn" href="https://intl.dpm.org.cn" target="_blank" rel="noopener">Cidade Proibida</a>
  <a class="btn ghost" href="http://en.chnmuseum.cn" target="_blank" rel="noopener">Museu Nacional</a>
  <a class="btn ghost" href="https://www.trip.com/things-to-do/" target="_blank" rel="noopener">Trip.com · ingressos</a>
</section>

<section role="tabpanel" id="tab-preparo">
  <h2>Antes de embarcar</h2>
  <ul class="tight">
    <li>Passaporte válido cobrindo a estada, com página em branco</li>
    <li><b>Alipay</b> e <b>WeChat Pay</b> configurados com cartão internacional, antes de sair do Brasil</li>
    <li><b>VPN</b> instalada e testada: Google, WhatsApp e Instagram são bloqueados na China</li>
    <li><b>eSIM</b> de dados e apps <b>Amap</b> (mapas) e <b>Didi</b> (táxi)</li>
    <li>Roupa de frio de verdade: −8 a −13 °C à noite em Pequim, Datong e Xi'an</li>
    <li>Dinheiro em espécie para mercados e templos; a China é quase toda digital</li>
  </ul>
  <h2>Ordem de grandeza do orçamento local</h2>
  <table>
    <thead><tr><th>Item</th><th>Referência</th></tr></thead>
    <tbody>
      <tr><td>Refeição em restaurante popular</td><td>¥25–50 por pessoa</td></tr>
      <tr><td>Metrô</td><td>¥3–7 por viagem</td></tr>
      <tr><td>Trem-bala (trecho de 3-5 h)</td><td>¥150–450</td></tr>
      <tr><td>Hotel 4★ por quarto/noite</td><td>¥400–800</td></tr>
      <tr><td>Ingressos por dia de museu/templo</td><td>¥50–150</td></tr>
    </tbody>
  </table>
  <p class="note">Valores de referência para planejamento; a cotação do yuan em 05/10/2026 era ¥1 = R$ 0,776.</p>
</section>

<footer>
  Página gerada para o grupo. Fotografias do Wikimedia Commons sob licenças livres (autores nos cartões).
  Mapa: OpenStreetMap. Esquema de posições: ilustrativo, não está em escala.
</footer>
</div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const CIDADES = {pontos_json};
const anel = ["pequim","datong","pingyao","xian","chongqing","changsha","xangai","hangzhou","nanjing","pequim"];
const variantes = [
  {{cor:"#2f6b4f", ids:["chongqing","zhangjiajie","changsha"], nome:"A · Zhangjiajie"}},
  {{cor:"#1f6f8b", ids:["changsha","guilin","xangai"], nome:"B · Guilin"}},
  {{cor:"#7a4b2a", ids:["hangzhou","huangshan","nanjing"], nome:"C · Huangshan"}}
];
const byId = Object.fromEntries(CIDADES.map(c => [c.id, c]));
const map = L.map('map', {{scrollWheelZoom:false}}).setView([33.5, 113], 4);
L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
  maxZoom: 18, attribution: '&copy; OpenStreetMap'
}}).addTo(map);

const coord = id => [byId[id].lat, byId[id].lon];
L.polyline(anel.map(coord), {{color:"#12263a", weight:3, opacity:.9}}).addTo(map);
variantes.forEach(v => L.polyline(v.ids.map(coord), {{color:v.cor, weight:2.5, dashArray:"7 6"}}).addTo(map));

CIDADES.forEach(c => {{
  const cor = c.id === "zhangjiajie" ? "#2f6b4f" : c.id === "guilin" ? "#1f6f8b" : c.id === "huangshan" ? "#7a4b2a" : "#12263a";
  const m = L.circleMarker([c.lat, c.lon], {{radius:8, color:cor, weight:3, fillColor:"#fff", fillOpacity:1}}).addTo(map);
  m.bindPopup(`<b>${{c.emoji}} ${{c.nome}}</b><br>${{c.noites}} noites · ${{c.datas}}<br>
    <a href="#" onclick="abrirCidade('${{c.id}}');return false;">ver detalhes →</a>`);
}});

function abrirCidade(id) {{
  document.querySelectorAll('nav.tabs button').forEach(b => b.setAttribute('aria-selected', b.dataset.tab === 'roteiro' ? 'true' : 'false'));
  document.querySelectorAll('section[role=tabpanel]').forEach(s => s.classList.toggle('on', s.id === 'tab-roteiro'));
  const d = document.getElementById('city-' + id);
  if (d) {{ d.open = true; d.scrollIntoView({{behavior:'smooth', block:'start'}}); }}
  map.closePopup();
}}

document.querySelectorAll('nav.tabs button').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('nav.tabs button').forEach(b => b.setAttribute('aria-selected', 'false'));
    btn.setAttribute('aria-selected', 'true');
    document.querySelectorAll('section[role=tabpanel]').forEach(s => s.classList.toggle('on', s.id === 'tab-' + btn.dataset.tab));
    if (btn.dataset.tab === 'roteiro') setTimeout(() => map.invalidateSize(), 60);
    window.scrollTo({{top: 0, behavior: 'smooth'}});
  }});
}});
</script>
</body>
</html>"""

    html = html.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    out = os.path.join(BASE, "china_guia.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("salvo:", out, round(os.path.getsize(out) / 1024 / 1024, 2), "MB")


DATA_IN = {"pequim": "2026-12-30", "datong": "2027-01-06", "pingyao": "2027-01-08",
           "xian": "2027-01-10", "chongqing": "2027-01-13", "changsha": "2027-01-15",
           "xangai": "2027-01-20", "hangzhou": "2027-01-23", "nanjing": "2027-01-24",
           "zhangjiajie": "2027-01-15", "guilin": "2027-01-17", "huangshan": "2027-01-23"}
DATA_OUT = {"pequim": "2027-01-06", "datong": "2027-01-08", "pingyao": "2027-01-10",
            "xian": "2027-01-13", "chongqing": "2027-01-15", "changsha": "2027-01-17",
            "xangai": "2027-01-23", "hangzhou": "2027-01-24", "nanjing": "2027-01-25",
            "zhangjiajie": "2027-01-18", "guilin": "2027-01-20", "huangshan": "2027-01-24"}

if __name__ == "__main__":
    main()
