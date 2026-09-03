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
from dataclasses import dataclass, field;

class _NA:
    def __repr__(self): return "NA";
    def __bool__(self): raise ValueError("NA has no truth value");
NA = _NA();

@dataclass
class SumVector:
    values: list;
    names: list = field(default_factory=list);
    attrs: dict = field(default_factory=dict);
    def __iter__(self): return iter(self.values);
    def __len__(self): return len(self.values);
    def __getitem__(self, key): return self.values[key];

@dataclass
class SumFactor(SumVector):
    levels: list = field(default_factory=list);
    ordered: bool = False;

@dataclass
class SumMatrix:
    values: list;
    nrow: int;
    ncol: int;
    row_names: list = field(default_factory=list);
    col_names: list = field(default_factory=list);
    attrs: dict = field(default_factory=dict);

@dataclass
class SumDataFrame:
    columns: dict;
    row_names: list = field(default_factory=list);
    attrs: dict = field(default_factory=dict);
    def __len__(self): return len(next(iter(self.columns.values()), []));
    def __getitem__(self, key): return self.columns[key];
    @property
    def names(self): return tuple(self.columns);
    def rows(self): return [dict(zip(self.columns, values)) for values in zip(*self.columns.values())];

@dataclass
class SumTimeSeries(SumVector):
    start: object = None;
    frequency: float = 1.0;

@dataclass
class SumTable:
    values: object;
    dimensions: tuple = ();
    dimnames: dict = field(default_factory=dict);

@dataclass
class SumList:
    values: list;
    names: list = field(default_factory=list);
    attrs: dict = field(default_factory=dict);
