# Guia da viagem à China — 30 dias

Página estática do roteiro: mapa do trajeto, sanfona por cidade, passagens aéreas, trens,
hospedagens com rateio de valores e lista de passeios.

Publicada no GitHub Pages: **https://SEU-USUARIO.github.io/china-guia/**

## Estrutura

```
index.html                  ← página final (é o que o GitHub Pages publica)
src/build_guia.py           ← dados do roteiro (cidades, atrações, dicas, hotéis, trens)
src/build_guia2.py          ← gerador do HTML (layout, CSS, JS, cálculos)
data/hoteis_cidades.json    ← hotéis levantados por cidade
img/                        ← fotos e créditos
```

`index.html` é **gerado**. Não edite à mão: rode o build.

## Como atualizar

1. Mudar o conteúdo em `src/build_guia.py` (roteiro, atrações, dicas) ou em `src/build_guia2.py` (textos das abas, layout)
2. Rodar o build:

```bash
cd china-guia
python3 src/build_guia2.py      # escreve index.html
```

3. Publicar:

```bash
git add -A
git commit -m "atualiza: <o que mudou>"
git push
```

O GitHub Pages republica sozinho em cerca de 30 segundos, no mesmo endereço.

## Requisitos

- Python 3 com `Pillow` (`pip install pillow`)
- As imagens precisam ter cabeçalho JFIF ou EXIF: o `python-docx` e alguns visualizadores
  rejeitam JPEG que começa em `FFD8FFDB` (tabela de quantização) ou `FFD8FFE2` (perfil ICC).
  Se aparecer imagem nova quebrada, rode:

```bash
python3 - <<'EOF'
JFIF = bytes.fromhex('FFE000104A46494600010100000100010000')
for f in ['img/nova.jpg']:
    b = open(f,'rb').read()
    if b[:2] == b'\xff\xd8' and b[2:4] not in (b'\xff\xe0', b'\xff\xe1'):
        open(f,'wb').write(b[:2] + JFIF + b[2:])
EOF
```

## O que é estático e o que vem da rede

- **Estático**: todas as fotos (embutidas em base64), textos, tabelas, cálculo de valores
- **Da rede**: tiles do OpenStreetMap (mapa), Leaflet (CDN) e os links de reserva
- Os valores digitados no site ficam salvos no navegador de cada pessoa (`localStorage`),
  não são compartilhados entre os viajantes

## Créditos das imagens

Wikimedia Commons, sob licenças livres. Autores indicados em cada cartão;
a foto de capa é de Steven Sun (CC BY-SA 4.0).
