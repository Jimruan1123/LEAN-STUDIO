# ADR-002｜外部零件生产与 Web 装配 / 数字零件契约
状态：方向确认；以下格式、坐标及操作分类为 V0.2 建议工程契约，待实测，不是已发布接口。补充 ADR-001。
## 职责
任何合法工具（Blender、FreeCAD、SolidWorks、CadQuery、供应商 CAD、自有装配）均可生产零件；经标准化及审核后导入。YIDA 承载轻量 Three.js 装配编辑器及数据/审批，不要求宜搭原生实现 CAD；嵌入受限时独立 Web 外链。复杂几何、精确 STEP 与分析按需外部服务。双主线自由设计与 SOP 产品共用零件契约。
## 文件与坐标
一个零件包：part.json（必需）、part.glb（固定件/预览必需，程序生成件可选）、part.step（精确工程源可选）、section.json（参数化截面件按需）、thumbnail（可选）。图谱与参数采用 mm、右手 Z-up，GLB/glTF 2.0 标准采用米、右手 Y-up；导入边界显式转换，如工程坐标 (x,y,z) mm 映射为渲染 (x,z,-y)/1000，反向同步，禁止重复缩放或轴转换。局部原点、基准面及接口随坐标变换；GLB 不提供工程设计历史，不可单独作为制造真值。原始模型可受控存储，引用 hash、版本、许可。供应商数据授权遵循 INGESTION。
## 编辑类型
A rigid：固定标准件；位姿、实例复制、规格替换，禁止几何缩放。
B parametric：直管、型材、平板等白名单几何；长度、宽度、厚度在许可范围内，以截面/轮廓或已定义生成器重建，不对带孔/螺纹/接头整体非均匀缩放。孔径、截面、壁厚、接口按参数规则保持或更新；供应商不可调规格通过替换型号实现。复杂开孔/倒角/布尔、折弯及精确 CAD 操作后置，未定义时拒绝并转外部。
C external：复杂自制或外购件，仅刚体装配；几何改造外部完成并导入新版本，旧设计继续引用旧版本。所有变更输出 diff，联动位姿、接口、尺寸、BOM、工程审核状态。
## 元数据必需项
schema_version、part_id、revision、name、category、edit_mode、source、license_status、geometry_ref/hash（如有）、geometry_generator（如有）、units、coordinate_system、local_origin、dimensions、parameters（类型/默认值/范围/步长/驱动关系）、interfaces（ID、位置、方向、兼容族、安装偏移及插深）、procurement（料号/计量单位/采购方式）、engineering_status。未知值显式 null，禁止自动认定承载。可选 supplier SKU、材料、质量、价格、截面惯性矩、载荷证据。模板/图谱只引用零件 ID+版本及实例参数；不可把 GLB 复制到每条实例记录。
## V0.2 最小试验
- A：导入一个外部 GLB 固定接头与元数据，定位/旋转/替换，禁止缩放。来源自主或授权。
- B：一个直管、一个型材、一个板材，验证 500→800 长度、25→30 板厚（示例参数），截面、孔径（如有）、接口、BOM 同步；超范围拒绝。
- C：同一零件用于自由框架及 SOP 工作台；修改 1500→1800，附加模块后保存 JSON，再打开复现。
- D：两个不同生产工具输出同类零件的标准化测试（候选 CadQuery、Blender）；坐标/尺寸/接口/版本校验。不要求两套软件都成为部署依赖。
- E：宜搭实际嵌入或外链，验证导入/装配/参数改动、存储重载、权限与浏览器能力。未接入时独立 Web 验证，不声称宜搭通过。
所有示例件为非制造认证件。真实采购、下料及承载仍待审核。
## 参考
https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html
https://threejs.org/docs/pages/GLTFLoader.html
