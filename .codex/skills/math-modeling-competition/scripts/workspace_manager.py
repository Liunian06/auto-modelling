#!/usr/bin/env python3
"""创建或检查数学建模比赛工作目录。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


SUBDIRS = (
    "赛题",
    "参考论文",
    "工作区/数据",
    "工作区/代码",
    "工作区/结果",
    "工作区/图表",
    "工作区/日志",
    "工作区/论文",
    "复盘",
)
INVALID_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def configure_output() -> None:
    """固定中文 JSON 的输出编码。"""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8")


def emit(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def component(value: str, label: str) -> str:
    value = value.strip()
    if not value or value in {".", ".."}:
        raise ValueError(f"{label}不能为空或特殊路径")
    if INVALID_CHARS.search(value) or value.endswith((" ", ".")):
        raise ValueError(f"{label}包含 Windows 路径不允许的字符")
    return value


def workdir_path(value: str) -> Path:
    path = Path(value).expanduser().resolve()
    parts = [item.lower() for item in path.parts]
    if any(
        parts[index] == ".codex" and parts[index + 1] == "skills"
        for index in range(len(parts) - 1)
    ):
        raise ValueError("用户工作目录不能位于 .codex\\skills 中")
    return path


def year_month(value: str) -> str:
    value = value.strip()
    if not re.fullmatch(r"\d{6}", value):
        raise ValueError("比赛年月必须使用 YYYYMM 六位数字")
    if not 1 <= int(value[4:6]) <= 12:
        raise ValueError("比赛月份必须在 01 到 12 之间")
    return value


def edition_year(value: str) -> str:
    value = value.strip()
    if not re.fullmatch(r"\d{4}", value):
        raise ValueError("届次年份必须使用四位数字")
    return value


def identifier(value: str) -> str:
    value = value.strip()
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", value):
        raise ValueError("英文标识必须以字母开头，且只包含字母和数字")
    return value.upper()


def problem_name(value: str) -> str:
    value = component(value, "题号")
    if value.endswith("题"):
        value = value[:-1]
    value = component(value.strip().upper(), "题号")
    return f"{value}题"


def competition_name(args: argparse.Namespace) -> str:
    return (
        f"{year_month(args.year_month)}-"
        f"{component(args.chinese_name, '中文简称')}"
        f"{identifier(args.identifier)}"
        f"{edition_year(args.edition)}"
    )


def ensure_dir(
    path: Path,
    created: list[str],
    existing: list[str],
) -> None:
    if path.exists():
        if not path.is_dir():
            raise ValueError(f"路径已存在但不是文件夹：{path}")
        existing.append(str(path))
        return
    path.mkdir(parents=True, exist_ok=False)
    created.append(str(path))


def log_template(competition: str, problem: str) -> str:
    updated = datetime.now().astimezone().isoformat(timespec="seconds")
    return f"""# 赛中进度与交接日志

## 基本信息

- 比赛：{competition}
- 题号：{problem}
- 更新时间：{updated}
- 当前负责人：待填写

## 当前状态

- 所处阶段：待判断
- 赛中步骤：未开始
- 本轮目标：待填写
- 总体状态：目录已初始化

## 已完成事项

- 已创建统一比赛与赛题工作目录。

## 关键决定及依据

- 暂无。

## 已尝试方案

| 方案 | 状态 | 证据或结果 | 采用或放弃理由 |
|---|---|---|---|
| 暂无 | 未开始 | 暂无 | 暂无 |

## 关键文件

| 类型 | 路径 | 用途 | 状态 |
|---|---|---|---|
| 赛题 | 待填写 | 官方赛题与附件 | 待补充 |
| 数据 | 待填写 | 原始或处理后数据 | 待补充 |
| 代码 | 待填写 | 建模与验证代码 | 待补充 |
| 结果 | 待填写 | 模型结果或预测数据 | 待补充 |
| 论文 | 待填写 | LaTeX 源文件与 PDF | 待补充 |

## 未完成事项

- 确认当前属于赛前、赛中还是赛后。
- 整理已有材料。
- 明确下一步任务。

## 阻塞、风险与待确认

- 暂无。

## 下一步

1. 将官方赛题和附件放入 `赛题`。
2. 更新本日志中的当前阶段、本轮目标和关键文件。

## 交接说明

- 接手者首先阅读：本日志和 `赛题` 中的材料。
- 可以直接运行的命令：待填写。
- 不要重复的工作：待填写。
- 需要用户决定的事项：待填写。
"""


def init_workspace(args: argparse.Namespace) -> int:
    root = workdir_path(args.workdir)
    competition = competition_name(args)
    problems = list(dict.fromkeys(problem_name(item) for item in args.problems))
    created: list[str] = []
    existing: list[str] = []
    created_files: list[str] = []
    preserved_files: list[str] = []

    ensure_dir(root, created, existing)
    data_root = root / "data"
    contest_dir = data_root / competition
    ensure_dir(data_root, created, existing)
    ensure_dir(contest_dir, created, existing)

    problem_dirs: list[str] = []
    for problem in problems:
        problem_dir = contest_dir / f"{competition}-{problem}"
        ensure_dir(problem_dir, created, existing)
        for relative in SUBDIRS:
            ensure_dir(problem_dir / Path(relative), created, existing)

        log = problem_dir / "工作区" / "日志" / "赛中进度与交接日志.md"
        if log.exists():
            if not log.is_file():
                raise ValueError(f"日志路径已存在但不是文件：{log}")
            preserved_files.append(str(log))
        else:
            log.write_text(
                log_template(competition, problem),
                encoding="utf-8",
                newline="\n",
            )
            created_files.append(str(log))
        problem_dirs.append(str(problem_dir))

    emit(
        {
            "成功": True,
            "操作": "初始化",
            "工作目录": str(root),
            "数据根目录": str(data_root),
            "比赛目录": str(contest_dir),
            "赛题目录": problem_dirs,
            "新建目录": created,
            "已有目录": existing,
            "新建文件": created_files,
            "保留文件": preserved_files,
            "说明": "已有目录和日志均未覆盖。",
        }
    )
    return 0


def inspect_problem(path: Path) -> dict:
    missing = [
        str(path / Path(relative))
        for relative in SUBDIRS
        if not (path / Path(relative)).is_dir()
    ]
    log = path / "工作区" / "日志" / "赛中进度与交接日志.md"
    return {
        "赛题目录": str(path),
        "目录存在": path.is_dir(),
        "完整": path.is_dir() and not missing and log.is_file(),
        "缺失目录": missing,
        "主日志": str(log),
        "主日志存在": log.is_file(),
    }


def inspect_workspace(args: argparse.Namespace) -> int:
    root = workdir_path(args.workdir)
    competition = component(args.competition, "比赛目录名")
    contest_dir = root / "data" / competition

    if args.problem:
        path = contest_dir / f"{competition}-{problem_name(args.problem)}"
        result = inspect_problem(path)
        emit({"操作": "检查赛题", "工作目录": str(root), **result})
        return 0 if result["完整"] else 2

    if not contest_dir.is_dir():
        emit(
            {
                "成功": False,
                "操作": "检查比赛",
                "比赛目录": str(contest_dir),
                "问题": "比赛目录不存在",
            }
        )
        return 2

    prefix = f"{competition}-"
    paths = sorted(
        item
        for item in contest_dir.iterdir()
        if item.is_dir() and item.name.startswith(prefix)
    )
    results = [inspect_problem(path) for path in paths]
    complete = bool(results) and all(item["完整"] for item in results)
    emit(
        {
            "成功": complete,
            "操作": "检查比赛",
            "比赛目录": str(contest_dir),
            "赛题数量": len(results),
            "赛题": results,
        }
    )
    return 0 if complete else 2


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        description="创建或检查数学建模比赛统一工作目录。"
    )
    commands = root.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="初始化目录和交接日志")
    init.add_argument("--workdir", required=True, help="用户明确指定的工作目录")
    init.add_argument("--year-month", required=True, help="比赛年月 YYYYMM")
    init.add_argument("--chinese-name", required=True, help="中文简称")
    init.add_argument("--identifier", required=True, help="英文标识")
    init.add_argument("--edition", required=True, help="届次年份")
    init.add_argument("--problems", nargs="+", required=True, help="题号列表")
    init.set_defaults(handler=init_workspace)

    inspect = commands.add_parser("inspect", help="检查已有比赛或赛题目录")
    inspect.add_argument("--workdir", required=True, help="用户明确指定的工作目录")
    inspect.add_argument("--competition", required=True, help="完整比赛目录名")
    inspect.add_argument("--problem", help="可选题号；省略时检查整场比赛")
    inspect.set_defaults(handler=inspect_workspace)
    return root


def main() -> int:
    configure_output()
    args = parser().parse_args()
    try:
        return args.handler(args)
    except (OSError, ValueError) as exc:
        emit({"成功": False, "操作": args.command, "错误": str(exc)})
        return 1


if __name__ == "__main__":
    sys.exit(main())
