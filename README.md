# Extracteur BCF vers CSV

Outil en ligne de commande développé en Python permettant d'extraire les données issues de fichiers BIM Collaboration Format (BCF) et de les exporter vers un format CSV compatible avec les tableurs et outils d'analyse de données.

## Présentation

Ce projet assure le traitement des données relatives aux problèmes de coordination (Issues, Clashes) issues des plateformes BIM, en respectant le standard openBIM BCF défini par buildingSMART. L'outil s'exécute de manière autonome dans tout environnement Python standard, garantissant ainsi sa portabilité et sa maintenabilité.

## Fonctionnalités

- Conformité buildingSMART : Extraction des métadonnées XML (`markup.bcf`) basée sur le schéma `markup.xsd`, incluant la prise en charge rétrocompatible (BCF 2.0, BCF 2.1, BCF 3.0).
- Autonomie : Repose exclusivement sur la bibliothèque standard de Python (`zipfile`, `xml.etree.ElementTree`, `csv`, `pathlib`).
- Compatibilité des données : Exporte un fichier CSV structuré avec l'encodage UTF-8 avec BOM (`utf-8-sig`) et le délimiteur point-virgule (`;`), assurant une lecture native sous les tableurs configurés avec les paramètres régionaux européens.
- Tolérance aux anomalies : 
  - Gestion des champs XML optionnels ou manquants.
  - Parcours récursif de l'archive ZIP sans dépendance stricte à l'arborescence.
  - Interception des fichiers XML corrompus ou malformés sans interruption du processus global.
- Traitement des caractères complexes : Prise en charge des textes multilingues et de la conservation des sauts de ligne au sein des descriptions.

## Utilisation

### Exécution en ligne de commande

Le script peut être exécuté depuis un terminal en spécifiant le fichier d'entrée et le fichier de destination.

```bash
python src/bcf_to_csv.py <fichier_entree.bcf> <fichier_sortie.csv>
```

Exemple :
```bash
python src/bcf_to_csv.py export_clash_detection.bcfzip suivi_clashs.csv
```

Note : L'exécution du script sans argument (`python src/bcf_to_csv.py`) déclenche une recherche automatique du premier fichier `.bcf` ou `.bcfzip` présent dans le répertoire de travail courant pour en effectuer la conversion.

### Déploiement sur un nouveau poste informatique

Pour que l'interface graphique fonctionne sur un nouvel ordinateur, il est nécessaire de suivre ces trois étapes d'installation :

1. **Installer Python** : Télécharger et installer Python depuis le site officiel (python.org). 
   *⚠️ Attention : Lors de l'installation sous Windows, il est impératif de cocher la case **"Add Python to PATH"**.*
2. **Installer les dépendances** : Double-cliquez simplement sur le fichier **`scripts/Installer_Dependances.bat`**. Une fenêtre noire va s'ouvrir, télécharger l'interface, puis vous indiquer quand c'est terminé.
3. **Exécution** : Une fois installé, l'utilisateur final n'a plus qu'à **double-cliquer sur le fichier `scripts/Lancer_Extracteur.bat`** (ou `src/extracteur_gui.pyw`). L'interface s'ouvrira directement de manière transparente.

### Intégration en tant que module

La fonction d'extraction peut être importée dans des scripts tiers ou des processus d'automatisation :

```python
from src.bcf_to_csv import bcf_to_csv

# Lancement de l'extraction
bcf_to_csv('archives/projet_2023.bcf', 'donnees_extraites.csv')
```

## Documentation technique

Pour une analyse détaillée du fonctionnement interne, de la structure des données et des normes XML appliquées, la documentation technique est disponible dans le fichier `docs/ARCHITECTURE.md`.
