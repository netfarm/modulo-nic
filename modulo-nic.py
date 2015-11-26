#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ft=python
#
# Modulo Registrazione Domini .it
# Copyright (c) 2011-2015 Gianluigi Tiesi <sherpya@netfarm.it>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# * Neither the name of the copyright holders nor the
# names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

__version__ = '0.3'

import os
import sys
import re
import codecs

from trml2pdf import trml2pdf

# some old version of trml2pdf does not defaults to utf-8
trml2pdf.encoding = 'utf-8'

# workaround to trml2pdf 0.3 with python2
def text_type(source):
    return source.decode('utf-8')
trml2pdf.text_type = text_type

from pdfrw import PdfReader, PdfWriter, PageMerge

import cgi
import cgitb

def getuvalue(self, key, default=None):
    value = self.getvalue(key, default)
    if type(value) == type(''):
        try:
            return value.decode('utf-8')
        except UnicodeDecodeError:
            return default
    return value

cgi.FieldStorage.getuvalue = getuvalue

if os.path.islink(sys.argv[0]):
    DATADIR = os.path.dirname(os.readlink(sys.argv[0]))
else:
    DATADIR = os.path.dirname(sys.argv[0])

re_email = re.compile(r'^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$')
re_cf    = re.compile(r'^\w\w\w\w\w\w\d\d\w\d\d\w\d\d\d\w$')
re_phone = re.compile(r'^\+\d\d\.[0-9]')

checked   = u'<unichar name="HEAVY CHECK MARK" />'
unchecked = u'<unichar name="LOWER RIGHT SHADOWED WHITE SQUARE" />'

_cf_odd =  [   1, 0, 5, 7, 9, 13, 15, 17, 19, 21,  # 0 - 9
               0, 0, 0, 0, 0, 0, 0,                # :;<=>?@
               1, 0, 5, 7, 9, 13, 15, 17, 19, 21,  # A-Z
               2, 4, 18, 20, 11, 3, 6, 8, 12, 14, 16, 10, 22, 25, 24, 23 ]
_cf_even = range(10) + [ 0, 0, 0, 0, 0, 0, 0 ] + range(26)

_province = [   u'AG', u'AL', u'AN', u'AO', u'AR', u'AP', u'AT', u'AV',
                u'BA', u'BT', u'BL', u'BN', u'BG', u'BI', u'BO', u'BZ',
                u'BS', u'BR', u'CA', u'CL', u'CB', u'CI', u'CE', u'CT',
                u'CZ', u'CH', u'CO', u'CS', u'CR', u'KR', u'CN', u'EN',
                u'FM', u'FE', u'FI', u'FG', u'FC', u'FR', u'GE', u'GO',
                u'GR', u'IM', u'IS', u'SP', u'AQ', u'LT', u'LE', u'LC',
                u'LI', u'LO', u'LU', u'MC', u'MN', u'MS', u'MT', u'ME',
                u'MI', u'MO', u'MB', u'NA', u'NO', u'NU', u'OT', u'OR',
                u'PD', u'PA', u'PR', u'PV', u'PG', u'PU', u'PE', u'PC',
                u'PI', u'PT', u'PN', u'PZ', u'PO', u'RG', u'RA', u'RC',
                u'RE', u'RI', u'RN', u'RM', u'RO', u'SA', u'VS', u'SS',
                u'SV', u'SI', u'SR', u'SO', u'TA', u'TE', u'TR', u'TO',
                u'OG', u'TP', u'TN', u'TV', u'TS', u'UD', u'VA', u'VE',
                u'VB', u'VC', u'VR', u'VV', u'VI', u'VT']

_iso3166_1 = [  u'AF', u'AX', u'AL', u'DZ', u'AS', u'AD', u'AO', u'AI', u'AQ',
                u'AG', u'AR', u'AM', u'AW', u'AU', u'AT', u'AZ', u'BS', u'BH',
                u'BD', u'BB', u'BY', u'BE', u'BZ', u'BJ', u'BM', u'BT', u'BO',
                u'BQ', u'BA', u'BW', u'BV', u'BR', u'IO', u'BN', u'BG', u'BF',
                u'BI', u'KH', u'CM', u'CA', u'CV', u'KY', u'CF', u'TD', u'CL',
                u'CN', u'CX', u'CC', u'CO', u'KM', u'CG', u'CD', u'CK', u'CR',
                u'CI', u'HR', u'CU', u'CW', u'CY', u'CZ', u'DK', u'DJ', u'DM',
                u'DO', u'EC', u'EG', u'SV', u'GQ', u'ER', u'EE', u'ET', u'FK',
                u'FO', u'FJ', u'FI', u'FR', u'GF', u'PF', u'TF', u'GA', u'GM',
                u'GE', u'DE', u'GH', u'GI', u'GR', u'GL', u'GD', u'GP', u'GU',
                u'GT', u'GG', u'GN', u'GW', u'GY', u'HT', u'HM', u'VA', u'HN',
                u'HK', u'HU', u'IS', u'IN', u'ID', u'IR', u'IQ', u'IE', u'IM',
                u'IL', u'IT', u'JM', u'JP', u'JE', u'JO', u'KZ', u'KE', u'KI',
                u'KP', u'KR', u'KW', u'KG', u'LA', u'LV', u'LB', u'LS', u'LR',
                u'LY', u'LI', u'LT', u'LU', u'MO', u'MK', u'MG', u'MW', u'MY',
                u'MV', u'ML', u'MT', u'MH', u'MQ', u'MR', u'MU', u'YT', u'MX',
                u'FM', u'MD', u'MC', u'MN', u'ME', u'MS', u'MA', u'MZ', u'MM',
                u'NA', u'NR', u'NP', u'NL', u'NC', u'NZ', u'NI', u'NE', u'NG',
                u'NU', u'NF', u'MP', u'NO', u'OM', u'PK', u'PW', u'PS', u'PA',
                u'PG', u'PY', u'PE', u'PH', u'PN', u'PL', u'PT', u'PR', u'QA',
                u'RE', u'RO', u'RU', u'RW', u'BL', u'SH', u'KN', u'LC', u'MF',
                u'PM', u'VC', u'WS', u'SM', u'ST', u'SA', u'SN', u'RS', u'SC',
                u'SL', u'SG', u'SX', u'SK', u'SI', u'SB', u'SO', u'ZA', u'GS',
                u'ES', u'LK', u'SD', u'SR', u'SJ', u'SZ', u'SE', u'CH', u'SY',
                u'TW', u'TJ', u'TZ', u'TH', u'TL', u'TG', u'TK', u'TO', u'TT',
                u'TN', u'TR', u'TM', u'TC', u'TV', u'UG', u'UA', u'AE', u'GB',
                u'US', u'UM', u'UY', u'UZ', u'VU', u'VE', u'VN', u'VG', u'VI',
                u'WF', u'EH', u'YE', u'ZM', u'ZW']

class validators:
    @staticmethod
    def domain(value):
        if not value.endswith('.it'): return False
        if value.count('.') != 1: return False
        if len(value) < 6: return False
        return True

    @staticmethod
    def email(value):
        return re_email.match(value) is not None

    @staticmethod
    def cf(value):
        if re_cf.match(value) is None:
            return False

        ctrlchar = ord(value[15].upper()) - 65
        value = map(lambda x: ord(x.upper()) - 48, value)
        checksum =  sum(map(lambda x: _cf_even[value[x]], xrange(1, 14, 2)))
        checksum += sum(map(lambda x: _cf_odd[value[x]],  xrange(0, 15, 2)))
        checksum %= 26
        return checksum == ctrlchar

    @staticmethod
    # Luhn - http://it.wikipedia.org/wiki/Partita_IVA
    def piva(value):
        if (len(value) != 11) or not value.isdigit():
            return False

        value = map(int, value)

        # dispari (odd)
        x = sum(map(lambda x: value[x], xrange(0, 10, 2)))

        # pari (even)
        y = 0
        for pos in xrange(1, 10, 2):
            c = 2 * value[pos]
            if c > 9: c -= 9
            y += c

        t = (x + y) % 10

        checksum = (10 - t) % 10
        return value[10] == checksum

    @staticmethod
    def cap(value):
        return (len(value) == 5) and value.isdigit()

    @staticmethod
    def iso(value):
        return value in _iso3166_1

    @staticmethod
    def province(value):
        return value in _province

    @staticmethod
    def text(value):
        return (len(value) > 4)

    @staticmethod
    def town(value):
        return (len(value) > 1)

    @staticmethod
    def digits(value):
        return (len(value) >= 5) and value.isdigit()

    @staticmethod
    def digits_optional(value):
        return (len(value) == 0) or validators.digits(value)

    @staticmethod
    def phone(value):
        return re_phone.match(value) is not None

    @staticmethod
    def phone_optional(value):
        return (len(value) == 0) or validators.phone(value)


_formfields = {
    'domain'        : (validators.domain, u'netfarm.it'),
    'registrant'    : (validators.text, u'Mario Rossi / ACME Inc.'),
    'cf'            : (validators.cf, u'RSSMRA60L01H501T'),
    'piva'          : (validators.piva, u'01538810506'),
    'address'       : (validators.text, u'Via Nazionale 10'),
    'cap'           : (validators.cap, u'56100'),
    'town'          : (validators.town, u'Pisa'),
    'province'      : (validators.province, u'PI'),
    'isocode'       : (validators.iso, u'IT'),
    'email'         : (validators.email, u'info@netfarm.it'),
    'phone'         : (validators.phone, u'+39.0500981576'),
    'fax'           : (validators.phone_optional, u'+39.0508665172'),
    'legalname'     : (validators.text, u'Giuseppe Garibaldi'),
    'legalcf'       : (validators.cf, u'GRBGPP07L04E425B'),
}

_notforsingle = ('legalname', 'legalcf', 'piva')
_upcase = ('province', 'isocode', 'legalcf')

def two_up(data):
    pdf = PdfReader(fdata=data)
    pages = PageMerge() + pdf.pages

    assert len(pages) == 2

    left, right = pages

    rotation = 270
    scale = 0.7071067811865476  # sqrt(0.5)

    x_increment = scale * pages.xobj_box[2]

    left.Rotate = rotation
    left.scale(scale)

    right.Rotate = rotation
    right.scale(scale)
    right.x = x_increment

    writer = PdfWriter()
    writer.addpage(pages.render())

    # retain and update metadata
    pdf.Info.Creator = 'modulo-nic.py %s' % __version__
    writer.trailer.Info = pdf.Info

    sys.stdout.write('Content-Type: application/x-pdf\n\n')
    writer.write(sys.stdout)

def pdf(fields):
    template = os.path.join(DATADIR, 'modulo-nic.rml')
    _input = codecs.open(template, 'r', 'utf-8').read()
    _input = _input % fields
    _input = _input.encode('utf-8')
    two_up(trml2pdf.parseString(_input))

def page():
    template = os.path.join(DATADIR, 'modulo-nic.html')
    template = codecs.open(template, 'r', 'utf-8').read()

    validated = True
    form = cgi.FieldStorage()

    fields = {  'version'   : unicode(__version__),
                'kind'      : form.getuvalue('kind', u'single').strip(),
                'debug'     : unicode(form)
    }

    submit = bool(form.getuvalue('submit', False))

    for sect in ('sect3', 'sect5'):
        value = form.getuvalue(sect, u'no').strip().lower()
        if value == u'yes':
            fields[sect + '_yes'] = u'checked="checked"'
            fields[sect + '_no'] = u''
            fields[sect + '_mandatory'] = u'&nbsp;'
        else:
            fields[sect + '_yes'] = u''
            fields[sect + '_no'] = u'checked="checked"'
            fields[sect + '_mandatory'] = u'<span class="red">È necessario accettare</span>'
            validated = False

    privacy = form.getuvalue('privacy', u'no').strip().lower()
    if privacy == u'yes':
        fields['privacy'] = 'SI'
        fields['privacy_yes'] = u'checked="checked"'
        fields['privacy_no'] = u''
        fields['privacy_tick_yes'] = checked
        fields['privacy_tick_no'] = unchecked
    else:
        fields['privacy'] = 'NO'
        fields['privacy_yes'] = u''
        fields['privacy_no'] = u'checked="checked"'
        fields['privacy_tick_yes'] = unchecked
        fields['privacy_tick_no'] = checked

    for key in _formfields.keys():
        fields[key + '_msg'] = u'<span class="black">es. %s</span>' % _formfields[key][1]

        value = form.getuvalue(key, u'').strip()
        fields[key] = value

        if not submit:
            continue

        if fields['kind'] == u'company':
            if key == 'cf': continue
        elif fields['kind'] == u'single' and (key in _notforsingle):
            continue

        valid = _formfields[key][0](value)
        validated = validated and valid

        if valid:
            if len(value):
                fields[key +'_msg'] = u'<span class="green">OK</span>'
        else:
            fields[key + '_msg'] = u'<span class="red">Non valido</span>'


    for up in _upcase:
        fields[up] = fields[up].upper()

    if submit:
        address = u'<i>%(address)s %(cap)s %(town)s (%(province)s)</i>' % fields

        if len(fields['fax']) > 0:
            fields['faxline'] = u'numero di fax <i>%(fax)s</i>,' % fields
        else:
            fields['faxline'] = u''

        # Persona fisica
        if fields['kind'] == u'single':
            fields['registrant_label'] = u'Il richiedente'
            fields['cfpivaHdr'] = u'codice fiscale'
            fields['cfpiva'] = fields['cf']
            fields['fulladdress'] = u'residente in ' + address
            fields['nation'] = u'Nazionalità <i>' + fields['isocode'] + u'</i>'
            fields['legal'] = u''
        # Aziende
        elif fields['kind'] == u'company':
            fields['registrant_label'] = 'L\'organizzazione'
            fields['cfpivaHdr'] = u'partita IVA'
            fields['cfpiva'] = fields['piva']
            fields['fulladdress'] = u'con sede in ' + address
            fields['nation'] = u'Nazione <i>' + fields['isocode'] + u'</i>'
            fields['legal'] =  u'rappresentata legalmente da <i>' + fields['legalname'] + u'</i>'
            fields['legal'] += u' codice fiscale <i>' + fields['legalcf'] + u'</i>'
            fields['legal'] += u' in qualità di rappresentante legale / firmatario autorizzato,'
        else:
            valid = False

        validated = validated and valid

    if submit and validated:
        return pdf(fields)

    template = template % fields
    print 'Content-Type: text/html; charset=UTF-8\n'
    print template.encode('utf-8')

if __name__ == '__main__':
    cgitb.enable()
    page()

