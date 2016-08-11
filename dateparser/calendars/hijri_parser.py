# coding: utf-8
from dateparser.parser import _parser
from convertdate import islamic
from datetime import datetime
from umalqurra.hijri_date import HijriDate
from umalqurra.ummalqura_arrray import UmalqurraArray


class hijri(object):

    @classmethod
    def to_gregorian(cls, year=None, month=None, day=None):
        h = HijriDate(year=year, month=month, day=day)
        return int(h.year_gr), int(h.month_gr), int(h.day_gr)


    @classmethod
    def from_gregorian(cls, year=None, month=None, day=None):
        h = HijriDate(year=year, month=month, day=day, gr=True)
        return int(h.year), int(h.month), int(h.day)

    @classmethod
    def month_length(cls, year, month):
        iy = year
        im = month
        id = 1
        ii = iy - 1
        iln = (ii * 12) + 1 + (im - 1)
        i = iln - 16260
        mcjdn = id + UmalqurraArray.ummalqura_dat[i - 1] - 1
        index = UmalqurraArray.get_index(mcjdn)
        ml = UmalqurraArray.ummalqura_dat[index] - UmalqurraArray.ummalqura_dat[index - 1]
        return ml


class hijri_date(object):
    def __init__(self, year, month, day):
        self.year=year
        self.month=month
        self.day=day

    def weekday(self):
        for week in hijri.monthcalendar(self.year, self.month):
            for idx, day in enumerate(week):
                if day==self.day:
                    return idx


class hijri_parser(_parser): 

    _time_conventions = {
        'am': [u"صباحاً"],
        'pm': [u"مساءً"],
    }

    @classmethod
    def replace_time_conventions(cls, source):
        result = source
        for latin, arabics in cls._time_conventions.items():
            for arabic in arabics:
                result = result.replace(arabic, latin)
        return result

    @classmethod
    def replace_digits(cls, source):
        # TODO
        return source

    @classmethod
    def replace_months(cls, source):
        # TODO
        return source

    @classmethod
    def replace_weekdays(cls, source):
        # TODO
        return source

    @classmethod
    def replace_time(cls, source):
        # TODO
        return source

    @classmethod
    def replace_days(cls, source):
        # TODO
        return source

    @classmethod
    def to_latin(cls, source):
        result = source
        result = cls.replace_months(result)
        result = cls.replace_weekdays(result)
        result = cls.replace_digits(result)
        result = cls.replace_days(result)
        result = cls.replace_time(result)
        result = cls.replace_time_conventions(result)

        result = result.strip()

        return result

    def _get_datetime_obj(self, **params):
        day = params['day']
        if not(0 < day <= hijri.month_length(params['year'], params['month'])) and not(self._token_day or hasattr(self, '_token_weekday')):
            day = hijri.month_length(params['year'], params['month'])
        year, month, day = hijri.to_gregorian(year=params['year'], month=params['month'], day=day)
        c_params = params.copy()
        c_params.update(dict(year=year,month=month, day=day))
        return datetime(**c_params)

    def _get_datetime_obj_params(self):
        if not self.now:
            self._set_relative_base()
        hijri_now_year, hijri_now_month, hijri_now_day = hijri.from_gregorian(self.now.year, self.now.month, self.now.day)
        params = {
            'day': self.day or hijri_now_day,
            'month': self.month or hijri_now_month,
            'year': self.year or hijri_now_year,
            'hour': 0, 'minute': 0, 'second': 0, 'microsecond': 0,
        }
        return params

    def _get_date_obj(self, token, directive):
        year, month, day = 1389, 1, 1
        if directive == '%A' and token.title() in self._weekdays:
            pass
        elif directive == '%m' and len(token) <= 2 and token.isdigit() and int(token) >= 1 and int(token) <= 12:
            month = int(token)
        #elif directive == '%B' and token in self._months:
        #    month = self._months.index(token) + 1
        elif directive == '%d' and len(token) <= 2 and token.isdigit() and 0 < int(token) <= hijri.month_length(year, month):
            day = int(token)
        elif directive == '%Y' and len(token) == 4 and token.isdigit():
            year = int(token)
        else:
            raise ValueError
        return hijri_date(year,month,day)

    @classmethod
    def parse(cls, datestring, settings):
        datestring = cls.to_latin(datestring)
        return super(hijri_parser, cls).parse(datestring, settings)
