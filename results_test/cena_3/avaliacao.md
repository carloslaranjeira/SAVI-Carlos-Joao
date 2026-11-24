# Avaliação da cena cena_3

Comparação do `result.json` com o `ground_truth.json` (o ground truth só é lido pelo avaliador).

## Número de caixas

No `result.json`: encontradas 3, reais 3: o número de caixas encontrado está certo.

## Parte 1 - Registo

Erro de cada câmara: E = T_gt⁻¹ · T_est; translação = norma da translação de E, rotação = ângulo da rotação de E (o mesmo de R_estᵀ R_gt).

| câmara | erro de translação (mm) | erro de rotação (°) |
|---|---|---|
| 000 | 0.00 | 0.000 |
| 001 | 0.07 | 0.014 |
| média (sem a 000) | 0.07 | 0.014 |
| máximo | 0.07 | 0.014 |

## Parte 2 - Segmentação

Para avaliar só a segmentação (sem os erros do registo), as nuvens foram juntadas com as poses verdadeiras e as Partes 2 e 3 correram sobre essa nuvem (em `partes_gt/`). Os pontos de cada caixa verdadeira são os que ficam dentro dela, com 5 mm de margem.

Caixas encontradas: 2, reais: 3 (2 conjuntos de pontos).

| caixa verdadeira | conjunto | pontos do conjunto | precisão | recall |
|---|---|---|---|---|
| 0 | 0 | 2273 | 0.978 | 0.711 |
| 2 | 1 | 5243 | 0.578 | 0.703 |
| média | | | 0.778 | 0.707 |

Caixas verdadeiras sem conjunto: 1.

## Parte 3 - Caixas

Erros de cada caixa verdadeira em relação à caixa estimada associada (maior IoU 3D), no referencial do mundo; o yaw e as dimensões têm em conta as simetrias da caixa. dL, dW, dH = estimado − verdadeiro.

### otimização (result.json)

| caixa verdadeira | caixa estimada | posição (mm) | altura z (mm) | yaw (°) | dL (mm) | dW (mm) | dH (mm) | IoU 3D |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2.9 | -0.0 | 2.60 | -2.4 | 4.5 | -0.0 | 0.918 |
| 1 | 2 | 5.3 | -0.0 | 2.03 | -2.4 | 10.6 | -0.2 | 0.883 |
| 2 | 1 | 2.7 | -0.0 | 0.14 | -3.2 | 4.0 | -0.0 | 0.937 |

IoU 3D médio: **0.913** (uma caixa verdadeira sem caixa estimada conta com IoU 0).

### bounding box (partes/ajuste.npz)

| caixa verdadeira | caixa estimada | posição (mm) | altura z (mm) | yaw (°) | dL (mm) | dW (mm) | dH (mm) | IoU 3D |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 19.1 | -0.0 | 0.51 | -2.0 | 15.3 | 20.5 | 0.594 |
| 1 | 2 | 18.0 | -0.0 | 1.38 | 16.7 | -2.6 | 20.1 | 0.607 |
| 2 | 1 | 3.3 | -0.0 | 0.39 | 1.5 | 2.1 | 3.5 | 0.894 |

IoU 3D médio: **0.698** (uma caixa verdadeira sem caixa estimada conta com IoU 0).


## Extra - Fotometria

cor_000 = s · cor + b de cada imagem:

| imagem | s estimado | s verdadeiro | b estimado | b verdadeiro |
|---|---|---|---|---|
| 000 | 1.000 | 1.000 | +0.000 | +0.000 |
| 001 | 0.991 | 1.000 | +0.006 | +0.000 |
