# 内嵌视觉锚点参考图目录 (`library/style-refs/`)

本目录与 `library/styles/` 中的实证风格母版一一对应，用于在本地存放用户精选的标杆海报原图，同时在推送至公开 Git 仓库时通过 `.gitignore` 自动过滤商用原图，避免版权风险。

## 目录结构与版权隔离规则

每当在 `library/styles/<style-id>.md` 完成一套实证风格母版提炼时，在此创建同名子目录：

```text
library/style-refs/
  <style-id>/
    local/          <-- 放入 2–3 张真实标杆海报原图（已被 .gitignore 忽略，不会上传 GitHub）
      .gitkeep
```

- **本地开箱即用**：Agent 选中某个已入库风格母版后，自动检查 `library/style-refs/<style-id>/local/` 是否存在参考图；如有，直接作为 Layer 1 生图模型的光影、构图与质感锚点图传入（若单图体积过大，先本地压缩为 `~1000px / 150 KB` 轻量版本再传给生图模型）。
- **宁缺毋滥**：每个风格只需精选 **2–3 张**无网页导航栏、无促销弹窗、无水印的顶级标杆原图（也支持放入本团队自己实测满意的优秀成图作为长期锚点）。
- **Git 版权安全**：仓库根目录 `.gitignore` 已设置忽略 `library/style-refs/**/local/*`（仅保留 `.gitkeep`），确保第三方品牌商用图只留在本机、绝不误传至公开 GitHub。
