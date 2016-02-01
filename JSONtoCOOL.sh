python JSONtoCOOL_converter.py AGILEPack_December_1D_btagging.json 2> /dev/null
hadd BTagCalibRUN2-08-14_inclDL1.root BTagCalibRUN2-08-14_copy.root AGILEPack_December_1D_btagging.root 2> /dev/null

SRC_DIR=$(pwd)  # come back to this directory later
cd $HOME
source setup_TestArea.sh
cp  $SRC_DIR/BTagCalibRUN2-08-14_inclDL1.root $TestArea/.
# Associate a GUID to this file
coolHist_setFileIdentifier.sh $TestArea/BTagCalibRUN2-08-14_inclDL1.root
# Insert the calibration ROOT file into a local COOL file catalogue:
coolHist_insertFileToCatalog.py  BTagCalibRUN2-08-14_inclDL1.root  &> temp.txt
cmd=$(grep -i 'Execute'  temp.txt | sed -E 's/\Execute //g')
rm temp.txt
echo $cmd
$cmd

# Generate a local database
coolHist_setReference.py OFLP200 /GLOBAL/BTagCalib/RUN12 1 BTagCalibRUN2-08-14_inclDL1 BTagCalibRUN2-08-14_inclDL1.root

# Open it to define it's channel
expect <<EOF
spawn AtlCoolConsole.py "sqlite://;schema=mycool.db;dbname=OFLP200"
expect ">>>"
send "setchan /GLOBAL/BTagCalib/RUN12 1 RUN12\n"
expect ">>>"
send "exit\n"
expect eof
EOF

# go back to the directory we started in
cd $SRC_DIR

# cleanup
unset SRC_DIR FILE