# 技术架构及数据契约

## 同源设计
用户（自然语言/配置表单/自由操作/导入）→ 意图解析与变更计划 → 事务化装配图谱 → 规则/约束求解 → CAD、可视化、BOM、工程报告。AI 不是几何真值来源，不直接改导出文件。失败操作回滚。标准模板是生成图谱的函数，非标装配可保存为模板，但参数语义需人工复核。

## 领域数据模型
单位 mm；右手坐标系，Z 向上；每个坐标变换明确所属参考系。版本化 catalog_id、part_id、instance_id 和 assembly_id。
- PartDefinition：几何来源/截面、参数、单位、供应商型号、材料、接口、许可、版本、验证状态。
- Interface：局部坐标系、轴/面、连接类别、兼容族、安装偏移、插入深度及允许自由度；未知值不默认零。
- PartInstance：定义版本、实例参数、位姿、所属模块、生命周期。
- Joint：实例+接口对、连接类型、约束、允许间隙/重叠、所需紧固件、来源与验证状态。
- AssemblyGraph：零件实例、连接边、约束、参数依赖、模块、版本、校核记录。
- ProductTemplate：图谱生成规则、参数范围、模块接口、SOP、工程限制及来源；不得覆盖非标编辑而不告知用户。
- Evidence：来源 URL/文件 ID/版本、许可、证据摘录、置信度、审批人、状态。

## 工具 API（规划，尚未实现）
create_part / connect_parts / move_part / resize_part / resize_assembly / add_module / remove_module / replace_part / import_assembly / analyze_assembly / save_as_template / validate_design / generate_bom / export_cad / undo / compare_versions。
输入结构化 JSON；操作前预检、输出 diff、问题、工程状态；关键变更可人工确认。禁止默默改变材料体系、承载等级及连接规格。模板参数变更必须处理自由添加的模块，冲突时返回明确提示。

## 技术候选
Three.js（渲染与选取）；CadQuery 或 build123d（CAD/STEP，二选一由实测决定）；OCCT/XCAF（STEP 装配导入）；FreeCAD（对照验证）；接口对齐与图谱是自有核心。BOM 按实际实例及版本聚合；切割长度按连接偏移计算，原材优化与锯缝另算。CAD 与视图来自同一图谱；不各自维护尺寸。

## 质量与安全
几何/装配/结构/制造分开验证；连通并不代表承载合格。载荷、跨度、连接件承载、挠度、稳定性、脚轮能力必须有证据。缺失时返回 NEEDS_REVIEW；工程审核前仅草案。导入模型禁止执行其中的宏或脚本；保留原始文件并隔离解析。

## 部署边界更新
依据 [ADR-001](WEB-YIDA-DEPLOYMENT.md)：浏览器轻量编辑器处理常见变换及 BOM；独立按需 CAD/AI 服务；Repository 接口隔离 LocalAdapter 与 YidaAdapter；图谱快照为唯一设计真值，BOM 为派生数据。宜搭优先业务数据/权限/流程，模型文件受控存储。初期不要求服务器或完整 FreeCAD 桌面运行环境；实际 WebGL、鉴权、API 和权限待验证。

## 外部资产与编辑边界
[ADR-002](PART-ASSET-CONTRACT.md) 定义 GLB + JSON + 可选 STEP 的零件包、截面生成器、坐标转换、固定/参数化/外部件分类及最小验收。所有装配和加工操作修改统一图谱；几何、接口和 BOM 联动更新。外部软件不绑定部署环境。

## AI-first 接口约束（ADR-004）
[统一 AI 设计操作契约](AI-DESIGN-INTERFACE.md)：外部 MCP 和内置 AI 共用 Design Action API，未来与手工 UI 共用操作入口；现有 UI 仍调用图谱函数。离线 `design-actions.cjs` 已验证白名单批处理、别名、只读副本预览、diff/BOM 与失败不提交。生产鉴权、版本冲突、确认提交、模型服务、MCP transport、聊天及线上同步未实现。

## 三级资源库（ADR-005）
[模型与模块库](MODEL-LIBRARY.md)：零件定义、功能模块、可配置完整模型分层；模型级语义尺寸映射到图谱，使用同一工具 API，避免把常规设计变成每次AI重建。V0.3-A 首个工作桌模型及共享配置函数已实现，模块库尚待开发。
