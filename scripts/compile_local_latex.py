#!/usr/bin/env python3
"""Compile the article with pdflatex and bibtex."""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from loguru import logger


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

ARTICLE_DIR = PROJECT_ROOT
ARTICLE_FILE = ARTICLE_DIR / "main.tex"
ARTICLE_JOB_NAME = "main"
AUXILIARY_SUFFIXES = {
  ".aux",
  ".bbl",
  ".blg",
  ".lof",
  ".log",
  ".lot",
  ".out",
  ".synctex.gz",
  ".toc",
  ".xwm",
}


def setup_logger() -> None:
  """Set up file and console logging."""
  log_file = LOGS_DIR / "compile_local_latex.log"

  logger.remove()
  logger.add(
    log_file,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
    level="DEBUG",
    encoding="utf-8",
    mode="w",
  )
  logger.add(
    sys.stderr,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
    level="INFO",
  )


def run_tool(tool: str, arguments: list[str]) -> None:
  executable = shutil.which(tool)
  if executable is None:
    raise RuntimeError(
      f"'{tool}' was not found on PATH. Install MiKTeX or add it to PATH."
    )

  subprocess.run(
    [executable, *arguments],
    cwd=ARTICLE_DIR,
    check=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    encoding="utf-8",
    errors="replace",
  )


def clean_auxiliary_files() -> None:
  removed = 0
  for path in ARTICLE_DIR.iterdir():
    if path.is_file() and any(
      path.name.endswith(suffix) for suffix in AUXILIARY_SUFFIXES
    ):
      path.unlink()
      removed += 1
  logger.info(f"Removed {removed} auxiliary file(s).")


def main() -> int:
  setup_logger()
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument(
    "--clean",
    action="store_true",
    help="remove auxiliary files before compiling",
  )
  args = parser.parse_args()
  logger.info(f"Starting article compilation with --clean={args.clean}")

  if not ARTICLE_FILE.exists():
    error_msg = f"File not found: {ARTICLE_FILE}"
    logger.error(error_msg)
    print(error_msg, file=sys.stderr)
    return 1

  try:
    if args.clean:
      clean_auxiliary_files()

    latex_arguments = [
      "-interaction=nonstopmode",
      "-halt-on-error",
      "-file-line-error",
      ARTICLE_FILE.name,
    ]
    run_tool("pdflatex", latex_arguments)
    run_tool("bibtex", [ARTICLE_JOB_NAME])
    run_tool("pdflatex", latex_arguments)
    run_tool("pdflatex", latex_arguments)

  except subprocess.CalledProcessError as error:
    error_msg = f"Compilation failed with exit code {error.returncode}."
    logger.error(error_msg)
    print(error_msg, file=sys.stderr)
    output = error.stdout or ""
    if output:
      logger.error("\nLast compiler messages:")
      logger.error("".join(output.splitlines(keepends=True)[-40:]))
      print("\nLast compiler messages:", file=sys.stderr)
      print("".join(output.splitlines(keepends=True)[-40:]), file=sys.stderr)
    return error.returncode or 1

  except RuntimeError as error:
    error_msg = str(error)
    logger.error(error_msg)
    print(error_msg, file=sys.stderr)
    return 1

  success_msg = f"Compilation completed: {ARTICLE_DIR / 'main.pdf'}"
  logger.info(success_msg)
  print(success_msg)
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
