# lep_pt = transverse momentum of the lepton,
# lep_eta = pseudo-rapidity of the lepton,
# lep_phi = azimuthal angle of the lepton,
# lep_E = energy of the lepton

import ROOT
from ROOT import TLegend, kRed, kBlue
import math

## 2lep 13 Tev sample
a = ROOT.TFile.Open("https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/2lep/Data/data_B.2lep.root")

#Creating canvas
canvas1 = ROOT.TCanvas("Canvas1","Title",800,600)
canvas2 = ROOT.TCanvas("Canvas2","Title",800,600)

#Getting the data from the .root file
tree = a.Get("mini")
tree.GetEntries()
print('Entries: ' + str(tree.GetEntries()))

#Defining the histograms
bins = 200
mini = 0
maxi = 200
hist1 = ROOT.TH1F("Mass Z Boson", "; mass [GeV]; events", bins, mini, maxi)
hist2 = ROOT.TH1F("Mass Z Boson 2", "; mass [GeV]; events", bins, mini, maxi)

#Lead and trail lepton as Lorentz Vectors
leadLepton  = ROOT.TLorentzVector()
trailLepton = ROOT.TLorentzVector()

#Functions
def InvMass_Hist(hist):  #Calculatng, returning and filling the histogram with the invariant mass
    leadLepton.SetPtEtaPhiE(tree.lep_pt[0]/1000., tree.lep_eta[0], tree.lep_phi[0], tree.lep_E[0]/1000.) # Define one TLorentz vector for each lepton; two vectors (devide by 1000 to get value in GeV)
    trailLepton.SetPtEtaPhiE(tree.lep_pt[1]/1000., tree.lep_eta[1], tree.lep_phi[1], tree.lep_E[1]/1000.)
    invmass = leadLepton + trailLepton  # Addition of two TLorentz vectors above
    if 0 < invmass.M() < 200:
        hist.Fill(invmass.M())  #Filling the histogram if the calculated mass is relevant

def Selection_cuts_Hist(T_low, T_high, Eta_low, Eta_high, Phi_low, hist_var):
    if (tree.lep_n >= 2 and tree.lep_charge[0] != tree.lep_charge[1] and tree.lep_type[0] == tree.lep_type[1]):  #Base conditions
        if (T_low*1000 < tree.lep_pt[0] < T_high*1000 and T_low*1000 < tree.lep_pt[1] < T_high*1000):  #Transverse momentum in GeV
            if (Eta_low < tree.lep_eta[0] < Eta_high and Eta_low < tree.lep_eta[1] < Eta_high):  #Pseudorapidity
                if (Phi_low < tree.lep_phi[0] and Phi_low < tree.lep_phi[1]):  #Azimuthal angle
                    InvMass_Hist(hist_var)

#Breit-Wigner and background function with Gaussian deviation
XLow = 80 #Lower edge for curve fitting
XUp = 100 #Upper edge for curve fitting

Fit = ROOT.TF1("Fit", "[0]*TMath::BreitWigner(x,[1],[2]) + gaus", XLow, XUp) #Predifined Breit-Wigner function
Fit.SetParameters(4000, 90.11, 3.386) #Setting some base parameters
Fit.Save(XLow, XUp, 0, 0, 0, 0) #Setting the interval for fitting

def hist_draw(hist, canvas, color):
    hist.Fit('Fit', "R", "", XLow, XUp) #R or S
    hist.SetFillStyle(3003)
    hist.SetFillColor(color)
    Fit.SetLineColor(kRed)
    hist.Draw()
    canvas.Draw() #Draws the histogram

print('Histogram 1:')

#Event loop
n=0
for event in tree:
    n += 1
    if(n%100000==0):
        print(n)
    Selection_cuts_Hist(0, 150, -1, 1, 0, hist1)

print('Histogram 2:')

n=0
for event in tree:
    n += 1
    if(n%100000==0):
        print(n)
    Selection_cuts_Hist(30, 60, -1, 1, 0, hist2)

    
hist_draw(hist1, canvas1, 4)
hist_draw(hist2, canvas2, 4)
