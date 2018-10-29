#! /usr/bin/env python
# From HATS exercises by Dr. Berry 
# root://cmseos.fnal.gov//store/user/drberry/HATS/makePlots.py

import argparse

import argparse
parser = argparse.ArgumentParser(description="A simple ttree plotter")
parser.add_argument("-i", "--inputfiles", dest="inputfiles", default=["ggtree_mc.root"], nargs='*', help="List of input ggNtuplizer files")
parser.add_argument("-o", "--outputfile", dest="outputfile", default="plots.root", help="Input ggNtuplizer file")
parser.add_argument("-m", "--maxevents", dest="maxevents", type=int, default=-1, help="Maximum number events to loop over")
parser.add_argument("-t", "--ttree", dest="ttree", default="ggNtuplizer/EventTree", help="TTree Name")
args = parser.parse_args()

import numpy as np
import ROOT
import os

# Function to check if a reconstructed electron is matched to a generator electron
def has_mcEle_match(event, ele_vec):
    min_delta_r = float('Inf')
    pid = 0
    for mc in range(event.nMC):
        if event.mcPt[mc] > 1.0:
            mc_vec = ROOT.TLorentzVector()
            mc_vec.SetPtEtaPhiE(event.mcPt[mc], event.mcEta[mc], event.mcPhi[mc], event.mcE[mc])
            delta_r = ele_vec.DeltaR(mc_vec)
            if delta_r < min_delta_r:
                min_delta_r = delta_r
                if delta_r < 0.3:
                    pid = abs(event.mcPID[mc])
    if pid == 11: return True
    return False

if os.path.isfile('~/.rootlogon.C'): ROOT.gROOT.Macro(os.path.expanduser('~/.rootlogon.C'))
ROOT.gROOT.SetBatch()
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetPalette(ROOT.kRainBow)
ROOT.gStyle.UseCurrentStyle()

sw = ROOT.TStopwatch()
sw.Start()

# Input ggNtuple
tchain = ROOT.TChain(args.ttree)
for filename in args.inputfiles: tchain.Add(filename)
print 'Total number of events: ' + str(tchain.GetEntries())

# Output file and any histograms we want
file_out = ROOT.TFile(args.outputfile, 'recreate')
h_elec_pt = ROOT.TH1D('h_elec_pt', 'Electron p_{T}', 98, 20.0, 1000.0)
h_elec_sigmaIEtaIEta = ROOT.TH1D('h_elec_sigmaIEtaIEta', 'Electron #sigma_{i#eta i#eta}', 100, 0.0, 0.1)
h_elec_zmass = ROOT.TH1D('h_elec_zmass', 'Z peak;Z Mass (GeV)', 70, 60.0, 130.0)

#Loop over all the events in the input ntuple
for ievent,event in enumerate(tchain):
    if ievent % 10000 == 0: print 'Processing entry ' + str(ievent)
    if ievent > args.maxevents and args.maxevents != -1: break

    # Loop over all the electrons in an event
    for i in range(event.nEle):
        if (event.elePt[i] > 20.0 and (event.eleIDbit[i]&2==2)):
            ele_vec = ROOT.TLorentzVector()
            ele_vec.SetPtEtaPhiE(event.elePt[i], event.eleEta[i], event.elePhi[i], event.eleEn[i])
            if not event.isData and has_mcEle_match(event, ele_vec):
                h_elec_pt.Fill(event.elePt[i])
                h_elec_sigmaIEtaIEta.Fill(event.eleSigmaIEtaIEtaFull5x5[i])
            else:
                h_elec_pt.Fill(event.elePt[i])
                h_elec_sigmaIEtaIEta.Fill(event.eleSigmaIEtaIEtaFull5x5[i])

    if event.nEle < 2: continue
    PassElectronSelection = True
    for i in range(2):
        if (event.eleIDbit[i]&2)!=2: PassElectronSelection = False
        if abs(event.eleEta[i]) > 2.5: PassElectronSelection = False
        if event.eleR9[i] < 0.3: PassElectronSelection = False
    lead_ele_vec = ROOT.TLorentzVector()
    lead_ele_vec.SetPtEtaPhiE(event.elePt[0], event.eleEta[0], event.elePhi[0], event.eleEn[0])
    sublead_ele_vec = ROOT.TLorentzVector()
    sublead_ele_vec.SetPtEtaPhiE(event.elePt[1], event.eleEta[1], event.elePhi[1], event.eleEn[1])
    zmass = (lead_ele_vec + sublead_ele_vec).M()
    if PassElectronSelection: h_elec_zmass.Fill(zmass)

file_out.Write()
file_out.Close()

sw.Stop()
print 'Real time: ' + str(round(sw.RealTime() / 60.0,2)) + ' minutes'
print 'CPU time:  ' + str(round(sw.CpuTime() / 60.0,2)) + ' minutes'
