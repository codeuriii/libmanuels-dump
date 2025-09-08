# Libmanuels Dump
Install required dependecies using
```bash
pip install -r requirements.txt
```
Dump your libmanuels with running libmanuels.py, follow the instructions and that's it  
Also you can use the script with arguments `--edition`, `--id` et `--no-delete`.
```bash
py libmanuels.py --edition Magnard --id 9782210783133 --no-delete
```
- edition: the manuel's edition (case sensitive)
- id: the manuel's id
- no-delete: essentialy for debugging, don't delete the temporary files when you hit Ctrl+C