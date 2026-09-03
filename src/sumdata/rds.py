#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#pylint:disable=W0301
#  
#  Copyright 2018- William Martinez Bas <metfar@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
def read_rds(path):
    try:
        import pyreadr;
    except ImportError as exc:
        raise RuntimeError("Reading external .rds files requires optional dependency pyreadr: pip install pyreadr") from exc;
    result=pyreadr.read_r(str(path));
    if not result: return None;
    if len(result)==1: return next(iter(result.values()));
    return dict(result);

def save_rds(path, value):
    try:
        import pyreadr;
    except ImportError as exc:
        raise RuntimeError("Writing external .rds files requires optional dependency pyreadr: pip install pyreadr") from exc;
    if not hasattr(pyreadr,"write_rds"): raise RuntimeError("Installed pyreadr does not provide write_rds()");
    pyreadr.write_rds(str(path), value); return str(path);
