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
import csv;
import os;
from .catalog import dataset_spec, dataset_names;
from .model import NA, SumDataFrame;

_MTCARS = [
("Mazda RX4",21,6,160,110,3.90,2.620,16.46,0,1,4,4),("Mazda RX4 Wag",21,6,160,110,3.90,2.875,17.02,0,1,4,4),("Datsun 710",22.8,4,108,93,3.85,2.320,18.61,1,1,4,1),("Hornet 4 Drive",21.4,6,258,110,3.08,3.215,19.44,1,0,3,1),("Hornet Sportabout",18.7,8,360,175,3.15,3.440,17.02,0,0,3,2),("Valiant",18.1,6,225,105,2.76,3.460,20.22,1,0,3,1),("Duster 360",14.3,8,360,245,3.21,3.570,15.84,0,0,3,4),("Merc 240D",24.4,4,146.7,62,3.69,3.190,20.00,1,0,4,2),("Merc 230",22.8,4,140.8,95,3.92,3.150,22.90,1,0,4,2),("Merc 280",19.2,6,167.6,123,3.92,3.440,18.30,1,0,4,4),("Merc 280C",17.8,6,167.6,123,3.92,3.440,18.90,1,0,4,4),("Merc 450SE",16.4,8,275.8,180,3.07,4.070,17.40,0,0,3,3),("Merc 450SL",17.3,8,275.8,180,3.07,3.730,17.60,0,0,3,3),("Merc 450SLC",15.2,8,275.8,180,3.07,3.780,18.00,0,0,3,3),("Cadillac Fleetwood",10.4,8,472,205,2.93,5.250,17.98,0,0,3,4),("Lincoln Continental",10.4,8,460,215,3.00,5.424,17.82,0,0,3,4),("Chrysler Imperial",14.7,8,440,230,3.23,5.345,17.42,0,0,3,4),("Fiat 128",32.4,4,78.7,66,4.08,2.200,19.47,1,1,4,1),("Honda Civic",30.4,4,75.7,52,4.93,1.615,18.52,1,1,4,2),("Toyota Corolla",33.9,4,71.1,65,4.22,1.835,19.90,1,1,4,1),("Toyota Corona",21.5,4,120.1,97,3.70,2.465,20.01,1,0,3,1),("Dodge Challenger",15.5,8,318,150,2.76,3.520,16.87,0,0,3,2),("AMC Javelin",15.2,8,304,150,3.15,3.435,17.30,0,0,3,2),("Camaro Z28",13.3,8,350,245,3.73,3.840,15.41,0,0,3,4),("Pontiac Firebird",19.2,8,400,175,3.08,3.845,17.05,0,0,3,2),("Fiat X1-9",27.3,4,79,66,4.08,1.935,18.90,1,1,4,1),("Porsche 914-2",26,4,120.3,91,4.43,2.140,16.70,0,1,5,2),("Lotus Europa",30.4,4,95.1,113,3.77,1.513,16.90,1,1,5,2),("Ford Pantera L",15.8,8,351,264,4.22,3.170,14.50,0,1,5,4),("Ferrari Dino",19.7,6,145,175,3.62,2.770,15.50,0,1,5,6),("Maserati Bora",15,8,301,335,3.54,3.570,14.60,0,1,5,8),("Volvo 142E",21.4,4,121,109,4.11,2.780,18.60,1,1,4,2)];

def _mtcars():
    names=("mpg","cyl","disp","hp","drat","wt","qsec","vs","am","gear","carb");
    return SumDataFrame({name:[row[index+1] for row in _MTCARS] for index,name in enumerate(names)}, [row[0] for row in _MTCARS], {"class":"data.frame","source":"generated SUM dataset"});

def data_home(path=None):
    if path is not None: return Path(path).expanduser();
    configured=os.environ.get("SUMDATA_HOME", "").strip();
    return Path(configured).expanduser() if configured else Path.home()/".local"/"share"/"sumdata"/"r-datasets";

def _coerce(text):
    value=str(text).strip();
    if value in ("", "NA", "NaN"): return NA;
    try:
        number=float(value);
        return int(number) if number.is_integer() else number;
    except ValueError: return value;

def _csv_dataset(path):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader=csv.DictReader(handle); rows=list(reader);
    if not rows: return SumDataFrame({});
    row_key="rownames" if "rownames" in rows[0] else None;
    keys=[key for key in rows[0] if key != row_key];
    columns={key:[_coerce(row.get(key,"")) for row in rows] for key in keys};
    row_names=[str(row.get(row_key,"")) for row in rows] if row_key else [];
    return SumDataFrame(columns, row_names, {"class":"data.frame","source":"Rdatasets CSV cache"});

def dataset(name, home=None):
    spec=dataset_spec(name);
    if spec.name.lower()=="mtcars": return _mtcars();
    root=data_home(home); path=root/spec.csv_name;
    if not path.exists():
        raise FileNotFoundError("Dataset '{}' is catalogued but not cached. Run: sumdata-fetch-r-datasets --dataset {}".format(spec.name, spec.name));
    return _csv_dataset(path);
