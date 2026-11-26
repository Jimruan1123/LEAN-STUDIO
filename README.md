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

## 当前开发优先级
[轻量 Web + 数据库 / 宜搭优先 ADR-001](docs/WEB-YIDA-DEPLOYMENT.md)。下一版本 V0.2 为独立 Web 双主线最小原型（规划，尚未发布）；成熟 APP 对标按需并行，不作为所有 Web 工作的前置条件。

[数字零件标准与轻量加工 ADR-002](docs/PART-ASSET-CONTRACT.md)：外部软件生产零件，Web/YIDA 负责装配及受控参数编辑；统一 GLB/JSON/可选 STEP 接入。

[ADR-003 方形铝型材优先](docs/ALUMINUM-FIRST.md)：首期仅 20/30/40 方形铝型材，28mm 精益管延后；V0.2-B 以铝型材双主线验证为目标。

## V0.2-C 4040 装配套件研究实验
[实验代码、测试记录及说明](research/upstream/4040-assembly-kit/README.md)：新增 E4040t 独立截面、简化角码/螺母/螺栓/端盖，28 实例、36 关系边、15 项离线测试通过。500→800 mm 横梁参数重建，GLB/JSON 回读；尚未实现通用吸附、完整碰撞检测、真实供应商认证、Three.js 或宜搭运行。仅研究成果，不关闭 V0.2/Gate。

## V0.2-D Web 装配研究原型
[源码及复现说明](apps/studio-web-v02d/README.md)：沿用 V0.2-C 4040t 五类 GLB，标准框架和受限自由直角装配，12 项 Node 图谱测试及 11 项 Chromium DOM 测试通过。Three.js r180/GLTFLoader/OrbitControls 已编写适配层，WebGL2 不可用及导航策略阻塞，真实渲染/部署仍未实测。宜搭尚未接入。下一步本地 Codex 完成真实 WebGL 验证，再扩展多端约束及 SOP 工作台。
