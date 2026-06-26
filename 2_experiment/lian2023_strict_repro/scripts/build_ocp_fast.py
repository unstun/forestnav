from __future__ import annotations

import os
import platform
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "lian2023_strict" / "cpp" / "ocp_fast.cpp"
PKG = ROOT / "src" / "lian2023_strict"


def shared_suffix() -> str:
    if platform.system() == "Darwin":
        return ".dylib"
    return ".so"


def main() -> int:
    if not SRC.exists():
        raise SystemExit(f"missing source: {SRC}")
    cxx = os.environ.get("CXX") or shutil.which("clang++") or shutil.which("g++") or "c++"
    out = PKG / f"_ocp_fast_lib{shared_suffix()}"
    cmd = [cxx, "-O3", "-std=c++17", "-fPIC", str(SRC), "-o", str(out)]
    if platform.system() == "Darwin":
        cmd.insert(4, "-dynamiclib")
    else:
        cmd.insert(4, "-shared")
    subprocess.run(cmd, cwd=str(ROOT), check=True)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
