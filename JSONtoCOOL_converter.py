import ROOT
import sys
import json

def _run():
    inFile = sys.argv[1]
    outFile = sys.argv[2]

    _sanity_check(inFile, ".json", 1)
    _sanity_check(outFile, ".root", 2)

    outHandle = ROOT.TFile.Open(outFile,"RECREATE")
    outHandle.mkdir("DL1/AntiKt4EMTopo")
    outHandle.cd("DL1/AntiKt4EMTopo")

    with open(inFile,'r') as fp:
        config_str = json.load(fp)

    ROOT_str_name = ROOT.TObjString(str(config_str))
    ROOT_str_name.Write("net_configuration")
    outHandle.Write()
    outHandle.Close()

def _sanity_check(file_name, string_end, n):
    if not file_name.endswith(string_end):
        print "Output file does not match expected format, please end with ", string_end
        sys.exit(n)

if __name__ == '__main__':
    _run()
