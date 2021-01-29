# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Command-line tools for demo module."""
import json
import random
from datetime import date, timedelta
from os.path import dirname, join

import click
from flask.cli import with_appcontext
from flask_principal import Identity
from invenio_access import any_user

from .services import Marc21DataType, Marc21RecordService
from .vocabularies import Vocabularies


def fake_access_right():
    """Generates a fake access_right."""
    vocabulary = Vocabularies.get_vocabulary("access_right")
    _type = random.choice(list(vocabulary.data.keys()))
    return _type


def fake_feature_date(days=365):
    """Generates a fake feature_date."""
    start_date = date.today()
    random_number_of_days = random.randrange(days)
    _date = start_date + timedelta(days=random_number_of_days)
    return _date.strftime("%Y-%m-%d")


def _load_json(filename):
    with open(join(dirname(__file__), filename), "rb") as fp:
        return json.load(fp)


def create_fake_record():
    """Create records for demo purposes."""
    data_to_use = _load_json("data/fake-record.json")
    data_acces = {
        "access_right": fake_access_right(),
        "embargo_date": fake_feature_date(),
    }

    # identity providing `any_user` system role
    identity = Identity(1)
    identity.provides.add(any_user)

    service = Marc21RecordService()

    draft = service.create(
        data=data_to_use,
        identity=identity,
        data_type=Marc21DataType.RECORD_FULL,
        access=data_acces,
    )

    record = service.publish(id_=draft.id, identity=identity)

    return record


def create_fake_metadata():
    """Create records for demo purposes."""
    data_to_use = "<record><controlfield tag='001'>990079940640203331</controlfield><controlfield tag='007'>cr</controlfield> <controlfield tag='008'>100504|1932</controlfield><controlfield tag='009'>AC08088803</controlfield><datafield tag='035' ind1=' ' ind2=' '><subfield code='a'>AC08088803</subfield></datafield><datafield tag='035' ind1=' ' ind2=' '><subfield code='a'>(AT-OBV)AC08088803</subfield><subfield code='a'>(Aleph)007994064ACC01</subfield><subfield code='a'>(DE-599)OBVAC08088803</subfield></datafield><datafield tag='245' ind1='0' ind2='0'><subfield code='a'>&lt;&lt;Die&gt;&gt; Internationale Werkbundsiedlung Wien 1932</subfield><subfield code='c'>hrsg. von Josef Frank</subfield></datafield></record>"
    data_acces = {
        "access_right": fake_access_right(),
        "embargo_date": fake_feature_date(),
    }

    # identity providing `any_user` system role
    identity = Identity(1)
    identity.provides.add(any_user)

    service = Marc21RecordService()

    draft = service.create(
        data=data_to_use,
        identity=identity,
        data_type=Marc21DataType.RECORD_METADATA,
        access=data_acces,
    )

    record = service.publish(id_=draft.id, identity=identity)

    return record


@click.group()
def marc21():
    """InvenioMarc21 records commands."""
    pass


@marc21.command("demo")
@with_appcontext
def demo():
    """Create 10 fake records for demo purposes."""
    click.secho("Creating demo records...", fg="blue")

    for _ in range(5):
        create_fake_metadata()

    for _ in range(5):
        create_fake_record()

    click.secho("Created records!", fg="green")
