# Avaliação da cena cena_4

Comparação do `result.json` com o `ground_truth.json` (o ground truth só é lido pelo avaliador).

## Número de caixas

No `result.json`: encontradas 2, reais 2: o número de caixas encontrado está certo.

## Parte 1 - Registo

Erro de cada câmara: E = T_gt⁻¹ · T_est; translação = norma da translação de E, rotação = ângulo da rotação de E (o mesmo de R_estᵀ R_gt).

| câmara | erro de translação (mm) | erro de rotação (°) |
|---|---|---|
| 000 | 0.00 | 0.000 |
| 001 | 0.42 | 0.033 |
| 002 | 0.42 | 0.037 |
| 003 | 2.22 | 0.107 |
| média (sem a 000) | 1.02 | 0.059 |
| máximo | 2.22 | 0.107 |

## Parte 2 - Segmentação

Para avaliar só a segmentação (sem os erros do registo), as nuvens foram juntadas com as poses verdadeiras e as Partes 2 e 3 correram sobre essa nuvem (em `partes_gt/`). Os pontos de cada caixa verdadeira são os que ficam dentro dela, com 5 mm de margem.

Caixas encontradas: 2, reais: 2 (2 conjuntos de pontos).

| caixa verdadeira | conjunto | pontos do conjunto | precisão | recall |
|---|---|---|---|---|
| 0 | 1 | 6188 | 0.986 | 0.605 |
| 1 | 0 | 8403 | 0.988 | 0.703 |
| média | | | 0.987 | 0.654 |

## Parte 3 - Caixas

Erros de cada caixa verdadeira em relação à caixa estimada associada (maior IoU 3D), no referencial do mundo; o yaw e as dimensões têm em conta as simetrias da caixa. dL, dW, dH = estimado − verdadeiro.

### otimização (result.json)

| caixa verdadeira | caixa estimada | posição (mm) | altura z (mm) | yaw (°) | dL (mm) | dW (mm) | dH (mm) | IoU 3D |
|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 0.2 | 0.0 | 0.09 | 0.2 | 0.3 | 0.2 | 0.994 |
| 1 | 0 | 0.4 | 0.2 | 0.10 | 0.3 | -0.2 | -0.3 | 0.990 |

IoU 3D médio: **0.992** (uma caixa verdadeira sem caixa estimada conta com IoU 0).

### bounding box (partes/ajuste.npz)

| caixa verdadeira | caixa estimada | posição (mm) | altura z (mm) | yaw (°) | dL (mm) | dW (mm) | dH (mm) | IoU 3D |
|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 2.5 | 0.0 | 0.12 | 6.3 | 2.2 | 3.5 | 0.913 |
| 1 | 0 | 1.4 | -0.9 | 1.17 | 6.5 | 7.2 | 3.7 | 0.883 |

IoU 3D médio: **0.898** (uma caixa verdadeira sem caixa estimada conta com IoU 0).


## Extra - Fotometria

cor_000 = s · cor + b de cada imagem:

| imagem | s estimado | s verdadeiro | b estimado | b verdadeiro |
|---|---|---|---|---|
| 000 | 1.000 | 1.000 | +0.000 | +0.000 |
| 001 | 0.992 | 1.000 | +0.005 | +0.000 |
| 002 | 0.984 | 1.000 | +0.011 | +0.000 |
| 003 | 0.985 | 1.000 | +0.010 | +0.000 |
