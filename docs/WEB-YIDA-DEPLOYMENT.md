# ADR-001｜轻量 Web + 数据库，宜搭优先
日期：2026-11-26。状态：路线已确认，技术与账号接入待验证。此 ADR 优先于旧路线中要求先完整完成 CAD 对标再开始 Web 的安排；不降低制造验收门槛。

## 最小部署
独立 HTTPS Web 编辑器：Three.js + TypeScript（候选 Vite，先不强制 React）；浏览器执行常见零件定位、尺寸和 BOM 联动；轻量图谱 JSON 是唯一设计真值。模型文件不重复存放于每个零件实例。初期本地存储或导入/导出 JSON，不要求后端。
宜搭优先承担项目、产品、零件元数据、设计版本、BOM、SOP、审批与权限管理。优先验证独立 Web 的外部链接及 iframe；嵌入失败可独立打开，不阻塞设计。可通过 OpenAPI 或自定义 HTTP 连接器对接。CAD/AI 服务仅在需要时启用；CadQuery/OCCT 可作为单一按需 Python 服务（候选 FastAPI），初期不建设微服务、容器集群、消息队列、通用约束求解器、完整桌面 CAD 替代品。FreeCAD 和插件是研发参考/验证工具，不是最终用户依赖。
数据层定义 Repository 接口，初期 LocalAdapter，后续 YidaAdapter；只有宜搭实际限制需要时才引入独立 SQL 存储。宜搭表单不是高吞吐几何数据库；大文件通过受控附件/对象存储引用，权限、版本、hash 可追溯。每个项目版本用一个不可变图谱快照，BOM 是可重建的派生数据，保存采用 revision 校验，避免双写；API 密钥仅服务端保管。鉴权、租户隔离和文件授权先于共享部署。

## 迭代交付
| 版本（规划） | 可体验成果 | 最小验收 |
|---|---|---|
| V0.2 | 独立 Web 小型编辑器，自由搭建精益管 + 标准铝型材台 | 旋转/缩放/选件，添加/删除、1500→1800、BOM、JSON 保存重载；实际浏览器证据 |
| V0.3 | 装配接口与配件，非标模块加入标准台 | 直角/分支连接、吸附、撤销、两主线及混合回归；无全量 CAD 依赖 |
| V0.4 | 宜搭最小集成 | 一个项目表/版本表，保存、读取、重开同一设计、权限检查；外链及 iframe 二选一通过，分别记录结果 |
| V0.5 | AI 操作与按需 CAD | 自然语言生成/修改图谱，diff、确认、回滚；调用 CAD 导出 STEP 并与 BOM 核对 |
| V0.6+ | 供应商、用户模型、工程知识和校核扩展 | 有权使用的数据、导入识别与现场工程审核；先标注未验证再升级 |
版本编号为计划而非发布状态；可根据证据调整顺序，宜搭接入技术探针提前并行，不等完整编辑器。用户模型/供应商资源及成熟 APP 对标也并行推进，每次只研究当前迭代需要的能力。保留旧 Gate 作为能力验收清单，不作为必须串行完成的瀑布流程。

## YIDA 最小技术探针（未执行）
P1：通过 HTTPS 托管 Web 页面，在企业账号验证外链与 iframe、桌面浏览器和钉钉客户端的 WebGL、CSP/frame-ancestors、登录与跨域。
P2：测试最小表单 CRUD、版本冲突、字段/附件大小、调用配额、权限、审计；先使用非敏感示例数据。确认账号套餐、应用授权和可用 API。
P3：保存一个图谱 JSON，退出后重新加载，验证版本 ID、BOM 和几何一致。P4：测试宜搭 HTTP 连接器调用小型只读服务；不将 token 暴露前端。
回退：独立 Web + 本地 JSON，或需要时受控 SQLite/Postgres 服务；不要求先解决宜搭登录才开始原型。GitHub 私有仓库用于代码版本管理，不等同可访问的 HTTPS 部署。

## 官方文档（2026-11-26 核查）
- 自定义页及表单 CRUD：https://developers.aliwork.com/docs/guide/about
- 开发中心 / iframe：https://developers.aliwork.com/
- 外部链接等页面类型：https://docs.aliwork.com/docs/developer/usage/newApp
- HTML/Iframe：https://docs.aliwork.com/docs/yida_support/_8/zqpbaq/hndctc
- 自定义连接器：https://docs.aliwork.com/docs/yida_subject/_2/gtkly9/stbfik
- API 概览：https://docs.aliwork.com/docs/developer/api/about

上述仅文档可行性，不证明当前企业账号授权、嵌入 WebGL、性能、存储或部署已经通过。
