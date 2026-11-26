#!/usr/bin/env python3
"""SAVIBoxes - Trabalho 1 de SAVI. RESULTADOS DO README: reescreve a secção "Resultados do teste".

    python savi/resultados_readme.py                       # results_test/ -> README.md e docs/teste/
    python savi/resultados_readme.py --results results_test --scenes test

O README.md tem duas partes:
    - uma parte fixa (abordagem de cada parte, respostas às questões, dificuldades), escrita à mão;
    - a secção "Resultados do teste", entre as marcas <!-- RESULTADOS:INICIO --> e
      <!-- RESULTADOS:FIM -->, que é escrita por este ficheiro a partir do que o run_test.py gravou em
      results_test/<cena>/ (result.json, partes/ e, se a cena tiver ground truth, avaliacao.md).
O run_test.py chama-o no fim. As figuras ficam em docs/teste/ (apagadas e feitas de novo em cada teste).

Sem ground truth (cenas do dia da apresentação), não há erros: a secção mostra as caixas estimadas, as
figuras e o s e o b estimados. Com ground truth, mostra também as tabelas de erros do avaliador.
Este ficheiro não corre nenhuma parte: só lê os resultados gravados (e as nuvens da cena, para as figuras).
"""

import argparse
import datetime
import json
import re
import sys
import traceback
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt   # noqa: E402
import numpy as np                # noqa: E402

FOLDER = Path(__file__).resolve().parent.parent          # pasta principal do trabalho
sys.path.insert(0, str(FOLDER / "savi"))
sys.path.insert(0, str(FOLDER / "simulator"))

README = FOLDER / "README.md"
FIGURES = FOLDER / "docs" / "teste"                     # figuras desta secção (só do último teste)
START, END = "<!-- RESULTADOS:INICIO -->", "<!-- RESULTADOS:FIM -->"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]    # otimização, bounding box, ...
INK, MUTED, GRID = "#1f1f1e", "#6b6a64", "#e6e5e0"
GROUP_COLORS = np.array([[0.9, 0.1, 0.1], [0.1, 0.4, 0.9], [0.1, 0.7, 0.2], [0.95, 0.6, 0.0], [0.6, 0.2, 0.8],
                         [0.0, 0.7, 0.7]])
plt.rcParams.update({"font.size": 10, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED,
                     "ytick.color": MUTED, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.titlesize": 11,
                     "legend.frameon": False, "savefig.dpi": 110, "savefig.bbox": "tight"})


# #####################################################################################################
# 1. LER OS RESULTADOS DE UMA CENA
# #####################################################################################################
def natural_key(path):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", path.name)]


def md_table(text, header):
    """Linhas (listas de células) da primeira tabela Markdown depois do título `header` (sem o cabeçalho)."""
    if header not in text:
        return []
    rows, started = [], False
    for line in text.split(header, 1)[1].splitlines():
        if line.startswith("|"):
            started = True
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not set(cells[0]) <= set("-"):
                rows.append(cells)
        elif started:
            break
    return rows[1:]


def read_scene(out, scenes_dir, known):
    """Tudo o que a secção precisa de uma cena, lido de results_test/<cena>/ (e da pasta da cena)."""
    from avaliador import load_ground_truth, true_exposures
    from comum import OUTPUT_FOLDER
    from parte1_registo import load_registration
    parts = out / OUTPUT_FOLDER
    r1 = load_registration(parts)
    scene_folder = Path(r1["scene_folder"])
    if not scene_folder.exists() and scenes_dir is not None:      # pasta movida: procura pelo nome
        scene_folder = scenes_dir / out.name
    r1["scene_folder"] = scene_folder
    result = json.loads((out / "result.json").read_text(encoding="utf-8"))
    report = (out / "avaliacao.md").read_text(encoding="utf-8") if (out / "avaliacao.md").exists() else ""
    gt = load_ground_truth(scene_folder) if scene_folder.exists() else None
    photo_path = parts / "fotometria.json"
    photometry = json.loads(photo_path.read_text(encoding="utf-8")) if photo_path.exists() else None
    real = known.get(out.name)
    found = re.search(r"encontradas (\d+), reais (\d+)", report)
    if found:
        real = int(found.group(2))
    elif gt is not None:
        real = len(gt["boxes"])
    return {"name": out.name, "out": out, "parts": parts, "r1": r1, "result": result, "report": report,
            "gt": gt, "photometry": photometry, "real": real, "true_exposures": true_exposures(gt) if gt else {},
            "images": len(r1["images"]), "registered": len(r1["registered"])}


def iou_of(report, method):
    m = re.search(re.escape(f"### {method}") + r".*?IoU 3D médio: \*\*([\d.]+)\*\*", report, re.S)
    return float(m.group(1)) if m else None


def exposure_changes(s):
    """A cena tem mudanças de exposição: pelo ground truth, se o houver, senão pelo s e b estimados."""
    if s["true_exposures"]:
        return any(abs(sv - 1) > 1e-6 or abs(bv) > 1e-6 for sv, bv in s["true_exposures"].values())
    rows = (s["photometry"] or {}).get("imagens", [])
    return any(abs(r["s"] - 1) > 0.03 or abs(r["b"]) > 0.02 for r in rows)


# #####################################################################################################
# 2. FIGURAS (docs/teste/)
# #####################################################################################################
def save(fig, name):
    fig.savefig(FIGURES / name)
    plt.close(fig)
    return f"docs/teste/{name}"


def render(points, colors, view, size=(760, 520), f=700, voxel=0.008):
    from generate_figures import draw_points            # código do professor (figuras do enunciado)
    return np.clip(draw_points(points, colors, view, f, size[0], size[1], voxel=voxel), 0, 1)


def image_grid(images, titles, columns, name, width=12.0):
    rows = int(np.ceil(len(images) / columns))
    h, w = images[0].shape[:2]
    fig, axes = plt.subplots(rows, columns, figsize=(width, (width / columns) * h / w * rows + 0.45 * rows),
                             squeeze=False)
    for ax in axes.ravel():
        ax.set_axis_off()
    for ax, image, title in zip(axes.ravel(), images, titles):
        ax.imshow(image)
        ax.set_title(title, color=INK, fontsize=10)
    fig.tight_layout(pad=0.4)
    return save(fig, name)


def figure_scenes(scenes):
    """A primeira imagem a cores de cada cena."""
    import cv2
    images = []
    for s in scenes:
        path = s["r1"]["scene_folder"] / "rgb" / f"{s['r1']['images'][0]}.png"
        bgr = cv2.imdecode(np.fromfile(str(path), np.uint8), cv2.IMREAD_COLOR)
        images.append(bgr[..., ::-1] / 255.0)
    return image_grid(images, [f"{s['name']} ({s['images']} {'imagem' if s['images'] == 1 else 'imagens'})" for s in scenes], min(len(scenes), 3),
                      "cenas.png")


def figure_iou(scenes):
    rows = [(s["name"], iou_of(s["report"], "otimização"), iou_of(s["report"], "bounding box")) for s in scenes]
    rows = [r for r in rows if r[1] is not None]
    if not rows:
        return None
    x = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(max(5.0, 1.3 * len(rows) + 2), 3.4))
    ax.bar(x - 0.2, [r[1] for r in rows], 0.38, color=SERIES[0], label="otimização")
    ax.bar(x + 0.2, [r[2] or 0 for r in rows], 0.38, color=SERIES[1], label="bounding box")
    for xi, r in zip(x, rows):
        ax.text(xi - 0.2, r[1] + 0.01, f"{r[1]:.3f}", ha="center", fontsize=8, color=INK)
    ax.set_xticks(x, [r[0] for r in rows])
    ax.set_ylabel("IoU 3D médio")
    ax.set_ylim(0, 1.08)
    ax.grid(axis="x", visible=False)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2)
    return save(fig, "iou.png")


def table_frame_clouds(s):
    """Nuvem agregada (cores corrigidas pela fotometria) e câmara de cada ponto, no referencial da mesa da
    Parte 2 (origem no centro do tampo, z para cima), e os dados da Parte 2."""
    from comum import load_scene, transform_points
    from extra_fotometria import load_corrected_scene
    from parte1_registo import aggregate
    from parte2_segmentacao import load_objects, load_segmentation
    scene = load_corrected_scene(load_scene(s["r1"]["scene_folder"]), s["parts"])
    cloud, cam = aggregate(scene, s["r1"]["T_cams"], s["r1"]["registered"])
    table, _, _ = load_objects(s["parts"])
    T = np.linalg.inv(table.T_camera0_table)
    return scene, table, T, cloud, cam, load_segmentation(s["parts"]), transform_points


def segment_colors(seg):
    """Uma cor por conjunto (cluster e, nos clusters separados pela cor, grupo de cor)."""
    labels, n = np.zeros(len(seg.points), int), 0
    for k in sorted(seg.boxes_per_cluster):
        mine = np.flatnonzero(seg.clusters == k)
        groups = seg.color_groups.get(k)
        groups = np.zeros(len(mine), int) if groups is None else groups
        for g in np.unique(groups):
            labels[mine[groups == g]] = n
            n += 1
    return GROUP_COLORS[labels % len(GROUP_COLORS)]


def figures_clouds(scenes):
    """Por cena: nuvem agregada (cor dos pixels), uma cor por câmara e objetos isolados (Parte 2); com ground
    truth, também a nuvem estimada sobre a verdadeira, de perto."""
    from avaliador import true_camera_poses
    from generate_figures import look_at
    from parte1_registo import aggregate
    from visualizacao import CAMERA_COLORS
    view = look_at((1.25, -1.45, 1.05), (-0.05, 0.1, 0.0))          # a vista das figuras do enunciado
    close = look_at((0.55, -0.65, 0.5), (0.0, 0.0, 0.08))
    clouds, cloud_titles, segs, seg_titles, overlays, overlay_titles = [], [], [], [], [], []
    for s in scenes:
        try:
            scene, table, T, cloud, cam, seg, transform_points = table_frame_clouds(s)
            p = transform_points(T, np.asarray(cloud.points))
            clouds += [render(p, np.asarray(cloud.colors), view),
                       render(p, np.asarray(CAMERA_COLORS)[cam % len(CAMERA_COLORS)], view)]
            cloud_titles += [f"{s['name']}: nuvem agregada", f"{s['name']}: uma cor por câmara"]
            rest = transform_points(T, np.asarray(cloud.voxel_down_sample(0.006).points))
            segs.append(render(np.vstack([rest, seg.points]),
                               np.vstack([np.full((len(rest), 3), 0.78), segment_colors(seg)]), view, voxel=0.006))
            n = len(np.unique(segment_colors(seg), axis=0))
            seg_titles.append(f"{s['name']}: {n} {'conjunto' if n == 1 else 'conjuntos'} de pontos")
            if s["gt"] is not None:
                true_cloud, _ = aggregate(scene, true_camera_poses(scene, s["gt"]))
                est, tru = cloud.voxel_down_sample(0.003), true_cloud.voxel_down_sample(0.003)
                pts = np.vstack([transform_points(T, np.asarray(tru.points)), transform_points(T, np.asarray(est.points))])
                col = np.vstack([np.tile([0.1, 0.7, 0.2], (len(tru.points), 1)),
                                 np.tile([0.9, 0.1, 0.1], (len(est.points), 1))])
                order = np.random.default_rng(0).permutation(len(pts))
                overlays.append(render(pts[order], col[order], close, voxel=0.003))
                overlay_titles.append(s["name"])
        except Exception as error:
            print(f"  (figuras da nuvem de {s['name']} não feitas: {error})")
    out = {}
    if clouds:
        out["nuvens"] = image_grid(clouds, cloud_titles, 2, "parte1_nuvens.png")
    if overlays:
        out["sobreposicao"] = image_grid(overlays, overlay_titles, min(len(overlays), 3), "parte1_sobreposicao.png")
    if segs:
        out["segmentacao"] = image_grid(segs, seg_titles, min(len(segs), 2), "parte2_segmentacao.png")
    return out


def gt_params_in_table(s, table):
    """Caixas verdadeiras no referencial da mesa da Parte 2: [x, y, yaw, length, width, height, z]."""
    from avaliador import box_in_world, world_params
    T = np.linalg.inv(table.T_camera0_table)
    return np.array([world_params(box_in_world(T @ np.asarray(b["T_camera0_box"]), b["length"], b["width"],
                                               b["height"])) for b in s["gt"]["boxes"]])


def figure_top_views(scenes):
    """Vista de cima de cada cena (referencial da mesa): pontos dos objetos, ground truth (se houver),
    bounding box e otimização."""
    from parte2_segmentacao import load_objects, load_segmentation
    from parte3_ajuste import draw_rects, load_fit
    columns = min(len(scenes), 3)
    rows = int(np.ceil(len(scenes) / columns))
    fig, axes = plt.subplots(rows, columns, figsize=(4.3 * columns, 3.6 * rows), squeeze=False)
    for ax in axes.ravel():
        ax.set_axis_off()
    for ax, s in zip(axes.ravel(), scenes):
        try:
            table, _, _ = load_objects(s["parts"])
            seg, fit = load_segmentation(s["parts"]), load_fit(s["parts"])
            ax.set_axis_on()
            sel = np.random.default_rng(0).choice(len(seg.points), min(len(seg.points), 10000), replace=False)
            ax.scatter(seg.points[sel, 0], seg.points[sel, 1], c=seg.colors[sel], s=1)
            if s["gt"] is not None:
                draw_rects(ax, gt_params_in_table(s, table), {"color": "k", "lw": 3.0}, "ground truth")
            if len(fit["params_bbox"]):
                draw_rects(ax, fit["params_bbox"], {"color": "gray", "ls": "--"}, "bounding box")
            draw_rects(ax, fit["params_opt"], {}, "otimização")
            ax.set_aspect("equal", adjustable="datalim")
            ax.set_title(s["name"])
            ax.tick_params(labelsize=7)
        except Exception as error:
            print(f"  (vista de cima de {s['name']} não feita: {error})")
    axes.ravel()[0].legend(loc="upper right", fontsize=7, frameon=True)
    fig.tight_layout()
    return save(fig, "parte3_vistas_de_cima.png")


def figure_evolution(s):
    """Evolução da otimização numa cena: as caixas em 4 iterações (vistas de cima) e o custo."""
    from parte2_segmentacao import load_segmentation
    from parte3_ajuste import NUM_PARAMS, draw_rects, load_fit
    fit, seg = load_fit(s["parts"]), load_segmentation(s["parts"])
    snaps, costs = np.asarray(fit["snapshots"]), np.asarray(fit["snapshot_costs"])
    if len(snaps) < 2:
        return None
    iterations = [0]                       # só as iterações (no jacobiano muda um só parâmetro de cada vez)
    for k in range(1, len(snaps)):
        if np.sum(snaps[k] != snaps[iterations[-1]]) > 1:
            iterations.append(k)
    if iterations[-1] != len(snaps) - 1:
        iterations.append(len(snaps) - 1)
    picks = sorted(set(np.linspace(0, len(iterations) - 1, 4).round().astype(int)))
    fig, axes = plt.subplots(1, len(picks) + 1, figsize=(3.6 * (len(picks) + 1), 3.6))
    sel = np.random.default_rng(0).choice(len(seg.points), min(len(seg.points), 8000), replace=False)
    for ax, i in zip(axes, picks):
        ax.scatter(seg.points[sel, 0], seg.points[sel, 1], c=seg.colors[sel], s=1)
        draw_rects(ax, snaps[iterations[i]].reshape(-1, NUM_PARAMS), {})
        ax.set_aspect("equal", adjustable="datalim")
        ax.set_title("estimativa inicial" if i == 0 else f"iteração {i} (custo {costs[iterations[i]]:.0f})",
                     fontsize=9)
        ax.tick_params(labelsize=7)
    axes[-1].plot(range(len(iterations)), costs[iterations], "-o", color=SERIES[0], lw=2, ms=4)
    axes[-1].set_xlabel("iteração")
    axes[-1].set_ylabel("custo")
    axes[-1].set_title("custo", fontsize=9)
    fig.suptitle(f"Evolução da otimização ({s['name']}, referencial da mesa)")
    fig.tight_layout()
    return save(fig, "parte3_evolucao.png")


def figure_photometry(s):
    """Mosaico das imagens de uma cena: originais em cima, corrigidas em baixo (com o s e o b)."""
    from extra_fotometria import figure_data
    data = figure_data(s["r1"], s["photometry"])
    images = np.asarray(data["images"])
    used = np.where((images < images.max()).any(axis=(0, 2)))[0]      # corta as colunas vazias à direita
    if len(used):
        images = images[:, :used[-1] + 9]
    plt.imsave(FIGURES / "extra_mosaico.png", images)
    return "docs/teste/extra_mosaico.png"


# #####################################################################################################
# 3. TABELAS E TEXTO DA SECÇÃO
# #####################################################################################################
def fmt(v, d=3):
    return "—" if v is None else f"{v:.{d}f}"


def section(scenes, figures, results_dir):
    has_gt = [s for s in scenes if s["gt"] is not None]
    exposure = [s for s in scenes if exposure_changes(s)]
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    L = [f"_Resultados obtidos pelo nosso sistema nas cenas do teste (`{results_dir.name}/`, {now}); secção gerada "
         "pelo `run_test.py`._", ""]
    L += [f"{len(scenes)} cenas; {len(has_gt)} com ground truth; {len(exposure)} com Exposure changes"
          + (f" ({', '.join(s['name'] for s in exposure)})" if exposure else "") + ".", ""]
    if "cenas" in figures:
        L += [f"![Cenas do teste]({figures['cenas']})", ""]

    # Resumo
    L += ["### Resumo", ""]
    L += ["| cena | imagens | câmaras registadas | caixas encontradas / reais | IoU otimização | IoU bounding box |",
          "|---|---|---|---|---|---|"]
    opt, bb = [], []
    for s in scenes:
        o, b = iou_of(s["report"], "otimização"), iou_of(s["report"], "bounding box")
        if o is not None:
            opt.append(o)
            bb.append(b or 0.0)
        real = "?" if s["real"] is None else s["real"]
        L.append(f"| `{s['name']}` | {s['images']} | {s['registered']} | {len(s['result']['boxes'])} / {real} | "
                 f"{'**' + fmt(o) + '**' if o is not None else '—'} | {fmt(b)} |")
    if opt:
        L.append(f"| **média** | | | | **{np.mean(opt):.3f}** | {np.mean(bb):.3f} |")
    L.append("")
    if "iou" in figures:
        L += [f"![IoU 3D médio por cena]({figures['iou']})", ""]
    if not has_gt:
        L += ["As cenas não têm `ground_truth.json`, por isso não há erros: as tabelas mostram o que o sistema "
              "estimou. O IoU é calculado pelo professor.", ""]

    # Parte 1
    L += ["### Parte 1 — Registo", ""]
    rows = []
    for s in has_gt:
        r = md_table(s["report"], "## Parte 1")
        mean = next((x for x in r if x[0].startswith("média")), None)
        mx = next((x for x in r if x[0].startswith("máximo")), None)
        if mean and mx:
            rows.append(f"| `{s['name']}` | {s['images']} | {mean[1]} | {mean[2]} | {mx[1]} | {mx[2]} |")
    if rows:
        L += ["Erro de cada câmara em relação ao ground truth (`E = T_gt⁻¹ · T_est`), média sem a câmara 000 e "
              "máximo; os erros de cada câmara estão em `results_test/<cena>/avaliacao.md`:", "",
              "| cena | imagens | translação média (mm) | rotação média (°) | translação máx. (mm) | rotação máx. (°) |",
              "|---|---|---|---|---|---|"] + rows + [""]
    if "nuvens" in figures:
        L += ["Nuvem agregada de cada cena com as poses estimadas: cor dos pixels e uma cor por câmara.", "",
              f"![Nuvens agregadas]({figures['nuvens']})", ""]
    if "sobreposicao" in figures:
        L += ["Nuvem com as poses estimadas (vermelho) sobre a nuvem com as poses verdadeiras (verde), de perto:", "",
              f"![Sobreposição com o ground truth]({figures['sobreposicao']})", ""]

    # Parte 2
    L += ["### Parte 2 — Segmentação", ""]
    if "segmentacao" in figures:
        L += ["Objetos isolados do resto da nuvem agregada (a cinzento), uma cor por conjunto de pontos:", "",
              f"![Segmentação]({figures['segmentacao']})", ""]
    rows = []
    for s in has_gt:
        m = next((x for x in md_table(s["report"], "## Parte 2") if x[0] == "média"), None)
        found = re.search(r"Caixas encontradas: (\d+), reais: (\d+)", s["report"])
        if m and found:
            rows.append(f"| `{s['name']}` | {found.group(1)} / {found.group(2)} | {m[3]} | {m[4]} |")
    if rows:
        L += ["Avaliação só da segmentação (nuvens juntas com as poses verdadeiras; pontos de cada caixa "
              "verdadeira com 5 mm de margem):", "",
              "| cena | caixas encontradas / reais | precisão média | recall médio |", "|---|---|---|---|"] + rows
        L += ["", "O *recall* fica abaixo de 1 de propósito: a referência inclui os pontos até 8 mm acima da mesa e "
              "a margem de 5 mm, que a segmentação retira. Nas caixas da mesma cor em contacto, os conjuntos vêm "
              "da divisão inicial da Parte 3, que a otimização depois corrige.", ""]

    # Parte 3
    L += ["### Parte 3 — Caixas", ""]
    if "vistas" in figures:
        L += ["Vista de cima de cada cena (referencial da mesa): "
              + ("preto = ground truth, " if has_gt else "")
              + "cinzento a tracejado = bounding box, cores = otimização.", "",
              f"![Vistas de cima]({figures['vistas']})", ""]
    if "evolucao" in figures:
        L += [f"![Evolução da otimização]({figures['evolucao']})", ""]
    if has_gt:
        L += ["Erros da otimização em cada caixa verdadeira (associação pelo IoU 3D, com as simetrias da caixa; "
              "dL, dW, dH = estimado − verdadeiro) e IoU 3D dos dois métodos:", "",
              "| cena | caixa | posição (mm) | altura z (mm) | yaw (°) | dL (mm) | dW (mm) | dH (mm) | IoU otimização "
              "| IoU bounding box |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for s in has_gt:
            bbox = {r[0]: r[8] for r in md_table(s["report"], "### bounding box")}
            for r in md_table(s["report"], "### otimização"):
                L.append(f"| `{s['name']}` | {r[0]} | " + " | ".join(r[2:8]) + f" | **{r[8]}** | {bbox.get(r[0], '—')} |")
        L.append("")
    without = [s for s in scenes if s["gt"] is None]
    if without:
        L += ["Caixas estimadas (otimização, referencial da mesa; `z` = altura da base acima da mesa):", "",
              "| cena | caixa | x (m) | y (m) | yaw (°) | length (m) | width (m) | height (m) | z (m) |",
              "|---|---|---|---|---|---|---|---|---|"]
        from parte3_ajuste import load_fit
        for s in without:
            for k, p in enumerate(load_fit(s["parts"])["params_opt"]):
                L.append(f"| `{s['name']}` | {k} | {p[0]:.3f} | {p[1]:.3f} | {np.degrees(p[2]):.1f} | {p[3]:.3f} | "
                         f"{p[4]:.3f} | {p[5]:.3f} | {p[6]:.3f} |")
        L.append("")

    # Extra: fotometria
    if exposure:
        L += ["### Extra — Correção fotométrica", "", "s e b de cada imagem em relação à 000 (que é a referência):", ""]
        L += ["| cena | imagem | s estimado | b estimado" + (" | s verdadeiro | b verdadeiro | erro de s | erro de b |"
                                                         if any(s["true_exposures"] for s in exposure) else " |"),
              "|---|---|---|---" + ("|---|---|---|---|" if any(s["true_exposures"] for s in exposure) else "|")]
        for s in exposure:
            truth = s["true_exposures"]
            for r in (s["photometry"] or {}).get("imagens", []):
                if r["imagem"] == "000":            # a 000 é a referência (s = 1, b = 0)
                    continue
                line = f"| `{s['name']}` | {r['imagem']} | {r['s']:.3f} | {r['b']:+.3f}"
                if truth and r["imagem"] in truth:
                    ts, tb = truth[r["imagem"]]
                    line += f" | {ts:.3f} | {tb:+.3f} | {abs(r['s'] - ts):.3f} | {abs(r['b'] - tb):.3f}"
                L.append(line + " |")
        L.append("")
        for s in exposure:
            ph = s["photometry"] or {}
            if "erro_cor_antes" in ph:
                L.append(f"- `{s['name']}`: erro de cor nos pontos vistos por mais do que uma câmara "
                         f"{ph['erro_cor_antes']:.3f} sem correção → {ph['erro_cor_depois']:.3f} com correção.")
        L.append("")
        if "mosaico" in figures:
            L += [f"Imagens de `{exposure[0]['name']}`: em cima as originais, em baixo as corrigidas.", "",
                  f"![Mosaico da correção fotométrica]({figures['mosaico']})", ""]
    return "\n".join(L)


# #####################################################################################################
# 4. PROGRAMA PRINCIPAL
# #####################################################################################################
def update_readme(results_dir, scenes_dir=None, readme=README):
    """Lê os resultados de cada cena, faz as figuras e reescreve a secção dos resultados do README."""
    results_dir = Path(results_dir)
    scenes_dir = Path(scenes_dir) if scenes_dir else None
    known = {}
    if scenes_dir is not None and (scenes_dir / "num_boxes.json").exists():
        data = json.loads((scenes_dir / "num_boxes.json").read_text(encoding="utf-8"))
        known = {k: int(v) for k, v in data.items() if not k.startswith("_")}
    scenes = []
    for out in sorted((p for p in results_dir.iterdir() if (p / "result.json").exists()), key=natural_key):
        try:
            scenes.append(read_scene(out, scenes_dir, known))
        except Exception as error:
            print(f"  ({out.name} fica de fora do README: {error})")
    if not scenes:
        print(f"README: não há resultados em {results_dir}")
        return
    FIGURES.mkdir(parents=True, exist_ok=True)
    for old in FIGURES.glob("*.png"):
        old.unlink()
    figures = {}
    steps = [("cenas", lambda: figure_scenes(scenes)), ("iou", lambda: figure_iou(scenes)),
             ("vistas", lambda: figure_top_views(scenes))]
    for key, make in steps:
        try:
            path = make()
            if path:
                figures[key] = path
        except Exception:
            traceback.print_exc()
    try:
        figures.update(figures_clouds(scenes))
    except Exception:
        traceback.print_exc()
    try:   # evolução: a cena com mais caixas
        path = figure_evolution(max(scenes, key=lambda s: len(s["result"]["boxes"])))
        if path:
            figures["evolucao"] = path
    except Exception:
        traceback.print_exc()
    exposure = [s for s in scenes if exposure_changes(s) and s["photometry"]]
    if exposure:
        try:
            figures["mosaico"] = figure_photometry(exposure[0])
        except Exception:
            traceback.print_exc()
    text = readme.read_text(encoding="utf-8")
    block = f"{START}\n{section(scenes, figures, results_dir)}\n{END}"
    if START in text and END in text:
        text = text[:text.index(START)] + block + text[text.index(END) + len(END):]
    else:
        text = text.rstrip() + "\n\n## Resultados do teste\n\n" + block + "\n"
    readme.write_text(text, encoding="utf-8")
    print(f"README.md: secção dos resultados reescrita ({len(scenes)} cenas, figuras em docs/teste/)")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--results", default=str(FOLDER / "results_test"), help="pasta escrita pelo run_test.py")
    parser.add_argument("--scenes", default=str(FOLDER / "test"), help="pasta das cenas (para o num_boxes.json)")
    args = parser.parse_args()
    update_readme(args.results, args.scenes)


if __name__ == "__main__":
    main()
