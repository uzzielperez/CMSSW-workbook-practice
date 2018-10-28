#!/usr/bin/python
import ROOT
from ROOT import TClass,TKey, TIter,TCanvas, TPad,TFile, TPaveText, TColor, TGaxis, TH1F, TPad, TH1D, TLegend
from ROOT import kBlack, kBlue, kRed, kGreen
from ROOT import gBenchmark, gStyle, gROOT, gDirectory
import re
import sys
import argparse
import copy

# Command line options
parser = argparse.ArgumentParser(description="")
parser.add_argument("-i", "--infile", default="ggtree_mc.root", help="Input file")
parser.add_argument("-t", "--ttree", default="ggNtuplizer/EventTree", help="Tree name. Default for ggNtuplizer out put is ggNtuplizer/EventTree")
args = parser.parse_args()

gStyle.SetOptStat(0)
canvas = ROOT.TCanvas("Plots","Plots", 800, 800)
tfile = ROOT.TFile.Open(args.infile)

var = "elePt"
#var = "eleSigmaIEtaIEtaFull5x5"

ttree  = tfile.Get(args.ttree)
ttree.SetLineColor(kBlack) 
ttree.SetLineWidth(2)
ttree.Draw(var)

ttreeIDbit2 = ttree.CopyTree("(eleIDbit & 2)== 2")
ttreeIDbit2.SetLineColor(kRed)
ttreeIDbit2.SetLineWidth(3)
ttreeIDbit2.Draw(var,"(eleIDbit & 2)== 2", "same")

ttreeIDbit4 = ttree.CopyTree("(eleIDbit & 4)== 4")
ttreeIDbit4.SetLineColor(kBlue)
ttreeIDbit4.SetLineWidth(3)
ttreeIDbit4.Draw(var,"(eleIDbit & 4)== 4", "same")

ttreeIDbit8 = ttree.CopyTree("(eleIDbit & 8)== 8")
ttreeIDbit8.SetLineColor(kGreen)
ttreeIDbit8.SetLineWidth(3)
ttreeIDbit8.Draw(var,"(eleIDbit & 8)== 8", "same")

xpos1, ypos1, xpos2, ypos2 = .50, 0.78, .85, .88
leg = TLegend(xpos1, ypos1, xpos2, ypos2)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.AddEntry(ttree, "nocut", "l")
leg.AddEntry(ttreeIDbit2, "eleIDbit=2", "l")
leg.AddEntry(ttreeIDbit4, "eleIDbit=4", "l")
leg.AddEntry(ttreeIDbit8, "eleIDbit=8", "l")
leg.Draw()
 
canvas.Update()
canvas.Draw()
canvas.Print("Electron_%s.pdf" %(var))
canvas.SetLogy()
canvas.Update()
canvas.Draw()
canvas.Print("LOGElectronPlots_%s.pdf" %(var))
