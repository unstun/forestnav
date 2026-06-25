---
name: mineru-pdf-to-md
description: |-
  用 MinerU Open API VLM 把 PDF 转成 Markdown。触发: Dr Sun 说"PDF 转 MD"、"MinerU 转论文"、"用 VLM 跑文献"、"修复公式丢失的 MD"、"批量重跑文献库公式"。
argument-hint: "[PDF 路径 / CitationKey / batch scope]"
user-invocable: true
context: inline
---

# MinerU PDF -> Markdown

用 MinerU 官方 `mineru-open-api` 的 VLM 模式处理 PDF。Dr Sun 已确认当前 MinerU 额度按免费方案使用；若 API 返回 billing、quota、payment 相关错误，立即停下并报告。

## 硬规则

- 不要把 token 写进文件、日志、git 或回复；只用环境变量 `MINERU_TOKEN`。
- 不要直接覆盖主文献库；先转到 `1_survey/papers/api_trials/`，通过质量门槛后再入库。
- arXiv 有源码时优先考虑 `fetch-arxiv-md`；PDF-only、公式丢失、表格/图片复杂时用本 skill。
- 每次批量前先 `--dry-run`，确认目标数量和范围。

## 单篇转换

```bash
MINERU_TOKEN="$MINERU_TOKEN" /Users/sun/.local/bin/mineru-open-api extract \
  1_survey/papers/pdf/<CitationKey>.pdf \
  --model vlm \
  --language en \
  --formula=true \
  --table=true \
  -f md,json \
  -o 1_survey/papers/api_trials/mineru_vlm/<CitationKey> \
  --timeout 1200
```

检查输出：

```bash
wc -l 1_survey/papers/api_trials/mineru_vlm/<CitationKey>/<CitationKey>.md
grep -c '^#' 1_survey/papers/api_trials/mineru_vlm/<CitationKey>/<CitationKey>.md
grep -cE '\$\$|\\tag\{|\\begin\{equation' 1_survey/papers/api_trials/mineru_vlm/<CitationKey>/<CitationKey>.md
```

## 批量修复文献库

默认只修复最该重跑的风险项：

```bash
python3 1_survey/scripts/batch_mineru_vlm.py --scope risk --dry-run
MINERU_TOKEN="$MINERU_TOKEN" python3 1_survey/scripts/batch_mineru_vlm.py --scope risk --timeout 1200
```

常用参数：

- `--scope risk`: `pymupdf4llm` 且公式数为 0 的成功转换项。
- `--scope pymupdf`: 所有 `pymupdf4llm` 项。
- `--limit N`: 先跑 N 篇抽检。
- `--start-index N`: 从 dry-run 列表第 N 项后继续。
- `--force`: 忽略已有 staged 结果，重新请求 MinerU。

脚本会：

- staged 输出到 `1_survey/papers/api_trials/mineru_vlm_batch/<CitationKey>/`
- 质量门槛通过后替换 `1_survey/papers/md/<CitationKey>.md`
- 图片复制到 `1_survey/papers/md/<CitationKey>_figs/`
- 更新 `1_survey/papers/md/conversion_status.csv`
- 记录 `batch_status.jsonl`

## 入库质量门槛

默认必须满足：

- Markdown 大小 >= 5000 bytes
- 行数 >= 50
- 标题数 >= 3
- 公式数 > 0

抽检时至少看一篇完整 MD：标题层级、公式、图片路径、frontmatter 的 `source: mineru-vlm` 和 `reviewed: false`。

## 收尾

批量完成后报告：成功篇数、总页数或目标数、失败项、剩余 risk 数。若改了主库文件，按项目规则提交一次 git commit。
