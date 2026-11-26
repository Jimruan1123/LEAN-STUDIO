# ADR-004 | AI-first 设计入口及统一操作契约
状态：产品方向已确认；离线操作接口 probe 已验证，尚无 MCP 服务、聊天窗口、模型调用或线上写入。适用于 20/30/40 铝型材首期（目前 Web 引擎仅 4040t）；28mm 延后。以本 ADR 约束后续研发。

## 产品定位
AI 根据自然语言/约束生成方案、选择零件、搭建、修改、检查；人负责需求、审阅、必要的手工编辑与工程批准。自由非标设计与 SOP 标准产品配置同等重要。不能把产品退化为只供手工拖拽的 CAD 或只能修改固定模板的配置器。所有新增底层能力必须可无界面调用、可发现、可测试。

## 统一架构
手工 UI / 内置聊天（未来） / 外部 MCP（未来） -> 意图与计划 -> Design Action API -> Assembly Graph + 装配规则 -> Three.js / BOM / 数据存取。
UI 和模型最终使用同一命令层、同一图谱；现有 UI 仍直接调用图谱函数，后续渐进迁移，保留功能回归。AI 不能执行任意 JS、直接改渲染对象、绕过约束或伪造 BOM。外部 MCP 客户端不直接操作浏览器 DOM。
MCP 是工具接入协议，不是几何引擎；未来本地 stdio 或远程鉴权 HTTP 服务按客户端支持决定。静态 GitHub Pages 不能单独运行服务端 MCP 或保存 API 密钥；远程访问须有授权的设计会话、数据持久化和命令同步，YIDA 或其他适配器负责业务数据。模型提供商/客户端/部署方式待验证，先不选定。
参考：https://ts.sdk.modelcontextprotocol.io/v2/get-started/first-server

## 现阶段可执行契约 probe
apps/studio-web-v02d/design-actions.cjs，Node/CommonJS，无新增依赖，无网络，无 UI 绑定；基于当前 graph.js。
preview(graph,{contract:"lean-actions/0.1",actions:[{op,args},...]})，1–200 个白名单操作；所有数值使用 mm，工程右手 Z-up；批内以 $alias 引用新建实例；ID 不允许猜测，未来通过查询发现。返回 ok、preview_only、graph、diff（零件新增/删除/变更 ID 与装配边数量变化）、bom、aliases；失败返回失败步骤与错误，不提交部分结果。
当前十类动作：create_profile、connect、move_part、resize_part、add_end_cap、detach、remove_part、convert_to_free、create_space_frame、resize_frame。以 adapter 参数规则为当前实验定义；不是完整公开 MCP 工具 schema。模板覆盖已有模型必须显式 replace_existing=true；预览永不写入原图谱。图谱验证仍沿用 V0.2-F 的有限规则，不等同完整几何、碰撞或工程检查。所有结果 NEEDS_REVIEW。
验证：node test-design-actions.cjs；基线 graph.js 30 项通过；7 项 adapter 测试通过（无 UI 自由双端装配、500→800 联动、模板转自由、错误批次原图谱不变、显式覆盖、参数/未知工具/alias 校验、确定性）。源码 blob 与测试对应。

## 未来工具与事务边界（规划）
get_capabilities / list_catalog / get_design / list_templates / list_modules / query_interfaces / get_selection / validate_design / preview_actions / commit_actions / undo / generate_bom / export_design。按需增加 replace_part、add_module、rotate、copy、工程校核等；不宣称当前支持。每个操作提供机器可读 JSON Schema、能力状态、语义单位、限制和错误类型。能力必须服务自由及标准设计；AI 可复用设计知识、参数化模板和标准模块，不能被限定只能调用整套模板。
事务：读取 project/design ID + revision；模型生成 action plan，明确假设/缺失需求；在副本预检与预览；返回 preview_id、diff、告警/BOM；用户确认后服务端校验相同 base_revision、授权、请求幂等性及预览摘要；以单次事务提交，冲突返回新版本要求重算；成功推送图谱/视图刷新、审计及可撤销版本。风险/权限/结构与采购审批必须独立；禁止任意代码执行或未经授权的外部发送。preview_id/revision/CAS/鉴权/真正提交与持久化尚未实现，不可把本次 preview 当成生产 API。
输出中区分设计草案、几何检查、装配兼容、工程审核。未知承载及采购型号不猜测，AI 不得直接批准制造或下料。

## 迭代门
下一轮继续基础搭建与 SOP 工作台、20/30 扩展，不安装 MCP、不接模型、不做聊天 UI。每轮功能新增必须同时定义/测试结构化操作，逐步迁移 UI。待底层能力可用后，先验证不依赖模型的命令批次（从空白非标设计、标准工作台改尺寸并增配件、闭环拒绝、撤销与存取），再以独立本地 MCP 或模型工具调用试验接自然语言，最终按需要接入 YIDA/内置聊天。两条路线同一接口；不要重复构建引擎。实际 AI 设计、模型选择、完整 JSON Schema、并发提交、授权、审计、MCP 握手与 UI 同步均 OPEN。
