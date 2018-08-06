// -*- C++ -*-
//
// Package:    Analyses/DiPhotonAnalyzer
// Class:      DiPhotonAnalyzer
// 
/**\class DiPhotonAnalyzer DiPhotonAnalyzer.cc Analyses/DiPhotonAnalyzer/plugins/DiPhotonAnalyzer.cc

 Description: Basic GEN only analyzer
 Implementation:
      Accesses MC level genParticle information. Outputs kinematic photon information,
      pt, eta, phi, Diphoton invariant mass, and photon pair momentum. 
*/
//
// Original Author:  Cilicia Uzziel Perez
//         Created:  Tue, 08 May 2018 00:41:08 GMT
//
//

using namespace std; 
// system include files
#include <memory>
#include <vector>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

// Misc.
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

//TFileService
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

//for the GenParticleCollection and GenParticles
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include <vector>
#include "TLorentzVector.h"
#include "TH2D.h"
#include "TTree.h"



//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<> and also remove the line from
// constructor "usesResource("TFileService");"
// This will improve performance in multithreaded jobs.

class DiPhotonAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit DiPhotonAnalyzer(const edm::ParameterSet&);
      ~DiPhotonAnalyzer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      // ----------member data ---------------------------
      edm::Service<TFileService> fs;
      edm::EDGetTokenT<vector<reco::GenParticle> > genParticlesToken_;
      edm::InputTag genParticles_;
      edm::InputTag particles_;

       TTree *fgenTree;
      //Structs
      struct eventInfo_t {
      Long64_t run;
      Long64_t LS;
      Long64_t evnum;
      };
      eventInfo_t fEventInfo; //ExoDiPhotons::eventInfo_t fEventInfo;
   
      struct genPhotonInfo_t{
        double pt; 
        double eta; 
        double phi;
        double E;
       }; 

      genPhotonInfo_t fSignalPhoton1;
      genPhotonInfo_t fSignalPhoton2; 
    
     struct genDiPhotonInfo_t{
        //kinematics 
        double Minv; 
        double qt; 
      }; 
    
      genDiPhotonInfo_t fSignalDiPhoton;    
      int numPhotons = 0;
};

// constants, enums and typedefs

// static data member definitions

// constructors and destructor
DiPhotonAnalyzer::DiPhotonAnalyzer(const edm::ParameterSet& iConfig)

{
   //now do what ever initialization is needed
   usesResource("TFileService");
   fgenTree = fs->make<TTree>("fgenTree","GENDiphotonTree");
    
   fgenTree->Branch("genPhoton1", &fSignalPhoton1, "pt/D:eta:phi:E");
   fgenTree->Branch("genPhoton2", &fSignalPhoton2, "pt/D:eta:phi:E");
   fgenTree->Branch("genDiPhoton", &fSignalDiPhoton, "Minv/D:qt");
   
   genParticlesToken_ = consumes<vector<reco::GenParticle>>(iConfig.getParameter<edm::InputTag>("particles"));
}


DiPhotonAnalyzer::~DiPhotonAnalyzer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
DiPhotonAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   using namespace std;
   
   //Init available in ExoDiphotons but do manual initialization here
  fEventInfo.run = -99999.99;
  fEventInfo.LS = -99999.99;
  fEventInfo.evnum = -99999.99;

  //Accessing GenParticles from the event. reco::GenParticleCollection is typedef for vector<reco::GenParticle>
  edm::Handle<vector<reco::GenParticle> > genParticles;
  iEvent.getByToken(genParticlesToken_,genParticles);
  
  if(!genParticles.isValid()) {
         cout << "No Gen Particles collection!" << endl;
         return;
  }

  fSignalPhoton1.pt = -99999.99;
  fSignalPhoton1.eta = -99999.99;
  fSignalPhoton1.phi = -99999.99;
  fSignalPhoton1.E = -99999.99;

  fSignalPhoton2.pt = -99999.99;
  fSignalPhoton2.eta = -99999.99;
  fSignalPhoton2.phi = -99999.99;
  fSignalPhoton2.E = -99999.99;

  fSignalDiPhoton.Minv = -99999.99;
  fSignalDiPhoton.qt = -99999.99;

  int photoncount = 0; 
  
  for(vector<reco::GenParticle>::const_iterator ip = genParticles->begin(); ip != genParticles->end(); ++ip){
      if(ip->status()==1 && ip->pdgId()==22){
         //cout << "Photon end state found" << endl;
        photoncount = photoncount + 1;
        double pt = ip->pt();
        double eta = ip->eta();
        double phi = ip->phi();
        double E = ip->energy();

        //Ordering photons
        if (pt > fSignalPhoton1.pt){
            fSignalPhoton2.pt = fSignalPhoton1.pt;
            fSignalPhoton2.eta = fSignalPhoton1.eta;
            fSignalPhoton2.phi = fSignalPhoton1.phi;
            fSignalPhoton2.E = fSignalPhoton1.E;
            
            fSignalPhoton1.pt = pt;
            fSignalPhoton1.eta = eta;
            fSignalPhoton1.phi = phi;
            fSignalPhoton1.E = E;
        }      
        if ((pt < fSignalPhoton1.pt) && (pt > fSignalPhoton2.pt)){
            fSignalPhoton2.pt = pt;
            fSignalPhoton2.eta = eta;
            fSignalPhoton2.phi = phi;
            fSignalPhoton2.E = E;
        }
      }//end photon end state condition
  }//end loop over gen particles 
  cout << "Number of photons in event: " << photoncount << endl;
  //Apply cuts offline
   
  //Fill DiPhoton Information
  TLorentzVector leadingPhoton, subleadingPhoton;
  leadingPhoton.SetPtEtaPhiE(fSignalPhoton1.pt, fSignalPhoton1.eta, fSignalPhoton1.phi, fSignalPhoton1.E);
  subleadingPhoton.SetPtEtaPhiE(fSignalPhoton2.pt, fSignalPhoton2.eta, fSignalPhoton2.phi, fSignalPhoton2.E);
  
   TLorentzVector total = leadingPhoton + subleadingPhoton;
   double ggmass = total.M();

   fSignalDiPhoton.Minv = ggmass;
   fSignalDiPhoton.qt = total.Pt();

   //Fill the tree Branches 
   fgenTree->Fill(); 


#ifdef THIS_IS_AN_EVENT_EXAMPLE
   Handle<ExampleData> pIn;
   iEvent.getByLabel("example",pIn);
#endif
   
#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
#endif
}


// ------------ method called once each job just before starting event loop  ------------
void 
DiPhotonAnalyzer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
DiPhotonAnalyzer::endJob() 
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
DiPhotonAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(DiPhotonAnalyzer);
