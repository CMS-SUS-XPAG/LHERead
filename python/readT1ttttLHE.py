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
        if myLHEevent.Model != "T1tttt":
            "The event does not correspond to T1tttt"
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
            if abs(p['ID']) == 6: Mtop.Fill(p['M'])
            if abs(p['ID']) == 24: MW.Fill(p['M'])
            if abs(p['ID']) == 5: Mb.Fill(p['M'])
            if abs(p['ID']) == 1000022: MLSP.Fill(p['M']/myLHEevent.LSPMass)                        
            pMother = myLHEevent.Particles[p['mIdx']]
            if abs(pMother['ID']) == 24: MWdaug.Fill(p['M'])
        del oneEvent, myLHEevent
        
    # write the histograms
    histoFILE = rt.TFile(sys.argv[2],"RECREATE")
    DalitzGluino.Write()
    MGluino.Write()
    MLSP.Write()
    Mtop.Write()
    MW.Write()
    Mb.Write()
    MWdaug.Write()
    histoFILE.Close()
    
