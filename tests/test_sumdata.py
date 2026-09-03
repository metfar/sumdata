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
from sumdata import DATASET_ITEMS, dataset, dataset_names, dataset_spec;

def test_catalog_has_contractual_108_items():
    assert len(DATASET_ITEMS)==108; assert len(dataset_names())==108;

def test_alias_metadata():
    spec=dataset_spec("BJsales.lead"); assert spec.family=="BJsales";

def test_mtcars_generated():
    frame=dataset("mtcars"); assert len(frame)==32; assert frame["mpg"][0]==21; assert frame.names[0]=="mpg";
