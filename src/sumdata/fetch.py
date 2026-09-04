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
from pathlib import Path;
from urllib.request import Request, urlopen;
import argparse;
from . import __version__;
from .catalog import CATALOG, dataset_spec;
from .datasets import data_home;

PUBLISHED_BASE="https://vincentarelbundock.github.io/Rdatasets/csv/datasets/";
RAW_BASE="https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/datasets/";
AUCKLAND_BASE="https://www.stat.auckland.ac.nz/~wild/data/Rdatasets/csv/datasets/";
CASE_SAFE_REF="cc03c29690889dbe83089f5206e2422db8c3f71f";
CASE_SAFE_BASE="https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/{}/csv/datasets/".format(CASE_SAFE_REF);

def _candidate_urls(spec):
    primary=PUBLISHED_BASE+spec.csv_name;
    raw=RAW_BASE+spec.csv_name;
    mirror=AUCKLAND_BASE+spec.csv_name;
    # CO2 and co2 are distinct R datasets whose names differ only by case.
    # Pin them first to a known Rdatasets commit where both paths coexist
    # correctly; current mirrors may omit or collapse one of the names.
    if spec.name in ("CO2","co2"):
        pinned=CASE_SAFE_BASE+spec.csv_name;
        return (pinned,primary,raw,mirror);
    return (primary,raw,mirror);

def _valid_payload(spec,payload):
    if not payload: return False;
    header=payload.splitlines()[0].decode("utf-8",errors="replace").strip().lower();
    if spec.name=="CO2": return header=="rownames,plant,type,treatment,conc,uptake";
    if spec.name=="co2": return header=="rownames,time,value";
    return True;

def _read_url(url):
    request=Request(url,headers={"User-Agent":"sumData/{}".format(__version__)});
    with urlopen(request,timeout=30) as response: return response.read();

def fetch_dataset(name,destination=None,overwrite=False):
    spec=dataset_spec(name); root=data_home(destination); root.mkdir(parents=True,exist_ok=True); target=root/spec.csv_name;
    if target.exists() and not overwrite: return target;
    errors=[];
    for url in _candidate_urls(spec):
        try:
            payload=_read_url(url);
            if not _valid_payload(spec,payload): raise ValueError("unexpected CSV schema for {}".format(spec.name));
            target.write_bytes(payload); return target;
        except Exception as exc: errors.append((url,exc));
    detail="; ".join("{}: {}".format(url,exc) for url,exc in errors);
    raise RuntimeError("Unable to download {} ({})".format(spec.name,detail));

def fetch_all(destination=None,overwrite=False):
    paths=[]; seen=set();
    for spec in CATALOG:
        if spec.csv_name in seen: continue;
        seen.add(spec.csv_name);
        try: paths.append(fetch_dataset(spec.name,destination,overwrite));
        except Exception as exc: print("warning: {}: {}".format(spec.name,exc));
    return tuple(paths);

def main(argv=None):
    parser=argparse.ArgumentParser(description="Download R datasets CSV files into the external sumData cache.");
    parser.add_argument("--version",action="version",version="sumdata-fetch-r-datasets {}".format(__version__));
    parser.add_argument("--dataset",action="append",default=[]); parser.add_argument("--destination"); parser.add_argument("--overwrite",action="store_true"); args=parser.parse_args(argv);
    if args.dataset:
        for name in args.dataset: print(fetch_dataset(name,args.destination,args.overwrite));
    else:
        for path in fetch_all(args.destination,args.overwrite): print(path);
    return 0;
