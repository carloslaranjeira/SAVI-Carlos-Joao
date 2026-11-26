# Avaliação da cena cena_5

Comparação do `result.json` com o `ground_truth.json` (o ground truth só é lido pelo avaliador).

## Número de caixas

No `result.json`: encontradas 1, reais 1: o número de caixas encontrado está certo.

## Parte 1 - Registo

Erro de cada câmara: E = T_gt⁻¹ · T_est; translação = norma da translação de E, rotação = ângulo da rotação de E (o mesmo de R_estᵀ R_gt).

| câmara | erro de translação (mm) | erro de rotação (°) |
|---|---|---|
| 000 | 0.00 | 0.000 |
| 001 | 1.90 | 0.037 |
| 002 | 1.48 | 0.035 |
| média (sem a 000) | 1.69 | 0.036 |
| máximo | 1.90 | 0.037 |

## Parte 2 - Segmentação

Para avaliar só a segmentação (sem os erros do registo), as nuvens foram juntadas com as poses verdadeiras e as Partes 2 e 3 correram sobre essa nuvem (em `partes_gt/`). Os pontos de cada caixa verdadeira são os que ficam dentro dela, com 5 mm de margem.

Caixas encontradas: 1, reais: 1 (1 conjuntos de pontos).

| caixa verdadeira | conjunto | pontos do conjunto | precisão | recall |
|---|---|---|---|---|
| 0 | 0 | 10046 | 0.992 | 0.683 |
| média | | | 0.992 | 0.683 |

## Parte 3 - Caixas

Erros de cada caixa verdadeira em relação à caixa estimada associada (maior IoU 3D), no referencial do mundo; o yaw e as dimensões têm em conta as simetrias da caixa. dL, dW, dH = estimado − verdadeiro.

### otimização (result.json)

| caixa verdadeira | caixa estimada | posição (mm) | altura z (mm) | yaw (°) | dL (mm) | dW (mm) | dH (mm) | IoU 3D |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 0.8 | -0.0 | 0.16 | -1.4 | -1.1 | -0.3 | 0.985 |

IoU 3D médio: **0.985** (uma caixa verdadeira sem caixa estimada conta com IoU 0).

### bounding box (partes/ajuste.npz)

| caixa verdadeira | caixa estimada | posição (mm) | altura z (mm) | yaw (°) | dL (mm) | dW (mm) | dH (mm) | IoU 3D |
|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 4.9 | -0.0 | 0.24 | -0.4 | 5.2 | 2.8 | 0.911 |

IoU 3D médio: **0.911** (uma caixa verdadeira sem caixa estimada conta com IoU 0).


## Extra - Fotometria

cor_000 = s · cor + b de cada imagem, em relação à imagem 000 (o verdadeiro vem do campo `photometry` do ground truth: s = s_000 / s_k, b = b_000 − s_000 · b_k / s_k):

| imagem | s estimado | s verdadeiro | erro de s | b estimado | b verdadeiro | erro de b |
|---|---|---|---|---|---|---|
| 000 | 1.000 | 1.000 | 0.000 | +0.000 | +0.000 | 0.000 |
| 001 | 1.164 | 1.168 | 0.004 | +0.139 | +0.137 | 0.001 |
| 002 | 0.807 | 0.808 | 0.001 | +0.109 | +0.108 | 0.001 |
| média (sem a 000) | | | 0.003 | | | 0.001 |

### Efeito na segmentação por cor (Nível 4)

A Parte 2 correu três vezes sobre a nuvem junta com as poses verdadeiras (em `partes_gt_fotometria/`), com as cores sem correção, com a correção estimada e com a correção verdadeira. Erro de cor = diferença média de cor (0 a 1) entre os pontos vistos por duas câmaras. Os conjuntos de pontos são só os da Parte 2 (clusters e grupos de cor, sem a geometria da Parte 3).

| cores | erro de cor | caixas estimadas | clusters separados por cor | conjuntos | precisão | recall | caixas sem conjunto |
|---|---|---|---|---|---|---|---|
| sem correção | 0.1533 | 1 de 1 | 0 de 1 | 1 | 0.992 | 0.683 | 0 |
| s e b estimados | 0.0146 | 1 de 1 | 0 de 1 | 1 | 0.992 | 0.682 | 0 |
| s e b verdadeiros | 0.0147 | 1 de 1 | 0 de 1 | 1 | 0.992 | 0.682 | 0 |
