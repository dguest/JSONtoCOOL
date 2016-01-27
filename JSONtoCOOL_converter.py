import ROOT
import sys, os
import json
from os import system 

def _run():
    inFile = sys.argv[1]
    outFile = sys.argv[2]

    _sanity_check(inFile, ".json", 1)
    _sanity_check(outFile, ".root", 2)

    #####################################################################################
    # Step 1: Create ROOT file that contains the JSON file content as TString object
    #####################################################################################
    with open(inFile,'r') as fp:
        config_str = json.load(fp)

    outHandle = ROOT.TFile.Open(inFile.replace(".json",".root"),"RECREATE")
    outHandle.mkdir("DL1/AntiKt4EMTopo")
    outHandle.mkdir("DL1/AntiKt4LCTopo")
    outHandle.cd("DL1/AntiKt4EMTopo")
    ROOT_str_name = ROOT.TObjString(str(config_str))
    ROOT_str_name.Write("net_configuration")
    outHandle.Write()
    outHandle.cd("../../DL1/AntiKt4LCTopo")
    ROOT_str_name.Write("net_configuration")
    outHandle.Write()
    outHandle.Close()
    
    #####################################################################################
    # Step 2: Merge the created ROOT file with an existing calibration ROOT file
    #####################################################################################
    system("hadd %s BTagCalibRUN2-08-14_copy.root %s" % (outFile, inFile.replace(".json",".root")))

    #####################################################################################
    # Step 3: Turn the ROOT calibration file into a local COOL DB
    #####################################################################################
    ROOTfile_path = os.path.abspath(outFile)
    # Insert the calibration ROOT file into a local COOL file catalogue:
    system("coolHist_insertFileToCatalog.py  %s &> temp.txt" % outFile)
    temp = open("temp.txt",'r')
    cmd = ""
    for line in temp:
        if "Execute" in line:
            print line
            cmd = line.split("Execute")[1]
    print ('executing cmd = ', cmd)
    system("%s" % cmd)
    system("coolHist_setReference.py OFLP200 /GLOBAL/BTagCalib/RUN12 1 %s %s " % (outFile.replace(".root",""), outFile))
    # TODO: fix this hack
    print "INSERT THIS NEXT:"
    print "setchan /GLOBAL/BTagCalib/RUN12 1 RUN12 "
    print "exit"
    system("AtlCoolConsole.py \"sqlite://;schema=mycool.db;dbname=OFLP200\" ")

def _sanity_check(file_name, string_end, n):
    if not file_name.endswith(string_end):
        print "Output file does not match expected format, please end with ", string_end
        sys.exit(n)


if __name__ == '__main__':
    _run()
