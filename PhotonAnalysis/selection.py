#! /usr/bin/env python
import numpy as np
import ROOT
import os

# Selection Functions

# Function to check if a reconstructed photon is matched to a generator photon
# from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideCMSDataAnalysisSchoolLPC2018egamma
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






