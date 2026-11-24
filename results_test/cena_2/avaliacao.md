# Avaliação da cena cena_2

Comparação do `result.json` com o `ground_truth.json` (o ground truth só é lido pelo avaliador).

## Número de caixas

No `result.json`: encontradas 2, reais 2: o número de caixas encontrado está certo.

## Parte 1 - Registo

Erro de cada câmara: E = T_gt⁻¹ · T_est; translação = norma da translação de E, rotação = ângulo da rotação de E (o mesmo de R_estᵀ R_gt).

| câmara | erro de translação (mm) | erro de rotação (°) |
|---|---|---|
| 000 | 0.00 | 0.000 |
| 001 | 0.58 | 0.092 |
| 002 | 1.65 | 0.062 |
| média (sem a 000) | 1.12 | 0.077 |
| máximo | 1.65 | 0.092 |

## Parte 2 - Segmentação

Para avaliar só a segmentação (sem os erros do registo), as nuvens foram juntadas com as poses verdadeiras e as Partes 2 e 3 correram sobre essa nuvem (em `partes_gt/`). Os pontos de cada caixa verdadeira são os que ficam dentro dela, com 5 mm de margem.

Caixas encontradas: 2, reais: 2 (2 conjuntos de pontos).

| caixa verdadeira | conjunto | pontos do conjunto | precisão | recall |
|---|---|---|---|---|
| 0 | 0 | 6785 | 0.983 | 0.686 |
| 1 | 1 | 5856 | 0.996 | 0.671 |
| média | | | 0.990 | 0.678 |

## Parte 3 - Caixas

Erros de cada caixa verdadeira em relação à caixa estimada associada (maior IoU 3D), no referencial do mundo; o yaw e as dimensões têm em conta as simetrias da caixa. dL, dW, dH = estimado − verdadeiro.

### otimização (result.json)

| caixa verdadeira | caixa estimada | posição (mm) | altura z (mm) | yaw (°) | dL (mm) | dW (mm) | dH (mm) | IoU 3D |
|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 1.4 | -0.0 | 0.08 | 1.4 | -0.1 | -0.2 | 0.980 |
| 1 | 0 | 0.7 | -0.1 | 0.01 | 0.8 | 1.0 | -0.3 | 0.981 |

IoU 3D médio: **0.980** (uma caixa verdadeira sem caixa estimada conta com IoU 0).

### bounding box (partes/ajuste.npz)

| caixa verdadeira | caixa estimada | posição (mm) | altura z (mm) | yaw (°) | dL (mm) | dW (mm) | dH (mm) | IoU 3D |
|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 7.0 | -0.0 | 0.31 | 0.3 | 0.1 | 1.9 | 0.851 |
| 1 | 0 | 6.4 | -0.1 | 0.02 | 10.2 | 1.1 | 2.5 | 0.861 |

IoU 3D médio: **0.856** (uma caixa verdadeira sem caixa estimada conta com IoU 0).


## Extra - Fotometria

cor_000 = s · cor + b de cada imagem:

| imagem | s estimado | s verdadeiro | b estimado | b verdadeiro |
|---|---|---|---|---|
| 000 | 1.000 | 1.000 | +0.000 | +0.000 |
| 001 | 0.996 | 1.000 | +0.002 | +0.000 |
| 002 | 0.991 | 1.000 | +0.005 | +0.000 |
