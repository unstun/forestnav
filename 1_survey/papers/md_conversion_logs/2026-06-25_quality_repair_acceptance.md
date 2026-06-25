---
origin: ai+local-source
reviewed: false
date: 2026-06-25
scope: path-quality motion-planning corpus repair acceptance
---

# 文献库 6 项系统问题修复验收

## 结论

本轮按附件目标完成文献库质量修复。PDF-only/公式风险项改用 MinerU Open API VLM 修复；`api_trials/` 仅作为本地中间产物，不入库。

## 验收结果

| 项 | 验收标准 | 当前结果 | 状态 |
|---|---:|---:|---|
| 标题相关性 | 跑题比例 < 5% | 3 / 489 = 0.61% | pass |
| 经典种子 | 有效 arXiv 种子全部入库 | 15 / 15 | pass |
| MD 数量 | >= 300 | 523 个非 README MD | pass |
| 转换覆盖 | 处理全部候选状态 | 489 / 489 状态行 | pass |
| 公式风险 | 成功库中 pymupdf4llm + formulas=0 为 0 | 0 | pass |
| 弱方向数量 | A/B/M/P 各 >= 10 | A=13, B=33, M=13, P=15 | pass |

## 当前语料统计

| 指标 | 值 |
|---|---:|
| `paper_list.csv` 候选 | 489 |
| PDF 文件 | 523 |
| 非 README Markdown | 523 |
| 转换成功 | 484 |
| 转换失败 | 5 |
| arXiv e-print 来源 | 383 |
| MinerU VLM 来源 | 96 |
| pymupdf4llm 来源 | 7 |
| none/失败来源 | 3 |

## 经典种子核验

以下附件要求的 15 个 seed 均已出现在 `1_survey/papers/paper_list.csv`：

`1601.06326`, `1105.1186`, `1405.5848`, `1404.2334`, `1306.3532`, `2002.06599`, `1706.09068`, `1310.3163`, `2101.11565`, `1901.03922`, `1104.2800`, `1804.07537`, `1510.08636`, `2010.15394`, `1710.00567`.

## 已知边界

- `reviewed: false` 仍然有效：这些 MD 可用于 AI 精读和人工筛选，不能直接作为论文 claim。
- 标题相关性检查只按 `search_papers.py` 的 `RELEVANCE_KEYWORDS` 自动门槛统计；最终是否跑题仍需人工抽查。
- MinerU VLM 输出比 PyMuPDF 保留更多公式和图片，但个别 inline math/OCR 仍可能需要精校。
