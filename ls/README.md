# ls

Directory listing of ftp.bom.gov.au

```sh
lftp -u anonymous, -e 'find /;bye' ftp2.bom.gov.au > bom.txt
wc-l bom.txt
# 595586
```

Extract the folders only from the listing:

```sh
grep '/$' bom.txt > bom-dir.txt
wc -l bom-dir.txt
# 4403 bom-dir.txt
```

```sh
echo "ls -l /anon/;bye" | lftp -u anonymous, ftp2.bom.gov.au
```

