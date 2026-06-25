@AGENTS.md

## Claude Code 无项目 hook 模式

本项目不保留 `.claude/settings.json`。以下规则替代原 Claude Code hook 的自动行为，是 Claude Code 必须主动执行的软约束。

1. 修改文件前先运行 `git status --short`。如果已有未提交改动，先判断是否与当前任务相关；不相关的改动不碰，相关但风险高时先向 Dr Sun 说明。
2. 修改代码、论文或研究记录前，如果工作区已有相关 dirty diff，先做本地备份提交；不要依赖自动 `PreToolUse` hook。
3. Dr Sun 问 git、commit、push、merge、分支等问题时，先看当前分支、最近 commit 和 `git status --short`。
4. Dr Sun 问进度、状态、上次、最近、记忆、热区时，按 `AGENTS.md` 先走 `memory-retrieval` 定向检索；如果该 skill 不可用，再读取 `bigmemory/热区/状态简报.md`、`bigmemory/热区/未关闭决策.md`、`bigmemory/热区/近期改动.md`。
5. 联网或文献检索前先按项目搜索策略选择工具：深度/多源调研优先隔离到搜索 agent 或 smart-search；快速 1-2 条验证才直连搜索；不要依赖自动搜索前 hook。
6. 修改 `.pipeline/survey/`、`.pipeline/contracts/`、`.pipeline/experiments/` 或 `bigmemory/冷区/调研记录/` 下带 frontmatter 的文档后，如果原来有 `reviewed: true`，必须手动改为 `reviewed: false`，或运行 `bash .claude/scripts/reset-reviewed.sh <file>`。
7. 完成有意义变更后，按 `AGENTS.md` 要求做验证并提交；提交作者使用当前工具默认身份即可，不要为了提交作者恢复 `.claude/settings.json`。
