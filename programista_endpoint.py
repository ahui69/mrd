#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FastAPI Router for Programista (Dev Tools)
"""

from __future__ import annotations
import os
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from programista import Programista

router = APIRouter(prefix="/api/dev", tags=["dev"])

# Auth
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "changeme")

def _auth(req: Request):
    tok = (req.headers.get("Authorization", "") or "").replace("Bearer ", "").strip()
    if tok != AUTH_TOKEN:
        raise HTTPException(401, "unauthorized")

# ── Models
class ExecRequest(BaseModel):
    cmd: str
    cwd: Optional[str] = None
    timeout: Optional[float] = None
    confirm: bool = False
    dry_run: bool = False
    shell: bool = False

class ProjectInitRequest(BaseModel):
    name: str
    kind: str = "py-lib"

class DepsAddRequest(BaseModel):
    project: str
    pkgs: List[str]
    tool: str = "pip"
    confirm: bool = False
    dry_run: bool = False

class GitRequest(BaseModel):
    project: str
    args: str
    confirm: bool = False
    dry_run: bool = False

class QARequest(BaseModel):
    project: str
    checks: List[str]
    confirm: bool = False
    dry_run: bool = False

class WriteFileRequest(BaseModel):
    path: str
    content: str

class SearchRequest(BaseModel):
    path: str = "."
    pattern: str

# ── Global instance
prog = Programista(root=os.getenv("DEV_ROOT", "/workspace"))

# ── Endpoints

@router.get("/snapshot")
def get_snapshot(_=Depends(_auth)):
    """📸 Get system snapshot (tools available)"""
    return prog.snapshot()

@router.post("/exec")
def exec_command(body: ExecRequest, _=Depends(_auth)):
    """🔧 Execute shell command (requires confirm=True)"""
    result = prog.exec(
        cmd=body.cmd,
        cwd=body.cwd,
        timeout=body.timeout,
        confirm=body.confirm,
        dry_run=body.dry_run,
        shell=body.shell
    )
    if not result.get("ok"):
        raise HTTPException(400, result.get("error", "exec failed"))
    return result

@router.post("/project/init")
def project_init(body: ProjectInitRequest, _=Depends(_auth)):
    """🏗️ Create new project scaffold"""
    result = prog.project_init(name=body.name, kind=body.kind)
    if not result.get("ok"):
        raise HTTPException(400, result.get("error", "init failed"))
    return result

@router.post("/deps/add")
def deps_add(body: DepsAddRequest, _=Depends(_auth)):
    """📦 Add dependencies to project"""
    result = prog.deps_add(
        project=body.project,
        pkgs=body.pkgs,
        tool=body.tool,
        confirm=body.confirm,
        dry_run=body.dry_run
    )
    if not result.get("ok"):
        raise HTTPException(400, result.get("error", "deps failed"))
    return result

@router.post("/qa")
def qa_check(body: QARequest, _=Depends(_auth)):
    """✅ Run QA checks (ruff/black/mypy/pytest)"""
    result = prog.qa(
        project=body.project,
        checks=body.checks,
        confirm=body.confirm,
        dry_run=body.dry_run
    )
    return result

@router.post("/git/init")
def git_init(project: str, confirm: bool = False, dry_run: bool = False, _=Depends(_auth)):
    """🔧 Initialize git repo"""
    result = prog.git_init(project=project, confirm=confirm, dry_run=dry_run)
    if not result.get("ok"):
        raise HTTPException(400, result.get("error", "git init failed"))
    return result

@router.post("/git")
def git_command(body: GitRequest, _=Depends(_auth)):
    """🔧 Execute git command"""
    result = prog.git(
        project=body.project,
        args=body.args,
        confirm=body.confirm,
        dry_run=body.dry_run
    )
    if not result.get("ok"):
        raise HTTPException(400, result.get("error", "git failed"))
    return result

@router.post("/file/write")
def write_file(body: WriteFileRequest, _=Depends(_auth)):
    """📝 Write file"""
    result = prog.write_file(path=body.path, content=body.content)
    return result

@router.get("/file/read")
def read_file(path: str, _=Depends(_auth)):
    """📖 Read file"""
    result = prog.read_file(path=path)
    if not result.get("ok"):
        raise HTTPException(404, result.get("error", "not found"))
    return result

@router.post("/search")
def search_files(body: SearchRequest, _=Depends(_auth)):
    """🔍 Search in files (regex)"""
    result = prog.search(path=body.path, pattern=body.pattern)
    return result

@router.get("/tree")
def file_tree(path: str = ".", max_depth: int = 4, _=Depends(_auth)):
    """🌳 Get file tree"""
    result = prog.tree(path=path, max_depth=max_depth)
    return result

@router.post("/dockerize")
def dockerize(project: str, kind: str = "py", _=Depends(_auth)):
    """🐳 Generate Dockerfile + docker-compose"""
    result = prog.dockerize(project=project, kind=kind)
    if not result.get("ok"):
        raise HTTPException(400, result.get("error", "dockerize failed"))
    return result
