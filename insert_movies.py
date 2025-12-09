import sqlite3

movies_data = [
    # 100 Telugu Movies with Real Hero Names
    ("Baahubali The Beginning, Baahubali The Conclusion, Mirchi, Billa", "Prabhas,Anushka", "Rajamouli film,Two parts,War scenes",
     "Bahubali,Baahubali The Beginning,Baahubali 2: The Conclusion", 1, 25),

    ("Magadheera, Nayak, Yevadu, Govindudu Andarivaadele", "Ram Charan,Kajal", "Reincarnation,400 years,Charan debut blockbuster",
     "Magadhira,Magadira,Naayak,", 1, 25),

    ("Ala Vaikunthapuramulo, Duvvada Jagannadham", "Allu Arjun,Pooja Hegde", "Trivikram,Stylish star,Bunny dance",
     "Ala Vaikunthapuram,AVPL", 1, 25),

    ("Pushpa,Pushpa2,Pushpa3", "Allu Arjun,Rashmika", "Red sanders,Icon star,Sukumar",
     "Pushpa The Rise,Pushpa1", 1, 25),
    
    ("Dear Comrade, Geeta Govindham", "Vijay Deverakonda,Rashmika Mandanna", "Comrade,College love,Rashmika hit",
     "DearComrade", 2, 25),

    ("RRR", "NTR,Ram Charan,Alia", "Rajamouli,Bheem,Ramaraju",
     "R R R,RRR Movie", 1, 25),

    ("Kushi, Mahanati", "Vijay Deverakonda,Samantha", "Love story,Rowdy star,Arya music",
     "Khushi,Kushi 2023", 2, 25),

    # 4 — Jr NTR + Samantha
    ("Ramayya Vastavayya, Rabhasa, Janatha Garage",
     "Jr NTR, Samantha",
     "Action,Family drama,Court issues,Environment theme",
     "RV,JanathaGaraje,Rabasa,Rabhsa",
     1, 25),

    # 5 — Mahesh Babu + Samantha
    ("Dookudu, Seethamma Vakitlo Sirimalle Chettu, Brahmotsavam",
     "Mahesh Babu, Samantha",
     "Family entertainer,Comedy,Drama",
     "Dukudu,SVSC,Bramhotsavam,Bramhotsovam",
     1, 25),

    # 6 — Allu Arjun + Sruthi Haasan
    ("Race Gurram",
     "Allu Arjun, Shruti Haasan",
     "Action,Family entertainer",
     "RaceGurram,Race Guram",
     1, 25),

    # 7 — Nani + Nivetha Thomas
    ("Gentleman, V",
     "Nani, Nivetha Thomas",
     "Thriller,Double role,Suspense",
     "Gentalman,Gentelman,Gentlman,V Movie,Vmovie",
     1, 25),

    # 8 — Pawan Kalyan + Samantha
    ("Attarintiki Daredi",
     "Pawan Kalyan, Samantha",
     "Comedy,Family entertainer",
     "AD,Atarinthiki,Atarintiki",
     1, 25),

    # 9 — Chiranjeevi + Shriya Saran
    ("Tagore",
     "Chiranjeevi, Shriya Saran",
     "Corruption,Social drama,Action",
     "Tagor,Thagor",
     1, 25),

    # 10 — Balakrishna + Nayantara
    ("Simha, Sri Rama Rajyam, Jai Simha",
     "Nandamuri Balakrishna, Nayantara",
     "Mythological,Action,Drama",
     "Simhaa,Simhaaa,Jaisimha,Sriramarajyam",
     1, 25),

    ("Arjun Reddy", "Vijay Deverakonda,Shalini", "Kabir Singh original,Angry surgeon,VD",
     "ArjunRedy,Arjun", 2, 25),

    ("Maharshi", "Mahesh Babu,Pooja Hegde", "Village adoption,Superstar,CEO story",
     "Maharshee,Maharshi Movie", 1, 25),

    # ("Bharat Ane Nenu", "Mahesh Babu,Kiara", "CM story,Political drama,Koratala Siva",
    #  "BAN,Bharath Ane Nenu", 1, 25),

    ("Srimanthudu", "Mahesh Babu,Shruti Hassan", "Village adoption,Koratala,Blockbuster",
     "Sreemantudu,Srimanthudu Movie", 1, 25),

    ("Athadu, Sainikudu", "Mahesh Babu,Trisha", "Nandyala family,Mysterious shooter,Classic",
     "Atadu,Athadu Movie", 1, 25),

    ("Pokiri", "Mahesh Babu,Ileana", "Pandem Kodi,Undercover cop,Puri Jagannadh",
     "Pokkiri,Pokiri Movie", 1, 25),

    ("Temper, Brindavanam, Baadshah, Janatha Garage", "Jr NTR,Kajal Agarwal", "Daya police,NTR transformation,Puri",
     "Tempper,Temper Movie", 1, 25),

    ("Janatha Garage", "Jr NTR,Samantha,Nithya Menon", "Koratala movie,Environmental theme,Mohan Lal",
     "JanathaGaraj,Janata Garage", 1, 25),

    ("Aravinda Sametha Veera Raghava", "Jr NTR,Pooja Hegde", "Faction,Trivikram,NTR emotion",
     "AravindaSameta", 2, 25),

    ("Simhadri, Samba", "Jr NTR,Bhoomika", "Rajamouli,Narasimhudu,Powerful",
     "Simhadri Movie,Simadri", 1, 25),

    # ("Aadi", "Jr NTR,Keerthi Chawla", "Debut mass,NTR fight,Revenge story",
    #  "Adi,Aadi Movie", 2, 25),

    ("Chatrapathi", "Prabhas,Shriya Saran", "Port area,Refugees Story,Rajamouli",
     "Chathrapathi,Chatrapati", 1, 25),

    # ("Saaho", "Prabhas,Shraddha", "Action thriller,Robbery,Ghibran",
    #  "Sahoo,Saaho Movie", 1, 25),

    ("Darling, Mr. Perfect", "Prabhas,Kajal", "Love drama,Europe trip,Family emotions",
     "Daring,Darling Movie", 1, 25),

    ("Indra", "Chiranjeevi,Aarti Agarwal", "Rayalaseema faction,Chiru action,Mass",
     "Indhra,Indra Movie", 1, 25),

    ("Tagore", "Chiranjeevi,Shriya Saran", "Anti corruption,Shankar remake,Power",
     "Thagore,Tagore Movie", 1, 25),

    # ("Gharana Mogudu", "Chiranjeevi,Nagma", "Industrialist,Mega dance,Hit songs",
    #  "GharanaMogudu,Gharanamogudu", 3, 25),

    ("Sye Raa Narasimha Reddy, God Father", "Chiranjeevi,Nayanthara", "Uyyalawada Narasimha Reddy,Freedom fighter",
     "SyeRaa Narasimha Reddy,Syeraa", 2, 25),

    ("Gabbar Singh, Katamarayudu", "Pawan Kalyan,Shruti Hassan", "Harish Shankar,Blockbuster,Power star",
     "GabarSingh,Gabbarsingh", 1, 25),

    ("Attarintiki Daredi", "Pawan Kalyan,Samantha", "Family entertainer,Trivikram,Comedy hit",
     "AD,Attarintiki Daredhi", 1, 25),

    ("Jalsa", "Pawan Kalyan,Ileana", "Trivikram comedy,Youthful,Devi music",
     "Jalsha,Jalsa Movie", 1, 25),

    ("Kushi", "Pawan Kalyan,Bhoomika", "Iconic love,Madras college,Super hit",
     "Khushi,Kushi Movie", 1, 25),

    # ("Tholi Prema", "Pawan Kalyan,Keerthi Reddy", "National Award,Classic love story",
    #  "Toli Prema,Tholiprema", 2, 25),

    # ("Arya", "Allu Arjun,Anu Mehta", "Love triangle,Sukumar,Bunny debut",
    #  "Aarya,Aria", 1, 25),

    ("Arya 2, Yevadu", "Allu Arjun,Kajal Agarwal", "Jealousy,Friendship,Sukumar",
     "Arya2,Arya II", 1, 25),

    ("Sarrainodu", "Allu Arjun,Rakul Preeth singh", "Mass action,Boyapati,Bunny fights",
     "Sarainodu,Sarrainodu Movie", 1, 25),

    ("Race Gurram,Yevadu", "Allu Arjun,Shruti Hassan", "Comedy,Kill bill pandey,Blockbuster",
     "RaceGurram,Race Gurram Movie", 1, 25),

    ("Vedam,Rudramadevi", "Allu Arjun,Anushka", "Anthology movie,KCR speech,Bold film",
     "Vedham,Vedam Movie", 2, 25),

    # ("Taxiwala", "Vijay Deverakonda,Malavika", "Ghost car,Comedy thriller",
    #  "Taxi wala,Taxiwalaa", 2, 25),

    # ("Liger", "Vijay Deverakonda,Ananya", "Boxer,Mike Tyson,Pan India attempt",
    #  "Ligar,Liger Movie", 3, 25),

    # ("World Famous Lover", "Vijay Deverakonda,Rashi", "Multiple stories,Emotional love",
    #  "WFL,World Famous Lover Movie", 3, 25),

    ("Eega,Yeto vellipoindhi manassu,", "Nani,Samantha", "Fly revenge,Rajamouli,Unique movie",
     "Eeega,Eega Movie", 2, 25),

    # ("Jersey", "Nani,Shraddha", "Cricket drama,Emotional story",
    #  "Jersy,Jersey Movie", 1, 25),

    # ("Ninnu Kori", "Nani,Nivetha", "USA backdrop,Love story,Melody songs",
    #  "Ninu Kori,Ninnukori", 1, 25),

    ("Shyam Singha Roy,Middle Class Abbai", "Nani,Sai Pallavi", "Reincarnation,Bengal story",
     "Shyam Singa Roy,SSR", 2, 25),

    # ("Majili", "Naga Chaitanya,Samantha", "Cricket,Divorce drama,Lovely",
    #  "Majjili,Majili Movie", 2, 25),

    # ("Premam", "Naga Chaitanya,Shruti", "College romance,Malayalam remake",
    #  "Premem,Premam Movie", 2, 25),

    ("Soggade Chinni Nayana,Bangarraju,Annamayya,Garana Bullodu", "Nagarjuna,Ramya Krishna", "Fantasy village,Devotional",
     "Bangaraju,Bangarraju Movie", 2, 25),

    ("Manam,Bangarraju,Premam", "Nagarjuna,Naga Chaitanya", "Rebirth story,Family multistar",
     "Manaam,Manam Movie", 1, 25),

    ("Oopiri", "Nagarjuna,Karthi", "Wheelchair,Nag classy role",
     "Oopri,Thozha", 1, 25),

    # ("Shiva", "Nagarjuna,Amala", "Ram Gopal Varma,Colony fights",
    #  "Siva,Shiva Movie", 2, 25),
]

conn = sqlite3.connect("movies.db")
c = conn.cursor()

c.executemany("""
INSERT INTO movies (answer, characters, hints, alternatives, level, time)
VALUES (?, ?, ?, ?, ?, ?)
""", movies_data)

conn.commit()
conn.close()

print("100 Movies Inserted Successfully!")
