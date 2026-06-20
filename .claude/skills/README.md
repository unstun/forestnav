# 本地 Skill 约定

本目录 `.claude/skills/` 存放**项目级** skill，跟随仓库走。
Dr Sun 2026-04-20 明确：**新增 skill 一律放本地**，不写入 `~/.claude/skills/`。

## Why

- 项目级 skill 跟仓库走，git 可追踪，跨机器/跨 AI 协作一致
- User 级（`~/.claude/skills/`）只适合真正跨项目的个人习惯
- 本项目 harness（`bigmemory`/`.pipeline`/`CLAUDE.md`）强调可复用可追溯，skill 同理

## 目录规范

```
.claude/skills/<skill-name>/
├── SKILL.md      # 必需：YAML frontmatter + 文档
├── *.sh / *.py   # 可选：脚本（chmod +x）
└── README.md     # 可选：用户向补充说明
```

## SKILL.md Frontmatter

```yaml
---
name: <skill-name>          # kebab-case，与目录名一致
description: <一句话>       # Skill 发现系统按此判断是否触发
---
```

description 要包含**触发关键词**——Dr Sun 或 AI 何时应调用该 skill。例：

```
description: 从 arXiv ID 拉 e-print 源码转 Markdown。用户说"转论文为 md"、"批量转 arXiv"时触发。
```

## 本项目既有本地 skill

大多数在 `.claude/skills/` 的 skill 都是本项目专有的研究 harness 组件
（`research-*`、`inno-*`、`experiment`、`survey`、`write`、`plan`、`review`、`archive` 等），
由 Dr Sun 的 harness 注入。新增时放在同级目录即可。

带 namespace 前缀的 skill（如 `superpowers:*`、`anthropic-skills:*`、`codex:*`、
`ppt-agent:*`、`claude-md-management:*`）来自 plugin，**不要覆盖**，
需要改造时在本地 fork 一个新 kebab-case skill。

## 新增 skill checklist

- [ ] 目录命名 kebab-case
- [ ] SKILL.md 含 frontmatter（name + description）
- [ ] description 含触发关键词
- [ ] 脚本 `chmod +x`
- [ ] 调试一次端到端流程
- [ ] git commit（硬规则 #6）
