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
from dataclasses import dataclass;
import re;

DATASET_ITEMS = ['AirPassengers', 'BJsales', 'BJsales.lead (BJsales)', 'BOD', 'CO2', 'ChickWeight', 'DNase', 'EuStockMarkets', 'Formaldehyde', 'HairEyeColor', 'Harman23.cor', 'Harman74.cor', 'Indometh', 'InsectSprays', 'JohnsonJohnson', 'LakeHuron', 'LifeCycleSavings', 'Loblolly', 'Nile', 'Orange', 'OrchardSprays', 'PlantGrowth', 'Puromycin', 'Seatbelts', 'Theoph', 'Titanic', 'ToothGrowth', 'UCBAdmissions', 'UKDriverDeaths', 'UKgas', 'USAccDeaths', 'USArrests', 'USJudgeRatings', 'USPersonalExpenditure', 'UScitiesD', 'VADeaths', 'WWWusage', 'WorldPhones', 'ability.cov', 'airmiles', 'airquality', 'anscombe', 'attenu', 'attitude', 'austres', 'beaver1 (beavers)', 'beaver2 (beavers)', 'cars', 'chickwts', 'co2', 'crimtab', 'discoveries', 'esoph', 'euro', 'euro.cross (euro)', 'eurodist', 'faithful', 'fdeaths (UKLungDeaths)', 'freeny', 'freeny.x (freeny)', 'freeny.y (freeny)', 'gait', 'infert', 'iris', 'iris3', 'islands', 'ldeaths (UKLungDeaths)', 'lh', 'longley', 'lynx', 'mdeaths (UKLungDeaths)', 'morley', 'mtcars', 'nhtemp', 'nottem', 'npk', 'occupationalStatus', 'penguins', 'penguins_raw (penguins)', 'precip', 'presidents', 'pressure', 'quakes', 'randu', 'rivers', 'rock', 'sleep', 'stack.loss (stackloss)', 'stack.x (stackloss)', 'stackloss', 'state.abb (state)', 'state.area (state)', 'state.center (state)', 'state.division (state)', 'state.name (state)', 'state.region (state)', 'state.x77 (state)', 'sunspot.m2014 (sunspot.month)', 'sunspot.month', 'sunspot.year', 'sunspots', 'swiss', 'treering', 'trees', 'uspop', 'volcano', 'warpbreaks', 'women'];

@dataclass(frozen=True)
class DatasetSpec:
    item: str;
    name: str;
    family: str = "";
    csv_name: str = "";

def _parse(item):
    match=re.match(r"^(.+?) \((.+)\)$", item);
    if match: return DatasetSpec(item, match.group(1), match.group(2), match.group(1)+".csv");
    return DatasetSpec(item, item, "", item+".csv");

CATALOG = tuple(_parse(item) for item in DATASET_ITEMS);
BY_EXACT = {spec.name:spec for spec in CATALOG};
BY_FOLDED = {};
_AMBIGUOUS = set();
for spec in CATALOG:
    key=spec.name.casefold();
    if key in BY_FOLDED and BY_FOLDED[key].name!=spec.name: _AMBIGUOUS.add(key);
    else: BY_FOLDED[key]=spec;
for key in _AMBIGUOUS: BY_FOLDED.pop(key,None);

def dataset_names(display=False):
    return tuple(spec.item if display else spec.name for spec in CATALOG);

def dataset_spec(name):
    text=str(name).strip();
    if text in BY_EXACT: return BY_EXACT[text];
    key=text.casefold();
    if key in _AMBIGUOUS: raise KeyError("Ambiguous R dataset name (case matters): {}".format(name));
    if key not in BY_FOLDED: raise KeyError("Unknown R dataset: {}".format(name));
    return BY_FOLDED[key];
