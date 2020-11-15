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