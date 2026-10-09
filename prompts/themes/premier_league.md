# Premier League theme: prompt catalog

Theme: English football in the Premier League era (1992 onward): PL clubs, players, managers, records, seasons, awards, FA Cup, League Cup, Community Shield, EFL/Championship promotion. Id prefix `pl`.

Conventions used below:
- `en:X` is an English Wikipedia page title. Every title cited has been checked with the MediaWiki API (redirects followed). A range like `en:2015–16 Liverpool F.C. season … en:2023–24 Liverpool F.C. season` means every season page in between; the full range was verified as well.
- "Season squad" means a player listed with at least 1 **Premier League** appearance (sub appearances count) in the club season article's squad statistics table, unless the notes say otherwise.
- "List of foreign PL players" refers to `en:List of foreign Premier League players`. Each player there has a span of PL seasons. "Since 2015–16" means the span reaches 2015–16 or later (an open span like "2020–" counts).
- Estimates come from the sources (fetched and parsed where marked ✓) or from my own knowledge of the season pages.

## Awards & honours

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| pl001 | Name a player who has won Premier League Player of the Month since 2015–16 | en:Premier League Player of the Month | 58 | modern | Mohamed Salah, Erling Haaland, Harry Kane, Bryan Mbeumo, Igor Thiago | ✓ 55 unique by parse; rows from August 2015 onward |
| pl002 | Name a manager who has won Premier League Manager of the Month since 2015–16 | en:Premier League Manager of the Month | 43 | modern | Pep Guardiola, Jürgen Klopp, Mikel Arteta, Andoni Iraola, Sergej Jakirović | ✓ 43 by parse |
| pl003 | Name a player who has won Premier League Goal of the Month since 2015–16 | en:Premier League Goal of the Month | 75 | modern | Marcus Rashford, Alejandro Garnacho, Michael Olise, Kaoru Mitoma, William Osula | ✓ 76 by parse |
| pl004 | Name a goalkeeper who has won Premier League Save of the Month | en:Premier League Save of the Month | 21 | modern | Alisson Becker, David Raya, Jordan Pickford, Mark Flekken, Thomas Kaminski | ✓ 21; the award only dates from the 2020s, so it is modern by construction |
| pl005 | Name a player picked in the PFA Premier League Team of the Year since 2015–16 | en:PFA Team of the Year (2010s); en:PFA Team of the Year (2020s) | 72 | modern | Mohamed Salah, Virgil van Dijk, N'Golo Kanté, Kieran Trippier, Danny Rose | ✓ 72; only the "Premier League" sub-tables of the 2015–16 to 2025–26 sections |
| pl006 | Name a player picked in the PFA Championship Team of the Year since 2019–20 | en:PFA Team of the Year (2010s); en:PFA Team of the Year (2020s) | 60 | modern | Aleksandar Mitrović, Ivan Toney, Crysencio Summerville, Chuba Akpom, Borja Sainz | ✓ the "Championship" sub-tables (103 since 2015–16, so 2019–20 onward keeps it under 120) |
| pl007 | Name a player who has won EFL Championship Player of the Month since 2015–16 | en:EFL Championship Player of the Month | 85 | modern | Aleksandar Mitrović, Ivan Toney, Jarrod Bowen, Crysencio Summerville, Adrian Segečić | ✓ 89 by parse |
| pl008 | Name a manager who has won EFL Championship Manager of the Month since 2015–16 | en:EFL Championship Manager of the Month | 55 | modern | Marcelo Bielsa, Vincent Kompany, Kieran McKenna, Daniel Farke, Tonda Eckert | ✓ about 55 (the parse picked up some pre-2015 names, so re-filter by row year) |
| pl009 | Name an EFL League One Player of the Month winner since 2020–21 | en:EFL League One Player of the Month | 45 | modern | Jonson Clarke-Harris, Alfie May, Will Keane, Jonathan Wilson-Esbrand | deep-cut prompt; check how many winners have articles before shipping |
| pl010 | Name a winner of the PFA Young Player of the Year since 1999–2000 | en:PFA Young Player of the Year | 26 | 2000s+ | Wayne Rooney, Gareth Bale, Phil Foden, Bukayo Saka, Cole Palmer | the all-time list is about 50; filter to 2000 onward |
| pl011 | Name a player who has won Premier League Goal of the Season | en:Premier League Goal of the Season | 30 | 2000s+ | Wayne Rooney, Son Heung-min, Alejandro Garnacho, Erik Lamela, Emre Can | full winners table |
| pl012 | Name a winner of Premier League Manager of the Season | en:Premier League Manager of the Season | 15 | 2000s+ | Alex Ferguson, Pep Guardiola, Jürgen Klopp, Mikel Arteta, George Burley | dedupe repeat winners; about 15 unique |
| pl013 | Name a Premier League Hall of Fame inductee | en:Premier League Hall of Fame | 32 | 2000s+ | Thierry Henry, Alan Shearer, Wayne Rooney, Yaya Touré, Jermain Defoe | players and managers (Ferguson, Wenger) |
| pl014 | Name a winner of the Alan Hardaker Trophy (League Cup final man of the match) | en:Alan Hardaker Trophy | 30 | 2000s+ | Vincent Kompany, Virgil van Dijk, John Terry, Des Walker | the award dates from 1990, so it is nearly all PL era |
| pl015 | Name a winner of the LMA Manager of the Year award | en:League Managers Association Awards | 28 | 2000s+ | Alex Ferguson, Jürgen Klopp, Claudio Ranieri, Kieran McKenna | "LMA Manager of the Year" table, 1993 onward |
| pl016 | Name a winner of Chelsea's Player of the Season award since 2000 | en:Chelsea F.C. Player of the Season | 18 | 2000s+ | Frank Lampard, Eden Hazard, Cole Palmer, Juan Mata, Mason Mount | filter rows 1999–2000 onward |
| pl017 | Name a winner of Manchester United's Sir Matt Busby Player of the Year since 2000 | en:Sir Matt Busby Player of the Year | 17 | 2000s+ | Cristiano Ronaldo, David de Gea, Bruno Fernandes, Ander Herrera, Gabriel Heinze | filter 1999–2000 onward |
| pl018 | Name a Premier League winner of the PFA Fans' Player of the Year | en:PFA Fans' Player of the Year | 20 | 2000s+ | Steven Gerrard, Thierry Henry, Riyad Mahrez, Cole Palmer | the page also lists lower divisions; keep only the top-flight column |
| pl019 | Name a player picked in the PFA Premier League Team of the Year in the 2000s | en:PFA Team of the Year (2000s) | 60 | 2000s+ | Thierry Henry, Steven Gerrard, John Terry, Ashley Cole, Shay Given | ✓ 60; "FA Premier League" sub-tables, 2000–01 to 2009–10 |
| pl020 | Name a player picked in the PFA Premier League Team of the Year in the 1990s | en:PFA Team of the Year (1990s) | 55 | classic | Alan Shearer, Eric Cantona, Dennis Bergkamp, Gary Pallister, Tim Flowers | ✓ about 55; 1992–93 to 1999–2000, top-flight sub-tables only |
| pl021 | Name a winner of the EFL Championship Player of the Season award | en:EFL Awards | 20 | 2000s+ | Teemu Pukki, Ollie Watkins, Chuba Akpom, Aleksandar Mitrović | one per yearly section, 2006 to 2026 |

## Goals, hat-tricks & season stats

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| pl022 | Name a player who has scored a Premier League hat-trick since 2015 | en:List of Premier League hat-tricks | 72 | modern | Erling Haaland, Mohamed Salah, Son Heung-min, Chris Wood, Aleksandar Mitrović | ✓ 69+ unique; dated 2015-08-01 onward. The parse missed about 28 rows, so the true count is a bit higher |
| pl023 | Name a player who has scored a Premier League hat-trick for a club outside the "Big Six" since 2015 | en:List of Premier League hat-tricks | 35 | modern | Jamie Vardy, Chris Wood, Aleksandar Mitrović, Michail Antonio, Callum Wilson | Big Six = Arsenal, Chelsea, Liverpool, Man City, Man Utd, Tottenham; scoring side is the bolded score |
| pl024 | Name a player who has scored four or more goals in a single Premier League match | en:List of Premier League hat-tricks | 32 | 2000s+ | Sergio Agüero, Jermain Defoe, Dimitar Berbatov, Andy Cole, Efan Ekoku | ✓ 32; rows with the 4/5 superscript |
| pl025 | Name a player who has scored a Premier League hat-trick for Chelsea | en:List of Premier League hat-tricks | 23 | 2000s+ | Didier Drogba, Frank Lampard, Eden Hazard, Cole Palmer, Gianluca Vialli | ✓ 23 |
| pl026 | Name a player who has scored a Premier League hat-trick for Arsenal | en:List of Premier League hat-tricks | 21 | 2000s+ | Thierry Henry, Robin van Persie, Pierre-Emerick Aubameyang, Ian Wright, Nwankwo Kanu | ✓ 21 |
| pl027 | Name a player who has scored a Premier League hat-trick for Manchester City | en:List of Premier League hat-tricks | 18 | modern | Erling Haaland, Sergio Agüero, Raheem Sterling, Gabriel Jesus, Edin Džeko | ✓ 18; mostly from the 2010s and later |
| pl028 | Name a player who has scored a Premier League hat-trick for Liverpool | en:List of Premier League hat-tricks | 16 | 2000s+ | Mohamed Salah, Robbie Fowler, Luis Suárez, Michael Owen, Yossi Benayoun | ✓ 16 |
| pl029 | Name a player who has scored a Premier League hat-trick for Manchester United | en:List of Premier League hat-tricks | 16 | 2000s+ | Wayne Rooney, Cristiano Ronaldo, Robin van Persie, Dimitar Berbatov, Andy Cole | ✓ 16 |
| pl030 | Name a player who has scored 20+ Premier League goals in a single season since 2015–16 | en:2015–16 Premier League … en:2025–26 Premier League (Top scorers) | 25 | modern | Erling Haaland, Mohamed Salah, Harry Kane, Cole Palmer, Danny Ings | every 20+ scorer appears in the top-scorers tables |
| pl031 | Name a player who featured in a Premier League season's top-scorers table since 2015–16 | en:2015–16 Premier League … en:2025–26 Premier League (Top scorers) | 70 | modern | Erling Haaland, Son Heung-min, Chris Wood, Yoane Wissa, Jean-Philippe Mateta | ✓ about 11 rows a season; union is about 70 after removing club and award links |
| pl032 | Name a goalkeeper who featured in a Premier League season's clean-sheets table since 2015–16 | en:2015–16 Premier League … en:2025–26 Premier League (Clean sheets) | 40 | modern | Alisson Becker, Ederson, David Raya, Matz Sels, Łukasz Fabiański | ✓ about 10 a season; union about 40 |
| pl033 | Name a player who featured in an EFL Championship season's top-scorers table since 2020–21 | en:2020–21 EFL Championship … en:2025–26 EFL Championship (Top scorers) | 45 | modern | Aleksandar Mitrović, Ivan Toney, Chuba Akpom, Sammie Szmodics, Josh Sargent | |
| pl034 | Name a player who has finished a season as the Championship's top scorer since 2010–11 | en:EFL Championship (Top scorers) | 16 | modern | Aleksandar Mitrović, Ivan Toney, Glenn Murray, Chuba Akpom | include joint top scorers |

## Title-winning & iconic squads

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| pl035 | Name a player who played in the Premier League for Leicester City in their 2015–16 title season | en:2015–16 Leicester City F.C. season | 26 | modern | Jamie Vardy, Riyad Mahrez, N'Golo Kanté, Danny Drinkwater, Daniel Amartey | PL appearances ≥ 1 |
| pl036 | Name a player who played in the Premier League for Chelsea in 2016–17 (Conte's title) | en:2016–17 Chelsea F.C. season | 25 | modern | Eden Hazard, N'Golo Kanté, Diego Costa, Marcos Alonso, Nathan Aké | |
| pl037 | Name a player who played in the Premier League for Manchester City in 2017–18 (the 100-point "Centurions") | en:2017–18 Manchester City F.C. season | 25 | modern | Kevin De Bruyne, Sergio Agüero, Leroy Sané, Fabian Delph, Brahim Díaz | |
| pl038 | Name a player who played in the Premier League for Manchester City in 2018–19 (the domestic treble) | en:2018–19 Manchester City F.C. season | 24 | modern | Raheem Sterling, Bernardo Silva, Vincent Kompany, Oleksandr Zinchenko, Phil Foden | |
| pl039 | Name a player who played in the Premier League for Liverpool in 2018–19 (97 points) | en:2018–19 Liverpool F.C. season | 25 | modern | Sadio Mané, Virgil van Dijk, Xherdan Shaqiri, Divock Origi, Alberto Moreno | |
| pl040 | Name a player who played in the Premier League for Liverpool in their 2019–20 title season | en:2019–20 Liverpool F.C. season | 25 | modern | Mohamed Salah, Jordan Henderson, Roberto Firmino, Adam Lallana, Neco Williams | |
| pl041 | Name a player who played in the Premier League for Manchester City in 2022–23 (the treble) | en:2022–23 Manchester City F.C. season | 25 | modern | Erling Haaland, Rodri, Jack Grealish, Cole Palmer, Sergio Gómez | |
| pl042 | Name a player who played in the Premier League for Arsenal in 2023–24 (89 points, runners-up) | en:2023–24 Arsenal F.C. season | 26 | modern | Bukayo Saka, Declan Rice, Kai Havertz, Jakub Kiwior, Reiss Nelson | |
| pl043 | Name a player who played in the Premier League for Aston Villa in 2023–24 (Champions League qualification) | en:2023–24 Aston Villa F.C. season | 28 | modern | Ollie Watkins, John McGinn, Emiliano Martínez, Moussa Diaby, Nicolò Zaniolo | |
| pl044 | Name a player who played in the Premier League for Liverpool in their 2024–25 title season | en:2024–25 Liverpool F.C. season | 28 | modern | Mohamed Salah, Ryan Gravenberch, Virgil van Dijk, Jarell Quansah, Federico Chiesa | sample answers checked against the page |
| pl045 | Name a player who played in the Premier League for Arsenal in their 2025–26 title season | en:2025–26 Arsenal F.C. season | 30 | modern | Bukayo Saka, Declan Rice, Viktor Gyökeres, Martín Zubimendi, Myles Lewis-Skelly | Arsenal were champions on 24 May 2026 per en:2025–26 Premier League; samples checked |
| pl046 | Name a player who played in the Premier League for Arsenal's 2003–04 "Invincibles" | en:2003–04 Arsenal F.C. season | 22 | 2000s+ | Thierry Henry, Patrick Vieira, Robert Pires, Kolo Touré, Jérémie Aliadière | |
| pl047 | Name a player who played in the Premier League for Chelsea in 2004–05 (Mourinho's first title) | en:2004–05 Chelsea F.C. season | 28 | 2000s+ | Frank Lampard, John Terry, Didier Drogba, Mateja Kežman, Alexey Smertin | |
| pl048 | Name a player who played in the Premier League for Manchester United in 2007–08 | en:2007–08 Manchester United F.C. season | 28 | 2000s+ | Cristiano Ronaldo, Wayne Rooney, Carlos Tevez, Nani, Chris Eagles | |
| pl049 | Name a player who played in the Premier League for Manchester City in 2011–12 (the "Agüeroooo" title) | en:2011–12 Manchester City F.C. season | 25 | 2000s+ | Sergio Agüero, David Silva, Vincent Kompany, Edin Džeko, Owen Hargreaves | |
| pl050 | Name a player who played in the Premier League for Manchester United in 1998–99 (the treble) | en:1998–99 Manchester United F.C. season | 30 | classic | David Beckham, Ryan Giggs, Dwight Yorke, Teddy Sheringham, Jonathan Greening | |
| pl051 | Name a player who played in the Premier League for Arsenal in 1997–98 (Wenger's first double) | en:1997–98 Arsenal F.C. season | 25 | classic | Dennis Bergkamp, Marc Overmars, Patrick Vieira, Nicolas Anelka, Alberto Méndez | |
| pl052 | Name a player who played in the Premier League for Blackburn Rovers in their 1994–95 title season | en:1994–95 Blackburn Rovers F.C. season | 22 | classic | Alan Shearer, Chris Sutton, Graeme Le Saux, Tim Flowers, Robbie Slater | |
| pl053 | Name a player who played in the Premier League for Everton in 2024–25, their final season at Goodison Park | en:2024–25 Everton F.C. season | 27 | modern | Jordan Pickford, Dominic Calvert-Lewin, Iliman Ndiaye, Jarrad Branthwaite, Jesper Lindstrøm | |
| pl054 | Name a player who played in the Premier League for Keegan's Newcastle "Entertainers" in 1995–96 | en:1995–96 Newcastle United F.C. season | 25 | classic | Les Ferdinand, David Ginola, Faustino Asprilla, Peter Beardsley, Darren Huckerby | |

## Club eras (multi-season squads)

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| pl055 | Name a player who played in the Premier League for Liverpool in the Klopp era (2015–16 to 2023–24) | en:2015–16 Liverpool F.C. season … en:2023–24 Liverpool F.C. season | 100 | modern | Mohamed Salah, Roberto Firmino, Sadio Mané, Divock Origi, Sheyi Ojo | season-based rule, so a few early 2015–16 Rodgers-only players (e.g. Kolo Touré) slip in; acceptable |
| pl056 | Name a player who played in the Premier League for Arsenal in the Arteta era (2019–20 onward) | en:2019–20 Arsenal F.C. season … en:2025–26 Arsenal F.C. season | 90 | modern | Bukayo Saka, Martin Ødegaard, Gabriel Martinelli, Pablo Marí, Cédric Soares | 2019–20 includes pre-Arteta appearances (Emery); acceptable |
| pl057 | Name a player who played in the Premier League for Manchester United in Ten Hag's two full seasons (2022–23, 2023–24) | en:2022–23 Manchester United F.C. season; en:2023–24 Manchester United F.C. season | 50 | modern | Marcus Rashford, Bruno Fernandes, Antony, Wout Weghorst, Hannibal Mejbri | |
| pl058 | Name a player who played in the Premier League for Manchester United in 2024–25 or 2025–26 | en:2024–25 Manchester United F.C. season; en:2025–26 Manchester United F.C. season | 45 | modern | Bruno Fernandes, Amad Diallo, Bryan Mbeumo, Matheus Cunha, Chido Obi | Amorim/Carrick period; samples checked |
| pl059 | Name a player who played in the Premier League for Tottenham under Postecoglou (2023–24, 2024–25) | en:2023–24 Tottenham Hotspur F.C. season; en:2024–25 Tottenham Hotspur F.C. season | 45 | modern | Son Heung-min, James Maddison, Micky van de Ven, Timo Werner, Mikey Moore | |
| pl060 | Name a player who played in the Premier League for Chelsea since the 2022 BlueCo takeover | en:2022–23 Chelsea F.C. season … en:2025–26 Chelsea F.C. season | 90 | modern | Cole Palmer, Enzo Fernández, Moisés Caicedo, Mykhailo Mudryk, David Datro Fofana | 2022–23 includes a few Tuchel-era players; fine |
| pl061 | Name a player who played in the Premier League for Newcastle since the 2021 PIF takeover | en:2021–22 Newcastle United F.C. season … en:2025–26 Newcastle United F.C. season | 60 | modern | Alexander Isak, Bruno Guimarães, Kieran Trippier, Elliot Anderson, Matt Targett | |
| pl062 | Name a player who has played in the Premier League for Brentford (2021–22 onward) | en:2021–22 Brentford F.C. season … en:2025–26 Brentford F.C. season | 60 | modern | Ivan Toney, Bryan Mbeumo, Yoane Wissa, Christian Eriksen, Saman Ghoddos | covers Brentford's whole PL history |
| pl063 | Name a player who has played in the Premier League for Nottingham Forest since their 2022 promotion | en:2022–23 Nottingham Forest F.C. season … en:2025–26 Nottingham Forest F.C. season | 70 | modern | Morgan Gibbs-White, Chris Wood, Anthony Elanga, Jesse Lingard, Emmanuel Dennis | Forest used about 30 players in 2022–23 alone |
| pl064 | Name a player who has played in the Premier League for Brighton (2017–18 onward) | en:2017–18 Brighton & Hove Albion F.C. season … en:2025–26 Brighton & Hove Albion F.C. season | 100 | modern | Kaoru Mitoma, Alexis Mac Allister, Leandro Trossard, Glenn Murray, Anthony Knockaert | |
| pl065 | Name a player who has played in the Premier League for Bournemouth since their 2022 return | en:2022–23 AFC Bournemouth season … en:2025–26 AFC Bournemouth season | 55 | modern | Antoine Semenyo, Dominic Solanke, Milos Kerkez, Justin Kluivert, Illia Zabarnyi | |
| pl066 | Name a player who played in the Premier League for Wolves between 2018–19 and 2025–26 | en:2018–19 Wolverhampton Wanderers F.C. season … en:2025–26 Wolverhampton Wanderers F.C. season | 95 | modern | Rúben Neves, Raúl Jiménez, Adama Traoré, Matheus Cunha, Hwang Hee-chan | Wolves were relegated in 2026 |
| pl067 | Name a player who has played in the Premier League for Leeds since 2020 (2020–23 and 2025–26) | en:2020–21 Leeds United F.C. season; en:2021–22 Leeds United F.C. season; en:2022–23 Leeds United F.C. season; en:2025–26 Leeds United F.C. season | 70 | modern | Patrick Bamford, Raphinha, Kalvin Phillips, Brenden Aaronson, Joël Piroe | samples checked |
| pl068 | Name a player who played in the Premier League for Luton Town in 2023–24 | en:2023–24 Luton Town F.C. season | 30 | modern | Ross Barkley, Carlton Morris, Elijah Adebayo, Tom Lockyer, Chiedozie Ogbene | samples checked |
| pl069 | Name a player who played in the Premier League for Ipswich Town in 2024–25 | en:2024–25 Ipswich Town F.C. season | 35 | modern | Liam Delap, Omari Hutchinson, Kalvin Phillips, Sam Morsy, Leif Davis | samples checked |
| pl070 | Name a player who played in the Premier League for Sunderland in 2025–26 | en:2025–26 Sunderland A.F.C. season | 30 | modern | Granit Xhaka, Enzo Le Fée, Wilson Isidor, Habib Diarra, Chemsdine Talbi | samples checked |
| pl071 | Name a player who has played in the Premier League for Aston Villa since their 2019 promotion | en:2019–20 Aston Villa F.C. season … en:2025–26 Aston Villa F.C. season | 85 | modern | Ollie Watkins, Jack Grealish, Emiliano Martínez, Leon Bailey, Jhon Durán | |
| pl072 | Name a player who played in the Premier League for Southampton in 2024–25 | en:2024–25 Southampton F.C. season | 33 | modern | Kyle Walker-Peters, Tyler Dibling, Aaron Ramsdale, Adam Armstrong, Ben Brereton Díaz | relegated with a record-low points tally |
| pl073 | Name a player who played in the Premier League for Crystal Palace between 2023–24 and 2025–26 | en:2023–24 Crystal Palace F.C. season … en:2025–26 Crystal Palace F.C. season | 45 | modern | Jean-Philippe Mateta, Eberechi Eze, Marc Guéhi, Daniel Muñoz, Will Hughes | the Glasner era (FA Cup 2025, Conference League 2026) |

## Managers

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| pl074 | Name a manager who has taken charge of a Premier League club since August 2020 (caretakers included) | en:List of Premier League managers | 92 | modern | Pep Guardiola, Mikel Arteta, Ange Postecoglou, Andoni Iraola, Simon Ireland | ✓ 92 by parse (tenure ending 2020 or later, or ongoing) |
| pl075 | Name a caretaker manager who took charge of a Premier League club since 2015 | en:List of Premier League managers | 40 | modern | Ryan Mason, Michael Carrick, Ruud van Nistelrooy, Darren Moore, Mike Jackson | ✓ 25 caretakers (double dagger) since 2020 alone; about 40 since 2015 |
| pl076 | Name a manager sacked by a Premier League club since 2015–16 | en:2015–16 Premier League … en:2025–26 Premier League (Managerial changes) | 70 | modern | José Mourinho, Erik ten Hag, Frank Lampard, Claudio Ranieri, Paul Clement | "Manner of departure" = Sacked; deduplicate |
| pl077 | Name a manager who managed a Premier League club during the 2015–16 season | en:2015–16 Premier League (Personnel and kits; Managerial changes) | 32 | modern | Claudio Ranieri, Jürgen Klopp, Louis van Gaal, Mauricio Pochettino, Rémi Garde | caretakers included |
| pl078 | Name a manager in charge of a Premier League club in 2026–27 | en:2026–27 Premier League (Personnel and kits; Managerial changes) | 23 | modern | Mikel Arteta, Xabi Alonso, Frank Lampard, Michael Carrick, Sergej Jakirović | ✓ current season; freeze the list at scrape date |
| pl079 | Name a manager of a "Big Six" club since 2015 (caretakers included) | en:List of Arsenal F.C. managers; en:List of Chelsea F.C. managers; en:List of Liverpool F.C. managers; en:List of Manchester City F.C. managers; en:List of Manchester United F.C. managers; en:List of Tottenham Hotspur F.C. managers | 42 | modern | Jürgen Klopp, José Mourinho, Mauricio Pochettino, Thomas Tuchel, Cristian Stellini | anyone in charge on or after 1 July 2015 |
| pl080 | Name a manager who has won the FA Cup or League Cup since 2015 | en:List of FA Cup finals; en:List of EFL Cup finals | 14 | modern | Pep Guardiola, Jürgen Klopp, Mikel Arteta, Oliver Glasner, Eddie Howe | winning managers 2015–2026; take the manager from each final's article |
| pl081 | Name a manager who managed a Championship club in 2025–26 | en:2025–26 EFL Championship (Personnel and sponsoring; Managerial changes) | 35 | modern | Frank Lampard, Kieran McKenna, Sergej Jakirović, Tonda Eckert | the personnel section heading differs from the PL page; locate the manager table |
| pl082 | Name a manager who won promotion from the Championship to the Premier League since 2015–16 | en:EFL Championship (League champions, runners-up and play-off finalists); club season articles | 28 | modern | Marcelo Bielsa, Vincent Kompany, Daniel Farke, Chris Wilder, Rob Edwards | champions, runners-up and play-off winners 2016–2026 |
| pl083 | Name a Spanish or Portuguese manager who has managed in the Premier League | en:List of Premier League managers | 25 | modern | Pep Guardiola, José Mourinho, Mikel Arteta, Nuno Espírito Santo, Javi Gracia | use the nationality flag column; caretakers included |
| pl084 | Name an Italian manager who has managed in the Premier League | en:List of Premier League managers | 16 | 2000s+ | Carlo Ancelotti, Antonio Conte, Roberto Mancini, Enzo Maresca, Walter Mazzarri | |
| pl085 | Name a manager who has managed 300+ Premier League matches | en:List of Premier League managers (Most games managed in the Premier League) | 20 | 2000s+ | Arsène Wenger, Alex Ferguson, David Moyes, Sean Dyche, Joe Kinnear | ✓ the top-20 table ends at 302 games, so all 20 rows qualify |
| pl086 | Name a manager of Tottenham Hotspur since 1992 (caretakers included) | en:List of Tottenham Hotspur F.C. managers | 28 | 2000s+ | Mauricio Pochettino, Harry Redknapp, José Mourinho, Juande Ramos, Christian Gross | |
| pl087 | Name a manager of Newcastle United since 1992 (caretakers included) | en:List of Newcastle United F.C. managers | 20 | 2000s+ | Kevin Keegan, Bobby Robson, Rafael Benítez, Eddie Howe, Joe Kinnear | |
| pl088 | Name a manager of Everton since 1992 (caretakers included) | en:List of Everton F.C. managers | 22 | 2000s+ | David Moyes, Carlo Ancelotti, Sean Dyche, Ronald Koeman, Duncan Ferguson | |
| pl089 | Name a manager of Manchester City since 1992 (caretakers included) | en:List of Manchester City F.C. managers | 18 | 2000s+ | Pep Guardiola, Roberto Mancini, Manuel Pellegrini, Kevin Keegan, Frank Clark | |
| pl090 | Name a manager of West Ham United since 1992 (caretakers included) | en:List of West Ham United F.C. managers | 17 | 2000s+ | Harry Redknapp, David Moyes, Manuel Pellegrini, Julen Lopetegui, Avram Grant | |
| pl091 | Name a manager of Aston Villa since 1992 (caretakers included) | en:List of Aston Villa F.C. managers | 22 | 2000s+ | Martin O'Neill, Unai Emery, Steven Gerrard, Dean Smith, Rémi Garde | |
| pl092 | Name a manager of Watford since 2012 (the Pozzo era, caretakers included) | en:List of Watford F.C. managers | 22 | modern | Quique Sánchez Flores, Javi Gracia, Marco Silva, Claudio Ranieri, Óscar García | famous for its managerial churn |
| pl093 | Name a manager of Crystal Palace since 2010 (caretakers included) | en:List of Crystal Palace F.C. managers | 18 | modern | Oliver Glasner, Roy Hodgson, Alan Pardew, Patrick Vieira, Frank de Boer | |
| pl094 | Name a manager of Southampton since 2010 (caretakers included) | en:List of Southampton F.C. managers | 18 | modern | Mauricio Pochettino, Ronald Koeman, Ralph Hasenhüttl, Russell Martin, Ivan Jurić | |
| pl095 | Name a manager of Leeds United since 2010 (caretakers included) | en:List of Leeds United F.C. managers | 22 | modern | Marcelo Bielsa, Daniel Farke, Jesse Marsch, Javi Gracia, Darko Milanič | |
| pl096 | Name a manager of Leicester City since 2000 (caretakers included) | en:List of Leicester City F.C. managers | 25 | 2000s+ | Claudio Ranieri, Brendan Rodgers, Enzo Maresca, Craig Shakespeare, Ruud van Nistelrooy | |
| pl097 | Name a manager of Sunderland since 2000 (caretakers included) | en:List of Sunderland A.F.C. managers | 25 | 2000s+ | Roy Keane, Steve Bruce, David Moyes, Paolo Di Canio, Régis Le Bris | |
| pl098 | Name a manager of Liverpool (caretakers included) | en:List of Liverpool F.C. managers | 22 | classic | Jürgen Klopp, Bill Shankly, Kenny Dalglish, Rafael Benítez, Roy Evans | iconic all-time list |
| pl099 | Name a manager who managed in the inaugural 1992–93 Premier League season | en:1992–93 FA Premier League | 28 | classic | Alex Ferguson, Kenny Dalglish, George Graham, Joe Royle, Ian Porterfield | managers table plus mid-season changes |

## Nationalities in the Premier League

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| pl100 | Name a Brazilian who has played in the Premier League since 2015–16 | List of foreign PL players (Brazil) | 90 | modern | Roberto Firmino, Gabriel Jesus, Casemiro, Bruno Guimarães, Igor Thiago | ✓ 90 |
| pl101 | Name a Spanish player who has played in the Premier League since 2015–16 | List of foreign PL players (Spain) | 115 | modern | Rodri, Marc Cucurella, Pedro Porro, David de Gea, Bojan | ✓ 119; near the 120 cap. Switch to 2018–19 onward if the scrape exceeds 120 |
| pl102 | Name a French player who has played in the Premier League since 2020–21 | List of foreign PL players (France) | 81 | modern | William Saliba, N'Golo Kanté, Jean-Philippe Mateta, Alexandre Lacazette, Malo Gusto | ✓ 81 (2015+ would be 120) |
| pl103 | Name a Portuguese player who has played in the Premier League since 2015–16 | List of foreign PL players (Portugal) | 61 | modern | Bruno Fernandes, Bernardo Silva, Rúben Dias, Diogo Jota, Hélder Costa | ✓ 61 |
| pl104 | Name a Dutch player who has played in the Premier League since 2015–16 | List of foreign PL players (Netherlands) | 79 | modern | Virgil van Dijk, Ryan Gravenberch, Cody Gakpo, Georginio Wijnaldum, Daryl Janmaat | ✓ 79 |
| pl105 | Name a German player who has played in the Premier League since 2015–16 | List of foreign PL players (Germany) | 54 | modern | İlkay Gündoğan, Kai Havertz, Antonio Rüdiger, Timo Werner, Lukas Nmecha | ✓ 54 |
| pl106 | Name a Belgian player who has played in the Premier League since 2015–16 | List of foreign PL players (Belgium) | 52 | modern | Kevin De Bruyne, Eden Hazard, Romelu Lukaku, Leandro Trossard, Roméo Lavia | ✓ 52 |
| pl107 | Name an Argentine player who has played in the Premier League since 2015–16 | List of foreign PL players (Argentina) | 47 | modern | Alexis Mac Allister, Lisandro Martínez, Enzo Fernández, Julián Álvarez, Facundo Buonanotte | ✓ 47 |
| pl108 | Name a Danish player who has played in the Premier League since 2015–16 | List of foreign PL players (Denmark) | 38 | modern | Christian Eriksen, Rasmus Højlund, Pierre-Emile Højbjerg, Kasper Schmeichel, Mathias Jensen | ✓ 38 |
| pl109 | Name a Norwegian player who has played in the Premier League since 2015–16 | List of foreign PL players (Norway) | 23 | modern | Erling Haaland, Martin Ødegaard, Alexander Sørloth, Jørgen Strand Larsen, Kristoffer Ajer | ✓ 23 |
| pl110 | Name an Ivorian player who has played in the Premier League since 2015–16 | List of foreign PL players (Ivory Coast) | 36 | modern | Wilfried Zaha, Nicolas Pépé, Sébastien Haller, Eric Bailly, Simon Adingra | ✓ 36 |
| pl111 | Name a Nigerian player who has played in the Premier League since 2015–16 | List of foreign PL players (Nigeria) | 33 | modern | Kelechi Iheanacho, Wilfred Ndidi, Alex Iwobi, Ola Aina, Joe Aribo | ✓ 33 |
| pl112 | Name a Senegalese player who has played in the Premier League since 2015–16 | List of foreign PL players (Senegal) | 31 | modern | Sadio Mané, Kalidou Koulibaly, Édouard Mendy, Ismaïla Sarr, Pape Matar Sarr | ✓ 31 |
| pl113 | Name a Ghanaian player who has played in the Premier League since 2015–16 | List of foreign PL players (Ghana) | 22 | modern | Thomas Partey, Mohammed Kudus, Antoine Semenyo, Jordan Ayew, Mohammed Salisu | ✓ 22 |
| pl114 | Name an American player who has played in the Premier League since 2015–16 | List of foreign PL players (United States) | 25 | modern | Christian Pulisic, Antonee Robinson, Tyler Adams, Matt Turner, Brenden Aaronson | ✓ 25 |
| pl115 | Name a Colombian player who has played in the Premier League since 2015–16 | List of foreign PL players (Colombia) | 21 | modern | Luis Díaz, Davinson Sánchez, Jhon Durán, Yerry Mina, Daniel Muñoz | ✓ 21 |
| pl116 | Name a Moroccan player who has played in the Premier League since 2015–16 | List of foreign PL players (Morocco) | 19 | modern | Hakim Ziyech, Noussair Mazraoui, Nayef Aguerd, Sofiane Boufal, Romain Saïss | ✓ 19 |
| pl117 | Name a Japanese player who has played in the Premier League | List of foreign PL players (Japan) | 20 | modern | Kaoru Mitoma, Takehiro Tomiyasu, Wataru Endō, Shinji Kagawa, Junichi Inamoto | ✓ 20 all-time, 15 of them since 2015 |
| pl118 | Name a South Korean player who has played in the Premier League | List of foreign PL players (Korea Republic) | 15 | 2000s+ | Son Heung-min, Park Ji-sung, Hwang Hee-chan, Ki Sung-yueng, Lee Chung-yong | ✓ 15 |
| pl119 | Name an Egyptian player who has played in the Premier League | List of foreign PL players (Egypt) | 14 | 2000s+ | Mohamed Salah, Mohamed Elneny, Omar Marmoush, Trézéguet, Mido | ✓ 14 |

## Career paths ("played for both")

These use Wikidata because no page table covers them. The SPARQL needs `p:P54/ps:P54`, not `wdt:P54`: preferred-rank current-club statements hide other clubs under `wdt`. Exclude spells whose end time (P582) is before 1993 so the answers are PL era. Wikidata has gaps and junk (youth or wartime guests, vandalised labels), so check the result against the clubs' player lists and season pages.

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| pl120 | Name a player who has played for both Chelsea and Manchester United (PL era) | Wikidata P54 Q9616 + Q18656 | 18 | 2000s+ | Juan Mata, Romelu Lukaku, Nemanja Matić, Mason Mount, Juan Sebastián Verón | ✓ 15 raw (after fixing labels) |
| pl121 | Name a player who has played for both Liverpool and Manchester City (PL era) | Wikidata P54 Q1130849 + Q50602 | 22 | 2000s+ | Raheem Sterling, James Milner, Robbie Fowler, Steve McManaman, Albert Riera | ✓ 25 raw |
| pl122 | Name a player who has played for both Liverpool and Chelsea (PL era) | Wikidata P54 Q1130849 + Q9616 | 20 | 2000s+ | Mohamed Salah, Fernando Torres, Daniel Sturridge, Joe Cole, Fabio Borini | ✓ 16 raw (missing some) |
| pl123 | Name a player who has played for both Arsenal and Manchester City (PL era) | Wikidata P54 Q9617 + Q50602 | 22 | 2000s+ | Gabriel Jesus, Raheem Sterling, Samir Nasri, Gaël Clichy, Sylvinho | ✓ 23 raw |
| pl124 | Name a player who has played for both Chelsea and Manchester City (PL era) | Wikidata P54 Q9616 + Q50602 | 22 | 2000s+ | Frank Lampard, Raheem Sterling, Nathan Aké, Shaun Wright-Phillips, Tal Ben Haim | ✓ 25 raw |
| pl125 | Name a player who has played for both Liverpool and Tottenham (PL era) | Wikidata P54 Q1130849 + Q18741 | 18 | 2000s+ | Peter Crouch, Robbie Keane, Brad Friedel, Jamie Redknapp, Neil Ruddock | ✓ 20 raw |
| pl126 | Name a player who has played for both Everton and Manchester United (PL era) | Wikidata P54 Q5794 + Q18656 | 25 | 2000s+ | Wayne Rooney, Marouane Fellaini, Romelu Lukaku, Tim Howard, Andrei Kanchelskis | ✓ 38 raw, with old-era noise |
| pl127 | Name a player who has played for both West Ham and Tottenham (PL era) | Wikidata P54 Q18747 + Q18741 | 28 | 2000s+ | Jermain Defoe, Michael Carrick, Scott Parker, Bobby Zamora, Mido | ✓ 32 raw |
| pl128 | Name a player who has played for both Newcastle and Sunderland (PL era) | Wikidata P54 Q18716 + Q18739 | 24 | 2000s+ | Andy Cole, Jack Colback, Titus Bramble, Ki Sung-yueng, Michael Chopra | ✓ 26 raw |
| pl129 | Name a player who has played for both Brighton and Chelsea (since 2010) | Wikidata P54 Q19453 + Q9616 | 13 | modern | Moisés Caicedo, Marc Cucurella, Robert Sánchez, João Pedro, Tariq Lamptey | ✓ 14 raw, some youth noise |
| pl130 | Name a player who has played for both Southampton and Liverpool (since 2000) | Wikidata P54 Q18732 + Q1130849 | 14 | modern | Virgil van Dijk, Sadio Mané, Adam Lallana, Dejan Lovren, Rickie Lambert | ✓ 11 since 2010, about 14 since 2000 (adds Crouch, Konchesky) |
| pl131 | Name a player who has played for both Leicester City and Chelsea (since 2005) | Wikidata P54 Q19481 + Q9616 | 13 | modern | N'Golo Kanté, Ben Chilwell, Wesley Fofana, Kiernan Dewsbury-Hall, Danny Drinkwater | ✓ 14 raw |

## Clubs, leagues & promotion

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| pl132 | Name a club that has played in the Championship since 2015–16 | en:2015–16 Football League Championship; en:2016–17 EFL Championship … en:2025–26 EFL Championship | 55 | modern | Leeds United, Sunderland, Wrexham, Luton Town, Rotherham United | union of the clubs tables |
| pl133 | Name a club that has played in League One since 2015–16 | en:2015–16 Football League One; en:2016–17 EFL League One … en:2025–26 EFL League One | 65 | modern | Sunderland, Portsmouth, Ipswich Town, Wigan Athletic, Accrington Stanley | |
| pl134 | Name a club that has played in League Two since 2015–16 | en:2015–16 Football League Two; en:2016–17 EFL League Two … en:2025–26 EFL League Two | 65 | modern | Wrexham, Notts County, Salford City, Bradford City, Forest Green Rovers | |
| pl135 | Name a club that has played in the National League since 2015–16 | en:2015–16 National League … en:2025–26 National League | 70 | modern | Wrexham, Notts County, Stockport County, Oldham Athletic, Dagenham & Redbridge | deep cuts; some clubs may lack articles (check) |
| pl136 | Name a club in the 2026–27 Championship | en:2026–27 EFL Championship | 24 | modern | West Ham United, Wolverhampton Wanderers, Burnley, Wrexham, Lincoln City | ✓ current season |
| pl137 | Name a club promoted to the Premier League since 2015–16 | en:EFL Championship (League champions, runners-up and play-off finalists) | 24 | modern | Leeds United, Burnley, Brentford, Coventry City, Huddersfield Town | promotions in 2016 through 2026 |
| pl138 | Name a club relegated from the Championship to League One since 2015–16 | en:EFL Championship (Relegated teams (from Championship to League One)) | 30 | modern | Wigan Athletic, Derby County, Reading, Rotherham United, Plymouth Argyle | |
| pl139 | Name a club promoted from League One to the Championship since 2015–16 | en:EFL Championship (Promoted teams (from League One to Championship)) | 30 | modern | Wrexham, Sunderland, Ipswich Town, Birmingham City, Barnsley | |
| pl140 | Name a club that has reached the Championship play-off final (2005 onward) | en:EFL Championship play-offs | 30 | 2000s+ | Leeds United, Sunderland, Brentford, Luton Town, Blackpool | winners and losers |
| pl141 | Name a club that has played in the Championship (2004–05 onward) | en:EFL Championship (Seasons in EFL Championship) | 75 | 2000s+ | Leeds United, Norwich City, Sunderland, Yeovil Town, Scunthorpe United | |
| pl142 | Name a club that has qualified for the Champions League through its Premier League finish | en:List of Premier League seasons (Seasons table, UCL column) | 13 | 2000s+ | Arsenal, Tottenham Hotspur, Newcastle United, Leicester City, Aston Villa | exclude entries qualifying as cup or UCL winners (marked); small but fun |
| pl143 | Name a club that played in the inaugural 1992–93 Premier League | en:1992–93 FA Premier League | 22 | classic | Manchester United, Arsenal, Oldham Athletic, Wimbledon, Sheffield Wednesday | |
| pl144 | Name a club that has played in the Charity/Community Shield | en:FA Community Shield | 35 | classic | Manchester United, Liverpool, Arsenal, Leicester City, Wigan Athletic | results table, all years |
| pl145 | Name a club that has reached the FA Cup final since 2000 | en:List of FA Cup finals | 22 | 2000s+ | Chelsea, Arsenal, Portsmouth, Wigan Athletic, Millwall | winners and runners-up |
| pl146 | Name a club that has reached the League Cup final since 2000 | en:List of EFL Cup finals | 24 | 2000s+ | Liverpool, Chelsea, Newcastle United, Bradford City, Cardiff City | |
| pl147 | Name a club that has reached the FA Cup semi-finals since 2015–16 | en:2015–16 FA Cup … en:2025–26 FA Cup (Semi-finals) | 24 | modern | Manchester City, Chelsea, Brighton, Coventry City, Watford | |
| pl148 | Name a club that has reached the League Cup semi-finals since 2015–16 | en:2015–16 Football League Cup; en:2016–17 EFL Cup … en:2025–26 EFL Cup (Semi-finals) | 24 | modern | Liverpool, Arsenal, Newcastle United, Burton Albion, Hull City | |
| pl149 | Name an English football derby or rivalry with its own Wikipedia article | en:List of association football rivalries in the United Kingdom (England sections) | 55 | 2000s+ | North London derby, Merseyside derby, Manchester derby, Tyne–Wear derby, M23 derby | ✓ about 60 linked derbies in the England & Wales sections; drop non-English and non-article links |

## Stadiums

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| pl150 | Name the home stadium of a 2025–26 Championship club | en:2025–26 EFL Championship (Stadiums and locations) | 24 | modern | King Power Stadium, St Mary's Stadium, Racecourse Ground, Portman Road, Kassam Stadium | ✓ |
| pl151 | Name the home stadium of a 2025–26 League One club | en:2025–26 EFL League One (Stadiums and locations) | 24 | modern | Kenilworth Road, Cardiff City Stadium, Valley Parade, Home Park, Plough Lane | ✓ |
| pl152 | Name a Premier League ground that opened in 2000 or later | en:List of Premier League stadiums (Opened column) | 15 | 2000s+ | Emirates Stadium, Tottenham Hotspur Stadium, London Stadium, Hill Dickinson Stadium, Gtech Community Stadium | |
| pl153 | Name the home stadium of a 2025–26 League Two club | en:2025–26 EFL League Two (Stadiums and locations) | 24 | modern | Memorial Stadium (Bristol), Abbey Stadium, Gresty Road, Broadfield Stadium, Holker Street | ✓ |
| pl154 | Name a football stadium in England with a capacity of 30,000 or more | en:List of football stadiums in England | 30 | modern | Wembley Stadium, Old Trafford, Anfield, Stadium of Light, Hillsborough Stadium | current capacities |

## Cup finals & big matches

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| pl155 | Name a player who started an FA Cup final from 2021 to 2026 | en:2021 FA Cup final … en:2026 FA Cup final (Details lineups) | 95 | modern | Erling Haaland, Bruno Fernandes, Eberechi Eze, Youri Tielemans, Dean Henderson | starters only (11 per side, 6 finals) |
| pl156 | Name a player who started a League Cup final from 2021 to 2026 | en:2021 EFL Cup final … en:2026 EFL Cup final (Details lineups) | 95 | modern | Mohamed Salah, Virgil van Dijk, Casemiro, Dan Burn, Caoimhín Kelleher | starters only |
| pl157 | Name a player who has scored in a League Cup final since 2000 | en:List of EFL Cup finals; individual final articles | 45 | 2000s+ | Didier Drogba, Sergio Agüero, Virgil van Dijk, Alexander Isak, Obafemi Martins | own goals excluded |
| pl158 | Name a player who has scored in the Community Shield since 2010 | en:2010 FA Community Shield … en:2026 FA Community Shield | 30 | modern | Mohamed Salah, Pierre-Emerick Aubameyang, Riyad Mahrez, Darwin Núñez, Cole Palmer | shoot-out goals excluded |
| pl159 | Name a player who has scored in an FA Cup semi-final since 2015–16 | en:2015–16 FA Cup … en:2025–26 FA Cup (Semi-finals) | 50 | modern | Bernardo Silva, Pierre-Emerick Aubameyang, Kelechi Iheanacho, Hakim Ziyech, Ismaïla Sarr | |
| pl160 | Name a player who has scored in a Championship play-off final since 2016 | en:2016 Football League Championship play-off final; en:2017 EFL Championship play-off final … en:2026 EFL Championship play-off final | 14 | modern | Ivan Toney, John McGinn, Tom Cairney, Adam Armstrong, Mohamed Diamé | 2017 final was 0–0 (Huddersfield on penalties); count could land just under 14 |
| pl161 | Name a player who started a Community Shield from 2020 to 2026 | en:2020 FA Community Shield … en:2026 FA Community Shield (Details lineups) | 100 | modern | Erling Haaland, Bukayo Saka, Mohamed Salah, Kalvin Phillips, Jamie Vardy | starters only, 7 matches; drop to 2022–2026 if the scrape exceeds 120 |

## Transfers

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| pl162 | Name a player who joined a "Big Six" club in the summer 2025 window (loans included) | en:List of English football transfers summer 2025 | 45 | modern | Florian Wirtz, Viktor Gyökeres, Benjamin Šeško, Hugo Ekitiké, Martín Zubimendi | "Moving to" = Arsenal, Chelsea, Liverpool, Man City, Man Utd, Tottenham; exclude youth and loan returns |
| pl163 | Name a player who joined a "Big Six" club in the summer 2024 window (loans included) | en:List of English football transfers summer 2024 | 40 | modern | Riccardo Calafiori, Federico Chiesa, Joshua Zirkzee, Matthijs de Ligt, Kiernan Dewsbury-Hall | same rule |
| pl164 | Name a player who joined a "Big Six" club in the summer 2023 window (loans included) | en:List of English football transfers summer 2023 | 45 | modern | Declan Rice, Mason Mount, Dominik Szoboszlai, Moisés Caicedo, Guglielmo Vicario | same rule |
| pl165 | Name a player who joined a "Big Six" club in the summer 2022 window (loans included) | en:List of English football transfers summer 2022 | 45 | modern | Erling Haaland, Darwin Núñez, Casemiro, Antony, Marc Cucurella | same rule |
| pl166 | Name a player who joined a Premier League club in the January 2026 window (loans included) | en:List of English football transfers winter 2025–26 | 70 | modern | (scrape-dependent) | "Moving to" = a 2025–26 PL club; check the count, and restrict to permanent deals if over 120 |
| pl167 | Name a player who joined a Premier League club in the January 2025 window (loans included) | en:List of English football transfers winter 2024–25 | 65 | modern | Omar Marmoush, Abdukodir Khusanov, Nico González, Mathys Tel, Kevin Danso | same rule as pl166 (2024–25 PL clubs) |

## Off the pitch: captains, owners, officials, kits & media

| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| pl168 | Name a Premier League club captain from 2015–16 to 2019–20 | en:2015–16 Premier League … en:2019–20 Premier League (Personnel and kits, Captain column) | 55 | modern | Jordan Henderson, Vincent Kompany, Wes Morgan, Troy Deeney, Ashley Williams | |
| pl169 | Name a Premier League club captain since 2020–21 | en:2020–21 Premier League … en:2026–27 Premier League (Personnel and kits, Captain column) | 60 | modern | Martin Ødegaard, Virgil van Dijk, Bruno Fernandes, Lewis Dunk, Sam Morsy | ✓ 2026–27 captains include Ødegaard, McGinn, Van Dijk, Dunk |
| pl170 | Name an owner of a 2026–27 Premier League club (person, family, fund or company) | en:List of owners of English football clubs (Premier League) | 30 | modern | Todd Boehly, Sir Jim Ratcliffe, Fenway Sports Group, Public Investment Fund, Tony Bloom | ✓ section links are noisy (industries, teams); curate to the owner column |
| pl171 | Name an owner of a Championship club | en:List of owners of English football clubs (EFL Championship) | 28 | modern | Ryan Reynolds, Rob McElhenney, Vichai Srivaddhanaprabha, Steve Gibson, Daniel Křetínský | ✓ fun Wrexham hook; curate the owner column |
| pl172 | Name a referee in the current Premier League Select Group | en:Select Group (Professional Referee Group) | 20 | modern | Michael Oliver, Craig Pawson, Simon Hooper, Chris Kavanagh, Sam Barrott | ✓ 20 linked referees (List of Premier League referees redirects here). Anthony Taylor is not in that sub-list, so check the FIFA section |
| pl173 | Name a former Premier League Select Group referee | en:Select Group (Former Select Group officials, Select Group 1, Referees) | 55 | 2000s+ | Mike Dean, Howard Webb, Mark Clattenburg, Martin Atkinson, Phil Dowd | |
| pl174 | Name a presenter or pundit on Match of the Day | en:Match of the Day (Presenters, analysts and commentators) | 45 | 2000s+ | Gary Lineker, Alan Shearer, Ian Wright, Micah Richards, Kelly Cates | current and previous presenters and analysts; commentators excluded |
| pl175 | Name a kit manufacturer used by a Premier League club since 2015–16 | en:2015–16 Premier League … en:2025–26 Premier League (Personnel and kits) | 15 | modern | Nike, Adidas, Puma, Castore, Kelme | ✓ about 15 unique (Nike, Adidas, Puma, Umbro, New Balance, Under Armour, Hummel, Macron, Castore, Joma, Kappa, Erreà, Kelme, Dryworld, Sudu) |
| pl176 | Name a company that has been a Premier League club's front-of-shirt sponsor since 2015–16 | en:2015–16 Premier League … en:2025–26 Premier League (Personnel and kits) | 45 | modern | Emirates, Etihad Airways, Standard Chartered, Stake.com, Wonga.com | ✓ 86 strings, about 45 linked; unlinked gambling brands lack articles and are dropped |
| pl177 | Name a company that has been a Premier League club's sleeve sponsor since 2017–18 | en:2017–18 Premier League … en:2025–26 Premier League (Personnel and kits, sleeve column) | 40 | modern | Visit Rwanda, OKX, Expedia, Deel, SumUp | sleeve sponsors began 2017–18; many lack articles. Samples taken from the 2026–27 table, so check they also appear in 2017–18 to 2025–26 or extend the range to 2026–27 |
| pl178 | Name a goalkeeper who made a Premier League appearance in 2025–26 | en:2025–26 Premier League; 20 club season articles (squad statistics, GK rows) | 45 | modern | David Raya, Alisson Becker, Jordan Pickford, Robin Roefs, Kepa Arrizabalaga | GK position rows with ≥ 1 PL appearance |
| pl179 | Name a goalkeeper who made a Premier League appearance in 2015–16 | en:2015–16 Premier League; 20 club season articles (squad statistics, GK rows) | 45 | modern | David de Gea, Kasper Schmeichel, Hugo Lloris, Petr Čech, Adrián | same rule as pl178, ten seasons earlier |

## Summary

**Total prompts: 179** (pl001–pl179)

**Era split**
| era | count | share |
|---|---|---|
| modern | 119 | 66% |
| 2000s+ | 51 | 28% |
| classic | 9 | 5% |

**Count per sub-heading**
| sub-heading | prompts | ids |
|---|---|---|
| Awards & honours | 21 | pl001–pl021 |
| Goals, hat-tricks & season stats | 13 | pl022–pl034 |
| Title-winning & iconic squads | 20 | pl035–pl054 |
| Club eras (multi-season squads) | 19 | pl055–pl073 |
| Managers | 26 | pl074–pl099 |
| Nationalities in the Premier League | 20 | pl100–pl119 |
| Career paths ("played for both") | 12 | pl120–pl131 |
| Clubs, leagues & promotion | 18 | pl132–pl149 |
| Stadiums | 5 | pl150–pl154 |
| Cup finals & big matches | 7 | pl155–pl161 |
| Transfers | 6 | pl162–pl167 |
| Off the pitch: captains, owners, officials, kits & media | 12 | pl168–pl179 |

**Template families:** single-season squads 20 (11%), multi-season club eras 19 (11%), nationality 20 (11%), manager-of-club lists 13 (7%), "played for both" 12 (7%), hat-trick list 8 (4%), transfer windows 6 (3%). Three families sit slightly above 10%; to get under, drop one or two of the weaker ones (e.g. pl043 Villa 2023–24, pl072 Southampton 2024–25, pl119 Egypt). Single-season and multi-season squads come from the same kind of source (club season articles) but are different prompt shapes.

**Verification:** all 268 distinct page titles cited (season ranges expanded in full) exist on en.wikipedia per the MediaWiki API. Counts marked ✓ were parsed from the live wikitext.

**Risky prompts**
- **pl120–pl131 (career paths):** depend on Wikidata P54. Coverage is incomplete (e.g. Liverpool+Chelsea returned 16 against a true count of about 20) and noisy (old players with no end-date qualifier, youth spells, vandalised labels such as "Sancho Panza" and "Juan Mata Pata"). Each needs manual curation against club player lists.
- **pl170, pl171 (owners), pl176, pl177 (shirt and sleeve sponsors):** the scrape must be curated. The owner sections link industries and sister franchises, and many betting-brand sponsors have no article.
- **pl166, pl167 (January windows):** counts unknown until scraped; may need a permanent-deals-only filter.
- **pl080 (cup-winning managers since 2015), pl129–pl131 (Brighton/Southampton/Leicester pairs), pl142 (UCL via PL finish), pl160 (play-off final scorers):** estimates are only just above the 12 floor.
- **pl101 (Spain since 2015):** 119 parsed, at the ceiling; tighten to 2018–19 onward if needed. pl161 (Community Shield starters 2020–26) could also go over 120; fallback noted.
- **pl009 (League One POTM), pl135 (National League clubs):** deep-cut lower-league answers; check article coverage.
- **pl078, pl136, pl169 (include the live 2026–27 season):** freeze the answer list at scrape date.
- **pl055, pl056, pl060:** a season-based rule labelled as a manager or owner era. A handful of boundary-season players from the previous regime are included.
- **pl172 (current referees):** Anthony Taylor does not appear in the Professional Referee Group sub-list as linked, so check which sub-sections to include.
