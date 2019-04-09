#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2019 Chintalagiri Shashank
#
# This file is part of tendril.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from decimal import Decimal
from tendril.schema.base import SchemaControlledYamlFile
from tendril.schema.helpers import SchemaSelectableObjectSet
from tendril.schema.helpers import MultilineString
from tendril.config import instance_path
from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)


class TendrilSignatory(object):
    def __init__(self, parent, name, designation):
        self.parent = parent
        self.name = name
        self.designation = designation

    def __repr__(self):
        return "<TendrilSignatory {0}, {1}>" \
               "".format(self.name, self.designation)


class TendrilBankAccountInfo(object):
    def __init__(self, parent, accno, bank_name,
                 branch_address, branch_code, micr, ifsc):
        self.parent = parent
        self.accno = accno
        self.bank_name = bank_name
        self.branch_address = branch_address
        self.branch_code = branch_code
        self.micr = micr
        self.ifsc = ifsc


class TendrilSignatories(SchemaSelectableObjectSet):
    def __init__(self, signatories):
        super(TendrilSignatories, self).__init__(
            signatories, TendrilSignatory)


class TendrilBankAccounts(SchemaSelectableObjectSet):
    def __init__(self, bank_accounts):
        super(TendrilBankAccounts, self).__init__(
            bank_accounts, TendrilBankAccountInfo)


class TendrilPersona(SchemaControlledYamlFile):
    supports_schema_name = 'TendrilPersona'
    supports_schema_version_max = Decimal('1.0')
    supports_schema_version_min = Decimal('1.0')

    def __init__(self, *args, **kwargs):
        self._signatory = kwargs.get('signatory', None)
        self._bank_account = kwargs.get('bank_account', None)
        super(TendrilPersona, self).__init__(*args, **kwargs)

    def elements(self):
        e = super(TendrilPersona, self).elements()
        e.extend([
            ('_ident', ('identity', 'ident'), None),
            ('name', ('identity', 'name'), None),
            ('name_full', ('identity', 'name_full'), None),
            ('name_short', ('identity', 'name_short'), None),
            ('phone', ('identity', 'phone'), None),
            ('email', ('identity', 'email'), None),
            ('website', ('identity', 'website'), None),
            ('address', ('identity', 'address'), MultilineString),
            ('address_line', ('identity', 'address_line'), None),
            ('iec', ('identity', 'iec'), None),
            ('pan', ('identity', 'pan'), None),
            ('cin', ('identity', 'cin'), None),
            ('gstin', ('identity', 'gstin'), None),
            ('logo', ('identity', 'logo'), instance_path),
            ('black_logo', ('identity', 'black_logo'), instance_path),
            ('square_logo', ('identity', 'square_logo'), instance_path),
            ('signatories', ('identity', 'signatories'), TendrilSignatories),
            ('bank_accounts', ('identity', 'bank_accounts'), TendrilBankAccounts)
        ])
        return e

    def schema_policies(self):
        policies = super(TendrilPersona, self).schema_policies()
        policies.update({})
        return policies

    @property
    def ident(self):
        return self._ident

    @property
    def signatory(self):
        return self.signatories[self._signatory]

    @signatory.setter
    def signatory(self, value):
        if value not in self.signatories.keys():
            raise ValueError("Unrecognized Signatory : {0}".format(value))
        self._signatory = value

    @property
    def bank_account(self):
        return self.bank_accounts[self._bank_account]

    @bank_account.setter
    def bank_account(self, value):
        if value not in self.bank_accounts.keys():
            raise ValueError("Unrecognized Bank Account : {0}".format(value))
        self._bank_account = value

    def __repr__(self):
        return "<TendrilPersona {0} {1}>".format(self.ident, self.path)


def load(manager):
    logger.debug("Loading {0}".format(__name__))
    manager.load_schema('TendrilPersona', TendrilPersona,
                        doc="Schema for Tendril Persona Definition Files")
