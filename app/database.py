import psycopg2
from uuid import uuid4


class Connection:
    def __init__(self):
        self.connector = self.init()

    def init(self):
        connect = psycopg2.connect("dbname=pi user=pi password=pi)
        cur = connect.cursor()
        with open("app/db/default.sql", "r", encoding="UTF-8") as sql:
            cur.execute(sql.read())
        return cur

    def close(self):
        self.connector.close()

    def execute(self, sql: str, *args):
        return self.connector.execute(sql, args)

    def commit(self):
        self.connector.commit()


class TicketSession(Connection):
    def __init__(self, session_id: str):
        Connection.__init__(self)

    def get_ticket(self, ticket_uuid: str) -> tuple[str, str, str, str, int] | None:
        ticket = list(self.execute("select * from tickets where uuid=?", ticket_uuid))
        if not ticket:
            return None
        return {
            "uuid": ticket[0][0],
            "nom": ticket[0][1],
            "prenom": ticket[0][2],
            "anniversaire": ticket[0][3],
            "used": ticket[0][4],
        }

    def create_ticket(self, nom: str, prenom: str, anniversaire: str) -> str:
        sql: str = (
            "insert into tickets (uuid, nom, prenom, anniversaire) values (?,?,?,?)"
        )
        uuid = uuid4()
        self.execute(sql, str(uuid), nom, prenom, anniversaire)
        self.commit()
        return str(uuid)

    def delete_ticket(self, ticket_uuid: str):
        self.execute("delete from tickets where uuid=?", ticket_uuid)
        self.commit()

    def use_ticket(self, ticket_uuid: str):
        self.execute("update tickets set used=1 where uuid=?", ticket_uuid)
        self.commit()
