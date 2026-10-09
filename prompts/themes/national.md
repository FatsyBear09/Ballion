# National football: themed prompt catalog

Theme: national teams (World Cups, Euros, Copa América, AFCON, Asian Cup, Gold Cup, Nations League, qualifiers, caps/goals, squads, captains, managers).
Every source title below was checked against the en.wikipedia API (`action=query&redirects=1`) on 2026-10-09; titles that resolve via a redirect are given as their canonical target.
Counts marked in notes as "scraped" were computed from the live page (squad templates, goalscorer sections, table rows); the rest are estimates.
2026 World Cup context (from en:2026 FIFA World Cup): Spain beat Argentina 1–0 a.e.t. in the final; France and England were the other semi-finalists.

Squad-page conventions used in notes: squad pages use `{{nat fs g player}}` rows with `no=`, `pos=`, `name=`, `age={{birth date and age2|...}}`, `caps=`, `club=`, `clubnat=` (club's national association) and `other=captain`; each team section has a `Coach:` line, with a flag icon when the coach's nationality differs from the team's.

## 2026 World Cup
| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| nat001 | Name a country that played at the 2026 World Cup | en:2026 FIFA World Cup squads (one `===Team===` section per nation) | 48 | modern | Spain, Argentina, Norway, Uzbekistan, Curaçao | answers are national-team articles; accept country-name redirects (e.g. "Ivory Coast", "DR Congo") |
| nat002 | Name a country that reached the knockout stage (round of 32) of the 2026 World Cup | en:2026 FIFA World Cup knockout stage (Round of 32 section) | 32 | modern | Spain, Brazil, United States, Australia, Egypt | the 32 teams appearing in round-of-32 match boxes |
| nat003 | Name a stadium that hosted a match at the 2026 World Cup | en:2026 FIFA World Cup#Venues | 16 | modern | MetLife Stadium, Estadio Azteca, SoFi Stadium, BC Place, Estadio Akron | accept the stadium's own article even though FIFA used neutral names ("New York New Jersey Stadium") |
| nat004 | Name a host city of the 2026 World Cup | en:2026 FIFA World Cup#Venues | 16 | modern | Los Angeles, Mexico City, Toronto, Monterrey, Kansas City | alias map: New York/New Jersey → New York City or East Rutherford; Dallas → Arlington; Boston → Foxborough; Miami → Miami Gardens; SF Bay Area → San Francisco or Santa Clara |
| nat005 | Name a player who scored 2 or more goals at the 2026 World Cup | en:2026 FIFA World Cup#Goalscorers | 57 | modern | Kylian Mbappé, Lionel Messi, Erling Haaland, Jude Bellingham, Ousmane Dembélé | scraped: 57 players with 2+ goals (own goals excluded) |
| nat006 | Name a player who scored in the knockout stage of the 2026 World Cup | en:2026 FIFA World Cup knockout stage (match-box goal lists) | 56 | modern | Kylian Mbappé, Lionel Messi, Cristiano Ronaldo, Jackson Irvine, Lucas Herrington | scraped ~56 linked scorers; exclude own goals and shoot-out penalties |
| nat007 | Name a player who appeared in the 2026 World Cup final | en:2026 FIFA World Cup final (line-ups) | 28 | modern | Lionel Messi, Lamine Yamal, Rodri, Unai Simón, Pau Cubarsí | Spain vs Argentina; starters plus substitutes who came on |
| nat008 | Name the head coach of a team at the 2026 World Cup | en:2026 FIFA World Cup squads (`Coach:` line per team) | 49 | modern | Carlo Ancelotti, Thomas Tuchel, Lionel Scaloni, Mauricio Pochettino, Bubista | scraped 48 lines; Saudi Arabia lists two (Sabri Lamouchi / Hervé Renard) |
| nat009 | Name a 2026 World Cup head coach who was coaching a country other than his own | en:2026 FIFA World Cup squads (`Coach:` lines carrying a flag icon) | 28 | modern | Carlo Ancelotti, Thomas Tuchel, Marcelo Bielsa, Dick Advocaat, Georgios Donis | scraped 27 flagged lines + Renard; page states flags mark coaches of a different nationality |
| nat010 | Name the captain of a team at the 2026 World Cup | en:2026 FIFA World Cup squads (`other=captain` field) | 48 | modern | Cristiano Ronaldo, Lionel Messi, Harry Kane, Mohamed Salah, Leandro Bacuna | scraped: exactly 48 |
| nat011 | Name a player who went to the 2026 World Cup with 100 or more caps | en:2026 FIFA World Cup squads (`caps` ≥ 100) | 59 | modern | Cristiano Ronaldo, Luka Modrić, Kevin De Bruyne, Salem Al-Dawsari, Aníbal Godoy | scraped 59; caps are as of tournament start |
| nat012 | Name a player born in 2005 or later who was in a 2026 World Cup squad | en:2026 FIFA World Cup squads (birth year in `age` field) | 67 | modern | Lamine Yamal, Pau Cubarsí, Endrick, Arda Güler, Bekhruz Karimov | scraped 67 |
| nat013 | Name a player born in 1990 or earlier who was in a 2026 World Cup squad | en:2026 FIFA World Cup squads (birth year in `age` field) | 54 | modern | Cristiano Ronaldo, Lionel Messi, Manuel Neuer, Guillermo Ochoa, Vozinha | scraped 54 |
| nat014 | Name a player who wore the No. 10 shirt at the 2026 World Cup | en:2026 FIFA World Cup squads (`no=10`) | 48 | modern | Lionel Messi, Kylian Mbappé, Neymar, Jamal Musiala, Mohanad Ali | scraped: one per team |
| nat015 | Name a player who wore the No. 7 shirt at the 2026 World Cup | en:2026 FIFA World Cup squads (`no=7`) | 48 | modern | Cristiano Ronaldo, Bukayo Saka, Vinícius Júnior, Son Heung-min, Otabek Shukurov | scraped: one per team |

## Squads
| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| nat016 | Name a player in Spain's 2026 World Cup-winning squad | en:2026 FIFA World Cup squads#Spain | 26 | modern | Lamine Yamal, Rodri, Pedri, Martín Zubimendi, Víctor Muñoz | squad template family |
| nat017 | Name a player in Argentina's 2026 World Cup squad | en:2026 FIFA World Cup squads#Argentina | 26 | modern | Lionel Messi, Julián Alvarez, Emiliano Martínez, Nico Paz, José Manuel López | runners-up |
| nat018 | Name a player in England's 2026 World Cup squad | en:2026 FIFA World Cup squads#England | 26 | modern | Harry Kane, Jude Bellingham, Declan Rice, Elliot Anderson, Djed Spence | semi-finalists |
| nat019 | Name a player in the United States' 2026 World Cup squad | en:2026 FIFA World Cup squads#United States | 26 | modern | Christian Pulisic, Weston McKennie, Tyler Adams, Max Arfsten, Alex Freeman | co-hosts |
| nat020 | Name a player in Morocco's 2022 World Cup squad | en:2022 FIFA World Cup squads#Morocco | 26 | modern | Achraf Hakimi, Hakim Ziyech, Yassine Bounou, Sofyan Amrabat, Yahia Attiyat Allah | first African semi-finalist |
| nat021 | Name a player in Croatia's 2018 World Cup squad | en:2018 FIFA World Cup squads#Croatia | 23 | modern | Luka Modrić, Ivan Rakitić, Mario Mandžukić, Ivan Perišić, Duje Ćaleta-Car | runners-up |
| nat022 | Name a player in Japan's 2022 World Cup squad | en:2022 FIFA World Cup squads#Japan | 26 | modern | Kaoru Mitoma, Takefusa Kubo, Ritsu Dōan, Daizen Maeda, Shūichi Gonda | beat Germany and Spain |
| nat023 | Name a player in Italy's Euro 2020-winning squad | en:UEFA Euro 2020 squads#Italy | 26 | modern | Gianluigi Donnarumma, Giorgio Chiellini, Federico Chiesa, Jorginho, Gaetano Castrovilli | |
| nat024 | Name a player in England's Euro 2024 squad | en:UEFA Euro 2024 squads#England | 26 | modern | Harry Kane, Bukayo Saka, Cole Palmer, Ollie Watkins, Adam Wharton | runners-up |
| nat025 | Name a player in Portugal's Euro 2016-winning squad | en:UEFA Euro 2016 squads#Portugal | 23 | modern | Cristiano Ronaldo, Pepe, Renato Sanches, Éder, Eliseu | |
| nat026 | Name a player in Argentina's 2021 Copa América-winning squad | en:2021 Copa América squads#Argentina | 28 | modern | Lionel Messi, Ángel Di María, Rodrigo De Paul, Emiliano Martínez, Agustín Marchesín | |
| nat027 | Name a player in Colombia's 2024 Copa América squad | en:2024 Copa América squads#Colombia | 26 | modern | Luis Díaz, James Rodríguez, Jhon Durán, Richard Ríos, Deiver Machado | runners-up |
| nat028 | Name a player in Senegal's 2021 Africa Cup of Nations-winning squad | en:2021 Africa Cup of Nations squads#Senegal | 28 | modern | Sadio Mané, Kalidou Koulibaly, Édouard Mendy, Bamba Dieng, Alfred Gomis | names use `{{sortname}}`; resolve to article links |
| nat029 | Name a player in Ivory Coast's 2023 Africa Cup of Nations-winning squad | en:2023 Africa Cup of Nations squads#Ivory Coast | 27 | modern | Sébastien Haller, Franck Kessié, Simon Adingra, Max Gradel, Jean-Philippe Krasso | scraped 27 |
| nat030 | Name a player in Morocco's 2025 Africa Cup of Nations squad | en:2025 Africa Cup of Nations squads#Morocco | 28 | modern | Achraf Hakimi, Brahim Díaz, Yassine Bounou, Neil El Aynaoui, Chemsdine Talbi | hosts; title outcome is footnoted as "awarded" on Wikipedia, so prompt avoids "winning" |
| nat031 | Name a player in Qatar's 2023 AFC Asian Cup-winning squad | en:2023 AFC Asian Cup squads#Qatar | 26 | modern | Akram Afif, Almoez Ali, Hassan Al-Haydos, Meshaal Barsham, Lucas Mendes | |

## Finals and multi-tournament squads
| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| nat032 | Name a player who appeared in the 2022 World Cup final | en:2022 FIFA World Cup final (line-ups) | 30 | modern | Lionel Messi, Kylian Mbappé, Ángel Di María, Randal Kolo Muani, Gonzalo Montiel | starters + used substitutes |
| nat033 | Name a player who appeared in the 2018 World Cup final | en:2018 FIFA World Cup final (line-ups) | 28 | modern | Antoine Griezmann, Paul Pogba, Luka Modrić, Corentin Tolisso, Marko Pjaca | starters + used substitutes |
| nat034 | Name a player who appeared in the Euro 2024 final | en:UEFA Euro 2024 final (line-ups) | 28 | modern | Lamine Yamal, Harry Kane, Bukayo Saka, Mikel Oyarzabal, Martín Zubimendi | starters + used substitutes |
| nat035 | Name a player who appeared in the Euro 2020 final | en:UEFA Euro 2020 final (line-ups) | 28 | modern | Raheem Sterling, Federico Chiesa, Gianluigi Donnarumma, Luke Shaw, Federico Bernardeschi | starters + used substitutes |
| nat036 | Name a player who appeared in the 2024 Copa América final | en:2024 Copa América final (line-ups) | 28 | modern | Lionel Messi, Lautaro Martínez, Luis Díaz, James Rodríguez, Jhon Córdoba | starters + used substitutes |
| nat037 | Name a player who was in Wales's squad at Euro 2016, Euro 2020 or the 2022 World Cup | en:UEFA Euro 2016 squads, en:UEFA Euro 2020 squads, en:2022 FIFA World Cup squads (#Wales) | 52 | modern | Gareth Bale, Aaron Ramsey, Ben Davies, Hal Robson-Kanu, Joe Morrell | scraped union 52 |
| nat038 | Name a player who was in Scotland's squad at Euro 2020, Euro 2024 or the 2026 World Cup | en:UEFA Euro 2020 squads, en:UEFA Euro 2024 squads, en:2026 FIFA World Cup squads (#Scotland) | 46 | modern | Andy Robertson, Scott McTominay, John McGinn, Che Adams, Findlay Curtis | scraped union 46 |
| nat039 | Name a player who was in Iceland's squad at Euro 2016 or the 2018 World Cup | en:UEFA Euro 2016 squads, en:2018 FIFA World Cup squads (#Iceland) | 32 | modern | Gylfi Sigurðsson, Aron Gunnarsson, Hannes Halldórsson, Alfreð Finnbogason, Rúnar Alex Rúnarsson | scraped union 32 |
| nat040 | Name a player who was in Northern Ireland's or the Republic of Ireland's squad at Euro 2016 | en:UEFA Euro 2016 squads (#Northern Ireland, #Republic of Ireland) | 46 | modern | Robbie Keane, Shane Long, Robbie Brady, Kyle Lafferty, Will Grigg | scraped 46 |
| nat041 | Name a player who was in Canada's squad at the 2022 or 2026 World Cup | en:2022 FIFA World Cup squads, en:2026 FIFA World Cup squads (#Canada) | 40 | modern | Alphonso Davies, Jonathan David, Cyle Larin, Stephen Eustáquio, Luc de Fougerolles | scraped union 40 |
| nat042 | Name a player who was in Brazil's squad at the 2018, 2022 or 2026 World Cup | en:2018 / 2022 / 2026 FIFA World Cup squads (#Brazil) | 52 | modern | Neymar, Vinícius Júnior, Casemiro, Richarlison, Weverton | scraped union 52 |
| nat043 | Name a player who was in France's squad at any World Cup or Euro from 2018 to 2026 | en:2018 / 2022 / 2026 FIFA World Cup squads, en:UEFA Euro 2020 / 2024 squads (#France) | 60 | modern | Kylian Mbappé, Antoine Griezmann, N'Golo Kanté, Steve Mandanda, Jean-Philippe Mateta | scraped union 60 |
| nat044 | Name a player who was in Germany's squad at any World Cup or Euro from 2018 to 2026 | en:2018 / 2022 / 2026 FIFA World Cup squads, en:UEFA Euro 2020 / 2024 squads (#Germany) | 66 | modern | Thomas Müller, Toni Kroos, Jamal Musiala, Marvin Plattenhardt, Assan Ouédraogo | scraped union 66 |
| nat045 | Name a player who was in the Netherlands' squad at any World Cup or Euro from 2016 to 2026 | en:2022 / 2026 FIFA World Cup squads, en:UEFA Euro 2020 / 2024 squads (#Netherlands) | 54 | modern | Virgil van Dijk, Memphis Depay, Cody Gakpo, Wout Weghorst, Bart Verbruggen | scraped union 54 (no 2016/2018 qualification) |
| nat046 | Name a player who appeared in the 2025 UEFA Nations League final | en:2025 UEFA Nations League final (line-ups) | 30 | modern | Cristiano Ronaldo, Lamine Yamal, Nuno Mendes, Mikel Oyarzabal, Rúben Neves | Portugal vs Spain; starters + used substitutes |
| nat047 | Name a player who appeared in the 2021 Copa América final | en:2021 Copa América final (line-ups) | 28 | modern | Lionel Messi, Neymar, Ángel Di María, Richarlison, Guido Rodríguez | Argentina vs Brazil at the Maracanã |

## Tournament goalscorers
| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| nat048 | Name a player who scored at the 2022 World Cup | en:2022 FIFA World Cup#Goalscorers | 117 | modern | Kylian Mbappé, Lionel Messi, Olivier Giroud, Christian Pulisic, Haji Wright | scraped 117; exclude own goals |
| nat049 | Name a player who scored at the 2018 World Cup | en:2018 FIFA World Cup#Goalscorers | 110 | modern | Harry Kane, Romelu Lukaku, Kylian Mbappé, José Giménez, Fakhreddine Ben Youssef | scraped 110; exclude own goals |
| nat050 | Name a player who scored in the knockout stage of the 2022 World Cup | en:2022 FIFA World Cup knockout stage (match-box goal lists) | 45 | modern | Lionel Messi, Kylian Mbappé, Gonçalo Ramos, Youssef En-Nesyri, Daizen Maeda | scraped ~45; exclude own goals and shoot-out penalties |
| nat051 | Name a player who scored at Euro 2024 | en:UEFA Euro 2024#Goalscorers | 85 | modern | Harry Kane, Jamal Musiala, Cody Gakpo, Georges Mikautadze, Ivan Schranz | scraped 85 |
| nat052 | Name a player who scored in the knockout stage of Euro 2024 | en:UEFA Euro 2024 knockout stage (match-box goal lists) | 28 | modern | Lamine Yamal, Dani Olmo, Jude Bellingham, Michael Gregoritsch, Remo Freuler | scraped ~27 (+ Ollie Watkins, whose link the quick scrape missed); exclude own goals and shoot-out penalties |
| nat053 | Name a player who scored at Euro 2020 | en:UEFA Euro 2020 statistics#Goalscorers | 80 | modern | Cristiano Ronaldo, Patrik Schick, Romelu Lukaku, Emil Forsberg, Kieffer Moore | scraped 80 |
| nat054 | Name a player who scored at Euro 2016 | en:UEFA Euro 2016 statistics#Goalscorers | 76 | modern | Antoine Griezmann, Gareth Bale, Dimitri Payet, Hal Robson-Kanu, Birkir Bjarnason | scraped 76 |
| nat055 | Name a player who scored at the 2024 Copa América | en:2024 Copa América#Goalscorers | 51 | modern | Lautaro Martínez, Vinícius Júnior, Salomón Rondón, Jonathan David, Eric Ramírez | scraped 51 |
| nat056 | Name a player who scored at the 2021 Copa América | en:2021 Copa América#Goalscorers | 41 | modern | Lionel Messi, Luis Díaz, Lautaro Martínez, Gianluca Lapadula, Edson Castillo | scraped 41 |
| nat057 | Name a player who scored at the 2025 Africa Cup of Nations | en:2025 Africa Cup of Nations#Goalscorers | 80 | modern | Mohamed Salah, Victor Osimhen, Brahim Díaz, Riyad Mahrez, Tawanda Maswanhise | scraped 80 |
| nat058 | Name a player who scored at the 2023 Africa Cup of Nations | en:2023 Africa Cup of Nations#Goalscorers | 81 | modern | Emilio Nsue, Mostafa Mohamed, Baghdad Bounedjah, Gelson Dala, Kings Kangwa | scraped 81 |
| nat059 | Name a player who scored at the 2021 Africa Cup of Nations | en:2021 Africa Cup of Nations#Goalscorers | 70 | modern | Vincent Aboubakar, Karl Toko Ekambi, Sofiane Boufal, Gabadinho Mhango, Ishmael Wadi | scraped 70 |
| nat060 | Name a player who scored at the 2019 Africa Cup of Nations | en:2019 Africa Cup of Nations#Goalscorers | 70 | modern | Sadio Mané, Riyad Mahrez, Odion Ighalo, Adam Ounas, Patrick Kaddu | scraped 70 |
| nat061 | Name a player who scored at the 2023 AFC Asian Cup | en:2023 AFC Asian Cup#Goalscorers | 80 | modern | Akram Afif, Mehdi Taremi, Ayase Ueda, Aymen Hussein, Nguyễn Quang Hải | scraped 80 |
| nat062 | Name a player who scored at the 2025 CONCACAF Gold Cup | en:2025 CONCACAF Gold Cup#Goalscorers | 55 | modern | Raúl Jiménez, Ismael Díaz, Tajon Buchanan, Haji Wright, Dante Sealy | scraped 55 |
| nat063 | Name a player who scored 5 or more goals in UEFA qualifying for the 2026 World Cup | en:2026 FIFA World Cup qualification (UEFA)#Top goalscorers | 22 | modern | Erling Haaland, Harry Kane, Memphis Depay, Marko Arnautović, Harry Wilson | scraped 22 (section lists 5+ goals) |

## Countries and qualification
| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| nat064 | Name a country that played at the 2022 World Cup | en:2022 FIFA World Cup squads (team sections) | 32 | modern | Argentina, Morocco, Croatia, Qatar, Wales | |
| nat065 | Name a country that played at Euro 2024 | en:UEFA Euro 2024 squads (team sections) | 24 | modern | Spain, England, Georgia, Slovenia, Albania | |
| nat066 | Name a country that played at the 2024 Copa América | en:2024 Copa América squads (team sections) | 16 | modern | Argentina, Colombia, Canada, Jamaica, Panama | 10 CONMEBOL + 6 CONCACAF |
| nat067 | Name a country that played at the 2025 Africa Cup of Nations | en:2025 Africa Cup of Nations squads (team sections) | 24 | modern | Morocco, Senegal, Nigeria, Botswana, Comoros | |
| nat068 | Name a country that played at the 2023 AFC Asian Cup | en:2023 AFC Asian Cup squads (team sections) | 24 | modern | Qatar, Japan, Jordan, Tajikistan, Hong Kong | |
| nat069 | Name a country that played at the 2025 CONCACAF Gold Cup | en:2025 CONCACAF Gold Cup squads (team sections) | 16 | modern | Mexico, United States, Canada, Trinidad and Tobago, Saudi Arabia | Saudi Arabia was an invited guest |
| nat070 | Name a country that played in League A of the 2024–25 UEFA Nations League | en:2024–25 UEFA Nations League A | 16 | modern | Portugal, Spain, France, Scotland, Bosnia and Herzegovina | |
| nat071 | Name a country that has won the Africa Cup of Nations | en:Africa Cup of Nations#Results | 16 | 2000s+ | Egypt, Senegal, Ivory Coast, Zambia, Sudan | include Morocco only if the results table lists the awarded 2025 title |
| nat072 | Name a country that has taken part in a World Cup penalty shoot-out | en:List of FIFA World Cup penalty shoot-outs (team summary table) | 33 | 2000s+ | Argentina, England, Croatia, Japan, Romania | table rows: 33 teams |
| nat073 | Name a country currently in the top 20 of the FIFA Men's World Ranking | en:FIFA Men's World Ranking (current top-20 table) | 20 | modern | Spain, Argentina, Morocco, Japan, Austria | live list: snapshot at scrape time |
| nat074 | Name a member nation of CONCACAF | en:List of men's national association football teams (CONCACAF section) | 41 | modern | Mexico, United States, Curaçao, Suriname, Montserrat | geography deep cuts; all have national-team articles |
| nat075 | Name a member nation of the Asian Football Confederation | en:List of men's national association football teams (AFC section) | 47 | modern | Japan, Saudi Arabia, Uzbekistan, Bhutan, Northern Mariana Islands | Australia counts (AFC since 2006) |
| nat076 | Name a country that won a men's football medal at the Olympics from 2000 to 2024 | en:Football at the Summer Olympics (men's results table) | 13 | 2000s+ | Brazil, Spain, Argentina, Morocco, Chile | gold, silver or bronze 2000–2024; answer is the senior national-team article (Olympic sides are U-23) |
| nat077 | Name a country that played in the UEFA play-offs for the 2026 World Cup | en:2026 FIFA World Cup qualification (UEFA)#Second round (play-off path brackets) | 16 | modern | Italy, Turkey, Sweden, Bosnia and Herzegovina, Kosovo | 12 group runners-up + 4 Nations League teams; section also links seeding tables, scrape only the path brackets |
| nat078 | Name a country that has played at exactly one men's World Cup | en:National team appearances in the FIFA World Cup (appearances table, value 1) | 17 | 2000s+ | Iceland, Ukraine, Cape Verde, Trinidad and Tobago, East Germany | scraped 17 incl. 2026 debutants Cape Verde, Curaçao, Jordan, Uzbekistan |

## Managers and captains
| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| nat079 | Name the head coach of a team at the 2022 World Cup | en:2022 FIFA World Cup squads (`Coach:` lines) | 32 | modern | Lionel Scaloni, Didier Deschamps, Gareth Southgate, Walid Regragui, Gregg Berhalter | scraped 32 |
| nat080 | Name the head coach of a team at the 2018 World Cup | en:2018 FIFA World Cup squads (`Coach:` lines) | 32 | modern | Didier Deschamps, Zlatko Dalić, Gareth Southgate, Héctor Cúper, Stanislav Cherchesov | scraped 32 |
| nat081 | Name the head coach of a team at Euro 2024 | en:UEFA Euro 2024 squads (`Coach:` lines) | 24 | modern | Luis de la Fuente, Julian Nagelsmann, Gareth Southgate, Willy Sagnol, Ralf Rangnick | scraped 24 |
| nat082 | Name the head coach of a team at Euro 2020 | en:UEFA Euro 2020 squads (`Coach:` lines) | 24 | modern | Roberto Mancini, Gareth Southgate, Joachim Löw, Kasper Hjulmand, Andriy Shevchenko | scraped 24 |
| nat083 | Name the head coach of a team at the 2023 Africa Cup of Nations | en:2023 Africa Cup of Nations squads (`Coach:` lines) | 24 | modern | Aliou Cissé, Walid Regragui, Emerse Faé, José Peseiro, Tom Saintfiet | scraped 24; Ivory Coast changed coach mid-tournament, accept both if listed |
| nat084 | Name the head coach of a team at the 2025 Africa Cup of Nations | en:2025 Africa Cup of Nations squads (`Coach:` lines) | 24 | modern | Walid Regragui, Hossam Hassan, Vladimir Petković, Pape Thiaw, Hugo Broos | scraped 24 |
| nat085 | Name the head coach of a team at the 2023 AFC Asian Cup | en:2023 AFC Asian Cup squads (`Coach:` lines) | 24 | modern | Jürgen Klinsmann, Roberto Mancini, Hajime Moriyasu, Hussein Ammouta, Igor Štimac | scraped 24; 21 of 24 were foreign |
| nat086 | Name the head coach of a team at the 2024 Copa América | en:2024 Copa América squads (`Coach:` lines) | 16 | modern | Lionel Scaloni, Marcelo Bielsa, Jesse Marsch, Dorival Júnior, Fernando Batista | scraped 16 |
| nat087 | Name a manager of Brazil or Argentina since 1990 (caretakers included) | en:List of Brazil national football team managers, en:List of Argentina national football team managers | 32 | 2000s+ | Tite, Lionel Scaloni, Diego Maradona, Carlo Ancelotti, Mano Menezes | appointments starting 1990 or later |
| nat088 | Name a manager of the Italy national team since 1990 | en:List of Italy national football team managers | 14 | 2000s+ | Marcello Lippi, Roberto Mancini, Antonio Conte, Gian Piero Ventura, Luigi Di Biagio | appointments starting 1990 or later, caretakers included |
| nat089 | Name a manager of the Mexico national team since 2000 (caretakers included) | en:List of Mexico national football team managers | 22 | 2000s+ | Javier Aguirre, Juan Carlos Osorio, Gerardo Martino, Miguel Herrera, Jaime Lozano | |
| nat090 | Name a manager of the South Korea national team since 2000 (caretakers included) | en:List of South Korea national football team managers | 18 | 2000s+ | Guus Hiddink, Jürgen Klinsmann, Hong Myung-bo, Paulo Bento, Uli Stielike | |
| nat091 | Name a head coach of Saudi Arabia since 2000 (caretakers included) | en:Saudi Arabia national football team#Coaching history | 28 | 2000s+ | Hervé Renard, Roberto Mancini, Juan Antonio Pizzi, Frank Rijkaard, Bert van Marwijk | Saudi Arabia changes coach often; good deep cuts |
| nat092 | Name a head coach of Nigeria since 2000 (caretakers included) | en:Nigeria national football team#Coaching history | 20 | 2000s+ | Gernot Rohr, Stephen Keshi, Lars Lagerbäck, Berti Vogts, José Peseiro | |
| nat093 | Name the captain of a team at the 2022 World Cup | en:2022 FIFA World Cup squads (`other=captain`) | 33 | modern | Lionel Messi, Hugo Lloris, Cristiano Ronaldo, Romain Saïss, Hassan Al-Haydos | scraped 33 (one team marks two) |
| nat094 | Name the captain of a team at Euro 2024 | en:UEFA Euro 2024 squads (`other=captain`) | 24 | modern | Harry Kane, Álvaro Morata, Kylian Mbappé, Virgil van Dijk, Guram Kashia | scraped 24 |
| nat095 | Name a player who has captained England since 2000 | en:List of England national football team captains (full captains table, first captaincy 2000+) | 45 | 2000s+ | Harry Kane, David Beckham, Steven Gerrard, Wayne Rooney, Jamie Carragher | includes one-off captains; ~45–51 rows |
| nat096 | Name the head coach of a team at the 2025 CONCACAF Gold Cup | en:2025 CONCACAF Gold Cup squads (coach lines) | 16 | modern | Javier Aguirre, Mauricio Pochettino, Jesse Marsch, Thomas Christiansen, Steve McClaren | scraped 16; 13 foreign |
| nat097 | Name the head coach of a team at the 2023 Women's World Cup | en:2023 FIFA Women's World Cup squads (`Head coach:` lines) | 33 | modern | Sarina Wiegman, Jorge Vilda, Hervé Renard, Vlatko Andonovski, Bruce Mwape | scraped 33 lines (one team changed coach) |
| nat098 | Name the captain of a team at Euro 2020 | en:UEFA Euro 2020 squads (`other=captain`) | 24 | modern | Cristiano Ronaldo, Harry Kane, Giorgio Chiellini, Gareth Bale, Goran Pandev | scraped 24 |
| nat099 | Name the captain of a team at the 2024 Copa América | en:2024 Copa América squads (`other=captain`) | 17 | modern | Lionel Messi, James Rodríguez, Alphonso Davies, Christian Pulisic, Luis Haquín | scraped 17 (one team lists two) |
| nat100 | Name the captain of a team at the 2025 Africa Cup of Nations | en:2025 Africa Cup of Nations squads (`other=captain`) | 24 | modern | Mohamed Salah, Achraf Hakimi, Riyad Mahrez, Wilfred Ndidi, Youssouf M'Changama | scraped 24 |
| nat101 | Name the captain of a team at the 2023 AFC Asian Cup | en:2023 AFC Asian Cup squads (`other=captain`) | 24 | modern | Son Heung-min, Sunil Chhetri, Wataru Endō, Salem Al-Dawsari, Hassan Maatouk | scraped 24 |

## Club and league representation at tournaments
| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| nat102 | Name a Manchester City player who went to the 2026 World Cup | en:2026 FIFA World Cup squads (`club` = Manchester City F.C.) | 19 | modern | Erling Haaland, Rodri, Rúben Dias, Omar Marmoush, Abdukodir Khusanov | scraped 19 |
| nat103 | Name a Bayern Munich player who went to the 2026 World Cup | en:2026 FIFA World Cup squads (`club` = FC Bayern Munich) | 17 | modern | Harry Kane, Jamal Musiala, Michael Olise, Hiroki Itō, Bara Sapoko Ndiaye | scraped 17 |
| nat104 | Name a Paris Saint-Germain player who went to the 2026 World Cup | en:2026 FIFA World Cup squads (`club` = Paris Saint-Germain FC) | 16 | modern | Ousmane Dembélé, Achraf Hakimi, Vitinha, Lee Kang-in, Khalil Ayari | scraped 16 |
| nat105 | Name an Arsenal player who went to the 2026 World Cup | en:2026 FIFA World Cup squads (`club` = Arsenal F.C.) | 15 | modern | Bukayo Saka, Declan Rice, Martin Ødegaard, Viktor Gyökeres, Piero Hincapié | scraped 15 |
| nat106 | Name a Barcelona player who went to the 2026 World Cup | en:2026 FIFA World Cup squads (`club` = FC Barcelona) | 14 | modern | Lamine Yamal, Pedri, Raphinha, Marcus Rashford, Joan Garcia | scraped 14 |
| nat107 | Name a Crystal Palace player who went to the 2026 World Cup | en:2026 FIFA World Cup squads (`club` = Crystal Palace F.C.) | 12 | modern | Jean-Philippe Mateta, Ismaïla Sarr, Daichi Kamada, Chadi Riad, Evann Guessand | scraped 12 |
| nat108 | Name a Real Madrid player who went to the 2022 World Cup | en:2022 FIFA World Cup squads (`club` = Real Madrid CF) | 13 | modern | Vinícius Júnior, Luka Modrić, Thibaut Courtois, Federico Valverde, Marco Asensio | scraped 13 |
| nat109 | Name a Manchester United player who went to the 2022 World Cup | en:2022 FIFA World Cup squads (`club` = Manchester United F.C.) | 14 | modern | Cristiano Ronaldo, Bruno Fernandes, Casemiro, Lisandro Martínez, Tyrell Malacia | scraped 14 |
| nat110 | Name an Al Sadd player who went to the 2022 World Cup | en:2022 FIFA World Cup squads (`club` = Al Sadd SC) | 15 | modern | Akram Afif, Hassan Al-Haydos, André Ayew, Boualem Khoukhi, Meshaal Barsham | scraped 15; mostly hosts Qatar |
| nat111 | Name an Inter Milan player who went to Euro 2024 | en:UEFA Euro 2024 squads (`club` = Inter Milan) | 13 | modern | Nicolò Barella, Hakan Çalhanoğlu, Marcus Thuram, Denzel Dumfries, Yann Sommer | scraped 13 |
| nat112 | Name a player at the 2026 World Cup who played for a Saudi Arabian club | en:2026 FIFA World Cup squads (`clubnat=KSA`) | 50 | modern | Cristiano Ronaldo, Sadio Mané, Riyad Mahrez, Darwin Núñez, Firas Al-Buraikan | scraped 50 |
| nat113 | Name a player at the 2026 World Cup who played for a Major League Soccer club | en:2026 FIFA World Cup squads (`clubnat` USA/CAN, MLS clubs only) | 45 | modern | Lionel Messi, Son Heung-min, Rodrigo De Paul, James Rodríguez, Kai Trewin | scraped: 39 US MLS + 6 Toronto/Vancouver; exclude USL clubs (Miami FC, Colorado Springs, El Paso) |
| nat114 | Name a player at the 2026 World Cup who played for a Turkish club | en:2026 FIFA World Cup squads (`clubnat=TUR`) | 45 | modern | Leroy Sané, N'Golo Kanté, Edson Álvarez, Noa Lang, Kerem Aktürkoğlu | scraped 45 |
| nat115 | Name a player at the 2026 World Cup who played for a Brazilian club | en:2026 FIFA World Cup squads (`clubnat=BRA`) | 32 | modern | Neymar, Lucas Paquetá, Memphis Depay, Giorgian de Arrascaeta, Isidro Pitta | scraped 32 |
| nat116 | Name a player at the 2022 World Cup who played for a Qatari club | en:2022 FIFA World Cup squads (`clubnat=QAT`) | 33 | modern | Akram Afif, Almoez Ali, André Ayew, Youssef Msakni, Shojae Khalilzadeh | scraped 33 (26 Qatar players + 7 from other nations) |
| nat117 | Name an Al Hilal player who went to the 2026 World Cup | en:2026 FIFA World Cup squads (`club` = Al Hilal SFC) | 12 | modern | Kalidou Koulibaly, Darwin Núñez, Théo Hernandez, Yassine Bounou, Salem Al-Dawsari | scraped 12 |
| nat118 | Name an Atlético Madrid player who went to the 2026 World Cup | en:2026 FIFA World Cup squads (`club` = Atlético Madrid) | 12 | modern | Julián Alvarez, Alexander Sørloth, Marcos Llorente, Giuliano Simeone, Obed Vargas | scraped 12 |
| nat119 | Name a player at the 2026 World Cup who played for a Scottish club | en:2026 FIFA World Cup squads (`clubnat=SCO`) | 20 | modern | Daizen Maeda, Kieran Tierney, Craig Gordon, Yang Hyun-jun, Alistair Johnston | scraped 20 |
| nat120 | Name a player at the 2026 World Cup who played for a Mexican club | en:2026 FIFA World Cup squads (`clubnat=MEX`) | 26 | modern | Enner Valencia, Alexis Vega, Gilberto Mora, Ismael Díaz, Yoel Bárcenas | scraped 26 |
| nat121 | Name a player at the 2026 World Cup who played for a Dutch club | en:2026 FIFA World Cup squads (`clubnat=NED`) | 38 | modern | Ivan Perišić, Wout Weghorst, Ricardo Pepi, Ayase Ueda, Juninho Bacuna | scraped 38; 12 of them Curaçao players |
| nat122 | Name a player at Euro 2024 who played for a Turkish club | en:UEFA Euro 2024 squads (`clubnat=TUR`) | 25 | modern | Dušan Tadić, Ferdi Kadıoğlu, Dominik Livaković, Sebastian Szymański, Rey Manaj | scraped 25 |
| nat123 | Name a player at Euro 2024 who played for a Saudi Arabian club | en:UEFA Euro 2024 squads (`clubnat=KSA`) | 13 | modern | Cristiano Ronaldo, N'Golo Kanté, Aymeric Laporte, Sergej Milinković-Savić, Solomon Kvirkvelia | scraped 13 |

## Ages, shirt numbers and positions
| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| nat124 | Name a player born in 2001 or later who was in a 2022 World Cup squad | en:2022 FIFA World Cup squads (birth year) | 79 | modern | Jude Bellingham, Jamal Musiala, Gavi, Pedri, Garang Kuol | scraped 79 |
| nat125 | Name a player born in 1987 or earlier who was in a 2022 World Cup squad | en:2022 FIFA World Cup squads (birth year) | 41 | modern | Lionel Messi, Cristiano Ronaldo, Luka Modrić, Pepe, Atiba Hutchinson | scraped 41 |
| nat126 | Name a player born in 2003 or later who was in a Euro 2024 squad | en:UEFA Euro 2024 squads (birth year) | 32 | modern | Lamine Yamal, Jude Bellingham, Kenan Yıldız, Arda Güler, Leo Sauer | scraped 32 |
| nat127 | Name a player who wore the No. 9 shirt at the 2022 World Cup | en:2022 FIFA World Cup squads (`no=9`) | 32 | modern | Olivier Giroud, Harry Kane, Richarlison, Julián Alvarez, Issam Jebali | one per team |
| nat128 | Name a player who wore the No. 10 shirt at Euro 2024 | en:UEFA Euro 2024 squads (`no=10`) | 24 | modern | Jude Bellingham, Kylian Mbappé, Jamal Musiala, Luka Modrić, Giorgi Chakvetadze | one per team |
| nat129 | Name a goalkeeper in a Euro 2024 squad | en:UEFA Euro 2024 squads (`pos=GK`) | 72 | modern | Unai Simón, Jordan Pickford, Manuel Neuer, Giorgi Mamardashvili, Bart Verbruggen | scraped 72 (3 per team) |
| nat130 | Name a goalkeeper in a 2022 World Cup squad | en:2022 FIFA World Cup squads (`pos=GK`) | 99 | modern | Emiliano Martínez, Thibaut Courtois, Yassine Bounou, Wojciech Szczęsny, Matt Turner | scraped 99 |

## Stadiums and host cities
| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| nat131 | Name a stadium that hosted a match at the 2018 or 2022 World Cup | en:2018 FIFA World Cup#Venues, en:2022 FIFA World Cup#Venues | 20 | modern | Luzhniki Stadium, Lusail Stadium, Al Bayt Stadium, Stadium 974, Ekaterinburg Arena | 12 + 8 |
| nat132 | Name a stadium that hosted a match at Euro 2020 or Euro 2024 | en:UEFA Euro 2020#Venues, en:UEFA Euro 2024#Venues | 20 | modern | Wembley Stadium, Allianz Arena, Olympiastadion (Berlin), Baku Olympic Stadium, Arena Națională | 11 + 10 with Munich shared |
| nat133 | Name a stadium that will host a match at the 2030 World Cup or Euro 2028 | en:2030 FIFA World Cup#Venues, en:UEFA Euro 2028#Venues | 29 | modern | Santiago Bernabéu Stadium, Wembley Stadium, Camp Nou, Hampden Park, Grand Stade Hassan II | scraped 20 + 9; Euro 2032 omitted because its venue list was still a candidate list |
| nat134 | Name a stadium that hosted a match at the 2024 Copa América | en:2024 Copa América#Venues | 14 | modern | Hard Rock Stadium, MetLife Stadium, SoFi Stadium, Mercedes-Benz Stadium, Children's Mercy Park | |
| nat135 | Name a stadium that hosted a match at the 2023 or 2025 Africa Cup of Nations | en:2023 Africa Cup of Nations#Venues, en:2025 Africa Cup of Nations#Venues | 15 | modern | Alassane Ouattara Stadium, Prince Moulay Abdellah Stadium, Grand Stade de Marrakech, Stade de la Paix, Stade Laurent Pokou | 6 + 9 |
| nat136 | Name a stadium that hosted a match at the 2019 or 2023 AFC Asian Cup | en:2019 AFC Asian Cup#Venues, en:2023 AFC Asian Cup#Venues | 17 | modern | Lusail Stadium, Khalifa International Stadium, Zayed Sports City Stadium, Al Janoub Stadium, Sharjah Stadium | 8 + 9 |
| nat137 | Name a stadium that hosted a match at the 2025 CONCACAF Gold Cup | en:2025 CONCACAF Gold Cup#Venues | 14 | modern | NRG Stadium, SoFi Stadium, Levi's Stadium, BC Place, Shell Energy Stadium | final at NRG Stadium |
| nat138 | Name a stadium that has hosted a men's European Championship final | en:List of UEFA European Championship finals (venue column) | 15 | classic | Wembley Stadium, Stade de France, Estádio da Luz, Stadio Olimpico, Parc des Princes | old and new Wembley are separate articles (Wembley Stadium (1923)) |

## Current squads and all-time leaders by country
| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| nat139 | Name a player in England's current squad or recent call-ups | en:England national football team#Current squad + #Recent call-ups | 52 | modern | Harry Kane, Jude Bellingham, Cole Palmer, Elliot Anderson, James Trafford | live list (scraped 22 + 30); re-scrape before each season |
| nat140 | Name a player in France's current squad or recent call-ups | en:France national football team#Current squad + #Recent call-ups | 44 | modern | Kylian Mbappé, Ousmane Dembélé, William Saliba, Rayan Cherki, Maghnes Akliouche | live list (21 + 23) |
| nat141 | Name a player in Brazil's current squad or recent call-ups | en:Brazil national football team#Current squad + #Recent call-ups | 74 | modern | Vinícius Júnior, Raphinha, Marquinhos, Estêvão, Andrey Santos | live list (25 + 49) |
| nat142 | Name a player in Argentina's current squad or recent call-ups | en:Argentina national football team#Current squad + #Recent call-ups | 67 | modern | Lionel Messi, Lautaro Martínez, Enzo Fernández, Franco Mastantuono, Valentín Barco | live list (34 + 33) |
| nat143 | Name a player in Spain's current squad or recent call-ups | en:Spain national football team#Current squad + #Recent call-ups | 53 | modern | Lamine Yamal, Pedri, Rodri, Dean Huijsen, Samu Omorodion | live list (24 + 29) |
| nat144 | Name a player in Germany's current squad or recent call-ups | en:Germany national football team#Current squad + #Recent call-ups | 57 | modern | Jamal Musiala, Florian Wirtz, Joshua Kimmich, Nick Woltemade, Assan Ouédraogo | live list (39 + 18) |
| nat145 | Name a player in Portugal's current squad or recent call-ups | en:Portugal national football team#Current squad + #Recent call-ups | 39 | modern | Cristiano Ronaldo, Bruno Fernandes, Vitinha, João Neves, Francisco Conceição | live list (24 + 15) |
| nat146 | Name a player in Italy's current squad or recent call-ups | en:Italy national football team#Current squad + #Recent call-ups | 76 | modern | Gianluigi Donnarumma, Nicolò Barella, Sandro Tonali, Mateo Retegui, Francesco Pio Esposito | live list (30 + 46); Italy missed the 2026 World Cup |
| nat147 | Name a player in the Netherlands' current squad or recent call-ups | en:Netherlands national football team#Current squad + #Recent call-ups | 44 | modern | Virgil van Dijk, Cody Gakpo, Frenkie de Jong, Jorrel Hato, Quinten Timber | live list (23 + 21) |
| nat148 | Name a player in the United States' current squad or recent call-ups | en:United States men's national soccer team#Current squad + #Recent call-ups | 55 | modern | Christian Pulisic, Weston McKennie, Tyler Adams, Diego Luna, Patrick Agyemang | live list (28 + 27) |
| nat149 | Name a player in France's all-time top 10 for caps or for goals | en:France national football team#Most appearances + #Top goalscorers | 15 | 2000s+ | Kylian Mbappé, Olivier Giroud, Thierry Henry, Hugo Lloris, Just Fontaine | scraped union 15 |
| nat150 | Name a player in Brazil's all-time top 10 for caps or for goals | en:Brazil national football team#Most appearances + #Top goalscorers | 20 | 2000s+ | Neymar, Pelé, Ronaldo, Cafu, Jairzinho | scraped union 20 (ties) |
| nat151 | Name a player in Argentina's all-time top 10 for caps or for goals | en:Argentina national football team#Most appearances + #Top goalscorers | 18 | 2000s+ | Lionel Messi, Gabriel Batistuta, Ángel Di María, Javier Mascherano, Luis Artime | scraped union 18 |
| nat152 | Name a player in Portugal's all-time top 10 for caps or for goals | en:Portugal national football team#Most appearances + #Top goalscorers | 16 | 2000s+ | Cristiano Ronaldo, Pepe, Luís Figo, Pauleta, Hélder Postiga | scraped union 16 |
| nat153 | Name a player in the United States' all-time top 10 for caps or for goals | en:United States men's national soccer team#Most appearances + #Top goalscorers | 17 | 2000s+ | Landon Donovan, Clint Dempsey, Christian Pulisic, Cobi Jones, Eric Wynalda | scraped union 17 |
| nat154 | Name a player in Nigeria's all-time top 10 for caps or for goals | en:Nigeria national football team#Most appearances + #Top goalscorers | 17 | 2000s+ | Victor Osimhen, Ahmed Musa, Rashidi Yekini, Vincent Enyeama, Segun Odegbami | union of two top-10 tables (scraped 10 + 10) |
| nat155 | Name a player in South Korea's all-time top 10 for caps or for goals | en:South Korea national football team#Most appearances + #Top goalscorers | 21 | 2000s+ | Son Heung-min, Cha Bum-kun, Hong Myung-bo, Lee Woon-jae, Kim Jae-han | scraped union 21 (ties) |
| nat156 | Name a player in Egypt's all-time top 10 for caps or for goals | en:Egypt national football team#Most appearances + #Top goalscorers | 16 | 2000s+ | Mohamed Salah, Hossam Hassan, Ahmed Hassan, Mohamed Aboutrika, Hassan El-Shazly | scraped union 16 |
| nat157 | Name the all-time top scorer of a UEFA national team | en:List of top international men's football goalscorers by country (filter UEFA members) | 56 | 2000s+ | Cristiano Ronaldo, Harry Kane, Robert Lewandowski, Edin Džeko, Andy Selva | 55 nations, ties add rows; confederation from en:List of men's national association football teams |
| nat158 | Name the all-time top scorer of an African (CAF) national team | en:List of top international men's football goalscorers by country (filter CAF members) | 55 | 2000s+ | Samuel Eto'o, Didier Drogba, Rashidi Yekini, Islam Slimani, Godfrey Chitalu | 54 CAF nations, ties add rows; Egypt = Hossam Hassan unless Salah overtakes |
| nat159 | Name the all-time top scorer of an Asian (AFC) national team | en:List of top international men's football goalscorers by country (filter AFC members) | 48 | 2000s+ | Ali Daei, Son Heung-min, Sunil Chhetri, Almoez Ali, Mokhtar Dahari | |
| nat160 | Name the all-time top scorer of a CONCACAF national team | en:List of top international men's football goalscorers by country (filter CONCACAF members) | 42 | 2000s+ | Jonathan David, Landon Donovan, Javier Hernández, Carlos Ruiz, Deon McCaulay | |
| nat161 | Name a South American man with 100 or more international caps | en:List of men's footballers with 100 or more international caps (Confederation = CONMEBOL) | 72 | 2000s+ | Lionel Messi, Luis Suárez, Neymar, Enner Valencia, Alexis Sánchez | scraped 72 |
| nat162 | Name an African man with 100 or more international caps | en:List of men's footballers with 100 or more international caps (Confederation = CAF) | 67 | 2000s+ | Sadio Mané, Mohamed Salah, Ahmed Hassan, Rigobert Song, Ahmed Musa | scraped 67 |
| nat163 | Name a CONCACAF man with 100 or more international caps | en:List of men's footballers with 100 or more international caps (Confederation = CONCACAF) | 83 | 2000s+ | Landon Donovan, Andrés Guardado, Guillermo Ochoa, Atiba Hutchinson, Aníbal Godoy | scraped 83 |

## Goals against: who has this striker scored against?
| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| nat164 | Name a country Lionel Messi has scored against | en:List of international goals scored by Lionel Messi (opponent column) | 45 | 2000s+ | Brazil, Bolivia, Croatia, Estonia, Guatemala | scraped 46 national-team links incl. own side → ~45 |
| nat165 | Name a country Cristiano Ronaldo has scored against | en:List of international goals scored by Cristiano Ronaldo (opponent column) | 48 | 2000s+ | Spain, Luxembourg, Ghana, Andorra, Faroe Islands | scraped ~48 |
| nat166 | Name a country Harry Kane has scored against | en:List of international goals scored by Harry Kane (opponent column) | 37 | modern | Germany, Italy, San Marino, Malta, Andorra | scraped ~37 |
| nat167 | Name a country Robert Lewandowski has scored against | en:List of international goals scored by Robert Lewandowski (opponent column) | 38 | 2000s+ | San Marino, Saudi Arabia, France, Gibraltar, Moldova | scraped ~38 |
| nat168 | Name a country Kylian Mbappé has scored against | en:List of international goals scored by Kylian Mbappé (opponent column) | 33 | modern | Argentina, Croatia, Poland, Gibraltar, Netherlands | scraped ~33 |
| nat169 | Name a country Neymar has scored against | en:List of international goals scored by Neymar (opponent column) | 31 | 2000s+ | Croatia, Peru, Japan, Bolivia, Panama | scraped ~31 |
| nat170 | Name a country Romelu Lukaku has scored against | en:List of international goals scored by Romelu Lukaku (opponent column) | 39 | 2000s+ | Tunisia, Panama, Russia, Gibraltar, Azerbaijan | scraped ~39 |
| nat171 | Name a country Erling Haaland has scored against | en:List of international goals scored by Erling Haaland (opponent column) | 27 | modern | Italy, Moldova, Israel, Gibraltar | scraped ~27 (includes 2026 World Cup goals) |
| nat172 | Name a country Edin Džeko has scored against | en:List of international goals scored by Edin Džeko (opponent column) | 33 | 2000s+ | Liechtenstein, Luxembourg, Greece, Iran, Wales | scraped ~33 |
| nat173 | Name a country Sunil Chhetri has scored against | en:List of international goals scored by Sunil Chhetri (opponent column) | 32 | 2000s+ | Pakistan, Kenya, Afghanistan, Thailand, Kuwait | scraped ~32 |
| nat174 | Name a country Ali Daei scored against | en:List of international goals scored by Ali Daei (opponent column) | 35 | 2000s+ | South Korea, Japan, Laos, Guam, Maldives | scraped ~35 (1993–2006) |

## World Cup and Euro scorers by nation
| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| nat175 | Name a player who has scored for England at a men's World Cup | en:England at the FIFA World Cup (goalscorers by tournament table) | 45 | classic | Harry Kane, Gary Lineker, Geoff Hurst, Bukayo Saka, Anthony Gordon | includes 2026 |
| nat176 | Name a player who has scored for England at a men's European Championship | en:England at the UEFA European Championship (match results, scorers column) | 38 | 2000s+ | Alan Shearer, Harry Kane, Wayne Rooney, Cole Palmer, Andy Carroll | exclude opponents' own goals |
| nat177 | Name a player who has scored for Brazil at a men's World Cup | en:Brazil at the FIFA World Cup (match results, scorers column) | 75 | classic | Ronaldo, Pelé, Neymar, Richarlison, Casemiro | |
| nat178 | Name a player who has scored for Spain at a men's World Cup | en:Spain at the FIFA World Cup (match results, scorers column) | 55 | 2000s+ | David Villa, Andrés Iniesta, Álvaro Morata, Mikel Oyarzabal, Fernando Hierro | includes 2026 title run |
| nat179 | Name a player who has scored for Portugal at a men's World Cup | en:Portugal at the FIFA World Cup (match results, scorers column) | 30 | 2000s+ | Cristiano Ronaldo, Eusébio, Gonçalo Ramos, Pepe, Deco | |
| nat180 | Name a player who has scored for Mexico at a men's World Cup | en:Mexico at the FIFA World Cup (match results, scorers column) | 45 | 2000s+ | Javier Hernández, Rafael Márquez, Hirving Lozano, Raúl Jiménez, Luis Hernández | |
| nat181 | Name a player who has scored for the United States at a men's World Cup | en:United States at the FIFA World Cup (match results, scorers column) | 35 | 2000s+ | Christian Pulisic, Landon Donovan, Clint Dempsey, Timothy Weah, Bert Patenaude | |
| nat182 | Name a player who has scored for Japan at a men's World Cup | en:Japan at the FIFA World Cup (match results, scorers column) | 22 | 2000s+ | Keisuke Honda, Ritsu Dōan, Takuma Asano, Ao Tanaka, Junichi Inamoto | scraped ~23 |
| nat183 | Name a player who has scored for Morocco at a men's World Cup | en:Morocco at the FIFA World Cup (goalscorers table) | 22 | 2000s+ | Youssef En-Nesyri, Hakim Ziyech, Azzedine Ounahi, Achraf Dari, Abdeljalil Hadda | scraped 22 rows |

## Records and awards
| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| nat184 | Name a player who has scored 5 or more goals at men's World Cups | en:List of FIFA World Cup top goalscorers (overall table, "at least 5 goals") | 111 | classic | Miroslav Klose, Lionel Messi, Kylian Mbappé, Ronaldo, Oleg Salenko | page states 111 players with 5+ |
| nat185 | Name a player who has scored an own goal at a men's World Cup | en:List of FIFA World Cup own goals | 75 | 2000s+ | Marcelo, Mario Mandžukić, Sergio Ramos, Aziz Behich, Ernie Brandts | 68+ rows incl. 2026; dedupe repeat offenders |
| nat186 | Name a player who has been sent off at a men's World Cup since 2010 | en:List of FIFA World Cup red cards (Tournament 2010–2026) | 50 | modern | Luis Suárez, Jérôme Boateng, Vincent Aboubakar, Wayne Hennessey, Igor Smolnikov | estimate (table uses rowspans per tournament); 2010–2026 rows |
| nat187 | Name a player who switched to a second senior national team in 2021 or later | en:List of association football players capped by two senior national teams#2021–present | 80 | modern | Brahim Díaz, Iñaki Williams, Houssem Aouar, Munir El Haddadi, Steven Caulker | 92 rows incl. ~10 women flagged "(female)"; men only → ~80 |
| nat188 | Name a player named in the UEFA Team of the Tournament at Euro 2016, 2020 or 2024 | en:UEFA European Championship awards (Team of the Tournament table) | 31 | modern | Cristiano Ronaldo, Lamine Yamal, Rodri, Leonardo Bonucci, Joshua Kimmich | 3 × 11 minus repeats |
| nat189 | Name a winner of the World Cup Golden Ball, Golden Boot, Golden Glove or Young Player Award since 2006 | en:FIFA World Cup awards | 21 | 2000s+ | Lionel Messi, Kylian Mbappé, Luka Modrić, Enzo Fernández, Pau Cubarsí | 6 tournaments × 4 awards minus repeats |
| nat190 | Name a player who has scored a hat-trick for England | en:List of England national football team hat-tricks | 50 | classic | Harry Kane, Wayne Rooney, Raheem Sterling, Michael Owen, Jermain Defoe | mostly pre-1990 entries; modern names keep it fun |
| nat191 | Name a player who has scored a hat-trick at the Copa América | en:List of Copa América hat-tricks | 60 | classic | Lionel Messi, Pelé, Paolo Guerrero, Eduardo Vargas, Javier Saviola | 72 rows, dedupe; mostly pre-1960 |

## Women's, youth and Olympic football
| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| nat192 | Name a player in Spain's 2023 Women's World Cup-winning squad | en:2023 FIFA Women's World Cup squads#Spain | 23 | modern | Aitana Bonmatí, Alexia Putellas, Olga Carmona, Salma Paralluelo, Misa Rodríguez | squad family |
| nat193 | Name a player in England's Women's Euro 2025-winning squad | en:UEFA Women's Euro 2025 squads#England | 23 | modern | Lucy Bronze, Chloe Kelly, Alessia Russo, Michelle Agyemang, Hannah Hampton | squad family |
| nat194 | Name a player in England's 2023 UEFA European Under-21 Championship-winning squad | en:2023 UEFA European Under-21 Championship squads#England | 23 | modern | Cole Palmer, Anthony Gordon, Morgan Gibbs-White, Curtis Jones, Taylor Harwood-Bellis | squad family |
| nat195 | Name a player in Spain's 2024 Olympic gold-medal squad | en:Football at the 2024 Summer Olympics – Men's team squads#Spain | 22 | modern | Fermín López, Pau Cubarsí, Álex Baena, Sergio Gómez, Arnau Tenas | squad family; include listed alternates |
| nat196 | Name a player who scored at the 2023 Women's World Cup | en:2023 FIFA Women's World Cup#Goalscorers | 100 | modern | Aitana Bonmatí, Hinata Miyazawa, Alexandra Popp, Lauren James, Barbra Banda | scraped 100 |
| nat197 | Name a country that played at Women's Euro 2025 | en:UEFA Women's Euro 2025 squads (team sections) | 16 | modern | England, Spain, Wales, Poland, Iceland | |
| nat198 | Name a player who scored at Women's Euro 2025 | en:UEFA Women's Euro 2025#Goalscorers | 74 | modern | Alexia Putellas, Esther González, Michelle Agyemang, Lauren James, Hannah Cain | scraped 74 |
| nat199 | Name a country that played at the 2023 Women's World Cup | en:2023 FIFA Women's World Cup squads (team sections) | 32 | modern | Spain, England, Australia, Morocco, Zambia | women's national-team articles |
| nat200 | Name a country that played in the men's football tournament at the 2024 Olympics | en:Football at the 2024 Summer Olympics – Men's team squads (team sections) | 16 | modern | Spain, France, Argentina, Morocco, Uzbekistan | |

## Summary
**Total prompts: 200** (nat001–nat200). Answer-count estimates range from 12 to 117; median about 26.

**Era split:** modern 151 (75.5%) · 2000s+ 43 (21.5%) · classic 6 (3%).

**Per sub-heading:**
| sub-heading | prompts |
|---|---|
| 2026 World Cup | 15 |
| Squads | 16 |
| Finals and multi-tournament squads | 16 |
| Tournament goalscorers | 16 |
| Countries and qualification | 15 |
| Managers and captains | 23 |
| Club and league representation at tournaments | 22 |
| Ages, shirt numbers and positions | 7 |
| Stadiums and host cities | 8 |
| Current squads and all-time leaders by country | 25 |
| World Cup and Euro scorers by nation | 9 |
| Goals against: who has this striker scored against? | 11 |
| Records and awards | 8 |
| Women's, youth and Olympic football | 9 |

**Largest template families** (all at or under 10% of the theme): "<team>'s <tournament> squad" 20 (16 men's senior + 4 women's/U21/Olympic); "scored at <tournament>" 20 (including the 2026, women's and knockout-only variants); head coach at a tournament 13; "<club> player at <tournament>" 12; "<country> current squad or recent call-ups" 10; "<league>-based player at <tournament>" 10; "country <striker> has scored against" 11; country at a tournament 10; captains 8; all-time top 10 for caps or goals 8.

**Verification:** all 107 distinct source page titles were checked with the Wikipedia API (`redirects=1`), in batches of 50 or fewer at about 2 requests per second. None is missing. Titles that resolve through a redirect were swapped for their target: "List of top international men's football goalscorers by country", "UEFA European Championship awards" (the redirect from "…Team of the Tournament") and "List of FIFA World Cup top goalscorers". Unverified titles that came back missing were replaced or dropped. For example, Son Heung-min and Lautaro Martínez have no "List of international goals scored by…" page; the Nigeria, Japan and Republic of Ireland manager lists don't exist, so Nigeria uses the team article's #Coaching history section; there is no "2022/2018 FIFA World Cup statistics" page, so those prompts use the main tournament article's #Goalscorers section. About 120 counts were scraped from the live pages (marked "scraped" in notes): squad templates, goalscorer sections, coach/captain fields, table rows and opponent links.

**Risky prompts:**
- Live lists that change over time: nat139–nat148 (current squads and recent call-ups) and nat073 (FIFA ranking top 20). Re-scrape them each season, or freeze them as dated snapshots.
- nat004 (2026 host cities): FIFA's host-city labels ("New York New Jersey", "San Francisco Bay Area", "Boston", "Dallas", "Miami") are not the municipality articles. The scraper needs the alias map given in the notes.
- Red cards at the World Cup since 2010: the count is an estimate, because the table uses rowspans per tournament.
- UEFA play-offs for 2026: the #Second round section also links teams that only appear in the Nations League seeding tables. Scrape only the path brackets (expected 16).
- Morocco's AFCON 2025 squad, and AFCON winners: Wikipedia footnotes the 2025 title as "awarded" to Morocco over Senegal. Prompts avoid the word "winning", and the AFCON-winners prompt should follow whatever the results table shows.
- All-time top scorer by confederation (UEFA/CAF/AFC/CONCACAF): needs a country → confederation join, and shared records add rows.
- Players who switched national team in 2021 or later: the source section mixes in women players flagged "(female)". Filter them out (about 80 men remain).
- England captains since 2000: the estimate is 45–51, and one-off friendly captains inflate it.
- Euro 2024 knockout scorers: the quick scrape missed Ollie Watkins's link, so check the match-box parsing.
- Floor-size prompts (12–13 answers): Crystal Palace / Al Hilal / Atlético players at the 2026 World Cup, Real Madrid at 2022, Inter and Saudi-based players at Euro 2024, and the Olympic medal nations. They are fine, but there is no slack if a page edit drops a row.
- Near the ceiling: 2022 World Cup scorers (117), 2018 World Cup scorers (110), players with 5+ World Cup goals (111) and 2022 World Cup goalkeepers (99).
- Deep-cut-heavy prompts, where answers beyond the first few are obscure: Saudi Arabia and Nigeria coaches since 2000, CONCACAF/AFC member nations, Ali Daei's and Sunil Chhetri's opponents, and Curaçao-heavy Dutch-club players at the 2026 World Cup.
