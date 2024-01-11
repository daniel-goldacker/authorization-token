import pytz

class DTConvert:
    def dateUtcToDateTimeZone(dateUTC, timeZone):
        localityTimeZone = pytz.timezone(timeZone)
        dateTimeZone = dateUTC.replace(tzinfo=pytz.utc).astimezone(localityTimeZone)

        return dateTimeZone
