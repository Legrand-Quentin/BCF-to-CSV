# Architecture et Fonctionnement technique

## Format BCF

Le fichier BIM Collaboration Format (BCF) se présente sous la forme d'une archive ZIP respectant une structure interne définie par le standard openBIM de buildingSMART.

Organisation structurelle typique d'une archive BCF :
- Fichier `bcf.version` situé à la racine, spécifiant la version du schéma BCF (ex: 2.0, 2.1, 3.0).
- Répertoires par sujet, dont le nom correspond au GUID de l'identifiant (ex: `80e13504-1319-406d-8192-dd0f1d8d88b5/`).
- Fichier `markup.bcf` contenu dans chaque répertoire de sujet. Il s'agit du document XML principal consignant les métadonnées textuelles (titre, statut, priorités, assignations, historique des commentaires).
- Fichiers additionnels optionnels : images (`snapshot.png`) et définitions de points de vue (`viewpoint.bcfv`).

## Processus d'extraction (In-Memory)

L'outil implémente un traitement des données en mémoire, éliminant la nécessité d'une extraction préalable de l'archive sur le système de fichiers, optimisant ainsi les performances et la gestion de l'espace disque.

### 1. Lecture de l'archive
Le module `zipfile` est utilisé pour ouvrir l'archive en mode lecture (`'r'`).
Le script procède à un balayage complet du contenu de l'archive (`bcf_zip.namelist()`) afin d'isoler l'ensemble des fichiers `markup.bcf`, indépendamment de la structure hiérarchique qui peut différer selon le logiciel auteur.

### 2. Traitement XML et conformité normative
Le module `xml.etree.ElementTree` assure l'analyse de chaque fichier `markup.bcf`. L'extraction est conçue pour respecter le schéma officiel `markup.xsd` :

- Rétrocompatibilité (BCF 2.0 à 2.1+) : Les propriétés telles que `TopicType` et `TopicStatus` ont évolué d'attributs de `<Topic>` vers des éléments enfants. Le traitement intègre une méthode de repli permettant d'extraire la donnée indépendamment de la version du schéma :
  ```python
  topic_type = topic.get('TopicType', topic.findtext('TopicType', ''))
  ```
- Gestion des éléments optionnels : Conformément au standard, la majorité des éléments (Priority, AssignedTo, Description) sont soumis à la contrainte `minOccurs="0"`. La méthode `findtext(..., '')` est appliquée pour assigner une chaîne de caractères vide par défaut, évitant ainsi le traitement de valeurs nulles (`NoneType`).
- Comptabilisation des commentaires : Le schéma XML stipule qu'un élément `<Comment>` contient diverses métadonnées ainsi qu'un élément enfant, également nommé `<Comment>`, destiné au texte. L'instruction `root.findall('Comment')` cible exclusivement les enfants directs, évitant la redondance dans le comptage qui résulterait d'une recherche récursive.

### 3. Consolidation et sérialisation CSV
Les propriétés extraites sont structurées sous forme de dictionnaires et transcrites dans un fichier CSV par l'intermédiaire de `csv.DictWriter`.

Optimisations appliquées à la sérialisation :
- Encodage : L'utilisation de `utf-8-sig` force l'insertion d'un Byte Order Mark (BOM). Ceci garantit l'interprétation correcte des caractères multilingues et spéciaux par Microsoft Excel.
- Délimitation : Le point-virgule (`;`) est utilisé comme séparateur, se conformant aux standards régionaux européens et prévenant les conflits d'interprétation des séparateurs décimaux.
- Intégrité textuelle : Les descriptions intégrant des sauts de ligne ou des caractères réservés sont encadrées de guillemets doubles par le module CSV de Python, maintenant l'intégrité de la structure tabulaire.

## Dépendances

L'outil repose exclusivement sur la bibliothèque standard du langage Python. L'absence de dépendances externes (telles que `pandas` ou `lxml`) facilite le déploiement sur divers environnements et systèmes informatiques sans nécessiter de gestion de paquets additionnelle.
