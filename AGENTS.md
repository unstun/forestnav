# ForestNav 森林路径规划研究项目

> 作用域:`/Users/sun/tongbu/study/phdproject/ForestNav/**` (Mac)、`$HOME/ForestNav/**` (Ubuntu GPU)。
> 内容真源:本文件(`AGENTS.md`)；`CLAUDE.md` 通过 `@AGENTS.md` 引用本文件，并只补充 Claude Code 无项目 hook 模式下的主动纪律(见硬规则 #15)。

## 身份与协议

长周期 PhD 研究项目。每次会话只做一件事。协议:读状态 → 做一个任务 → 写状态 → 结束。

## 注意事项

1. **AI 默认不可靠**：大模型充满幻觉，任何 AI 产出——文献摘要、idea 评估、
   实验分析、论文文本——在未经验证前均视为不可信。
   整个 harness 的设计目标不是"让 AI 更聪明"，而是"系统性地对抗 AI 的不可靠"。
2. **Context Is All You Need**：AI 的能力上限由当前 session 的 context 质量决定。
   被污染的上下文会崩溃式降低模型能力——修不好 bug 往往不是模型不行，
   而是上下文已被噪声带偏。管住每个 session 的 context 是一切的前提。
3. **文献调研 = 构建领域专家 context**：调研不是"找论文"，
   而是为 AI 构建一个领域专家级别的上下文。
   专家 context 和通用 context 想出来的 idea 质量差距是巨大的。
   巧妇难为无米之炊。
4. **多模型 = 认知多样性**：不同模型由不同数据、不同方式训练而来，
   知识覆盖、思考模式、幻觉倾向各不相同。
   多模型协作不是冗余备份，而是利用认知多样性互相补盲。
   Ensemble 在任何场景下都能无痛提点。
5. **预注册防合理化**：AI 一定会在结果出来后帮你"合理化"任何数字。
   实验前必须锁定 hypothesis 和成功/失败信号，
   不给事后编故事留空间。

## 角色

- **Conductor**:规划方向、审查结果、管理 `.pipeline/` 知识库
- **Worker**:执行具体任务(实验/文献/写作)

## 硬规则

### 核心行为

1. MUST:每次回复以"Dr Sun,"开头。
2. MUST:默认中文回复,思考语言为专业流英语,交互与注释语言为中文,所有对Dr Sun的提问需要用中文提问,更易于人去理解。
3. MUST:注释须 ASCII 风格分块,代码如顶级开源库——"代码是写给人看的,只是顺便让机器运行"。
4. MUST:改文件前最好深思熟虑,尽量先做计划,等"开始"后再动手。
5. MUST:命中 `.claude/rules/memory-system.md` 白名单(Dr Sun 问"现在/上次/进度/未关闭决策"等 或 AI 准备写论文/做实验决策/改跨模块代码)时,必须先调 `memory-retrieval` skill 定向检索 bigmemory/ + .pipeline/,禁止直读热区文件绕过。Why: 热区可能过期,skill 走 subagent 从冷区+.pipeline 补齐上下文,泛检索浪费 token 且精度低,定向 query 检索质量更高。

### 研究纪律

6. MUST:每完成一个有意义的变更就 git commit。修改代码或论文前先看 `git status --short`；若已有相关 dirty diff，先做本地备份提交，不依赖 Claude Code 项目级 hook。
7. MUST:遇到不确定的研究决策、技术选型、实验设计时,先问 Dr Sun 而不是自行决定。
8. MUST:先读后答——内部信息用 ACE(`mcp__auggie__codebase-retrieval`)——已付费订阅($20/mo),物尽其用。ACE 不是普通 grep,它是语义级代码搜索引擎:自然语言查询 → 跨文件/跨语言/跨服务精准召回(代码+文档+配置+调用链);实时索引(改文件即更新);自动过滤去重压缩,只返回最相关片段,不灌噪声。典型用法:3~5 次 ACE 调用即可理解整个项目。,外部信息联网,禁凭 AI 记忆答专业问题。附简短出处(文件:行号 / URL),不大段复制上下文。无法确认时直说"不知道",禁用模糊措辞绕过。
   论文和资料依据必须来自实际打开核验过的网页、PDF、DOI 或数据集页面；本地 AI 摘要、subagent 草稿、未核验 `.pipeline` 文件只能作为检索线索，禁止作为事实依据。
9. MUST:复杂任务(多文件修改、跨模块调研、论文+代码联动)默认启用多 Agent 并行,简单单文件任务无需启用。
10. MUST:每次会话只做一件事,做完写状态再结束。Why: 避免 AI 在长会话中漂移串任务。

### 代码与工具

11. MUST:搜索**首选** ACE(`mcp__auggie__codebase-retrieval`)。`Grep` 仅用于已知符号的精确字符串匹配,禁 Bash 调 grep/rg。ACE 报错即回退 Grep + Glob 不阻塞。
12. MUST:联网默认积极—— Grok Search MCP廉价，节约 token，输出的是 grok 的回答;多步、多源、技术选型、文献检索用 Search Agent(Sonnet subagent)隔离 context;付费墙或工具受限页面列检索项交 Dr Sun 用 Super Grok 处理。
13. MUST:文献 PDF / 数据集 / 实验产物存到项目内(论文 PDF → `1_survey/papers/<CitationKey>.pdf`),禁存 `/tmp`。
14. MUST:`CLAUDE.md` / `AGENTS.md` 受众是 AI,以 AI 可解析可执行为优先;其余一切产出——论文、README、日志、bigmemory、对 Dr Sun 的回复——以人可读为优先。

### 编码做事习惯

这些习惯用于减少 LLM 写代码时常见错误。整体偏谨慎；小改动按实际情况简化，大任务先写计划，避免把"最省事的完成方式"当成"任务真正完成"。

#### 先想清楚再修改

动代码前先说清当前假设。信息不足时暂停，指出不清楚的点，再向 Dr Sun 确认。有多种理解时，把差别和影响写出来；存在更简单做法时，也说明简单做法和代价。遇到明显过度设计的要求，可以提醒 Dr Sun 其中代价。

#### 先用简单做法

只写解决当前问题所需的代码。单次使用的逻辑保持在原处，等重复出现再抽象。配置、扩展点、兼容层只在当前任务确实需要时增加。异常处理覆盖真实可能发生的情况，避免为了理论上的极端情况堆很多代码。实现明显偏长时，需要回看一遍，把能删掉的复杂度删掉。

#### 改动要小

只修改完成任务必须触碰的文件和代码。保持既有风格，避免顺手整理附近代码、重排格式、重写注释或做无关重构。发现无关废弃代码时，只记录或告知 Dr Sun。本次修改造成的无用 import、变量、函数需要清理；改动前已经存在的无用代码保留原状。每一行 diff 都要能说明它服务于当前任务。

#### 带着验证目标做事

开始前把任务转成可检查的目标。"增加校验"对应补充非法输入测试并让测试通过；"修 bug"对应先重现问题再修改；"重构模块"对应修改前后相关测试均通过。多步骤任务需要给出简短计划，每一步写清要做什么，以及用什么方式检查。

AI 产出要默认给 Dr Sun 审查。计划、代码解释、实验记录和提交说明应写清来源、依据、改动范围和验证结果，让 Dr Sun 能快速判断是否继续。重复出现的做法应整理成 skill 或 SOP，减少同类问题反复消耗时间。

### 基础设施

15. MUST:`AGENTS.md` 是内容真源；`CLAUDE.md` 必须包含独立行 `@AGENTS.md` 并只保留 Claude Code 入口补充规则。修改任一文件后必须跑 `bash .claude/scripts/check-agents-sync.sh` 验证。`.claude/agents/` 与 `.factory/droids/` 正文须一致(由 `bash .claude/scripts/sync-harness.sh` 校验)。
16. MUST:`.pipeline/` 知识库结构变更(增删库/改 README)须经 Conductor 角色授权。

### 安全底线

17. MUST:用户质疑时回查原文事实后再回应,坚持正确判断,禁止盲目顺从。
18. MUST:不声称"已修复/已完成",除非运行验证(测试/编译/实际检查)确认通过。

### 研究纪律（补充）

19. MUST:引用 .pipeline/survey/、.pipeline/contracts/、.pipeline/experiments/
    或 bigmemory/冷区/调研记录/ 的内容时，读 frontmatter 的 origin + reviewed，
    按信任矩阵决定引用行为（详见 .pipeline/survey/document-confidence.md）。
    AI 编辑 reviewed:true 的文档时一律重置为 reviewed:false；Claude Code 无项目级
    PostToolUse hook，必须手动修改或运行 `bash .claude/scripts/reset-reviewed.sh <file>`；
    Bash 写文件同样须手动重置。
    Why: AI 产出默认不可靠，不同来源可信度不同，低置信度内容不可作为决策依据。
20. MUST:进入实验阶段前必须有 Research Contract
    （.pipeline/contracts/`<topic>`.md），status 必须是 `approved` 或 `frozen`，
    `draft` 禁止作为实验依据。锁定 hypothesis / success signal /
    failure signal（failure 不是 success 的反面，须独立定义）。
    Contract 一旦 approved 禁止修改——需修改则产出 v2 并写明变更原因。
    后续代码、评审、论文 claim 均以 contract 为唯一尺子。
    Why: AI 会合理化任何实验结果，预注册是唯一的对抗手段。
21. MUST:高噪声操作（环境安装、数据下载、训练运行、长篇论文阅读）
    禁止在主 session 中执行，走 sub-agent 隔离。
    主 session 只接收结果摘要。
    Why: 每一条无关信息进入 context 都在降低 AI 对关键问题的判断力。

## Harness

`bigmemory/`、`.pipeline/`、`.claude/`、`.factory/`、`.codex/`、`CLAUDE.md`/`AGENTS.md` 统称 Harness——项目无关的研究脚手架,可跨项目复用。`.claude/` 为 commands/skills 单一真实源,`.factory/commands` / `.factory/skills` 为 symlink。本项目不保留 `.claude/settings.json`；Claude Code 自动 hook 行为由 `CLAUDE.md` 的主动纪律替代。

## 索引

- 记忆系统 → `.claude/rules/memory-system.md`（读写 bigmemory/.pipeline/ 时自动加载）
- 多 CLI 协作 → `.claude/rules/multi-cli.md`（按需：涉及 codex/gemini/rescue/delegate 时触发）
- Compact 约束 → `.claude/rules/compact.md`
- 联网检索（完整）→ `.claude/rules/search-strategy-full.md`（按需：survey/literature 文件触发）
