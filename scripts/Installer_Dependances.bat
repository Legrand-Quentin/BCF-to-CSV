@echo off
echo ========================================================
echo   Installation des pre-requis pour l'Extracteur BCF
echo ========================================================
echo.
echo Veuillez patienter pendant le telechargement de l'interface...
echo.

:: Se positionner à la racine du projet (un dossier au-dessus du script)
cd /d "%~dp0\.."

:: Installer les dépendances
pip install -r requirements.txt

echo.
echo ========================================================
if %errorlevel% neq 0 (
    echo [ERREUR] L'installation a echoue. 
    echo Assurez-vous d'avoir bien installe Python et d'avoir 
    echo imperativement coche la case "Add Python to PATH".
) else (
    echo [SUCCES] L'interface graphique est prete !
    echo Vous pouvez desormais double-cliquer sur le fichier Lancer_Extracteur.bat
)
echo ========================================================
echo.
pause
