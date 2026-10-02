# Prompt catalog

Target: ≤ ~100 answers per prompt (hard ceiling ~130). Counts are pre-scrape estimates.
Module = file in prompts/collectors/ that implements the prompt.

## awards.py — individual honours (p004–p023)
| id | prompt | est. |
|---|---|---|
| p004 | Name a Ballon d'Or winner | 45 |
| p005 | Name a player who has finished in the top 3 of the Ballon d'Or | 80 |
| p006 | Name a winner of FIFA World Player of the Year or The Best FIFA Men's Player | 20 |
| p007 | Name a European Golden Shoe winner | 40 |
| p008 | Name a Premier League Golden Boot winner | 30 |
| p009 | Name a Premier League Player of the Season winner | 30 |
| p010 | Name a PFA Players' Player of the Year winner | 45 |
| p011 | Name an FWA Footballer of the Year winner | 70 |
| p012 | Name a World Cup Golden Ball winner | 25 |
| p013 | Name a World Cup Golden Boot (top scorer) winner | 25 |
| p014 | Name an African Footballer of the Year winner | 35 |
| p015 | Name a South American Footballer of the Year winner | 30 |
| p016 | Name an Asian Footballer of the Year winner | 30 |
| p017 | Name a Golden Boy award winner | 23 |
| p018 | Name a player who has finished a season as La Liga's top scorer (Pichichi) | 70 |
| p019 | Name a player who has finished a season as Serie A's top scorer (Capocannoniere) | 70 |
| p020 | Name a player who has finished a season as Bundesliga top scorer | 45 |
| p021 | Name a player who has finished a season as Ligue 1 top scorer | 70 |
| p022 | Name a player who has been top scorer of a European Cup / Champions League season | 60 |
| p023 | Name a player who has been top scorer of a European Championship tournament | 25 |

## records.py — stats, records, finals, transfers (p024–p043)
| id | prompt | est. |
|---|---|---|
| p024 | Name a player who has scored 100+ Premier League goals | 35 |
| p025 | Name a player who has scored 100+ Bundesliga goals | 45 |
| p026 | Name a player who has scored 100+ Serie A goals | 80 |
| p027 | Name a player who has scored 100+ Ligue 1 goals | 70 |
| p028 | Name a player who has scored 30+ European Cup / Champions League goals | 50 |
| p029 | Name a men's player who has scored 50+ international goals | 80 |
| p030 | Name a men's player with 150+ international caps | 80 |
| p031 | Name a player who has scored 20+ goals for England's men's team | 40 |
| p032 | Name a player who has made 500+ Premier League appearances | 30 |
| p033 | Name a player who has scored 3+ Premier League hat-tricks | 50 |
| p034 | Name a player who has scored a hat-trick at a men's World Cup | 55 |
| p035 | Name a player who has played at 4 or more men's World Cups | 40 |
| p036 | Name a player who has scored in a men's World Cup final | 65 |
| p037 | Name a player who has scored in a Champions League final (1993 onward) | 60 |
| p038 | Name a player who has scored in an FA Cup final (1990 onward) | 60 |
| p039 | Name a player who has scored in a men's European Championship final | 30 |
| p040 | Name a player whose transfer set a world-record fee | 45 |
| p041 | Name a goalkeeper who has won the Premier League Golden Glove | 15 |
| p042 | Name a player who has won the Premier League with two different clubs | 30 |
| p043 | Name a player who has won the European Cup / Champions League with two different clubs | 60 |

## national.py — national teams, tournaments, squads (p044–p063)
| id | prompt | est. |
|---|---|---|
| p044 | Name a country that has qualified for a men's World Cup | 80 |
| p045 | Name a country that has hosted or co-hosted a men's World Cup | 20 |
| p046 | Name a country that has qualified for a men's European Championship | 40 |
| p047 | Name a country that has played at an Africa Cup of Nations finals | 45 |
| p048 | Name a country that has reached a men's World Cup semi-final | 25 |
| p049 | Name a country that has won a men's continental championship (Euros, Copa América, AFCON, Asian Cup, Gold Cup, OFC Nations Cup) | 45 |
| p050 | Name a player who captained a men's World Cup-winning team | 22 |
| p051 | Name a player who has won both the men's World Cup and the European Cup / Champions League | 100 |
| p052 | Name a player in Brazil's 2002 World Cup-winning squad | 23 |
| p053 | Name a player in Spain's 2010 World Cup-winning squad | 23 |
| p054 | Name a player in Germany's 2014 World Cup-winning squad | 23 |
| p055 | Name a player in France's 2018 World Cup-winning squad | 23 |
| p056 | Name a player in Argentina's 2022 World Cup-winning squad | 26 |
| p057 | Name a player in Greece's Euro 2004-winning squad | 23 |
| p058 | Name a player in Italy's 2006 World Cup-winning squad | 23 |
| p059 | Name a manager who has won the men's World Cup | 20 |
| p060 | Name a manager who has won the men's European Championship | 17 |
| p061 | Name a stadium that has hosted a men's World Cup final | 20 |
| p062 | Name a stadium that has hosted a European Cup / Champions League final | 45 |
| p063 | Name a country that has played at a Copa América | 20 |

## clubs.py — clubs, competitions, stadiums (p064–p083)
| id | prompt | est. |
|---|---|---|
| p064 | Name a club that has played in the Premier League | 51 |
| p065 | Name a club that has been relegated from the Premier League | 45 |
| p066 | Name a club that has played in the Bundesliga | 57 |
| p067 | Name a club that has played in La Liga | 63 |
| p068 | Name a club that has played in Serie A | 68 |
| p069 | Name a club that has played in Ligue 1 | 80 |
| p070 | Name a club that has played in Major League Soccer | 35 |
| p071 | Name a club that has reached a European Cup / Champions League final | 40 |
| p072 | Name a club that has won the UEFA Cup / Europa League | 30 |
| p073 | Name a club that has won the European Cup Winners' Cup | 32 |
| p074 | Name a club that has won the FA Cup | 45 |
| p075 | Name a club that has won the English League Cup | 24 |
| p076 | Name a club that has won the Copa del Rey | 25 |
| p077 | Name a club that has won the Copa Libertadores | 26 |
| p078 | Name a club that has won the Copa Sudamericana | 20 |
| p079 | Name a club that has won the AFC Champions League / Asian Club Championship | 25 |
| p080 | Name a club that has won the CAF Champions League / African Cup of Champions Clubs | 25 |
| p081 | Name a club that has won the Intercontinental Cup or the FIFA Club World Cup | 30 |
| p082 | Name a club that has been Dutch league champions | 25 |
| p083 | Name a stadium that has been the home ground of a Premier League club | 60 |

## managers.py — managers and career paths (p084–p103)
| id | prompt | est. |
|---|---|---|
| p084 | Name a manager who has won the European Cup / Champions League | 60 |
| p085 | Name a manager who has won the English top-flight title | 60 |
| p086 | Name a manager who has won the Bundesliga | 35 |
| p087 | Name a manager who has won La Liga | 60 |
| p088 | Name a manager who has won Serie A | 60 |
| p089 | Name a manager of the England men's national team (caretakers included) | 20 |
| p090 | Name a manager of Manchester United (caretakers included) | 25 |
| p091 | Name a manager of Real Madrid | 60 |
| p092 | Name a manager of FC Barcelona | 60 |
| p093 | Name a manager of Chelsea since 2003 (caretakers included) | 20 |
| p094 | Name a manager of Arsenal (caretakers included) | 25 |
| p095 | Name a player who has played for both Real Madrid and Barcelona | 40 |
| p096 | Name a player who has played for both Arsenal and Tottenham | 30 |
| p097 | Name a player who has played for both Manchester United and Manchester City | 40 |
| p098 | Name a player who has played for both Liverpool and Everton | 50 |
| p099 | Name a player who has played for both AC Milan and Inter | 100 |
| p100 | Name a player who has played for both Celtic and Rangers | 20 |
| p101 | Name a player who has played for both Chelsea and Arsenal | 40 |
| p102 | Name a player who has played for both Bayern Munich and Borussia Dortmund | 40 |
| p103 | Name a player who has played for both Paris Saint-Germain and Marseille | 40 |
