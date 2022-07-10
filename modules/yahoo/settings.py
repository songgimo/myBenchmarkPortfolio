class Region:
    US = 'US'
    AU = 'AU'
    CA = 'CA'
    FR = 'FR'
    DE = 'DE'
    HK = 'HK'
    IT = 'IT'
    ES = 'ES'
    GB = 'GB'
    IN = 'IN'


class Interval:
    MINUTE = '1m'
    FIVE_MINUTES = '5m'
    FIFTEEN_MINUTES = '15m'
    WEEK = '1wk'
    MONTH = '1mo'


class Range:
    DAY = '1d'
    FIVE_DAYS = '5d'
    MONTH = '1mo'
    THREE_MONTHS = '3mo'
    SIX_MONTHS = '6mo'
    YEAR = '1y'
    FIVE_YEARS = '5y'
    MAX = 'max'


class Language:
    EN = 'en'
    FR = 'fr'
    DE = 'de'
    IT = 'it'
    ES = 'es'
    ZH = 'zh'


class Urls:
    BASE = 'https://yfapi.net'

    QUOTE = '/v6/finance/quote'
    OPTIONS = '/v7/finance/options/{symbol}'
    SPARK = '/v8/finance/spark'
    QUOTE_SUMMARY = '/v11/finance/quoteSummary/{symbol}'
    CHART = '/v8/finance/chart/{ticker}'
    RECOMMENDATION = '/v6/finance/recommendationsbysymbol/{symbol}'
    AUTO_COMPLETE = '/v6/finance/autocomplete'
    MARKET_SUMMARY = '/v6/finance/quote/marketSummary'
    TRENDING = '/v1/finance/trending/{region}'

    class Websocket:
        ADD_WATCHLIST = '/ws/screeners/v1/finance/screener/predefined/saved'
        INSIGHT = '/ws/insights/v1/finance/insights'
