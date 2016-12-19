`find . -type f -name "* *.png" -exec bash -c 'mv "$0" "${0// /_}"' {} \;`
for file in *.png
do
    mkdir -p ${file:0:26}
    mv $file ${file:0:26}
done
