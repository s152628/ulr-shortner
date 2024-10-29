# Verslag URL-shortner Python

## Stap 1: mapping tonen

Stap 1 heeft mij het langste geduurd. Achterhalen hoe te werken met Flask was heeft mij het langste bezig gehouden. Ik probeerde te snel door de documentatie heen te lezen waardoor ik veel heb gemist en vast liep. Hierdoor heb ik iets van een drie kwartier liggen sukkelen met routes zonder de documentatie deftig door te nemen. Nadat ik de documentatie dan eens aandachtig had doorgelezen ging dit veel vlotter en raakte ik snel overweg met het gebruik van Flask.

## Stap 2: mapping uitbreiden

Stap 2 ging redelijk vlot, ik kon al reeds overweg met Jinja door opdrachten van vorig jaar en de eerste opdracht van dit jaar. In deze stap heb ik dan een html template toegevoegd waarin ik een form heb gezet met 2 imput velden en een submit knop. Deze form heb ik dan gelinked aan de route /shorturl waardoor ik in mijn bestand main.py makkelijk op deze route requests kon maken naar mijn alias en url die werden ingevuld op de form. De errors heb ik dan kunnen behandelen met de ingebouwde jinja van Flask. Als er geen url werd opgegeven of geen alias werd opgegeven werd er voor het missende element een respectievelijke error message aangemaakt en toegevoegd aan de error list die door jinja werd uitgelezen op de html pagina.

## stap 3: persistente mapping

De SQLite database inwerken bij mijn code verliep redelijk vlot en zonder problemen. Door middel van de documentatie goed te doorlopen had ik snel mijn database aangemaakt en toegevoegd aan mijn code. Het zoeken van de juiste queries verliep vlot en ik werd ook bijgestaan door github copilot autocomplete die het schrijven van de queries nog eens sneller liet verlopen. Waar ik even bij vast heb gezeten was het committen van de aanpassingen. De lijn db.commit() stond nog niet in mijn code en ik had dit niet door waardoor ik maar niet begreep waarom mijn aanpassingen aan de database niet tevoorschijn kwamen.

## stap 4: redirects

Redirects verliepen heel vlot. Ik had al reeds in stap 2 gebruik gemaakt van redirect. Ik heb redirect daarna verwijdert omdat dit nog niet werd gevraagd in de stap waar ik toen zat. Maar door het eerdere gebruik ben ik snel over stap 4 gegaan. Later heb ik wel ontdekt dat ik de redirect nogal omslachtig had gemaakt. Ik heb mijn code een paar stappen verder dan ook volledig herschreven.

## stap 5: randomized aliassen

Door gebruik van de random library en chr() en ord() was het redelijk makkelijk om een randomized alias te maken van 15 tekens lang. Ik heb een apparte functie aangemaakt voor een random alias aan te maken en deze werd dan aangeroepen in plaats van een alias te halen via de form.

## stap 6: styling

Aan styling heb ik niet te veel tijd gespendeerd. Ik heb achterhaald hoe je de styling het beste toevoegd aan de html file door gebruik te maken van een map 'static' en url_for(). Hierna heb ik de styling zelf laten schrijven door chatGPT om het mijzelf makkelijk te maken en meer tijd te kunnen spenderen aan het effectieve coderen.

## stap 7: foutafhandeling

Voor foutafhandeling heb ik een extra redirect aangemaakt die doorverwees naar een 404 template dat ik had aangemaakt. Ik keek hier na of de gegeven url werkelijk een url was door een nieuwe functie toe te voegen genaamd is_url_valid(). Ik heb hier gebruik gemaakt van de library van Requests om een request te maken naar de gegeven url. Als deze request lukte dan werd er een alias aangemaakt en werd deze alias met url in de database opgeslagen. Indien dit niet lukte werd de gebruiker naar een nieuwe pagina gestuurd waar werd vermeld dat er geen bruikbare url was doorgegeven. Dit heb ik later aangepast in stap 11 aangezien er gevraagd werd naar het gebruik van reguliere expressies om dit na te kijken. Al denk ik dat het gebruik van requests beter was om te zorgen dat je de database minder moet opschonen.

## stap 8: logging

Logging ging redeljk vlot en heeft mij niet zo veel tijd gekost. Ik ben enkel even bezig geweest met de logging.basicConfig deftig aan te passen naar mijn voorkeuren. Voor de rest leek logging heel hard op het gebruik van print().

## stap 9: caching

Caching heeft mij een lange tijd bezig gehouden omdat ik veel moeite had met decorators. Na hier veel mee te knoeien in eigen experimentjes, begreep ik decorators al iets beter. Maar de stap die ik hier heb werkte nog niet correct al had ik dit niet door. Ik had moeite met na te kijken of mijn caching wel degelijk werkte of niet maar ben er dan maar vanuit gegaan van wel. Eerst werkte ze zeker niet omdat ik fout begrepen had dat de eigen decorator onder de app.route decorator moest staan. Hierna werkte ze ook niet omdat ik de decorator op het foute onderdeel van mijn code had staan maar dit had ik pas door in stap 10.

## stap 10: universele logging

Stap 10 zelf heeft mij niet lang geduurd. Dit viel goed mee dankzij de documentatie "decorators with parameters" goed door te nemen en github copilot die me hulp biedde als ik vastliep. Wat wel lang heeft geduurd in deze stap is het herschrijven van mijn code. Ik had eerder mijn /shorturl/<alias> gemerged met /shorturl waardoor ik een error kreeg in verband met caching. Ik heb deze dan terug opgesplitst maar efficiënter gemaakt. Dit zodat de gebruiker een url of een reeds bestaande alias kon ingeven in het invul veld. Als een bestaande alias werd ingevuld werd de gebruiker doorgestuurd naar de website die verbonden is aan die alias dit gebeurd via 2 redirects. De eerste redirect was naar de /<alias> route een nieuwe route die ik had aangemaakt. Vanuit deze route word je dan automatisch doorgestuurd naar de gegeven alias als deze bestaat. Als een url werd ingevuld werd hiervoor een alias aangemaakt. Om dit te laten werken had ik een aparte functie aangemaakt voor een url uit de database te halen. Hier heb ik dan de caching decorator op geplaatst. De functie get_url_by_alias(alias) werd dan aangeroepen in de /<alias> route.

## stap 11: vormelijke controle URL

Dit had ik al reeds gedaan door gebruik te maken van de Requests library. Maar aangezien er gevraagd werd naar het gebruik van reguliere expressies heb ik dit nog aangepast.

## Algemene ervaring

Het vorig project was voor mij redelijk demotiverend. Niets lukte goed en ik heb te veel gefocust op chatGPT voor mijn vorig project waardoor ik er op het einde zelf niet aanuitkon en dan ook niet heb ingediend.

Dit project heeft mij terug gemotiveerd. Ik heb mij enorm geamuseerd met het project en het verliep over het algemeen goed naast enkele obstakels die ik onderweg ben tegengekomen.
