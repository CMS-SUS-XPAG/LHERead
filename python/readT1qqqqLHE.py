import sys
import ROOT as rt
import math
from LHEevent import *
from LHEfile import *
import plotTools

if __name__ == '__main__':

    #T1tttt histograms
    DalitzGluino = rt.TH2D("DalitzGluino", "DalitzGluino",100, 0., 1., 100, 0., 1.)
    MGluino = rt.TH1D("MGluino", "MGluino", 100, 0., 2.)
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
        if myLHEevent.Model != "T1qqqq":
            "The event does not correspond to T1qqqq"
            sys.exit()
        for i in range(0,len(myLHEevent.Particles)):
            p = myLHEevent.Particles[i]
            #print p
            # gluino plots
            if abs(p['ID']) == 1000021:
                MGluino.Fill(p['M']/myLHEevent.sMotherMass)
                # find daughters
                gluinoDaugh = []
                for q in myLHEevent.Particles:
                    if q['mIdx'] == i: gluinoDaugh.append(q)
                if len(gluinoDaugh) != 3:
                    print "TOO MANY/FEW GLUINO DAUGHTERS (3 expected, %i found)" %len(gluinoDaugh)
                    sys.exit() 
                DalitzGluino.Fill(plotTools.InvariantMassSq(gluinoDaugh[0],gluinoDaugh[1])/math.pow(myLHEevent.sMotherMass,2.),
                               plotTools.InvariantMassSq(gluinoDaugh[0],gluinoDaugh[2])/math.pow(myLHEevent.sMotherMass,2.))
            # other plots
            if abs(p['ID']) == 1000022: MLSP.Fill(p['M']/myLHEevent.LSPMass)                        
        del oneEvent, myLHEevent
        
    c1 = rt.TCanvas("c1", "c1", 600, 600)
    DalitzGluino.GetXaxis().SetTitle("m_{LSP,b1}^{2}")
    DalitzGluino.GetYaxis().SetTitle("m_{LSP,b2}^{2}")
    DalitzGluino.Draw("COLZ")
    c1.SaveAs("DalitzGluino.gif")
    MGluino.GetXaxis().SetTitle("m_{gluino}/m_{gluino}^{GEN}")
    MGluino.Draw()
    c1.SaveAs("MGluino.gif")
    MLSP.GetXaxis().SetTitle("m_{LSP}/m_{LSP}^{GEN}")
    MLSP.Draw()
    c1.SaveAs("MLSP.gif")

    # write the histograms
    histoFILE = rt.TFile(sys.argv[2],"RECREATE")
    DalitzGluino.Write()
    MGluino.Write()
    MLSP.Write()
    histoFILE.Close()
    
