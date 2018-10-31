#! /usr/bin/env python
import re
import argparse
parser = argparse.ArgumentParser(description="A simple ttree plotter")
parser.add_argument("-f", "--filelist", dest="filelist", default=["plots_loose.root", "plots_tight.root"], nargs='*', help="List of input ROOT files")
parser.add_argument("-o", "--options", dest="options", default="norm", help="Cuts placed on TTree")
parser.add_argument("-v", "--variable", dest="variable", default=["zmass"], nargs='*', help="Variable to plot")
parser.add_argument("-l", "--legend", dest="legend", default=r'plots_([^(]*).root', help="Legend label pattern")
parser.add_argument("-x", "--cuts", dest="cuts", default="", help="Cuts placed on TTree")
args = parser.parse_args()

import ROOT
from ROOT import TLegend
ROOT.gROOT.SetBatch()
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetPalette(ROOT.kRainBow)
ROOT.gStyle.UseCurrentStyle()

can = ROOT.TCanvas("Plots","Plots", 800,800)
tfiles = []

xpos1, ypos1, xpos2, ypos2 = .50, 0.78, .85, .88

for infile in args.filelist:
	print infile 
	tfiles.append(ROOT.TFile.Open(infile))

#var = "h_elec_pt"
#var = "h_elec_sigmaIEtaIEta"
var = "h_elec_zmass"
#var = "h_elec_%s" %(args.variable[0])
hists = []

leg = TLegend(xpos1, ypos1, xpos2, ypos2)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)

pattern = r'plots_([^(]*).root'
print args.legend
i = 0
for tfile in tfiles:
	hist = tfile.Get(var)
	hist.SetLineColor(i+1)
	hist.Draw("same")	
	leg.AddEntry(hist, "%s" %(re.findall(pattern, args.filelist[i])[0]) ,"l")
	i = i + 1 

leg.Draw()
can.Update()
can.Draw()
can.Print("Electron_%s.pdf" %(var))
