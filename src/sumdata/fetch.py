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
from .catalog import CATALOG, dataset_spec;
from .datasets import data_home;

BASE="https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/datasets/";

def fetch_dataset(name, destination=None, overwrite=False):
    spec=dataset_spec(name); root=data_home(destination); root.mkdir(parents=True, exist_ok=True); target=root/spec.csv_name;
    if target.exists() and not overwrite: return target;
    request=Request(BASE+spec.csv_name, headers={"User-Agent":"sumData/0.1.0a1"});
    with urlopen(request, timeout=30) as response: payload=response.read();
    target.write_bytes(payload); return target;

def fetch_all(destination=None, overwrite=False):
    paths=[]; seen=set();
    for spec in CATALOG:
        if spec.csv_name in seen: continue;
        seen.add(spec.csv_name);
        try: paths.append(fetch_dataset(spec.name, destination, overwrite));
        except Exception as exc: print("warning: {}: {}".format(spec.name, exc));
    return tuple(paths);

def main(argv=None):
    parser=argparse.ArgumentParser(description="Download R datasets CSV files into the external sumData cache.");
    parser.add_argument("--dataset", action="append", default=[]); parser.add_argument("--destination"); parser.add_argument("--overwrite", action="store_true"); args=parser.parse_args(argv);
    if args.dataset:
        for name in args.dataset: print(fetch_dataset(name,args.destination,args.overwrite));
    else:
        for path in fetch_all(args.destination,args.overwrite): print(path);
    return 0;
