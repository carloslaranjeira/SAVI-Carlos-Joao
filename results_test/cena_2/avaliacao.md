# Avaliação da cena cena_2

Comparação do `result.json` com o `ground_truth.json` (o ground truth só é lido pelo avaliador).

## Número de caixas

No `result.json`: encontradas 3, reais 3: o número de caixas encontrado está certo.

## Parte 1 - Registo

Erro de cada câmara: E = T_gt⁻¹ · T_est; translação = norma da translação de E, rotação = ângulo da rotação de E (o mesmo de R_estᵀ R_gt).

| câmara | erro de translação (mm) | erro de rotação (°) |
|---|---|---|
| 000 | 0.00 | 0.000 |

## Parte 2 - Segmentação

Para avaliar só a segmentação (sem os erros do registo), as nuvens foram juntadas com as poses verdadeiras e as Partes 2 e 3 correram sobre essa nuvem (em `partes_gt/`). Os pontos de cada caixa verdadeira são os que ficam dentro dela, com 5 mm de margem.

Caixas encontradas: 3, reais: 3 (3 conjuntos de pontos).

| caixa verdadeira | conjunto | pontos do conjunto | precisão | recall |
|---|---|---|---|---|
| 0 | 0 | 7325 | 0.999 | 0.732 |
| 1 | 1 | 3739 | 0.991 | 0.786 |
| 2 | 2 | 1808 | 0.961 | 0.800 |
| média | | | 0.984 | 0.773 |

## Parte 3 - Caixas

Erros de cada caixa verdadeira em relação à caixa estimada associada (maior IoU 3D), no referencial do mundo; o yaw e as dimensões têm em conta as simetrias da caixa. dL, dW, dH = estimado − verdadeiro.

### otimização (result.json)

| caixa verdadeira | caixa estimada | posição (mm) | altura z (mm) | yaw (°) | dL (mm) | dW (mm) | dH (mm) | IoU 3D |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 1.8 | 0.0 | 0.16 | -3.3 | -2.2 | -0.0 | 0.973 |
| 1 | 1 | 2.6 | -0.0 | 0.17 | -2.5 | -4.7 | 0.1 | 0.960 |
| 2 | 2 | 2.9 | -0.0 | 0.14 | -4.8 | -9.6 | 0.0 | 0.893 |

IoU 3D médio: **0.942** (uma caixa verdadeira sem caixa estimada conta com IoU 0).

### bounding box (partes/ajuste.npz)

| caixa verdadeira | caixa estimada | posição (mm) | altura z (mm) | yaw (°) | dL (mm) | dW (mm) | dH (mm) | IoU 3D |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 3.5 | 0.0 | 0.31 | -1.3 | -2.2 | 3.0 | 0.932 |
| 1 | 1 | 8.5 | -0.0 | 0.05 | -2.0 | -4.5 | 3.0 | 0.867 |
| 2 | 2 | 15.7 | -0.0 | 0.83 | -15.8 | -4.4 | 2.9 | 0.778 |

IoU 3D médio: **0.859** (uma caixa verdadeira sem caixa estimada conta com IoU 0).


## Extra - Fotometria

cor_000 = s · cor + b de cada imagem, em relação à imagem 000 (o verdadeiro vem do campo `photometry` do ground truth: s = s_000 / s_k, b = b_000 − s_000 · b_k / s_k):

| imagem | s estimado | s verdadeiro | erro de s | b estimado | b verdadeiro | erro de b |
|---|---|---|---|---|---|---|
| 000 | 1.000 | 1.000 | 0.000 | +0.000 | +0.000 | 0.000 |
