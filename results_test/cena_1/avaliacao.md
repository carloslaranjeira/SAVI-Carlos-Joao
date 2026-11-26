# Avaliação da cena cena_1

Comparação do `result.json` com o `ground_truth.json` (o ground truth só é lido pelo avaliador).

## Número de caixas

No `result.json`: encontradas 2, reais 2: o número de caixas encontrado está certo.

## Parte 1 - Registo

Erro de cada câmara: E = T_gt⁻¹ · T_est; translação = norma da translação de E, rotação = ângulo da rotação de E (o mesmo de R_estᵀ R_gt).

| câmara | erro de translação (mm) | erro de rotação (°) |
|---|---|---|
| 000 | 0.00 | 0.000 |
| 001 | 2.41 | 0.045 |
| média (sem a 000) | 2.41 | 0.045 |
| máximo | 2.41 | 0.045 |

## Parte 2 - Segmentação

Para avaliar só a segmentação (sem os erros do registo), as nuvens foram juntadas com as poses verdadeiras e as Partes 2 e 3 correram sobre essa nuvem (em `partes_gt/`). Os pontos de cada caixa verdadeira são os que ficam dentro dela, com 5 mm de margem.

Caixas encontradas: 2, reais: 2 (2 conjuntos de pontos).

| caixa verdadeira | conjunto | pontos do conjunto | precisão | recall |
|---|---|---|---|---|
| 0 | 1 | 7096 | 0.987 | 0.717 |
| 1 | 0 | 13018 | 0.992 | 0.691 |
| média | | | 0.989 | 0.704 |

## Parte 3 - Caixas

Erros de cada caixa verdadeira em relação à caixa estimada associada (maior IoU 3D), no referencial do mundo; o yaw e as dimensões têm em conta as simetrias da caixa. dL, dW, dH = estimado − verdadeiro.

### otimização (result.json)

| caixa verdadeira | caixa estimada | posição (mm) | altura z (mm) | yaw (°) | dL (mm) | dW (mm) | dH (mm) | IoU 3D |
|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 1.8 | 0.0 | 0.10 | -3.6 | 1.4 | -0.0 | 0.976 |
| 1 | 0 | 1.7 | 0.0 | 0.01 | -2.9 | 1.6 | -0.5 | 0.971 |

IoU 3D médio: **0.974** (uma caixa verdadeira sem caixa estimada conta com IoU 0).

### bounding box (partes/ajuste.npz)

| caixa verdadeira | caixa estimada | posição (mm) | altura z (mm) | yaw (°) | dL (mm) | dW (mm) | dH (mm) | IoU 3D |
|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 4.9 | 0.0 | 0.22 | -2.4 | 5.9 | 2.4 | 0.918 |
| 1 | 0 | 1.6 | 0.0 | 0.15 | 0.9 | 6.1 | 0.7 | 0.932 |

IoU 3D médio: **0.925** (uma caixa verdadeira sem caixa estimada conta com IoU 0).


## Extra - Fotometria

cor_000 = s · cor + b de cada imagem, em relação à imagem 000 (o verdadeiro vem do campo `photometry` do ground truth: s = s_000 / s_k, b = b_000 − s_000 · b_k / s_k):

| imagem | s estimado | s verdadeiro | erro de s | b estimado | b verdadeiro | erro de b |
|---|---|---|---|---|---|---|
| 000 | 1.000 | 1.000 | 0.000 | +0.000 | +0.000 | 0.000 |
| 001 | 0.999 | 1.000 | 0.001 | +0.000 | +0.000 | 0.000 |
| média (sem a 000) | | | 0.001 | | | 0.000 |
