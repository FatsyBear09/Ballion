# La Liga / Spanish football prompt catalog (`ll`)

Theme scope: La Liga, Segunda División, Copa del Rey, Supercopa de España, Spanish clubs and their players/managers, El Clásico, Pichichi/Zamora-style awards, Liga F. Cross-league careers, Ballon d'Or-type awards, national teams and Champions League content are left to other themes (Spanish clubs' Europa/Conference League finals are kept here as club-season stories).

Conventions:
- Every source title below was verified to exist on en.wikipedia via the API (redirects resolved; canonical titles are used). `§` = section of that page. "Season pages" = the per-season articles named in the cell (e.g. `2015–16 La Liga` … `2025–26 La Liga`), all verified.
- "Category ∩" sources = intersection of two en.wikipedia categories (members in main namespace); counts below were computed from the live category members.
- Estimates were sanity-checked by fetching and parsing the source wikitext for most prompts (marked `checked` in notes). Unchecked ones are rough.
- Wikipedia data is current to roughly September 2026 (2026–27 season pages exist).

## Goals & scoring records

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ll001 | Name a player who has scored 100+ La Liga goals | en:List of La Liga top scorers §La Liga players with 100 or more goals | 84 | classic | Lionel Messi, Cristiano Ronaldo, Karim Benzema, Iago Aspas, Pahiño | checked (84 rows) |
| ll002 | Name a player who has scored 100+ La Liga goals and was still playing in La Liga in 2010 or later | en:List of La Liga top scorers §La Liga players with 100 or more goals | 19 | 2000s+ | Messi, Antoine Griezmann, Iago Aspas, Cristhian Stuani, Álvaro Negredo | checked; filter "Last" column ≥ 2010 |
| ll003 | Name a player who finished in La Liga's top-10 scorers in any season since 2015–16 | Season pages 2015–16 La Liga … 2025–26 La Liga §Top goalscorers | 62 | modern | Robert Lewandowski, Kylian Mbappé, Ante Budimir, Jaime Mata, Thierno Barry | checked; ties at 10th included as listed |
| ll004 | Name a player who finished in La Liga's top-10 scorers in a season from 2009–10 to 2014–15 | Season pages 2009–10 La Liga … 2014–15 La Liga §Top goalscorers | 40 | 2000s+ | Messi, Cristiano Ronaldo, Radamel Falcao, Gonzalo Higuaín, Roberto Soldado | checked (36 parsed) |
| ll005 | Name a player who finished in La Liga's top-10 scorers in a season from 2000–01 to 2008–09 | Season pages 2000–01 La Liga … 2008–09 La Liga §Top goalscorers / Pichichi table | 45 | 2000s+ | Raúl, Samuel Eto'o, David Villa, Diego Forlán, Diego Tristán | checked (38 parsed); some early pages list only top 5–8 |
| ll006 | Name a player who scored 20+ La Liga goals in a single season since 2010–11 | Season pages 2010–11 La Liga … 2025–26 La Liga §Top goalscorers | 24 | modern | Messi, Lewandowski, Ante Budimir, Artem Dovbyk, Vedat Muriqi | checked |
| ll007 | Name a player who has scored a La Liga hat-trick since 2015–16 | en:List of La Liga hat-tricks §Hat-tricks | 67 | modern | Cristiano Ronaldo, Lewandowski, Mbappé, Taty Castellanos, Lucas Boyé | checked; matches dated ≥ 2015-08-01 |
| ll008 | Name a player who has scored a La Liga hat-trick since 2015–16 for a club other than Real Madrid, Barcelona or Atlético | en:List of La Liga hat-tricks §Hat-tricks | 47 | modern | Iago Aspas, Gerard Moreno, Artem Dovbyk, Michael Olunga, Pere Milla | checked; "For" column filter |
| ll009 | Name a player who scored a La Liga hat-trick between 2004–05 and 2014–15 | en:List of La Liga hat-tricks §Hat-tricks | 60 | 2000s+ | Messi, Ronaldo, Falcao, Frédéric Kanouté, Juan Román Riquelme | checked |
| ll010 | Name a player who has scored 4 or more goals in a single La Liga match since 2000 | en:List of La Liga hat-tricks §Hat-tricks (superscript 4/5) | 22 | 2000s+ | Messi, Ronaldo, Luis Suárez, Alexander Sørloth, Santi Mina | checked |
| ll011 | Name a player who finished in La Liga's top-10 assist providers in a season from 2015–16 to 2023–24 | Season pages 2015–16 La Liga … 2023–24 La Liga §Top assists | 71 | modern | Messi, Toni Kroos, Dani Parejo, Nico Williams, Brian Oliván | checked; later pages have no assists table |
| ll012 | Name a club Lionel Messi scored a La Liga hat-trick against | en:List of La Liga hat-tricks §Hat-tricks (rows for Messi, "Against" column) | 19 | 2000s+ | Real Madrid, Valencia, Sevilla, Osasuna, CD Tenerife | checked; answers are clubs |
| ll013 | Name a club Cristiano Ronaldo scored a La Liga hat-trick against | en:List of La Liga hat-tricks §Hat-tricks (rows for Ronaldo) | 20 | 2000s+ | Atlético Madrid, Sevilla, Getafe, Girona, Racing de Santander | checked; answers are clubs |
| ll014 | Name a club that has conceded a La Liga hat-trick since 2015–16 | en:List of La Liga hat-tricks §Hat-tricks ("Against" column) | 30 | modern | Barcelona, Real Madrid, Granada, Racing de Santander, SD Huesca | checked; answers are clubs |
| ll015 | Name a player who has made 400+ La Liga appearances | en:List of footballers with 400 or more La Liga appearances | 88 | 2000s+ | Joaquín, Raúl García, Antoine Griezmann, Dani Parejo, Andoni Zubizarreta | checked (as of Sep 2026) |
| ll016 | Name a player who finished in the Segunda División top-10 scorers in a season since 2019–20 | Season pages 2019–20 Segunda División … 2025–26 Segunda División §Top goalscorers | 54 | modern | Darwin Núñez, Cristhian Stuani, Javi Puado, Borja Bastón, Curro Sánchez | checked |
| ll017 | Name a player listed among the Copa del Rey top scorers in a season since 2022–23 | Season pages 2022–23 Copa del Rey … 2025–26 Copa del Rey §Top scorers | 55 | modern | Vinícius Júnior, Ferran Torres, Endrick, Julián Alvarez, Sergio Castel | partly checked (2019–26 union = 104, so cut to 2022+); ties make tables long |

## El Clásico & the big two

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ll018 | Name a player who has scored in El Clásico since 2015–16 | en:List of El Clásico matches (all competition tables) | 40 | modern | Messi, Karim Benzema, Vinícius Júnior, Fermín López, Franck Kessié | checked; own goals excluded |
| ll019 | Name a player who has scored a hat-trick in El Clásico | en:El Clásico §Hat-tricks | 25 | classic | Messi, Kylian Mbappé, Romário, Iván Zamorano, Paulino Alcántara | page states 25 players |
| ll020 | Name a player in El Clásico's all-time top goalscorers table | en:El Clásico §Top goalscorers | 20 | classic | Messi, Cristiano Ronaldo, Benzema, Raúl, Ferenc Puskás | checked |
| ll021 | Name a player who appeared in a Supercopa de España final between Real Madrid and Barcelona (2023–2026) | en:2023 Supercopa de España final, en:2024 Supercopa de España final, en:2025 Supercopa de España final, en:2026 Supercopa de España final (line-ups) | 60 | modern | Vinícius Júnior, Robert Lewandowski, Gavi, Lamine Yamal, Gonzalo García | starters + used subs; Saudi-hosted finals |
| ll022 | Name a player in Real Madrid's or Barcelona's all-time top-20 appearance makers | en:List of Real Madrid CF records and statistics §Most appearances; en:List of FC Barcelona records and statistics §Most appearances | 40 | 2000s+ | Messi, Iker Casillas, Xavi, Sergio Busquets, Manolo Sanchís | top-20 cut per club |
| ll023 | Name a player in Real Madrid's or Barcelona's all-time top-20 goalscorers | en:List of Real Madrid CF records and statistics §Most goals; en:List of FC Barcelona records and statistics §Top goalscorers | 40 | classic | Cristiano Ronaldo, Messi, Raúl, Luis Suárez, César Rodríguez | top-20 cut per club |

## Awards & trophies

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ll024 | Name a winner of the La Liga Player of the Month award | en:La Liga Player of the Month §Winners | 70 | modern | Messi, Jude Bellingham, Gabri Veiga, Jon Ander Serantes, Carlos Espí | checked (≈70 players after removing club links); started 2013 |
| ll025 | Name a winner of the La Liga Manager of the Month award | en:La Liga Manager of the Month §Winners | 40 | modern | Diego Simeone, Hansi Flick, Míchel, Iñigo Pérez, José Ramón Sandoval | checked |
| ll026 | Name a winner of the La Liga U23 Player of the Month award | en:La Liga U23 Player of the Month §Winners | 22 | modern | Lamine Yamal, Pedri, Arda Güler, Pau Cubarsí, Williot Swedberg | checked; started 2023–24 |
| ll027 | Name a winner of the La Liga Goal of the Month award | en:La Liga Goal of the Month §Winners | 35 | modern | Vinícius Júnior, Lamine Yamal, Nico Williams, Luka Sučić, Largie Ramazani | checked; started 2023–24 |
| ll028 | Name a player named in a La Liga Team of the Season | en:La Liga Awards §Team of the season | 70 | modern | Lamine Yamal, Luka Modrić, Jan Oblak, Daniel Vivian, Santiago Mouriño | checked; covers 2013–14 onward |
| ll029 | Name a winner of a La Liga season award (Player, Manager, African Player, U23 Player, Goal or Save of the Season) | en:La Liga Awards §Annual awards (all sub-sections) | 40 | modern | Raphinha, Hansi Flick, Lamine Yamal, Jan Oblak, Luka Sučić | 2008–09 onward; union of sub-tables |
| ll030 | Name a winner of a discontinued LFP award (Best Forward, Midfielder, Attacking Midfielder, Defender, Goalkeeper, Breakthrough or Best American Player) | en:La Liga Awards §Discontinued awards | 30 | 2000s+ | Messi, Cristiano Ronaldo, Iker Casillas, Isco, Sergio Busquets | 2008–09 to 2014–15 |
| ll031 | Name a Ricardo Zamora Trophy winner (La Liga) | en:Ricardo Zamora Trophy §Primera División | 60 | classic | Jan Oblak, Thibaut Courtois, Víctor Valdés, Joan García, Andoni Zubizarreta | checked |
| ll032 | Name a goalkeeper who finished in the top five of La Liga's Zamora Trophy standings since 2015–16 | Season pages 2015–16 La Liga … 2025–26 La Liga §Zamora Trophy | 25 | modern | Jan Oblak, Marc-André ter Stegen, Yassine Bounou, Dominik Greif, Iago Herrerín | checked |
| ll033 | Name a winner of the Zarra Trophy (top Spanish scorer in La Liga or Segunda División) | en:Zarra Trophy §La Liga, §Segunda División | 30 | modern | David Villa, Iago Aspas, Lamine Yamal, Borja Bastón, Stoichkov (Spanish footballer) | checked; awarded since 2005–06 |
| ll034 | Name a winner of MARCA's Miguel Muñoz Trophy (La Liga coach of the season) | en:Miguel Muñoz Trophy §La Liga | 17 | 2000s+ | Pep Guardiola, José Mourinho, Diego Simeone, Míchel, Asier Garitano | checked |
| ll035 | Name a winner of MARCA's Trofeo Alfredo Di Stéfano (La Liga best player) | en:Trofeo Alfredo Di Stéfano | 16 | 2000s+ | Messi, Cristiano Ronaldo, Jude Bellingham, Lamine Yamal, Diego Forlán | checked |
| ll036 | Name a winner of the Don Balón Award | en:Don Balón Award | 60 | classic | Messi, Iker Casillas, Raúl, Michael Laudrup, Julen Guerrero | 1976–2010; count player and coach categories only (page also lists referees) |
| ll037 | Name a winner of the Trofeo EFE (best Ibero-American player in La Liga) | en:Trofeo EFE | 28 | classic | Messi, Cristiano Ronaldo, Ronaldinho, Fernando Redondo, Rommel Fernández | checked; 1990–91 onward, women's winners added since 2019–20 (Linda Caicedo) |
| ll038 | Name a club whose player has won La Liga Player of the Month | en:La Liga Player of the Month §Awards won by club | 25 | modern | Real Madrid, Barcelona, Villarreal, Getafe, SD Eibar | answers are clubs |
| ll039 | Name a country whose player has won La Liga Player of the Month | en:La Liga Player of the Month §Awards won by nationality | 22 | modern | Argentina, Brazil, Norway, Ukraine, Kosovo | answers are national teams/countries |
| ll188 | Name a winner of the Segunda División Player of the Month award | en:Segunda División Player of the Month §Winners | 100 | modern | Borja Iglesias, Ayoze Pérez, Asier Villalibre, Achille Emaná, Chupete | checked (≈100 players after removing club links) |

## Season squads (title winners & famous runs)

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ll040 | Name a player in a Real Madrid La Liga title-winning squad since 2016–17 (2016–17, 2019–20, 2021–22, 2023–24) | en:2016–17 Real Madrid CF season, en:2019–20 Real Madrid CF season, en:2021–22 Real Madrid CF season, en:2023–24 Real Madrid CF season §Players | 47 | modern | Karim Benzema, Luka Modrić, Jude Bellingham, Joselu, Mariano Díaz | checked (union of first-team squad tables) |
| ll041 | Name a player in Real Madrid's 2024–25 first-team squad | en:2024–25 Real Madrid CF season §Players | 25 | modern | Kylian Mbappé, Vinícius Júnior, Endrick, Arda Güler, Fran García | checked |
| ll042 | Name a player in a Barcelona La Liga title-winning squad from 2014–15 to 2018–19 | en:2014–15 FC Barcelona season, en:2015–16 FC Barcelona season, en:2017–18 FC Barcelona season, en:2018–19 FC Barcelona season §Players | 70 | modern | Messi, Neymar, Luis Suárez, Paulinho, Douglas (footballer, born 1990) | squads 31–37 each incl. B-team call-ups; first-team table only |
| ll043 | Name a player in Barcelona's 2024–25 first-team squad | en:2024–25 FC Barcelona season §Players | 23 | modern | Lamine Yamal, Raphinha, Pedri, Pau Cubarsí, Marc Casadó | checked |
| ll044 | Name a player in a Barcelona squad under Pep Guardiola (2008–09 to 2011–12) | en:2008–09 FC Barcelona season … en:2011–12 FC Barcelona season §Players | 38 | 2000s+ | Messi, Xavi, Zlatan Ibrahimović, Aliaksandr Hleb, Ibrahim Afellay | checked |
| ll045 | Name a player in an Atlético Madrid La Liga title-winning squad (2013–14 or 2020–21) | en:2013–14 Atlético Madrid season, en:2020–21 Atlético Madrid season §Players | 42 | modern | Diego Godín, Koke, Luis Suárez, Diego Costa, Toby Alderweireld | checked |
| ll046 | Name a player in Atlético Madrid's 2024–25 first-team squad | en:2024–25 Atlético Madrid season §Players | 25 | modern | Julián Alvarez, Antoine Griezmann, Alexander Sørloth, Conor Gallagher, Robin Le Normand | |
| ll047 | Name a player in Girona's 2023–24 squad (third place, first Champions League qualification) | en:2023–24 Girona FC season §First-team squad | 23 | modern | Artem Dovbyk, Savinho, Aleix García, Iván Martín, Portu | checked |
| ll048 | Name a player in Villarreal's 2020–21 squad (Europa League winners) | en:2020–21 Villarreal CF season §Players | 25 | modern | Gerard Moreno, Pau Torres, Dani Parejo, Gerónimo Rulli, Paco Alcácer | squad table (wikitable) |
| ll049 | Name a player in Sevilla's 2019–20 squad (Europa League winners) | en:2019–20 Sevilla FC season §Players | 21 | modern | Jesús Navas, Lucas Ocampos, Jules Koundé, Sergio Reguilón, Yassine Bounou | checked |
| ll050 | Name a player in Sevilla's 2022–23 squad (seventh Europa League title) | en:2022–23 Sevilla FC season §Players | 25 | modern | Ivan Rakitić, Youssef En-Nesyri, Yassine Bounou, Erik Lamela, Suso | checked |
| ll051 | Name a player in Real Betis's 2021–22 squad (Copa del Rey winners) | en:2021–22 Real Betis season §Players | 27 | modern | Nabil Fekir, Sergio Canales, Borja Iglesias, Joaquín, Juan Miranda | checked |
| ll052 | Name a player in Athletic Bilbao's 2023–24 squad (Copa del Rey winners) | en:2023–24 Athletic Bilbao season §Players | 26 | modern | Nico Williams, Iñaki Williams, Oihan Sancet, Unai Simón, Raúl García | checked |
| ll053 | Name a player who has been in Athletic Bilbao's first-team squad since 2020–21 | Season pages 2020–21 Athletic Bilbao season … 2025–26 Athletic Bilbao season §Players | 50 | modern | Nico Williams, Iñaki Williams, Oihan Sancet, Gorka Guruzeta, Asier Villalibre | rough; earlier season pages parse thinly |
| ll054 | Name a player in Real Sociedad's 2022–23 squad (fourth place) | en:2022–23 Real Sociedad season §Players | 26 | modern | Takefusa Kubo, Mikel Merino, Mikel Oyarzabal, Brais Méndez, Alexander Sørloth | checked |
| ll055 | Name a player in Real Sociedad's 2019–20 squad (Copa del Rey winners) | en:2019–20 Real Sociedad season §Players | 23 | modern | Martin Ødegaard, Alexander Isak, Mikel Oyarzabal, Portu, Willian José | checked |
| ll056 | Name a player in Valencia's 2018–19 squad (Copa del Rey winners) | en:2018–19 Valencia CF season §Players | 25 | modern | Rodrigo, Dani Parejo, José Gayà, Carlos Soler, Kevin Gameiro | |
| ll057 | Name a player in a Barcelona squad under Xavi (2021–22 to 2023–24) | en:2021–22 FC Barcelona season, en:2022–23 FC Barcelona season, en:2023–24 FC Barcelona season §Players | 55 | modern | Lewandowski, Gavi, Pedri, İlkay Gündoğan, Pierre-Emerick Aubameyang | union |

## Club goalscorers by season

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ll058 | Name a player who scored for Real Madrid in 2016–17 (any competition) | en:2016–17 Real Madrid CF season §Goals | 21 | modern | Cristiano Ronaldo, Álvaro Morata, Isco, Marco Asensio, Mariano Díaz | checked |
| ll059 | Name a player who scored for Real Madrid in 2024–25 (any competition) | en:2024–25 Real Madrid CF season §Goals | 18 | modern | Mbappé, Vinícius Júnior, Bellingham, Arda Güler, Brahim Díaz | checked |
| ll060 | Name a player who scored for Real Madrid in 2025–26 (any competition) | en:2025–26 Real Madrid CF season §Goals | 17 | modern | Mbappé, Vinícius Júnior, Arda Güler, Franco Mastantuono, Gonzalo García | checked |
| ll061 | Name a player who scored for Barcelona in 2024–25 (any competition) | en:2024–25 FC Barcelona season §Goalscorers | 20 | modern | Lewandowski, Raphinha, Lamine Yamal, Fermín López, Pau Víctor | |
| ll062 | Name a player who scored for Barcelona in 2025–26 (any competition) | en:2025–26 FC Barcelona season §Goalscorers | 20 | modern | Raphinha, Lewandowski, Lamine Yamal, Ferran Torres, Marcus Rashford | |
| ll063 | Name a player who scored for Atlético Madrid in 2020–21 (any competition) | en:2020–21 Atlético Madrid season §Goalscorers | 16 | modern | Luis Suárez, Ángel Correa, Marcos Llorente, João Félix, Yannick Carrasco | checked |
| ll064 | Name a player who scored for Villarreal in 2024–25 (any competition) | en:2024–25 Villarreal CF season §Goalscorers | 17 | modern | Ayoze Pérez, Álex Baena, Nicolas Pépé, Thierno Barry, Gerard Moreno | checked |
| ll065 | Name a player who scored for Real Sociedad in 2022–23 (any competition) | en:2022–23 Real Sociedad season §Goalscorers | 15 | modern | Takefusa Kubo, Alexander Sørloth, Brais Méndez, Umar Sadiq, Mikel Oyarzabal | goalscorer table only partly linked; risky |
| ll066 | Name a player who scored for Real Betis in 2024–25 (any competition) | en:2024–25 Real Betis season §Goalscorers | 18 | modern | Isco, Antony, Cédric Bakambu, Vitor Roque, Abde Ezzalzouli | |
| ll067 | Name a player who scored for Girona in 2023–24 (any competition) | en:2023–24 Girona FC season §Squad statistics (goals column) | 16 | modern | Artem Dovbyk, Cristhian Stuani, Savinho, Viktor Tsyhankov, Iván Martín | goals > 0 in stats table |
| ll196 | Name a player who scored for Real Madrid in 2021–22 (any competition) | en:2021–22 Real Madrid CF season §Goals | 20 | modern | Karim Benzema, Vinícius Júnior, Rodrygo, Luka Modrić, Luka Jović | checked |
| ll197 | Name a player who scored for Barcelona in 2014–15 (any competition, the MSN treble season) | en:2014–15 FC Barcelona season §Squad, appearances and goals (goals > 0) | 20 | modern | Messi, Neymar, Luis Suárez, Ivan Rakitić, Munir El Haddadi | Efs table |
| ll192 | Name a player who scored for Atlético Madrid in 2024–25 (any competition) | en:2024–25 Atlético Madrid season §Goalscorers | 18 | modern | Julián Alvarez, Antoine Griezmann, Alexander Sørloth, Conor Gallagher, Giuliano Simeone | |
| ll193 | Name a player who scored for Athletic Bilbao in 2024–25 (any competition) | en:2024–25 Athletic Bilbao season §Appearances and goals (goals > 0) | 18 | modern | Nico Williams, Iñaki Williams, Oihan Sancet, Gorka Guruzeta, Maroan Sannadi | Efs table |

## Cup finals

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ll068 | Name a player who appeared in the 2020 Copa del Rey final (Real Sociedad v Athletic, played 2021) | en:2020 Copa del Rey final §Details | 30 | modern | Mikel Oyarzabal, Alexander Isak, Iñaki Williams, Iker Muniain, Robin Le Normand | starters + used subs |
| ll069 | Name a player who appeared in the 2021 Copa del Rey final (Barcelona v Athletic) | en:2021 Copa del Rey final §Details | 30 | modern | Messi, Antoine Griezmann, Frenkie de Jong, Unai Simón, Óscar de Marcos | starters + used subs |
| ll070 | Name a player who appeared in the 2022 Copa del Rey final (Real Betis v Valencia) | en:2022 Copa del Rey final §Details | 32 | modern | Borja Iglesias, Nabil Fekir, Hugo Duro, José Gayà, Juan Miranda | checked |
| ll071 | Name a player who appeared in the 2023 Copa del Rey final (Real Madrid v Osasuna) | en:2023 Copa del Rey final §Details | 30 | modern | Vinícius Júnior, Rodrygo, Luka Modrić, Lucas Torró, Sergio Herrera | checked |
| ll072 | Name a player who appeared in the 2024 Copa del Rey final (Athletic v Mallorca) | en:2024 Copa del Rey final §Details | 34 | modern | Nico Williams, Oihan Sancet, Vedat Muriqi, Dani Rodríguez, Dominik Greif | checked |
| ll073 | Name a player who appeared in the 2025 Copa del Rey final (Barcelona v Real Madrid) | en:2025 Copa del Rey final §Details | 33 | modern | Pedri, Kylian Mbappé, Jules Koundé, Ferran Torres, Aurélien Tchouaméni | checked |
| ll074 | Name a player who appeared in the 2026 Copa del Rey final (Atlético Madrid v Real Sociedad) | en:2026 Copa del Rey final §Details | 34 | modern | Julián Alvarez, Mikel Oyarzabal, Ademola Lookman, Jan Oblak, Ander Barrenetxea | checked |
| ll075 | Name a player who has scored in a Copa del Rey final since 2000 | en:2000 Copa del Rey final … en:2026 Copa del Rey final (goals) | 68 | 2000s+ | Messi, Cristiano Ronaldo, Gareth Bale, Gaizka Toquero, Hugo Duro | checked; own goals excluded |
| ll076 | Name a player who has scored in a Supercopa de España final since 2020 | en:2020 Supercopa de España final … en:2026 Supercopa de España final | 16 | modern | Lewandowski, Vinícius Júnior, Lamine Yamal, Asier Villalibre, Alejandro Balde | checked |
| ll077 | Name a player who has scored in any Supercopa de España match since the four-team format (2020 edition onward) | en:2020 Supercopa de España, en:2021 Supercopa de España … en:2026 Supercopa de España (semi-finals + finals) | 45 | modern | Vinícius Júnior, Lewandowski, Antoine Griezmann, Toni Kroos, Isco | rough |
| ll078 | Name a player who appeared for Sevilla in a Europa League final (2014, 2015, 2016, 2020, 2023) | en:2014 UEFA Europa League final, en:2015 UEFA Europa League final, en:2016 UEFA Europa League final, en:2020 UEFA Europa League final, en:2023 UEFA Europa League final (Sevilla line-ups) | 49 | modern | Jesús Navas, Ivan Rakitić, Carlos Bacca, Yassine Bounou, Diogo Figueiras | checked |
| ll079 | Name a player who appeared for Atlético Madrid in a Europa League final (2010, 2012, 2018) | en:2010 UEFA Europa League final, en:2012 UEFA Europa League final, en:2018 UEFA Europa League final (Atlético line-ups) | 36 | 2000s+ | Antoine Griezmann, Diego Forlán, Radamel Falcao, David de Gea, Tomáš Ujfaluši | checked |
| ll080 | Name a player who appeared for Villarreal in the 2021 Europa League final | en:2021 UEFA Europa League final (Villarreal line-up) | 17 | modern | Gerard Moreno, Pau Torres, Raúl Albiol, Gerónimo Rulli, Juan Foyth | checked |
| ll081 | Name a player who appeared for Real Betis in the 2025 Conference League final | en:2025 UEFA Conference League final (Betis line-up) | 16 | modern | Isco, Antony, Abde Ezzalzouli, Johnny Cardoso, Giovani Lo Celso | |
| ll082 | Name a player who has won the Copa del Rey with Barcelona since 2015 (appeared in the final) | en:2015 Copa del Rey final, en:2016 Copa del Rey final, en:2017 Copa del Rey final, en:2018 Copa del Rey final, en:2021 Copa del Rey final, en:2025 Copa del Rey final (Barcelona line-ups) | 45 | modern | Messi, Neymar, Andrés Iniesta, Philippe Coutinho, Óscar Mingueza | starters + used subs |
| ll083 | Name a player who has won the Copa del Rey with Real Madrid since 2011 (appeared in the final) | en:2011 Copa del Rey final, en:2014 Copa del Rey final, en:2023 Copa del Rey final (Real Madrid line-ups) | 40 | modern | Cristiano Ronaldo, Gareth Bale, Ángel Di María, Vinícius Júnior, Esteban Granero | starters + used subs |
| ll186 | Name a player who appeared in the 2019 Copa del Rey final (Barcelona v Valencia) | en:2019 Copa del Rey final §Details | 28 | modern | Messi, Philippe Coutinho, Rodrigo, Kevin Gameiro, Jaume Doménech | checked; starters + used subs (28) |
| ll200 | Name a player who appeared in the 2013 Copa del Rey final (Atlético beat Real Madrid at the Bernabéu) | en:2013 Copa del Rey final §Details | 28 | 2000s+ | Cristiano Ronaldo, Diego Costa, Radamel Falcao, Thibaut Courtois, Miranda | starters + used subs |
| ll187 | Name a player who has scored in a Copa del Rey semi-final since 2019–20 | Season pages 2019–20 Copa del Rey … 2025–26 Copa del Rey §Semi-finals (goals) | 40 | modern | Pedri, Jude Bellingham, Nico Williams, Mikel Oyarzabal, Marc Bernal | checked (33 parsed); two-legged ties |

## Clubs & competitions

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ll084 | Name a club that has played in La Liga since 2015–16 | Season pages 2015–16 La Liga … 2026–27 La Liga §Stadiums and locations | 33 | modern | Real Madrid, Girona, SD Eibar, SD Huesca, Real Oviedo | checked |
| ll085 | Name a club that played in La Liga between 2000–01 and 2008–09 | Season pages 2000–01 La Liga … 2008–09 La Liga §Teams | 38 | 2000s+ | Deportivo de La Coruña, Real Zaragoza, Recreativo de Huelva, CD Numancia, Gimnàstic de Tarragona | rough |
| ll086 | Name a club that has been relegated from La Liga since 2010–11 | Season pages 2010–11 La Liga … 2025–26 La Liga §League table (bottom three) | 32 | modern | Deportivo de La Coruña, Málaga, Espanyol, Elche, Cádiz | rough |
| ll087 | Name a club that has been promoted to La Liga since 2015–16 | Season pages 2015–16 La Liga … 2026–27 La Liga §Promotion and relegation (pre-season) | 24 | modern | Girona, Leganés, Real Oviedo, Racing de Santander, Elche | rough |
| ll088 | Name a club that has taken part in the Segunda División promotion play-offs (2011 onward) | en:La Liga play-offs §2011–present | 32 | modern | Girona, Rayo Vallecano, Real Oviedo, Albacete, Hércules | checked |
| ll089 | Name a club that has played in the Segunda División since 2020–21 | Season pages 2020–21 Segunda División … 2026–27 Segunda División §Teams | 55 | modern | Sporting Gijón, Real Zaragoza, Málaga, FC Andorra, CD Eldense | rough |
| ll090 | Name a club that has won the Segunda División title since 2000 | en:Segunda División §Champions | 20 | 2000s+ | Atlético Madrid, Real Betis, SD Eibar, Granada, Leganés | rough; Segunda article champions list |
| ll091 | Name a former La Liga club that has played in Primera Federación (third tier, since 2021–22) | en:2021–22 Primera División RFEF, en:2022–23 Primera Federación … en:2025–26 Primera Federación §Teams, cross-checked with en:List of La Liga clubs | 25 | modern | Deportivo de La Coruña, Racing de Santander, Málaga, Córdoba, Gimnàstic de Tarragona | "fallen giants"; first season page has a different canonical title |
| ll092 | Name a club that has finished in La Liga's top seven since 2010–11 | Season pages 2010–11 La Liga … 2025–26 La Liga §League table | 17 | modern | Real Madrid, Villarreal, Getafe, Málaga, Granada | rough |
| ll093 | Name a club that has played in a Copa del Rey final since 2000 | en:List of Copa del Rey finals §List of finals | 20 | 2000s+ | Barcelona, Espanyol, Recreativo de Huelva, Getafe, Osasuna | rough |
| ll094 | Name a club that has reached the Copa del Rey quarter-finals since 2019–20 | Season pages 2019–20 Copa del Rey … 2025–26 Copa del Rey §Quarter-finals | 24 | modern | Real Madrid, Athletic Bilbao, CD Mirandés, Leganés, Albacete | checked |
| ll095 | Name a club from outside La Liga that reached the Copa del Rey round of 16 since 2019–20 | Season pages 2019–20 Copa del Rey … 2025–26 Copa del Rey §Round of 16 (tier in brackets ≠ 1) | 23 | modern | CD Mirandés, CD Alcoyano, Unionistas de Salamanca, Cultural Leonesa, CDA Navalcarnero | checked; giant-killers |
| ll096 | Name a club that has played in Liga F (2022–23 onward) | en:2022–23 Liga F … en:2026–27 Liga F §Teams | 24 | modern | FC Barcelona Femení, Real Madrid Femenino, Atlético Madrid Femenino, Madrid CFF, Alhama CF | checked |
| ll097 | Name a country that has had a player in La Liga from Africa | en:List of foreign La Liga players §Africa (CAF) | 35 | 2000s+ | Morocco, Cameroon, Nigeria, Mauritania, Burundi | answers are countries; all-time |

## Stadiums, cities & brands

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ll098 | Name a stadium that has hosted La Liga matches since 2015–16 | Season pages 2015–16 La Liga … 2026–27 La Liga §Stadiums and locations | 38 | modern | Santiago Bernabéu, Camp Nou, Metropolitano, Ipurua, Nuevo Mirandilla | checked; dedupe redirects (renamed grounds) |
| ll099 | Name a football stadium in Spain with a capacity of 20,000 or more | en:List of football stadiums in Spain §Current stadiums | 36 | modern | Santiago Bernabéu, Camp Nou, Mestalla, Estadio de La Cartuja, La Romareda | checked |
| ll190 | Name a stadium used by a Segunda División club in 2025–26 | en:2025–26 Segunda División §Stadiums and locations | 22 | modern | Estadio Riazor, La Rosaleda, El Molinón, Campos de Sport de El Sardinero, Estadio Municipal de Anduva | checked |
| ll100 | Name a stadium that has hosted a Copa del Rey final | en:List of Copa del Rey finals §List of finals (venue column) | 31 | classic | Santiago Bernabéu, Mestalla, Estadio de La Cartuja, Vicente Calderón, Campo de O'Donnell | checked |
| ll101 | Name a city or town that has had a La Liga club since 2015–16 | Season pages 2015–16 La Liga … 2026–27 La Liga §Stadiums and locations | 28 | modern | Madrid, Barcelona, Seville, Eibar, Cornellà de Llobregat | checked |
| ll102 | Name a kit manufacturer that has supplied a La Liga club since 2015–16 | Season pages 2015–16 La Liga … 2026–27 La Liga §Personnel and kits/sponsorship (kit maker column) | 15 | modern | Nike, Adidas, Puma, Joma, Xtep | checked; companies with articles |
| ll103 | Name a company that has been a La Liga club's main shirt sponsor since 2015–16 | Season pages 2015–16 La Liga … 2026–27 La Liga §Personnel and kits/sponsorship (main sponsor column) | 45 | modern | Spotify, Emirates, Rakuten, Riyadh Air, Kutxabank | checked; only sponsors with en articles count |
| ll104 | Name a broadcaster that has shown La Liga outside Spain | en:List of La Liga broadcasters §International broadcasters | 60 | modern | ESPN, beIN Sports, DAZN, Premier Sports, Viaplay | rough |
| ll105 | Name a president of Real Madrid or FC Barcelona | en:List of Real Madrid CF presidents; en:List of FC Barcelona presidents | 55 | classic | Florentino Pérez, Joan Laporta, Santiago Bernabéu, Josep Maria Bartomeu, Joan Gamper | |
| ll106 | Name a stadium that has hosted a Copa del Rey or Supercopa de España final since 2015 | en:2015 Copa del Rey final … en:2026 Copa del Rey final; en:2015 Supercopa de España … en:2026 Supercopa de España (venues) | 14 | modern | Estadio de La Cartuja, Metropolitano, King Abdullah Sports City, Ibn Batouta Stadium, La Rosaleda | two-legged Supercopas (2015–17) add home grounds; `2019 Supercopa de España` redirects (no 2019 edition), skip it |

## Managers

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ll107 | Name a manager who took charge of a La Liga club during 2025–26 | en:2025–26 La Liga §Personnel and kits, §Managerial changes | 34 | modern | Hansi Flick, Xabi Alonso, Diego Simeone, Ernesto Valverde, Míchel | checked |
| ll108 | Name a manager involved in a mid-season La Liga managerial change since 2022–23 (outgoing or incoming) | Season pages 2022–23 La Liga … 2026–27 La Liga §Managerial changes (in-season rows) | 45 | modern | Julen Lopetegui, Gennaro Gattuso, José Luis Mendilibar, Quique Sánchez Flores, Diego Alonso | pre-season rows excluded |
| ll109 | Name a manager who managed in La Liga between 2015–16 and 2019–20 | Season pages 2015–16 La Liga … 2019–20 La Liga §Personnel, §Managerial changes | 77 | modern | Zinedine Zidane, Rafael Benítez, Quique Setién, Gary Neville, Paco Jémez | checked |
| ll110 | Name a manager who managed in La Liga between 2020–21 and 2024–25 | Season pages 2020–21 La Liga … 2024–25 La Liga §Personnel, §Managerial changes | 80 | modern | Carlo Ancelotti, Xavi, Imanol Alguacil, Javier Aguirre, Iñigo Pérez | rough |
| ll111 | Name a non-Spanish manager who has managed in La Liga since 2015–16 | Season pages 2015–16 La Liga … 2026–27 La Liga §Personnel, §Managerial changes (flag ≠ Spain) | 35 | modern | Zidane, Ancelotti, Flick, Manuel Pellegrini, Pellegrino Matarazzo | rough |
| ll112 | Name a manager who has won the Copa del Rey since 2000 | en:List of Copa del Rey finals; en:2000 Copa del Rey final … en:2026 Copa del Rey final (winning manager in line-ups) | 22 | 2000s+ | Pep Guardiola, Luis Enrique, Carlo Ancelotti, Imanol Alguacil, Joaquín Caparrós | |
| ll113 | Name a manager who has won the Supercopa de España since 2000 | en:Supercopa de España; en:2000 Supercopa de España … en:2026 Supercopa de España (winning manager) | 20 | 2000s+ | Pep Guardiola, José Mourinho, Xavi, Marcelino, Juande Ramos | `2019 Supercopa de España` redirects (no such edition); January 2020 edition is `2020 Supercopa de España` |
| ll114 | Name a manager of Valencia since 2000 (caretakers included) | en:List of Valencia CF managers | 25 | 2000s+ | Rafael Benítez, Unai Emery, Marcelino, Gary Neville, Rubén Baraja | |
| ll115 | Name a manager of Atlético Madrid since 1995 (caretakers included) | en:List of Atlético Madrid managers | 20 | 2000s+ | Diego Simeone, Radomir Antić, Javier Aguirre, Quique Sánchez Flores, Carlos Bianchi | |
| ll116 | Name a manager of Athletic Bilbao since 2000 (caretakers included) | en:List of Athletic Bilbao managers | 16 | 2000s+ | Ernesto Valverde, Marcelo Bielsa, Marcelino, Joaquín Caparrós, Jupp Heynckes | |
| ll117 | Name a manager of Real Sociedad since 2000 (caretakers included) | en:List of Real Sociedad managers | 20 | 2000s+ | Imanol Alguacil, David Moyes, Philippe Montanier, Jagoba Arrasate, Raynald Denoueix | |
| ll118 | Name a head coach of Sevilla since 2015–16 (caretakers included) | Season pages 2015–16 Sevilla FC season … 2025–26 Sevilla FC season (head coach / managerial changes) | 14 | modern | Unai Emery, Julen Lopetegui, Jorge Sampaoli, José Luis Mendilibar, Vincenzo Montella | Sevilla has no managers list page; use season pages |
| ll194 | Name a manager who took charge of a Segunda División club during 2025–26 | en:2025–26 Segunda División §Personnel and sponsors, §Managerial changes | 30 | modern | Rubi, Luis García, Fran Escribá, Antonio Hidalgo, Borja Jiménez | checked (22 at season start + changes) |

## Club player lists

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ll119 | Name a player who has made an official appearance for Real Madrid since 2020–21 | en:List of Real Madrid CF players (career years ≥ 2020) | 90 | modern | Vinícius Júnior, Jude Bellingham, Endrick, Antonio Blanco, Víctor Chust | list is complete (every official appearance) |
| ll120 | Name a player who played for Real Madrid in the Galácticos era (2000–01 to 2005–06) | en:List of Real Madrid CF players (career overlaps 2000–2006) | 85 | 2000s+ | Zinedine Zidane, David Beckham, Ronaldo Nazário, Luís Figo, Jonathan Woodgate | rough |
| ll121 | Name a goalkeeper who has played for Real Madrid since 2000 | en:List of Real Madrid CF players (position GK, career ≥ 2000) | 20 | 2000s+ | Iker Casillas, Thibaut Courtois, Keylor Navas, Andriy Lunin, Jerzy Dudek | checked |
| ll122 | Name a notable Barcelona player (roughly 100+ league games) whose Barcelona career ran into 2008 or later | en:List of FC Barcelona players | 75 | 2000s+ | Messi, Andrés Iniesta, Sergio Busquets, Pedri, Seydou Keita | checked; list criterion "generally 100+ league matches" |
| ll123 | Name a notable Atlético Madrid player whose Atlético career ran into the Simeone era (2011–12 or later) | en:List of Atlético Madrid players | 47 | modern | Koke, Antoine Griezmann, Jan Oblak, Diego Godín, Juanfran | checked |
| ll124 | Name a player who has been in Valencia's first-team squad since 2021–22 | Season pages 2021–22 Valencia CF season … 2025–26 Valencia CF season §Players (La Liga squad information) | 65 | modern | José Gayà, Giorgi Mamardashvili, Hugo Duro, Javi Guerra, Pepelu | rough; en:List of Valencia CF players stops around 2020, so season pages are used instead |
| ll191 | Name a Real Sociedad player listed among the club's notable players whose career there ran into 2010 or later | en:List of Real Sociedad players | 45 | modern | Mikel Oyarzabal, Carlos Vela, Asier Illarramendi, Xabi Prieto, Igor Zubeldia | checked |
| ll125 | Name a player who has captained a La Liga club since 2020–21 | Season pages 2020–21 La Liga … 2026–27 La Liga §Personnel (captain column) | 65 | modern | Messi, Karim Benzema, Koke, Cristhian Stuani, Diego Villares | checked |

## Transfers

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ll126 | Name a player Real Madrid signed between 2019–20 and 2025–26 | Season pages 2019–20 Real Madrid CF season … 2025–26 Real Madrid CF season §Transfers – In | 35 | modern | Kylian Mbappé, Jude Bellingham, Aurélien Tchouaméni, Dean Huijsen, Franco Mastantuono | exclude loan returns and academy promotions |
| ll127 | Name a player Barcelona signed between 2019–20 and 2025–26 | Season pages 2019–20 FC Barcelona season … 2025–26 FC Barcelona season §Transfers – In | 40 | modern | Robert Lewandowski, Raphinha, Jules Koundé, Dani Olmo, Miralem Pjanić | include loans-in; exclude loan returns |
| ll128 | Name a player Atlético Madrid signed between 2019–20 and 2025–26 | Season pages 2019–20 Atlético Madrid season … 2025–26 Atlético Madrid season §Transfers – In | 45 | modern | João Félix, Julián Alvarez, Alexander Sørloth, Kieran Trippier, Samuel Lino | exclude loan returns |
| ll129 | Name a player Sevilla signed between 2019–20 and 2025–26 | Season pages 2019–20 Sevilla FC season … 2025–26 Sevilla FC season §Transfers – In | 50 | modern | Lucas Ocampos, Jules Koundé, Youssef En-Nesyri, Isco, Jesús Corona | exclude loan returns |
| ll130 | Name a player Real Sociedad signed between 2019–20 and 2025–26 | Season pages 2019–20 Real Sociedad season … 2025–26 Real Sociedad season §Transfers – In | 35 | modern | Alexander Isak, Takefusa Kubo, David Silva, Martin Ødegaard, Brais Méndez | exclude loan returns |
| ll131 | Name a player Girona signed between 2022–23 and 2025–26 | Season pages 2022–23 Girona FC season … 2025–26 Girona FC season §Transfers – In | 40 | modern | Artem Dovbyk, Savinho, Daley Blind, Viktor Tsyhankov, Ladislav Krejčí | loans-in count |
| ll132 | Name a player who permanently left Barcelona between 2019–20 and 2025–26 | Season pages 2019–20 FC Barcelona season … 2025–26 FC Barcelona season §Transfers – Out | 60 | modern | Messi, Luis Suárez, Ousmane Dembélé, Ivan Rakitić, Clément Lenglet | permanent exits incl. free/released; loans out excluded |
| ll133 | Name a player who permanently left Real Madrid between 2018–19 and 2025–26 | Season pages 2018–19 Real Madrid CF season … 2025–26 Real Madrid CF season §Transfers – Out | 60 | modern | Cristiano Ronaldo, Sergio Ramos, Casemiro, Karim Benzema, Achraf Hakimi | permanent exits; loans out excluded |
| ll195 | Name a player Villarreal signed between 2019–20 and 2025–26 | Season pages 2019–20 Villarreal CF season … 2025–26 Villarreal CF season §Transfers – In | 45 | modern | Dani Parejo, Francis Coquelin, Arnaut Danjuma, Alexander Sørloth, Thierno Barry | exclude loan returns |
| ll198 | Name a player who permanently left Valencia between 2019–20 and 2025–26 | Season pages 2019–20 Valencia CF season … 2025–26 Valencia CF season §Transfers – Out | 45 | modern | Ferran Torres, Rodrigo, Dani Parejo, Carlos Soler, Giorgi Mamardashvili | the 'fire sale' years; loans out excluded |
| ll199 | Name a player Real Betis signed between 2019–20 and 2025–26 | Season pages 2019–20 Real Betis season … 2025–26 Real Betis season §Transfers – In | 50 | modern | Isco, Antony, Vitor Roque, Héctor Bellerín, Giovani Lo Celso | loans-in count; exclude loan returns |
| ll134 | Name a player in Real Madrid's or Barcelona's top-10 record transfer fees paid or received | en:List of Real Madrid CF records and statistics §Highest transfer fees paid, §Highest transfer fees received; en:List of FC Barcelona records and statistics §Transfer fee paid, §Transfer fee received | 35 | 2000s+ | Neymar, Gareth Bale, Philippe Coutinho, Eden Hazard, Achraf Hakimi | checked (RM 10+10, Barça ~10+7) |
| ll135 | Name a player whose move to or from a Spanish club is on Wikipedia's list of most expensive transfers | en:List of most expensive association football transfers §Highest transfer records in association football | 17 | modern | Neymar, Jude Bellingham, Antoine Griezmann, Kepa Arrizabalaga, Lucas Hernandez | checked; borderline small |

## Career paths: played for both

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ll136 | Name a player who has played for both Real Madrid and Atlético Madrid | en:Madrid derby §Players who played for both clubs; cross-check Category ∩ Real Madrid CF players / Atlético Madrid footballers | 56 | 2000s+ | Thibaut Courtois, Álvaro Morata, Marcos Llorente, Sergio Reguilón, Hugo Sánchez | category ∩ = 56 |
| ll137 | Name a player who has played for both Barcelona and Atlético Madrid | Category ∩ FC Barcelona players / Atlético Madrid footballers | 48 | 2000s+ | Antoine Griezmann, Luis Suárez, David Villa, João Félix, Arda Turan | checked |
| ll138 | Name a player who has played for both Barcelona and Valencia | Category ∩ FC Barcelona players / Valencia CF players | 48 | 2000s+ | Jordi Alba, David Villa, Ferran Torres, André Gomes, Gaizka Mendieta | checked |
| ll139 | Name a player who has played for both Barcelona and Sevilla | Category ∩ FC Barcelona players / Sevilla FC players | 41 | 2000s+ | Ivan Rakitić, Dani Alves, Jules Koundé, Seydou Keita, Luuk de Jong | checked |
| ll140 | Name a player who has played for both Real Madrid and Sevilla | Category ∩ Real Madrid CF players / Sevilla FC players | 45 | 2000s+ | Sergio Ramos, Isco, Sergio Reguilón, Mariano Díaz, Davor Šuker | checked |
| ll141 | Name a player who has played for both Real Madrid and Real Betis | Category ∩ Real Madrid CF players / Real Betis players | 43 | 2000s+ | Isco, Dani Ceballos, Rafael van der Vaart, Alfonso Pérez | checked |
| ll142 | Name a player who has played for both Barcelona and Real Betis | Category ∩ FC Barcelona players / Real Betis players | 39 | 2000s+ | Héctor Bellerín, Marc Bartra, Emerson Royal, Abde Ezzalzouli, Alfonso Pérez | checked |
| ll143 | Name a player who has played for both Atlético Madrid and Sevilla | Category ∩ Atlético Madrid footballers / Sevilla FC players | 40 | 2000s+ | José Antonio Reyes, Kevin Gameiro, Vitolo, Clément Lenglet | checked |
| ll144 | Name a player who has played for both Valencia and Villarreal | Category ∩ Valencia CF players / Villarreal CF players | 40 | 2000s+ | Dani Parejo, Raúl Albiol, Roberto Soldado, Francis Coquelin | checked |
| ll145 | Name a player who has played for both Athletic Bilbao and Real Sociedad | Category ∩ Athletic Bilbao footballers / Real Sociedad footballers | 35 | 2000s+ | Iñigo Martínez, Joseba Etxeberria, Bittor Alkiza | checked; Basque derby crossovers |
| ll146 | Name a player who has played for both Barcelona and Girona | Category ∩ FC Barcelona players / Girona FC players | 42 | modern | Eric García, Oriol Romeu, Pablo Torre | checked |
| ll147 | Name a player who has played for both Real Madrid and Getafe | Category ∩ Real Madrid CF players / Getafe CF footballers | 33 | 2000s+ | Roberto Soldado, Esteban Granero, Pedro León, Borja Mayoral | checked |

## Nationalities in La Liga

All from en:List of foreign La Liga players (country sections; each entry lists clubs and La Liga years), plus en:List of Argentine footballers in La Liga and en:List of Brazilian footballers in La Liga, which have the same format. "Since 2015–16" = entry's La Liga years reach 2016 or later.

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ll148 | Name a Uruguayan who has played in La Liga since 2015–16 | en:List of foreign La Liga players §Uruguay | 55 | modern | Luis Suárez, Federico Valverde, Diego Godín, Cristhian Stuani, Mauro Arambarri | checked |
| ll149 | Name a French player who has played in La Liga since 2015–16 | en:List of foreign La Liga players §France | 84 | modern | Antoine Griezmann, Kylian Mbappé, Karim Benzema, Jules Koundé, Loïc Badé | checked |
| ll150 | Name a Portuguese player who has played in La Liga since 2015–16 | en:List of foreign La Liga players §Portugal | 66 | modern | Cristiano Ronaldo, João Félix, João Cancelo, Gonçalo Guedes, André Silva | checked |
| ll151 | Name an Argentine who has played in La Liga since 2020–21 | en:List of Argentine footballers in La Liga | 102 | modern | Messi, Julián Alvarez, Rodrigo De Paul, Taty Castellanos, Lucas Boyé | checked |
| ll152 | Name a Brazilian who has played in La Liga since 2018–19 | en:List of Brazilian footballers in La Liga | 63 | modern | Vinícius Júnior, Raphinha, Rodrygo, Éder Militão, Abner Vinícius | checked |
| ll153 | Name a Moroccan who has played in La Liga | en:List of foreign La Liga players §Morocco | 69 | modern | Achraf Hakimi, Yassine Bounou, Youssef En-Nesyri, Abde Ezzalzouli, Nayef Aguerd | checked; two-thirds active since 2015 |
| ll154 | Name a Dutch player who has played in La Liga since 2000 | en:List of foreign La Liga players §Netherlands | 60 | 2000s+ | Frenkie de Jong, Memphis Depay, Patrick Kluivert, Ruud van Nistelrooy, Luuk de Jong | checked |
| ll155 | Name an Italian who has played in La Liga since 2000 | en:List of foreign La Liga players §Italy | 68 | 2000s+ | Fabio Cannavaro, Giuseppe Rossi, Ciro Immobile, Simone Zaza, Christian Abbiati | checked |
| ll156 | Name a Colombian who has played in La Liga since 2010–11 | en:List of foreign La Liga players §Colombia | 42 | modern | Radamel Falcao, James Rodríguez, Carlos Bacca, Luis Muriel, Santiago Arias | checked |
| ll157 | Name a Mexican who has played in La Liga | en:List of foreign La Liga players §Mexico | 49 | 2000s+ | Hugo Sánchez, Rafael Márquez, Carlos Vela, Andrés Guardado, Héctor Herrera | checked |
| ll158 | Name a Nigerian who has played in La Liga | en:List of foreign La Liga players §Nigeria | 44 | 2000s+ | Samuel Chukwueze, Ikechukwu Uche, Kelechi Iheanacho, Finidi George, Kalu Uche | checked |
| ll159 | Name a Senegalese player who has played in La Liga | en:List of foreign La Liga players §Senegal | 39 | modern | Nicolas Jackson, Boulaye Dia, Pape Gueye, Papa Kouly Diop | checked |
| ll160 | Name a player from England, Scotland, Wales, Northern Ireland or the Republic of Ireland who has played in La Liga | en:List of foreign La Liga players §England, §Scotland, §Wales, §Northern Ireland, §Republic of Ireland | 58 | 2000s+ | Jude Bellingham, David Beckham, Gareth Bale, Kieran Trippier, Gary Lineker | checked |
| ll161 | Name a Danish, Swedish, Norwegian, Finnish or Icelandic player who has played in La Liga since 2010–11 | en:List of foreign La Liga players §Denmark, §Sweden, §Norway, §Finland, §Iceland | 44 | modern | Alexander Sørloth, Alexander Isak, Martin Ødegaard, Martin Braithwaite, Andreas Christensen | checked |
| ll162 | Name a player from an AFC country (Asia or Australia) who has played in La Liga | en:List of foreign La Liga players §Asia (AFC) sections | 44 | modern | Takefusa Kubo, Lee Kang-in, Takashi Inui, Wu Lei, Mathew Ryan | checked |
| ll163 | Name an American or Canadian who has played in La Liga | en:List of foreign La Liga players §United States, §Canada | 19 | modern | Yunus Musah, Sergiño Dest, Tajon Buchanan, Cyle Larin, Jozy Altidore | checked |
| ll164 | Name a Belgian who has played in La Liga | en:List of foreign La Liga players §Belgium | 38 | modern | Thibaut Courtois, Eden Hazard, Yannick Carrasco, Michy Batshuayi, Toby Alderweireld | checked |
| ll165 | Name a Serbian, Montenegrin or Bosnian player who has played in La Liga since 2010–11 | en:List of foreign La Liga players §Serbia, §Montenegro, §Bosnia and Herzegovina | 57 | modern | Luka Jović, Miralem Pjanić, Stefan Savić, Ermedin Demirović, Kenan Kodro | checked |
| ll166 | Name a Croatian who has played in La Liga since 2000 | en:List of foreign La Liga players §Croatia | 35 | 2000s+ | Luka Modrić, Ivan Rakitić, Ante Budimir, Mateo Kovačić, Luka Sučić | checked |
| ll167 | Name a Ukrainian, Georgian or Russian player who has played in La Liga since 2015–16 | en:List of foreign La Liga players §Ukraine, §Georgia, §Russia | 25 | modern | Artem Dovbyk, Andriy Lunin, Giorgi Mamardashvili, Viktor Tsygankov, Denis Cheryshev | rough |

## Nationality at a club

Same sources and filters as above, restricted to entries whose club list includes the named club.

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ll168 | Name a Brazilian who has played for Real Madrid | en:List of Brazilian footballers in La Liga (club = Real Madrid) | 26 | 2000s+ | Vinícius Júnior, Ronaldo Nazário, Roberto Carlos, Éder Militão, Sávio | checked |
| ll169 | Name a Brazilian who has played for Barcelona | en:List of Brazilian footballers in La Liga (club = Barcelona) | 33 | 2000s+ | Neymar, Ronaldinho, Rivaldo, Raphinha, Vitor Roque | checked |
| ll170 | Name a Brazilian who has played for Atlético Madrid | en:List of Brazilian footballers in La Liga (club = Atlético Madrid) | 30 | 2000s+ | Filipe Luís, Miranda, Renan Lodi, Samuel Lino, Leivinha | checked |
| ll171 | Name an Argentine who has played for Atlético Madrid | en:List of Argentine footballers in La Liga (club = Atlético Madrid) | 51 | 2000s+ | Diego Simeone, Sergio Agüero, Julián Alvarez, Rodrigo De Paul, Rubén Ayala | checked |
| ll172 | Name an Argentine who has played for Real Madrid | en:List of Argentine footballers in La Liga (club = Real Madrid) | 28 | 2000s+ | Alfredo Di Stéfano, Ángel Di María, Gonzalo Higuaín, Fernando Redondo, Nico Paz | checked |
| ll173 | Name an Argentine who has played for Barcelona | en:List of Argentine footballers in La Liga (club = Barcelona) | 20 | 2000s+ | Messi, Javier Mascherano, Diego Maradona, Javier Saviola, Juan Román Riquelme | checked |
| ll174 | Name an Argentine who has played for Sevilla | en:List of Argentine footballers in La Liga (club = Sevilla) | 40 | 2000s+ | Éver Banega, Lucas Ocampos, Marcos Acuña, Papu Gómez, Federico Fazio | checked |
| ll175 | Name an Argentine who has played for Valencia | en:List of Argentine footballers in La Liga (club = Valencia) | 39 | 2000s+ | Mario Kempes, Pablo Aimar, Roberto Ayala, Nicolás Otamendi, Ezequiel Garay | checked |
| ll176 | Name a French player who has played for Barcelona | en:List of foreign La Liga players §France (club = Barcelona) | 20 | 2000s+ | Thierry Henry, Antoine Griezmann, Ousmane Dembélé, Jules Koundé, Philippe Christanval | checked |
| ll177 | Name a French player who has played for Real Madrid | en:List of foreign La Liga players §France (club = Real Madrid) | 18 | 2000s+ | Zinedine Zidane, Karim Benzema, Kylian Mbappé, Eduardo Camavinga, Lassana Diarra | checked |
| ll178 | Name a French player who has played for Sevilla | en:List of foreign La Liga players §France (club = Sevilla) | 27 | modern | Jules Koundé, Wissam Ben Yedder, Kevin Gameiro, Samir Nasri, Anthony Martial | checked |
| ll179 | Name a Uruguayan who has played for Atlético Madrid | en:List of foreign La Liga players §Uruguay (club = Atlético Madrid) | 18 | 2000s+ | Diego Godín, Diego Forlán, José Giménez, Luis Suárez, Lucas Torreira | checked |
| ll180 | Name a Dutch player who has played for Barcelona | en:List of foreign La Liga players §Netherlands (club = Barcelona) | 22 | 2000s+ | Johan Cruyff, Frenkie de Jong, Patrick Kluivert, Memphis Depay, Winston Bogarde | checked |

## Women's football (Liga F)

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| ll181 | Name a notable Barcelona Femení player | en:List of FC Barcelona Femení players §Players | 46 | modern | Alexia Putellas, Aitana Bonmatí, Caroline Graham Hansen, Salma Paralluelo, Mapi León | checked |
| ll182 | Name a player who finished in Liga F's top scorers table in a season since 2022–23 | en:2022–23 Liga F … en:2025–26 Liga F §Top goalscorers | 27 | modern | Alexia Putellas, Salma Paralluelo, Ewa Pajor, Linda Caicedo, Edna Imade | checked |
| ll183 | Name a winner of the Liga F Player of the Month award | en:Liga F Player of the Month §Winners | 18 | modern | Alexia Putellas, Ewa Pajor, Linda Caicedo, Athenea del Castillo, Lucía Moral | checked; started 2024–25 |
| ll184 | Name a South American player who has played in Spain's top women's division (Liga F / Primera División) | en:List of foreign Liga F players §South America (CONMEBOL) | 96 | modern | Linda Caicedo, Geyse, Deyna Castellanos, Estefanía Banini, Gabi Nunes | checked |
| ll185 | Name an African player who has played in Spain's top women's division (Liga F / Primera División) | en:List of foreign Liga F players §Africa (CAF) | 54 | modern | Asisat Oshoala, Rasheedat Ajibade, Racheal Kundananji, Gift Monday | checked |
| ll189 | Name a player in Real Madrid Femenino's 2024–25 squad | en:2024–25 Real Madrid Femenino season §Players | 25 | modern | Linda Caicedo, Athenea del Castillo, Caroline Weir, Signe Bruun, Misa Rodríguez | rough |

## Summary

**Total prompts:** 200 (ll001–ll200; ids are unique, but the ones added late sit inside their topical sections, so the order isn't strictly sequential).

**Era split:** modern 132 (66%) · 2000s+ 59 (29.5%) · classic 9 (4.5%).

**Per sub-heading:**

| sub-heading | prompts | modern | 2000s+ | classic |
|---|---|---|---|---|
| Goals & scoring records | 17 | 8 | 8 | 1 |
| El Clásico & the big two | 6 | 2 | 1 | 3 |
| Awards & trophies | 17 | 11 | 3 | 3 |
| Season squads | 18 | 17 | 1 | 0 |
| Club goalscorers by season | 14 | 14 | 0 | 0 |
| Cup finals | 19 | 16 | 3 | 0 |
| Clubs & competitions | 14 | 10 | 4 | 0 |
| Stadiums, cities & brands | 10 | 8 | 0 | 2 |
| Managers | 13 | 7 | 6 | 0 |
| Club player lists | 8 | 5 | 3 | 0 |
| Transfers | 13 | 12 | 1 | 0 |
| Career paths: played for both | 12 | 1 | 11 | 0 |
| Nationalities in La Liga | 20 | 14 | 6 | 0 |
| Nationality at a club | 13 | 1 | 12 | 0 |
| Women's football (Liga F) | 6 | 6 | 0 | 0 |

**Template families (cap ≈ 20 each):** nationality in La Liga 20; season squad / squad union 20 (ll040–ll057 + ll124 + ll189); single-final line-ups 9; club-season goalscorers 14; transfers in/out 12; "played for both" 12; nationality-at-club 13; manager lists 13. Answer types are mixed: players, clubs (ll012–ll014, ll038, ll084–ll096), countries (ll039, ll097), stadiums (ll098–ll100, ll106, ll190), cities (ll101), companies (ll102–ll104), managers and presidents.

**Title verification:** all ~250 cited titles, including every page in the season ranges and the 11 club categories, resolve on en.wikipedia. The canonical title is cited wherever there was a redirect: La Liga Team of the Season / LFP Awards → `La Liga Awards`; Segunda División play-offs → `La Liga play-offs`; Derbi barceloní → `Derbi Barceloní`; 2021–22 Primera Federación → `2021–22 Primera División RFEF`; 2025 UEFA Europa Conference League final → `2025 UEFA Conference League final`. `2019 Supercopa de España` redirects to the competition article because there was no 2019 edition; this is noted in ll106/ll113. These candidate titles were missing, so the prompts use other sources: List of footballers with 100 or more La Liga goals (→ List of La Liga top scorers), List of Sevilla FC / Real Betis / Villarreal / Espanyol / Celta managers (→ season pages or dropped), List of Sevilla FC players, Real Madrid/Barcelona captains lists, La Liga Player/Manager of the Season, Copa del Rey Final, 2019 Supercopa de España final, 2013–14 Girona FC season, Category:La Masia alumni, Category:Deportivo de La Coruña players.

**Risky prompts:**
- ll017 (Copa del Rey top-scorer tables are long because of ties; the count may run high). ll065 (the Real Sociedad 2022–23 goalscorer table is only partly linked; it may fall below 12).
- ll124: `List of Valencia CF players` is stale (stops around 2020), so this prompt uses season-page squad tables instead. Those use a non-template wikitable format, so the scraper needs a custom parser.
- Transfers (ll126–ll133, ll195, ll198, ll199): the In/Out tables mix loan returns, academy promotions and loans. The scraper must filter on the "type" column.
- Category ∩ prompts (ll136–ll147): categories can lag or include youth/B-team players. For example, Saúl Ñíguez wasn't yet in Sevilla's category. ll136 can use the Madrid derby list as its primary source.
- ll091 (two-step scrape: Primera Federación teams ∩ former La Liga clubs), ll097 (country answers from section headings), ll104 (broadcaster list is rough; mixes channels and companies), ll106 (small and mixed venues), ll135 (17 answers; depends on a top-50 list that changes).
- ll036 Don Balón: the page also lists referees, which must be excluded.
- Near the upper bound: ll151 (102), ll188 (100), ll184 (96, including the pre-Liga F era), ll119 (90).
- Rough counts not parsed: ll053, ll085–ll087, ll089, ll090, ll092, ll093, ll110, ll111, ll120.
- Women's prompts (ll181–ll185, ll189) are well sourced but have lower page views, so rarity tiers may be compressed.
- Ranges ending in 2026–27 (ll084, ll098, ll101–ll103, ll125) and the "since 20xx" filters will grow as the season goes on. Re-scrape before release.
