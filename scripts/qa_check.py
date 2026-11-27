#!/usr/bin/env python3
"""Deterministic, lightweight visual delivery checks for art-direction-learning.

Zero mandatory third-party dependencies (Python 3.9+ stdlib works out of the box for
dimension/aspect-ratio checks and SVG safe-zone overlay previews). Automatically uses
Pillow, zxingcpp, pyzbar, OpenCV, zbarimg, or macOS sips when installed for publish-size
QR decoding and advisory brand HEX sampling.
"""

from __future__ import annotations

import argparse
import base64
import json
import math
import os
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


SAFE_ZONE_PRESETS: dict[str, dict[str, float]] = {
    # Per M-033 (TikTok / Reels / Shorts / Douyin conservative 9:16 UI occlusion margins)
    "9:16": {"top": 0.14, "bottom": 0.22, "left": 0.06, "right": 0.15},
    "tiktok": {"top": 0.14, "bottom": 0.22, "left": 0.06, "right": 0.15},
    "reels": {"top": 0.14, "bottom": 0.20, "left": 0.06, "right": 0.14},
    "4:5": {"top": 0.05, "bottom": 0.08, "left": 0.05, "right": 0.05},
    "2:3": {"top": 0.05, "bottom": 0.05, "left": 0.05, "right": 0.05},
    "margin-5pct": {"top": 0.05, "bottom": 0.05, "left": 0.05, "right": 0.05},
}


def parse_ratio(text: str) -> float:
    if ":" in text:
        a, b = text.split(":", 1)
        return float(a) / float(b)
    if "/" in text:
        a, b = text.split("/", 1)
        return float(a) / float(b)
    return float(text)


def _read_png_size(data: bytes) -> tuple[int, int] | None:
    if len(data) >= 24 and data[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", data[16:24])
        return int(w), int(h)
    return None


def _read_gif_size(data: bytes) -> tuple[int, int] | None:
    if len(data) >= 10 and data[:6] in (b"GIF87a", b"GIF89a"):
        w, h = struct.unpack("<HH", data[6:10])
        return int(w), int(h)
    return None


def _read_webp_size(data: bytes) -> tuple[int, int] | None:
    if len(data) < 30 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None
    chunk = data[12:16]
    if chunk == b"VP8X" and len(data) >= 30:
        w = 1 + int.from_bytes(data[24:27], "little")
        h = 1 + int.from_bytes(data[27:30], "little")
        return w, h
    if chunk == b"VP8 " and len(data) >= 30:
        w = struct.unpack("<H", data[26:28])[0] & 0x3FFF
        h = struct.unpack("<H", data[28:30])[0] & 0x3FFF
        return int(w), int(h)
    if chunk == b"VP8L" and len(data) >= 25:
        bits = struct.unpack("<I", data[21:25])[0]
        w = (bits & 0x3FFF) + 1
        h = ((bits >> 14) & 0x3FFF) + 1
        return int(w), int(h)
    return None


def _read_jpeg_size(path: Path) -> tuple[int, int] | None:
    with path.open("rb") as fh:
        if fh.read(2) != b"\xff\xd8":
            return None
        while True:
            byte = fh.read(1)
            if not byte:
                return None
            if byte != b"\xff":
                continue
            marker = fh.read(1)
            while marker == b"\xff":
                marker = fh.read(1)
            if not marker:
                return None
            m = marker[0]
            if m in (0xD8, 0xD9, 0x01) or (0xD0 <= m <= 0xD7):
                continue
            seg_len_bytes = fh.read(2)
            if len(seg_len_bytes) < 2:
                return None
            seg_len = struct.unpack(">H", seg_len_bytes)[0]
            if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                sof = fh.read(5)
                if len(sof) < 5:
                    return None
                h, w = struct.unpack(">HH", sof[1:5])
                return int(w), int(h)
            fh.seek(seg_len - 2, os.SEEK_CUR)


def get_image_dimensions(path: Path) -> tuple[int, int]:
    try:
        from PIL import Image  # type: ignore

        with Image.open(path) as img:
            return int(img.width), int(img.height)
    except Exception:
        pass

    head = path.read_bytes()[:64]
    for reader in (_read_png_size, _read_gif_size, _read_webp_size):
        size = reader(head)
        if size:
            return size
    jpeg_size = _read_jpeg_size(path)
    if jpeg_size:
        return jpeg_size

    if shutil.which("sips"):
        proc = subprocess.run(
            ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
            capture_output=True,
            text=True,
        )
        if proc.returncode == 0:
            w = h = None
            for line in proc.stdout.splitlines():
                if "pixelWidth:" in line:
                    w = int(line.split(":")[-1].strip())
                elif "pixelHeight:" in line:
                    h = int(line.split(":")[-1].strip())
            if w and h:
                return w, h

    raise ValueError(f"Unable to determine image dimensions for {path}")


def check_dimensions(
    width: int,
    height: int,
    expected_ratio: str | None,
    ratio_tolerance: float,
    min_width: int | None,
    min_height: int | None,
) -> dict[str, Any]:
    actual_ratio = round(width / height, 4) if height else 0.0
    issues: list[str] = []
    if min_width and width < min_width:
        issues.append(f"width {width}px < min_width {min_width}px")
    if min_height and height < min_height:
        issues.append(f"height {height}px < min_height {min_height}px")
    target_ratio = None
    if expected_ratio:
        target_ratio = round(parse_ratio(expected_ratio), 4)
        if abs(actual_ratio - target_ratio) / max(target_ratio, 1e-6) > ratio_tolerance:
            issues.append(
                f"aspect ratio {actual_ratio} ({width}x{height}) deviates from expected {expected_ratio} ({target_ratio}) beyond {ratio_tolerance*100:.1f}%"
            )
    return {
        "status": "fail" if issues else "pass",
        "width": width,
        "height": height,
        "aspect_ratio": actual_ratio,
        "expected_ratio": expected_ratio,
        "issues": issues,
    }


def _downscale_image(src: Path, dst: Path, publish_width: int, orig_width: int, orig_height: int) -> tuple[bool, str]:
    if orig_width <= publish_width:
        shutil.copyfile(src, dst)
        return True, "original_within_publish_width"
    target_height = max(1, round(orig_height * (publish_width / orig_width)))
    try:
        from PIL import Image  # type: ignore

        with Image.open(src) as img:
            resized = img.resize((publish_width, target_height), Image.Resampling.LANCZOS)
            resized.save(dst, format="PNG")
        return True, f"pillow_resized_{publish_width}x{target_height}"
    except Exception:
        pass

    if shutil.which("sips"):
        proc = subprocess.run(
            ["sips", "-Z", str(max(publish_width, target_height)), "-s", "format", "png", str(src), "--out", str(dst)],
            capture_output=True,
            text=True,
        )
        if proc.returncode == 0 and dst.is_file():
            return True, f"sips_resized_{publish_width}px"

    shutil.copyfile(src, dst)
    return False, "unresized_no_resizer_available"


def _decode_qr(image_path: Path) -> tuple[str | None, list[str]]:
    # 1. zxingcpp
    try:
        import zxingcpp  # type: ignore
        from PIL import Image  # type: ignore

        with Image.open(image_path) as img:
            results = zxingcpp.read_barcodes(img)
        return "zxingcpp", [r.text for r in results if getattr(r, "text", None)]
    except Exception:
        pass

    # 2. pyzbar
    try:
        from pyzbar.pyzbar import decode  # type: ignore
        from PIL import Image  # type: ignore

        with Image.open(image_path) as img:
            results = decode(img)
        return "pyzbar", [r.data.decode("utf-8", errors="replace") for r in results]
    except Exception:
        pass

    # 3. OpenCV
    try:
        import cv2  # type: ignore

        img = cv2.imread(str(image_path))
        if img is not None:
            detector = cv2.QRCodeDetector()
            ok, decoded_info, _, _ = detector.detectAndDecodeMulti(img)
            if ok and decoded_info:
                return "opencv", [t for t in decoded_info if t]
            text, _, _ = detector.detectAndDecode(img)
            return "opencv", [text] if text else []
    except Exception:
        pass

    # 4. zbarimg CLI
    if shutil.which("zbarimg"):
        proc = subprocess.run(["zbarimg", "--raw", "-q", str(image_path)], capture_output=True, text=True)
        if proc.returncode in (0, 4):
            lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
            return "zbarimg", lines

    return None, []


def check_qr(
    path: Path,
    orig_width: int,
    orig_height: int,
    publish_width: int,
    expected_url: str | None,
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        test_img = Path(tmp) / "publish_preview.png"
        resized_ok, resize_method = _downscale_image(path, test_img, publish_width, orig_width, orig_height)
        decoder, decoded = _decode_qr(test_img)

    if decoder is None:
        return {
            "status": "skipped_missing_decoder",
            "publish_width": publish_width,
            "resize_method": resize_method,
            "decoded_values": [],
            "hint": "Install a QR decoder (e.g. `pip install zxing-cpp pillow` or `brew install zbar`) or scan at publish size on a real phone camera before delivery.",
        }

    issues: list[str] = []
    if not resized_ok and orig_width > publish_width:
        issues.append(f"could not downscale from {orig_width}px to publish width {publish_width}px")
    if not decoded:
        issues.append(f"no QR code decoded at publish width {publish_width}px using {decoder}")
    elif expected_url:
        norm_expected = expected_url.strip().rstrip("/")
        matched = any(val.strip().rstrip("/") == norm_expected for val in decoded)
        if not matched:
            issues.append(f"decoded QR payload {decoded!r} does not match expected URL {expected_url!r}")

    return {
        "status": "fail" if issues else "pass",
        "decoder": decoder,
        "publish_width": publish_width,
        "resize_method": resize_method,
        "decoded_values": decoded,
        "expected_url": expected_url,
        "issues": issues,
    }


def write_safe_zone_overlay(
    image_path: Path,
    width: int,
    height: int,
    preset: str,
    out_path: Path,
    embed_image: bool = False,
) -> dict[str, Any]:
    margins = SAFE_ZONE_PRESETS[preset]
    top_h = round(height * margins["top"])
    bot_h = round(height * margins["bottom"])
    left_w = round(width * margins["left"])
    right_w = round(width * margins["right"])
    safe_x = left_w
    safe_y = top_h
    safe_w = max(1, width - left_w - right_w)
    safe_h = max(1, height - top_h - bot_h)

    if embed_image:
        ext = image_path.suffix.lower().lstrip(".")
        mime = "jpeg" if ext in ("jpg", "jpeg") else (ext or "png")
        b64 = base64.b64encode(image_path.read_bytes()).decode("ascii")
        href = f"data:image/{mime};base64,{b64}"
    else:
        href = image_path.resolve().as_uri()

    font_size = max(16, round(min(width, height) * 0.024))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <title>Safe-Zone QA Overlay ({preset}) — {image_path.name}</title>
  <image href="{href}" x="0" y="0" width="{width}" height="{height}" preserveAspectRatio="none"/>
  <!-- Translucent UI occlusion danger zones -->
  <rect x="0" y="0" width="{width}" height="{top_h}" fill="#EF4444" fill-opacity="0.34"/>
  <rect x="0" y="{height - bot_h}" width="{width}" height="{bot_h}" fill="#EF4444" fill-opacity="0.34"/>
  <rect x="0" y="{top_h}" width="{left_w}" height="{safe_h}" fill="#EF4444" fill-opacity="0.28"/>
  <rect x="{width - right_w}" y="{top_h}" width="{right_w}" height="{safe_h}" fill="#EF4444" fill-opacity="0.34"/>
  <!-- Safe content boundary -->
  <rect x="{safe_x}" y="{safe_y}" width="{safe_w}" height="{safe_h}" fill="none" stroke="#22C55E" stroke-width="{max(2, round(min(width, height) * 0.004))}" stroke-dasharray="14 8"/>
  <g font-family="system-ui, -apple-system, Helvetica, Arial, sans-serif" font-weight="700" font-size="{font_size}" fill="#FFFFFF">
    <text x="{round(width * 0.04)}" y="{max(font_size + 8, round(top_h * 0.55))}">TOP UI ZONE ({int(margins['top']*100)}% / {top_h}px)</text>
    <text x="{round(width * 0.04)}" y="{height - max(12, round(bot_h * 0.45))}">BOTTOM CAPTION / CTA UI ZONE ({int(margins['bottom']*100)}% / {bot_h}px)</text>
    <text x="{safe_x + 14}" y="{safe_y + font_size + 12}" fill="#22C55E">SAFE AREA: {safe_w}×{safe_h}px ({preset})</text>
  </g>
</svg>
'''
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(svg, encoding="utf-8")
    return {
        "status": "generated",
        "preset": preset,
        "output_path": str(out_path.resolve()),
        "safe_box_px": {"x": safe_x, "y": safe_y, "width": safe_w, "height": safe_h},
    }


def _hex_to_rgb(code: str) -> tuple[int, int, int]:
    cleaned = code.strip().lstrip("#")
    if len(cleaned) != 6:
        raise ValueError(f"Invalid HEX color: {code}")
    return int(cleaned[0:2], 16), int(cleaned[2:4], 16), int(cleaned[4:6], 16)


def sample_brand_hex_advisory(path: Path, hex_codes: list[str]) -> dict[str, Any]:
    try:
        from PIL import Image  # type: ignore
    except Exception:
        return {
            "status": "skipped_missing_pillow",
            "advisory_only": True,
            "note": "Brand HEX sampling is advisory only (never a hard fail for photographic lighting). Install Pillow to enable pixel sampling.",
        }

    with Image.open(path) as img:
        rgb = img.convert("RGB")
        rgb.thumbnail((240, 240))
        pixels = list(rgb.getdata())

    results = []
    for code in hex_codes:
        tr, tg, tb = _hex_to_rgb(code)
        min_dist = min(math.sqrt((r - tr) ** 2 + (g - tg) ** 2 + (b - tb) ** 2) for r, g, b in pixels)
        near_ratio = sum(
            1 for r, g, b in pixels if math.sqrt((r - tr) ** 2 + (g - tg) ** 2 + (b - tb) ** 2) <= 28.0
        ) / max(len(pixels), 1)
        results.append({
            "brand_hex": f"#{code.strip().lstrip('#').upper()}",
            "min_rgb_distance": round(min_dist, 2),
            "near_match_pixel_ratio": round(near_ratio, 4),
        })

    return {
        "status": "advisory",
        "advisory_only": True,
        "note": "Advisory sampling for solid/vector brand regions; lighting/shadows in photography naturally shift RGB values.",
        "samples": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", help="Path to rendered artwork (PNG/JPG/WEBP/GIF)")
    parser.add_argument("--expected-ratio", help="Expected aspect ratio, e.g. 9:16, 2:3, 16:9, 1:1")
    parser.add_argument("--ratio-tolerance", type=float, default=0.02, help="Relative ratio tolerance (default: 0.02)")
    parser.add_argument("--min-width", type=int, help="Minimum required pixel width")
    parser.add_argument("--min-height", type=int, help="Minimum required pixel height")
    parser.add_argument("--check-qr", action="store_true", help="Verify QR readability at publish display width")
    parser.add_argument("--publish-width", type=int, default=375, help="Simulated publish display width in px (default: 375)")
    parser.add_argument("--expected-url", help="Expected decoded QR URL (implies --check-qr)")
    parser.add_argument("--safe-zone-overlay", help="Output path for SVG safe-zone visual overlay preview")
    parser.add_argument("--safe-zone-preset", choices=sorted(SAFE_ZONE_PRESETS), default="9:16")
    parser.add_argument("--embed-image", action="store_true", help="Embed base64 image inside the overlay SVG")
    parser.add_argument("--brand-hex", nargs="*", help="Advisory-only user-specified brand HEX colors to sample (e.g. #0C224E #00A3E0)")

    args = parser.parse_args()
    image_path = Path(args.image).expanduser().resolve()
    if not image_path.is_file():
        print(json.dumps({"overall_status": "fail", "error": f"Image not found: {image_path}"}, ensure_ascii=False, indent=2))
        return 1

    width, height = get_image_dimensions(image_path)
    report: dict[str, Any] = {
        "image": str(image_path),
        "checks": {},
    }
    report["checks"]["dimensions"] = check_dimensions(
        width, height, args.expected_ratio, args.ratio_tolerance, args.min_width, args.min_height
    )

    if args.check_qr or args.expected_url:
        report["checks"]["qr_check"] = check_qr(
            image_path, width, height, args.publish_width, args.expected_url
        )

    if args.safe_zone_overlay:
        report["checks"]["safe_zone_overlay"] = write_safe_zone_overlay(
            image_path, width, height, args.safe_zone_preset, Path(args.safe_zone_overlay), embed_image=args.embed_image
        )

    if args.brand_hex:
        report["checks"]["brand_hex_advisory"] = sample_brand_hex_advisory(image_path, args.brand_hex)

    statuses = [
        check.get("status")
        for check in report["checks"].values()
        if not check.get("advisory_only")
    ]
    if "fail" in statuses:
        report["overall_status"] = "fail"
    elif any(str(st).startswith("skipped_") for st in statuses):
        report["overall_status"] = "needs_manual_or_decoder"
    else:
        report["overall_status"] = "pass"

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["overall_status"] == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
