import ROOT
import sys
import json

def _run():
    inFile = sys.argv[1]

    # Check the input format matches expectation (JSON)
    # TODO: The input file should be a text file (JSON, YAML, whatever...). sanity check will be changed to make sure it's not a ROOT file.
    _sanity_check(inFile, ".json", 1)

    with open(inFile,'r') as fp:
        config_str = json.load(fp)

    outHandle = ROOT.TFile.Open(inFile.replace(".json",".root"),"RECREATE")
    outHandle.mkdir("DL1/AntiKt4EMTopo")
    outHandle.mkdir("DL1/AntiKt4LCTopo")
    outHandle.cd("DL1/AntiKt4EMTopo")
    ROOT_str_name = ROOT.TObjString(str(config_str))
    ROOT_str_name.Write("net_configuration")
    outHandle.Write()
    outHandle.cd("/DL1/AntiKt4LCTopo")
    ROOT_str_name.Write("net_configuration")
    outHandle.Write()
    outHandle.Close()

def _sanity_check(file_name, string_end, n):
    if not file_name.endswith(string_end):
        raise NameError("Input file does not match expected format, please end with ", string_end)
        sys.exit(n)


if __name__ == '__main__':
    _run()
