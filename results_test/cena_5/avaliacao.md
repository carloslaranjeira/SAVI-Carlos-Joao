# Avaliação da cena cena_5

Comparação do `result.json` com o `ground_truth.json` (o ground truth só é lido pelo avaliador).

## Número de caixas

No `result.json`: encontradas 1, reais 1: o número de caixas encontrado está certo.

## Parte 1 - Registo

Erro de cada câmara: E = T_gt⁻¹ · T_est; translação = norma da translação de E, rotação = ângulo da rotação de E (o mesmo de R_estᵀ R_gt).

| câmara | erro de translação (mm) | erro de rotação (°) |
|---|---|---|
| 000 | 0.00 | 0.000 |

## Parte 2 - Segmentação

Para avaliar só a segmentação (sem os erros do registo), as nuvens foram juntadas com as poses verdadeiras e as Partes 2 e 3 correram sobre essa nuvem (em `partes_gt/`). Os pontos de cada caixa verdadeira são os que ficam dentro dela, com 5 mm de margem.

Caixas encontradas: 1, reais: 1 (1 conjuntos de pontos).

| caixa verdadeira | conjunto | pontos do conjunto | precisão | recall |
|---|---|---|---|---|
| 0 | 0 | 4133 | 0.998 | 0.802 |
| média | | | 0.998 | 0.802 |

## Parte 3 - Caixas

Erros de cada caixa verdadeira em relação à caixa estimada associada (maior IoU 3D), no referencial do mundo; o yaw e as dimensões têm em conta as simetrias da caixa. dL, dW, dH = estimado − verdadeiro.

### otimização (result.json)

| caixa verdadeira | caixa estimada | posição (mm) | altura z (mm) | yaw (°) | dL (mm) | dW (mm) | dH (mm) | IoU 3D |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0.2 | 0.0 | 0.12 | -0.5 | -0.7 | -0.1 | 0.991 |

IoU 3D médio: **0.991** (uma caixa verdadeira sem caixa estimada conta com IoU 0).

### bounding box (partes/ajuste.npz)

| caixa verdadeira | caixa estimada | posição (mm) | altura z (mm) | yaw (°) | dL (mm) | dW (mm) | dH (mm) | IoU 3D |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 7.5 | 0.0 | 0.99 | -4.2 | -1.9 | 3.0 | 0.863 |

IoU 3D médio: **0.863** (uma caixa verdadeira sem caixa estimada conta com IoU 0).


## Extra - Fotometria

cor_000 = s · cor + b de cada imagem:

| imagem | s estimado | s verdadeiro | b estimado | b verdadeiro |
|---|---|---|---|---|
| 000 | 1.000 | 1.000 | +0.000 | +0.000 |
