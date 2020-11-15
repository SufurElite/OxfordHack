from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import uuid
from cassandra.util import datetime_from_uuid1

def uploadQAs(email, setname, qas):
    cloud_config= {
            'secure_connect_bundle': '/mnt/c/Users/Rufus Behr/Downloads/secure-connect-oxfordhack.zip'
    }
    auth_provider = PlainTextAuthProvider()
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect("Flashcards")
    foo = uuid.uuid1()
    dt_foo = datetime_from_uuid1(foo)
    for i in range(len(qas)):
        session.execute(
            """
            INSERT INTO cards (email, setname, question, answer)
            VALUES (%(email)s, %(setname)s, %(question)s, %(answer)s)
            """,
            {'email': email, 'setname': setname, 'question': qas[i][0], 'answer': qas[i][1]}
        )
def downloadQAs(email, setname):
    cloud_config= {
            'secure_connect_bundle': '/mnt/c/Users/Rufus Behr/Downloads/secure-connect-oxfordhack.zip'
    }
    print(email)
    print(setname)

    auth_provider = PlainTextAuthProvider()
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect("Flashcards")
    # Needs to be optimised for larger sets
    # Not scalable currenlty
    # need a better primary/partion key in the table in the future
    user_lookup_stmt = session.prepare("SELECT * FROM cards")
    rows = session.execute(user_lookup_stmt)
    cards = []
    color = ["red","gray"]
    i = 0
    for row in rows:
        if row.email == email and row.setname == setname:
            card = {
                'question': row.question,
                'answer' : row.answer,
                'color' : color[i%2],
                'flipped' : False
            }
            cards.append(card)
            i+=1
    return cards

def getStudySets(email):
    cloud_config= {
            'secure_connect_bundle': '/mnt/c/Users/Rufus Behr/Downloads/secure-connect-oxfordhack.zip'
    }
    auth_provider = PlainTextAuthProvider()
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect("Flashcards")
    # Needs to be optimised for larger sets
    # Not scalable currenlty
    # need a better primary/partion key in the table in the future
    user_lookup_stmt = session.prepare("SELECT * FROM cards")
    rows = session.execute(user_lookup_stmt)
    sets = []
    for row in rows:
        if row.email == email and row.setname not in sets:
            sets.append(row.setname)
    return sets
