from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Categories, Base, Items, Users

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()

session = DBSession()

User1 = Users(name="John Doe", email="johndoe@gmail.com")

session.add(User1)
session.commit()

Category1 = Categories(name="Movies")

session.add(Category1)
session.commit()

Movie1 = Items(cat_id=1, name="Avengers: Endgame", user_id=1,
               description="""
               Avengers: Endgame is a 2019 American superhero film based on
               the Marvel Comics superhero team the Avengers, produced by
               Marvel Studios and distributed by Walt Disney Studios Motion
               Pictures. It is the sequel to 2012's The Avengers, 2015's, and
               2018's, and the twenty-second film in the Marvel Cinematic
               Universe.
               """, cat=Category1, user=User1)

session.add(Movie1)
session.commit()

Movie2 = Items(cat_id=1, name="Spider-Man: Homecoming", user_id=1,
               description="""
               Spider-Man: Homecoming is a 2017 American superhero film
               based on the Marvel Comics character Spider-Man, co-produced
               by Columbia Pictures and Marvel Studios, and distributed by
               Sony Pictures Releasing. It is the second Spider-Man film
               reboot and the sixteenth film in the Marvel Cinematic Universe.
               The film is directed by Jon Watts, from a screenplay by the
               writing teams of Jonathan Goldstein and John Francis Daley,
               Watts and Christopher Ford, and Chris McKenna and Erik Sommers.
               """, cat=Category1, user=User1)

session.add(Movie2)
session.commit()

Movie3 = Items(cat_id=1, name="Who Am I", user_id=1,
               description="""
               Benjamin, a young German computer whiz, is invited
               to join a subversive hacker group that wants to be
               noticed on the world's stage.
               """, cat=Category1, user=User1)

session.add(Movie3)
session.commit()

Movie4 = Items(cat_id=1, name="A Quiet Place", user_id=1,
               description="""
               A Quiet Place is a 2018 American post-apocalyptic horror
               film directed by John Krasinski, who wrote the screenplay
               with Bryan Woods and Scott Beck. The film stars Krasinski,
               alongside Emily Blunt, Millicent Simmonds, and Noah Jupe.
               """, cat=Category1, user=User1)

session.add(Movie4)
session.commit()

Category2 = Categories(name="TV programs")

session.add(Category2)
session.commit()

Program1 = Items(cat_id=2, name="Mr. Robot", user_id=1,
                 description="""
                 Mr. Robot is an American drama thriller television series
                 created by Sam Esmail for USA Network. It stars Rami Malek
                 as Elliot Alderson, a cybersecurity engineer and hacker with
                 social anxiety disorder and clinical depression. Elliot is
                 recruited by an insurrectionary anarchist known as "Mr. Robot"
                 , played by Christian Slater, to join a group of hacktivists
                 called "fsociety".The group aims to destroy all debt records
                 by encrypting the financial data of E Corp, the largest
                 conglomerate in the world.
                 """, cat=Category2, user=User1)

session.add(Program1)
session.commit()

Program2 = Items(cat_id=2, name="Mission: Impossible", user_id=1,
                 description="""
                 Mission: Impossible is an American television series,
                 created and initially produced by Bruce Geller, chronicling
                 the exploits of a team of secret government agents known as
                 the Impossible Missions Force (IMF). In the first season the
                 team is led by Dan Briggs, played by Steven Hill; Jim Phelps,
                 played by Peter Graves, takes charge for the remaining
                 seasons. Each episode opens with a fast-paced montage of shots
                 from that episode that unfolds as the series' theme music
                 composed by Lalo Schifrin plays, after which in a prologue
                 Briggs or Phelps receives his instructions from a voice
                 delivered on a recording which then self-destructs.
                 """, cat=Category2, user=User1)

session.add(Program2)
session.commit()

Program3 = Items(cat_id=2, name="Friends", user_id=1,
                 description="""
                 Friends is an American television sitcom, created by David
                 Crane and Marta Kauffman, which aired on NBC from September
                 22, 1994, to May 6, 2004, lasting ten seasons. With an
                 ensemble cast starring Jennifer Aniston, Courteney Cox, Lisa
                 Kudrow, Matt LeBlanc, Matthew Perry and David Schwimmer, the
                 show revolved around six friends in their 20s and 30s who
                 lived in Manhattan, New York City. The series was produced by
                 Bright/Kauffman/Crane Productions, in association with Warner
                 Bros. Television. The original executive producers were
                 Kevin S. Bright, Kauffman, and Crane.
                 """, cat=Category2, user=User1)

session.add(Program3)
session.commit()

Program4 = Items(cat_id=2, name="Supernatural", user_id=1,
                 description="""
                 Supernatural is an American dark fantasy television series
                 created by Eric Kripke. It was first broadcast on September
                 13, 2005, on The WB, and subsequently became part of successor
                 The CW's lineup. Starring Jared Padalecki as Sam Winchester
                 and Jensen Ackles as Dean Winchester, the series follows the
                 two brothers as they hunt demons, ghosts, monsters, and other
                 supernatural beings. The series is produced by Warner Bros.
                 Television, in association with Wonderland Sound and Vision.
                 Along with Kripke, executive producers have been McG, Robert
                 Singer, Phil Sgriccia, Sera Gamble, Jeremy Carver, John
                 Shiban, Ben Edlund and Adam Glass. Former executive producer
                 and director Kim Manners died of lung cancer during production
                 of the fourth season.
                 """, cat=Category2, user=User1)

session.add(Program4)
session.commit()

Category3 = Categories(name="Symphonies")

session.add(Category3)
session.commit()

Symphony1 = Items(cat_id=3, name="Symphony No. 6 (Beethoven)", user_id=1,
                  description="""
                  The Symphony No. 6 in F major, Op. 68, also known as the
                  Pastoral Symphony (German: Pastorale), is a symphony composed
                  by Ludwig van Beethoven and completed in 1808. One of
                  Beethoven's few works containing explicitly programmatic
                  content, the symphony was first performed in the Theater an
                  der Wien on 22 December 1808 in a four-hour concert.
                  """, cat=Category3, user=User1)

session.add(Symphony1)
session.commit()

Symphony2 = Items(cat_id=3, name="Symphony No. 1 (Bernstein)", user_id=1,
                  description="""
                  Leonard Bernstein's Symphony No. 1 Jeremiah was composed in
                  1942. Jeremiah is a programmatic work, following the Biblical
                  story of the prophet Jeremiah. The third movement uses texts
                  from the Book of Lamentations in the Hebrew Bible, sung by a
                  mezzo-soprano. The work won the New York Music Critics'
                  Circle Award for the best American work of 1944.
                  """, cat=Category3, user=User1)

session.add(Symphony2)
session.commit()

Symphony3 = Items(cat_id=3, name="Simple Symphony", user_id=1,
                  description="""
                  The Simple Symphony, Op. 4, is a work for string orchestra or
                  string quartet by Benjamin Britten. It was written between
                  December 1933 and February 1934 in Lowestoft, using bits of
                  score that the composer had written for the piano as a young
                  teenager, between 1923 and 1926. It was composed for string
                  orchestra and received its first performance in 1934 at
                  Stuart Hall in Norwich, with Britten conducting an amateur
                  orchestra. """, cat=Category3, user=User1)

session.add(Symphony3)
session.commit()


print("Filled the database with fake-real data :)")
