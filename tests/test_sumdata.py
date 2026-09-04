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

def test_co2_urls_preserve_case():
    from sumdata.fetch import CASE_SAFE_REF, _candidate_urls;
    upper=_candidate_urls(dataset_spec("CO2")); lower=_candidate_urls(dataset_spec("co2"));
    assert upper[0].endswith("/CO2.csv"); assert lower[0].endswith("/co2.csv"); assert upper[0]!=lower[0];
    assert CASE_SAFE_REF in upper[0]; assert CASE_SAFE_REF in lower[0];

def test_co2_payload_schema_validation():
    from sumdata.fetch import _valid_payload;
    upper=b"rownames,Plant,Type,Treatment,conc,uptake\n1,Qn1,Quebec,nonchilled,95,16\n";
    lower=b"rownames,time,value\n1,1959,315.42\n";
    assert _valid_payload(dataset_spec("CO2"),upper); assert not _valid_payload(dataset_spec("CO2"),lower);
    assert _valid_payload(dataset_spec("co2"),lower); assert not _valid_payload(dataset_spec("co2"),upper);

def test_fetch_cli_version(capsys):
    from sumdata.fetch import main;
    import pytest;
    with pytest.raises(SystemExit) as exc: main(["--version"]);
    assert exc.value.code==0; assert "0.1.0a2" in capsys.readouterr().out;

def test_case_colliding_dataset_names_are_distinct():
    assert dataset_spec("CO2").name=="CO2"; assert dataset_spec("co2").name=="co2";


def test_sumdata_cli_version(capsys):
    from sumdata.cli import main;
    import pytest;
    with pytest.raises(SystemExit) as exc: main(["--version"]);
    assert exc.value.code==0; assert "0.1.0a2" in capsys.readouterr().out;
