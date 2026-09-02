import sys
import os
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, 
                               QVBoxLayout, QWidget, QPushButton, QMessageBox)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices

# Importation du moteur d'extraction (sans dépendance externe)
from bcf_to_csv import bcf_to_csv

class DropZone(QLabel):
    """Zone de dépôt pour les fichiers BCF acceptant le glisser-déposer."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Glissez et déposez un fichier BCF ici\n(.bcf ou .bcfzip)")
        self.setAlignment(Qt.AlignCenter)
        self.set_default_style()
        self.setAcceptDrops(True)
        self.main_window = parent

    def set_default_style(self):
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaaaaa;
                border-radius: 6px;
                padding: 20px;
                background-color: #f8f9fa;
                font-size: 14px;
                color: #555555;
            }
        """)

    def set_hover_style(self):
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #0056b3;
                border-radius: 6px;
                padding: 20px;
                background-color: #e9ecef;
                font-size: 14px;
                color: #0056b3;
                font-weight: bold;
            }
        """)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().endswith(('.bcf', '.bcfzip')):
                event.acceptProposedAction()
                self.set_hover_style()
                return
        event.ignore()

    def dragLeaveEvent(self, event):
        self.set_default_style()

    def dropEvent(self, event):
        self.set_default_style()
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.main_window.process_file(file_path)

class MainWindow(QMainWindow):
    """Fenêtre principale de l'application."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Extracteur BCF vers CSV")
        self.resize(500, 320)
        self.csv_path = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Zone de glisser-déposer
        self.drop_zone = DropZone(self)
        layout.addWidget(self.drop_zone, stretch=2)

        # Label d'état
        self.status_label = QLabel("En attente d'un fichier...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #6c757d; font-size: 13px;")
        layout.addWidget(self.status_label)

        # Bouton d'ouverture (désactivé par défaut)
        self.open_button = QPushButton("Ouvrir le fichier CSV")
        self.open_button.setMinimumHeight(45)
        self.open_button.setCursor(Qt.PointingHandCursor)
        self.open_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #e9ecef;
                color: #adb5bd;
            }
        """)
        self.open_button.setEnabled(False)
        self.open_button.clicked.connect(self.open_csv)
        layout.addWidget(self.open_button)

    def process_file(self, file_path):
        """Traite le fichier BCF déposé et génère le CSV."""
        input_path = Path(file_path)
        output_path = input_path.with_suffix('.csv')
        
        self.status_label.setText("Conversion en cours...")
        self.status_label.setStyleSheet("color: #0056b3; font-size: 13px;")
        self.open_button.setEnabled(False)
        QApplication.processEvents()

        try:
            # Appel de la fonction d'extraction du noyau
            bcf_to_csv(str(input_path), str(output_path))
            
            # Vérification de la création effective
            if output_path.exists():
                self.csv_path = str(output_path)
                self.status_label.setText(f"Conversion terminée : {output_path.name}")
                self.status_label.setStyleSheet("color: #28a745; font-size: 13px; font-weight: bold;")
                self.open_button.setEnabled(True)
            else:
                raise FileNotFoundError("Le fichier de destination n'a pas pu être créé.")
                
        except Exception as e:
            self.status_label.setText("Erreur lors de la conversion.")
            self.status_label.setStyleSheet("color: #dc3545; font-size: 13px; font-weight: bold;")
            QMessageBox.critical(self, "Erreur de traitement", f"Une anomalie est survenue :\n{str(e)}")

    def open_csv(self):
        """Ouvre le fichier CSV généré avec l'application par défaut du système."""
        if self.csv_path and os.path.exists(self.csv_path):
            if os.name == 'nt':
                os.startfile(self.csv_path)
            else:
                QDesktopServices.openUrl(QUrl.fromLocalFile(self.csv_path))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
