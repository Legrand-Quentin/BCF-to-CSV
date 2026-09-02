"""
Module d'extraction de données BCF (BIM Collaboration Format).

Ce script permet d'extraire de façon robuste les métadonnées (problèmes, clashs, 
commentaires) contenues dans un fichier archive BCF (standardisé par buildingSMART) 
pour les exporter vers un fichier CSV prêt à être exploité dans Microsoft Excel, PowerBI, etc.

Le script respecte les schémas officiels (markup.xsd) et assure une rétrocompatibilité 
pour gérer différentes versions d'export de logiciels (BCF 2.0 / 2.1).

Dépendances:
    Uniquement la bibliothèque standard Python (zipfile, xml.etree.ElementTree, csv, pathlib).
"""
import zipfile
import xml.etree.ElementTree as ET
import csv
from pathlib import Path

def bcf_to_csv(input_bcf: str, output_csv: str) -> None:
    """
    Extrait les données pertinentes d'une archive BCF et les sauvegarde en format CSV.
    
    Le fichier BCF est parcouru en mémoire en tant qu'archive ZIP. Le processus
    identifie et parse tous les fichiers 'markup.bcf' présents. Les balises optionnelles
    sont gérées avec des valeurs par défaut pour garantir la stabilité de l'extraction
    face aux fichiers mal formés. Les commentaires sont comptabilisés en évitant 
    les doublons structurels du schéma BCF.

    Le fichier CSV généré utilise l'encodage 'utf-8-sig' (UTF-8 avec BOM) et le 
    séparateur point-virgule (';') pour garantir une ouverture sans configuration 
    préalable sous les versions francophones/européennes de Microsoft Excel.

    Args:
        input_bcf (str): Chemin d'accès au fichier source BCF (.bcf, .bcfzip).
                         Peut être un chemin absolu ou relatif.
        output_csv (str): Chemin d'accès où sera écrit le fichier CSV résultant.

    Returns:
        None

    Raises:
        Le script intercepte la majorité des exceptions liées à la lecture du ZIP
        et au parsing XML. Celles-ci généreront des avertissements ou erreurs dans
        la sortie standard (console) plutôt que d'interrompre violemment le flux.
    """
    input_path = Path(input_bcf)
    output_path = Path(output_csv)
    
    if not input_path.exists():
        print(f"Erreur : Le fichier d'entrée '{input_bcf}' n'existe pas.")
        return
        
    extracted_data = []
    
    try:
        # Le fichier BCF est une archive ZIP. Lecture en mode 'r' (read).
        with zipfile.ZipFile(input_path, 'r') as bcf_zip:
            # Récupérer tous les fichiers nommés 'markup.bcf', peu importe leur dossier parent
            markup_files = [f for f in bcf_zip.namelist() if f.endswith('markup.bcf')]
            
            if not markup_files:
                print(f"Aucun fichier 'markup.bcf' trouvé dans l'archive '{input_bcf}'.")
                return

            for markup_file in markup_files:
                # Lecture directe (en mémoire) du contenu XML
                with bcf_zip.open(markup_file) as xml_file:
                    try:
                        tree = ET.parse(xml_file)
                        root = tree.getroot()  # Racine attendue : <Markup>
                        
                        # Rechercher la balise <Topic> contenant les informations clés
                        topic = root.find('Topic')
                        if topic is not None:
                            # Les attributs Guid, TopicType et TopicStatus peuvent être des attributs (BCF 2.1+) 
                            # ou des balises enfants (BCF 2.0). Utilisation du .get avec fallback sur .findtext.
                            guid = topic.get('Guid', '')
                            topic_type = topic.get('TopicType', topic.findtext('TopicType', ''))
                            topic_status = topic.get('TopicStatus', topic.findtext('TopicStatus', ''))
                            
                            # Extraction des champs optionnels (minOccurs="0" dans le schéma markup.xsd)
                            title = topic.findtext('Title', '')
                            priority = topic.findtext('Priority', '')
                            creation_author = topic.findtext('CreationAuthor', '')
                            assigned_to = topic.findtext('AssignedTo', '')
                            creation_date = topic.findtext('CreationDate', '')
                            description = topic.findtext('Description', '')
                            
                            # Compter le nombre de balises <Comment> associées à ce sujet.
                            # On cherche uniquement les enfants directs de <Markup> car la norme 
                            # incorpore une sous-balise également nommée <Comment> contenant le texte.
                            comments_count = len(root.findall('Comment'))
                            
                            extracted_data.append({
                                'GUID': guid,
                                'Title': title,
                                'TopicStatus': topic_status,
                                'TopicType': topic_type,
                                'Priority': priority,
                                'CreationAuthor': creation_author,
                                'AssignedTo': assigned_to,
                                'CreationDate': creation_date,
                                'Description': description,
                                'CommentsCount': comments_count
                            })
                    except ET.ParseError:
                        print(f"Avertissement : Erreur de parsing XML (fichier corrompu ou invalide) pour {markup_file}")
                        
    except zipfile.BadZipFile:
        print(f"Erreur : Le fichier '{input_bcf}' n'est pas un fichier ZIP/BCF valide ou est corrompu.")
        return
        
    # En-têtes des colonnes pour la sérialisation CSV
    fieldnames = [
        'GUID', 'Title', 'TopicStatus', 'TopicType', 'Priority', 
        'CreationAuthor', 'AssignedTo', 'CreationDate', 'Description', 'CommentsCount'
    ]
    
    try:
        # Encodage utf-8-sig pour assurer la présence du BOM et la lecture native par MS Excel.
        # newline='' évite la création de sauts de ligne supplémentaires (CRLF) sous Windows.
        with open(output_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            # Point-virgule (;) utilisé comme séparateur, standard européen des tableurs.
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(extracted_data)
        print(f"Extraction terminée. {len(extracted_data)} sujets exportés vers '{output_csv}'.")
    except IOError as e:
        print(f"Erreur système lors de l'écriture du fichier CSV de destination : {e}")


if __name__ == "__main__":
    import sys
    
    # --- Interface en ligne de commande (CLI) ---
    print("--- Script de conversion BCF vers CSV ---")
    
    if len(sys.argv) == 3:
        # Arguments fournis : <fichier_entree.bcf> <fichier_sortie.csv>
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        bcf_to_csv(input_file, output_file)
    else:
        # Mode démo/interactif si aucun argument n'est fourni
        print("Usage en ligne de commande : python bcf_to_csv.py <fichier.bcf> <resultat.csv>")
        print("\nExemple d'intégration Python :")
        print("  from bcf_to_csv import bcf_to_csv")
        print("  bcf_to_csv('projet_maquette.bcfzip', 'export_commentaires.csv')")
        
        # Recherche automatisée d'un fichier .bcf ou .bcfzip dans le répertoire de travail
        bcf_files = list(Path('.').glob('*.bcf')) + list(Path('.').glob('*.bcfzip'))
        
        if bcf_files:
            test_file = bcf_files[0]
            out_file = test_file.with_suffix('.csv')
            print(f"\nFichier détecté : {test_file}. Lancement de la conversion vers {out_file}.")
            bcf_to_csv(str(test_file), str(out_file))
        else:
            print("\nAucun fichier .bcf ou .bcfzip n'a été trouvé dans le répertoire courant pour une exécution automatique.")
