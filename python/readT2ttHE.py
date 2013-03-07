import sys
import ROOT as rt
import math
from LHEevent import *
from LHEfile import *
import plotTools

if __name__ == '__main__':

    #T2tt histograms
    MStop = rt.TH1D("MStop", "MStop", 100, 0., 2.)
    MLSP = rt.TH1D("MLSP", "MLSP", 100, 0., 2.)
    Mtop = rt.TH1D("Mtop", "Mtop", 50, 150., 200.)
    MW = rt.TH1D("MW", "MW", 50, 70., 90.)
    Mb = rt.TH1D("Mb", "Mb", 20, 0., 10.)
    MWdaug = rt.TH1D("MWdaug", "MWdaug", 50, 0., 10.)
    
    # find events in file
    myLHEfile = LHEfile(sys.argv[1])
    myLHEfile.setMax(10000)
    eventsReadIn = myLHEfile.readEvents()

    for oneEvent in eventsReadIn:
        # read the event content
        myLHEevent = LHEevent()
        myLHEevent.fillEvent(oneEvent)

        # fill topology-specific histograms (this goes in a model loop)
        if myLHEevent.Model != "T2tt":
            "The event does not correspond to T2tt"
            sys.exit()
        for i in range(0,len(myLHEevent.Particles)):
            p = myLHEevent.Particles[i]
            #print p
            # stop plots
            if abs(p['ID']) == 1000006: MStop.Fill(p['M']/myLHEevent.sMotherMass)
            if abs(p['ID']) == 6: Mtop.Fill(p['M'])
            if abs(p['ID']) == 24: MW.Fill(p['M'])
            if abs(p['ID']) == 5: Mb.Fill(p['M'])
            if abs(p['ID']) == 1000022: MLSP.Fill(p['M']/myLHEevent.LSPMass)                        
            pMother = myLHEevent.Particles[p['mIdx']]
            if abs(pMother['ID']) == 24: MWdaug.Fill(p['M'])
        del oneEvent, myLHEevent
        
    c1 = rt.TCanvas("c1", "c1", 600, 600)
    MStop.GetXaxis().SetTitle("m_{stop}/m_{stop}^{GEN}")
    MStop.Draw()
    c1.SaveAs("MStop.gif")
    MLSP.GetXaxis().SetTitle("m_{LSP}/m_{LSP}^{GEN}")
    MLSP.Draw()
    c1.SaveAs("MLSP.gif")
    Mtop.GetXaxis().SetTitle("m_{top}")
    Mtop.Draw()
    c1.SaveAs("Mtop.gif")
    MW.GetXaxis().SetTitle("m_{W}")
    MW.Draw()
    c1.SaveAs("MW.gif")
    Mb.GetXaxis().SetTitle("m_{b}")
    Mb.Draw()
    c1.SaveAs("Mb.gif")
    MWdaug.GetXaxis().SetTitle("m_{Wdaug}")
    MWdaug.Draw()
    c1.SaveAs("MWdaug.gif")

    # write the histograms
    histoFILE = rt.TFile(sys.argv[2],"RECREATE")
    MStop.Write()
    MLSP.Write()
    Mtop.Write()
    MW.Write()
    Mb.Write()
    MWdaug.Write()
    histoFILE.Close()
