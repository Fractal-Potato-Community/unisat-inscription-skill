# Bitcoin 铭文开发 Skill

用于 Bitcoin 和 Fractal Bitcoin 铭文协议开发的 Claude Code Skill，包含完整的 UniSat API 文档。

[English](README.md)

## 关于

本 Skill 由 **Fractal Potato Community** 贡献，包含了日常使用 UniSat 进行接口开发的一些实用经验和技巧。

## 功能特性

### 协议规范
- **BRC-20**: 部署/铸造/转账操作，4字节和5字节 tick，验证规则
- **Runes**: UTXO 原生模型，Runestone 编码，蚀刻/铸造/转账
- **Ordinals**: Sat 编号，信封格式，递归铭文，父子关系
- **CAT20**: Fractal Bitcoin 的 OP_CAT 代币标准

### UniSat API 覆盖
- **Bitcoin 主网**: 完整 indexer（BRC-20、Runes、Alkanes、Collections），铭刻服务，Marketplace v3
- **Fractal 网络**: BRC20-Swap（无 Gas 转账），CAT20-DEX，Runes 支持，Collection 管理

### 验证工具
- BRC-20/CAT20 格式验证 Python 脚本
- Rune 名称验证

## 安装

### 方式一：导入 .skill 文件（推荐）

下载 `inscription-formats.skill` 并导入 Claude Code。

### 方式二：手动安装

将 `inscription-formats/` 文件夹复制到以下位置之一：

```bash
# 项目级别（仅当前项目）
.claude/skills/inscription-formats/

# 全局（所有项目）
~/.claude/skills/inscription-formats/
```

## 使用方法

安装后，当你询问以下内容时，Claude 会自动使用此 skill：

- BRC-20、Runes、Ordinals 或 CAT20 协议
- UniSat API 端点和集成
- 铭文格式验证
- Fractal Bitcoin 开发

### 示例查询

```
"生成一个 BRC-20 部署铭文，代币名 TEST，总量 21000000"

"如何使用 UniSat API 获取 BRC-20 余额？"

"展示 Fractal 上 BRC20-Swap 的转账流程"

"验证这个铭文 JSON 格式是否正确"
```

## 文件结构

```
inscription-formats/
├── SKILL.md                           # Skill 主文件
├── references/
│   ├── brc20-spec.md                  # BRC-20 协议规范
│   ├── runes-spec.md                  # Runes 协议规范
│   ├── ordinals-spec.md               # Ordinals 协议规范
│   ├── fractal-spec.md                # Fractal Bitcoin 特性
│   └── unisat-api.md                  # UniSat API 文档（1000+ 行）
└── scripts/
    └── validate_inscription.py        # 格式验证脚本
```

## API 覆盖概览

| 类别 | Bitcoin 主网 | Fractal |
|------|-------------|---------|
| BRC-20 Indexer | ✅ | ✅ |
| Runes Indexer | ✅ | ✅ |
| Alkanes | ✅ | ❌ |
| BRC20-Swap | ❌ | ✅ |
| CAT20-DEX | ❌ | ✅ |
| 铭刻服务 | ✅ | ✅ |
| Marketplace v3 | ✅ | ✅ |

## 贡献

欢迎提交 Issue 和 Pull Request。请确保任何协议更新都经过官方文档验证。

## 相关资源

- [UniSat API Swagger UI](https://open-api.unisat.io)
- [UniSat 开发者文档](https://docs.unisat.io)
- [UniSat GitHub](https://github.com/unisat-wallet/unisat-dev-docs)
- [Ordinals 协议](https://docs.ordinals.com)
- [Runes 协议](https://docs.ordinals.com/runes.html)

## 许可证

MIT License - 见 [LICENSE](LICENSE) 文件。

## 更新日志

### v1.0.0 (2024-12)
- 首次发布
- BRC-20、Runes、Ordinals、CAT20 协议规范
- Bitcoin 和 Fractal 网络的 UniSat API 文档
- BRC20-Swap 实现指南（含生产环境代码示例）
- 格式验证脚本
