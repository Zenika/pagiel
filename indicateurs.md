# DOM
## DOMaccesses
Type : entier

## DOMelementMaxDepth
Profondeur maximale d'imbrication des noeuds HTML

Type : entier

## DOMelementsCount
Nombre de noeuds HTML

Type : entier

## DOMidDuplicated
Nombre d'ids dupliqués

Type : entier

## DOMinserts
Nombre de noeuds insérés

Type : entier

## DOMmutationsAttributes
Nombre de changement d'attribut de node 

Type : entier

## DOMmutationsInserts
Nombre de noeuds insérés

Type : entier

## DOMmutationsRemoves
Nombre de noeuds supprimés

Type : entier

## DOMqueries
Nombre de requêtes sur le DOM

Type : entier

## DOMqueriesAvoidable
Nombre de requêtes sur le DOM répétées 

Type : entier

## DOMqueriesByClassName
Nombre d'appels à document.getElementsByClassName

Type : entier

## DOMqueriesById
Nombre d'appels à document.getElementById

Type : entier

## DOMqueriesByQuerySelectorAll
Nombre d'appels à document.querySelector(All)

Type : entier

## DOMqueriesByTagName
Nombre d'appels à document.getElementsByTagName

Type : entier

## DOMqueriesDuplicated
Nombre de requêtes répétées

Type : entier

## DOMqueriesWithoutResults
Nombre de requêtes sans résultat

Type : entier

## bodyHTMLSize
Taille du contenue du body (document.body.innerHTML.length) (bytes)

Type : entier

## commentsSize
Taille des commentaires sur la page (bytes)

Type : entier

## documentHeight
Hauteur de la page (px)

Type : entier

## hiddenContentSize
Taille du contenue caché de la page (avec display:none) (bytes)

Type : entier

## iframesCount
Nombre d'iframes

Type : entier

## nodesWithInlineCSS
Nombre de nodes avec du css inline

Type : entier

## whiteSpacesSize
Taille des noeuds de texte avec uniquement des blancs (bytes)

Type : entier

# assets
## ExternalizeCss
Externaliser les css

Type : chaine de charactère

## ExternalizeJs
Externaliser les js

Type : chaine de charactère

## MinifiedCss
Minifier les css

Type : chaine de charactère

## MinifiedJs
Minifier les js

Type : chaine de charactère

## StyleSheets
Limiter le nombre de fichiers css

Type : chaine de charactère

## UseStandardTypefaces
Utiliser des polices de caractères standards

Type : chaine de charactère

## assetsWithCookies
Nombre de fichier requêté sur des domaines avec des cookies

Type : entier

Exemple de comparaison : `== 0.0`

## assetsWithQueryString
Nombre de fichier requêté avec des paramètres dans les URLs

Type : entier

Exemple de comparaison : `== 0.0`

## cssSize
Volume total de fichier css

Type : entier

## fileMinification
Type : entier

## jsSize
Volume total de fichier javascript

Type : entier

## jsonSize
Volume total de fichier JSON

Type : entier

## multipleRequests
Fichier statique requêté plus d'une fois

Type : entier

Exemple de comparaison : `== 0.0`

## smallCssFiles
Nombre de petit fichier css

Type : entier

## smallJsFiles
Nombre de petit fichier javascript

Type : entier

# caching
## AddExpiresOrCacheControlHeaders
Ajouter des expires ou cache-control headers

Type : chaine de charactère

## cacheHits
Nombre de cache hits sur un serveur de cache

Type : entier

## cacheMisses
Nombre de cache misses sur un serveur de cache

Type : entier

## cachePasses
Nombre de cache passes sur un serveur de cache

Type : entier

## cachingDisabled
Nombre de fichier dont le cache est désactivé

Type : entier

## cachingNotSpecified
Nombre de fichier dont le cache est non spécifié

Type : entier

## cachingTooShort
Nombre de fichier dont le cache est très court

Type : entier

## cachingUseImmutable
Nombre de fichier qui pourrait bénéficier de l'en-tête Cache-Control: immutable

Type : entier

## oldCachingHeaders
Nombre de réponse avec les en-têtes de cache HTTP 1.0 (Expires et Pragma) 

Type : entier

# compression
## CompressHttp
Compresser les ressources

Type : chaine de charactère

## assetsNotGzipped
Nombre de fichier statique non gzip

Type : entier

## bodySize
Volume total de fichier décompressé

Type : entier

## compression
Type : entier

## contentLength
Volume total de fichier compressé

Type : entier

## gzipRequests
Nombre de requêtes compressée avec gzip

Type : entier

# cookies
## MaxCookiesLength
Taille maximum des cookies par domaine

Type : chaine de charactère

## NoCookieForStaticRessources
Pas de cookie pour les ressources statiques

Type : chaine de charactère

## cookiesRecv
Taille totale de cookies reçus

Type : entier

## cookiesSent
Taille totale de cookies envoyés

Type : entier

## documentCookiesCount
Nombre de cookies dans document.cookie

Type : entier

## documentCookiesLength
Taille de document.cookie (bytes)

Type : entier

Exemple de comparaison : `<= 512.0`

## domainsWithCookies
Nombre de dommaine avec des cookies

Type : entier

# css
## cssBase64Length
Longueur de contenue encodé en base64 dans les fichiers css

Type : entier

## cssBreakpoints
Nombre de breakpoints CSS

Type : entier

## cssColors
Nombre de couleurs utilisés dans le css

Type : entier

## cssComments
Nombre de commentaires dans les fichiers css

Type : entier

## cssCommentsLength
Longueur des commentaires dans les fichiers css

Type : entier

## cssComplexSelectors
Nombre de sélecteurs complexes

Type : entier

## cssDeclarations
Nombre de déclarations faite dans les fichiers css

Type : entier

## cssDuplicatedProperties
Nombre de propriétés dupliqués dans un sélecteur

Type : entier

## cssDuplicatedSelectors
Nombre de sélecteurs dupliqués

Type : entier

## cssEmptyRules
Nombre de règles sans propriétées

Type : entier

## cssExpressions
Nombre de règles avec des expressions

Type : entier

## cssImportants
Nombre de propriétés avec une valeur forcée avec !important

Type : entier

## cssImports
Nombre de règle avec @import

Type : entier

## cssInlineStyles
Nombre de style inline

Type : entier

## cssLength
Taille des fichiers css (bytes)

Type : entier

## cssMediaQueries
Nombre de media queries

Type : entier

## cssMobileFirst
Nombre de règles mobile first

Type : entier

## cssMultiClassesSelectors
Nombre de sélecteurs avec multiples classes

Type : entier

## cssNotMinified
Nombre de fichiers css non minifiés

Type : entier

## cssOldIEFixes
Nombre de fixes pour des vieille version d'Internet Explorer

Type : entier

## cssOldPropertyPrefixes
Nombre de propriétés avec un préfixe non nécéssaire

Type : entier

## cssParsingErrors
Nombre d'erreurs lors du parsing du css

Type : entier

## cssPropertyResets
Type : entier

## cssQualifiedSelectors
Nombre de sélecteurs qualifiés (ex : header#nav, h1.title)

Type : entier

## cssRedundantBodySelectors
Nombre de sélecteurs de body redondant (ex: body .foo)

Type : entier

## cssRedundantChildNodesSelectors
Nombre de sélecteurs de node enfant redondant

Type : entier

## cssRules
Nombre de règles css

Type : entier

## cssSelectorLengthAvg
Longueur moyenne des sélecteurs css

Type : nombre à virgule

## cssSelectors
Nombre de sélecteurs css

Type : entier

## cssSelectorsByAttribute
Nombre de sélecteurs par attribut

Type : entier

## cssSelectorsByClass
Nombre de sélecteurs par classe

Type : entier

## cssSelectorsById
Nombre de sélecteurs par id

Type : entier

## cssSelectorsByPseudo
Nombre de pseudo-selectors

Type : entier

## cssSelectorsByTag
Nombre de sélecteurs par tag

Type : entier

## cssSpecificityClassAvg
Moyenne de la spécificité pour les sélecteurs par classe, pseudo-class ou attribut

Type : nombre à virgule

## cssSpecificityClassTotal
Spécificité totale des sélecteurs par classe, pseudo-class, et attribut

Type : entier

## cssSpecificityIdAvg
Moyenne de la spécificité pour les sélecteurs par id

Type : nombre à virgule

## cssSpecificityIdTotal
Spécificité totale des sélecteurs par id

Type : entier

## cssSpecificityTagAvg
Moyenne de la spécificité pour les sélecteurs par tag

Type : nombre à virgule

## cssSpecificityTagTotal
Spécificité totale des sélecteurs par tag

Type : entier

## similarColors
Nombre de couleurs similaires

Type : entier

# domains
## DomainsNumber
Limiter le nombre de domaines

Type : chaine de charactère

## blockedRequests
Nombre de requête bloqué à cause de filtrage de domaine

Type : entier

## domains
Nombre de domaines requêtés pour charger la page

Type : entier

Exemple de comparaison : `< 3.0`

## domainsToDomComplete
Nombre de domaines requêté pour atteindre l'état DomComplete

Type : entier

## domainsToDomContentLoaded
Nombre de domaines requêté pour atteindre l'état DomContentLoaded

Type : entier

## domainsToFirstPaint
Nombre de domaines requêté pour faire le premier changement visuel

Type : entier

## maxRequestsPerDomain
Nombre maximal de requêtes faire sur un seul domaine

Type : entier

## medianRequestsPerDomain
Médiane du nombre de requête faite par domaine

Type : entier

# eco
## ecoindex
Valeur de l'écoindex de la page

Type : entier

Exemple de comparaison : `>= 65.0`

## ges
Emission de gaz à effet de serre associée à la page (en gramme equivalent CO2, geCO2)

Type : nombre à virgule

## grade
Note associée à l'ecoindex

Type : chaine de charactère

## water
Consomation d'eau associée à la page

Type : nombre à virgule

# fonts
## heavyFonts
Type : entier

## nonWoff2Fonts
Type : entier

## webfontSize
Volume de web font chargé (bytes)

Type : entier

# headers
## headersBiggerThanContent
Nombre de réponse reçus avec partie une en-tête plus importante que le body

Type : entier

## headersCount
Nomre de réponses et d'en-tête reçus

Type : entier

## headersRecvCount
Nombre d'en-têtes reçus

Type : entier

## headersRecvSize
Volume d'en-têtes reçus (bytes)

Type : entier

## headersSentCount
Nombre d'en-têtes envoyés

Type : entier

## headersSentSize
Volume d'en-têtes envoyés (bytes)

Type : entier

## headersSize
Volume total d'en-tête (bytes)

Type : entier

## incorrectContentTypes
Nombre de Content-Type incorrects

Type : entier

# images
## DontResizeImageInBrowser
Ne pas retailler les images dans le navigateur

Type : chaine de charactère

## EmptySrcTag
Eviter les tags SRC vides

Type : chaine de charactère

## ImageDownloadedNotDisplayed
Ne pas télécharger des images inutilement

Type : chaine de charactère

## OptimizeBitmapImages
Optimiser les images bitmap

Type : chaine de charactère

## OptimizeSvg
Optimiser les images svg

Type : chaine de charactère

## hiddenImages
Nombre d'images caché par un style display: none

Type : entier

## imageCount
Nombre d'images

Type : entier

## imageOptimization
Type : entier

## imageSize
Volume d'image chargé (bytes)

Type : entier

## imagesScaledDown
Nombre d'images retaillés dans le navigateur

Type : entier

## imagesTooLarge
Nombre d'image trop grosse

Type : entier

## imagesWithoutDimensions
Nombre de balises img sans dimensions

Type : entier

## lazyLoadableImagesBelowTheFold
Nombre d'image sous la ligne de flotaison qui pourraient être lazy loader

Type : entier

## smallImages
Petites image qui pourrait être encodé en base64

Type : entier

## videoCount
Nombre de vidéo

Type : entier

## videoSize
Volume de vidéo chargé (bytes)

Type : entier

# jquery
## jQueryDOMReads
Nombre de lectures du DOM avec jQuery

Type : entier

## jQueryDOMWriteReadSwitches
Nombre d'opération de lecture du DOM qui suivent une série d'écriture

Type : entier

## jQueryDOMWrites
Nombre d'écriture du DOM avec jQuery

Type : entier

## jQueryEventTriggers
Nombre d'event trigger de jQuery

Type : entier

## jQueryOnDOMReadyFunctions
Nombre de fonctions liées à l'évènement onDOMReady

Type : entier

## jQuerySizzleCalls
Nombre d'appel à Sizzle

Type : entier

## jQueryVersion
Version de jQuery

Type : entier

## jQueryVersionsLoaded
Nombre d'instances de jQuery chargées

Type : entier

## jQueryWindowOnLoadFunctions
Nombre de fonctions liées à l'évènement windowOnLoad

Type : entier

# js
## Plugins
Ne pas utiliser de plugins

Type : chaine de charactère

## consoleMessages
Nombre d'appel à des fonctions console.*

Type : entier

## globalVariables
Nombre de variables globales

Type : entier

## globalVariablesFalsy
Nombre de variables globales avec une valeur falsy

Type : entier

## jsErrors
Nombre d'erreur de javascript

Type : entier

## localStorageEntries
Nombre d'entrées dans le localStorage

Type : entier

## windowAlerts
Nombre d'appel à window.alert

Type : entier

## windowConfirms
Nombre d'appel à window.confirm

Type : entier

## windowPrompts
Nombre d'appel à window.prompt

Type : entier

# other
## SocialNetworkButton
N'utilisez pas les boutons standards des réseaux sociaux

Type : chaine de charactère

## isWordPress
Est-ce que le site utilise wordpress

Type : booléen

# performances
## CumulativeLayoutShift
Type : entier

## FirstVisualChange
Type : entier

## LargestContentfulPaint
Type : entier

## LastVisualChange
Type : entier

## LoadEvenEnd
Type : entier

## SpeedIndex
Type : entier

## TTFB
Type : entier

## VisualReadiness
Type : entier

## backEndTime
Temps pour le premier octet de réponse par rapport au temps total de chargement (ms)

Type : entier

## domComplete
Timing du domComplete (windows.performance)

Type : entier

## domContentLoaded
Type : entier

## domContentLoadedEnd
Type : entier

## domContentLoadedEventEnd
Type : entier

## domContentLoadedEventStart
Type : entier

## domContentLoadedTime
Type : entier

## domElements
Type : entier

## domInteractive
Type : entier

## firstPaint
Type : entier

## frontEndTime
Temps pour l'évènement window.load par rapport au temps total de chargement (ms)

Type : entier

## fullyLoaded
Type : entier

## performanceTimingPageLoad
Temps nécéssaire pour charger entièrement la page (ms)

Type : entier

## performanceTimingTTFB
Temps nécéssaire pour recevoir le premier octet de la première réponse (ms)

Type : entier

## timeBackend
Temps pour le premier octet de réponse par rapport au temps total de chargement (%)

Type : entier

## timeFrontend
Temps pour l'évènement window.load par rapport au temps total de chargement (%)

Type : entier

## timeToFirstByte
Temps nécéssaire pour recevoir le premier octet de la première réponse (ms)

Type : entier

## timeToLastByte
Temps nécéssaire pour recevoir le dernière octet de la dernière réponse (ms)

Type : entier

# performances_cpu
## Layout
Type : entier

## ParseHTML
Type : entier

## RunTask
Type : entier

## documentWriteCalls
Nombre d'appel à document.write

Type : entier

## evalCalls
Nombre d'appel à eval

Type : entier

## eventsBound
Nombre d'évènement écouté via EventTaget.addEventListener

Type : entier

## eventsDispatched
Nombre d'appel à EventTarget.dispatchEvent

Type : entier

## eventsScrollBound
Nombre d'écoutes sur l'évènement scroll

Type : entier

## garbageCollection
Type : entier

## layoutCount
Nombre de calcul de layout

Type : entier

## layoutDuration
Durée total des calculs de layout

Type : entier

## paintCompositeRender
Type : entier

## recalcStyleCount
Nombre total de recalculs du style

Type : entier

## recalcStyleDuration
Durée totale des recalculs du style

Type : entier

## scriptDuration
Durée totale des script javascript

Type : entier

## scriptEvaluation
Type : entier

## scriptParseCompile
Type : entier

## styleLayout
Type : entier

## taskDuration
Durée totale des taches effectué par le navigateur

Type : entier

# protocols
## mainDomainHttpProtocol
Protocol HTTP sur domaine principal

Type : entier

## mainDomainTlsProtocol
Protocol TLS du domaine principal

Type : entier

## oldHttpProtocol
Nombre de domaines utilisant un vieux protocol HTTP (1.0 ou 1.1)

Type : entier

## oldTlsProtocol
Nombre de domaines utilisant un vieux protocol TLS (1.2)

Type : entier

# requests
## HttpError
Eviter les requêtes en erreur

Type : chaine de charactère

## HttpRequests
Limiter le nombre de requêtes HTTP

Type : chaine de charactère

## NoRedirect
Eviter les redirections

Type : chaine de charactère

## UseETags
Utiliser des ETags

Type : chaine de charactère

## ajaxRequests
Nombre de requête AJAX

Type : entier

## base64Count
Nombre de fichier en base64

Type : entier

## base64Size
Volume de fichier encodé en base64 (bytes)

Type : entier

## biggestLatency
Temps pour le premier byte de la réponse la plus lente (ms)

Type : entier

## biggestResponse
Volume de la plus grosse requête (byte)

Type : entier

## bodySize
Volume total après décompression de toutes les réponses

Type : entier

## closedConnections
Nombre de requête dont la connection avec le serveur n'est pas persistante

Type : entier

## contentLength
Volume total des réponses, i.e. ce qui a été transférer dans les paquets

Type : entier

## cssCount
Nombre de fichier CSS

Type : entier

Exemple de comparaison : `< 3.0`

## emptyRequests
Nombre de réponse dont le body est vide

Type : entier

## fastestResponse
Temps pour le dernier byte de la réponse la plus rapide (ms)

Type : entier

## fontsCount
Nombre de fichier de police de caractère

Type : entier

## gzipRequests
Nombre de réponse compressée avec GZIP

Type : entier

## htmlCount
Nombre de fichier HTML

Type : entier

## htmlSize
Volume de fichiers HTML chargés (bytes)

Type : entier

## httpsRequests
Nombre de requête HTTPS

Type : entier

Exemple de comparaison : `<= 27.0`

## identicalFiles
Nombre de fichiers identiques obtenue à partir d'urls différents

Type : entier

## imageCount
Nombre d'images

Type : entier

## jsCount
Nombre de fichier javascript

Type : entier

## jsonCount
Nombre de fichier JSON

Type : entier

## medianLatency
Médiane du temps pour le premier byte sur toutes les réponses (ms)

Type : entier

## medianResponse
Médiane du temps pour le dernier byte sur toutes les réponses (ms)

Type : entier

## notFound
Nombre d'erreurs 404 reçu

Type : entier

## otherCount
Nombre d'autres fichiers

Type : entier

## otherSize
Volume d'autre type de fichier chargé (bytes)

Type : entier

## performanceTimingConnect
Temps nécessaire pour se connecter au serveur 

Type : entier

## performanceTimingDNS
Temps nécessaire pour faire la résolution DNS

Type : entier

## postRequests
Nombre de requête POST effectué au chargement de la page

Type : entier

## redirects
Nombre de redirects (reçu 301, 302, 303)

Type : entier

## redirectsTime
Temps nécessaire pour envoyer et recevoir les redirections

Type : entier

## requests
Nombre total de requête effectué

Type : entier

## requestsToDomComplete
Nombre de requêtes pour atteindre l'état DomComplete

Type : entier

## requestsToDomContentLoaded
Nombre de requête pour atteindre l'état DomContentLoaded

Type : entier

## requestsToFirstPaint
Nombre de requête nécessaire pour faire le premier affichage

Type : entier

## slowestResponse
Temps pour le dernier byte de la réponse la plus lente (ms)

Type : entier

## smallestLatency
Temps pour le premier byte de la réponse la plus rapide (ms)

Type : entier

## smallestResponse
Volume de la plus petite requête (byte)

Type : entier

## statusCodesTrail
Liste des code de réponses que la requête principale a suivi

Type : chaine de charactère

## synchronousXHR
Nombre de requête XML synchrone

Type : entier

## totalRequests
Type : entier

## totalWeight
Type : entier

## videoCount
Nombre de vidéo

Type : entier

## webfontCount
Nombre de fichier de police web

Type : entier

