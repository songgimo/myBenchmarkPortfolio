ERROR_CODE = {
    '0': '정상처리',
    '-200': '시세과부하',
    '-301': '계좌번호 없음',
    '-308': '주문전송 과부하',
}


class Consts:
    DELISTING = '0'
    EXCEPT_DELISTING = '1'
    DEFAULT_PASSWORD_TYPE = '00'


class OptCodes:
    STOCK_INFO = 'opt10001'
    ALL_PRICE = 'opt10004'
    CURRENT_PRICE = 'opt10007'
    BULK_FILLED_DATA = 'opt10055'
    INVEST_FUND_VOLUME = 'opt10059'
    DAILY_CANDLE = 'opt10005'
    DAILY_CHART = 'opt10081'


class OpwCodes:
    ACCOUNT_INFO = 'OPW00004'
    MARGIN_DATA = 'opw00011'


class Chejan:
    STOCK_CODE = '9001'
    STOCK_FILLED_PRICE_CODE = '910'
    STOCK_FILLED_QTY_CODE = '911'
    ORDER_NUMBER = '9203'


class CustomScreenNumbers:
    REAL_CURRENT_PRICE = ''
    REAL_ORDERBOOK = ''
    REAL_STOCK_FILLED = ''
    CONDITION = ''


class SetRealReg:
    ONLY_LAST_REGISTRY = '0'
    ADD_REGISTRY = '1'
    CURRENT_PRICE_CODE = '10'
    FILLED_DATE = '20'
    TRADE_AMOUNT = '15'


class IsRepeat:
    USED = 2
    UNUSED = 0


class Trading:
    NEW_BUY_ORDER = 1
    NEW_SELL_ORDER = 2
    CANCEL_BUY = 3
    CANCEL_SELL = 4
    CHANGE_BUY = 5
    CHANGE_SELL = 6

    LIMIT = '00'
    MARKET = '03'


class InvestFunds:
    QUANTITY = '2'
    BUYING = '1'
    NET_BUYING = '0'
    SINGLE_UNIT = '1'


class ResultStatus:
    SUCCESS = '0'


class StockCodes:
    ALL_KOSPI = '0'
    ALL_KOSDAQ = '10'


class NTypes:
    INTEREST_STOCK_INFO = '0'
    INTEREST_FUTURE_INFO = '3'


class ValueName:
    STOCK_CODE = '종목코드'
    TODAY_YESTERDAY = '당일전일'
    ACCOUNT_NUMBER = '계좌번호'
    PASSWORD = '비밀번호'
    PASSWORD_TYPE = '비밀번호입력매체구분'
    BASE_DATE = '기준일자'
    EXCEPT_DELISTING = '상장폐지조회구분'
    BID_PRICE = '매수가격'


class CustomItemName:
    STOCK_NAME = '종목명'
    HIGHEST_PRICE = '상한가'
    OPENING_PRICE = '시가'
    CURRENT_PRICE = '현재가'

    NAME_LIST = [STOCK_NAME, HIGHEST_PRICE, OPENING_PRICE, CURRENT_PRICE]