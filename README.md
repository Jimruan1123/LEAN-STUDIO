# LEAN-STUDIO

**基线：V0.1.0-init | 2026-11-26 | 立项与概念验证，非生产工程软件**

AI 原生工业精益结构设计平台，面向精益管及铝型材，兼顾通用自由设计、SOP 标准产品配置、混合设计、已有模型导入及改造。两条主线地位相同。以可审计装配图谱为唯一工程数据源，AI 通过受约束的工具修改图谱，确定性程序生成几何、BOM、切割清单和规则结果。

## 文档入口
- [项目章程与路线](docs/ROADMAP.md)
- [技术架构及数据契约](docs/ARCHITECTURE.md)
- [验证计划与验收门](docs/VALIDATION.md)
- [资源接入及权限](research/INGESTION.md)
- [开源与供应商调研清单](research/BENCHMARKS.md)
- [实验 001](examples/EXP-001.md)
- [执行规范](AGENTS.md) / [开放问题](OPEN_ISSUES.md)

## 快速验证
Python 3.10+，无第三方依赖：
```sh
python -m unittest discover -s tests -v
python -m engine.prototype
```
该程序仅验证图谱、自由构建、参数化模板展开、模块增删和确定性 BOM。未实现真实 CAD、三维交互、实际连接件与力学验证；任何输出均不可用于采购、下料或承载认证。
