# Contribuer à BFCtoCSV

Nous sommes ravis que vous souhaitiez contribuer à BFCtoCSV ! Toutes les contributions, qu'il s'agisse de corrections de bugs, d'améliorations de la documentation ou de nouvelles fonctionnalités, sont les bienvenues.

## Comment contribuer

1. **Signalez un bug ou proposez une fonctionnalité**
   Avant d'écrire du code, n'hésitez pas à ouvrir une *Issue* sur GitHub pour discuter de ce que vous aimeriez modifier ou ajouter.

2. **Faites un Fork du dépôt**
   Créez votre propre copie du projet sur votre compte GitHub.

3. **Créez une branche pour votre modification**
   ```bash
   git checkout -b feature/ma-nouvelle-fonctionnalite
   # ou
   git checkout -b fix/correction-bug
   ```

4. **Développez et testez**
   Assurez-vous que votre code respecte l'architecture existante (notamment le fait de s'appuyer au maximum sur la bibliothèque standard de Python, comme décrit dans `ARCHITECTURE.md`).

5. **Faites un Commit de vos changements**
   Rédigez des messages de commit clairs.
   ```bash
   git commit -m "feat: ajout du support pour telle balise BCF"
   ```

6. **Soumettez une Pull Request (PR)**
   Poussez votre branche sur votre fork et ouvrez une Pull Request vers le dépôt principal. Expliquez clairement ce que fait votre PR.

## Règles de développement
- Le code source doit rester compatible avec Python 3.10+.
- Évitez d'ajouter des dépendances externes lourdes non nécessaires (le projet tire sa force de son autonomie).
- Documentez les modifications techniques importantes dans le fichier `ARCHITECTURE.md`.

Merci de votre aide pour rendre cet outil plus utile à la communauté BIM !
