# Avaliação da cena cena_1

Comparação do `result.json` com o `ground_truth.json` (o ground truth só é lido pelo avaliador).

## Número de caixas

No `result.json`: encontradas 4, reais 4: o número de caixas encontrado está certo.

## Parte 1 - Registo

Erro de cada câmara: E = T_gt⁻¹ · T_est; translação = norma da translação de E, rotação = ângulo da rotação de E (o mesmo de R_estᵀ R_gt).

| câmara | erro de translação (mm) | erro de rotação (°) |
|---|---|---|
| 000 | 0.00 | 0.000 |
| 001 | 0.10 | 0.007 |
| 002 | 0.24 | 0.010 |
| média (sem a 000) | 0.17 | 0.009 |
| máximo | 0.24 | 0.010 |

## Parte 2 - Segmentação

Para avaliar só a segmentação (sem os erros do registo), as nuvens foram juntadas com as poses verdadeiras e as Partes 2 e 3 correram sobre essa nuvem (em `partes_gt/`). Os pontos de cada caixa verdadeira são os que ficam dentro dela, com 5 mm de margem.

Caixas encontradas: 4, reais: 4 (4 conjuntos de pontos).

| caixa verdadeira | conjunto | pontos do conjunto | precisão | recall |
|---|---|---|---|---|
| 0 | 1 | 4243 | 0.987 | 0.677 |
| 1 | 0 | 9687 | 0.992 | 0.707 |
| 2 | 3 | 6430 | 0.990 | 0.652 |
| 3 | 2 | 6457 | 0.992 | 0.726 |
| média | | | 0.990 | 0.691 |

## Parte 3 - Caixas

Erros de cada caixa verdadeira em relação à caixa estimada associada (maior IoU 3D), no referencial do mundo; o yaw e as dimensões têm em conta as simetrias da caixa. dL, dW, dH = estimado − verdadeiro.

### otimização (result.json)

| caixa verdadeira | caixa estimada | posição (mm) | altura z (mm) | yaw (°) | dL (mm) | dW (mm) | dH (mm) | IoU 3D |
|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 0.9 | -0.0 | 0.13 | -1.7 | -0.2 | 0.0 | 0.987 |
| 1 | 0 | 0.8 | 0.0 | 0.14 | 1.8 | -0.0 | -0.4 | 0.985 |
| 2 | 3 | 0.8 | -0.0 | 0.04 | -1.5 | -0.1 | 0.1 | 0.990 |
| 3 | 2 | 1.2 | 0.1 | 0.23 | -2.3 | -0.4 | 0.2 | 0.974 |

IoU 3D médio: **0.984** (uma caixa verdadeira sem caixa estimada conta com IoU 0).

### bounding box (partes/ajuste.npz)

| caixa verdadeira | caixa estimada | posição (mm) | altura z (mm) | yaw (°) | dL (mm) | dW (mm) | dH (mm) | IoU 3D |
|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 2.4 | -0.0 | 0.34 | 1.6 | 4.2 | 3.8 | 0.904 |
| 1 | 0 | 2.7 | 0.0 | 0.39 | 3.1 | 5.4 | 2.6 | 0.925 |
| 2 | 3 | 3.6 | -0.0 | 0.40 | 3.4 | 4.2 | 3.2 | 0.925 |
| 3 | 2 | 4.0 | -0.6 | 0.56 | 1.1 | 6.1 | 2.5 | 0.879 |

IoU 3D médio: **0.908** (uma caixa verdadeira sem caixa estimada conta com IoU 0).


## Extra - Fotometria

cor_000 = s · cor + b de cada imagem:

| imagem | s estimado | s verdadeiro | b estimado | b verdadeiro |
|---|---|---|---|---|
| 000 | 1.000 | 1.000 | +0.000 | +0.000 |
| 001 | 0.993 | 1.000 | +0.004 | +0.000 |
| 002 | 0.986 | 1.000 | +0.008 | +0.000 |
