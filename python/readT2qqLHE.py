import sys
import ROOT as rt
import math
from LHEevent import *
from LHEfile import *
import plotTools

if __name__ == '__main__':

    #T2qq histograms
    MSquark = rt.TH1D("MSquark", "MSquark", 100, 0., 2.)
    MLSP = rt.TH1D("MLSP", "MLSP", 100, 0., 2.)
    
    # find events in file
    myLHEfile = LHEfile(sys.argv[1])
    myLHEfile.setMax(10000)
    eventsReadIn = myLHEfile.readEvents()

    for oneEvent in eventsReadIn:
        # read the event content
        myLHEevent = LHEevent()
        myLHEevent.fillEvent(oneEvent)

        # fill topology-specific histograms (this goes in a model loop)
        if myLHEevent.Model != "T2qq":
            "The event does not correspond to T2qq"
            sys.exit()
        for i in range(0,len(myLHEevent.Particles)):
            p = myLHEevent.Particles[i]
            #print p
            # squark plots
            if ((abs(p['ID']) >= 1000001 and abs(p['ID']) <= 1000006) or (abs(p['ID']) >= 2000001 and abs(p['ID']) <= 2000006)):
                MSquark.Fill(p['M']/myLHEevent.sMotherMass)
            # other plots
            if abs(p['ID']) == 1000022: MLSP.Fill(p['M']/myLHEevent.LSPMass)                        
        del oneEvent, myLHEevent
        
    c1 = rt.TCanvas("c1", "c1", 600, 600)
    MSquark.GetXaxis().SetTitle("m_{squark}/m_{squark}^{GEN}")
    MSquark.Draw()
    c1.SaveAs("MSquark.gif")
    MLSP.GetXaxis().SetTitle("m_{LSP}/m_{LSP}^{GEN}")
    MLSP.Draw()
    c1.SaveAs("MLSP.gif")

    # write the histograms
    histoFILE = rt.TFile(sys.argv[2],"RECREATE")
    MSquark.Write()
    MLSP.Write()
    histoFILE.Close()
    
