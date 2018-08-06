import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        #'file:myfile.root'
        'file:/uscms/home/cuperez/nobackup/PhotonAnalysis/CMSSW_9_4_4/src/SMGG_TuneCUEP8M1_13TeV_pythia8_cfi_py_GEN.root'    
    )
)

process.TFileService = cms.Service("TFileService",
                fileName = cms.string("DemoDiPhotonInfo.root")
                            )


process.demo = cms.EDAnalyzer('DiPhotonAnalyzer', 
    particles = cms.InputTag("genParticles")
  )


process.p = cms.Path(process.demo)
