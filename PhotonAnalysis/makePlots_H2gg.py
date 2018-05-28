#! /usr/bin/env python

# Code from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideCMSDataAnalysisSchoolLPC2018egamma
# Command line options
import argparse
parser = argparse.ArgumentParser(description="A simple ttree plotter")
parser.add_argument("-i", "--inputfiles", dest="inputfiles", default=["ggtree_mc_GluGluHToGG_M-125.root"], nargs='*', help="List of input ggNtuplizer files")
parser.add_argument("-o", "--outputfile", dest="outputfile", default="plots.root", help="Input ggNtuplizer file")
parser.add_argument("-m", "--maxevents", dest="maxevents", type=int, default=-1, help="Maximum number events to loop over")
parser.add_argument("-t", "--ttree", dest="ttree", default="ggNtuplizer/EventTree", help="TTree Name")
args = parser.parse_args()

import numpy as np
import ROOT
import os

# Function to check if a reconstructed photon is matched to a generator photon
def has_mcPho_match(event, pho_vec):
    min_delta_r = float('Inf')
    pid = 0
    for mc in range(event.nMC):
        if event.mcPt[mc] > 1.0:
            mc_vec = ROOT.TLorentzVector()
            mc_vec.SetPtEtaPhiE(event.mcPt[mc], event.mcEta[mc], event.mcPhi[mc], event.mcE[mc])
            delta_r = pho_vec.DeltaR(mc_vec)
            if delta_r < min_delta_r:
                min_delta_r = delta_r
                if delta_r < 0.3:
                    pid = abs(event.mcPID[mc])
    if pid == 22: return True
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
h_pho_pt = ROOT.TH1D('h_pho_pt', 'Photon p_{T}', 98, 20.0, 1000.0)
h_pho_sigmaIEtaIEta = ROOT.TH1D('h_pho_sigmaIEtaIEta', 'Photon #sigma_{i#eta i#eta}', 100, 0.0, 0.1)
h_pho_higgsmass = ROOT.TH1D('h_pho_higgsmass', 'Higgs Mass peak;#gamma#gamma Mass (GeV)', 80, 80, 160.0)

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
                h_pho_sigmaIEtaIEta.Fill(event.phoSigmaIEtaIEtaFull5x5[i])
            else:
                h_pho_pt.Fill(event.phoEt[i])
                h_pho_sigmaIEtaIEta.Fill(event.phoSigmaIEtaIEtaFull5x5[i])

    if event.nPho < 2: continue
    PassPhotonSelection = True
    for i in range(2):
        if (event.phoIDbit[i]&2)!=2: PassPhotonSelection = False
        if abs(event.phoEta[i]) > 2.5: PassPhotonSelection = False
        if event.phoR9[i] < 0.75: PassPhotonSelection = False
    lead_pho_vec = ROOT.TLorentzVector()
    lead_pho_vec.SetPtEtaPhiE(event.phoEt[0], event.phoEta[0], event.phoPhi[0], event.phoE[0])
    sublead_pho_vec = ROOT.TLorentzVector()
    sublead_pho_vec.SetPtEtaPhiE(event.phoEt[1], event.phoEta[1], event.phoPhi[1], event.phoE[1])
    higgsmass = (lead_pho_vec + sublead_pho_vec).M()
    if PassPhotonSelection: h_pho_higgsmass.Fill(higgsmass)

file_out.Write()
file_out.Close()

sw.Stop()
print 'Real time: ' + str(round(sw.RealTime() / 60.0,2)) + ' minutes'
print 'CPU time:  ' + str(round(sw.CpuTime() / 60.0,2)) + ' minutes'
