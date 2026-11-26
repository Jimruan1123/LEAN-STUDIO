# EXP-002-A | 开源能力继承实测
2026-11-26。CadQuery 2.8.0 实际运行：6 项通过，详见 result.json。
运行：安装 requirements-exp002.txt 后执行 python -m engine.exp002，重新生成 STEP 与 JSON。STEP 输出在聊天运行环境已生成；仓库通过脚本复现，不提交二进制附件。

## 采用决策
- CadQuery（Apache 2.0，安装包元数据）：直接依赖原生 B-rep、Location、Assembly、布尔交集与 STEP round trip。OCCT 经 CadQuery/OCP 调用；依赖许可证及发布义务仍需完整清查。
- Assembly4：参考 LCS 对接思想，自主编写坐标变换，未复制插件源码，未运行 FreeCAD。https://github.com/oursland/FreeCAD_Assembly4
- FrameForge：参考型材裁切、偏移、斜切、修剪；尚未运行，未复制源码。https://github.com/lukh/frameforge
- FreeCAD 内置 Assembly 与专业插件：下一阶段实际 APP 操作对标，优先研究可复用操作及数据契约。
- CadQuery 官方铝型材装配案例：https://cadquery.readthedocs.io/en/latest/assy.html
- Three.js：后续视图依赖，尚未接入。

## 验收边界
自主示例：管外径28、内径26、套筒内径28.4、外径34、长度50，轴向间隙2 mm。仅几何演示，无供应商规格依据，非可采购件，非真实夹紧连接。位置由局部坐标系直接计算，不是通用约束求解。三件共轴实例，未验证多分支或任意角接头；未验证载荷、紧固件、可制造性。现有抽象图谱 EXP-001 与本模块尚未集成。G1 仍 OPEN。

下一步：复现 FreeCAD/FrameForge/Assembly4 中的型材与接头流程；对照许可及实际运行；选取真实获授权供应商接头与用户工装，扩充 LCS 接口、自由装配与 SOP 模板共用数据结构。
