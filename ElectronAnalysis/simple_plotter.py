#!/usr/bin/python
import ROOT
from ROOT import TClass,TKey, TIter,TCanvas, TPad,TFile, TPaveText, TColor, TGaxis, TH1F, TPad, TH1D, TLegend
from ROOT import kBlack, kBlue, kRed
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
ttree  = tfile.Get(args.ttree)
ttree.SetLineColor(kBlack) 
ttree.SetLineWidth(2)
ttree.Draw("elePt")

ttreepT20 = ttree.CopyTree("elePt>20")
ttreepT20.SetLineColor(kRed)
ttreepT20.SetLineWidth(3)
ttreepT20.Draw("elePt","elePt>20", "same")

xpos1, ypos1, xpos2, ypos2 = .50, 0.78, .85, .88
leg = TLegend(xpos1, ypos1, xpos2, ypos2)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.AddEntry(ttree, "Pt>0", "l")
leg.AddEntry(ttreepT20, "Pt>20", "l")
leg.Draw()
 
canvas.Update()
canvas.Draw()
canvas.Print("Electron_%s.pdf" %("study"))
canvas.SetLogy()
canvas.Update()
canvas.Draw()
canvas.Print("LOGElectronPlots_%s.pdf" %("study"))
