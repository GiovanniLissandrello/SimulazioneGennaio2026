from database.DB_connect import DBConnect
from model.Constructor import Constructor
from model.arco import Arco


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodi(anno1, anno2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(c.constructorId), c.constructorRef , c.name , c.nationality 
                    from constructors c , results r , races r2 
                    where c.constructorId = r.constructorId 
                    and r.raceId = r2.raceId 
                    and year >= %s and year <=%s
                    and r.points is not null"""

        cursor.execute(query,(anno1, anno2,))

        for row in cursor:
            results.append(Constructor(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllArchi(anno1, anno2, dictC):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.constructorid as idC1, t1.name , t2.constructorid as idC2, t2.name, count(*) as peso
                    from (select r.constructorId, c.name , r.driverId  
                    from constructors c , results r , races r2 
                    where c.constructorId = r.constructorId 
                    and r.raceId = r2.raceId 
                    and r2.year >= %s and r2.year <= %s
                    and r.points is not null
                    group by r.constructorId, r.driverId) t1,
                    (select r.constructorId, c.name, r.driverId  
                    from constructors c , results r , races r2 
                    where c.constructorId = r.constructorId 
                    and r.raceId = r2.raceId 
                    and r2.year >= %s and r2.year <= %s
                    and r.points is not null
                    group by r.constructorId, r.driverId) t2
                    where t1.driverId = t2.driverid 
                    and t1.constructorid > t2.constructorid 
                    group by t1.constructorid, t2.constructorid"""

        cursor.execute(query, (anno1, anno2,anno1, anno2))

        for row in cursor:
            results.append(Arco(dictC.get(row["idC1"]) ,dictC.get(row["idC2"]), row["peso"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAnziano(anno1,anno2,idC):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select max(d.dob) as dobMax
                    from constructors c, drivers d , results r , races r2
                    where c.constructorId = r.constructorId 
                    and r.driverId = d.driverId 
                    and r.raceId = r2.raceId 
                    and r.points is not null
                    and r2.year >= %s and r2.year <= %s 
                    and c.constructorId = %s"""

        cursor.execute(query,(anno1,anno2,idC))

        for row in cursor:
            results.append(row["dobMax"])

        cursor.close()
        conn.close()
        return results