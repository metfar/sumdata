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
import argparse;
from . import __version__, dataset_names;

def main(argv=None):
    parser=argparse.ArgumentParser(prog="sumdata",description="SUM common data layer.");
    parser.add_argument("--version",action="version",version="sumData {}".format(__version__));
    parser.add_argument("--list-r-datasets",action="store_true",help="list the contractual R datasets catalog");
    args=parser.parse_args(argv);
    if args.list_r_datasets:
        for name in dataset_names(display=True): print(name);
        return 0;
    parser.print_help(); return 0;
