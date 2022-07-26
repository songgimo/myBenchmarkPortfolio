from server.utils import execute_db, execute_db_many


class SetQueries(object):
    @staticmethod
    def stock_info():
        query = """
            CREATE TABLE IF NOT EXISTS stock_info (
                code VARCHAR(16) NOT NULL PRIMARY KEY,
                name VARCHAR(32)
                sector VARCHAR(32)
                type VARCHAR(32)
                date_created DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """.format()
        return execute_db(query)

    @staticmethod
    def dividend_history():
        query = """
            CREATE TABLE IF NOT EXISTS dividend_history (
                code VARCHAR(16) NOT NULL PRIMARY KEY,
                percent DECIMAL
                dividend_date TIMESTAMP 
                date_created DATETIME DEFAULT CURRENT_TIMESTAMP
                FOREIGN KEY (code) REFERENCES stock_info(code),
            )
        """

        return execute_db(query)

    @staticmethod
    def stock_history():
        query = """
            CREATE TABLE IF NOT EXISTS stock_history (
                code VARCHAR(16) NOT NULL PRIMARY KEY,
                candle_date bigint NOT NULL,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT,
                date_created DATETIME DEFAULT CURRENT_TIMESTAMP
                FOREIGN KEY (code) REFERENCES stock_info(code),
                CONSTRAINT const UNIQUE (code, candle_date)
            )
        """

        return execute_db(query)

    @staticmethod
    def portfolio_row():
        query = """
            CREATE TABLE IF NOT EXISTS stock_history (
            code VARCHAR(16) NOT NULL PRIMARY KEY,
            price DECIMAL
            amount VARCHAR(32)
            dividend VARCHAR(32)
            date_created DATETIME DEFAULT CURRENT_TIMESTAMP 
        """
        return query


class GetQueries(object):
    @staticmethod
    def all_candle_by_name(name):
        query = """
            SELECT candle_date, open, high, low, close
            FROM price_info
            JOIN stock_info ON stock_info.code = daily_info.code
            WHERE stock_info.name = %s
            ORDER BY candle_date ASC
        """

        return execute_db(query, value=name)

    @staticmethod
    def is_exists_price_info_by_code(code):
        query = """
            SELECT candle_date
            FROM price_info
            WHERE code = %s
            ORDER BY candle_date DESC 
            LIMIT 1
        """

        res = execute_db(query, value=code)
        return res


class PutQueries(object):
    @staticmethod
    def price_info(code, value_list):
        query = """
            INSERT IGNORE INTO price_info(code, candle_date, open, high, low, close)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return execute_db_many(query, value_list, code)

    @staticmethod
    def stock_info(codes):
        code_name_list = [list(items) for items in codes.items()]

        query = """
            INSERT IGNORE INTO stock_info(code, name)
            VALUES (%s, %s)
        """

        return execute_db_many(query, code_name_list)
