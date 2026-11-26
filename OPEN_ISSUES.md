# OPEN ISSUE LIST

| ID | 优先级 | 问题 | 状态 |
|---|---|---|---|
| OI-001 | P0 | GitHub 私有仓库初始化，基线文件已写入 | CLOSED |
| OI-002 | P0 | 20/30/40 方形铝型材供应商系列、截面及连接规格待确定 | OPEN |
| OI-003 | P0 | 用户自有装配样本、BOM 与来源权限尚未提供 | OPEN |
| OI-004 | P0 | 候选开源许可证、版本、安装和联合运行待核验 | OPEN |
| OI-005 | P0 | CAD 及 WebGL 环境实测，STEP 保留装配层级 | OPEN |
| OI-006 | P0 | 装配接口、切割偏移、紧固件、合法重叠规则未实现 | OPEN |
| OI-007 | P1 | 工程载荷、跨距、稳定性、安全与实际制造审核 | OPEN |
| OI-008 | P1 | 受限资料存储及权限审批方案 | OPEN |
| OI-009 | P0 | AI 统一操作接口：离线 preview probe 已测；完整 schema、UI 统一入口、版本/授权/提交/撤销、MCP 与模型接入待实施 | PARTIAL |
| OI-010 | P0 | 宜搭账号授权、HTTPS 外链/iframe、WebGL、API CRUD、配额与权限实测 | OPEN |
| OI-011 | P0 | V0.2 轻量 Web 双主线编辑器，JSON 保存重载与浏览器实测 | OPEN |

| OI-012 | P2 | 28 mm 精益管材料体系扩展 | DEFERRED |
| OI-013 | P0 | V0.2-D Three.js r180 CDN/本地 HTTP、WebGL2 及实际 GLB 渲染、选取、尺寸联动验证（当前环境 DNS/浏览器策略受限） | PARTIAL |
| OI-014 | P1 | 自由模式多端关联、任意方向与 SOP 工作台/混合配置；当前仅 XZ 单端吸附及固定框架 | OPEN |

2026-11-26 用户侧截图确认 GitHub Pages 可访问，Three.js r180/GLB 视口已显示 4040t 框架，UI 显示 28 实例及 36 关系。用户浏览器的初步渲染证据，不等同于旋转、拾取、参数变化、吸附、碰撞及 YIDA 验收。截图含浏览器私人界面，不上传公开仓库。OI-013 保留后续交互验证。

ADR-004：V0.2-F 现有图谱 30 项及离线 action probe 7 项测试通过；不等同线上 MCP、自然语言或聊天功能实现。

| OI-015 | P1 | 标准模型库 V0.3-A 首个工作桌已实现；模块、模型分类/缩略图、任意槽高、混合参数保持、保存标准模型及工程检查待完成 | PARTIAL |

2026-11-26 V0.3-A.1: 用户报告模型库不明显及黑屏；模型库入口上移并增加预览示意，移除环境贴图生成、简化灯光、模板变更自动取景、首帧/异常提示。81项图谱/API/DOM测试通过；真实WebGL及Pages线上验收仍OPEN，黑屏根因未确认。

2026-11-26 V0.3-A.2 correction: user reports black-colored profiles, not a black viewport. Five GLBs checked: NORMAL absent, winding consistent. Runtime normal reconstruction + neutral silver material and ambient light; unlit diagnostic query added. Local graph/API/model/DOM regressions passed, actual WebGL color and Pages deployment still unverified. OI-013 remains PARTIAL.

V0.3-B.1 custom slot height implemented for manual attachment and offline AI actions. Default workdesk rails, arbitrary-height drag snapping, plates/modules and live WebGL verification remain open.

V0.3-B.2: standard workdesk height and tabletop controls now implemented; support edges are conceptual. Shelf/module library, board fastening, overhang, load check and live WebGL acceptance remain open.
