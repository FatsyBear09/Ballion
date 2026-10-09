# Champions League prompts (`ucl`)

Theme: UEFA Champions League plus some European Cup history. Scope excludes Europa/Conference League, Super Cup and Club World Cup (General theme) and national-team football.
All source page titles below were verified to exist on en.wikipedia via the query API on 2026-10-09 (redirects noted where relevant).
Shared rules unless a note says otherwise: "played in a final" = started or came on (`{{subon}}`), unused substitutes and managers excluded; "made an appearance" = ≥1 UCL appearance (qualifying excluded) in the club season page's statistics table; goal prompts exclude own goals and qualifying rounds; era tags follow SPEC.md.
Estimates for finals, knockout and league-phase scorers, hat-tricks, stadiums and clubs-by-country come from parsing the source wikitext (the quick parser undercounts slightly); the rest are hand estimates.

## Finals: who played

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ucl001 | Name a player who played in the 2026 Champions League final (PSG v Arsenal) | en:2026 UEFA Champions League final (Details lineups) | 33 | modern | Ousmane Dembélé, Bukayo Saka, Khvicha Kvaratskhelia, Martín Zubimendi, Senny Mayulu | starters + subs marked {{subon}}; unused subs and managers excluded (same rule for every single-final prompt) |
| ucl002 | Name a player who played in the 2025 Champions League final (PSG 5–0 Inter) | en:2025 UEFA Champions League final (Details) | 32 | modern | Ousmane Dembélé, Lautaro Martínez, Désiré Doué, Yann Aurel Bisseck, Senny Mayulu | starters + used subs |
| ucl003 | Name a player who played in the 2024 Champions League final (Dortmund v Real Madrid) | en:2024 UEFA Champions League final (Details) | 30 | modern | Vinícius Júnior, Jude Bellingham, Jadon Sancho, Niclas Füllkrug, Ian Maatsen | starters + used subs |
| ucl004 | Name a player who played in the 2023 Champions League final (Man City v Inter) | en:2023 UEFA Champions League final (Details) | 28 | modern | Erling Haaland, Rodri, Lautaro Martínez, Federico Dimarco, Robin Gosens | starters + used subs; lineup markup differs from other finals, check scraper |
| ucl005 | Name a player who played in the 2022 Champions League final (Liverpool v Real Madrid) | en:2022 UEFA Champions League final (Details) | 28 | modern | Mohamed Salah, Vinícius Júnior, Thibaut Courtois, Fabinho, Naby Keïta | starters + used subs |
| ucl006 | Name a player who played in the 2021 Champions League final (Man City v Chelsea) | en:2021 UEFA Champions League final (Details) | 28 | modern | Kai Havertz, Kevin De Bruyne, N'Golo Kanté, Mason Mount, Fernandinho | starters + used subs |
| ucl007 | Name a player who played in the 2020 Champions League final (PSG v Bayern) | en:2020 UEFA Champions League final (Details) | 30 | modern | Neymar, Kylian Mbappé, Kingsley Coman, Joshua Kimmich, Ander Herrera | starters + used subs |
| ucl008 | Name a player who played in the 2019 Champions League final (Tottenham v Liverpool) | en:2019 UEFA Champions League final (Details) | 28 | modern | Mohamed Salah, Harry Kane, Divock Origi, Kieran Trippier, Fernando Llorente | starters + used subs |
| ucl009 | Name a player who played in the 2018 Champions League final (Real Madrid v Liverpool) | en:2018 UEFA Champions League final (Details) | 27 | modern | Gareth Bale, Mohamed Salah, Loris Karius, Adam Lallana, Nacho | starters + used subs |
| ucl010 | Name a player who played in the 2017 Champions League final (Juventus v Real Madrid) | en:2017 UEFA Champions League final (Details) | 28 | modern | Cristiano Ronaldo, Mario Mandžukić, Gonzalo Higuaín, Isco, Marco Asensio | starters + used subs |
| ucl011 | Name a player who played in the 2016 Champions League final (Real Madrid v Atlético) | en:2016 UEFA Champions League final (Details) | 28 | modern | Cristiano Ronaldo, Antoine Griezmann, Yannick Carrasco, Lucas Vázquez, Augusto Fernández | starters + used subs |
| ucl012 | Name a player who played in the 2015 Champions League final (Juventus v Barcelona) | en:2015 UEFA Champions League final (Details) | 28 | modern | Lionel Messi, Neymar, Paul Pogba, Ivan Rakitić, Roberto Pereyra | starters + used subs |
| ucl013 | Name a player who played in the 2014 Champions League final (Real Madrid v Atlético, Lisbon) | en:2014 UEFA Champions League final (Details) | 29 | 2000s+ | Cristiano Ronaldo, Sergio Ramos, Diego Costa, Thibaut Courtois, José Sosa | starters + used subs |
| ucl014 | Name a player who played in the 2012 Champions League final (Bayern v Chelsea) | en:2012 UEFA Champions League final (Details) | 26 | 2000s+ | Didier Drogba, Arjen Robben, Juan Mata, Ryan Bertrand, Anatoliy Tymoshchuk | starters + used subs |
| ucl015 | Name a player who played in the 2008 Champions League final (Man United v Chelsea, Moscow) | en:2008 UEFA Champions League final (Details) | 28 | 2000s+ | Cristiano Ronaldo, John Terry, Frank Lampard, Owen Hargreaves, Juliano Belletti | starters + used subs |
| ucl016 | Name a player who played in the 2005 Champions League final (Milan v Liverpool, Istanbul) | en:2005 UEFA Champions League final (Details) | 28 | 2000s+ | Steven Gerrard, Kaká, Andriy Shevchenko, Djimi Traoré, Vladimír Šmicer | starters + used subs |
| ucl017 | Name a player who played in the 1999 Champions League final (Man United v Bayern) | en:1999 UEFA Champions League final (Details) | 27 | classic | David Beckham, Ole Gunnar Solskjær, Teddy Sheringham, Oliver Kahn, Carsten Jancker | starters + used subs |
| ucl018 | Name a player who played in a Champions League final for an English club, 2018 onward | en:2018, 2019, 2021, 2022, 2023, 2026 UEFA Champions League final pages (Details) | 85 | modern | Mohamed Salah, Harry Kane, Bukayo Saka, Mason Mount, Moussa Sissoko | Liverpool, Tottenham, Chelsea, Man City, Arsenal sides only; starters + used subs; dedupe |

## Finals: clubs across eras

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ucl019 | Name a player who played in a Champions League final for Barcelona (2006, 2009 or 2011) | en:2006 / 2009 / 2011 UEFA Champions League final (Details) | 33 | 2000s+ | Lionel Messi, Ronaldinho, Xavi, Eric Abidal, Oleguer | Barcelona side only; starters + used subs (same rule for all club-era final prompts) |
| ucl020 | Name a player who played in a Champions League final for Manchester United (1999, 2008, 2009 or 2011) | en:1999 / 2008 / 2009 / 2011 UEFA Champions League final (Details) | 45 | 2000s+ | Cristiano Ronaldo, Wayne Rooney, Ryan Giggs, Park Ji-sung, Jesper Blomqvist | Man United side only |
| ucl021 | Name a player who played in a Champions League final for Juventus (1996–2017) | en:1996, 1997, 1998, 2003, 2015, 2017 UEFA Champions League final pages | 65 | 2000s+ | Alessandro Del Piero, Gianluigi Buffon, Zinedine Zidane, Paulo Dybala, Mark Iuliano | Juventus side only |
| ucl022 | Name a player who played in a Champions League final for Real Madrid (1998, 2000 or 2002) | en:1998 / 2000 / 2002 UEFA Champions League final (Details) | 33 | 2000s+ | Raúl, Roberto Carlos, Zinedine Zidane, Fernando Morientes, Iván Campo | Real Madrid side only |
| ucl023 | Name a player who played in a Champions League final for Bayern Munich (1999–2013) | en:1999, 2001, 2010, 2012, 2013 UEFA Champions League final pages | 55 | 2000s+ | Thomas Müller, Arjen Robben, Oliver Kahn, Stefan Effenberg, Hans-Jörg Butt | Bayern side only; 2020 final deliberately excluded |
| ucl024 | Name a player who played in a European Cup final for Real Madrid, 1956–1960 | en:1956, 1957, 1958, 1959, 1960 European Cup final pages | 24 | classic | Alfredo Di Stéfano, Ferenc Puskás, Paco Gento, Raymond Kopa, Héctor Rial | Real Madrid side only; no substitutes in that era |
| ucl025 | Name a player who played in a European Cup final for Benfica, Inter or Milan, 1961–1965 | en:1961, 1962, 1963, 1964, 1965 European Cup final pages | 40 | classic | Eusébio, Gianni Rivera, Sandro Mazzola, Mário Coluna, Giovanni Trapattoni | those three clubs' sides only (Real Madrid and Barcelona players in those finals excluded) |
| ucl026 | Name a player who played in the 1967 or 1968 European Cup final | en:1967 European Cup final; en:1968 European Cup final | 44 | classic | Bobby Charlton, George Best, Eusébio, Billy McNeill, Jimmy Johnstone | both teams in both finals (Celtic, Inter, Man United, Benfica) |
| ucl027 | Name a player who played in a European Cup final for Ajax, 1971–1973 | en:1971, 1972, 1973 European Cup final pages | 22 | classic | Johan Cruyff, Johan Neeskens, Ruud Krol, Piet Keizer, Johnny Rep | Ajax side only |
| ucl028 | Name a player who played in a European Cup final for Bayern Munich, 1974–1976 | en:1974, 1975, 1976 European Cup final pages | 22 | classic | Franz Beckenbauer, Gerd Müller, Sepp Maier, Uli Hoeneß, Karl-Heinz Rummenigge | Bayern side only; 1974 replay included |
| ucl029 | Name a player who played in a European Cup final for Liverpool, 1977–1984 | en:1977, 1978, 1981, 1984 European Cup final pages | 30 | classic | Kenny Dalglish, Ian Rush, Graeme Souness, Bruce Grobbelaar, Alan Kennedy | Liverpool side only; 1985 final excluded |
| ucl030 | Name a player who played in a European Cup final for Nottingham Forest or Aston Villa (1979–1982) | en:1979, 1980, 1982 European Cup final pages | 28 | classic | Peter Shilton, Trevor Francis, Peter Withe, John Robertson, Nigel Spink | Forest and Villa sides only |
| ucl031 | Name a player who played in a final for AC Milan, 1989–1995 | en:1989 & 1990 European Cup final; 1993, 1994, 1995 UEFA Champions League final pages | 36 | classic | Paolo Maldini, Marco van Basten, Ruud Gullit, Frank Rijkaard, Daniele Massaro | Milan side only |
| ucl032 | Name a player who played in a Champions League final for Ajax (1995 or 1996) | en:1995 / 1996 UEFA Champions League final (Details) | 22 | classic | Patrick Kluivert, Edwin van der Sar, Clarence Seedorf, Jari Litmanen, Nwankwo Kanu | Ajax side only |

## Finals: roles, nationalities, records

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ucl033 | Name a Brazilian who played in a Champions League final, 2010 onward | en:2010–2026 UEFA Champions League final pages (lineup flagicons) | 40 | modern | Vinícius Júnior, Neymar, Casemiro, Marquinhos, Lucas Beraldo | nationality = flagicon in lineup table; starters + used subs (same for all nationality prompts) |
| ucl034 | Name an English player who played in a Champions League final, 2010 onward | en:2010–2026 UEFA Champions League final pages (lineup flagicons) | 40 | modern | Harry Kane, Bukayo Saka, Jude Bellingham, Declan Rice, Myles Lewis-Skelly | flagicon ENG |
| ucl035 | Name a French player who played in a Champions League final, 2010 onward | en:2010–2026 UEFA Champions League final pages (lineup flagicons) | 40 | modern | Kylian Mbappé, Ousmane Dembélé, Karim Benzema, Raphaël Varane, Senny Mayulu | flagicon FRA |
| ucl036 | Name a German player who played in a Champions League final, 2010 onward | en:2010–2026 UEFA Champions League final pages (lineup flagicons) | 45 | modern | Toni Kroos, Thomas Müller, Kai Havertz, Niclas Füllkrug, Kevin Großkreutz | flagicon GER |
| ucl037 | Name a Spanish player who played in a Champions League final, 2010 onward | en:2010–2026 UEFA Champions League final pages (lineup flagicons) | 40 | modern | Sergio Ramos, Rodri, Andrés Iniesta, Fabián Ruiz, Martín Zubimendi | flagicon ESP |
| ucl038 | Name an African international who played in a Champions League final, 2010 onward | en:2010–2026 UEFA Champions League final pages (lineup flagicons) | 25 | modern | Mohamed Salah, Sadio Mané, Achraf Hakimi, Édouard Mendy, Joël Matip | flagicon of any CAF nation |
| ucl039 | Name a South American (non-Brazilian) who played in a Champions League final, 2010 onward | en:2010–2026 UEFA Champions League final pages (lineup flagicons) | 35 | modern | Lionel Messi, Lautaro Martínez, Federico Valverde, Willian Pacho, Piero Hincapié | flagicon of a CONMEBOL nation other than Brazil |
| ucl040 | Name a country that had a player appear in a Champions League final, 2015 onward | en:2015–2026 UEFA Champions League final pages (lineup flagicons) | 40 | modern | France, Brazil, Croatia, Senegal, Georgia | answers = country / national-team articles; starters + used subs |
| ucl041 | Name a player who came off the bench in a Champions League final, 2015 onward | en:2015–2026 UEFA Champions League final pages (Details) | 65 | modern | Lucas Vázquez, Divock Origi, Gonçalo Ramos, Noni Madueke, Roberto Pereyra | {{subon}} rows only |
| ucl042 | Name a goalkeeper who played in a Champions League final, 2010 onward | en:2010–2026 UEFA Champions League final pages (Details) | 20 | modern | Thibaut Courtois, Alisson Becker, Gianluigi Donnarumma, Matvey Safonov, Roman Weidenfeller | GK rows that started or came on |
| ucl043 | Name a goalkeeper who played in a Champions League final, 1993–2009 | en:1993–2009 UEFA Champions League final pages (Details) | 24 | 2000s+ | Iker Casillas, Gianluigi Buffon, Edwin van der Sar, Jerzy Dudek, Santiago Cañizares | GK rows that started or came on |
| ucl044 | Name a player who captained a side in a Champions League final, 2010 onward | en:2010–2026 UEFA Champions League final pages (Details, (c) marker) | 22 | modern | Sergio Ramos, Jordan Henderson, Marquinhos, Martin Ødegaard, Javier Zanetti | starting captain marked (c) only |
| ucl045 | Name a manager who has managed in a Champions League final, 2015 onward | en:2015–2026 UEFA Champions League final pages (Details, Manager rows) | 13 | modern | Zinedine Zidane, Jürgen Klopp, Pep Guardiola, Edin Terzić, Hansi Flick | both benches |
| ucl046 | Name a manager who managed in a Champions League final, 1993–2014 | en:1993–2014 UEFA Champions League final pages (Details, Manager rows) | 28 | 2000s+ | Alex Ferguson, José Mourinho, Rafael Benítez, Avram Grant, Héctor Cúper | both benches; dedupe |
| ucl047 | Name a player who took a penalty in a Champions League final shoot-out, 2000 onward | en:2001, 2003, 2005, 2008, 2012, 2016, 2026 UEFA Champions League final pages (penalties field) | 65 | 2000s+ | Cristiano Ronaldo, John Terry, Andriy Shevchenko, Bastian Schweinsteiger, Juanfran | scored or missed both count |
| ucl048 | Name an official Player of the Match in a Champions League final (2001 onward) | en:2001–2026 UEFA Champions League final pages (infobox man_of_the_match) | 26 | 2000s+ | Cristiano Ronaldo, Lionel Messi, Didier Drogba, Kingsley Coman, Vitinha | one per final, verified field present 2001–2026 |
| ucl049 | Name a player who scored in a European Cup final, 1956–1992 | en:List of European Cup and UEFA Champions League finals (links to 1956–1992 European Cup final pages for scorers) | 70 | classic | Alfredo Di Stéfano, Ferenc Puskás, Eusébio, Bobby Charlton, Ronald Koeman | complements catalog p037 (1993 onward); own goals excluded |
| ucl050 | Name a captain who lifted the European Cup, 1956–1992 | en:European Cup and UEFA Champions League records and statistics (Players > Captaincy table) | 30 | classic | Franz Beckenbauer, Johan Cruyff, Bobby Charlton, Emlyn Hughes, Dennis Mortimer | rows 1956–1992 of the winning-captains table |
| ucl051 | Name a player who has played in three or more Champions League finals (1993 onward) | en:1993–2026 UEFA Champions League final pages (Details) | 50 | 2000s+ | Cristiano Ronaldo, Luka Modrić, Paolo Maldini, Marquinhos, Edwin van der Sar | starters + used subs; count finals per player, keep ≥3 |

## Winning runs: squads

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ucl052 | Name a player who made a Champions League appearance for Barcelona in 2014–15 | en:2014–15 FC Barcelona season (Statistics > appearances, UCL column) | 24 | modern | Lionel Messi, Neymar, Luis Suárez, Jordi Alba, Munir El Haddadi | ≥1 UCL appearance incl. as sub; same rule for every squad prompt |
| ucl053 | Name a player who made a Champions League appearance for Real Madrid in 2016–17 | en:2016–17 Real Madrid CF season (Statistics) | 25 | modern | Cristiano Ronaldo, Isco, Marco Asensio, Álvaro Morata, Mariano Díaz | ≥1 UCL appearance |
| ucl054 | Name a player who made a Champions League appearance for Liverpool in 2018–19 | en:2018–19 Liverpool F.C. season (Statistics) | 24 | modern | Mohamed Salah, Virgil van Dijk, Divock Origi, Georginio Wijnaldum, Daniel Sturridge | ≥1 UCL appearance |
| ucl055 | Name a player who made a Champions League appearance for Tottenham in 2018–19 | en:2018–19 Tottenham Hotspur F.C. season (Statistics) | 23 | modern | Son Heung-min, Harry Kane, Lucas Moura, Fernando Llorente, Kieran Trippier | ≥1 UCL appearance |
| ucl056 | Name a player who made a Champions League appearance for Bayern Munich in 2019–20 | en:2019–20 FC Bayern Munich season (Statistics) | 23 | modern | Robert Lewandowski, Alphonso Davies, Serge Gnabry, Philippe Coutinho, Ivan Perišić | ≥1 UCL appearance |
| ucl057 | Name a player who made a Champions League appearance for Chelsea in 2020–21 | en:2020–21 Chelsea F.C. season (Statistics) | 26 | modern | Mason Mount, Kai Havertz, N'Golo Kanté, Olivier Giroud, Kurt Zouma | ≥1 UCL appearance |
| ucl058 | Name a player who made a Champions League appearance for Real Madrid in 2021–22 | en:2021–22 Real Madrid CF season (Statistics) | 26 | modern | Karim Benzema, Vinícius Júnior, Luka Modrić, Rodrygo, Eduardo Camavinga | ≥1 UCL appearance |
| ucl059 | Name a player who made a Champions League appearance for Manchester City in 2022–23 | en:2022–23 Manchester City F.C. season (Statistics) | 25 | modern | Erling Haaland, Kevin De Bruyne, Rodri, Riyad Mahrez, Cole Palmer | ≥1 UCL appearance |
| ucl060 | Name a player who made a Champions League appearance for Inter in 2022–23 | en:2022–23 Inter Milan season (Statistics) | 25 | modern | Lautaro Martínez, Romelu Lukaku, André Onana, Edin Džeko, Danilo D'Ambrosio | ≥1 UCL appearance |
| ucl061 | Name a player who made a Champions League appearance for Real Madrid in 2023–24 | en:2023–24 Real Madrid CF season (Statistics) | 25 | modern | Jude Bellingham, Vinícius Júnior, Rodrygo, Joselu, Brahim Díaz | ≥1 UCL appearance |
| ucl062 | Name a player who made a Champions League appearance for Borussia Dortmund in 2023–24 | en:2023–24 Borussia Dortmund season (Statistics) | 26 | modern | Jadon Sancho, Mats Hummels, Niclas Füllkrug, Marco Reus, Youssoufa Moukoko | ≥1 UCL appearance |
| ucl063 | Name a player who made a Champions League appearance for PSG in 2024–25 | en:2024–25 Paris Saint-Germain FC season (Statistics) | 27 | modern | Ousmane Dembélé, Khvicha Kvaratskhelia, Désiré Doué, Gianluigi Donnarumma, Senny Mayulu | ≥1 UCL appearance |
| ucl064 | Name a player who made a Champions League appearance for Barcelona in 2024–25 | en:2024–25 FC Barcelona season (Statistics) | 25 | modern | Lamine Yamal, Raphinha, Robert Lewandowski, Pedri, Pau Cubarsí | ≥1 UCL appearance |
| ucl065 | Name a player who made a Champions League appearance for Inter in 2024–25 | en:2024–25 Inter Milan season (Statistics) | 26 | modern | Lautaro Martínez, Marcus Thuram, Yann Sommer, Francesco Acerbi, Mehdi Taremi | ≥1 UCL appearance |
| ucl066 | Name a player who made a Champions League appearance for Liverpool in 2024–25 | en:2024–25 Liverpool F.C. season (Statistics) | 26 | modern | Mohamed Salah, Virgil van Dijk, Luis Díaz, Caoimhín Kelleher, Jarell Quansah | ≥1 UCL appearance |
| ucl067 | Name a player who made a Champions League appearance for Aston Villa in 2024–25 | en:2024–25 Aston Villa F.C. season (Statistics) | 24 | modern | Ollie Watkins, Emiliano Martínez, Marcus Rashford, Jhon Durán, Jacob Ramsey | ≥1 UCL appearance; January signings count |
| ucl068 | Name a player who made a Champions League appearance for Newcastle United (2023–24 or 2025–26) | en:2023–24 Newcastle United F.C. season; en:2025–26 Newcastle United F.C. season (Statistics) | 35 | modern | Bruno Guimarães, Anthony Gordon, Alexander Isak, Joelinton, Lewis Miley | either season; ≥1 UCL appearance |
| ucl069 | Name a player who made a Champions League appearance for Arsenal in 2025–26 | en:2025–26 Arsenal F.C. season (Statistics) | 26 | modern | Bukayo Saka, Declan Rice, Viktor Gyökeres, Eberechi Eze, Max Dowman | ≥1 UCL appearance |
| ucl070 | Name a player who made a Champions League appearance for Bayern Munich in 2025–26 | en:2025–26 FC Bayern Munich season (Statistics) | 26 | modern | Harry Kane, Michael Olise, Luis Díaz, Jamal Musiala, Lennart Karl | ≥1 UCL appearance |

## Club eras: goalscorers

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ucl071 | Name a player who scored a Champions League goal for Real Madrid during the 2016–2018 three-peat (2015–16 to 2017–18) | en:2015–16, 2016–17, 2017–18 Real Madrid CF season (Statistics > Goalscorers, UCL column) | 25 | modern | Cristiano Ronaldo, Gareth Bale, Karim Benzema, Marco Asensio, Mariano Díaz | ≥1 UCL goal in any listed season; qualifying excluded (same rule for all club-era scorer prompts) |
| ucl072 | Name a player who scored a Champions League goal for Real Madrid, 2021–22 to 2024–25 | en:2021–22 to 2024–25 Real Madrid CF season pages (Goalscorers) | 30 | modern | Vinícius Júnior, Kylian Mbappé, Karim Benzema, Joselu, Lucas Vázquez | ≥1 UCL goal |
| ucl073 | Name a player who scored a Champions League goal for Manchester City, 2016–17 to 2022–23 | en:2016–17 to 2022–23 Manchester City F.C. season pages (Goalscorers) | 45 | modern | Sergio Agüero, Erling Haaland, Raheem Sterling, Phil Foden, Kelechi Iheanacho | 2016 play-off round v Steaua excluded |
| ucl074 | Name a player who scored a Champions League goal for Liverpool, 2017–18 to 2021–22 | en:2017–18 to 2021–22 Liverpool F.C. season pages (Goalscorers) | 33 | modern | Mohamed Salah, Roberto Firmino, Sadio Mané, Divock Origi, Alex Oxlade-Chamberlain | 2017 play-off round v Hoffenheim excluded |
| ucl075 | Name a player who scored a Champions League goal for Arsenal, 2023–24 to 2025–26 | en:2023–24, 2024–25, 2025–26 Arsenal F.C. season pages (Goalscorers) | 28 | modern | Bukayo Saka, Kai Havertz, Gabriel Martinelli, Viktor Gyökeres, Leandro Trossard | ≥1 UCL goal |
| ucl076 | Name a player who scored a Champions League goal for PSG in 2024–25 or 2025–26 | en:2024–25 & 2025–26 Paris Saint-Germain FC season pages (Goalscorers) | 25 | modern | Ousmane Dembélé, Khvicha Kvaratskhelia, Désiré Doué, Achraf Hakimi, Senny Mayulu | ≥1 UCL goal |
| ucl077 | Name a player who scored a Champions League goal for Barcelona in 2024–25 or 2025–26 | en:2024–25 & 2025–26 FC Barcelona season pages (Goalscorers) | 24 | modern | Raphinha, Robert Lewandowski, Lamine Yamal, Fermín López, Ferran Torres | ≥1 UCL goal |
| ucl078 | Name a player who scored a Champions League goal for Bayern Munich, 2019–20 to 2025–26 | en:2019–20 to 2025–26 FC Bayern Munich season pages (Goalscorers) | 40 | modern | Robert Lewandowski, Harry Kane, Jamal Musiala, Eric Maxim Choupo-Moting, Lennart Karl | ≥1 UCL goal |
| ucl079 | Name a player who scored a Champions League goal for Manchester United since 2015–16 | en:2015–16, 2017–18, 2018–19, 2020–21, 2021–22, 2023–24 Manchester United F.C. season pages (Goalscorers) | 35 | modern | Marcus Rashford, Cristiano Ronaldo, Romelu Lukaku, Rasmus Højlund, Anthony Martial | 2015 play-off round v Club Brugge excluded |
| ucl080 | Name a player who scored a Champions League goal for Chelsea, 2015–16 onward | en:Chelsea F.C. season pages 2015–16 to 2022–23 and 2025–26 (Goalscorers) | 40 | modern | Kai Havertz, Olivier Giroud, Eden Hazard, Cole Palmer, Hakim Ziyech | only seasons Chelsea played the UCL |
| ucl081 | Name a player who scored a Champions League goal for Newcastle United (2023–24 or 2025–26) | en:2023–24 & 2025–26 Newcastle United F.C. season pages (Goalscorers) | 18 | modern | Anthony Gordon, Alexander Isak, Bruno Guimarães, Harvey Barnes, Jacob Murphy | ≥1 UCL goal |
| ucl082 | Name a player who scored a Champions League goal for Atlético Madrid, 2015–16 onward | en:2015–16 to 2025–26 Atlético Madrid season pages (Goalscorers) | 45 | modern | Antoine Griezmann, Julián Alvarez, Álvaro Morata, Saúl Ñíguez, Alexander Sørloth | ≥1 UCL goal |
| ucl083 | Name a player who scored a Champions League goal for Juventus, 2015–16 onward | en:2015–16 to 2025–26 Juventus FC season pages (Goalscorers) | 45 | modern | Cristiano Ronaldo, Paulo Dybala, Dušan Vlahović, Álvaro Morata, Weston McKennie | seasons without UCL football skipped |
| ucl084 | Name a player who scored a Champions League goal for Real Madrid, 2009–10 to 2013–14 | en:2009–10 to 2013–14 Real Madrid CF season pages (Goalscorers) | 30 | 2000s+ | Cristiano Ronaldo, Karim Benzema, Gonzalo Higuaín, Mesut Özil, José Callejón | ≥1 UCL goal |
| ucl085 | Name a player who scored a Champions League goal for Arsenal, 2003–04 to 2009–10 | en:2003–04 to 2009–10 Arsenal F.C. season pages (Goalscorers) | 35 | 2000s+ | Thierry Henry, Robin van Persie, Cesc Fàbregas, Emmanuel Adebayor, Nicklas Bendtner | qualifying excluded |
| ucl086 | Name a player who scored a Champions League goal for Barcelona, 2005–06 to 2010–11 | en:2005–06 to 2010–11 FC Barcelona season pages (Goalscorers) | 35 | 2000s+ | Lionel Messi, Samuel Eto'o, Ronaldinho, Thierry Henry, Bojan | ≥1 UCL goal |
| ucl087 | Name a player who scored a Champions League goal for Chelsea, 2003–04 to 2011–12 | en:2003–04 to 2011–12 Chelsea F.C. season pages (Goalscorers) | 40 | 2000s+ | Didier Drogba, Frank Lampard, Michael Ballack, Juan Mata, Salomon Kalou | qualifying excluded |

## Knockout goalscorers by season

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ucl088 | Name a player who scored in the 2015–16 Champions League knockout phase | en:2015–16 UEFA Champions League knockout phase (Round of 16, Quarter-finals, Semi-finals match boxes) | 45 | modern | Cristiano Ronaldo, Antoine Griezmann, Thomas Müller, Kevin De Bruyne, Saúl Ñíguez | goals1/goals2 fields R16–SF; final excluded; own goals excluded (same rule for each season prompt) |
| ucl089 | Name a player who scored in the 2016–17 Champions League knockout phase | en:2016–17 UEFA Champions League knockout phase | 59 | modern | Cristiano Ronaldo, Kylian Mbappé, Sergi Roberto, Leroy Sané, Tiémoué Bakayoko | R16–SF |
| ucl090 | Name a player who scored in the 2017–18 Champions League knockout phase | en:2017–18 UEFA Champions League knockout phase | 52 | modern | Mohamed Salah, Cristiano Ronaldo, Edin Džeko, Kostas Manolas, Alex Oxlade-Chamberlain | R16–SF |
| ucl091 | Name a player who scored in the 2018–19 Champions League knockout phase | en:2018–19 UEFA Champions League knockout phase | 50 | modern | Lionel Messi, Divock Origi, Lucas Moura, Matthijs de Ligt, Fernando Llorente | R16–SF; page uses different box markup, check scraper |
| ucl092 | Name a player who scored in the 2019–20 Champions League knockout phase | en:2019–20 UEFA Champions League knockout phase | 49 | modern | Robert Lewandowski, Serge Gnabry, Josip Iličić, Mario Pašalić, Tyler Adams | R16–SF incl. single-leg Lisbon ties |
| ucl093 | Name a player who scored in the 2020–21 Champions League knockout phase | en:2020–21 UEFA Champions League knockout phase | 45 | modern | Kylian Mbappé, Erling Haaland, Riyad Mahrez, Mason Mount, Hakim Ziyech | R16–SF |
| ucl094 | Name a player who scored in the 2021–22 Champions League knockout phase | en:2021–22 UEFA Champions League knockout phase | 48 | modern | Karim Benzema, Rodrygo, Riyad Mahrez, Arnaut Danjuma, Francis Coquelin | R16–SF |
| ucl095 | Name a player who scored in the 2022–23 Champions League knockout phase | en:2022–23 UEFA Champions League knockout phase | 43 | modern | Erling Haaland, Bernardo Silva, Vinícius Júnior, Ismaël Bennacer, Edin Džeko | R16–SF |
| ucl096 | Name a player who scored in the 2023–24 Champions League knockout phase | en:2023–24 UEFA Champions League knockout phase | 55 | modern | Vinícius Júnior, Harry Kane, Joselu, Mats Hummels, Galeno | R16–SF |
| ucl097 | Name a player who scored in the 2024–25 Champions League round of 16, quarter-finals or semi-finals | en:2024–25 UEFA Champions League knockout phase (Round of 16 to Semi-finals) | 62 | modern | Ousmane Dembélé, Raphinha, Lautaro Martínez, Francesco Acerbi, Harvey Elliott | play-offs excluded (own prompt) |
| ucl098 | Name a player who scored in the 2025–26 Champions League round of 16, quarter-finals or semi-finals | en:2025–26 UEFA Champions League knockout phase (Round of 16 to Semi-finals) | 64 | modern | Harry Kane, Lamine Yamal, Julián Alvarez, Lennart Karl, Ole Didrik Blomberg | play-offs excluded (own prompt) |
| ucl099 | Name a player who scored in the 2024–25 knockout phase play-offs | en:2024–25 UEFA Champions League knockout phase (Knockout phase play-offs) | 41 | modern | Kylian Mbappé, Erling Haaland, Serhou Guirassy, Vangelis Pavlidis, Chemsdine Talbi | 16 matches; incl. Man City v Real Madrid, Celtic v Bayern |
| ucl100 | Name a player who scored in the 2025–26 knockout phase play-offs | en:2025–26 UEFA Champions League knockout phase (Knockout phase play-offs) | 50 | modern | Vinícius Júnior, Victor Osimhen, Anthony Gordon, Jens Petter Hauge, Elvin Cafarguliyev | 16 matches; incl. Qarabağ v Newcastle, Bodø/Glimt v Inter |
| ucl101 | Name a player who scored in a Champions League semi-final, 2015–16 to 2025–26 | en:2015–16 to 2025–26 UEFA Champions League knockout phase pages (Semi-finals) | 80 | modern | Cristiano Ronaldo, Mohamed Salah, Lucas Moura, Joselu, Viktor Gyökeres | semi-final legs only |
| ucl102 | Name a player who scored in a Champions League quarter-final, 2020–21 to 2025–26 | en:2020–21 to 2025–26 UEFA Champions League knockout phase pages (Quarter-finals) | 85 | modern | Kevin De Bruyne, Vinícius Júnior, Arda Güler, Ademola Lookman, Aleksandar Pavlović | quarter-final legs only |
| ucl103 | Name a player who scored in a Champions League semi-final, 2004–05 to 2014–15 | en:2004–05 to 2007–08 UEFA Champions League knockout stage; 2008–09 to 2014–15 UEFA Champions League knockout phase (Semi-finals) | 80 | 2000s+ | Lionel Messi, Luis García, Andrés Iniesta, Park Ji-sung, Robert Lewandowski | semi-final legs only; page titles switch from 'stage' to 'phase' in 2008–09 |

## Knockout goalscorers by club

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ucl104 | Name a player who has scored against Real Madrid in a Champions League knockout tie since 2015–16 | en:2015–16 to 2025–26 UEFA Champions League knockout phase pages | 26 | modern | Kevin De Bruyne, Mohamed Salah, Leroy Sané, Riyad Mahrez, Julián Alvarez | goals by the team facing Real Madrid, R16–SF (play-offs included); finals excluded |
| ucl105 | Name a player who has scored against Barcelona in a Champions League knockout tie since 2015–16 | en:2015–16 to 2025–26 UEFA Champions League knockout phase pages | 26 | modern | Divock Origi, Thomas Müller, Edin Džeko, Kostas Manolas, Philippe Coutinho | as above; Coutinho scored for Bayern in the 8–2 |
| ucl106 | Name a player who has scored against Bayern Munich in a Champions League knockout tie since 2015–16 | en:2015–16 to 2025–26 UEFA Champions League knockout phase pages | 29 | modern | Cristiano Ronaldo, Kylian Mbappé, Vinícius Júnior, Joselu, Marquinhos | as above |
| ucl107 | Name a player who has scored against Manchester City in a Champions League knockout tie since 2016–17 | en:2016–17 to 2025–26 UEFA Champions League knockout phase pages | 24 | modern | Kylian Mbappé, Mohamed Salah, Karim Benzema, Rodrygo, Moussa Dembélé | as above; Dembélé = Lyon 2020 |
| ucl108 | Name a player who has scored against Paris Saint-Germain in a Champions League knockout tie since 2015–16 | en:2015–16 to 2025–26 UEFA Champions League knockout phase pages | 30 | modern | Neymar, Sergi Roberto, Marcus Rashford, Riyad Mahrez, Harvey Elliott | as above; Neymar for Barcelona 2017 |
| ucl109 | Name a player who has scored against Arsenal in a Champions League knockout tie since 2015–16 | en:2015–16 to 2025–26 UEFA Champions League knockout phase pages | 25 | modern | Lionel Messi, Robert Lewandowski, Arjen Robben, Ousmane Dembélé, Galeno | goals by Arsenal's opponents, R16–SF; finals excluded |
| ucl110 | Name a player who scored for an Italian club in a Champions League knockout tie since 2015–16 | en:2015–16 to 2025–26 UEFA Champions League knockout phase pages | 67 | modern | Lautaro Martínez, Cristiano Ronaldo, Paulo Dybala, Josip Iličić, Davide Zappacosta | club association = fbaicon ITA in the match box |
| ucl111 | Name a player who scored for a German club in a Champions League knockout tie since 2015–16 | en:2015–16 to 2025–26 UEFA Champions League knockout phase pages | 72 | modern | Robert Lewandowski, Harry Kane, Erling Haaland, Niclas Füllkrug, Tyler Adams | club association = fbaicon GER |

## League phase goalscorers

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ucl112 | Name a player who scored for an English club in the 2025–26 league phase | en:2025–26 UEFA Champions League league phase (Matches) | 59 | modern | Erling Haaland, Bukayo Saka, Mohamed Salah, Anthony Gordon, Nico O'Reilly | goals1/goals2 for the side with fbaicon ENG; own goals excluded (same rule for all league-phase scorer prompts) |
| ucl113 | Name a player who scored for a Spanish club in the 2025–26 league phase | en:2025–26 UEFA Champions League league phase (Matches) | 35 | modern | Kylian Mbappé, Lamine Yamal, Julián Alvarez, Ferran Torres, Oihan Sancet | fbaicon ESP |
| ucl114 | Name a player who scored for a German club in the 2025–26 league phase | en:2025–26 UEFA Champions League league phase (Matches) | 34 | modern | Harry Kane, Serhou Guirassy, Michael Olise, Patrik Schick, Jonathan Burkardt | fbaicon GER |
| ucl115 | Name a player who scored for an Italian club in the 2025–26 league phase | en:2025–26 UEFA Champions League league phase (Matches) | 30 | modern | Lautaro Martínez, Dušan Vlahović, Scott McTominay, Ademola Lookman, Pio Esposito | fbaicon ITA |
| ucl116 | Name a player who scored for a club outside the big five leagues in the 2025–26 league phase | en:2025–26 UEFA Champions League league phase (Matches) | 92 | modern | Victor Osimhen, Vangelis Pavlidis, Jens Petter Hauge, Promise David, Dastan Satpayev | any side not ENG/ESP/GER/ITA/FRA; large list, near the upper bound |
| ucl117 | Name a player who scored for an English club in the 2024–25 league phase | en:2024–25 UEFA Champions League league phase (Matches) | 37 | modern | Mohamed Salah, Erling Haaland, Bukayo Saka, Ollie Watkins, Jhon Durán | fbaicon ENG |
| ucl118 | Name a player who scored for a German club in the 2024–25 league phase | en:2024–25 UEFA Champions League league phase (Matches) | 41 | modern | Harry Kane, Serhou Guirassy, Florian Wirtz, Benjamin Šeško, Ermedin Demirović | fbaicon GER |
| ucl119 | Name a player who scored for a French club in the 2024–25 league phase | en:2024–25 UEFA Champions League league phase (Matches) | 36 | modern | Ousmane Dembélé, Jonathan David, Bradley Barcola, Takumi Minamino, Soungoutou Magassa | fbaicon FRA (PSG, Monaco, Lille, Brest) |
| ucl120 | Name a player who scored for a Spanish club in the 2024–25 league phase | en:2024–25 UEFA Champions League league phase (Matches) | 29 | modern | Kylian Mbappé, Raphinha, Lamine Yamal, Antoine Griezmann, Miguel Gutiérrez | fbaicon ESP (Real Madrid, Barcelona, Atlético, Girona) |
| ucl121 | Name a player who scored for a Dutch or Portuguese club in the 2024–25 league phase | en:2024–25 UEFA Champions League league phase (Matches) | 33 | modern | Viktor Gyökeres, Ángel Di María, Luuk de Jong, Santiago Giménez, Ayase Ueda | fbaicon NED or POR (PSV, Feyenoord, Sporting, Benfica) |
| ucl122 | Name a player who scored for a French or Portuguese club in the 2025–26 league phase | en:2025–26 UEFA Champions League league phase (Matches) | 34 | modern | Ousmane Dembélé, Khvicha Kvaratskhelia, Mason Greenwood, Pierre-Emerick Aubameyang, Anatoliy Trubin | fbaicon FRA or POR; Trubin = Benfica goalkeeper's goal v Real Madrid; exclude own goals |
| ucl123 | Name a player who scored for an English club in the 2023–24 group stage | en:2023–24 UEFA Champions League group stage (Matches) | 30 | modern | Erling Haaland, Bukayo Saka, Rasmus Højlund, Alexander Isak, Micah Hamilton | Arsenal, Man City, Man United, Newcastle |

## Hat-tricks

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ucl124 | Name a player who has scored a Champions League hat-trick since 2015–16 | en:List of UEFA Champions League hat-tricks (Hat-tricks table) | 50 | modern | Cristiano Ronaldo, Kylian Mbappé, Erling Haaland, Josip Iličić, Mislav Oršić | rows dated 2015-07-01 onward; qualifying excluded by the list |
| ucl125 | Name a player who has scored a Champions League hat-trick in the league-phase era (2024–25 onward) | en:List of UEFA Champions League hat-tricks | 17 | modern | Harry Kane, Raphinha, Vinícius Júnior, Serhou Guirassy, Vangelis Pavlidis | rows dated 2024-07-01 onward; grows during 2026–27 |
| ucl126 | Name a player who has scored four or more goals in a Champions League match | en:List of UEFA Champions League hat-tricks (rows marked 4/5) | 18 | 2000s+ | Lionel Messi, Robert Lewandowski, Erling Haaland, Anthony Gordon, Bafétimbi Gomis | superscript 4 or 5 in the table |
| ucl127 | Name a player who has scored a Champions League hat-trick for an English club | en:List of UEFA Champions League hat-tricks | 27 | 2000s+ | Wayne Rooney, Erling Haaland, Raheem Sterling, Lucas Moura, Anthony Gordon | 'For' column club with fbaicon ENG |
| ucl128 | Name a player who has scored a Champions League hat-trick for a Spanish club | en:List of UEFA Champions League hat-tricks | 23 | 2000s+ | Cristiano Ronaldo, Lionel Messi, Karim Benzema, Alexander Sørloth, Fermín López | 'For' column club with fbaicon ESP |
| ucl129 | Name a player who has scored a Champions League hat-trick for a club outside the big five leagues | en:List of UEFA Champions League hat-tricks | 25 | 2000s+ | Luiz Adriano, Mislav Oršić, Vangelis Pavlidis, Evanilson, Dado Pršo | 'For' club not ENG/ESP/GER/ITA/FRA |
| ucl130 | Name a non-European player who has scored a Champions League hat-trick | en:List of UEFA Champions League hat-tricks | 34 | 2000s+ | Lionel Messi, Neymar, Vinícius Júnior, Victor Osimhen, Serhou Guirassy | player flagicon outside UEFA |
| ucl131 | Name a player who scored a Champions League hat-trick between 1992–93 and 2014–15 | en:List of UEFA Champions League hat-tricks | 70 | 2000s+ | Andriy Shevchenko, Filippo Inzaghi, Bafétimbi Gomis, Juul Ellerman, Bernd Hobsch | rows dated before 2015-07-01 |
| ucl132 | Name a country whose player has scored a Champions League hat-trick | en:List of UEFA Champions League hat-tricks (Hat-tricks by nationality table) | 38 | 2000s+ | Brazil, France, England, Bosnia and Herzegovina, Guinea | answers = country / national-team articles |

## Players: awards and records

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ucl133 | Name a player named in a Champions League Squad of the Season, 2015–16 to 2020–21 | en:2015–16 to 2020–21 UEFA Champions League season pages (Statistics > Squad of the season) | 75 | modern | Cristiano Ronaldo, Lionel Messi, Kevin De Bruyne, Alphonso Davies, Jan Oblak | union of the six squads |
| ucl134 | Name a player named in a Champions League Team of the Season, 2021–22 to 2025–26 | en:2021–22 to 2025–26 UEFA Champions League season pages (Statistics > Team of the Season) | 42 | modern | Vinícius Júnior, Rodri, Lamine Yamal, Achraf Hakimi, Nuno Mendes | union of the five XIs |
| ucl135 | Name a goalkeeper named in a Champions League Squad or Team of the Season, 2015–16 onward | en:2015–16 to 2025–26 UEFA Champions League season pages (Squad/Team of the Season, GK rows) | 14 | modern | Thibaut Courtois, Manuel Neuer, Gianluigi Donnarumma, Keylor Navas, Édouard Mendy | GK rows only; small list |
| ucl136 | Name a country with a player named in a Champions League Team of the Season, 2021–22 to 2025–26 | en:2021–22 to 2025–26 UEFA Champions League season pages (Team of the Season flagicons) | 18 | modern | Brazil, France, England, Morocco, Georgia | answers = country articles |
| ucl137 | Name a country with a player named in a Champions League Squad of the Season, 2015–16 to 2020–21 | en:2015–16 to 2020–21 UEFA Champions League season pages (Squad of the season flagicons) | 25 | modern | Spain, Brazil, Belgium, Canada, Costa Rica | answers = country articles |
| ucl138 | Name a player who appears in a season's top goalscorers table, 2015–16 to 2025–26 | en:2015–16 to 2025–26 UEFA Champions League season pages (Statistics > Top goalscorers) | 65 | modern | Cristiano Ronaldo, Erling Haaland, Robert Lewandowski, Sébastien Haller, Serhou Guirassy | union of the season tables (each lists ~10 incl. ties); qualifying goals excluded |
| ucl139 | Name a player who has made 100 or more Champions League appearances | en:List of footballers with 100 or more UEFA Champions League appearances | 57 | 2000s+ | Cristiano Ronaldo, Lionel Messi, Iker Casillas, Thomas Müller, Marquinhos | list table; updates as active players pass 100 |
| ucl140 | Name a player who has won the European Cup / Champions League four or more times | en:European Cup and UEFA Champions League records and statistics (Players > Most wins table) | 34 | 2000s+ | Cristiano Ronaldo, Luka Modrić, Toni Kroos, Nacho, Juan Santisteban | rows with 4, 5 or 6 wins |
| ucl141 | Name a player who took a penalty in a Champions League knockout shoot-out since 2015–16 | en:2015–16, 2023–24, 2024–25 UEFA Champions League knockout phase pages + 2016 & 2026 UEFA Champions League final (penalties fields) | 70 | modern | Cristiano Ronaldo, Bernardo Silva, Darwin Núñez, Antonio Rüdiger, Juanfran | 8 shoot-outs per records page list; scored or missed both count |

## Clubs: seasons

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ucl142 | Name a club that played in the 2015–16 Champions League group stage | en:2015–16 UEFA Champions League group stage (Teams) | 32 | modern | Real Madrid, Wolfsburg, Gent, Astana, Maccabi Tel Aviv | 32 group-stage teams |
| ucl143 | Name a club that played in the 2016–17 Champions League group stage | en:2016–17 UEFA Champions League group stage (Teams) | 32 | modern | Barcelona, Leicester City, Ludogorets Razgrad, Rostov, Legia Warsaw | 32 group-stage teams (same rule for all season prompts) |
| ucl144 | Name a club that played in the 2017–18 Champions League group stage | en:2017–18 UEFA Champions League group stage (Teams) | 32 | modern | Real Madrid, RB Leipzig, Qarabağ, Maribor, APOEL |  |
| ucl145 | Name a club that played in the 2019–20 Champions League group stage | en:2019–20 UEFA Champions League group stage (Teams) | 32 | modern | Liverpool, Atalanta, Red Bull Salzburg, Genk, Slavia Prague |  |
| ucl146 | Name a club that played in the 2022–23 Champions League group stage | en:2022–23 UEFA Champions League group stage (Teams) | 32 | modern | Napoli, Eintracht Frankfurt, Celtic, Viktoria Plzeň, Maccabi Haifa |  |
| ucl147 | Name a club that played in the 2024–25 Champions League league phase | en:2024–25 UEFA Champions League league phase (Teams and seeding) | 36 | modern | Aston Villa, Brest, Girona, Sturm Graz, Slovan Bratislava | 36 teams |
| ucl148 | Name a club that played in the 2025–26 Champions League league phase | en:2025–26 UEFA Champions League league phase (Teams and seeding) | 36 | modern | Newcastle United, Union Saint-Gilloise, Bodø/Glimt, Pafos, Kairat | 36 teams |
| ucl149 | Name a club in the 2026–27 Champions League league phase | en:2026–27 UEFA Champions League league phase (Teams and seeding) | 36 | modern | Manchester United, Como, Real Betis, Viking, Sabah | current season; 36 teams fixed since the August draw |
| ucl150 | Name a club that played in the 2004–05 Champions League group stage | en:2004–05 UEFA Champions League group stage (Teams) | 32 | 2000s+ | Chelsea, Monaco, Deportivo de La Coruña, Panathinaikos, Maccabi Tel Aviv |  |
| ucl151 | Name a club that played in the 2009–10 Champions League group stage | en:2009–10 UEFA Champions League group stage (Teams) | 32 | 2000s+ | Inter Milan, Bordeaux, Unirea Urziceni, Debrecen, AZ |  |

## Clubs: how far they went

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ucl152 | Name a club that reached the Champions League quarter-finals, 2015–16 to 2025–26 | en:2015–16 to 2025–26 UEFA Champions League knockout phase pages (Quarter-finals) | 32 | modern | Real Madrid, Ajax, Monaco, Atalanta, Sporting CP | quarter-final participants, dedupe |
| ucl153 | Name a club that reached the Champions League semi-finals, 2012–13 onward | en:2012–13 to 2025–26 UEFA Champions League knockout phase pages (Semi-finals) | 19 | modern | Real Madrid, Liverpool, Ajax, Roma, RB Leipzig | semi-final participants |
| ucl154 | Name a club that reached the Champions League round of 16, 2015–16 onward | en:2015–16 to 2025–26 UEFA Champions League knockout phase pages (Round of 16) | 60 | modern | Chelsea, Porto, Club Brugge, Gent, Red Bull Salzburg | R16 participants; play-off losers excluded |
| ucl155 | Name a club that played in the 2024–25 or 2025–26 knockout phase (play-offs included) | en:2024–25 & 2025–26 UEFA Champions League knockout phase (Qualified teams) | 32 | modern | Arsenal, Bayern Munich, Feyenoord, Club Brugge, Bodø/Glimt | top 24 of each league phase |
| ucl156 | Name a club that finished in the league-phase top eight (2024–25 or 2025–26) | en:2024–25 & 2025–26 UEFA Champions League league phase (League phase table) | 13 | modern | Liverpool, Barcelona, Arsenal, Lille, Aston Villa | positions 1–8, straight to round of 16 |
| ucl157 | Name a club that finished 9th–24th in a league phase (2024–25 or 2025–26) | en:2024–25 & 2025–26 UEFA Champions League league phase (League phase table) | 28 | modern | Real Madrid, Manchester City, PSG, Club Brugge, Qarabağ | positions 9–24 in either season |
| ucl158 | Name a club eliminated in a league phase, finishing 25th–36th (2024–25 or 2025–26) | en:2024–25 & 2025–26 UEFA Champions League league phase (League phase table) | 22 | modern | RB Leipzig, Girona, Bologna, Dinamo Zagreb, Slovan Bratislava | positions 25–36 in either season |
| ucl159 | Name a club involved in a league-phase match decided by four or more goals (2024–25 or 2025–26) | en:2024–25 & 2025–26 UEFA Champions League league phase (Matches) | 30 | modern | Bayern Munich, PSG, Liverpool, Young Boys, Dinamo Zagreb | winner or loser of any match with margin ≥4 |
| ucl160 | Name a club that topped its Champions League group, 2015–16 to 2023–24 | en:2015–16 to 2023–24 UEFA Champions League group stage pages (group tables) | 32 | modern | Bayern Munich, Liverpool, Monaco, Lille, Real Sociedad | 1st place in a group table |
| ucl161 | Name a club that finished bottom of its Champions League group, 2015–16 to 2023–24 | en:2015–16 to 2023–24 UEFA Champions League group stage pages (group tables) | 55 | modern | Manchester United, Newcastle United, Sevilla, Maccabi Tel Aviv, BATE Borisov | 4th place in a group table |
| ucl162 | Name a club that made its Champions League group/league-phase debut in 2015–16 or later | en:UEFA Champions League clubs performance comparison (first participation column) | 30 | modern | Leicester City, RB Leipzig, Atalanta, Girona, Kairat | first non-qualifying participation ≥ 2015–16 |
| ucl163 | Name a club that won a Champions League play-off round tie, 2021–22 to 2026–27 | en:2021–22 to 2026–27 UEFA Champions League qualifying (Play-off round) | 26 | modern | Benfica, Sheriff Tiraspol, Bodø/Glimt, Pafos, Kairat | titles redirect from '... qualifying phase and play-off round'; both paths |
| ucl164 | Name a club that knocked an English club out of the Champions League knockout phase, 2015–16 onward | en:2015–16 to 2025–26 UEFA Champions League knockout phase pages | 25 | modern | Real Madrid, PSG, Monaco, Sevilla, Porto | tie winner v English club; finals excluded; all-English ties excluded |
| ucl165 | Name a club Bayern Munich have faced in a Champions League knockout tie, 2015–16 onward | en:2015–16 to 2025–26 UEFA Champions League knockout phase pages | 20 | modern | Real Madrid, PSG, Arsenal, Lazio, Beşiktaş | play-offs to SF; finals excluded |
| ucl166 | Name a club Real Madrid have faced in a Champions League knockout tie, 2015–16 onward | en:2015–16 to 2025–26 UEFA Champions League knockout phase pages | 16 | modern | Manchester City, Bayern Munich, Wolfsburg, Atalanta, RB Leipzig | play-offs to SF; finals excluded |
| ucl167 | Name a club Manchester City have faced in the Champions League (2011–12 onward) | en:Manchester City F.C. in international football (UEFA and FIFA competitions match lists) | 50 | modern | Real Madrid, Bayern Munich, Monaco, Feyenoord, Viktoria Plzeň | UCL matches only, qualifying excluded |
| ucl168 | Name a club Arsenal have faced in the Champions League (1998–99 onward) | en:Arsenal F.C. in European football (List of matches) | 70 | 2000s+ | Barcelona, Bayern Munich, PSV Eindhoven, Olympiacos, Lens | rows with competition = Champions League; qualifying rounds excluded |
| ucl169 | Name a club Liverpool have faced in the Champions League (2001–02 onward) | en:List of Liverpool F.C. matches in international competitions | 60 | 2000s+ | Real Madrid, AC Milan, Chelsea, Ludogorets Razgrad, Debrecen | UCL rows only; qualifying excluded |
| ucl170 | Name a club Manchester United have faced in the Champions League under Alex Ferguson (1993–2013) | en:Manchester United F.C. in international football | 65 | 2000s+ | Barcelona, Bayern Munich, Porto, Oțelul Galați, Kispest Honvéd | UCL matches 1993–94 to 2012–13; qualifying excluded |
| ucl171 | Name a club Chelsea have faced in the Champions League (1999–2000 onward) | en:Chelsea F.C. in international football | 65 | 2000s+ | Barcelona, Liverpool, Atlético Madrid, Krasnodar, Hertha BSC | UCL matches; qualifying excluded |
| ucl172 | Name a club with ten or more Champions League group/league-phase participations | en:UEFA Champions League clubs performance comparison | 40 | 2000s+ | Real Madrid, Porto, Olympiacos, Rosenborg, Club Brugge | participation count in the club column ≥10 |
| ucl173 | Name a club that lost all six of its Champions League group matches | en:European Cup and UEFA Champions League records and statistics (Specific group stage records > Six losses) | 22 | 2000s+ | Marseille, Benfica, Villarreal, Košice, Oțelul Galați | 22 clubs, 1991–2023; Dinamo Zagreb twice |
| ucl174 | Name a club that reached the Champions League semi-finals, 1992–93 to 2011–12 | en:UEFA Champions League clubs performance comparison (SF/F/C cells) | 30 | 2000s+ | Manchester United, Monaco, Deportivo de La Coruña, Schalke 04, Panathinaikos | SF, runner-up or champion cells in those seasons |
| ucl175 | Name a club that reached the Champions League quarter-finals, 2000–01 to 2014–15 | en:UEFA Champions League clubs performance comparison (QF or better cells) | 45 | 2000s+ | Arsenal, Leeds United, Lyon, APOEL, Galatasaray | QF, SF, F or C cells in those seasons |
| ucl176 | Name a club that reached the Champions League round of 16, 2003–04 to 2014–15 | en:UEFA Champions League clubs performance comparison (R16 or better cells) | 65 | 2000s+ | Chelsea, Celtic, Lokomotiv Moscow, Rangers, Copenhagen | R16 or better in those seasons |
| ucl177 | Name a club that has won a Champions League penalty shoot-out (1992–93 onward) | en:European Cup and UEFA Champions League records and statistics (Deciding drawn ties > Penalty shoot-out) | 20 | 2000s+ | Real Madrid, Liverpool, Atlético Madrid, APOEL, Fenerbahçe | winners of listed shoot-outs from 1992–93; finals included |

## Clubs by country (1992 onward)

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ucl178 | Name a Spanish club that has played in the Champions League group stage or league phase | en:UEFA Champions League clubs performance comparison (Spain block) | 14 | 2000s+ | Real Madrid, Villarreal, Málaga, Celta Vigo, Mallorca | 1992–93 onward; qualifying-only clubs excluded (same for all country prompts) |
| ucl179 | Name a German club that has played in the Champions League group stage or league phase | en:UEFA Champions League clubs performance comparison (Germany block) | 15 | 2000s+ | Bayern Munich, RB Leipzig, Union Berlin, Hertha BSC, 1. FC Kaiserslautern |  |
| ucl180 | Name an Italian club that has played in the Champions League group stage or league phase | en:UEFA Champions League clubs performance comparison (Italy block) | 12 | 2000s+ | Juventus, Atalanta, Bologna, Como, Udinese | Como debuts in 2026–27 |
| ucl181 | Name a French club that has played in the Champions League group stage or league phase | en:UEFA Champions League clubs performance comparison (France block) | 12 | 2000s+ | Paris Saint-Germain, Lille, Brest, Montpellier, Auxerre |  |
| ucl182 | Name a Portuguese, Dutch or Belgian club that has played in the Champions League group stage or league phase | en:UEFA Champions League clubs performance comparison (Portugal, Netherlands, Belgium blocks) | 20 | 2000s+ | Benfica, Ajax, Club Brugge, Union Saint-Gilloise, Willem II |  |
| ucl183 | Name a Russian, Ukrainian, Turkish or Greek club that has played in the Champions League group stage or league phase | en:UEFA Champions League clubs performance comparison | 18 | 2000s+ | Galatasaray, Shakhtar Donetsk, Zenit Saint Petersburg, Rubin Kazan, Bursaspor |  |
| ucl184 | Name a club from Scandinavia, Finland, Switzerland, Austria or Scotland that has played in the Champions League group stage or league phase | en:UEFA Champions League clubs performance comparison | 29 | 2000s+ | Celtic, Red Bull Salzburg, Bodø/Glimt, Basel, HJK |  |
| ucl185 | Name a club from Central or Eastern Europe, the Balkans, Cyprus, Israel or the Caucasus that has played in the Champions League group stage or league phase | en:UEFA Champions League clubs performance comparison | 38 | 2000s+ | Red Star Belgrade, Dinamo Zagreb, Sheriff Tiraspol, Ferencváros, Artmedia Petržalka | CZE, SVK, HUN, POL, SVN, ROU, CRO, SRB, BUL, BLR, AZE, KAZ, MDA, CYP, ISR blocks |

## Countries

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ucl186 | Name a country whose club has played in the Champions League group stage or league phase | en:UEFA Champions League clubs performance comparison (country blocks) | 34 | 2000s+ | England, Spain, Kazakhstan, Moldova, Finland | answers = country articles (or association article per scraper convention) |
| ucl187 | Name a country with a club in a Champions League league phase (2024–25 to 2026–27) | en:2024–25, 2025–26, 2026–27 UEFA Champions League league phase (Teams and seeding) | 21 | modern | England, Norway, Cyprus, Kazakhstan, Azerbaijan | union of association flags |
| ucl188 | Name a country with a club that played in the Champions League knockout phase, 2015–16 onward | en:2015–16 to 2025–26 UEFA Champions League knockout phase pages | 18 | modern | England, Spain, Norway, Azerbaijan, Denmark | includes play-off round of 2024–25/2025–26 |
| ucl189 | Name a country that has produced a European Cup / Champions League-winning manager | en:List of European Cup and UEFA Champions League winning managers (By nationality) | 15 | classic | Italy, Spain, Germany, Netherlands, Romania | answers = country articles |

## Stadiums and cities

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ucl190 | Name a stadium that hosted a 2024–25 Champions League league-phase match | en:2024–25 UEFA Champions League league phase (Matches, stadium field) | 35 | modern | Anfield, Allianz Arena, Villa Park, Stade de Roudourou, Tehelné pole | Brest played at Guingamp's Roudourou; Sturm Graz at Klagenfurt |
| ucl191 | Name a stadium that hosted a 2025–26 Champions League league-phase match | en:2025–26 UEFA Champions League league phase (Matches, stadium field) | 38 | modern | Emirates Stadium, St James' Park, Aspmyra Stadion, Almaty Central Stadium, Alphamega Stadium | Barcelona used both Montjuïc and the new Camp Nou |
| ucl192 | Name a stadium that hosted a 2023–24 Champions League group-stage match | en:2023–24 UEFA Champions League group stage (Matches, stadium field) | 32 | modern | Old Trafford, Westfalenstadion, Anoeta Stadium, Volksparkstadion, Bosuilstadion | Union Berlin used the Olympiastadion; Shakhtar played in Hamburg |
| ucl193 | Name a stadium that hosted a Champions League semi-final, 2015–16 onward | en:2015–16 to 2025–26 UEFA Champions League knockout phase pages (Semi-finals stadium field) | 22 | modern | Anfield, Santiago Bernabéu, Johan Cruyff Arena, Estádio José Alvalade, Estadi Olímpic Lluís Companys | 2020 single-leg semis in Lisbon included |
| ucl194 | Name a stadium that hosted a Champions League semi-final, 2000–01 to 2014–15 | en:2000–01 to 2007–08 knockout stage + 2008–09 to 2014–15 knockout phase pages (Semi-finals) | 30 | 2000s+ | Old Trafford, San Siro, Stamford Bridge, Riazor, BayArena | stadium field of semi-final legs |
| ucl195 | Name a stadium hosting a 2026–27 Champions League league-phase match | en:2026–27 UEFA Champions League league phase (Matches, stadium field) | 36 | modern | Old Trafford, Villa Park, Stadio Giuseppe Sinigaglia, Viking Stadion, Raiffeisen Arena (Linz) | current season: venues listed for all scheduled fixtures; re-scrape after matchday 8 in case of relocations |
| ucl196 | Name a city that hosted a Champions League knockout match, 2020–21 onward | en:2020–21 to 2025–26 UEFA Champions League knockout phase pages (stadium field city links) | 39 | modern | Madrid, Manchester, Budapest, Bodø, Bruges | 2021 COVID neutral venues (e.g. Budapest, Bucharest) count |
| ucl197 | Name a city with a club in the 2026–27 Champions League league phase | en:2026–27 UEFA Champions League league phase (Matches, stadium field city links) | 32 | modern | London, Madrid, Como, Stavanger, Linz | home-match city; Shakhtar's relocated home city counts as listed |

## Managers

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ucl198 | Name a manager who coached a club in the 2025–26 Champions League league phase | en:2025–26 UEFA Champions League league phase (Teams and seeding) + each linked 2025–26 club season page (infobox manager / head coach) | 42 | modern | Mikel Arteta, Luis Enrique, Xabi Alonso, Eddie Howe, Kjetil Knutsen | incl. mid-season replacements who managed a UCL match; scrape the 36 club season pages |
| ucl199 | Name a manager whose club reached the Champions League quarter-finals, 2020–21 onward | en:2020–21 to 2025–26 UEFA Champions League knockout phase pages (Quarter-finals) + quarter-finalists' club season pages (infobox manager) | 30 | modern | Carlo Ancelotti, Pep Guardiola, Mikel Arteta, Unai Emery, Rui Borges | manager in charge at the quarter-final |
| ucl200 | Name a manager whose club reached the Champions League semi-finals, 2015–16 onward | en:2015–16 to 2025–26 UEFA Champions League knockout phase pages (Semi-finals) + semi-finalists' club season pages (infobox manager) | 22 | modern | Zinedine Zidane, Jürgen Klopp, Erik ten Hag, Rudi Garcia, Julian Nagelsmann | manager in charge at the semi-final |

## Summary

- **Total prompts:** 200
- **Era split:** modern 137 (68%), 2000s+ 50 (25%), classic 13 (6%)
- **Per sub-heading:**
  - Finals: who played: 18
  - Finals: clubs across eras: 14
  - Finals: roles, nationalities, records: 19
  - Winning runs: squads: 19
  - Club eras: goalscorers: 17
  - Knockout goalscorers by season: 16
  - Knockout goalscorers by club: 8
  - League phase goalscorers: 12
  - Hat-tricks: 9
  - Players: awards and records: 9
  - Clubs: seasons: 10
  - Clubs: how far they went: 26
  - Clubs by country (1992 onward): 8
  - Countries: 4
  - Stadiums and cities: 8
  - Managers: 3

- **Template families (each ≤10%):** club-season squads 19, single-final matchday 18, club-era goalscorers 17, knockout scorers by season/round 16, finals by club across eras 14, league-phase scorers by club country 12, group/league-phase club lists 10, hat-tricks 9, knockout scorers v/for a club 8, nationality-in-finals 8, clubs by country 8.
- **Source verification:** every title cited was checked with the query API (batches of ≤50, ~0.6 s apart). Titles that came back missing were swapped for other sources. There is no "List of European Cup and UEFA Champions League winning players" page, no winning-captains list page and no "Category:UEFA Champions League winning players". So the winner-nationality prompts use the lineups on the final pages, and the captains prompt uses the records-page table. There are no "… group stage" pages from 2024–25 onward (they are "league phase" pages instead) and no "… league phase" pages before 2024–25. "German/Dutch football clubs in international competitions" don't exist, so the country club lists use "UEFA Champions League clubs performance comparison". "2025–26 Bayern Munich season" is missing, so "2025–26 FC Bayern Munich season" is used. Redirects: "UEFA Champions League records and statistics" goes to "European Cup and UEFA Champions League records and statistics"; "… qualifying phase and play-off round" goes to "20XX–YY UEFA Champions League qualifying"; "Celtic F.C. in European football" goes to "… in international football"; "Paris Saint-Germain F.C. …" goes to "Paris Saint-Germain FC …". The 2000–01 to 2007–08 pages are titled "knockout stage" (not "phase").
- **Risky prompts:**
  - Hard to scrape: shoot-out takers (finals and knockout ties), final captains (`(c)` marker), final goalkeepers, plus the 2018–19 knockout page and the 2023 final, whose markup is different from the other seasons.
  - Manager prompts that span many pages (2025–26 league-phase managers, quarter-final and semi-final managers) need each club's season-page infobox, and a rule for managers who changed mid-season.
  - The opponent prompts (Arsenal, Liverpool, Man United, Chelsea, Man City) have to filter by competition inside long all-UEFA match tables.
  - Lists close to the 12-answer floor: managers in finals since 2015 (13), league-phase top-eight clubs (13), Italian and French clubs by country (12 each), Squad/Team of the Season goalkeepers (14), Real Madrid knockout opponents (16).
  - Lists close to the ceiling: non-big-five league-phase scorers 2025–26 (~92), English-club final players since 2018 (~85), quarter-final scorers 2020–21 onward (~85).
  - Moving targets: 2026–27 league-phase clubs, stadiums and cities (season in progress), league-phase-era hat-tricks, the 100+ appearances list.
  - The classic club-era final prompts will put most answers in the rare tiers, because those players' pages get few views.
