echo "/!\ not yet tested /!\"
echo "you need to set env SSHPASS before on your local machine"
echo "export SSHPASS=xxxxxxx"
echo "--------------------------------------------------------"
echo ""
sshpass -V
sshpass -e scp -o stricthostkeychecking=no -r 6c4nf_cd@6c4nf.ftp.infomaniak.com:/home/clients/4d2bacdb41356fc6dce1c18e19077c30/sites/curatedadventures.club/content tmp_content
echo "content folder downloaded"
zip -r content_backup.zip tmp_content
rm -R tmp_content
echo "content backup zipped"
git commit content_backup.zip -m "content_backup"
git push
echo "content backup commited & pushed"
