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
from pathdef _parse_topic_xml(xml_file) -> dict:
    """Parse le contenu XML d'un fichier markup.bcf et retourne un dictionnaire de données."""
    tree = ET.parse(xml_file)
    root = tree.getroot()  # Racine attendue : <Markup>
    
    topic = root.find('Topic')
    if topic is None:
        return {}

    # Rétrocompatibilité (BCF 2.0 / 2.1+)
    guid = topic.get('Guid', '')
    topic_type = topic.get('TopicType', topic.findtext('TopicType', ''))
    topic_status = topic.get('TopicStatus', topic.findtext('TopicStatus', ''))
    
    # Champs optionnels
    title = topic.findtext('Title', '')
    priority = topic.findtext('Priority', '')
    creation_author = topic.findtext('CreationAuthor', '')
    assigned_to = topic.findtext('AssignedTo', '')
    creation_date = topic.findtext('CreationDate', '')
    description = topic.findtext('Description', '')
    
    # Comptage des commentaires (enfants directs de <Markup>)
    comments_count = len(root.findall('Comment'))
    
    return {
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
    }

def _extract_bcf_data(input_path: Path) -> list[dict]:
    """Ouvre l'archive ZIP BCF et extrait les données de tous ses fichiers markup.bcf."""
    extracted_data = []
    
    try:
        with zipfile.ZipFile(input_path, 'r') as bcf_zip:
            markup_files = [f for f in bcf_zip.namelist() if f.endswith('markup.bcf')]
            
            if not markup_files:
                print(f"Aucun fichier 'markup.bcf' trouvé dans l'archive '{input_path}'.")
                return []

            for markup_file in markup_files:
                with bcf_zip.open(markup_file) as xml_file:
                    try:
                        data = _parse_topic_xml(xml_file)
                        if data:
                            extracted_data.append(data)
                    except ET.ParseError:
                        print(f"Avertissement : Erreur de parsing XML (fichier corrompu) pour {markup_file}")
                        
    except zipfile.BadZipFile:
        print(f"Erreur : Le fichier '{input_path}' n'est pas un fichier ZIP/BCF valide.")
        
    return extracted_data

def _write_csv(output_path: Path, data: list[dict]) -> None:
    """Écrit les dictionnaires de données dans un fichier CSV formaté pour Excel."""
    if not data:
        return
        
    fieldnames = [
        'GUID', 'Title', 'TopicStatus', 'TopicType', 'Priority', 
        'CreationAuthor', 'AssignedTo', 'CreationDate', 'Description', 'CommentsCount'
    ]
    
    try:
        with open(output_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(data)
        print(f"Extraction terminée. {len(data)} sujets exportés vers '{output_path}'.")
    except IOError as e:
        print(f"Erreur système lors de l'écriture du fichier CSV : {e}")

def bcf_to_csv(input_bcf: str, output_csv: str) -> None:
    """Point d'entrée principal : Coordonne l'extraction et la sauvegarde CSV."""
    input_path = Path(input_bcf)
    output_path = Path(output_csv)
    
    if not input_path.exists():
        print(f"Erreur : Le fichier d'entrée '{input_bcf}' n'existe pas.")
        return
        
    extracted_data = _extract_bcf_data(input_path)
    if extracted_data:
        _write_csv(output_path, extracted_data)


if __name__ == "__main__":
    import sys
    
    print("--- Script de conversion BCF vers CSV ---")
    
    if len(sys.argv) == 3:
        bcf_to_csv(sys.argv[1], sys.argv[2])
    else:
        print("Usage en ligne de commande : python bcf_to_csv.py <fichier.bcf> <resultat.csv>")
        print("\nExemple d'intégration Python :")
        print("  from src.bcf_to_csv import bcf_to_csv")
        print("  bcf_to_csv('projet_maquette.bcfzip', 'export_commentaires.csv')")
        
        bcf_files = list(Path('.').glob('*.bcf')) + list(Path('.').glob('*.bcfzip'))
        
        if bcf_files:
            test_file = bcf_files[0]
            out_file = test_file.with_suffix('.csv')
            print(f"\nFichier détecté : {test_file}. Lancement de la conversion vers {out_file}.")
            bcf_to_csv(str(test_file), str(out_file))
        else:
            print("\nAucun fichier .bcf ou .bcfzip n'a été trouvé dans le répertoire courant pour une exécution automatique.")ip n'a été trouvé dans le répertoire courant pour une exécution automatique.")
