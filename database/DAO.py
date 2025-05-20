from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():

    @staticmethod
    def getAllNations():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary = True)

        query = """select distinct Country
                    from go_retailers gr """
        cursor.execute(query,)

        for row in cursor:
            result.append(row["Country"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getRetailerNazione(country):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """select distinct *
                    from go_retailers gr 
                    where gr.Country = %s """
        cursor.execute(query, (country,), )

        for row in cursor:
            result.append(Retailer(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(country, anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """select distinct gds.Retailer_code as cod1, gds2.Retailer_code as cod2, count(distinct gds2.Product_number) as weight
                    from go_daily_sales gds ,go_daily_sales gds2, go_retailers gr, go_retailers gr2
                    where gds.Product_number = gds2.Product_number
                    and gds.Retailer_code < gds2.Retailer_code 
                    and gds.Retailer_code = gr.Retailer_code 
                    and gds2.Retailer_code = gr2.Retailer_code
                    and gr.Country = %s
                    and gr2.Country = %s
                    and year(gds2.`Date`) = %s
                    and year(gds.`Date`) = %s
                    group by gds.Retailer_code, gds2.Retailer_code"""
        cursor.execute(query, (country, country, anno, anno,))

        for row in cursor:
            result.append((row["cod1"], row["cod2"], row["weight"]))
        cursor.close()
        conn.close()
        return result
