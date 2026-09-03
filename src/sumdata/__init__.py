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
from .catalog import CATALOG, DATASET_ITEMS, DatasetSpec, dataset_names, dataset_spec;
from .datasets import dataset, data_home;
from .model import NA, SumVector, SumFactor, SumMatrix, SumDataFrame, SumTimeSeries, SumTable, SumList;
from .rds import read_rds, save_rds;
__version__="0.1.0a1";
readRDS=read_rds; saveRDS=save_rds;
