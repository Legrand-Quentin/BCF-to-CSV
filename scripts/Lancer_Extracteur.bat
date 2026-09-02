@echo off
:: Se positionner à la racine du projet
cd /d "%~dp0\.."

:: Lancement de l'interface graphique sans terminal
start pythonw src\extracteur_gui.pyw
exit
