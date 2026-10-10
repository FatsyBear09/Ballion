# General theme: prompt catalog

Theme id prefix `gen`. Scope: everything not owned by the Premier League, La Liga, Champions League or National-team themes (see `SPEC.md`).

Source conventions:
- `en:Title` is an English Wikipedia page title, verified via the API on 2026-10-09 (all titles below resolved with no `missing`). `en:A … en:B` means every season page in that range, one per season, all verified.
- `wd:pair(A, B)` means a Wikidata SPARQL query for humans (`P31=Q5`) with `P54` (member of sports team) pointing at both clubs' main first-team items (exclude reserve, youth and women's items). Each answer must have an enwiki sitelink.
- "Season squad" means anyone listed with at least one league appearance in the club-season page's squad/statistics table.
- Today is 2026-10-09, so the current season is 2026–27 (2026 for MLS and South America), and 2025–26 is the last completed season.

## Ballon d'Or and global awards

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| gen001 | Name a player nominated for the 2026 Ballon d'Or | en:2026 Ballon d'Or | 30 | modern | Mbappé, Yamal, Kane, Michael Olise, Julián Quiñones | 30-man nominee table |
| gen002 | Name a player nominated for the 2025 Ballon d'Or | en:2025 Ballon d'Or | 30 | modern | Dembélé, Yamal, Vitinha, Scott McTominay, Denzel Dumfries | nominee table |
| gen003 | Name a player nominated for the 2024 Ballon d'Or | en:2024 Ballon d'Or | 30 | modern | Rodri, Vinícius Júnior, Bellingham, Florian Wirtz, Artem Dovbyk | nominee table |
| gen004 | Name a player nominated for the 2023 Ballon d'Or | en:2023 Ballon d'Or | 30 | modern | Messi, Haaland, Kvaratskhelia, Bernardo Silva, Randal Kolo Muani | nominee table |
| gen005 | Name a player nominated for the 2022 Ballon d'Or | en:2022 Ballon d'Or | 30 | modern | Benzema, Mané, De Bruyne, Rafael Leão, Christopher Nkunku | nominee table |
| gen006 | Name a player nominated for the 2021 Ballon d'Or | en:2021 Ballon d'Or | 30 | modern | Messi, Lewandowski, Jorginho, N'Golo Kanté, Simon Kjær | nominee table |
| gen007 | Name a player nominated for the Ballon d'Or between 2016 and 2019 | en:2016 Ballon d'Or … en:2019 Ballon d'Or | 70 | modern | Ronaldo, Messi, Griezmann, Riyad Mahrez, Kalidou Koulibaly | union of four nominee tables |
| gen008 | Name a player on a FIFA Ballon d'Or shortlist (2010–2015) | en:FIFA Ballon d'Or | 60 | 2000s+ | Messi, Iniesta, Xavi, Gareth Bale, Diego Forlán | 23-man shortlists per year; union |
| gen009 | Name a player who finished in the Ballon d'Or top 10 since 2010 | en:FIFA Ballon d'Or; en:2016 Ballon d'Or … en:2025 Ballon d'Or | 50 | modern | Messi, Ronaldo, Modrić, Wesley Sneijder, Franck Ribéry | ranking tables, places 1–10; no 2020 edition |
| gen010 | Name a club whose player won the Ballon d'Or (club at the time of the award) | en:Ballon d'Or (wins by club) | 22 | classic | Real Madrid, Barcelona, Inter Miami CF, Dynamo Kyiv, Blackpool | men's award only |
| gen011 | Name a club that had a player nominated for the 2024, 2025 or 2026 Ballon d'Or | en:2024 Ballon d'Or; en:2025 Ballon d'Or; en:2026 Ballon d'Or | 30 | modern | Real Madrid, Paris Saint-Germain, Arsenal, Inter Miami CF, Al-Qadsiah | the club column of the nominee tables; a mid-year transfer counts the listed club |
| gen012 | Name a country with a player nominated for the 2024, 2025 or 2026 Ballon d'Or | same as gen011 | 25 | modern | France, Spain, England, Georgia, Ukraine | nationality flag in nominee tables; the answer is the men's national team or country article |
| gen013 | Name a player who finished in the top 3 for the Kopa Trophy | en:Kopa Trophy | 21 | modern | Mbappé, Yamal, Bellingham, Christian Pulisic, Justin Kluivert | men's table; top 3 per year since 2018 |
| gen014 | Name a goalkeeper who finished top 3 for the Yashin Trophy or won The Best FIFA Men's Goalkeeper | en:Yashin Trophy; en:The Best FIFA Goalkeeper | 17 | modern | Courtois, Alisson, Emiliano Martínez, Yassine Bounou, Andriy Lunin | union of both tables (men only) |
| gen015 | Name a player nominated for The Best FIFA Men's Player | en:The Best FIFA Football Awards 2016 … en:The Best FIFA Football Awards 2025 | 55 | modern | Messi, Ronaldo, Haaland, Jamie Vardy, Pierre-Emerick Aubameyang | "Winners and nominees" section, men's player list per edition |
| gen016 | Name a coach who finished in the top 3 for The Best FIFA Men's Coach | en:The Best FIFA Football Coach | 20 | modern | Guardiola, Klopp, Ancelotti, Claudio Ranieri, Fernando Santos | men's table, top 3 per year |
| gen017 | Name a goalscorer nominated for the FIFA Puskás Award since 2019 | en:FIFA Puskás Award | 70 | modern | Son Heung-min, Erik Lamela, Richarlison, Alejandro Garnacho, Marcin Oleksy | year sub-sections 2019–2025, all nominees (men and women) |
| gen018 | Name a country with a FIFA Puskás Award winner | en:FIFA Puskás Award (awards won by nationality) | 13 | 2000s+ | Brazil, Argentina, Egypt, South Korea, Malaysia | any winner since 2009 |
| gen019 | Name a player named in a FIFPRO Men's World 11 since 2015 | en:FIFPRO World 11 (men's winners) | 45 | modern | Messi, Ronaldo, Van Dijk, Achraf Hakimi, N'Golo Kanté | |
| gen020 | Name a goalkeeper or defender named in a FIFPRO Men's World 11 | en:FIFPRO World 11 (men's winners) | 35 | 2000s+ | Sergio Ramos, Neuer, Carles Puyol, Rúben Dias, Lúcio | all years since 2005; position as listed in the table |
| gen021 | Name a country represented in a FIFPRO Men's World 11 since 2015 | en:FIFPRO World 11 (men's winners) | 16 | modern | Argentina, Portugal, Brazil, Egypt, Norway | nationality flags |
| gen022 | Name a player named in a UEFA Team of the Year (2001–2020) | en:UEFA Team of the Year | 95 | 2000s+ | Ronaldo, Messi, Iniesta, Pavel Nedvěd, Ricardo Carvalho | year sections 2001–2020 |
| gen023 | Name a winner of the Golden Foot award | en:Golden Foot (award winners) | 22 | 2000s+ | Ronaldinho, Salah, Lewandowski, Ryan Giggs, Didier Drogba | men's award only |
| gen024 | Name a player on the 2020 Ballon d'Or Dream Team shortlist | en:Ballon d'Or Dream Team | 110 | classic | Pelé, Maradona, Messi, Paolo Maldini, Lev Yashin | all nominees, all positions |
| gen025 | Name a UEFA Jubilee "Golden Player" | en:UEFA Jubilee Awards | 52 | classic | Zidane, Cruyff, Ferenc Puskás, Jari Litmanen, Denis Law | one per member association (2003–04) |
| gen181 | Name a player nominated for the 2026 Kopa Trophy or the 2026 Yashin Trophy (men) | en:2026 Ballon d'Or (Men's Kopa Trophy; Men's Yashin Trophy) | 20 | modern | Lamine Yamal, Pau Cubarsí, Lennart Karl, Éli Junior Kroupi, Vozinha | the two 10-man nominee lists |
| gen182 | Name a winner of the FIFA Puskás Award | en:FIFA Puskás Award | 17 | 2000s+ | Cristiano Ronaldo, Zlatan Ibrahimović, Mohamed Salah, Son Heung-min, Marcin Oleksy | winners 2009–2025 |

## Women's football

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| gen026 | Name a woman who finished in the top 3 for the Ballon d'Or Féminin | en:Ballon d'Or Féminin | 16 | modern | Alexia Putellas, Aitana Bonmatí, Ada Hegerberg, Sam Kerr, Mariona Caldentey | winners table, places 1–3 |
| gen027 | Name a player named in a FIFPRO Women's World 11 | en:FIFPRO World 11 (women's winners) | 60 | modern | Marta, Megan Rapinoe, Alexia Putellas, Lucy Bronze, Wendie Renard | first edition 2015 |
| gen028 | Name a player on the list of most expensive women's football transfers | en:List of most expensive women's association football transfers (most expensive player transfers) | 35 | modern | Naomi Girma, Olivia Smith, Racheal Kundananji, Keira Walsh, Mayra Ramírez | main transfers table only; NWSL trades are excluded |
| gen029 | Name a club that has played in the NWSL | en:National Women's Soccer League (current and former clubs) | 20 | modern | Portland Thorns FC, Orlando Pride, Angel City FC, Kansas City Current, Bay FC | includes defunct clubs |

## Bundesliga

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| gen030 | Name a player who made a Bundesliga appearance for Bayer Leverkusen in their unbeaten 2023–24 title season | en:2023–24 Bayer 04 Leverkusen season | 27 | modern | Florian Wirtz, Granit Xhaka, Jeremie Frimpong, Alejandro Grimaldo, Adam Hložek | season squad |
| gen031 | Name a player who made a Bundesliga appearance for Bayern Munich under Vincent Kompany (2024–25 or 2025–26) | en:2024–25 FC Bayern Munich season; en:2025–26 FC Bayern Munich season | 40 | modern | Harry Kane, Jamal Musiala, Michael Olise, Luis Díaz, Tom Bischof | union of two season squads |
| gen032 | Name a player who has scored a Bundesliga hat-trick since the start of 2015–16 | en:List of Bundesliga hat-tricks | 70 | modern | Lewandowski, Haaland, Kane, Serhou Guirassy, Timo Werner | about 140 hat-tricks dated 2015-08-01 or later |
| gen033 | Name a player who has been named in a Bundesliga Team of the Season | en:Bundesliga Awards (Team of the Season) | 45 | modern | Kane, Haaland, Wirtz, Alejandro Grimaldo, Jesper Lindstrøm | award introduced in the late 2010s |
| gen034 | Name a player who finished in the top 5 of the Bundesliga scoring chart in a season since 2017–18 | en:2017–18 Bundesliga … en:2025–26 Bundesliga (top scorers table) | 40 | modern | Lewandowski, Kane, Haaland, Serhou Guirassy, André Silva | ranks 1–5 including ties |
| gen035 | Name an American who has played in the Bundesliga | en:List of foreign Bundesliga players (United States) | 95 | 2000s+ | Christian Pulisic, Gio Reyna, Tyler Adams, John Brooks, Bobby Wood | nationality as listed on the page |
| gen036 | Name a Japanese player who has played in the Bundesliga | en:List of foreign Bundesliga players (Japan) | 75 | modern | Shinji Kagawa, Makoto Hasebe, Daichi Kamada, Ritsu Dōan, Yasuhiko Okudera | |
| gen037 | Name an English player who has played in the Bundesliga | en:List of foreign Bundesliga players (England) | 45 | modern | Harry Kane, Jude Bellingham, Jadon Sancho, Jamie Bynoe-Gittens, Owen Hargreaves | |
| gen038 | Name a South Korean who has played in the Bundesliga | en:List of foreign Bundesliga players (Korea Republic) | 25 | modern | Son Heung-min, Kim Min-jae, Cha Bum-kun, Jeong Woo-yeong, Jens Castrop | |
| gen039 | Name a club promoted to the Bundesliga since 2015 | en:2015–16 Bundesliga … en:2026–27 Bundesliga (teams / promoted sections) | 25 | modern | RB Leipzig, Union Berlin, 1. FC Heidenheim, SV Elversberg, Holstein Kiel | clubs listed as promoted for each season, plus play-off winners |
| gen040 | Name a head coach who managed a Bundesliga club during 2025–26 | en:2025–26 Bundesliga (personnel and managerial changes) | 26 | modern | Vincent Kompany, Niko Kovač, Erik ten Hag, Kasper Hjulmand, Merlin Polzin | permanent and caretaker coaches |
| gen041 | Name the home stadium of a 2026–27 Bundesliga club | en:2026–27 Bundesliga (stadiums and locations) | 18 | modern | Allianz Arena, Westfalenstadion, BayArena, Arena AufSchalke, Home Deluxe Arena | the answer is the stadium article |
| gen042 | Name a club playing in the 2026–27 2. Bundesliga | en:2026–27 2. Bundesliga (teams) | 18 | modern | Hertha BSC, VfL Wolfsburg, FC St. Pauli, VfL Bochum, VfL Osnabrück | verified table: 18 clubs |
| gen043 | Name a player who has scored in a DFB-Pokal final since 2010 | en:2010 DFB-Pokal final … en:2026 DFB-Pokal final | 40 | modern | Lewandowski, Haaland, Thomas Müller, Christopher Nkunku, Ante Rebić | own goals excluded; shoot-out kicks excluded |
| gen044 | Name a club that has played in a DFB-Pokal final since 2000 | en:List of DFB-Pokal finals | 22 | 2000s+ | Bayern Munich, Borussia Dortmund, Bayer Leverkusen, Arminia Bielefeld, Alemannia Aachen | winners and runners-up from 2000 on |
| gen045 | Name a winner of Germany's Footballer of the Year award since 2000 | en:Footballer of the Year (Germany) | 20 | 2000s+ | Oliver Kahn, Michael Ballack, Harry Kane, Robert Lewandowski, Grafite | men's list |
| gen046 | Name a player who has played for both RB Leipzig and Red Bull Salzburg | wd:pair(RB Leipzig, FC Red Bull Salzburg) | 45 | modern | Dayot Upamecano, Naby Keïta, Dominik Szoboszlai, Konrad Laimer, Péter Gulácsi | first teams only (exclude FC Liefering) |
| gen183 | Name a Moroccan who has played in the Bundesliga | en:List of foreign Bundesliga players (Morocco) | 35 | modern | Achraf Hakimi, Noussair Mazraoui, Amine Harit, Bilal El Khannouss, Mehdi Benatia | |
| gen184 | Name a club relegated from the Bundesliga since 2015 | en:2015–16 Bundesliga … en:2025–26 Bundesliga (relegated clubs) | 25 | modern | Hamburger SV, Schalke 04, Hertha BSC, VfL Wolfsburg, SC Paderborn 07 | automatic relegation plus relegation play-off losers |

## Serie A

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| gen047 | Name a player who made a Serie A appearance for Napoli in their 2022–23 Scudetto season | en:2022–23 SSC Napoli season | 28 | modern | Victor Osimhen, Khvicha Kvaratskhelia, Kim Min-jae, Stanislav Lobotka, Eljif Elmas | season squad |
| gen048 | Name a player who made a Serie A appearance for Napoli in Antonio Conte's 2024–25 title season | en:2024–25 SSC Napoli season | 30 | modern | Scott McTominay, Romelu Lukaku, Kvaratskhelia, Giovanni Di Lorenzo, Billy Gilmour | season squad |
| gen049 | Name a player who made a Serie A appearance for Inter in their 2023–24 "second star" season | en:2023–24 Inter Milan season | 28 | modern | Lautaro Martínez, Marcus Thuram, Nicolò Barella, Hakan Çalhanoğlu, Yann Bisseck | season squad |
| gen050 | Name a player who made a Serie A appearance for AC Milan in their 2021–22 title season | en:2021–22 AC Milan season | 30 | modern | Rafael Leão, Olivier Giroud, Sandro Tonali, Theo Hernández, Pietro Pellegri | season squad |
| gen051 | Name a player who made a Serie A appearance for Juventus during their nine-in-a-row (2011–12 to 2019–20) | en:2011–12 Juventus FC season … en:2019–20 Juventus FC season | 110 | 2000s+ | Cristiano Ronaldo, Gianluigi Buffon, Andrea Pirlo, Gonzalo Higuaín, Simone Padoin | union of nine season squads; near the ceiling |
| gen052 | Name a player who has scored a Serie A hat-trick since the start of 2015–16 | en:List of Serie A hat-tricks | 60 | modern | Ciro Immobile, Cristiano Ronaldo, Lautaro Martínez, Duván Zapata, Andrea Belotti | hat-tricks dated 2015-08-01 or later |
| gen053 | Name a player who finished in the top 5 of the Serie A scoring chart in a season since 2017–18 | en:2017–18 Serie A … en:2025–26 Serie A (top goalscorers table) | 40 | modern | Immobile, Ronaldo, Lautaro, Osimhen, Mateo Retegui | ranks 1–5 including ties |
| gen054 | Name a player named in the Serie A Team of the Year since 2018–19 | en:Serie A Team of the Year | 60 | modern | Osimhen, Lautaro, Barella, Kvaratskhelia, Theo Hernández | season sub-sections 2018–19 to 2025–26 |
| gen055 | Name a winner of the Serie A Footballer of the Year / Most Valuable Player award | en:Serie A Footballer of the Year | 22 | 2000s+ | Kaká, Zlatan Ibrahimović, Francesco Totti, Victor Osimhen, Lautaro Martínez | list of winners, 1997 to present |
| gen056 | Name a winner of the Serie A Young Footballer of the Year | en:Serie A Young Footballer of the Year | 14 | 2000s+ | Daniele De Rossi, Alexandre Pato, Marek Hamšík, Javier Pastore, Alberto Gilardino | award ran 1997–2010 |
| gen057 | Name an English player who has played in Serie A | en:List of foreign Serie A players (England) | 45 | 2000s+ | Fikayo Tomori, Tammy Abraham, Chris Smalling, Ruben Loftus-Cheek, Paul Gascoigne | |
| gen058 | Name a Japanese player who has played in Serie A | en:List of foreign Serie A players (Japan) | 15 | 2000s+ | Hidetoshi Nakata, Yuto Nagatomo, Keisuke Honda, Takehiro Tomiyasu, Shunsuke Nakamura | |
| gen059 | Name a head coach who managed a Serie A club during 2025–26 | en:2025–26 Serie A (personnel and managerial changes) | 30 | modern | Antonio Conte, Massimiliano Allegri, Cristian Chivu, Gian Piero Gasperini, Cesc Fàbregas | permanent and caretaker coaches |
| gen060 | Name a club relegated from Serie A since 2015 | en:2014–15 Serie A … en:2025–26 Serie A (relegated clubs) | 30 | modern | Parma, Sampdoria, Salernitana, Frosinone, Benevento | bottom three each season |
| gen061 | Name the home stadium of a 2026–27 Serie A club | en:2026–27 Serie A (stadiums and locations) | 18 | modern | San Siro, Stadio Olimpico, Stadio Diego Armando Maradona, Stadio Giuseppe Sinigaglia, Stadio Benito Stirpe | shared grounds counted once |
| gen062 | Name a player who has scored in a Coppa Italia final since 2010 | en:2010 Coppa Italia final … en:2026 Coppa Italia final | 30 | modern | Lautaro Martínez, Dušan Vlahović, Federico Chiesa, Ivan Perišić, Dan Ndoye | own goals and shoot-out kicks excluded |
| gen063 | Name a Juventus head coach since 2000 | en:List of Juventus FC managers | 16 | 2000s+ | Massimiliano Allegri, Antonio Conte, Andrea Pirlo, Luciano Spalletti, Luigi Delneri | caretakers included |
| gen064 | Name an AC Milan head coach since 2000 | en:List of AC Milan managers | 20 | 2000s+ | Carlo Ancelotti, Stefano Pioli, Allegri, Clarence Seedorf, Cristian Brocchi | caretakers included |
| gen065 | Name an Inter head coach since 2000 | en:List of Inter Milan managers | 20 | 2000s+ | José Mourinho, Antonio Conte, Simone Inzaghi, Cristian Chivu, Andrea Stramaccioni | caretakers included |
| gen066 | Name a player who has played for both Juventus and Inter | wd:pair(Juventus FC, Inter Milan) | 70 | 2000s+ | Zlatan Ibrahimović, Patrick Vieira, Fabio Cannavaro, Juan Cuadrado, Arturo Vidal | |
| gen067 | Name a player who has played for both Napoli and Juventus | wd:pair(SSC Napoli, Juventus FC) | 50 | 2000s+ | Gonzalo Higuaín, Fabio Cannavaro, Fabio Quagliarella, Ciro Ferrara, José Altafini | |
| gen068 | Name a player who has played for both Roma and Lazio | wd:pair(AS Roma, SS Lazio) | 35 | classic | Pedro, Aleksandar Kolarov, Angelo Peruzzi, Lionello Manfredonia | |
| gen185 | Name a club promoted to Serie A since 2015 | en:2015–16 Serie A … en:2026–27 Serie A (promoted clubs) | 28 | modern | Como 1907, Parma, Frosinone, Venezia, Pisa | |

## Ligue 1

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| gen069 | Name a player who made a Ligue 1 appearance for Monaco in their 2016–17 title season | en:2016–17 AS Monaco FC season | 30 | modern | Kylian Mbappé, Bernardo Silva, Radamel Falcao, Fabinho, Kamil Glik | season squad |
| gen070 | Name a player who made a Ligue 1 appearance for Lille in their 2020–21 title season | en:2020–21 Lille OSC season | 28 | modern | Jonathan David, Burak Yılmaz, Renato Sanches, Mike Maignan, Boubakary Soumaré | season squad |
| gen071 | Name a player who made a Ligue 1 appearance for PSG under Luis Enrique (2023–24 to 2025–26) | en:2023–24 Paris Saint-Germain FC season; en:2024–25 Paris Saint-Germain FC season; en:2025–26 Paris Saint-Germain FC season | 55 | modern | Mbappé, Ousmane Dembélé, Vitinha, Désiré Doué, Senny Mayulu | union of three season squads |
| gen072 | Name a winner of the Ligue 1 Player of the Year award | en:Ligue 1 Player of the Year | 25 | 2000s+ | Mbappé, Neymar, Dembélé, Pauleta, Juninho Pernambucano | UNFP award since 1994 |
| gen073 | Name a winner of the Ligue 1 Young Player of the Year award | en:Ligue 1 Young Player of the Year | 30 | 2000s+ | Mbappé, Eden Hazard, Aurélien Tchouaméni, Désiré Doué, Warren Zaïre-Emery | |
| gen199 | Name a winner of the UNFP Ligue 1 Goalkeeper of the Year award | en:Trophées UNFP du football (Goalkeeper of the Year) | 13 | 2000s+ | Hugo Lloris, Steve Mandanda, Grégory Coupet, Keylor Navas, Lucas Chevalier | |
| gen074 | Name a player named in the UNFP Ligue 1 Team of the Year since 2015–16 | en:Trophées UNFP du football (Ligue 1 Team of the Year) | 80 | modern | Mbappé, Neymar, Marquinhos, Jonathan David, Wissam Ben Yedder | season sub-sections 2015–16 to 2025–26 |
| gen075 | Name a winner of the UNFP Ligue 1 Player of the Month award since 2015 | en:UNFP Player of the Month | 50 | modern | Mbappé, Neymar, Jonathan David, Wissam Ben Yedder | monthly winners from August 2015 |
| gen076 | Name a player who has scored a Ligue 1 hat-trick since the start of 2015–16 | en:List of Ligue 1 hat-tricks | 60 | modern | Mbappé, Edinson Cavani, Neymar, Jonathan David, Andy Delort | hat-tricks dated 2015-08-01 or later |
| gen077 | Name a player who finished in the top 5 of the Ligue 1 scoring chart in a season since 2017–18 | en:2017–18 Ligue 1 … en:2025–26 Ligue 1 (top scorers table) | 40 | modern | Mbappé, Wissam Ben Yedder, Jonathan David, Mason Greenwood, Alexandre Lacazette | ranks 1–5 including ties |
| gen078 | Name a head coach who managed a Ligue 1 club during 2025–26 | en:2025–26 Ligue 1 (personnel and managerial changes) | 24 | modern | Luis Enrique, Roberto De Zerbi, Paulo Fonseca, Vahid Halilhodžić, Antoine Kombouaré | personnel table uses plain text; scrape names and resolve to articles |
| gen079 | Name a club promoted to Ligue 1 since 2015 | en:2015–16 Ligue 1 … en:2026–27 Ligue 1 (promoted clubs) | 28 | modern | RC Lens, Stade Brestois, Paris FC, Le Mans FC, Clermont Foot | play-off winners included |
| gen080 | Name the home stadium of a 2026–27 Ligue 1 club | en:2026–27 Ligue 1 (stadiums and locations) | 18 | modern | Parc des Princes, Stade Vélodrome, Stade Jean-Bouin, Stade Marie-Marvingt, Stade de l'Aube | |
| gen081 | Name a club that has played in a Coupe de France final since 2000 | en:List of Coupe de France finals | 28 | 2000s+ | PSG, Marseille, Stade Rennais, Les Herbiers VF, Calais RUFC | winners and runners-up; amateur giant-killers have articles |
| gen082 | Name a PSG head coach since 2000 | en:List of Paris Saint-Germain FC managers | 15 | 2000s+ | Carlo Ancelotti, Unai Emery, Thomas Tuchel, Mauricio Pochettino, Antoine Kombouaré | caretakers included |
| gen083 | Name a player who has played for both Marseille and Lyon | wd:pair(Olympique de Marseille, Olympique Lyonnais) | 50 | 2000s+ | Mathieu Valbuena, Bafétimbi Gomis, Sonny Anderson, Jérémy Morel | |
| gen084 | Name a player who has played for both PSG and Real Madrid | wd:pair(Paris Saint-Germain FC, Real Madrid CF) | 18 | 2000s+ | Mbappé, Sergio Ramos, Ángel Di María, Claude Makélélé, Nicolas Anelka | cross-league career |
| gen085 | Name a player who has played for both PSG and Barcelona | wd:pair(Paris Saint-Germain FC, FC Barcelona) | 16 | modern | Messi, Neymar, Ousmane Dembélé, Ronaldinho, Maxwell | cross-league career |
| gen086 | Name a player who has played for both PSG and Inter | wd:pair(Paris Saint-Germain FC, Inter Milan) | 18 | 2000s+ | Achraf Hakimi, Zlatan Ibrahimović, Mauro Icardi, Milan Škriniar, Thiago Motta | |
| gen186 | Name a club relegated from Ligue 1 since 2015 | en:2015–16 Ligue 1 … en:2025–26 Ligue 1 (relegated clubs) | 28 | modern | Girondins de Bordeaux, AS Saint-Étienne, Montpellier HSC, AC Ajaccio, ES Troyes AC | play-off losers included |

## Netherlands, Portugal, Scotland and Turkey

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| gen087 | Name a player who made an Eredivisie appearance for Ajax in 2018–19 | en:2018–19 AFC Ajax season | 28 | modern | Frenkie de Jong, Matthijs de Ligt, Hakim Ziyech, Dušan Tadić, Noussair Mazraoui | season squad |
| gen088 | Name a player who made an Eredivisie appearance for Feyenoord in their 2022–23 title season | en:2022–23 Feyenoord season | 28 | modern | Santiago Giménez, Orkun Kökçü, Lutsharel Geertruida, Quilindschy Hartman, Danilo | season squad |
| gen089 | Name a player who has scored an Eredivisie hat-trick since the start of 2015–16 | en:List of Eredivisie hat-tricks | 70 | modern | Sébastien Haller, Alexander Isak, Dušan Tadić, Santiago Giménez, Ayase Ueda | |
| gen090 | Name a player who finished as Eredivisie top scorer in a season since 2005–06 | en:2005–06 Eredivisie … en:2025–26 Eredivisie (top scorers) | 20 | 2000s+ | Luis Suárez, Klaas-Jan Huntelaar, Vangelis Pavlidis, Bas Dost, Alfreð Finnbogason | shared top scorers count |
| gen091 | Name a winner of the Eredivisie Player of the Month award | en:Eredivisie Player of the Month | 50 | modern | Dušan Tadić, Santiago Giménez, Luuk de Jong, Ismael Saibari | award started 2017 |
| gen092 | Name a club playing in the 2026–27 Eredivisie | en:2026–27 Eredivisie (teams) | 18 | modern | Ajax, PSV Eindhoven, Feyenoord, Go Ahead Eagles, ADO Den Haag | |
| gen187 | Name the home stadium of a 2026–27 Eredivisie club | en:2026–27 Eredivisie (stadiums and locations) | 18 | modern | Johan Cruyff Arena, Philips Stadion, De Kuip, AFAS Stadion, De Adelaarshorst | |
| gen189 | Name a player who finished in the top 5 of the Eredivisie scoring chart in a season since 2020–21 | en:2020–21 Eredivisie … en:2025–26 Eredivisie (top scorers) | 25 | modern | Sébastien Haller, Santiago Giménez, Vangelis Pavlidis, Luuk de Jong, Sem Steijn | ranks 1–5 including ties |
| gen093 | Name a player who has played for both Ajax and PSV | wd:pair(AFC Ajax, PSV Eindhoven) | 60 | classic | Ronald Koeman, Steven Bergwijn, Jan Wouters | |
| gen094 | Name a player who has played for both Ajax and Barcelona | wd:pair(AFC Ajax, FC Barcelona) | 30 | 2000s+ | Johan Cruyff, Frenkie de Jong, Patrick Kluivert, Marc Overmars, Jari Litmanen | cross-league career |
| gen095 | Name a player who made a Primeira Liga appearance for Sporting CP in their 2020–21 title season | en:2020–21 Sporting CP season | 28 | modern | Pedro Gonçalves, Nuno Mendes, João Palhinha, Sebastián Coates, Matheus Nunes | season squad |
| gen096 | Name a player who finished as Primeira Liga top scorer in a season since 2000 | en:List of Portuguese football champions (champions and top scorers) | 22 | 2000s+ | Viktor Gyökeres, Jonas, Radamel Falcao, Liédson, Mário Jardel | top-scorer column, 2000–01 on |
| gen097 | Name a winner of the LPFP Primeira Liga Player of the Year | en:LPFP Primeira Liga Player of the Year | 18 | 2000s+ | Gyökeres, Bruno Fernandes, Darwin Núñez, Simão Sabrosa, Sebastián Coates | since 2005–06 |
| gen098 | Name a club playing in the 2026–27 Primeira Liga | en:2026–27 Primeira Liga (teams) | 18 | modern | Benfica, Porto, Sporting CP, Braga, Académico de Viseu | |
| gen188 | Name the home stadium of a 2026–27 Primeira Liga club | en:2026–27 Primeira Liga (stadiums and locations) | 18 | modern | Estádio da Luz, Estádio do Dragão, Estádio José Alvalade, Estádio Municipal de Braga, Estádio do Fontelo | |
| gen099 | Name an FC Porto head coach since 2000 | en:List of FC Porto managers | 16 | 2000s+ | José Mourinho, André Villas-Boas, Sérgio Conceição, Julen Lopetegui, Francesco Farioli | caretakers included |
| gen100 | Name a Benfica head coach since 2000 | en:List of S.L. Benfica managers | 18 | 2000s+ | Jorge Jesus, Roger Schmidt, José Mourinho, Bruno Lage, Fernando Santos | caretakers included |
| gen101 | Name a player who has played for both Benfica and Porto | wd:pair(S.L. Benfica, FC Porto) | 60 | classic | Maxi Pereira, Deco, Paulo Futre, Derlei | |
| gen102 | Name a player who made a Premiership appearance for Celtic in their 2016–17 invincible treble season | en:2016–17 Celtic F.C. season | 30 | modern | Moussa Dembélé, Scott Sinclair, Kieran Tierney, Scott Brown, Patrick Roberts | season squad |
| gen103 | Name a club that has played in the Scottish Premiership (2013–present) | en:2013–14 Scottish Premiership … en:2026–27 Scottish Premiership | 22 | modern | Celtic, Rangers, Hearts, Livingston, Inverness Caledonian Thistle | union of season team lists |
| gen104 | Name a player who finished as Süper Lig top scorer in a season since 2000 | en:List of Süper Lig top scorers (top scorers by season) | 22 | 2000s+ | Mauro Icardi, Victor Osimhen, Burak Yılmaz, Alex de Souza, Hakan Şükür | |
| gen105 | Name a club playing in the 2026–27 Süper Lig | en:2026–27 Süper Lig (teams) | 18 | modern | Galatasaray, Fenerbahçe, Beşiktaş, Göztepe, Amed SFK | |
| gen200 | Name a club playing in the 2026–27 Scottish Premiership | en:2026–27 Scottish Premiership (teams) | 12 | modern | Celtic, Rangers, Hearts, Aberdeen, Hibernian | exactly 12, so the minimum size |
| gen106 | Name a player who has played for both Galatasaray and Fenerbahçe | wd:pair(Galatasaray S.K. (football), Fenerbahçe S.K. (football)) | 40 | 2000s+ | Emre Belözoğlu, Mehmet Topal, Serdar Aziz, Tanju Çolak | |
| gen107 | Name a European club that went a whole top-flight league season unbeaten | en:List of unbeaten football club seasons (Europe) | 60 | classic | Arsenal, Juventus, Bayer Leverkusen, Celtic, Lincoln Red Imps | men's section only; many deep cuts from small leagues |

## MLS and North America

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| gen108 | Name a player who has played for Inter Miami in the Messi era (2023 onward) | en:2023 Inter Miami CF season; en:2024 Inter Miami CF season; en:2025 Inter Miami CF season; en:2026 Inter Miami CF season | 80 | modern | Lionel Messi, Luis Suárez, Sergio Busquets, Rodrigo De Paul, Benjamin Cremaschi | at least one competitive appearance in any squad table |
| gen109 | Name a Designated Player of Inter Miami or LAFC | en:Designated Player Rule (Inter Miami CF; Los Angeles FC) | 22 | modern | Messi, Son Heung-min, Carlos Vela, Denis Bouanga, Blaise Matuidi | club DP history sections |
| gen110 | Name a Designated Player of the LA Galaxy | en:Designated Player Rule (LA Galaxy) | 22 | 2000s+ | David Beckham, Robbie Keane, Javier Hernández, Riqui Puig, Romain Alessandrini | |
| gen111 | Name a winner of the MLS MVP award | en:Landon Donovan MVP Award | 28 | 2000s+ | Messi, Carlos Vela, Josef Martínez, Landon Donovan, Preki | |
| gen112 | Name a winner of the MLS Golden Boot | en:MLS Golden Boot | 28 | 2000s+ | Josef Martínez, Carlos Vela, Denis Bouanga, Chris Wondolowski, Bradley Wright-Phillips | |
| gen113 | Name a player named in the MLS Best XI since 2015 | en:MLS Best XI | 80 | modern | Messi, Carlos Vela, Zlatan Ibrahimović, Sebastian Giovinco, Lucas Zelarayán | |
| gen114 | Name a winner of the MLS Newcomer of the Year award | en:MLS Newcomer of the Year Award | 20 | modern | Zlatan Ibrahimović, Sebastian Giovinco, Miguel Almirón, Thiago Almada, Anders Dreyer | |
| gen115 | Name a player who has scored an MLS hat-trick since 2015 | en:List of Major League Soccer hat-tricks | 90 | modern | Messi, Zlatan Ibrahimović, Carlos Vela, Josef Martínez, Sebastian Giovinco | regular season and playoffs as listed |
| gen116 | Name a player who has scored 100+ MLS goals | en:List of Major League Soccer players with 100 or more goals | 22 | 2000s+ | Chris Wondolowski, Landon Donovan, Carlos Vela, Bradley Wright-Phillips, Jaime Moreno | |
| gen117 | Name a player who has played 400+ MLS games | en:List of Major League Soccer players with 400 or more games played | 25 | 2000s+ | Nick Rimando, Kyle Beckerman, Chris Wondolowski, Jeff Larentowicz, Dax McCarty | |
| gen118 | Name a club that has won the MLS Cup | en:MLS Cup (results / winners) | 17 | 2000s+ | LA Galaxy, Seattle Sounders FC, Atlanta United FC, Columbus Crew, Real Salt Lake | |
| gen119 | Name a player who has scored in an MLS Cup final since 2010 | en:MLS Cup 2010 … en:MLS Cup 2025 | 35 | modern | Robbie Keane, Josef Martínez, Diego Valeri, Dejan Joveljić | regulation and extra time only |
| gen120 | Name a stadium that is or was home to an MLS club | en:List of Major League Soccer stadiums | 30 | modern | Mercedes-Benz Stadium, BMO Stadium, Lumen Field, Chase Stadium, Geodis Park | current table; add the former-stadiums table if present |
| gen121 | Name a club that played the MLS All-Stars in an All-Star Game | en:MLS All-Star Game (MLS All-Stars vs invited opponents) | 18 | 2000s+ | Arsenal, Juventus, Real Madrid, Bayern Munich, Fulham | European guests from 2005 on; also Celtic, Chelsea, Everton |
| gen122 | Name a head coach of an MLS club in the 2026 season | en:2026 Major League Soccer season (personnel / coaching changes) | 32 | modern | Javier Mascherano, Phil Neville, Óscar Pareja, Marco Donadel | permanent and interim coaches |
| gen123 | Name a club playing in Liga MX in 2026–27 | en:2026–27 Liga MX season | 18 | modern | Club América, C.D. Guadalajara, Tigres UANL, C.F. Monterrey, FC Juárez | |
| gen191 | Name a player who finished in the top 5 of the MLS scoring chart in a season since 2023 | en:2023 Major League Soccer season … en:2025 Major League Soccer season (top scorers) | 15 | modern | Lionel Messi, Denis Bouanga, Christian Benteke, Sam Surridge | regular season; ranks 1–5 including ties |
| gen192 | Name a player in either squad for the 2025 MLS All-Star Game | en:2025 MLS All-Star Game (squads: MLS All-Stars; Liga MX All-Stars) | 52 | modern | Lionel Messi, Sergio Ramos, James Rodríguez, Anders Dreyer, Ángel Correa | named squads, including replaced or withdrawn players |
| gen193 | Name a country with a player in the MLS Best XI since 2015 | en:MLS Best XI | 25 | modern | Argentina, United States, Mexico, Italy, Sweden | nationality flags |

## Saudi Pro League and Asia

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| gen124 | Name a club playing in the 2026–27 Saudi Pro League | en:2026–27 Saudi Pro League (teams) | 18 | modern | Al-Nassr, Al-Hilal, Al-Ittihad, Al-Qadsiah, Al-Kholood Club | |
| gen125 | Name a player who finished as Saudi Pro League top scorer in a season | en:Saudi Pro League (top scorers by season) | 30 | 2000s+ | Cristiano Ronaldo, Aleksandar Mitrović, Abderrazak Hamdallah, Nasser Al-Shamrani, Omar Al Somah | |
| gen126 | Name a player who made a league appearance for Al-Nassr in 2023–24 | en:2023–24 Al-Nassr FC season | 30 | modern | Cristiano Ronaldo, Sadio Mané, Marcelo Brozović, Otávio, Aymeric Laporte | season squad |
| gen127 | Name a player who made a league appearance for Al-Hilal in their record-breaking 2023–24 season | en:2023–24 Al Hilal SFC season | 30 | modern | Neymar, Aleksandar Mitrović, Sergej Milinković-Savić, Kalidou Koulibaly, Salem Al-Dawsari | season squad |
| gen128 | Name a player who made a league appearance for Al-Ittihad in their 2024–25 title season | en:2024–25 Al-Ittihad Club season | 30 | modern | Karim Benzema, N'Golo Kanté, Moussa Diaby, Steven Bergwijn, Houssem Aouar | season squad |
| gen129 | Name a Portuguese player who has played in the Saudi Pro League | en:List of foreign Saudi Professional League players (Portugal) | 50 | modern | Cristiano Ronaldo, Rúben Neves, João Cancelo, Otávio, João Félix | |
| gen130 | Name a French player who has played in the Saudi Pro League | en:List of foreign Saudi Professional League players (France) | 55 | modern | Karim Benzema, N'Golo Kanté, Moussa Diaby, Theo Hernández, Bafétimbi Gomis | |
| gen131 | Name a player who has scored a Saudi Pro League hat-trick since 2023–24 | en:List of Saudi Pro League hat-tricks | 35 | modern | Cristiano Ronaldo, Aleksandar Mitrović, Ivan Toney, Karim Benzema, Abderrazak Hamdallah | hat-tricks dated 2023-08-01 or later |
| gen132 | Name a head coach who managed a Saudi Pro League club from 2023–24 to 2025–26 | en:2023–24 Saudi Pro League; en:2024–25 Saudi Pro League; en:2025–26 Saudi Pro League | 55 | modern | Jorge Jesus, Simone Inzaghi, Stefano Pioli, Steven Gerrard, Laurent Blanc | personnel and managerial-changes tables |
| gen133 | Name a club in the 2025–26 AFC Champions League Elite | en:2025–26 AFC Champions League Elite (teams) | 24 | modern | Al-Hilal, Al-Ahli, Al-Ittihad, Vissel Kobe, Buriram United | league-stage clubs only (exclude play-off losers) |
| gen190 | Name a player who finished in the top 5 of the Saudi Pro League scoring chart since 2023–24 | en:2023–24 Saudi Pro League … en:2025–26 Saudi Pro League (top scorers) | 15 | modern | Cristiano Ronaldo, Aleksandar Mitrović, Ivan Toney, Karim Benzema, Abderrazak Hamdallah | ranks 1–5 including ties |
| gen194 | Name a player who scored in the 2024–25 AFC Champions League Elite knockout stage | en:2024–25 AFC Champions League Elite knockout stage | 31 | modern | Cristiano Ronaldo, Riyad Mahrez, Jhon Durán, Galeno, Akram Afif | 31 linked scorers; Al-Ahli's title run |

## Transfers and money

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| gen134 | Name a player on the list of the 50 most expensive football transfers | en:List of most expensive association football transfers (top 50 table) | 44 | modern | Neymar, Mbappé, Bellingham, Alexander Isak, Jhon Durán | players who appear more than once count once; table updated 2026-09-01 |
| gen135 | Name a club that bought or sold a player in one of the 50 most expensive transfers | en:List of most expensive association football transfers (top 50 table) | 35 | modern | Real Madrid, Barcelona, Chelsea, Benfica, Al-Nassr | From and To columns |
| gen136 | Name the nationality of a player in the 50 most expensive transfers | en:List of most expensive association football transfers (top 50 table) | 18 | modern | France, Brazil, England, Argentina, Sweden | the answer is the country or men's national team article |
| gen137 | Name a club that has paid a world-record transfer fee | en:List of most expensive association football transfers (world football transfer record, historical progression) | 20 | classic | Real Madrid, Paris Saint-Germain, Barcelona, Napoli, SS Lazio | buying club column |

## Europa League, Conference League and Super Cup

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| gen138 | Name a player who has scored in a Europa League final since 2010 | en:2010 UEFA Europa League final … en:2026 UEFA Europa League final | 35 | modern | Antoine Griezmann, Radamel Falcao, Ademola Lookman, Brennan Johnson, Coke | own goals and shoot-out kicks excluded |
| gen139 | Name a manager who has won the UEFA Cup or Europa League since 2000 | en:List of UEFA Cup and Europa League–winning managers | 22 | 2000s+ | José Mourinho, Unai Emery, Diego Simeone, Gian Piero Gasperini, Juande Ramos | |
| gen140 | Name a player who finished as Europa League top scorer in a season since 2009–10 | en:List of UEFA Cup and Europa League top scorers (top scorers by season) | 25 | modern | Radamel Falcao, Aritz Aduriz, Bruno Fernandes, Ayoub El Kaabi, Borja Mayoral | shared top scorers count |
| gen141 | Name a player in the all-time UEFA Cup / Europa League top scorers table | en:List of UEFA Cup and Europa League top scorers (all-time, group stage to final) | 30 | 2000s+ | Aritz Aduriz, Radamel Falcao, Alexandre Lacazette, Henrik Larsson, Klaas-Jan Huntelaar | |
| gen142 | Name a player who has scored a Europa League hat-trick since 2015–16 | en:List of UEFA Europa League hat-tricks | 60 | modern | Aubameyang, Alexandre Lacazette, Ademola Lookman, Edin Džeko, Mu'nas Dabbur | hat-tricks dated 2015-07-01 or later |
| gen143 | Name a player who has scored a Conference League hat-trick | en:List of UEFA Conference League hat-tricks | 18 | modern | Harry Kane, Nicolò Zaniolo, Ayoub El Kaabi, Kévin Denkey, Gift Orban | only about 20 rows, so a small prompt |
| gen144 | Name a player who scored in the 2025–26 Europa League knockout phase | en:2025–26 UEFA Europa League knockout phase | 85 | modern | Ollie Watkins, Morgan Gibbs-White, Lorenzo Pellegrini, Antony, Iago Aspas | knockout play-offs to final; `goals1/goals2` fields of the football boxes; about 85 linked scorers |
| gen145 | Name a player who scored in the 2024–25 Europa League knockout phase | en:2024–25 UEFA Europa League knockout phase | 100 | modern | Bruno Fernandes, Dominic Solanke, James Maddison, Nico Williams, Mikel Oyarzabal | about 100 linked scorers; own goals excluded |
| gen146 | Name a player who scored in the 2025–26 Conference League knockout phase | en:2025–26 UEFA Conference League knockout phase | 85 | modern | Ismaïla Sarr, Albert Guðmundsson, Mikael Ishak, Troy Parrott, Rolando Mandragora | knockout play-offs to final; about 85 linked scorers |
| gen195 | Name a player who scored in the 2024–25 Conference League knockout phase | en:2024–25 UEFA Conference League knockout phase | 90 | modern | Isco, Moise Kean, Noni Madueke, Antony, Cédric Bakambu | about 90 linked scorers; Chelsea's winning run |
| gen147 | Name a club that reached a Europa League semi-final since 2015–16 | en:2015–16 UEFA Europa League … en:2025–26 UEFA Europa League (knockout phase bracket) | 32 | modern | Sevilla, Roma, Manchester United, Eintracht Frankfurt, Bodø/Glimt | |
| gen148 | Name a club that reached a Conference League semi-final | en:2021–22 UEFA Europa Conference League … en:2025–26 UEFA Conference League (knockout phase) | 18 | modern | Roma, Fiorentina, Olympiacos, Djurgårdens IF, FC Basel | 2021–22 and 2022–23 pages use the old "Europa Conference League" name |
| gen149 | Name a club in the 2026–27 Europa League league phase | en:2026–27 UEFA Europa League (league phase table) | 36 | modern | AC Milan, Juventus, Bayer Leverkusen, Sunderland, S.C.U. Torreense | league-phase table only, not qualifying losers |
| gen150 | Name a country with a club in the 2026–27 Conference League league phase | en:2026–27 UEFA Conference League (league phase table) | 28 | modern | England, Spain, Poland, Cyprus, Kosovo | the answer is the country article; association of the club |
| gen151 | Name a player who made a Europa League appearance for Atalanta in their 2023–24 winning run | en:2023–24 Atalanta BC season | 26 | modern | Ademola Lookman, Teun Koopmeiners, Gianluca Scamacca, Charles De Ketelaere, Ederson | Europa League column of the season squad table |
| gen152 | Name a player who made a Europa League appearance for Eintracht Frankfurt in their 2021–22 winning run | en:2021–22 Eintracht Frankfurt season | 26 | modern | Daichi Kamada, Filip Kostić, Kevin Trapp, Rafael Borré, Ansgar Knauff | Europa League column of the season squad table |
| gen153 | Name a stadium that has hosted a UEFA Cup or Europa League final since 1998 | en:List of UEFA Cup and Europa League finals | 27 | 2000s+ | Aviva Stadium, Puskás Aréna, San Mamés Stadium, Philips Stadion | single-match finals only (1998 on) |
| gen154 | Name a stadium that has hosted a UEFA Super Cup since 1998 | en:UEFA Super Cup (list of venues since 1998) | 20 | 2000s+ | Stade Louis II, Windsor Park, Vodafone Park | |
| gen155 | Name a player who has scored in a UEFA Super Cup since 2010 | en:2010 UEFA Super Cup … en:2026 UEFA Super Cup | 35 | modern | Lionel Messi, Pedro, Diego Costa, Kylian Mbappé, Lee Kang-in | own goals and shoot-out kicks excluded |
| gen156 | Name a club that has played in the UEFA Super Cup since 2000 | en:List of UEFA Super Cup matches | 28 | 2000s+ | Real Madrid, Sevilla, Atalanta, Zenit Saint Petersburg, Galatasaray | |

## Club World Cup and South America

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| gen157 | Name a club that played at the 2025 FIFA Club World Cup | en:2025 FIFA Club World Cup (qualified teams) | 32 | modern | Real Madrid, Chelsea, Inter Miami CF, Auckland City, Espérance de Tunis | |
| gen158 | Name a player who scored in the 2025 Club World Cup knockout stage | en:2025 FIFA Club World Cup knockout stage | 37 | modern | Cole Palmer, Harry Kane, Erling Haaland, Kylian Mbappé, Hércules | 37 linked scorers counted from the page; own goals excluded |
| gen159 | Name a stadium that hosted a 2025 Club World Cup match | en:2025 FIFA Club World Cup (venues) | 12 | modern | MetLife Stadium, Hard Rock Stadium, Rose Bowl, Lincoln Financial Field, TQL Stadium | exactly 12, so the minimum size |
| gen160 | Name a country with a club at the 2025 FIFA Club World Cup | en:2025 FIFA Club World Cup (qualified teams) | 20 | modern | Brazil, United States, Germany, New Zealand, Tunisia | |
| gen196 | Name a player who scored for a non-European club at the 2025 FIFA Club World Cup | en:2025 FIFA Club World Cup Group A … en:2025 FIFA Club World Cup Group H; en:2025 FIFA Club World Cup knockout stage | 65 | modern | Lionel Messi, Marcos Leonardo, Kalidou Koulibaly, Germán Cano, Hércules | scorer's team outside UEFA; own goals excluded |
| gen197 | Name a head coach who led a club at the 2025 FIFA Club World Cup | en:2025 FIFA Club World Cup squads | 32 | modern | Xabi Alonso, Pep Guardiola, Javier Mascherano, Diego Simeone, Renato Paiva | "Manager:" line of each squad |
| gen161 | Name a club that played at a FIFA Club World Cup from 2000 to 2023 | en:FIFA Club World Cup (performances by club) | 70 | 2000s+ | Real Madrid, Barcelona, Corinthians, TP Mazembe, Al Ahly | excludes the 32-team 2025 edition |
| gen162 | Name a player who won the Golden, Silver or Bronze Ball at a FIFA Club World Cup | en:FIFA Club World Cup awards (Golden Ball) | 50 | 2000s+ | Messi, Cristiano Ronaldo, Luka Modrić, Cole Palmer, Gaku Shibasaki | |
| gen163 | Name a player who has scored in a FIFA Club World Cup final | en:List of FIFA Club World Cup finals | 35 | 2000s+ | Cole Palmer, Messi, Cristiano Ronaldo, Roberto Firmino, João Pedro | finals 2000–2025; own goals excluded |
| gen164 | Name a club that has played in a Copa Libertadores final since 2000 | en:List of Copa Libertadores finals | 30 | 2000s+ | Boca Juniors, River Plate, Flamengo, LDU Quito, Athletico Paranaense | winners and runners-up |
| gen165 | Name a player who has scored in a Copa Libertadores final since 2010 | en:2010 Copa Libertadores finals … en:2018 Copa Libertadores finals; en:2019 Copa Libertadores final … en:2025 Copa Libertadores final | 40 | modern | Gabriel Barbosa, Breno Lopes, Deyverson, John Kennedy, Germán Cano | two-legged finals to 2018 (plural titles), single-match from 2019 |
| gen166 | Name a club playing in the 2026 Brasileirão Série A | en:2026 Campeonato Brasileiro Série A (teams) | 20 | modern | Flamengo, Palmeiras, Corinthians, Mirassol | |
| gen167 | Name a club playing in Argentina's 2026 Liga Profesional | en:2026 AFA Liga Profesional de Fútbol (teams) | 30 | modern | Boca Juniors, River Plate, Racing Club, Independiente, Barracas Central | title redirects from "2026 Argentine Primera División" |

## Cross-league careers, titles and records

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| gen168 | Name a player who has played for both Juventus and Real Madrid | wd:pair(Juventus FC, Real Madrid CF) | 30 | 2000s+ | Cristiano Ronaldo, Zinedine Zidane, Fabio Cannavaro, Gonzalo Higuaín, Sami Khedira | |
| gen169 | Name a player who has played for both Bayern Munich and Real Madrid | wd:pair(FC Bayern Munich, Real Madrid CF) | 25 | 2000s+ | David Alaba, Toni Kroos, Arjen Robben, Xabi Alonso, Paul Breitner | |
| gen170 | Name a player who has played for both Bayern Munich and Juventus | wd:pair(FC Bayern Munich, Juventus FC) | 20 | 2000s+ | Arturo Vidal, Douglas Costa, Matthijs de Ligt, Kingsley Coman, Medhi Benatia | |
| gen198 | Name a player who has played for both Chelsea and AC Milan | wd:pair(Chelsea F.C., AC Milan) | 25 | 2000s+ | Andriy Shevchenko, Christian Pulisic, Olivier Giroud, Fikayo Tomori, Hernán Crespo | cross-league career |
| gen171 | Name a club that has won the league in England, Spain, Germany, Italy or France since 2015 | en:List of English football champions; en:List of Spanish football champions; en:List of German football champions; en:List of Italian football champions; en:List of French football champions | 16 | modern | Real Madrid, Bayern Munich, Bayer Leverkusen, Leicester City, Lille | seasons 2014–15 to 2025–26 |
| gen172 | Name a manager who won a league title in England, Spain, Germany, Italy or France since 2015 | the 2014–15 … 2025–26 season pages for the five leagues (champions), then the champion's club-season page for the manager | 30 | modern | Pep Guardiola, Jürgen Klopp, Claudio Ranieri, Xabi Alonso, Leonardo Jardim | manager in charge at season end; two-hop scrape (see Risky) |
| gen173 | Name a footballer who has scored 500 or more career goals | en:List of footballers with 500 or more goals | 40 | classic | Cristiano Ronaldo, Messi, Pelé, Robert Lewandowski, Josef Bican | main table (not the RSSSF list) |
| gen174 | Name a man who has made 1,000 or more official appearances | en:List of men's footballers with 1,000 or more official appearances | 40 | classic | Cristiano Ronaldo, Peter Shilton, Rogério Ceni, Gianluigi Buffon | title resolves via redirect from "List of footballers with the most official appearances" |

## Clubs, ownership and stadiums

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| gen175 | Name a club owned (now or before) by the City Football Group | en:City Football Group (CFG-owned clubs; former clubs) | 15 | modern | Manchester City, New York City FC, Girona, Palermo, Lommel SK | exclude the "partner clubs" section |
| gen176 | Name a football stadium with a capacity of 60,000 or more | en:List of association football stadiums by capacity | 55 | 2000s+ | Camp Nou, Wembley Stadium, Westfalenstadion, Rungrado 1st of May Stadium, Salt Lake Stadium | capacity column ≥ 60,000 |

## Video games and pop culture

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| gen177 | Name a footballer who has been a FIFA or EA Sports FC cover athlete (FIFA 15 onward) | en:FIFA (video game series) (games in the series, FIFA 15 to FIFA 23); en:EA Sports FC 24; en:EA Sports FC 25; en:EA Sports FC 26 | 45 | modern | Messi, Ronaldo, Mbappé, Marco Reus, Yann Sommer | "Cover athlete:" lines, regional covers included; exclude non-footballers |
| gen178 | Name a footballer who was a FIFA cover athlete from FIFA 2001 to FIFA 09 | en:FIFA (video game series) (FIFA 2001 to FIFA 09) | 50 | 2000s+ | Wayne Rooney, Ronaldinho, Thierry Henry, Kaká, Ebi Smolarek | regional covers included |
| gen179 | Name a Pro Evolution Soccer or eFootball cover star | en:Pro Evolution Soccer (series overview, "Cover athlete" lines) | 35 | 2000s+ | Messi, Cristiano Ronaldo, Neymar, Philippe Coutinho, Pierluigi Collina | referee Collina has an article; teams listed as covers are excluded |
| gen180 | Name a footballer (current or former) who is a Kings League team president | en:Kings League (teams organisation) | 25 | modern | Iker Casillas, Sergio Agüero, Lamine Yamal, Neymar, Hasan Salihamidžić | footballers only; streamers and musicians excluded |

## Summary

**Total: 200 prompts** (gen001–gen200). IDs gen181–gen200 were added in a second pass and sit inside their topical sections, so ids are not in order within each table.

### Era split
| era | count | share | target |
|---|---|---|---|
| modern | 131 | 65.5% | ≥ 60% |
| 2000s+ | 59 | 29.5% | ≤ 30% |
| classic | 10 | 5.0% | ≤ 10% |

### Count per sub-heading
| sub-heading | prompts |
|---|---|
| Ballon d'Or and global awards | 27 |
| Women's football | 4 |
| Bundesliga | 19 |
| Serie A | 23 |
| Ligue 1 | 20 |
| Netherlands, Portugal, Scotland and Turkey | 25 |
| MLS and North America | 19 |
| Saudi Pro League and Asia | 12 |
| Transfers and money | 4 |
| Europa League, Conference League and Super Cup | 20 |
| Club World Cup and South America | 13 |
| Cross-league careers, titles and records | 8 |
| Clubs, ownership and stadiums | 2 |
| Video games and pop culture | 4 |

### Template families (cap is about 10% = 20)
| family | count | ids |
|---|---|---|
| club-season squad ("made an appearance for X in season Y") | 20 (10.0%) | 030, 031, 047–051, 069–071, 087, 088, 095, 102, 108, 126–128, 151, 152 |
| Wikidata club pairs ("played for both X and Y") | 17 | 046, 066–068, 083–086, 093, 094, 101, 106, 168–170, 198 |
| competition-phase or final scorers | 14 | 043, 062, 119, 138, 144–146, 155, 158, 163, 165, 194–196 |
| current-season club lists | 10 | 042, 092, 098, 105, 123, 124, 149, 166, 167, 200 |
| stadiums | 10 | 041, 061, 080, 120, 153, 154, 159, 176, 187, 188 |
| Ballon d'Or nominee and ranking lists | 9 | 001–009 |
| nationality in a league | 9 | 035–038, 057, 058, 129, 130, 183 |
| hat-tricks | 8 | 032, 052, 076, 089, 115, 131, 142, 143 |
| season coaches | 6 | 040, 059, 078, 122, 132, 197 |
| season top-5 scorers | 6 | 034, 053, 077, 189–191 |
| promoted / relegated clubs | 6 | 039, 060, 079, 184–186 |
| club manager lists since 2000 | 6 | 063–065, 082, 099, 100 |

Answer types are mixed: players (most), clubs (about 35), managers (about 20), stadiums (10), countries (8) and transfers (4).

### Verification
- Every `en:` title (376 distinct after expanding season ranges) was checked with the Wikipedia query API in batches of 50 at about 1.6 requests per second. None is missing.
- Redirects to note:
  - `2020 Ballon d'Or` redirects to `Ballon d'Or`, because there was no 2020 edition. Skip it in the 2016–2025 ranges.
  - `2024–25` and `2025–26 UEFA Europa Conference League` redirect to `… UEFA Conference League`. gen148 names both forms.
  - `List of UEFA Cup and Europa League winning managers` resolves to the en-dash title used in gen139.
  - `2026 Argentine Primera División` resolves to `2026 AFA Liga Profesional de Fútbol`.
  - `List of footballers with the most official appearances` resolves to `List of men's footballers with 1,000 or more official appearances`.
- Titles that did not exist were replaced before writing:
  - "List of Saudi Arabian football transfers summer 2023": not used. Saudi signings are covered through season squads and the foreign-player lists.
  - "List of FIFA video game cover athletes": the "Cover athlete:" lines on `FIFA (video game series)` are used instead.
  - "UNFP Player of the Year": `Ligue 1 Player of the Year` is used instead.
  - "List of FC Bayern Munich managers", "List of Borussia Dortmund managers": not used, and those prompts were dropped.
  - "List of Serie A top scorers by season": season pages are used instead.
  - "2018 Copa Libertadores final": the two-legged title `2018 Copa Libertadores finals` is used.
- Counts were sampled from the live wikitext for the following, and estimates adjusted:
  - hat-trick lists (rows dated 2015 or later)
  - foreign-player lists (England, Japan, United States, Korea Republic and Morocco in the Bundesliga; England and Japan in Serie A; France and Portugal in the SPL)
  - the 2026 Ballon d'Or nominees, Kopa and Yashin lists
  - the top-50 transfers table (44 players)
  - the 2026–27 league team tables
  - knockout-phase scorer lists (2025 Club World Cup 37; 2024–25 ACL Elite 31; Europa and Conference League phases 85–100)
  - the Kings League chairpersons (about 25 footballers)
  - the City Football Group, Designated Player and UNFP goalkeeper lists
  - the unbeaten-seasons Europe section

### Risky prompts
- **Small, near 12:** gen159 (exactly 12 venues), gen200 (exactly 12 clubs), gen018 (13 countries), gen199 (13 keepers), gen056 (14). gen143 (about 18) is also on the small side.
- **Near the ceiling:** gen051 (about 110), gen024 (about 110), gen145 (about 100).
- **Hard scrapes:**
  - gen172 needs two hops (season champion, then the manager at season end).
  - gen078, gen122 and gen132 take coaches from personnel tables that are partly plain text, so names must be resolved to articles.
  - gen177–179 read cover athletes from prose "Cover athlete:" lines and must filter out teams and non-footballers.
  - gen180 needs a manual footballer-only filter, because many Kings League presidents are streamers with articles.
- **Thin common tier:** gen107 (unbeaten seasons, mostly small-league clubs), gen195 and gen146 (Conference League knockout scorers, many obscure), gen133 (Asian clubs).
- **Data completeness:**
  - The Wikidata pair prompts depend on P54 coverage, so their counts are estimates.
  - gen028 (women's transfers) may include players without enwiki articles. Drop those rows.
- **Shelf life:** the current-season prompts (gen041, 042, 061, 080, 092, 098, 105, 123, 124, 149, 166, 167, 187, 188, 200) and the 2026 Ballon d'Or prompts (gen001, 181) need a re-scrape or retirement each season.
- **Scope overlap:** gen145 (Manchester United/Tottenham Europa League run) and gen171/172 touch Premier League clubs, but they sit here because the competition or cross-league framing is General's.

## Build status

Built: **180** of 200 catalog prompts, each with 12–130 answers (`data/answers_raw/gen*.csv`).

### Dropped (20)
Not built because the source couldn't produce a clean answer list of 12–130 entries, unless a reason is given.

| id | catalog prompt | reason |
|---|---|---|
| gen046 | Name a player who has played for both RB Leipzig and Red Bull Salzburg | failed the scrape or quality check |
| gen066 | Name a player who has played for both Juventus and Inter | failed the scrape or quality check |
| gen067 | Name a player who has played for both Napoli and Juventus | failed the scrape or quality check |
| gen068 | Name a player who has played for both Roma and Lazio | failed the scrape or quality check |
| gen083 | Name a player who has played for both Marseille and Lyon | failed the scrape or quality check |
| gen084 | Name a player who has played for both PSG and Real Madrid | failed the scrape or quality check |
| gen085 | Name a player who has played for both PSG and Barcelona | failed the scrape or quality check |
| gen086 | Name a player who has played for both PSG and Inter | failed the scrape or quality check |
| gen093 | Name a player who has played for both Ajax and PSV | failed the scrape or quality check |
| gen094 | Name a player who has played for both Ajax and Barcelona | failed the scrape or quality check |
| gen101 | Name a player who has played for both Benfica and Porto | failed the scrape or quality check |
| gen106 | Name a player who has played for both Galatasaray and Fenerbahçe | failed the scrape or quality check |
| gen143 | Name a player who has scored a Conference League hat-trick | failed the scrape or quality check |
| gen168 | Name a player who has played for both Juventus and Real Madrid | failed the scrape or quality check |
| gen169 | Name a player who has played for both Bayern Munich and Real Madrid | failed the scrape or quality check |
| gen170 | Name a player who has played for both Bayern Munich and Juventus | failed the scrape or quality check |
| gen172 | Name a manager who won a league title in England, Spain, Germany, Italy or France since 2015 | season pages don't reliably name the champion's manager (e.g. 2014–15 Chelsea) |
| gen191 | Name a player who finished in the top 5 of the MLS scoring chart in a season since 2023 | failed the scrape or quality check |
| gen193 | Name a country with a player in the MLS Best XI since 2015 | failed the scrape or quality check |
| gen198 | Name a player who has played for both Chelsea and AC Milan | failed the scrape or quality check |

### Reworded (108)
Mostly tightened to match what the source supports.

| id | catalog wording | built wording |
|---|---|---|
| gen008 | Name a player on a FIFA Ballon d'Or shortlist (2010–2015) | Name a player on the FIFA Ballon d'Or shortlist between 2010 and 2015 |
| gen009 | Name a player who finished in the Ballon d'Or top 10 since 2010 | Name a player who finished in the Ballon d'Or top 10 in a year from 2010 to 2025 |
| gen010 | Name a club whose player won the Ballon d'Or (club at the time of the award) | Name a club whose player won the men's Ballon d'Or (the player's club at the time) |
| gen013 | Name a player who finished in the top 3 for the Kopa Trophy | Name a player who finished in the top 3 for the Kopa Trophy (2018–2025, men's) |
| gen014 | Name a goalkeeper who finished top 3 for the Yashin Trophy or won The Best FIFA Men's Goalkeeper | Name a goalkeeper who finished in the top 3 for the men's Yashin Trophy or The Best FIFA Men's Goalkeeper |
| gen015 | Name a player nominated for The Best FIFA Men's Player | Name a player nominated for The Best FIFA Men's Player (2016–2025) |
| gen016 | Name a coach who finished in the top 3 for The Best FIFA Men's Coach | Name a coach who finished in the top 3 for The Best FIFA Men's Coach (2016–2025) |
| gen017 | Name a goalscorer nominated for the FIFA Puskás Award since 2019 | Name a goalscorer nominated for the FIFA Puskás Award (2019–2025) |
| gen018 | Name a country with a FIFA Puskás Award winner | Name a country with a FIFA Puskás Award winner (2009–2025) |
| gen020 | Name a goalkeeper or defender named in a FIFPRO Men's World 11 | Name a goalkeeper or defender named in a FIFPRO Men's World 11 (2005–2025) |
| gen023 | Name a winner of the Golden Foot award | Name a winner of the Golden Foot award (men's, 2003–2025) |
| gen025 | Name a UEFA Jubilee "Golden Player" | Name a player in the top 50 of the UEFA Golden Jubilee Poll (2004) |
| gen026 | Name a woman who finished in the top 3 for the Ballon d'Or Féminin | Name a woman who finished in the top 3 for the Ballon d'Or Féminin (2018–2025) |
| gen027 | Name a player named in a FIFPRO Women's World 11 | Name a player named in a FIFPRO Women's World 11 (2015 onward) |
| gen028 | Name a player on the list of most expensive women's football transfers | Name a player on the list of the most expensive women's football transfers |
| gen029 | Name a club that has played in the NWSL | Name a club that has played in the NWSL (2013–2026, incl. former clubs) |
| gen031 | Name a player who made a Bundesliga appearance for Bayern Munich under Vincent Kompany (2024–25 or 2025–26) | Name a player who made a Bundesliga appearance for Bayern Munich in 2024–25 or 2025–26 |
| gen033 | Name a player who has been named in a Bundesliga Team of the Season | Name a player named in the Bundesliga Team of the Season (2017–18 to 2025–26) |
| gen034 | Name a player who finished in the top 5 of the Bundesliga scoring chart in a season since 2017–18 | Name a player who finished in the top 5 of the Bundesliga scoring chart in a season from 2017–18 to 2025–26 |
| gen039 | Name a club promoted to the Bundesliga since 2015 | Name a club promoted to the Bundesliga between 2015 and 2026 |
| gen041 | Name the home stadium of a 2026–27 Bundesliga club | Name the home stadium of a club in the 2026–27 Bundesliga |
| gen043 | Name a player who has scored in a DFB-Pokal final since 2010 | Name a player who has scored in a DFB-Pokal final from 2010 to 2026 (own goals and shoot-outs excluded) |
| gen048 | Name a player who made a Serie A appearance for Napoli in Antonio Conte's 2024–25 title season | Name a player who made a Serie A appearance for Napoli in their 2024–25 title season |
| gen049 | Name a player who made a Serie A appearance for Inter in their 2023–24 "second star" season | Name a player who made a Serie A appearance for Inter in their 2023–24 title season |
| gen051 | Name a player who made a Serie A appearance for Juventus during their nine-in-a-row (2011–12 to 2019–20) | Name a player who made a Serie A appearance for Juventus in a title season from 2011–12 to 2019–20 |
| gen053 | Name a player who finished in the top 5 of the Serie A scoring chart in a season since 2017–18 | Name a player who finished in the top 5 of the Serie A scoring chart in a season from 2017–18 to 2025–26 |
| gen054 | Name a player named in the Serie A Team of the Year since 2018–19 | Name a player named in the AIC Serie A Team of the Year (2018–19 to 2024–25) |
| gen055 | Name a winner of the Serie A Footballer of the Year / Most Valuable Player award | Name a winner of the Serie A Footballer of the Year (MVP) award |
| gen056 | Name a winner of the Serie A Young Footballer of the Year | Name a winner of the Serie A Young Footballer of the Year award |
| gen060 | Name a club relegated from Serie A since 2015 | Name a club relegated from Serie A between 2015–16 and 2025–26 |
| gen061 | Name the home stadium of a 2026–27 Serie A club | Name the home stadium of a club in the 2026–27 Serie A |
| gen062 | Name a player who has scored in a Coppa Italia final since 2010 | Name a player who has scored in a Coppa Italia final from 2010 to 2026 (own goals and shoot-outs excluded) |
| gen072 | Name a winner of the Ligue 1 Player of the Year award | Name a winner of the UNFP Ligue 1 Player of the Year award |
| gen073 | Name a winner of the Ligue 1 Young Player of the Year award | Name a winner of the UNFP Ligue 1 Young Player of the Year award |
| gen074 | Name a player named in the UNFP Ligue 1 Team of the Year since 2015–16 | Name a player named in the UNFP Ligue 1 Team of the Year (2015–16 to 2025–26) |
| gen075 | Name a winner of the UNFP Ligue 1 Player of the Month award since 2015 | Name a winner of the UNFP Ligue 1 Player of the Month award since August 2015 |
| gen077 | Name a player who finished in the top 5 of the Ligue 1 scoring chart in a season since 2017–18 | Name a player who finished in the top 5 of the Ligue 1 scoring chart in a season from 2017–18 to 2025–26 |
| gen079 | Name a club promoted to Ligue 1 since 2015 | Name a club promoted to Ligue 1 between 2015 and 2026 |
| gen080 | Name the home stadium of a 2026–27 Ligue 1 club | Name the home stadium of a club in the 2026–27 Ligue 1 |
| gen090 | Name a player who finished as Eredivisie top scorer in a season since 2005–06 | Name a player who finished as Eredivisie top scorer in a season from 2005–06 to 2025–26 |
| gen091 | Name a winner of the Eredivisie Player of the Month award | Name a winner of the Eredivisie Player of the Month award (2017–18 onward) |
| gen095 | Name a player who made a Primeira Liga appearance for Sporting CP in their 2020–21 title season | Name a player in Sporting CP's first-team squad in their 2020–21 title season |
| gen096 | Name a player who finished as Primeira Liga top scorer in a season since 2000 | Name a player who finished as Primeira Liga top scorer in a season from 2000–01 to 2025–26 |
| gen097 | Name a winner of the LPFP Primeira Liga Player of the Year | Name a winner of the LPFP Primeira Liga Player of the Year award |
| gen102 | Name a player who made a Premiership appearance for Celtic in their 2016–17 invincible treble season | Name a player who made a Scottish Premiership appearance for Celtic in their 2016–17 invincible season |
| gen103 | Name a club that has played in the Scottish Premiership (2013–present) | Name a club that has played in the Scottish Premiership (2013–14 to 2026–27) |
| gen104 | Name a player who finished as Süper Lig top scorer in a season since 2000 | Name a player who finished as Süper Lig top scorer in a season from 2000–01 to 2025–26 |
| gen107 | Name a European club that went a whole top-flight league season unbeaten | Name a European club that went a whole top-flight league season unbeaten (men's) |
| gen108 | Name a player who has played for Inter Miami in the Messi era (2023 onward) | Name a player who has played for Inter Miami since the start of 2023 (the Messi era) |
| gen111 | Name a winner of the MLS MVP award | Name a winner of the MLS MVP award (1996–2025) |
| gen112 | Name a winner of the MLS Golden Boot | Name a winner of the MLS Golden Boot (1996–2025) |
| gen115 | Name a player who has scored an MLS hat-trick since 2015 | Name a player who has scored an MLS hat-trick since the start of 2015 (regular season or playoffs) |
| gen116 | Name a player who has scored 100+ MLS goals | Name a player who has scored 100 or more MLS regular-season goals |
| gen117 | Name a player who has played 400+ MLS games | Name a player who has made 400 or more MLS regular-season appearances |
| gen118 | Name a club that has won the MLS Cup | Name a club that has won the MLS Cup (1996–2025) |
| gen119 | Name a player who has scored in an MLS Cup final since 2010 | Name a player who has scored in an MLS Cup final from 2010 to 2025 (own goals and shoot-outs excluded) |
| gen121 | Name a club that played the MLS All-Stars in an All-Star Game | Name a club that has played the MLS All-Stars in an MLS All-Star Game |
| gen122 | Name a head coach of an MLS club in the 2026 season | Name a head coach who managed an MLS club in the 2026 season (to October 2026) |
| gen123 | Name a club playing in Liga MX in 2026–27 | Name a club playing in the 2026–27 Liga MX season |
| gen125 | Name a player who finished as Saudi Pro League top scorer in a season | Name a player who finished as top scorer of a Saudi top-flight season |
| gen126 | Name a player who made a league appearance for Al-Nassr in 2023–24 | Name a player who made a Saudi Pro League appearance for Al-Nassr in 2023–24 |
| gen127 | Name a player who made a league appearance for Al-Hilal in their record-breaking 2023–24 season | Name a player who made a Saudi Pro League appearance for Al-Hilal in their record-breaking 2023–24 season |
| gen128 | Name a player who made a league appearance for Al-Ittihad in their 2024–25 title season | Name a player who made a Saudi Pro League appearance for Al-Ittihad in their 2024–25 title season |
| gen131 | Name a player who has scored a Saudi Pro League hat-trick since 2023–24 | Name a player who has scored a Saudi Pro League hat-trick since the start of 2023–24 |
| gen132 | Name a head coach who managed a Saudi Pro League club from 2023–24 to 2025–26 | Name a head coach who managed a Saudi Pro League club between 2023–24 and 2025–26 |
| gen133 | Name a club in the 2025–26 AFC Champions League Elite | Name a club in the league stage of the 2025–26 AFC Champions League Elite |
| gen136 | Name the nationality of a player in the 50 most expensive transfers | Name a country whose players appear in the 50 most expensive football transfers |
| gen137 | Name a club that has paid a world-record transfer fee | Name a club that has paid a world-record transfer fee (1893 onward) |
| gen138 | Name a player who has scored in a Europa League final since 2010 | Name a player who has scored in a UEFA Europa League final from 2010 to 2026 (own goals and shoot-outs excluded) |
| gen140 | Name a player who finished as Europa League top scorer in a season since 2009–10 | Name a player who finished as top scorer of a UEFA Cup / Europa League season from 2009–10 to 2025–26 |
| gen141 | Name a player in the all-time UEFA Cup / Europa League top scorers table | Name a player in the all-time UEFA Cup / Europa League top scorers table (group or league phase to final) |
| gen142 | Name a player who has scored a Europa League hat-trick since 2015–16 | Name a player who has scored a UEFA Europa League hat-trick since 2015–16 |
| gen144 | Name a player who scored in the 2025–26 Europa League knockout phase | Name a player who scored in the 2025–26 UEFA Europa League knockout phase (own goals and shoot-outs excluded) |
| gen145 | Name a player who scored in the 2024–25 Europa League knockout phase | Name a player who scored in the 2024–25 UEFA Europa League knockout phase (own goals and shoot-outs excluded) |
| gen146 | Name a player who scored in the 2025–26 Conference League knockout phase | Name a player who scored in the 2025–26 UEFA Conference League knockout phase (own goals and shoot-outs excluded) |
| gen147 | Name a club that reached a Europa League semi-final since 2015–16 | Name a club that reached a UEFA Europa League semi-final from 2015–16 to 2025–26 |
| gen148 | Name a club that reached a Conference League semi-final | Name a club that reached a UEFA Conference League semi-final (2021–22 to 2025–26) |
| gen149 | Name a club in the 2026–27 Europa League league phase | Name a club in the 2026–27 UEFA Europa League league phase |
| gen150 | Name a country with a club in the 2026–27 Conference League league phase | Name a country with a club in the 2026–27 UEFA Conference League league phase |
| gen151 | Name a player who made a Europa League appearance for Atalanta in their 2023–24 winning run | Name a player who made a UEFA Europa League appearance for Atalanta in their 2023–24 winning run |
| gen152 | Name a player who made a Europa League appearance for Eintracht Frankfurt in their 2021–22 winning run | Name a player who made a UEFA Europa League appearance for Eintracht Frankfurt in their 2021–22 winning run |
| gen155 | Name a player who has scored in a UEFA Super Cup since 2010 | Name a player who has scored in a UEFA Super Cup from 2010 to 2026 (own goals and shoot-outs excluded) |
| gen158 | Name a player who scored in the 2025 Club World Cup knockout stage | Name a player who scored in the 2025 FIFA Club World Cup knockout stage (own goals and shoot-outs excluded) |
| gen159 | Name a stadium that hosted a 2025 Club World Cup match | Name a stadium that hosted a 2025 FIFA Club World Cup match |
| gen161 | Name a club that played at a FIFA Club World Cup from 2000 to 2023 | Name a club that played at the FIFA Club World Cup / Club World Championship from 2000 to 2023 |
| gen162 | Name a player who won the Golden, Silver or Bronze Ball at a FIFA Club World Cup | Name a player who won the Golden Ball, Silver Ball or Bronze Ball at a FIFA Club World Cup (2000–2025) |
| gen163 | Name a player who has scored in a FIFA Club World Cup final | Name a player who has scored in a FIFA Club World Cup final (2000–2025; own goals and shoot-outs excluded) |
| gen165 | Name a player who has scored in a Copa Libertadores final since 2010 | Name a player who has scored in a Copa Libertadores final from 2010 to 2025 (own goals and shoot-outs excluded) |
| gen166 | Name a club playing in the 2026 Brasileirão Série A | Name a club playing in the 2026 Campeonato Brasileiro Série A |
| gen171 | Name a club that has won the league in England, Spain, Germany, Italy or France since 2015 | Name a club that has won the league title in England, Spain, Germany, Italy or France between 2014–15 and 2025–26 |
| gen174 | Name a man who has made 1,000 or more official appearances | Name a men's footballer who has made 1,000 or more official appearances |
| gen175 | Name a club owned (now or before) by the City Football Group | Name a club that the City Football Group owns or has owned |
| gen177 | Name a footballer who has been a FIFA or EA Sports FC cover athlete (FIFA 15 onward) | Name a footballer who has been a FIFA or EA Sports FC cover athlete (FIFA 15 to EA Sports FC 26) |
| gen179 | Name a Pro Evolution Soccer or eFootball cover star | Name a person who has been a Pro Evolution Soccer / eFootball PES cover star |
| gen180 | Name a footballer (current or former) who is a Kings League team president | Name a footballer (current or former) who is or was a Kings League team chairperson |
| gen181 | Name a player nominated for the 2026 Kopa Trophy or the 2026 Yashin Trophy (men) | Name a player nominated for the men's Kopa Trophy or Yashin Trophy in 2026 |
| gen182 | Name a winner of the FIFA Puskás Award | Name a winner of the FIFA Puskás Award (2009–2025) |
| gen184 | Name a club relegated from the Bundesliga since 2015 | Name a club relegated from the Bundesliga between 2015–16 and 2025–26 |
| gen185 | Name a club promoted to Serie A since 2015 | Name a club promoted to Serie A between 2015 and 2026 |
| gen186 | Name a club relegated from Ligue 1 since 2015 | Name a club relegated from Ligue 1 between 2015–16 and 2025–26 |
| gen187 | Name the home stadium of a 2026–27 Eredivisie club | Name the home stadium of a club in the 2026–27 Eredivisie |
| gen188 | Name the home stadium of a 2026–27 Primeira Liga club | Name the home stadium of a club in the 2026–27 Primeira Liga |
| gen189 | Name a player who finished in the top 5 of the Eredivisie scoring chart in a season since 2020–21 | Name a player who finished in the top 5 of the Eredivisie scoring chart in a season from 2020–21 to 2025–26 |
| gen190 | Name a player who finished in the top 5 of the Saudi Pro League scoring chart since 2023–24 | Name a player who finished in the top 10 of the Saudi Pro League scoring chart in a season from 2023–24 to 2025–26 |
| gen192 | Name a player in either squad for the 2025 MLS All-Star Game | Name a player in either squad for the 2025 MLS All-Star Game (MLS All-Stars or Liga MX All-Stars) |
| gen194 | Name a player who scored in the 2024–25 AFC Champions League Elite knockout stage | Name a player who scored in the 2024–25 AFC Champions League Elite knockout stage (own goals excluded) |
| gen195 | Name a player who scored in the 2024–25 Conference League knockout phase | Name a player who scored in the 2024–25 UEFA Conference League knockout phase (own goals and shoot-outs excluded) |
| gen196 | Name a player who scored for a non-European club at the 2025 FIFA Club World Cup | Name a player who scored for a non-European club at the 2025 FIFA Club World Cup (own goals excluded) |
