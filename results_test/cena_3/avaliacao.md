# Avaliação da cena cena_3

Comparação do `result.json` com o `ground_truth.json` (o ground truth só é lido pelo avaliador).

## Número de caixas

No `result.json`: encontradas 3, reais 3: o número de caixas encontrado está certo.

## Parte 1 - Registo

Erro de cada câmara: E = T_gt⁻¹ · T_est; translação = norma da translação de E, rotação = ângulo da rotação de E (o mesmo de R_estᵀ R_gt).

| câmara | erro de translação (mm) | erro de rotação (°) |
|---|---|---|
| 000 | 0.00 | 0.000 |
| 001 | 0.52 | 0.007 |
| média (sem a 000) | 0.52 | 0.007 |
| máximo | 0.52 | 0.007 |

## Parte 2 - Segmentação

Para avaliar só a segmentação (sem os erros do registo), as nuvens foram juntadas com as poses verdadeiras e as Partes 2 e 3 correram sobre essa nuvem (em `partes_gt/`). Os pontos de cada caixa verdadeira são os que ficam dentro dela, com 5 mm de margem.

Caixas encontradas: 3, reais: 3 (3 conjuntos de pontos).

| caixa verdadeira | conjunto | pontos do conjunto | precisão | recall |
|---|---|---|---|---|
| 0 | 1 | 4540 | 0.997 | 0.685 |
| 1 | 0 | 6170 | 0.996 | 0.691 |
| 2 | 2 | 2260 | 0.990 | 0.739 |
| média | | | 0.994 | 0.705 |

## Parte 3 - Caixas

Erros de cada caixa verdadeira em relação à caixa estimada associada (maior IoU 3D), no referencial do mundo; o yaw e as dimensões têm em conta as simetrias da caixa. dL, dW, dH = estimado − verdadeiro.

### otimização (result.json)

| caixa verdadeira | caixa estimada | posição (mm) | altura z (mm) | yaw (°) | dL (mm) | dW (mm) | dH (mm) | IoU 3D |
|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 0.9 | 0.0 | 0.01 | -5.3 | 1.3 | -0.1 | 0.961 |
| 1 | 0 | 1.7 | 0.0 | 0.02 | 3.4 | -2.3 | -0.2 | 0.956 |
| 2 | 2 | 31.9 | -0.0 | 0.28 | -2.0 | -65.8 | 0.0 | 0.602 |

IoU 3D médio: **0.840** (uma caixa verdadeira sem caixa estimada conta com IoU 0).

### bounding box (partes/ajuste.npz)

| caixa verdadeira | caixa estimada | posição (mm) | altura z (mm) | yaw (°) | dL (mm) | dW (mm) | dH (mm) | IoU 3D |
|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 40.6 | 0.0 | 0.37 | -5.1 | -19.2 | 33.5 | 0.364 |
| 1 | 0 | 4.7 | 0.0 | 0.14 | 2.6 | 0.8 | 2.1 | 0.889 |
| 2 | 2 | 43.1 | 0.0 | 0.25 | 32.0 | -61.9 | 27.4 | 0.433 |

IoU 3D médio: **0.562** (uma caixa verdadeira sem caixa estimada conta com IoU 0).


## Extra - Fotometria

cor_000 = s · cor + b de cada imagem, em relação à imagem 000 (o verdadeiro vem do campo `photometry` do ground truth: s = s_000 / s_k, b = b_000 − s_000 · b_k / s_k):

| imagem | s estimado | s verdadeiro | erro de s | b estimado | b verdadeiro | erro de b |
|---|---|---|---|---|---|---|
| 000 | 1.000 | 1.000 | 0.000 | +0.000 | +0.000 | 0.000 |
| 001 | 1.065 | 1.066 | 0.001 | +0.129 | +0.129 | 0.000 |
| média (sem a 000) | | | 0.001 | | | 0.000 |

### Efeito na segmentação por cor (Nível 4)

A Parte 2 correu três vezes sobre a nuvem junta com as poses verdadeiras (em `partes_gt_fotometria/`), com as cores sem correção, com a correção estimada e com a correção verdadeira. Erro de cor = diferença média de cor (0 a 1) entre os pontos vistos por duas câmaras. Os conjuntos de pontos são só os da Parte 2 (clusters e grupos de cor, sem a geometria da Parte 3).

| cores | erro de cor | caixas estimadas | clusters separados por cor | conjuntos | precisão | recall | caixas sem conjunto |
|---|---|---|---|---|---|---|---|
| sem correção | 0.1575 | 3 de 3 | 0 de 2 | 2 | 0.785 | 0.718 | 1 |
| s e b estimados | 0.0224 | 3 de 3 | 1 de 2 | 3 | 0.992 | 0.702 | 0 |
| s e b verdadeiros | 0.0224 | 3 de 3 | 1 de 2 | 3 | 0.992 | 0.708 | 0 |
