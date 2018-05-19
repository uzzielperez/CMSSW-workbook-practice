#! /usr/bin/env python

import argparse
from selection import * 

parser = argparse.ArgumentParser(description="A simple ttree plotter")
parser.add_argument("-i", "--inputfiles", dest="inputfiles", default=["ggtree_mc_GluGluHToGG_M-125.root"], nargs='*', help="List of input ggNtuplizer files")
parser.add_argument("-o", "--outputfile", dest="outputfile", default="plots.root", help="Input ggNtuplizer file")
parser.add_argument("-m", "--maxevents", dest="maxevents", type=int, default=-1, help="Maximum number events to loop over")
parser.add_argument("-t", "--ttree", dest="ttree", default="ggNtuplizer/EventTree", help="TTree Name")
args = parser.parse_args()

import numpy as np
import ROOT
import os

if os.path.isfile('~/.rootlogon.C'): ROOT.gROOT.Macro(os.path.expanduser('~/.rootlogon.C'))
ROOT.gROOT.SetBatch()
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetPalette(ROOT.kRainBow)
ROOT.gStyle.UseCurrentStyle()

# Start Timer 
sw = ROOT.TStopwatch()
sw.Start()

# Input ggNtuple
tchain = ROOT.TChain(args.ttree)
for filename in args.inputfiles: tchain.Add(filename)
print 'Total number of events: ' + str(tchain.GetEntries())

# Output file
file_out = ROOT.TFile(args.outputfile, 'recreate')

# 'Real'
h_pho_pt = ROOT.TH1D('h_pho_pt', 'Photon p_{T}', 98, 20.0, 1000.0)
h_pho_Eta = ROOT.TH1D('h_pho_Eta', 'Photon Eta', 80, -3, 3)
h_pho_Phi = ROOT.TH1D('h_pho_Phi', 'Photon Phi', 80, -3.5, 3.5)
h_pho_sigmaIEtaIEta = ROOT.TH1D('h_pho_sigmaIEtaIEta', 'Photon #sigma_{i#eta i#eta}', 100, 0.0, 0.1)

# 'Fake'
hf_pho_pt = ROOT.TH1D('hf_pho_pt', 'FPhoton p_{T}', 98, 20.0, 1000.0)
hf_pho_Eta = ROOT.TH1D('hf_pho_Eta', 'FPhoton Eta', 80, -3, 3)
hf_pho_Phi = ROOT.TH1D('hf_pho_Phi', 'FPhoton Phi', 80, -3.5, 3.5)
hf_pho_sigmaIEtaIEta = ROOT.TH1D('hf_pho_sigmaIEtaIEta', 'FPhoton #sigma_{i#eta i#eta}', 100, 0.0, 0.1)


#Loop over all the events in the input ntuple
for ievent,event in enumerate(tchain):
    if ievent > args.maxevents and args.maxevents != -1: break
    if ievent % 10000 == 0: print 'Processing entry ' + str(ievent)

    # Loop over all the photons in an event
    for i in range(event.nPho):
        if (event.phoEt[i] > 20.0 and (event.phoIDbit[i]&2==2)):
            pho_vec = ROOT.TLorentzVector()
            pho_vec.SetPtEtaPhiE(event.phoEt[i], event.phoEta[i], event.phoPhi[i], event.phoE[i])
            if not event.isData and has_mcPho_match(event, pho_vec):
                h_pho_pt.Fill(event.phoEt[i])
		h_pho_Eta.Fill(event.phoEta[i])
		h_pho_Phi.Fill(event.phoPhi[i])
                h_pho_sigmaIEtaIEta.Fill(event.phoSigmaIEtaIEtaFull5x5[i])
	    if not has_mcPho_match(event, pho_vec):
		hf_pho_pt.Fill(event.phoEt[i])
		hf_pho_Eta.Fill(event.phoEta[i])
		hf_pho_Phi.Fill(event.phoPhi[i])
                hf_pho_sigmaIEtaIEta.Fill(event.phoSigmaIEtaIEtaFull5x5[i])

file_out.Write()
file_out.Close()

sw.Stop()
print 'Real time: ' + str(round(sw.RealTime() / 60.0,2)) + ' minutes'
print 'CPU time:  ' + str(round(sw.CpuTime() / 60.0,2)) + ' minutes'
