# 内嵌视觉锚点参考图目录 (`library/style-refs/`)

本目录与 `library/styles/` 中的实证风格母版一一对应，用于在本地存放用户精选的标杆海报原图，同时在推送至公开 Git 仓库时通过 `.gitignore` 自动过滤商用原图，避免版权风险。

## 目录结构与版权隔离规则

每当在 `library/styles/<style-id>.md` 完成一套实证风格母版提炼时，在此创建同名子目录：

```text
library/style-refs/
  <style-id>/
    descriptor.svg  <-- 随包分发的零版权可视化参考卡（色板 HEX、字阶、留白框、网格与光影示意，进 Git）
    local/          <-- 放入 2–3 张真实标杆海报原图（已被 .gitignore 忽略，不会上传 GitHub）
      .gitkeep
```

- **三级借用与缺图降级**：`library.py get <style-id>` 会自动探测 `local/` 原图与 `descriptor.svg`，返回 `anchor_tier`（`full_local_anchors` / `partial_local_anchors` / `descriptor_only` / `text_only`）。新机器尚未补齐 `local/` 时，`validate` 会给出 warning（不影响 `valid: true`），调用方按 `output-qa-gate.md` 降级至 `L2/L3` 并依托 `descriptor.svg` 与文字规范交付。
- **宁缺毋滥**：每个风格只需精选 **2–3 张**无网页导航栏、无促销弹窗、无水印的顶级标杆原图（也支持放入本团队自己实测满意的优秀成图作为长期锚点）。
- **Git 版权安全**：仓库根目录 `.gitignore` 已设置忽略 `library/style-refs/**/local/*`（仅保留 `.gitkeep`），确保第三方品牌商用图只留在本机、绝不误传至公开 GitHub；自绘的 `descriptor.svg` 无版权风险，随仓库直接同步。
